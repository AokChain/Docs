import pytest

from conftest import page
from wikilib.slug import Slugger, slugify


@pytest.mark.parametrize("text, slug", [
    ("Run a node", "run-a-node"),
    ("What's new in 4.0?", "whats-new-in-40"),
    ("getblock (RPC)", "getblock-rpc"),
    ("Tokens & sub tokens", "tokens--sub-tokens"),
    ("  Trimmed  ", "trimmed"),
    ("snake_case stays", "snake_case-stays"),
    ("-rpcport and -rpcbind", "-rpcport-and--rpcbind"),
    ("Mjölnir", "mjölnir"),
])
def test_slugify_like_github(text, slug):
    assert slugify(text) == slug


def test_repeated_headings_are_numbered():
    s = Slugger()
    assert [s.slug("Example"), s.slug("Example"), s.slug("Example")] == ["example", "example-1", "example-2"]


def test_numbered_heading_does_not_collide():
    s = Slugger()
    assert [s.slug("Example 1"), s.slug("Example"), s.slug("Example")] == ["example-1", "example", "example-2"]


def test_template_ids_are_kept_free():
    assert Slugger(["w-main"]).slug("W main") == "w-main-1"


def test_heading_ids_in_pages(build, out):
    build({"node/config.md": page("Config", """
        ## The `rpcport` option
        ### Example
        ## Other
        ### Example
    """)})
    html = out("config/index.html")
    assert '<h2 id="the-rpcport-option"><a class="h-anchor" href="#the-rpcport-option">' in html
    assert 'id="example"' in html and 'id="example-1"' in html
    toc = html.split('<nav class="toc"', 1)[1]
    assert 'href="#the-rpcport-option"' in toc and 'href="#example-1"' in toc


def test_heading_with_a_link_is_not_wrapped(build, out):
    build({"node/a.md": page("A", "## See [[b]]"), "node/b.md": page("B", "Text.", order=2)})
    html = out("a/index.html")
    assert '<h2 id="see-b">See <a href="/doc/b/">B</a></h2>' in html
