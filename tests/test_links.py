import re

import pytest

from conftest import page
from wikilib.config import BuildError

TARGET = page("Offline staking", """
    ## Set it up
    Steps.
    ## Stop
    More.
""")


def test_wiki_link_takes_the_title(build, out):
    build({"staking/offline-staking.md": TARGET,
           "start/intro.md": page("Intro", "See [[offline-staking]].")})
    html = out("intro/index.html")
    assert '<a href="/doc/offline-staking/">Offline staking</a>' in html


def test_wiki_link_with_text_and_anchor(build, out):
    build({"staking/offline-staking.md": TARGET,
           "start/intro.md": page("Intro", "[[offline-staking|staking for others]] and [[offline-staking#stop|how to stop]]")})
    html = out("intro/index.html")
    assert '<a href="/doc/offline-staking/">staking for others</a>' in html
    assert '<a href="/doc/offline-staking/#stop">how to stop</a>' in html


def test_wiki_link_anchor_without_text_takes_the_heading(build, out):
    build({"staking/offline-staking.md": TARGET,
           "start/intro.md": page("Intro", "[[offline-staking#set-it-up]]")})
    assert '<a href="/doc/offline-staking/#set-it-up">Set it up</a>' in out("intro/index.html")


def test_link_to_an_anchor_on_the_same_page(build, out):
    build({"staking/offline-staking.md": page("Offline staking", """
        Jump to [[#stop|the end]] or [the end](#stop).
        ## Stop
    """)})
    html = out("offline-staking/index.html")
    assert '<a href="#stop">the end</a>' in html


def test_wiki_link_under_another_base(build, out):
    build({"staking/offline-staking.md": TARGET, "start/intro.md": page("Intro", "[[offline-staking]]")}, base="/")
    assert '<a href="/offline-staking/">Offline staking</a>' in out("intro/index.html")


def test_missing_page_fails(build):
    with pytest.raises(BuildError) as e:
        build({"start/intro.md": page("Intro", "See [[no-such-page]].")})
    assert any("broken wiki link [[no-such-page]]" in m for m in e.value.messages)


def test_missing_anchor_fails(build):
    with pytest.raises(BuildError) as e:
        build({"staking/offline-staking.md": TARGET,
               "start/intro.md": page("Intro", "[[offline-staking#nowhere]]")})
    assert any("no heading #nowhere in offline-staking" in m for m in e.value.messages)


def test_missing_local_anchor_fails(build):
    with pytest.raises(BuildError) as e:
        build({"start/intro.md": page("Intro", "[up](#top-of-page)")})
    assert any("#top-of-page" in m for m in e.value.messages)


def test_root_relative_links_get_the_base(build, out):
    build({"staking/offline-staking.md": TARGET,
           "start/intro.md": page("Intro", "[all](/all-pages/) and [stop](/offline-staking/#stop)")})
    html = out("intro/index.html")
    assert 'href="/doc/all-pages/"' in html
    assert 'href="/doc/offline-staking/#stop"' in html


def test_relative_md_links_fail(build):
    with pytest.raises(BuildError) as e:
        build({"start/intro.md": page("Intro", "[x](../staking/offline-staking.md)")})
    assert any("relative link" in m for m in e.value.messages)


def test_external_links_get_the_arrow(build, out):
    build({"start/intro.md": page("Intro", "The [explorer](https://v3.aokscan.com/) and https://github.com/AokChain")})
    html = out("intro/index.html")
    assert re.search(r'<a href="https://v3.aokscan.com/" class="ext">explorer<svg class="icon icon-ext"', html)
    assert 'href="https://github.com/AokChain"' in html


def test_backlinks(build, out):
    build({"staking/offline-staking.md": TARGET,
           "start/intro.md": page("Intro", "[[offline-staking]] twice: [[offline-staking#stop]]"),
           "start/other.md": page("Other", "[[offline-staking]]", order=2)})
    html = out("offline-staking/index.html")
    section = html.split('id="w-backlinks"', 1)[1].split("</section>", 1)[0]
    assert section.count("<li>") == 2
    assert section.index("Intro") < section.index("Other")
