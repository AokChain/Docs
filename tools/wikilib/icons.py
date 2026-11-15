"""The inline icon sprite. Pages reference icons as <use href="#i.NAME"/>
(Heroicons, 24/outline) or "#b.NAME" (Simple Icons brand marks); each page
gets exactly the <symbol>s it uses, so no icon file is fetched. The dot keeps
icon ids apart from heading anchors, which never contain one."""
import re
from functools import lru_cache

from .config import THEME

# The AOK mark and the AOK logo (mark and letters), as on the website.
MARK = (
    "M19.5 39A19.5 19.5 0 0 1 0 19.5v-.13A19.37 19.37 0 0 1 19.37 0h.13a19.5 19.5 0 0 1 0 39Z"
    "m-1.907-17.623h3.63l2.158 7.519h7.115l-2.145-7.519h2.595v-1.665h-3.08l-.341-1.202h3.421V16.87"
    "h-3.894L24.635 8.4H14.188l-2.423 8.47H7.877v1.641h3.418l-.342 1.202H7.877v1.665h2.591l-2.14 7.519"
    "h7.121l2.145-7.519Zm9.897 5.876h-2.044l-1.681-5.875h2.044l1.681 5.875Zm-14.117 0h-2.047l1.684-5.875"
    "h2.044l-1.681 5.875Zm11.963-7.54h-2.056l-.341-1.202h2.047l.35 1.202Zm-4.586 0h-2.673l.345-1.202"
    "h1.978l.35 1.202Zm-5.211 0h-2.047l.341-1.202h2.044l-.338 1.202Zm8.974-2.842h-2.035l-1.771-6.175"
    "h2.047l1.759 6.175Zm-4.573 0h-1.045l.516-1.828.529 1.828Zm-3.59 0h-2.044l1.759-6.175h2.047"
    "l-1.762 6.175Z"
)
LOGO_LETTERS = (
    '<path d="M48.686 12.13h4.394l3.263 12.848h-1.816l-.833-2.872H47.98l-.8 2.891h-1.8zm-.316 8.252h4.955l-1.651-6.584h-1.617z"/>'
    '<path d="M57.178 18.637c0-4.254 1.149-6.7 5.116-6.7s5.133 2.423 5.133 6.7c0 4.367-1.146 6.55-5.133 6.55-3.967 0-5.116-2.256-5.116-6.55m8.379 0c0-3.18-.613-4.957-3.263-4.957s-3.264 1.757-3.264 4.957c0 3.221.594 4.813 3.264 4.813 2.688 0 3.263-1.518 3.263-4.813"/>'
    '<path d="M73.473 19.544l-2 .109v5.331h-1.8V12.142h1.8v5.774l1.963-.111 2.875-5.663h2.1l-3.357 6.421 3.524 6.42h-2.122z"/>'
)
SPECIAL = {
    "i.aok-mark": ("0 0 39 39", f'<path d="{MARK}"/>'),
    "i.aok-logo": ("0 0 79 38", f'<path transform="scale(.97436)" d="{MARK}"/>' + LOGO_LETTERS),
}
USE = re.compile(r'href="#((?:i|b)\.[a-z0-9-]+)"')


@lru_cache(maxsize=None)
def symbol(name):
    if name in SPECIAL:
        box, inner = SPECIAL[name]
        return f'<symbol id="{name}" viewBox="{box}">{inner}</symbol>'
    kind, _, base = name.partition(".")
    folder = "heroicons" if kind == "i" else "simple"
    path = THEME / "icons" / folder / f"{base}.svg"
    if not path.exists():
        raise KeyError(f"icon {name}: no file theme/icons/{folder}/{base}.svg")
    src = path.read_text(encoding="utf-8")
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S)
    src = re.sub(r"<title>.*?</title>", "", src, flags=re.S)
    inner = re.search(r"<svg[^>]*>(.*)</svg>", src, flags=re.S).group(1)
    inner = re.sub(r"\s+", " ", inner).strip()
    inner = re.sub(r"\s*/>", "/>", inner)
    inner = re.sub(r' (?:stroke-linecap|stroke-linejoin)="round"', "", inner)
    return f'<symbol id="{name}" viewBox="0 0 24 24">{inner}</symbol>'


def sprite_for(html):
    names = sorted(set(USE.findall(html)))
    body = "".join(symbol(n) for n in names)
    return f'<svg class="sprite" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">{body}</svg>'
