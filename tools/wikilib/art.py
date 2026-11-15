"""Line art for the wiki, in the manner of the AOK website: thin lines, small
nodes, one ink, colours from CSS classes (.ln, .dt, .nd ... in docs.css).

The home page drawing is the wiki itself: the AOK coin with one ray per
section, a node on the ray for every page of that section, and a faint arc
for every wiki link between pages of different sections. It is drawn from
the pages at build time, so it grows with the wiki.
"""
import math
import random

from .icons import MARK

GOLDEN = math.pi * (3 - math.sqrt(5))


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


class Sheet:
    """Collects lines and nodes by class and writes them as a few paths."""

    def __init__(self):
        self.lines, self.dots, self.curves, self.extra = {}, {}, {}, []

    def line(self, cls, a, b):
        self.lines.setdefault(cls, []).append((a, b))

    def curve(self, cls, a, c, b):
        self.curves.setdefault(cls, []).append((a, c, b))

    def dot(self, cls, p):
        self.dots.setdefault(cls, []).append(p)

    def add(self, svg):
        self.extra.append(svg)

    def svg(self, group=None):
        out = []
        for cls, segs in self.curves.items():
            d = "".join(f"M{f(a[0])} {f(a[1])}Q{f(c[0])} {f(c[1])} {f(b[0])} {f(b[1])}" for a, c, b in segs)
            out.append(f'<path class="{cls}" d="{d}"/>')
        for cls, segs in self.lines.items():
            d = "".join(f"M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}" for a, b in segs)
            out.append(f'<path class="{cls}" d="{d}"/>')
        out += self.extra
        for cls, pts in self.dots.items():
            d = "".join(f"M{f(x)} {f(y)}h0" for x, y in pts)
            out.append(f'<path class="{cls}" d="{d}"/>')
        body = "\n".join(out)
        return f'<g class="{group}">\n{body}\n</g>' if group else body


def svg_open(cls, w, h, aspect, label=None, uid="art"):
    attrs = f'class="art {cls}" viewBox="0 0 {w} {h}" preserveAspectRatio="{aspect}"'
    if label:
        title, desc = label
        return (f'<svg {attrs} role="img" aria-labelledby="{uid}-t {uid}-d" xmlns="http://www.w3.org/2000/svg">'
                f'<title id="{uid}-t">{title}</title><desc id="{uid}-d">{desc}</desc>')
    return f'<svg {attrs} aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">'


def mark(cx, cy, r, cls):
    s = r * 2 / 39
    return f'<path class="{cls}" transform="translate({f(cx - r)} {f(cy - r)}) scale({s:.4f})" d="{MARK}"/>'


def knn_links(pts, k, max_d):
    links = set()
    for i, p in enumerate(pts):
        near = sorted((math.dist(p, q), j) for j, q in enumerate(pts) if j != i)
        for d, j in near[:k]:
            if d <= max_d:
                links.add((min(i, j), max(i, j)))
    return sorted(links)


def coin(sheet, cx, cy, r, rng, n=46):
    """The AOK coin as on the website: a ring of linked nodes, the rim, the mark."""
    ring = []
    for i in range(n):
        t = math.sqrt((i + 0.5) / n)
        rr = r * 0.7 + r * 0.27 * t + rng.uniform(-r * 0.03, r * 0.03)
        th = i * GOLDEN + rng.uniform(-0.03, 0.03)
        ring.append((cx + rr * math.cos(th), cy + rr * math.sin(th)))
    for a, b in knn_links(ring, 3, r * 0.42):
        sheet.line("ln-f", ring[a], ring[b])
    for p in ring:
        sheet.dot("dt", p)
    sheet.add(f'<circle class="ln-2" cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}"/>')
    sheet.add(mark(cx, cy, r * 0.62, "ink"))


# ------------------------------------------------------------------ the wiki

LAYOUTS = {
    # canvas, coin centre and radius, the fan of rays (degrees, 0 = right,
    # clockwise because SVG y points down), hub distance, page spacing, how
    # far the rays run past their last page
    "wide": dict(w=1600, h=820, cx=1190, cy=420, r=112, a0=-150, a1=146, hub=2.35, step=23, run=900,
                 aspect="xMaxYMid meet"),
    "tall": dict(w=400, h=400, cx=200, cy=396, r=60, a0=-174, a1=-6, hub=2.5, step=14, run=420,
                 aspect="xMidYMax meet"),
}


def wiki_map(layout, sections, links, uid):
    """sections: [(title, [page slug, ...]), ...] in sidebar order.
    links: [(slug, slug), ...] wiki links between pages."""
    L = LAYOUTS[layout]
    rng = random.Random(64)
    cx, cy, r = L["cx"], L["cy"], L["r"]
    n = max(len(sections), 1)
    pos = {}
    rays, twigs, coin_sheet = Sheet(), Sheet(), Sheet()
    angles = [L["a0"] + (L["a1"] - L["a0"]) * (k + 0.5) / n for k in range(n)]

    for k, (_title, slugs) in enumerate(sections):
        a = math.radians(angles[k])
        ca, sa = math.cos(a), math.sin(a)
        # rays that point back toward the headline are drawn closer in
        squeeze = 0.62 if ca < -0.35 else 1.0
        step = L["step"] * squeeze
        start, hub = r * 1.3, r * L["hub"]
        hx, hy = cx + hub * ca, cy + hub * sa
        rays.line("ln-r", (cx + start * ca, cy + start * sa), (hx - 10 * ca, hy - 10 * sa))
        rays.add(f'<circle class="nd" cx="{f(hx)}" cy="{f(hy)}" r="8"/>')
        rays.dot("dt-3", (hx, hy))
        last = hub
        for i, slug in enumerate(slugs):
            d = hub + 30 + i * step
            side = 1 if i % 2 else -1
            off = side * (10 + (i % 3) * 6 + rng.uniform(0, 4))
            bx, by = cx + d * ca, cy + d * sa
            px, py = bx - off * sa, by + off * ca
            twigs.line("ln", (bx, by), (px, py))
            twigs.dot("dt-2" if i == 0 else "dt", (px, py))
            pos[slug] = (px, py)
            last = d
        # the ray runs on past its last page, fading out toward the edge
        rays.line("ln", (hx + 10 * ca, hy + 10 * sa), (cx + last * ca, cy + last * sa))
        tail = last + (L["run"] - last) * (0.35 if squeeze < 1 else 1.0)
        rays.line("ln-f", (cx + (last + 8) * ca, cy + (last + 8) * sa), (cx + tail * ca, cy + tail * sa))
        rays.dot("dt-f", (cx + (last + step) * ca, cy + (last + step) * sa))

    # finer rays between the sections, broken like the rays of the old coin
    for k in range(n):
        for frac in (0.33, 0.67):
            if k == n - 1 and L["a1"] - L["a0"] < 300:
                continue
            a = math.radians(angles[k] + (L["a1"] - L["a0"]) / n * frac)
            ca, sa = math.cos(a), math.sin(a)
            if ca < -0.35:
                continue
            s0 = r * rng.uniform(1.32, 1.5)
            s1 = r * rng.uniform(1.9, 2.6)
            rays.line("ln-f", (cx + s0 * ca, cy + s0 * sa), (cx + s1 * ca, cy + s1 * sa))
            if rng.random() < 0.6:
                s2 = s1 + r * rng.uniform(0.25, 0.4)
                s3 = s2 + r * rng.uniform(0.5, 1.4)
                rays.line("ln-f", (cx + s2 * ca, cy + s2 * sa), (cx + s3 * ca, cy + s3 * sa))

    # wiki links between sections bend in toward the coin
    arcs = Sheet()
    seen = set()
    for a_slug, b_slug in links:
        if a_slug not in pos or b_slug not in pos:
            continue
        key = tuple(sorted((a_slug, b_slug)))
        if key in seen:
            continue
        seen.add(key)
        (x1, y1), (x2, y2) = pos[a_slug], pos[b_slug]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        qx, qy = mx + (cx - mx) * 0.38, my + (cy - my) * 0.38
        arcs.curve("ln-a", (x1, y1), (qx, qy), (x2, y2))

    coin(coin_sheet, cx, cy, r, rng)
    pages = sum(len(s) for _, s in sections)
    label = ("The wiki as a network",
             f"The AOK coin with {len(sections)} rays, one for each section, a node for each of the "
             f"{pages} pages and an arc for each of the {len(seen)} links between sections.")
    out = [svg_open(f"art-map art-map--{layout}", L["w"], L["h"], L["aspect"], label, uid)]
    out.append(arcs.svg("dg-arcs"))
    out.append(rays.svg("dg-rays"))
    out.append(twigs.svg("dg-pages"))
    out.append(coin_sheet.svg("dg-coin"))
    out.append("</svg>")
    return "\n".join(out)


def lost(uid="lost"):
    """The 404 page: a ray from the coin that ends in an empty node."""
    rng = random.Random(4)
    w, h = 560, 260
    cx, cy, r = 92, 150, 54
    s, c = Sheet(), Sheet()
    a = math.radians(-12)
    ca, sa = math.cos(a), math.sin(a)
    hub = r * 2.6
    hx, hy = cx + hub * ca, cy + hub * sa
    s.line("ln-r", (cx + r * 1.28 * ca, cy + r * 1.28 * sa), (hx - 9 * ca, hy - 9 * sa))
    s.add(f'<circle class="nd" cx="{f(hx)}" cy="{f(hy)}" r="7"/>')
    s.dot("dt-3", (hx, hy))
    d = hub
    for i in range(5):
        d = hub + 30 + i * 26
        side = 1 if i % 2 else -1
        off = side * (11 + (i % 3) * 5)
        bx, by = cx + d * ca, cy + d * sa
        s.line("ln", (bx, by), (bx - off * sa, by + off * ca))
        s.dot("dt", (bx - off * sa, by + off * ca))
    # the line breaks off; the page it led to is not there
    s.line("ln", (hx + 9 * ca, hy + 9 * sa), (cx + d * ca, cy + d * sa))
    gap = d + 34
    s.line("ln-f", (cx + gap * ca, cy + gap * sa), (cx + (gap + 40) * ca, cy + (gap + 40) * sa))
    ex, ey = cx + (gap + 66) * ca, cy + (gap + 66) * sa
    s.add(f'<circle class="nd-now" cx="{f(ex)}" cy="{f(ey)}" r="12"/>')
    coin(c, cx, cy, r, rng, n=34)
    return "\n".join([svg_open("art-lost", w, h, "xMidYMid meet", uid=uid), s.svg(), c.svg(), "</svg>"])
