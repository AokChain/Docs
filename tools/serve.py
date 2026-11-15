#!/usr/bin/env python3
"""Serve build/ locally the way the web server does: under the base path,
with the same security headers (CSP and the rest), the same redirects
(/doc to /doc/, /docs/... to /doc/...) and the wiki's 404 page. HSTS and
upgrade-insecure-requests are left out on plain http. Standard library only.

    python3 tools/serve.py              # http://127.0.0.1:8770/doc/
    python3 tools/serve.py 8800
"""
import functools
import http.server
import json
import mimetypes
import re
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"

# The headers the server block sends with every response.
CSP = ("default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; "
       "connect-src 'self' https://v3.aokscan.com; manifest-src 'self'; base-uri 'none'; "
       "form-action 'none'; frame-ancestors 'none'; upgrade-insecure-requests")
HEADERS = {
    "Content-Security-Policy": CSP,
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Strict-Transport-Security": "max-age=15552000",
    "X-Robots-Tag": "noindex, nofollow",
}
FINGERPRINTED = re.compile(r"/assets/(?:fonts/)?[^/]+\.[0-9a-f]{10}\.(?:css|js|json|svg|png|woff2)$")
TYPES = {".woff2": "font/woff2", ".json": "application/json", ".svg": "image/svg+xml",
         ".js": "text/javascript", ".css": "text/css", ".txt": "text/plain", ".ico": "image/x-icon"}


def build_base(build=BUILD):
    try:
        return json.loads((build / ".wiki-build.json").read_text())["base"]
    except (OSError, ValueError, KeyError):
        return "/doc/"


class Handler(http.server.SimpleHTTPRequestHandler):
    base = "/doc/"
    build = BUILD

    def end_headers(self):
        for name, value in HEADERS.items():
            if name == "Strict-Transport-Security":
                continue
            if name == "Content-Security-Policy":
                value = value.replace("; upgrade-insecure-requests", "")
            self.send_header(name, value)
        super().end_headers()

    def guess_type(self, path):
        return TYPES.get(Path(str(path)).suffix.lower()) or mimetypes.guess_type(str(path))[0] or "application/octet-stream"

    def redirect(self, location):
        self.send_response(301)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def send_head(self):
        path, sep, query = self.path.partition("?")
        base = self.base
        if base != "/":
            bare = base.rstrip("/")
            if path == bare:
                return self.redirect(base + sep + query)
            if path == "/docs" or path.startswith("/docs/"):
                return self.redirect(base + path[len("/docs/"):] + sep + query)
            if path == "/":
                return self.redirect(base)
            if not path.startswith(base):
                self.send_error(404)
                return None
        rel = path[len(base):]
        if any(part.startswith(".") for part in rel.split("/") if part):
            self.send_error(404)
            return None
        target = self.build / rel
        if target.is_dir():
            if not (target / "index.html").exists():
                self.send_error(404)
                return None
            if not path.endswith("/"):
                return self.redirect(path + "/" + sep + query)
        self.path = "/" + rel + (sep + query if sep else "")
        return super().send_head()

    def send_response(self, code, message=None):
        super().send_response(code, message)
        if code == 200:
            immutable = FINGERPRINTED.search(self.path.partition("?")[0])
            self.send_header("Cache-Control", "max-age=31536000" if immutable else "no-cache")

    def send_error(self, code, message=None, explain=None):
        page = self.build / "404.html"
        if code != 404 or not page.exists():
            return super().send_error(code, message, explain)
        body = page.read_bytes()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def log_message(self, *args):
        pass


def make_server(port=0, build=BUILD):
    """A threaded server on 127.0.0.1 (port 0 picks a free one) and its wiki URL."""
    handler = type("BoundHandler", (Handler,), {"base": build_base(build), "build": Path(build)})
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(handler, directory=str(build)))
    return server, f"http://127.0.0.1:{server.server_address[1]}{handler.base}"


def start(port=0, build=BUILD):
    """make_server() running in a background thread."""
    server, url = make_server(port, build)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, url


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8770
    if not (BUILD / "index.html").exists():
        sys.exit("build/ is empty: run tools/build.py first")
    server, url = make_server(port)
    print(f"{url} (build/, production headers); Ctrl+C stops")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
