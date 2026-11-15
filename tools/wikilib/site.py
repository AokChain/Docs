"""The build: pages in, a static site out.

  1. read every page (front matter, text rules), index slugs and aliases
  2. parse the Markdown of every page (headings, links, images)
  3. resolve links against all pages; any broken link stops the build
  4. dates and changes from git
  5. write the assets (file names carry a content hash), the search index,
     the pages, the section pages, All pages, Recent changes, the alias
     redirects and the 404 page
"""
import datetime
import hashlib
import json
import re
import shutil
import struct
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from . import art, checks, gitinfo, icons, markdown, search
from . import pages as pagelib
from .config import THEME, BuildError

MARKER = ".wiki-build.json"
RECENT_MAX = 60
TOP_PAGES = 4


def digest(data):
    return hashlib.sha256(data).hexdigest()[:10]


def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d:%b} {d.day}, {d.year}"


def image_size(path):
    """(width, height) of a PNG, GIF, JPEG, WebP or SVG file, or None."""
    data = path.read_bytes()
    try:
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", data[16:24])
        if data[:6] in (b"GIF87a", b"GIF89a"):
            return struct.unpack("<HH", data[6:10])
        if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            kind = data[12:16]
            if kind == b"VP8X":
                return (int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1)
            if kind == b"VP8 ":
                w, h = struct.unpack("<HH", data[26:30])
                return (w & 0x3FFF, h & 0x3FFF)
            if kind == b"VP8L":
                b = int.from_bytes(data[21:25], "little")
                return ((b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1)
        if data[:2] == b"\xff\xd8":
            i = 2
            while i < len(data) - 9:
                if data[i] != 0xFF:
                    i += 1
                    continue
                marker = data[i + 1]
                if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                    i += 2
                    continue
                length = struct.unpack(">H", data[i + 2:i + 4])[0]
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                    h, w = struct.unpack(">HH", data[i + 5:i + 9])
                    return (w, h)
                i += 2 + length
        if path.suffix == ".svg":
            text = data[:4000].decode("utf-8", "replace")
            m = re.search(r'viewBox="[\d.\-]+[\s,]+[\d.\-]+[\s,]+([\d.]+)[\s,]+([\d.]+)"', text)
            if m:
                return (round(float(m.group(1))), round(float(m.group(2))))
    except (struct.error, ValueError, IndexError):
        return None
    return None


class Site:
    def __init__(self, cfg, page_dirs, out):
        self.cfg = cfg
        self.base = cfg.base
        self.page_dirs = [Path(d).resolve() for d in page_dirs]
        self.out = Path(out).resolve()
        self.warnings = []

    # -------------------------------------------------------------- read

    def read(self):
        errors = []
        self.pages, failed = pagelib.load(self.page_dirs, self.cfg, errors)
        if failed:
            # links to the pages that could not be read would only add noise
            raise BuildError(errors)
        self.by_slug, self.aliases = pagelib.index(self.pages, errors)
        for p in self.pages:
            p.url = f"{self.base}{p.slug}/"
        self.content_assets = self._content_assets(errors)
        titles = {p.slug: p.title for p in self.pages}
        md = markdown.make_parser()
        self.md = md
        for p in self.pages:
            p.parsed, problems = markdown.parse(md, p.body, p.label, p.body_line, titles)
            errors.extend(problems)
        for p in self.pages:
            errors.extend(self._resolve(p))
        if errors:
            raise BuildError(errors)
        for p in self.pages:
            for slug in sorted(p.links_to):
                self.by_slug[slug].backlinks.append(p)
        for p in self.pages:
            p.backlinks.sort(key=lambda b: b.title.lower())
        for s in self.cfg.sections:
            s.pages = sorted((p for p in self.pages if p.section is s), key=lambda p: (p.order, p.title.lower()))

    def _content_assets(self, errors):
        """Files under assets/ next to each pages directory, by path."""
        found = {}
        for d in self.page_dirs:
            root = d.parent / "assets"
            if not root.is_dir():
                continue
            for f in sorted(root.rglob("*")):
                if not f.is_file() or any(part.startswith(".") for part in f.relative_to(root).parts):
                    continue
                rel = f.relative_to(root).as_posix()
                if rel in found and found[rel].read_bytes() != f.read_bytes():
                    errors.append(f"assets/{rel}: two different files with this name ({found[rel]} and {f})")
                found.setdefault(rel, f)
        return found

    def _resolve(self, page):
        errors = []
        for ref in page.parsed.refs:
            if ref.kind == "wiki":
                raw = ref.token.meta["raw"]
                slug = ref.target or page.slug
                target = self.by_slug.get(slug) or self.aliases.get(slug)
                if target is None:
                    errors.append(f"{ref.line}: broken wiki link {raw}: no page {slug!r}")
                    continue
                label = ref.token.meta["text"]
                href = "" if target is page else target.url
                if ref.anchor:
                    heading = next((h for h in target.parsed.headings if h.id == ref.anchor), None)
                    if ref.anchor not in target.parsed.ids:
                        errors.append(f"{ref.line}: broken wiki link {raw}: no heading #{ref.anchor} in {target.slug}")
                        continue
                    href += "#" + ref.anchor
                    label = label or (heading.text if heading else ref.anchor)
                ref.token.meta.update(href=href or target.url, label=label or target.title)
                if target is not page:
                    page.links_to.add(target.slug)
            elif ref.kind == "anchor":
                if ref.anchor not in page.parsed.ids:
                    errors.append(f"{ref.line}: link #{ref.anchor}: no such heading on this page")
            elif ref.kind == "path":
                href, target, problem = self._resolve_path(ref.target, ref.anchor)
                if problem:
                    errors.append(f"{ref.line}: link {ref.target}{'#' + ref.anchor if ref.anchor else ''}: {problem}")
                    continue
                ref.token.attrSet("href", href)
                if target is not None and target is not page:
                    page.links_to.add(target.slug)
            elif ref.kind == "image":
                src = ref.target
                rel = src[len("/assets/"):] if src.startswith("/assets/") else None
                if rel is None or rel not in self.content_assets:
                    errors.append(f"{ref.line}: image {src}: no such file; images go in assets/img/ "
                                  f"and are written /assets/img/<name>")
                    continue
                ref.token.attrSet("src", f"{self.base}assets/{rel}")
                ref.token.meta["size"] = image_size(self.content_assets[rel])
        return errors

    def _resolve_path(self, path, frag):
        """A root-relative link: base URL added, target checked."""
        p = path.strip("/")
        suffix = "#" + frag if frag else ""
        if p.startswith("assets/"):
            if p[len("assets/"):] not in self.content_assets:
                return None, None, "no such file in assets/"
            return f"{self.base}{p}", None, None
        if p == "":
            return self.base + suffix, None, None
        parts = p.split("/")
        if len(parts) == 1:
            target = self.by_slug.get(parts[0]) or self.aliases.get(parts[0])
            if target:
                if frag and frag not in target.parsed.ids:
                    return None, None, f"no heading #{frag} in {target.slug}"
                return target.url + suffix, target, None
            if parts[0] in ("all-pages", "recent-changes"):
                return f"{self.base}{parts[0]}/" + suffix, None, None
        if len(parts) == 2 and parts[0] == "sections" and self.cfg.section(parts[1]):
            return f"{self.base}sections/{parts[1]}/" + suffix, None, None
        return None, None, "no such page (link pages with [[slug]])"

    # -------------------------------------------------------------- git

    def read_git(self):
        commits, seen = [], set()
        for d in self.page_dirs:
            repo = gitinfo.toplevel(d)
            if repo is None:
                continue
            log = gitinfo.log(repo, d)
            dates = gitinfo.last_changed(log)
            for p in self.pages:
                if p.path.is_relative_to(d):
                    p.repo = repo
                    p.repo_path = p.path.relative_to(repo).as_posix()
                    p.updated = dates.get(p.repo_path, "")
            for c in log:
                if c.hash not in seen:
                    seen.add(c.hash)
                    commits.append(c)
        commits.sort(key=lambda c: c.time, reverse=True)
        by_path = {p.repo_path: p for p in self.pages if p.repo_path}
        self.changes = []
        for c in commits[:RECENT_MAX]:
            subject = c.subject
            if checks.text_problems(subject):
                self.warnings.append(f"commit {c.hash[:10]}: subject left out of Recent changes "
                                     f"({'; '.join(checks.text_problems(subject))})")
                subject = "Edited pages"
            touched, names = [], set()
            for status, path, _old in c.files:
                page = by_path.get(path)
                name = page.title if page else Path(path).stem.replace("-", " ").capitalize()
                if name in names:
                    continue
                names.add(name)
                touched.append({"title": name, "url": page.url if page else "", "removed": status == "D"})
            self.changes.append({
                "date": c.date, "nice": nice_date(c.date), "subject": subject,
                "hash": c.hash, "short": c.hash[:7], "url": f"{self.cfg.repo}/commit/{c.hash}", "pages": touched,
            })

    # -------------------------------------------------------------- write

    def prepare_out(self):
        if self.out.exists():
            if any(self.out.iterdir()) and not (self.out / MARKER).exists():
                raise BuildError([f"{self.out}: not empty and not a wiki build; refusing to clear it"])
            shutil.rmtree(self.out)
        (self.out / "assets").mkdir(parents=True)

    def _put(self, rel, data):
        path = self.out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))

    def _hashed(self, folder, src, data=None):
        data = src.read_bytes() if data is None else data
        name = f"{src.stem}.{digest(data)}{src.suffix}"
        self._put(f"assets/{folder}{name}", data)
        return f"{self.base}assets/{folder}{name}", name

    def write_assets(self):
        a = {}
        fonts = {}
        for f in sorted((THEME / "fonts").iterdir()):
            if f.suffix == ".woff2":
                a["font-" + f.stem], fonts[f.name] = self._hashed("fonts/", f)
            elif f.suffix == ".txt":
                self._put(f"assets/fonts/{f.name}", f.read_bytes())
        css = (THEME / "css" / "docs.css").read_text(encoding="utf-8")
        css = re.sub(r'url\("\.\./fonts/([^"]+)"\)', lambda m: f'url("fonts/{fonts[m.group(1)]}")', css)
        a["css"], _ = self._hashed("", THEME / "css" / "docs.css", css.encode("utf-8"))
        a["nojs"], _ = self._hashed("", THEME / "css" / "nojs.css")
        a["js"], _ = self._hashed("", THEME / "js" / "docs.js")
        a["favicon"], _ = self._hashed("", THEME / "img" / "favicon.svg")
        a["touch"], _ = self._hashed("", THEME / "img" / "apple-touch-icon.png")
        self._put("favicon.ico", (THEME / "img" / "favicon.ico").read_bytes())
        self._put("assets/licenses.txt", (THEME / "licenses.txt").read_bytes())
        index = search.build(self.pages).encode("utf-8")
        name = f"search.{digest(index)}.json"
        self._put(f"assets/{name}", index)
        a["search"] = f"{self.base}assets/{name}"
        for rel, src in self.content_assets.items():
            self._put(f"assets/{rel}", src.read_bytes())
        self.assets = a

    def env(self):
        env = Environment(
            loader=FileSystemLoader(str(THEME / "templates")),
            autoescape=True, undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True,
        )
        cfg = self.cfg
        env.globals.update(
            site=cfg, base=self.base, links=cfg.links, assets=self.assets, sections=cfg.sections,
            home_url=self.base, all_url=f"{self.base}all-pages/", recent_url=f"{self.base}recent-changes/",
            repo=cfg.repo, page_count=len(self.pages),
        )
        env.filters["nice_date"] = nice_date
        return env

    def canonical(self, path):
        return self.cfg.site_url + path[len(self.base):]

    def render(self, env, template, rel, **ctx):
        html = env.get_template(template).render(**ctx)
        html = html.replace("<!--sprite-->", icons.sprite_for(html), 1)
        # the same text rules over the finished page (drawing data left out)
        problems = checks.file_problems(re.sub(r'\sd="[^"]*"', "", html), f"build/{rel}")
        if problems:
            raise BuildError(problems)
        self._put(rel, html)

    def toc(self, page):
        out = []
        for h in page.parsed.headings:
            if h.level == 2:
                out.append({"id": h.id, "text": h.text, "children": []})
            elif h.level == 3:
                if out:
                    out[-1]["children"].append({"id": h.id, "text": h.text})
                else:
                    out.append({"id": h.id, "text": h.text, "children": []})
        return out

    def write_pages(self, env):
        for p in self.pages:
            p.html = markdown.render(self.md, p.parsed.tokens)
        for s in self.cfg.sections:
            for i, p in enumerate(s.pages):
                prev = s.pages[i - 1] if i > 0 else None
                nxt = s.pages[i + 1] if i + 1 < len(s.pages) else None
                path = p.repo_path or f"pages/{s.id}/{p.slug}.md"
                meta = {
                    "updated": p.updated,
                    "edit": "" if p.generated_by else f"{self.cfg.repo}/edit/{self.cfg.branch}/{path}",
                    "history": f"{self.cfg.repo}/commits/{self.cfg.branch}/{path}",
                    "generated": self.cfg.generated_from if p.generated_by else "",
                }
                self.render(env, "page.html", f"{p.slug}/index.html", kind="page", page=p, section=s,
                            title=p.title, description=p.description, canonical=self.canonical(p.url),
                            current_slug=p.slug, current_section=s.id, toc=self.toc(p),
                            prev=prev, next=nxt, meta=meta)
            self.render(env, "section.html", f"sections/{s.id}/index.html", kind="section", section=s,
                        title=s.title, description=s.summary, canonical=self.canonical(s.url),
                        current_slug="", current_section=s.id)

    def write_lists(self, env):
        groups = {}
        for p in sorted(self.pages, key=lambda p: p.title.lower()):
            letter = p.title[:1].upper()
            groups.setdefault(letter if letter.isalpha() else "#", []).append(p)
        letters = sorted(groups, key=lambda k: (k == "#", k))
        url = f"{self.base}all-pages/"
        self.render(env, "all_pages.html", "all-pages/index.html", kind="all", title="All pages",
                    description=f"Every page of the {self.cfg.name}, from A to Z.",
                    canonical=self.canonical(url), current_slug="", current_section="",
                    groups=[(k, groups[k]) for k in letters])
        days = []
        for c in self.changes:
            if not days or days[-1][0] != c["nice"]:
                days.append((c["nice"], c["date"], []))
            days[-1][2].append(c)
        url = f"{self.base}recent-changes/"
        self.render(env, "recent.html", "recent-changes/index.html", kind="recent", title="Recent changes",
                    description=f"The latest edits to the {self.cfg.name}.",
                    canonical=self.canonical(url), current_slug="", current_section="", days=days)

    def write_home(self, env):
        links = []
        for p in self.pages:
            for slug in sorted(p.links_to):
                t = self.by_slug[slug]
                if t.section is not p.section:
                    links.append((p.slug, slug))
        sections = [(s.title, [p.slug for p in s.pages]) for s in self.cfg.sections]
        self.render(env, "home.html", "index.html", kind="home", title=self.cfg.name,
                    description="Guides and reference for AokChain: wallets, staking, tokens, nodes and the RPC interface.",
                    canonical=self.cfg.site_url, current_slug="", current_section="",
                    art_wide=art.wiki_map("wide", sections, links, "map-w"),
                    art_tall=art.wiki_map("tall", sections, links, "map-t"),
                    recent=self.changes[:5], top=TOP_PAGES)

    def write_extras(self, env):
        self.render(env, "not_found.html", "404.html", kind="notfound", title="Page not found",
                    description="This page is not in the docs.", canonical=self.cfg.site_url,
                    current_slug="", current_section="", art_lost=art.lost())
        for alias, target in sorted(self.aliases.items()):
            self.render(env, "redirect.html", f"{alias}/index.html", target=target,
                        canonical=self.canonical(target.url))
        if self.base == "/":
            rules = "Disallow: /" if self.cfg.noindex else "Allow: /"
            self._put("robots.txt", f"User-agent: *\n{rules}\n")

    def build(self):
        self.read()
        self.read_git()
        self.prepare_out()
        self.write_assets()
        env = self.env()
        self.write_pages(env)
        self.write_lists(env)
        self.write_home(env)
        self.write_extras(env)
        self._put(MARKER, json.dumps({
            "base": self.base, "pages": len(self.pages), "aliases": len(self.aliases),
            "built": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        }, indent=1) + "\n")
        return self
