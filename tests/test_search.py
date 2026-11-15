import json

from conftest import page


def load_index(site, tmp_path):
    name = site.assets["search"].rsplit("/", 1)[1]
    return json.loads((tmp_path / "out" / "assets" / name).read_text(encoding="utf-8"))


def test_index_has_every_page(build, tmp_path):
    site = build({
        "staking/offline-staking.md": page("Offline staking", """
            Intro text about keys.
            ## Set it up
            Create a `staking address` first.
            ### On the node
            Run the command.
        """, description="Let another node stake your coins."),
        "node/run-a-node.md": page("Run a node", "Install it."),
    })
    data = load_index(site, tmp_path)
    assert data["v"] == 1
    by_url = {p["u"]: p for p in data["pages"]}
    p = by_url["/doc/offline-staking/"]
    assert p["t"] == "Offline staking"
    assert p["s"] == "Staking"
    assert p["d"] == "Let another node stake your coins."
    assert p["h"] == [["Set it up", "set-it-up"], ["On the node", "on-the-node"]]
    assert p["x"][0] == ["", "Intro text about keys."]
    assert ["set-it-up", "Create a staking address first."] in p["x"]
    assert "/doc/run-a-node/" in by_url


def test_index_file_name_changes_with_content(build, tmp_path):
    a = build({"node/a.md": page("A", "One.")}).assets["search"]
    b = build({"node/a.md": page("A", "Two.")}).assets["search"]
    assert a != b and a.startswith("/doc/assets/search.") and a.endswith(".json")


def test_index_is_linked_from_every_page(build, out):
    site = build({"node/a.md": page("A", "One.")})
    for rel in ("index.html", "a/index.html", "all-pages/index.html", "404.html"):
        assert f'data-index="{site.assets["search"]}"' in out(rel)


def test_long_pages_are_cut(build, tmp_path):
    long = "word " * 3000
    site = build({"node/a.md": page("A", f"## Part\n{long}")})
    text = load_index(site, tmp_path)["pages"][0]["x"]
    assert all(len(body) <= 2000 for _anchor, body in text)
