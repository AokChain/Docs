import re

import pytest

from conftest import page
from wikilib import checks
from wikilib.config import BuildError


def problems(build, files, **kw):
    with pytest.raises(BuildError) as e:
        build(files, **kw)
    return e.value.messages


def test_hangul_fails(build):
    msgs = problems(build, {"start/a.md": page("A", chr(0xC548) + chr(0xB155))})
    assert any("Hangul" in m for m in msgs)


def test_email_fails_but_ssh_remote_is_fine(build):
    msgs = problems(build, {"start/a.md": page("A", "Write to someone@example.com")})
    assert any("email address" in m for m in msgs)
    build({"start/a.md": page("A", "`git clone git@github.com:AokChain/AokChain.git`")})


# Built at run time, so the repository itself holds no private addresses.
PRIVATE_SAMPLES = [".".join(map(str, parts)) for parts in ((10, 20, 30, 40), (172, 20, 1, 2), (172, 31, 255, 255), (192, 168, 100, 200))]


@pytest.mark.parametrize("ip", PRIVATE_SAMPLES)
def test_private_ip_fails(ip):
    assert any("private IP" in p for p in checks.text_problems(f"rpcallowip={ip}"))


@pytest.mark.parametrize("text", ["rpcallowip=127.0.0.1", "172.32.0.1", "192.0.2.10", "version 10.15.7", "110.0.0.1"])
def test_not_private(text):
    assert not checks.text_problems(text)


def test_blocked_words(monkeypatch):
    monkeypatch.setattr(checks, "_BLOCKED_RE", re.compile("forbiddenname", re.IGNORECASE))
    assert any("blocked word" in p for p in checks.text_problems("Made with ForbiddenName"))
    assert not checks.text_problems("Made with care")


def test_front_matter_rules(build):
    msgs = problems(build, {
        "start/a.md": "---\ntitle: A\norder: 1\n---\n\nText.\n",
        "start/b.md": page("B", "Text.", description="x" * 161),
        "start/c.md": page("C", "Text.", order=2, colour="teal"),
        "start/d.md": "---\ntitle: D\ndescription: Fine.\norder: first\n---\n",
        "start/e.md": "No front matter here.\n",
    })
    joined = "\n".join(msgs)
    assert "a.md: front matter: description is missing" in joined
    assert "b.md: front matter: description has 161 characters, at most 160" in joined
    assert "c.md: unknown front matter field 'colour'" in joined
    assert "d.md: front matter: order must be a whole number" in joined
    assert "e.md:1: no front matter" in joined


def test_section_must_exist(build):
    msgs = problems(build, {"cooking/a.md": page("A", "x")})
    assert any("no section 'cooking' in sections.yml" in m for m in msgs)


def test_h1_in_body_fails(build):
    msgs = problems(build, {"start/a.md": page("A", "# Another title\n\nText.")})
    assert any("H1 heading 'Another title'" in m for m in msgs)


def test_image_rules(build):
    msgs = problems(build, {"start/a.md": page("A", "![](/assets/img/x.png) ![x](https://example.com/x.png) ![y](/assets/img/none.png)")},
                    assets={"img/x.png": b"\x89PNG\r\n\x1a\n" + b"\0" * 32})
    joined = "\n".join(msgs)
    assert "has no alt text" in joined
    assert "images come from this site" in joined
    assert "image /assets/img/none.png: no such file" in joined


def test_image_gets_base_and_size(build, out):
    png = b"\x89PNG\r\n\x1a\n\0\0\0\rIHDR" + (640).to_bytes(4, "big") + (360).to_bytes(4, "big") + b"\0" * 8
    build({"start/a.md": page("A", "![The wallet](/assets/img/w.png)")}, assets={"img/w.png": png})
    assert '<img src="/doc/assets/img/w.png" alt="The wallet" width="640" height="360"' in out("a/index.html")


def test_raw_html_rules(build):
    msgs = problems(build, {"start/a.md": page("A", '<script>x()</script>\n\n<details open style="color:red"><summary>More</summary>x</details>')})
    joined = "\n".join(msgs)
    assert "<script> is not allowed" in joined
    assert "attribute 'style' on <details> is not allowed" in joined


def test_allowed_html_and_comments(build, out):
    build({"start/a.md": page("A", "Press <kbd>Ctrl</kbd>.\n\n<!-- a note for writers -->\n\n<details><summary>More</summary>\n\nHidden.\n\n</details>")})
    html = out("a/index.html")
    assert "<kbd>Ctrl</kbd>" in html and "<details>" in html
    assert "a note for writers" not in html


def test_unknown_code_language_fails(build):
    msgs = problems(build, {"start/a.md": page("A", "```klingon\nqapla\n```")})
    assert any("unknown code language 'klingon'" in m for m in msgs)


def test_code_is_highlighted_without_inline_styles(build, out):
    build({"start/a.md": page("A", '```json\n{"a": 1}\n```\n\n| n | v |\n|--:|:-:|\n| 1 | 2 |')})
    html = out("a/index.html")
    assert '<span class="nt">"a"</span>' in html
    assert 'class="ta-right"' in html and 'class="ta-center"' in html
    assert "style=" not in html


def test_callouts(build, out):
    build({"start/a.md": page("A", "> [!WARNING]\n> Keep a backup.")})
    html = out("a/index.html")
    assert '<div class="callout callout-warning" role="note">' in html
    assert '<use href="#i.exclamation-triangle"/></svg>Warning</p>' in html
    assert '<symbol id="i.exclamation-triangle"' in html
