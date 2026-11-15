import pytest

from conftest import page
from wikilib.config import BuildError


def test_alias_page_forwards(build, out):
    site = build({"node/run-a-node.md": page("Run a node", "Text.", aliases="[node, full-node]")})
    assert sorted(site.aliases) == ["full-node", "node"]
    html = out("node/index.html")
    assert '<meta http-equiv="refresh" content="0; url=/doc/run-a-node/">' in html
    assert '<link rel="canonical" href="https://web.aok.network/doc/run-a-node/">' in html
    assert '<a href="/doc/run-a-node/">Run a node</a>' in html
    assert 'name="robots" content="noindex' in html


def test_canonical_follows_the_base(build, out):
    build({"node/run-a-node.md": page("Run a node", "Text.", aliases="[node]")}, base="/")
    assert '<link rel="canonical" href="https://docs.aok.network/run-a-node/">' in out("node/index.html")


def test_wiki_link_to_an_alias_goes_to_the_page(build, out):
    build({"node/run-a-node.md": page("Run a node", "Text.", aliases="[node]"),
           "start/intro.md": page("Intro", "[[node]]")})
    assert '<a href="/doc/run-a-node/">Run a node</a>' in out("intro/index.html")


def test_duplicate_alias_fails(build):
    with pytest.raises(BuildError) as e:
        build({"node/a.md": page("A", "x", aliases="[old]"), "node/b.md": page("B", "x", order=2, aliases="[old]")})
    assert any("alias 'old' is already an alias" in m for m in e.value.messages)


def test_alias_equal_to_a_slug_fails(build):
    with pytest.raises(BuildError) as e:
        build({"node/a.md": page("A", "x", aliases="[b]"), "node/b.md": page("B", "x", order=2)})
    assert any("alias 'b' is the slug of" in m for m in e.value.messages)


def test_duplicate_slug_fails(build):
    with pytest.raises(BuildError) as e:
        build({"node/same.md": page("A", "x"), "wallets/same.md": page("B", "x")})
    assert any("slug 'same' is already used" in m for m in e.value.messages)


def test_reserved_slug_fails(build):
    with pytest.raises(BuildError) as e:
        build({"node/all-pages.md": page("All", "x")})
    assert any("used by the wiki itself" in m for m in e.value.messages)
