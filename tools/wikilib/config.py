"""Settings (wiki.yml) and sections (sections.yml)."""
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
THEME = ROOT / "theme"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class BuildError(Exception):
    """One or more problems; the build stops and prints all of them."""

    def __init__(self, messages):
        self.messages = list(messages)
        super().__init__("\n".join(self.messages))


@dataclass
class Section:
    id: str
    title: str
    summary: str
    icon: str
    url: str = ""
    pages: list = field(default_factory=list)


@dataclass
class Config:
    root: Path
    name: str
    base: str
    site_url: str
    repo: str
    branch: str
    noindex: bool
    generated_from: str
    site: str               # the website, without a slash at the end
    explorer: str
    api: str                # the API's base address
    github: str
    menu: list
    footer: list
    sections: list

    def section(self, section_id):
        for s in self.sections:
            if s.id == section_id:
                return s
        return None


def _read_yaml(path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise BuildError([f"{path.name}: missing"]) from None
    except yaml.YAMLError as e:
        raise BuildError([f"{path.name}: not valid YAML: {e}"]) from None


def load(root=ROOT, base=None, launch=False):
    """launch: the values of the `launch` mapping of wiki.yml take the place of
    the ones of the test period (the addresses, noindex)."""
    errors = []
    wiki = _read_yaml(root / "wiki.yml") or {}
    launch_values = wiki.pop("launch", None) or {}
    if launch:
        if not isinstance(launch_values, dict) or not launch_values:
            errors.append("wiki.yml: --launch needs a launch mapping")
        else:
            wiki.update(launch_values)
    raw_sections = _read_yaml(root / "sections.yml") or []

    base = base or wiki.get("base") or "/"
    if not (base.startswith("/") and base.endswith("/")):
        errors.append(f"base {base!r}: must start and end with /")
    services = {}
    for key in ("site", "explorer", "api", "github"):
        value = str(wiki.get(key) or "").rstrip("/")
        if not value.startswith(("https://", "http://")):
            errors.append(f"wiki.yml: {key} must be an address (https://...)")
        services[key] = value
    # Under a base such as /doc/ the wiki is part of the website
    site_urls = wiki.get("site_url") or {}
    site_url = site_urls.get(base) or (services["site"] + base if base != "/" else "")
    if not site_url:
        errors.append(f"wiki.yml: no site_url for base {base!r}")
    menu, footer = wiki.get("menu") or [], wiki.get("footer") or []
    for where, entries in [("menu", menu)] + [(f"footer: {c.get('title')}", c.get("links") or []) for c in footer
                                              if isinstance(c, dict)]:
        for e in entries:
            if not (isinstance(e, dict) and e.get("label") and e.get("href")):
                errors.append(f"wiki.yml: {where}: every entry needs a label and an href")

    icons = wiki.get("section_icons") or {}
    sections, seen = [], set()
    if not isinstance(raw_sections, list):
        errors.append("sections.yml: must be a list of sections")
        raw_sections = []
    for i, s in enumerate(raw_sections, 1):
        if not isinstance(s, dict):
            errors.append(f"sections.yml: entry {i} is not a mapping")
            continue
        sid = str(s.get("id") or "")
        if not SLUG.match(sid):
            errors.append(f"sections.yml: entry {i}: id {sid!r} must be lowercase-hyphen")
            continue
        if sid in seen:
            errors.append(f"sections.yml: section {sid!r} appears twice")
            continue
        seen.add(sid)
        for key in ("title", "summary"):
            if not str(s.get(key) or "").strip():
                errors.append(f"sections.yml: section {sid!r} has no {key}")
        icon = icons.get(sid, "document-text")
        if not (THEME / "icons" / "heroicons" / f"{icon}.svg").exists():
            errors.append(f"wiki.yml: section_icons.{sid}: no icon theme/icons/heroicons/{icon}.svg")
        sections.append(Section(sid, str(s.get("title", "")).strip(), str(s.get("summary", "")).strip(), icon))

    for key in ("name", "repo", "branch"):
        if not wiki.get(key):
            errors.append(f"wiki.yml: {key} is missing")
    if errors:
        raise BuildError(errors)

    cfg = Config(
        root=root,
        name=wiki["name"],
        base=base,
        site_url=site_url if site_url.endswith("/") else site_url + "/",
        repo=wiki["repo"].rstrip("/"),
        branch=wiki["branch"],
        noindex=bool(wiki.get("noindex", True)),
        generated_from=wiki.get("generated_from", ""),
        menu=menu,
        footer=footer,
        **services,
        sections=sections,
    )
    for s in cfg.sections:
        s.url = f"{base}sections/{s.id}/"
    return cfg
