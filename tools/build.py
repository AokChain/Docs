#!/usr/bin/env python3
"""Build the wiki into build/.

    .venv/bin/python tools/build.py                    # base /doc/ (web.aok.network/doc/)
    .venv/bin/python tools/build.py --base /           # for docs.aok.network
    .venv/bin/python tools/build.py --pages ../other/pages --pages pages

--pages may be given more than once; the pages of all directories are built
together (slugs stay unique across them). Images come from the assets/
folder next to each pages directory. Any problem in any page stops the
build with a message per problem; nothing is written then.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from wikilib import config  # noqa: E402
from wikilib.config import BuildError  # noqa: E402
from wikilib.site import Site  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the AokChain wiki.")
    ap.add_argument("--base", help="URL path the wiki is served under (default: base in wiki.yml)")
    ap.add_argument("--pages", action="append", type=Path,
                    help="pages directory (repeatable, default ./pages)")
    ap.add_argument("--out", type=Path, default=config.ROOT / "build", help="output directory (default build/)")
    ap.add_argument("--launch", action="store_true",
                    help="the addresses of the launch (the launch mapping of wiki.yml) in place of the test ones")
    args = ap.parse_args(argv)
    try:
        cfg = config.load(base=args.base, launch=args.launch)
        site = Site(cfg, args.pages or [Path("pages")], args.out).build()
    except BuildError as e:
        print(f"build failed: {len(e.messages)} problem{'s' if len(e.messages) != 1 else ''}", file=sys.stderr)
        for m in e.messages:
            print(f"  {m}", file=sys.stderr)
        return 1
    for w in site.warnings:
        print(f"warning: {w}", file=sys.stderr)
    print(f"built {len(site.pages)} pages, {len(site.aliases)} aliases into {args.out} (base {cfg.base})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
