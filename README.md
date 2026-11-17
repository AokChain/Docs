# AokChain Docs

The AokChain documentation as a wiki: Markdown pages in `pages/`, built into a static site by `tools/build.py`. It is served under the AOK website at `/doc/`, built from this repository, and carries the website's menu and footer.

The site is plain HTML, CSS and a little JavaScript, with the design of the AOK website. It needs no server-side code and makes no third-party requests.

## Layout

| Path | What |
|---|---|
| `pages/<section>/<slug>.md` | The pages, one file each. The folder is the section |
| `assets/img/` | Images used by the pages |
| `sections.yml` | The sections, in the order the sidebar and the home page show them |
| `wiki.yml` | Name, base path, the addresses of the website, the block explorer and the API, the website's menu and footer, the section icons |
| `tools/build.py` | Builds `build/` (the `wikilib` package next to it does the work) |
| `tools/check.py` | Opens the built site in headless Chrome and checks every page |
| `tools/serve.py` | Serves `build/` locally with the production headers |
| `tools/deploy.sh` | Copies `build/` to the web server |
| `theme/` | Templates, CSS, JavaScript, fonts and icons |
| `tests/` | Tests (`python -m pytest`) and the fixture pages they and the theme work use |

## Writing a page

Create `pages/<section id>/<slug>.md`. The section ids are in `sections.yml`. The page is published at `<base>/<slug>/`, so slugs are unique across the whole wiki: lowercase words joined by hyphens.

```markdown
---
title: Offline staking
description: Let another node stake your AOK while the coins stay in your wallet.
order: 2
aliases: [staking-offline]
---

The text starts here. The title is the only H1, so sections start at ##.

## Set it up
```

Front matter:

| Field | |
|---|---|
| `title` | Required. At most 80 characters |
| `description` | Required. One sentence, at most 160 characters. Shown in search results, link previews and section listings |
| `order` | Required. A whole number: the position in the section |
| `aliases` | Optional. Old slugs that redirect to this page |
| `generated_by` | Optional. For generated pages, such as `tools/rpc_reference.py`: the page shows where it comes from instead of an edit link |

The body is GitHub-flavored Markdown: tables, strikethrough, autolinks, task lists and footnotes. Also:

- Addresses of the services: write `@@site@@`, `@@explorer@@` and `@@api@@` (the API's base address), or `@@site_host@@` and `@@explorer_host@@` for the name alone, instead of the address itself: `[@@site_host@@/download](@@site@@/download/)`, `curl -s @@api@@/status`. The build puts in the addresses of `wiki.yml`, so no page changes when a service moves.
- Wiki links: `[[slug]]` (the link text is the page's title), `[[slug|text]]`, `[[slug#anchor|text]]` and `[[#anchor|text]]` on the same page. Anchors are GitHub's: lowercase, spaces become hyphens, punctuation is dropped.
- Callouts: `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]` and `> [!CAUTION]` on the first line of a quote.
- Code: fenced blocks with a language (`bash`, `ini`, `json`, `text` and any other Pygments name) are highlighted at build time and get a copy button.
- Images: `![what the image shows](/assets/img/name.png)`. Paths start at the wiki root; the base is added. Alt text is required.
- Links to other wiki addresses may be written from the root too: `[All pages](/all-pages/)`.
- Raw HTML is limited to `details`, `summary`, `kbd`, `br`, `sub`, `sup` and `abbr`. HTML comments are dropped.

The build stops with one message per problem when a page:

- holds Hangul (the wiki is English only), an email address, a private IP address (examples use `127.0.0.1` or `192.0.2.x`) or a blocked word;
- misses a front matter field, has one that is too long or unknown, or repeats a slug or an alias;
- links to a page or a heading that does not exist, links relatively (`../x.md`), or has an image without alt text or from another site;
- has an H1 in its body, an unknown code language, or HTML outside the short list.

The wiki makes the rest: the sidebar, breadcrumbs, "On this page", previous and next within the section, "Linked from", "Last updated" (from git), edit and history links, section pages, All pages, Recent changes (from the git log of `pages/`), redirect pages for aliases, the 404 page and the search index.

## Build, check, deploy

```sh
python3 -m venv .venv            # once; or bootstrap pip into the venv if ensurepip is missing
.venv/bin/pip install -r requirements-dev.txt

.venv/bin/python tools/build.py                  # base /doc/, pages from ./pages
.venv/bin/python tools/build.py --base /         # for docs.aok.network
.venv/bin/python tools/build.py --pages tests/fixtures/pages     # the fixture pages
.venv/bin/python tools/build.py --pages ../a/pages --pages ../b/pages   # several page folders together

.venv/bin/python tools/serve.py                  # http://127.0.0.1:8770/doc/ with the production headers
.venv/bin/python tools/check.py                  # every page at 1440, 1024, 390 and 360 px, light and dark
.venv/bin/python tools/check.py --site http://127.0.0.1:8765   # follow the links into the website on a local copy of it
.venv/bin/python tools/check.py https://web.aok.network/doc/
.venv/bin/python -m pytest

tools/deploy.sh
```

`tools/check.py` fails on console errors, Content Security Policy violations, failed requests, requests to other sites, horizontal scrolling, text contrast below WCAG AA, missing fonts, links or anchors that do not answer, alias pages that do not forward, and a 404 page or headers that are not right. `--shots DIR` saves a screenshot of every page, width and theme.

`tools/deploy.sh` reads the target from `.deploy.env`, which is not in git: `AOK_DEPLOY_HOST`, `AOK_DEPLOY_DIR`, `AOK_DEPLOY_KEY` (optional) and `AOK_DEPLOY_BASE` (default `/doc/`). It refuses a build made for another base.

## Rules for the site

- English only, `<html lang="en">`, no Hangul anywhere in the repository.
- No inline scripts, no inline styles and no `style` attributes: the server sends a strict Content Security Policy (`script-src 'self'; style-src 'self'`). CSS and JavaScript file names carry a content hash, so they can be cached for a year.
- No third-party requests: fonts (Noto Sans, Lora, Noto Sans Mono, SIL Open Font License) and icons (Heroicons, MIT; Simple Icons, CC0) are served from the site, see `theme/licenses.txt`.
- While `noindex` is set in `wiki.yml`, every page carries `<meta name="robots" content="noindex, nofollow">`.
- No internal addresses, host names, people's names or vulnerability details in pages, commits or this repository.
