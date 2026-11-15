"""The search index: one JSON file, fetched by docs.js the first time someone
uses the search. Per page: address, title, section, description, headings
and the text cut at its headings. Ranking happens in the browser: title,
then headings, then text."""
import json

CHUNK_MAX = 2000     # characters of text kept per heading
PAGE_MAX = 40000     # characters of text kept per page


def entry(page):
    headings, text, used = [], [], 0
    for anchor, heading, body in page.parsed.chunks:
        if heading:
            headings.append([heading, anchor])
        body = body[:CHUNK_MAX]
        if body and used < PAGE_MAX:
            body = body[:PAGE_MAX - used]
            used += len(body)
            text.append([anchor, body])
    return {
        "u": page.url,
        "t": page.title,
        "s": page.section.title,
        "d": page.description,
        "h": headings,
        "x": text,
    }


def build(pages):
    data = {"v": 1, "pages": [entry(p) for p in pages]}
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
