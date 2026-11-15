"""The Markdown of the wiki: GitHub-flavored Markdown (tables, strikethrough,
autolinks, task lists, footnotes, alerts) plus [[wiki links]].

Pages go through three steps:

  parse()     tokens, heading anchors, the links and images in the page and
              the problems that need only the page itself
  resolve()   links checked against every page, hrefs rewritten under the
              base URL (needs all pages parsed first)
  render()    HTML

Rendering adds: an id on every heading, callouts for > [!NOTE] and the other
alerts, Pygments classes on fenced code, a scrolling wrapper on tables,
classes instead of style attributes (the CSP allows no inline styles), and
the arrow icon on links to other sites.
"""
import re
from dataclasses import dataclass, field

from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml
from mdit_py_plugins.gfm import gfm_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from .slug import Slugger

WIKILINK = re.compile(r"\[\[([^\[\]|\n]+)(?:\|([^\[\]\n]*))?\]\]")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
# Ids used by the page templates; headings never take them.
TEMPLATE_IDS = ("w-main", "w-sidebar", "w-toc", "w-backlinks", "w-search", "w-search-list")

# Raw HTML is limited to a few harmless tags (and comments, which are
# dropped). Anything else, including style and event attributes, fails.
ALLOWED_HTML = {
    "details": {"open"}, "summary": set(), "kbd": set(), "br": set(),
    "sub": set(), "sup": set(), "abbr": {"title"},
}
TAG = re.compile(r"<(/?)([A-Za-z][A-Za-z0-9-]*)((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>")
ATTR = re.compile(r"([^\s=/>]+)(?:\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s>]+))?")
COMMENT = re.compile(r"<!--.*?-->", re.S)

CALLOUT_ICONS = {
    "note": "information-circle", "tip": "light-bulb", "important": "exclamation-circle",
    "warning": "exclamation-triangle", "caution": "shield-exclamation",
}
# Code fence languages shown without highlighting.
PLAIN = {"text", "txt", "plain", "plaintext"}
FORMATTER = HtmlFormatter(nowrap=True)


@dataclass
class Heading:
    level: int
    text: str
    id: str


@dataclass
class Ref:
    """A link or image found in a page, resolved once all pages are known."""
    kind: str        # wiki, anchor, path, image
    token: object
    target: str      # slug, path or image source
    anchor: str
    line: int


@dataclass
class Parsed:
    tokens: list
    headings: list = field(default_factory=list)
    ids: set = field(default_factory=set)
    refs: list = field(default_factory=list)
    chunks: list = field(default_factory=list)   # [anchor, heading, text] for search


def fence_lang(info):
    info = (info or "").strip()
    return info.split()[0].lower() if info else ""


def lexer_for(lang):
    try:
        return get_lexer_by_name(lang, stripnl=False, ensurenl=True)
    except ClassNotFound:
        return None


# ------------------------------------------------------------------ parser

def _wikilink_rule(state, silent):
    if not state.src.startswith("[[", state.pos):
        return False
    m = WIKILINK.match(state.src, state.pos)
    if not m:
        return False
    if not silent:
        target, text = m.group(1).strip(), (m.group(2) or "").strip()
        slug, _, anchor = target.partition("#")
        tok = state.push("wikilink", "a", 0)
        tok.meta = {"slug": slug.strip(), "anchor": anchor.strip(), "text": text, "raw": m.group(0)}
    state.pos = m.end()
    return True


def make_parser():
    md = MarkdownIt("commonmark", {"html": True, "typographer": False, "linkify": False})
    md.use(gfm_plugin)
    md.inline.ruler.before("link", "wikilink", _wikilink_rule)
    for name, rule in RENDER_RULES.items():
        md.add_render_rule(name, rule)
    return md


def inline_text(children, titles=None):
    """Plain text of inline tokens, as a browser's textContent would read."""
    out = []
    for c in children or []:
        if c.type in ("text", "code_inline"):
            out.append(c.content)
        elif c.type in ("softbreak", "hardbreak"):
            out.append(" ")
        elif c.type == "wikilink":
            m = c.meta
            out.append(m.get("label") or m["text"] or (titles or {}).get(m["slug"], m["slug"]))
    return "".join(out).strip()


def _html_problems(src):
    problems = []
    for m in TAG.finditer(COMMENT.sub("", src)):
        closing, name, rest = m.group(1), m.group(2).lower(), m.group(3)
        if name not in ALLOWED_HTML:
            problems.append(f"HTML tag <{name}> is not allowed (allowed: {', '.join(sorted(ALLOWED_HTML))})")
            continue
        if closing:
            continue
        for a in ATTR.finditer(rest.strip().rstrip("/")):
            attr = a.group(1).lower()
            if attr not in ALLOWED_HTML[name]:
                problems.append(f"attribute {attr!r} on <{name}> is not allowed")
    return problems


def parse(md, body, label, first_line, titles):
    """Tokens and everything the page itself can tell; problems go to errors."""
    errors = []
    env = {}
    tokens = md.parse(body, env)
    page = Parsed(tokens)
    slugger = Slugger(TEMPLATE_IDS)

    def where(tok):
        return f"{label}:{first_line + (tok.map[0] if tok.map else 0)}"

    def walk_inline(children, at):
        for j, c in enumerate(children or []):
            if c.type == "wikilink":
                page.refs.append(Ref("wiki", c, c.meta["slug"], c.meta["anchor"], at))
            elif c.type == "link_open":
                href = c.attrGet("href") or ""
                if href.startswith("#"):
                    page.refs.append(Ref("anchor", c, "", href[1:], at))
                elif href.startswith("//"):
                    errors.append(f"{at}: link {href!r}: write the full https:// address")
                elif href.startswith("/"):
                    path, _, frag = href.partition("#")
                    page.refs.append(Ref("path", c, path, frag, at))
                elif SCHEME.match(href):
                    scheme = href.split(":", 1)[0].lower()
                    if scheme == "mailto":
                        errors.append(f"{at}: mailto link: no email addresses in the wiki")
                    elif scheme in ("http", "https"):
                        c.attrJoin("class", "ext")
                        for close in children[j + 1:]:
                            if close.type == "link_close":
                                close.meta["ext"] = True
                                break
                else:
                    errors.append(f"{at}: relative link {href!r}: link pages with [[slug]] "
                                  "and files with /assets/...")
            elif c.type == "image":
                src = c.attrGet("src") or ""
                if not inline_text(c.children).strip():
                    errors.append(f"{at}: image {src!r} has no alt text: write ![what it shows]({src})")
                if src.startswith("/"):
                    page.refs.append(Ref("image", c, src, "", at))
                elif SCHEME.match(src) or src.startswith("//"):
                    errors.append(f"{at}: image {src!r}: images come from this site, put the file in assets/img/")
                else:
                    errors.append(f"{at}: image {src!r}: use a path from the wiki root, /assets/img/...")
            elif c.type == "html_inline":
                errors.extend(f"{at}: {p}" for p in _html_problems(c.content))

    for i, tok in enumerate(tokens):
        if tok.type == "heading_open":
            inline = tokens[i + 1]
            text = inline_text(inline.children, titles)
            hid = slugger.slug(text)
            tok.attrSet("id", hid)
            level = int(tok.tag[1])
            tok.meta["self_link"] = not any(c.type in ("link_open", "wikilink") for c in inline.children or [])
            page.headings.append(Heading(level, text, hid))
            page.ids.add(hid)
            if level == 1:
                errors.append(f"{where(tok)}: H1 heading {text!r}: the title is the only H1, start the body at ##")
        elif tok.type == "inline":
            walk_inline(tok.children, where(tok))
        elif tok.type == "fence":
            lang = fence_lang(tok.info)
            if lang and lang not in PLAIN and lexer_for(lang) is None:
                errors.append(f"{where(tok)}: unknown code language {lang!r} (for example bash, ini, json, text)")
        elif tok.type == "html_block":
            errors.extend(f"{where(tok)}: {p}" for p in _html_problems(tok.content))
        elif tok.type in ("th_open", "td_open"):
            style = str(tok.attrs.pop("style", "") or "")
            if style.startswith("text-align:"):
                tok.attrJoin("class", "ta-" + style.split(":", 1)[1].strip())

    for n in range(1, len((env.get("footnotes") or {}).get("list", {})) + 1):
        page.ids.update((f"fn{n}", f"fnref{n}"))
    page.chunks = _chunks(tokens, titles)
    return page, errors


def _chunks(tokens, titles):
    """The text of a page cut at its h2 and h3 headings, for the search."""
    chunks = [["", "", []]]
    skip_next_inline = False
    for tok in tokens:
        if tok.type == "heading_open":
            skip_next_inline = True
            if tok.tag in ("h2", "h3"):
                chunks.append([tok.attrGet("id"), "", []])
            continue
        if tok.type == "inline":
            text = inline_text(tok.children, titles)
            if skip_next_inline:
                skip_next_inline = False
                if not chunks[-1][1] and chunks[-1][0]:
                    chunks[-1][1] = text
                    continue
            chunks[-1][2].append(text)
        elif tok.type in ("fence", "code_block"):
            chunks[-1][2].append(tok.content[:600])
    out = []
    for anchor, heading, parts in chunks:
        text = re.sub(r"\s+", " ", " ".join(parts)).strip()
        if anchor or text:
            out.append([anchor, heading, text])
    return out


# ------------------------------------------------------------------ render

def _heading_open(self, tokens, idx, options, env):
    tok = tokens[idx]
    hid = escapeHtml(str(tok.attrGet("id")))
    out = f"<{tok.tag} id=\"{hid}\">"
    if tok.meta.get("self_link"):
        out += f'<a class="h-anchor" href="#{hid}">'
    return out


def _heading_close(self, tokens, idx, options, env):
    opener = tokens[idx - 2]
    return ("</a>" if opener.meta.get("self_link") else "") + f"</{tokens[idx].tag}>\n"


def _wikilink(self, tokens, idx, options, env):
    m = tokens[idx].meta
    if "href" not in m:
        return f'<span class="wl-missing">{escapeHtml(m["raw"])}</span>'
    return f'<a href="{escapeHtml(m["href"])}">{escapeHtml(m["label"])}</a>'


def _link_close(self, tokens, idx, options, env):
    icon = ""
    if tokens[idx].meta.get("ext"):
        icon = '<svg class="icon icon-ext" aria-hidden="true"><use href="#i-arrow-up-right"/></svg>'
    return icon + "</a>"


def _image(self, tokens, idx, options, env):
    tok = tokens[idx]
    alt = escapeHtml(self.renderInlineAsText(tok.children, options, env))
    src = escapeHtml(str(tok.attrGet("src")))
    extra = ""
    size = tok.meta.get("size")
    if size:
        extra += f' width="{size[0]}" height="{size[1]}"'
    title = tok.attrGet("title")
    if title:
        extra += f' title="{escapeHtml(str(title))}"'
    return f'<img src="{src}" alt="{alt}"{extra} loading="lazy" decoding="async">'


def _fence(self, tokens, idx, options, env):
    tok = tokens[idx]
    lang = fence_lang(tok.info)
    lexer = lexer_for(lang) if lang and lang not in PLAIN else None
    body = highlight(tok.content, lexer, FORMATTER) if lexer else escapeHtml(tok.content)
    label = f'<span class="code-lang">{escapeHtml(lang)}</span>' if lang and lang not in PLAIN else ""
    return f'<div class="code"><div class="code-bar">{label}</div><pre><code>{body}</code></pre></div>\n'


def _code_block(self, tokens, idx, options, env):
    body = escapeHtml(tokens[idx].content)
    return f'<div class="code"><div class="code-bar"></div><pre><code>{body}</code></pre></div>\n'


def _table_open(self, tokens, idx, options, env):
    return '<div class="table-wrap"><table>\n'


def _table_close(self, tokens, idx, options, env):
    return "</table></div>\n"


def _alert_open(self, tokens, idx, options, env):
    kind = tokens[idx].meta["kind"].lower()
    return f'<div class="callout callout-{kind}" role="note">\n'


def _alert_title_open(self, tokens, idx, options, env):
    kind = tokens[idx - 1].meta["kind"].lower()
    return (f'<p class="callout-title"><svg class="icon" aria-hidden="true">'
            f'<use href="#i-{CALLOUT_ICONS[kind]}"/></svg>')


def _alert_title_close(self, tokens, idx, options, env):
    return "</p>\n"


def _alert_close(self, tokens, idx, options, env):
    return "</div>\n"


def _html(self, tokens, idx, options, env):
    out = COMMENT.sub("", tokens[idx].content)
    return out if out.strip() else ""


RENDER_RULES = {
    "heading_open": _heading_open, "heading_close": _heading_close,
    "wikilink": _wikilink, "link_close": _link_close, "image": _image,
    "fence": _fence, "code_block": _code_block,
    "table_open": _table_open, "table_close": _table_close,
    "alert_open": _alert_open, "alert_title_open": _alert_title_open,
    "alert_title_close": _alert_title_close, "alert_close": _alert_close,
    "html_block": _html, "html_inline": _html,
}


def render(md, tokens):
    return md.renderer.render(tokens, md.options, {})
