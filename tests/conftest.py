import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from wikilib import config  # noqa: E402
from wikilib.site import Site  # noqa: E402


def page(title, body, order=1, description=None, **extra):
    """The text of a page file with front matter."""
    lines = ["---", f"title: {title}", f"description: {description or 'A page for the tests.'}", f"order: {order}"]
    for key, value in extra.items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + textwrap.dedent(body).strip() + "\n"


@pytest.fixture
def build(tmp_path):
    """build({"staking/offline.md": page(...)}) -> the built Site (BuildError on problems)."""

    def run(files, base="/doc/", assets=None):
        pages = tmp_path / "content" / "pages"
        for rel, text in files.items():
            f = pages / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(text, encoding="utf-8")
        for rel, data in (assets or {}).items():
            f = tmp_path / "content" / "assets" / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(data)
        cfg = config.load(base=base)
        return Site(cfg, [pages], tmp_path / "out").build()

    return run


@pytest.fixture
def out(tmp_path):
    def read(rel):
        return (tmp_path / "out" / rel).read_text(encoding="utf-8")
    return read
