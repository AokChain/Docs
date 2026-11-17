"""Finding the pages and reading their front matter.

A page is pages/<section id>/<slug>.md and starts with YAML front matter:

    ---
    title: Offline staking
    description: Let another node stake your coins while they stay in your wallet.
    order: 3
    aliases: [staking]                  # optional: old slugs that redirect here
    generated_by: tools/rpc_reference.py   # optional: generated pages
    ---
"""
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import checks
from .config import SLUG

FRONT = re.compile(r"\A---[ \t]*\n(.*?\n)?---[ \t]*(?:\n|\Z)", re.S)
KEYS = ("title", "description", "order", "aliases", "generated_by")
TITLE_MAX = 80
DESCRIPTION_MAX = 160
# Addresses the wiki itself uses; no page or alias can take them.
RESERVED = {"all-pages", "recent-changes", "sections", "assets", "search", "index", "404"}


@dataclass
class Page:
    slug: str
    section: object
    path: Path
    label: str              # the path shown in messages
    title: str
    description: str
    order: int
    aliases: list
    generated_by: str
    body: str
    body_line: int          # line number of the first body line in the file
    url: str = ""
    repo: Path = None       # git top level of the file, if any
    repo_path: str = ""     # path of the file inside that repository
    parsed: object = None
    html: str = ""
    updated: str = ""       # YYYY-MM-DD
    links_to: set = field(default_factory=set)
    backlinks: list = field(default_factory=list)


def _label(path):
    try:
        rel = os.path.relpath(path)
    except ValueError:
        return str(path)
    return str(path) if rel.startswith("..") else rel


ADDRESS = re.compile(r"@@([a-z_]+)@@")


def addresses(cfg):
    """What a page may write between @@ and @@: the addresses of wiki.yml."""
    host = lambda url: re.sub(r"^https?://", "", url).split("/")[0]
    return {"site": cfg.site, "site_host": host(cfg.site), "explorer": cfg.explorer,
            "explorer_host": host(cfg.explorer), "api": cfg.api, "github": cfg.github}


def read_page(path, section, errors, names=None):
    label = _label(path)
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"{label}: not UTF-8 text")
        return None
    raw = raw.lstrip("﻿").replace("\r\n", "\n")
    if names is not None:
        for unknown in sorted(set(ADDRESS.findall(raw)) - set(names)):
            errors.append(f"{label}: @@{unknown}@@ is not an address of wiki.yml ({', '.join(sorted(names))})")
        raw = ADDRESS.sub(lambda m: names.get(m.group(1), m.group(0)), raw)
    errors.extend(checks.file_problems(raw, label))

    slug = path.stem
    if not SLUG.match(slug):
        errors.append(f"{label}: file name {path.name!r}: slugs are lowercase words joined by hyphens")
    m = FRONT.match(raw)
    if not m:
        errors.append(f"{label}:1: no front matter: start the file with --- title, description, order ---")
        return None
    try:
        meta = yaml.safe_load(m.group(1) or "") or {}
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        line = (mark.line + 2) if mark else 1
        hint = ""
        if "mapping values are not allowed" in str(e) and mark:
            bad = (m.group(1) or "").splitlines()[mark.line]
            key, _, value = bad.partition(":")
            hint = f": a value with ': ' in it needs quotes, {key.strip()}: \"{value.strip()}\""
        errors.append(f"{label}:{line}: front matter is not valid YAML{hint or ': ' + str(e).splitlines()[0]}")
        return None
    if not isinstance(meta, dict):
        errors.append(f"{label}:1: front matter must be key: value lines")
        return None

    bad = len(errors)
    for key in sorted(set(meta) - set(KEYS)):
        errors.append(f"{label}: unknown front matter field {key!r} (fields: {', '.join(KEYS)})")
    title = meta.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append(f"{label}: front matter: title is missing")
    elif len(title.strip()) > TITLE_MAX:
        errors.append(f"{label}: front matter: title has {len(title.strip())} characters, at most {TITLE_MAX}")
    desc = meta.get("description")
    if not isinstance(desc, str) or not desc.strip():
        errors.append(f"{label}: front matter: description is missing (one sentence)")
    else:
        desc = " ".join(desc.split())
        if len(desc) > DESCRIPTION_MAX:
            errors.append(f"{label}: front matter: description has {len(desc)} characters, "
                          f"at most {DESCRIPTION_MAX}")
    order = meta.get("order")
    if not isinstance(order, int) or isinstance(order, bool):
        errors.append(f"{label}: front matter: order must be a whole number (the position in its section)")
    aliases = meta.get("aliases") or []
    if isinstance(aliases, str):
        aliases = [aliases]
    if not isinstance(aliases, list) or not all(isinstance(a, str) for a in aliases):
        errors.append(f"{label}: front matter: aliases must be a list of old slugs")
        aliases = []
    for a in aliases:
        if not SLUG.match(a):
            errors.append(f"{label}: front matter: alias {a!r} is not a lowercase-hyphen slug")
    gen = meta.get("generated_by") or ""
    if not isinstance(gen, str):
        errors.append(f"{label}: front matter: generated_by must be a path, such as tools/rpc_reference.py")
        gen = ""
    if len(errors) > bad:
        return None

    return Page(
        slug=slug, section=section, path=path, label=label,
        title=title.strip(), description=desc, order=order, aliases=list(aliases),
        generated_by=gen.strip(), body=raw[m.end():], body_line=raw[:m.end()].count("\n") + 1,
    )


def load(dirs, cfg, errors):
    """Every page in the given pages directories, and the number of files
    that could not be read as pages (their problems are in errors)."""
    pages, failed = [], 0
    for d in dirs:
        d = Path(d).resolve()
        if not d.is_dir():
            errors.append(f"{_label(d)}: no such pages directory")
            continue
        for entry in sorted(d.iterdir()):
            if entry.name.startswith("."):
                continue
            if not entry.is_dir():
                errors.append(f"{_label(entry)}: pages go in a section folder, pages/<section id>/<slug>.md")
                continue
            section = cfg.section(entry.name)
            if section is None:
                errors.append(f"{_label(entry)}: no section {entry.name!r} in sections.yml")
                continue
            for f in sorted(entry.iterdir()):
                if f.name.startswith("."):
                    continue
                if f.is_dir() or f.suffix != ".md":
                    errors.append(f"{_label(f)}: only .md pages go in pages/ (images go in assets/img/)")
                    continue
                page = read_page(f, section, errors, addresses(cfg))
                if page:
                    pages.append(page)
                else:
                    failed += 1
    return pages, failed


def index(pages, errors):
    """Slug and alias lookups; duplicates and reserved names are errors."""
    by_slug, aliases = {}, {}
    for p in pages:
        if p.slug in RESERVED:
            errors.append(f"{p.label}: the slug {p.slug!r} is used by the wiki itself, pick another")
        elif p.slug in by_slug:
            errors.append(f"{p.label}: slug {p.slug!r} is already used by {by_slug[p.slug].label}")
        else:
            by_slug[p.slug] = p
    for p in pages:
        for a in p.aliases:
            if a in RESERVED:
                errors.append(f"{p.label}: alias {a!r} is used by the wiki itself")
            elif a == p.slug:
                errors.append(f"{p.label}: alias {a!r} is the page's own slug; leave it out")
            elif a in by_slug:
                errors.append(f"{p.label}: alias {a!r} is the slug of {by_slug[a].label}")
            elif a in aliases:
                errors.append(f"{p.label}: alias {a!r} is already an alias of {aliases[a].label}")
            else:
                aliases[a] = p
    return by_slug, aliases
