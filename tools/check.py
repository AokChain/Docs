#!/usr/bin/env python3
"""Open the wiki in headless Chrome and report what a visitor's browser
would: console errors, script errors, CSP violations, failed requests,
horizontal scrolling, text contrast under 4.5:1 (3:1 for large text),
missing fonts, and every same-site link or asset that does not answer.
Each page is checked at 1440, 1024, 390 and 360 px wide, in the light and
the dark theme. The search, the menu, the copy buttons and the 404 page are
also tried once. Standard library only.

    .venv/bin/python tools/check.py                         # serves build/ with the production headers
    .venv/bin/python tools/check.py https://web.aok.network/doc/
    .venv/bin/python tools/check.py --shots /tmp/shots --only / --only /staking-guide/

Exit status 1 when anything failed.
"""
import argparse
import base64
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import serve  # noqa: E402
from wikilib.checks import HANGUL  # noqa: E402,F401

WIDTHS = (1440, 1024, 390, 360)
THEMES = ("light", "dark")
UA = "aok-docs-check"


class CDP:
    """A minimal WebSocket client for the Chrome DevTools protocol."""

    def __init__(self, ws_url):
        host_port, path = ws_url[len("ws://"):].split("/", 1)
        host, port = host_port.split(":")
        self.sock = socket.create_connection((host, int(port)), timeout=60)
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall((
            f"GET /{path} HTTP/1.1\r\nHost: {host_port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
        ).encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += self.sock.recv(4096)
        if b" 101 " not in resp.split(b"\r\n", 1)[0]:
            raise RuntimeError(resp[:200])
        self.buf = resp.split(b"\r\n\r\n", 1)[1]
        self.next_id = 0
        self.events = []

    def _send(self, text):
        data = text.encode()
        head = bytes([0x81])
        n = len(data)
        if n < 126:
            head += bytes([0x80 | n])
        elif n < 65536:
            head += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            head += bytes([0x80 | 127]) + struct.pack(">Q", n)
        mask = os.urandom(4)
        self.sock.sendall(head + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.sock.recv(1 << 20)
            if not chunk:
                raise EOFError
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def _recv(self):
        message = b""
        while True:
            b1, b2 = self._read(2)
            n = b2 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._read(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._read(8))[0]
            payload = self._read(n)
            if b1 & 0x0F in (0x9, 0xA):
                continue
            message += payload
            if b1 & 0x80:
                return json.loads(message.decode())

    def call(self, method, **params):
        self.next_id += 1
        my_id = self.next_id
        self._send(json.dumps({"id": my_id, "method": method, "params": params}))
        while True:
            msg = self._recv()
            if msg.get("id") == my_id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
            self.events.append(msg)

    def pump(self, seconds):
        end = time.time() + seconds
        self.sock.settimeout(0.1)
        try:
            while time.time() < end:
                try:
                    self.events.append(self._recv())
                except (socket.timeout, TimeoutError):
                    pass
        finally:
            self.sock.settimeout(60)

    def wait_for(self, method, seconds=20):
        end = time.time() + seconds
        while time.time() < end:
            for e in self.events:
                if e.get("method") == method:
                    return e
            self.pump(0.1)
        return None

    def js(self, expression, await_promise=False):
        res = self.call("Runtime.evaluate", expression=expression, returnByValue=True, awaitPromise=await_promise)
        if "exceptionDetails" in res:
            raise RuntimeError(f"evaluate failed: {res['exceptionDetails'].get('text')}: {expression[:80]}")
        return res.get("result", {}).get("value")


class Chrome:
    def __init__(self):
        exe = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
        if not exe:
            sys.exit("check.py needs google-chrome")
        self.profile = tempfile.mkdtemp(prefix="aok-docs-check-")
        self.proc = subprocess.Popen([
            exe, "--headless=new", "--remote-debugging-port=0", f"--user-data-dir={self.profile}",
            "--no-first-run", "--no-default-browser-check", "--disable-extensions", "--disable-sync",
            "--disable-background-networking", "--disable-component-update", "--mute-audio",
            "--hide-scrollbars", "--force-color-profile=srgb", "about:blank",
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        port_file = Path(self.profile) / "DevToolsActivePort"
        for _ in range(200):
            if port_file.exists() and port_file.read_text().strip():
                break
            time.sleep(0.05)
        port = port_file.read_text().split()[0]
        targets = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=10).read())
        page = next(t for t in targets if t.get("type") == "page")
        self.cdp = CDP(page["webSocketDebuggerUrl"])
        for domain in ("Page", "Runtime", "Log", "Network"):
            self.cdp.call(f"{domain}.enable")

    def close(self):
        try:
            self.proc.terminate()
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        shutil.rmtree(self.profile, ignore_errors=True)


# Runs in the page: overflow, contrast, structure. Returns a list of problems.
PAGE_PROBES = r"""
(() => {
  const out = [];
  const doc = document.documentElement;
  if (doc.scrollWidth > doc.clientWidth + 1) {
    let widest = null, right = doc.clientWidth;
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.right > right + 1 && r.width > 0) { right = r.right; widest = el; }
    }
    out.push('horizontal scroll: page is ' + doc.scrollWidth + 'px wide' +
      (widest ? ' (' + widest.tagName.toLowerCase() + '.' + [...widest.classList].join('.') + ')' : ''));
  }
  const parse = (c) => {
    let m = c.match(/^rgba?\(([^)]+)\)/);
    if (m) { const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; }
    m = c.match(/^color\(srgb ([^)]+)\)/);
    if (m) { const p = m[1].split(/[\s\/]+/).filter(Boolean).map(Number); return [p[0] * 255, p[1] * 255, p[2] * 255, p.length > 3 ? p[3] : 1]; }
    return null;
  };
  const blend = (top, under) => {
    const a = top[3];
    return [top[0] * a + under[0] * (1 - a), top[1] * a + under[1] * (1 - a), top[2] * a + under[2] * (1 - a), 1];
  };
  const lum = (c) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]);
  };
  const background = (el) => {
    const layers = [];
    for (let n = el; n; n = n.parentElement) {
      const s = getComputedStyle(n);
      if (s.backgroundImage && s.backgroundImage !== 'none' && !s.backgroundImage.startsWith('radial-gradient')) return null;
      const c = parse(s.backgroundColor);
      if (c && c[3] > 0) { layers.push(c); if (c[3] >= 1) break; }
    }
    let color = [255, 255, 255, 1];
    for (let i = layers.length - 1; i >= 0; i--) color = blend(layers[i], color);
    return color;
  };
  const seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const t = walker.currentNode;
    if (!t.textContent.trim()) continue;
    const el = t.parentElement;
    if (!el || seen.has(el)) continue;
    seen.add(el);
    if (el.closest('[aria-hidden="true"], .sr-only, template, script, style, noscript, [hidden]')) continue;
    const s = getComputedStyle(el);
    if (s.visibility === 'hidden' || s.display === 'none' || parseFloat(s.opacity) === 0) continue;
    const rect = el.getBoundingClientRect();
    if (!rect.width || !rect.height) continue;
    if (el.closest('button:disabled, input:disabled')) continue;
    const bg = background(el);
    const fg0 = parse(s.color);
    if (!bg || !fg0) continue;
    const fg = blend(fg0, bg);
    const l1 = lum(fg), l2 = lum(bg);
    const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    const size = parseFloat(s.fontSize), weight = parseInt(s.fontWeight, 10) || 400;
    const need = (size >= 24 || (size >= 18.66 && weight >= 700)) ? 3 : 4.5;
    if (ratio < need) {
      out.push('contrast ' + ratio.toFixed(2) + ' < ' + need + ': ' + el.tagName.toLowerCase() +
        (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : '') +
        ' "' + t.textContent.trim().slice(0, 40) + '"');
    }
  }
  return out;
})()
"""

STRUCTURE = r"""
(() => {
  const out = [];
  if (document.documentElement.lang !== 'en') out.push('html lang is not "en"');
  const h1 = document.querySelectorAll('h1');
  if (h1.length !== 1) out.push(h1.length + ' h1 elements');
  if (!document.querySelector('a.skip[href="#w-main"]')) out.push('no skip link');
  if (!document.querySelector('main#w-main')) out.push('no main landmark');
  if (!document.querySelector('header.site-header') || !document.querySelector('footer.site-footer')) out.push('no header or footer');
  for (const img of document.querySelectorAll('img')) if (!img.getAttribute('alt')) out.push('image without alt: ' + img.src);
  for (const el of document.querySelectorAll('[style]')) out.push('style attribute on ' + el.tagName.toLowerCase());
  for (const el of document.querySelectorAll('a[href], button')) {
    if (el.closest('[hidden], template')) continue;
    const s = getComputedStyle(el);
    if (s.display === 'none') continue;
    const name = (el.getAttribute('aria-label') || el.textContent || el.getAttribute('title') || '').trim();
    if (!name) out.push('no accessible name: ' + el.outerHTML.slice(0, 80));
  }
  const ids = {};
  for (const el of document.querySelectorAll('[id]')) { ids[el.id] = (ids[el.id] || 0) + 1; }
  for (const [id, n] of Object.entries(ids)) if (n > 1) out.push('id "' + id + '" used ' + n + ' times');
  for (const a of document.querySelectorAll('a[href^="#"]')) {
    const id = decodeURIComponent(a.getAttribute('href').slice(1));
    if (id && !document.getElementById(id)) out.push('link to missing #' + id);
  }
  const loaded = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, ''));
  for (const fam of ['Noto Sans', 'Lora']) if (!loaded.includes(fam)) out.push('font not loaded: ' + fam);
  const hangul = new RegExp('[' + String.fromCharCode(0x1100) + '-' + String.fromCharCode(0x11ff) + String.fromCharCode(0x3130) + '-' + String.fromCharCode(0x318f) + String.fromCharCode(0xac00) + '-' + String.fromCharCode(0xd7a3) + ']');
  if (hangul.test(document.body.innerText)) out.push('Hangul on the page');
  const links = [...document.querySelectorAll('a[href]')].map(a => a.href);
  const assets = [...document.querySelectorAll('link[href], script[src], img[src]')].map(n => n.href || n.src);
  return { problems: out, links, assets, html: document.documentElement.outerHTML.length };
})()
"""


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.refresh = [], set(), None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "meta" and (a.get("http-equiv") or "").lower() == "refresh":
            self.refresh = a.get("content")


def fetch(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.headers, r.read() if method == "GET" else b"", r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read(), url


class Checker:
    def __init__(self, base_url, args):
        self.base = base_url if base_url.endswith("/") else base_url + "/"
        self.origin = "{0.scheme}://{0.netloc}".format(urllib.parse.urlsplit(self.base))
        self.args = args
        self.problems = []
        self.links = {}      # url -> first page that linked it
        self.html_cache = {}

    def fail(self, where, what):
        self.problems.append(f"{where}: {what}")
        print(f"  FAIL {where}: {what}", flush=True)

    def internal(self, url):
        return url.startswith(self.base) or url == self.base.rstrip("/")

    def pages(self):
        """Pages to open: every page of the local build, or a crawl of the live site."""
        if self.args.only:
            return [urllib.parse.urljoin(self.base, p.lstrip("/")) for p in self.args.only]
        if self.args.build:
            build = Path(self.args.build)
            out = []
            for f in sorted(build.rglob("index.html")):
                rel = f.parent.relative_to(build).as_posix()
                if "http-equiv=\"refresh\"" in f.read_text(encoding="utf-8")[:2000]:
                    continue
                out.append(self.base + ("" if rel == "." else rel + "/"))
            return out
        seen, queue, out = set(), [self.base], []
        while queue and len(seen) < 800:
            url = queue.pop(0)
            if url in seen:
                continue
            seen.add(url)
            status, headers, body, final = fetch(url)
            if status != 200 or "text/html" not in (headers.get("Content-Type") or ""):
                continue
            p = LinkParser()
            p.feed(body.decode("utf-8", "replace"))
            if p.refresh:
                continue
            out.append(url)
            for href in p.links:
                nxt = urllib.parse.urljoin(url, href).split("#")[0]
                if self.internal(nxt) and nxt.endswith("/") and nxt not in seen:
                    queue.append(nxt)
        return out

    def open(self, chrome, url, width, theme):
        cdp = chrome.cdp
        cdp.call("Emulation.setDeviceMetricsOverride", width=width, height=900, deviceScaleFactor=1, mobile=width < 640)
        cdp.call("Emulation.setEmulatedMedia", features=[
            {"name": "prefers-color-scheme", "value": theme},
            {"name": "prefers-reduced-motion", "value": "reduce"},
        ])
        cdp.events.clear()
        cdp.call("Page.navigate", url=url)
        if not cdp.wait_for("Page.loadEventFired", 30):
            self.fail(url, "page did not finish loading")
        cdp.pump(0.4)
        cdp.js("document.fonts.ready.then(() => true)", await_promise=True)

    def console_problems(self, chrome, where, expect_404=False):
        for e in chrome.cdp.events:
            m, p = e.get("method"), e.get("params", {})
            if m == "Runtime.exceptionThrown":
                d = p.get("exceptionDetails", {})
                self.fail(where, f"script error: {d.get('exception', {}).get('description') or d.get('text')}")
            elif m == "Runtime.consoleAPICalled" and p.get("type") in ("error", "warning", "assert"):
                args = " ".join(str(a.get("value", a.get("description", ""))) for a in p.get("args", []))
                self.fail(where, f"console {p['type']}: {args[:200]}")
            elif m == "Log.entryAdded":
                entry = p.get("entry", {})
                text = entry.get("text", "")
                if expect_404 and "404" in text and entry.get("source") == "network":
                    continue
                if entry.get("level") in ("error", "warning") or "Content Security Policy" in text:
                    self.fail(where, f"{entry.get('source')} {entry.get('level')}: {text[:200]}")
            elif m == "Network.loadingFailed":
                if p.get("canceled"):
                    continue
                self.fail(where, f"request failed: {p.get('errorText')} {p.get('blockedReason') or ''}".strip())
            elif m == "Network.responseReceived":
                r = p.get("response", {})
                if r.get("status", 200) >= 400 and not (expect_404 and p.get("type") == "Document"):
                    self.fail(where, f"HTTP {r.get('status')} for {r.get('url')}")
                if not r.get("url", "").startswith((self.origin, "data:")):
                    self.fail(where, f"request to another site: {r.get('url')}")

    def check_page(self, chrome, url, shots):
        path = url[len(self.origin):]
        first = True
        for theme in THEMES:
            for width in self.args.widths:
                where = f"{path} @{width} {theme}"
                if first:
                    self.open(chrome, url, width, theme)
                    lost = chrome.cdp.js("document.body.classList.contains('kind-notfound')")
                    self.console_problems(chrome, where, expect_404=lost)
                    info = chrome.cdp.js(STRUCTURE)
                    for p in info["problems"]:
                        self.fail(path, p)
                    for link in info["links"] + info["assets"]:
                        # same-page anchors are checked in the page itself
                        if link.startswith(self.origin) and link.split("#")[0] != url:
                            self.links.setdefault(link, path)
                    first = False
                else:
                    chrome.cdp.call("Emulation.setDeviceMetricsOverride", width=width, height=900,
                                    deviceScaleFactor=1, mobile=width < 640)
                    chrome.cdp.call("Emulation.setEmulatedMedia", features=[
                        {"name": "prefers-color-scheme", "value": theme},
                        {"name": "prefers-reduced-motion", "value": "reduce"},
                    ])
                    chrome.cdp.pump(0.15)
                for p in chrome.cdp.js(PAGE_PROBES):
                    self.fail(where, p)
                if shots:
                    self.screenshot(chrome, shots, path, width, theme)

    def screenshot(self, chrome, folder, path, width, theme):
        cdp = chrome.cdp
        height = cdp.js("Math.min(document.documentElement.scrollHeight, 12000)")
        shot = cdp.call("Page.captureScreenshot", format="png", captureBeyondViewport=True,
                        clip={"x": 0, "y": 0, "width": width, "height": height, "scale": 1})
        name = (path.strip("/").replace("/", "_") or "home") + f"-{width}-{theme}.png"
        Path(folder, name).write_bytes(base64.b64decode(shot["data"]))
        cdp.call("Emulation.setDeviceMetricsOverride", width=width, height=900, deviceScaleFactor=1, mobile=width < 640)

    def check_links(self):
        print(f"links: {len(self.links)} same-site addresses", flush=True)
        for url, page in sorted(self.links.items()):
            target, _, frag = url.partition("#")
            if target not in self.html_cache:
                status, headers, body, _final = fetch(target)
                self.html_cache[target] = (status, headers, body)
            status, headers, body = self.html_cache[target]
            if status != 200:
                self.fail(page, f"link {url}: HTTP {status}")
                continue
            if frag and "text/html" in (headers.get("Content-Type") or ""):
                p = LinkParser()
                p.feed(body.decode("utf-8", "replace"))
                if urllib.parse.unquote(frag) not in p.ids:
                    self.fail(page, f"link {url}: no id #{frag} on that page")

    def check_server(self):
        """Redirects, the 404 page and the headers of the server."""
        status, headers, body, _ = fetch(self.base + "no-such-page-here/")
        if status != 404:
            self.fail("404", f"a missing page answers {status}, not 404")
        elif b'class="kind-notfound"' not in body:
            self.fail("404", "a missing page does not show the wiki's 404 page")
        for name in ("Content-Security-Policy", "X-Content-Type-Options", "X-Frame-Options", "Referrer-Policy",
                     "Permissions-Policy", "Cross-Origin-Opener-Policy", "X-Robots-Tag"):
            for probe in (self.base, self.base + "no-such-page-here/"):
                st, h, _, _ = fetch(probe)
                if not h.get(name):
                    self.fail("headers", f"{probe} has no {name}")
        if self.base.startswith("https://"):
            st, h, _, _ = fetch(self.base)
            if not h.get("Strict-Transport-Security"):
                self.fail("headers", "no Strict-Transport-Security")
        bare = self.base.rstrip("/")
        if bare != self.origin:
            req = urllib.request.Request(bare, headers={"User-Agent": UA})
            opener = urllib.request.build_opener(NoRedirect)
            try:
                opener.open(req, timeout=20)
                self.fail("redirect", f"{bare} does not redirect")
            except urllib.error.HTTPError as e:
                if e.code != 301 or not e.headers.get("Location", "").endswith(urllib.parse.urlsplit(self.base).path):
                    self.fail("redirect", f"{bare} answers {e.code} {e.headers.get('Location')}")

    def check_aliases(self):
        """Every alias page of the build forwards to a page that answers. For a
        live address the alias list comes from the local build/ when it was
        built for the same base."""
        build = Path(self.args.build) if self.args.build else serve.BUILD
        if not self.args.build:
            if serve.build_base(build) != urllib.parse.urlsplit(self.base).path or not (build / "index.html").exists():
                return
        for f in sorted(build.rglob("index.html")):
            head = f.read_text(encoding="utf-8")[:2000]
            if 'http-equiv="refresh"' not in head:
                continue
            rel = f.parent.relative_to(build).as_posix()
            url = self.base + rel + "/"
            status, headers, body, _ = fetch(url)
            p = LinkParser()
            p.feed(body.decode("utf-8", "replace"))
            target = (p.refresh or "").split("url=", 1)[-1]
            if status != 200 or not target:
                self.fail(url, "alias page does not forward")
                continue
            st, _, _, _ = fetch(urllib.parse.urljoin(url, target))
            if st != 200:
                self.fail(url, f"alias target {target} answers {st}")

    def interactions(self, chrome, pages):
        """Search by keyboard, the menu on a phone, the copy button, the 404 page."""
        cdp = chrome.cdp
        doc = None
        for u in pages:
            if u == self.base or any(k in u for k in ("/sections/", "all-pages", "recent-changes")):
                continue
            status, _, body, _ = fetch(u)
            if status == 200 and b'class="kind-page"' in body:
                doc = u
                break
        if doc:
            self.open(chrome, doc, 1440, "light")
            cdp.events.clear()
            press(cdp, "/")
            focused = cdp.js("document.activeElement && document.activeElement.id")
            if focused != "w-search":
                self.fail("keyboard", f'"/" does not focus the search (focus: {focused})')
            word = cdp.js("(document.querySelector('.doc-title').textContent.match(/[A-Za-z]{4,}/) || ['docs'])[0]")
            cdp.call("Input.insertText", text=word.lower())
            cdp.pump(0.8)
            n = cdp.js("document.querySelectorAll('#w-search-list [role=option]').length")
            if not n:
                self.fail("search", f'no results for "{word}"')
            else:
                before = cdp.js("location.href")
                press(cdp, "ArrowDown")
                press(cdp, "Enter")
                cdp.pump(1.2)
                if cdp.js("location.href") == before and n > 1:
                    self.fail("search", "Enter on a result does not open it")
            self.console_problems(chrome, "search")
            self.open(chrome, doc, 390, "light")
            cdp.events.clear()
            cdp.js("document.querySelector('[data-menu]').click()")
            cdp.pump(0.3)
            if not cdp.js("document.getElementById('w-sidebar').classList.contains('is-open') && "
                          "getComputedStyle(document.getElementById('w-sidebar')).display !== 'none'"):
                self.fail("menu", "the menu button does not open the sidebar at 390 px")
            press(cdp, "Escape")
            cdp.pump(0.2)
            if cdp.js("document.getElementById('w-sidebar').classList.contains('is-open')"):
                self.fail("menu", "Escape does not close the menu")
            cdp.js("document.querySelector('[data-search-open]') && document.querySelector('[data-search-open]').click()")
            cdp.pump(0.3)
            if not cdp.js("document.activeElement && document.activeElement.id === 'w-search'"):
                self.fail("search", "the search button does not open the search at 390 px")
            for p in cdp.js(PAGE_PROBES):
                self.fail("search @390", p)
            self.console_problems(chrome, "menu")
        code_page = None
        for u in pages:
            if self.html_cache.get(u.split("#")[0], (0, {}, b""))[2].find(b'class="code"') >= 0:
                code_page = u
                break
        if code_page:
            self.open(chrome, code_page, 1440, "light")
            cdp.call("Browser.grantPermissions", permissions=["clipboardReadWrite", "clipboardSanitizedWrite"],
                     origin=self.origin)
            cdp.call("Emulation.setFocusEmulationEnabled", enabled=True)
            cdp.events.clear()
            cdp.js("document.querySelector('.code-copy').click()")
            cdp.pump(0.4)
            if not cdp.js("document.querySelector('.code-copy').classList.contains('is-done')"):
                self.fail("copy", f"the copy button on {code_page} does not copy")
            self.console_problems(chrome, "copy")
        self.open(chrome, self.base + "staking-rewards-missing/", 1440, "light")
        self.console_problems(chrome, "404", expect_404=True)
        cdp.pump(0.6)
        if not cdp.js("document.body.classList.contains('kind-notfound')"):
            self.fail("404", "missing page does not show the 404 page in the browser")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


KEYS = {"ArrowDown": 40, "ArrowUp": 38, "Enter": 13, "Escape": 27, "/": 191}


def press(cdp, key):
    code = KEYS[key]
    base = {"key": key, "windowsVirtualKeyCode": code, "nativeVirtualKeyCode": code}
    if key == "/":
        cdp.call("Input.dispatchKeyEvent", type="keyDown", text="/", code="Slash", **base)
    else:
        cdp.call("Input.dispatchKeyEvent", type="rawKeyDown", code=key, **base)
    cdp.call("Input.dispatchKeyEvent", type="keyUp", **base)
    cdp.pump(0.15)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the wiki in headless Chrome.")
    ap.add_argument("url", nargs="?", help="a wiki address, such as https://web.aok.network/doc/ (default: serve build/)")
    ap.add_argument("--build", type=Path, default=None, help="the build to serve (default build/)")
    ap.add_argument("--only", action="append", help="check only this page path (repeatable)")
    ap.add_argument("--widths", default=",".join(map(str, WIDTHS)))
    ap.add_argument("--shots", type=Path, help="save a full-page screenshot of every page, width and theme here")
    args = ap.parse_args(argv)
    args.widths = [int(w) for w in args.widths.split(",")]
    server = None
    if args.url:
        base_url = args.url
        args.build = None
    else:
        args.build = args.build or serve.BUILD
        if not (Path(args.build) / "index.html").exists():
            sys.exit("build/ is empty: run tools/build.py first")
        server, base_url = serve.start(0, Path(args.build))
    if args.shots:
        args.shots.mkdir(parents=True, exist_ok=True)
    checker = Checker(base_url, args)
    chrome = Chrome()
    try:
        pages = checker.pages()
        print(f"{base_url}: {len(pages)} pages at {', '.join(map(str, args.widths))} px, light and dark", flush=True)
        for url in pages:
            print(f"page {url[len(checker.origin):]}", flush=True)
            checker.check_page(chrome, url, args.shots)
        checker.check_links()
        checker.check_aliases()
        checker.check_server()
        checker.interactions(chrome, pages)
    finally:
        chrome.close()
        if server:
            server.shutdown()
    if checker.problems:
        print(f"\n{len(checker.problems)} problems", file=sys.stderr)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
