"""The AokChain wiki builder: Markdown pages in, a static site out.

tools/build.py is the command line; this package holds the parts:

  config    wiki.yml and sections.yml
  pages     finding the pages, front matter, the content rules
  markdown  the Markdown dialect: GFM, wiki links, callouts, code
  slug      GitHub-style heading anchors
  checks    the text rules (English only, no private details)
  gitinfo   "Last updated" and "Recent changes" from git
  search    the search index
  icons     the inline icon sprite
  art       the line art
  site      the build itself
"""

ROOT_MARKER = "wiki.yml"
