/* AokChain docs: search, copy buttons, the menu on small screens and the
   "On this page" highlight. No dependencies. Every page works without this
   file; it only adds to them. */
(function () {
  "use strict";

  var d = document;
  var body = d.body;
  var header = d.querySelector(".site-header");
  var narrow = window.matchMedia("(max-width: 1023.98px)");
  // Below this width the header shows a search button instead of the field
  var compact = window.matchMedia("(max-width: 1279.98px)");

  function $(sel, root) { return (root || d).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || d).querySelectorAll(sel)); }
  function el(tag, cls, text) {
    var node = d.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }
  function readStore(key) {
    try { return JSON.parse(window.sessionStorage.getItem(key) || "null"); } catch (e) { return null; }
  }
  function writeStore(key, value) {
    try { window.sessionStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* private mode */ }
  }

  var live = el("p", "sr-only");
  live.setAttribute("aria-live", "polite");
  body.appendChild(live);
  function announce(text) {
    live.textContent = "";
    window.setTimeout(function () { live.textContent = text; }, 30);
  }

  /* ------------------------------------------------------------ search */

  var index = null;
  var loading = null;

  function loadIndex() {
    if (index) return Promise.resolve(index);
    if (!loading) {
      loading = fetch(body.getAttribute("data-index"), { credentials: "same-origin" })
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.json();
        })
        .then(function (data) {
          index = data.pages.map(function (p) {
            return {
              u: p.u, t: p.t, s: p.s, d: p.d, h: p.h, x: p.x,
              tl: p.t.toLowerCase(),
              dl: p.d.toLowerCase(),
              hl: p.h.map(function (h) { return h[0].toLowerCase(); }),
              xl: p.x.map(function (x) { return x[1].toLowerCase(); })
            };
          });
          return index;
        })
        .catch(function (e) { loading = null; throw e; });
    }
    return loading;
  }

  function escapeRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }

  function parseQuery(q) {
    var seen = {};
    return q.toLowerCase().split(/\s+/)
      .map(function (w) { return w.replace(/^[^a-z0-9_#@/-]+|[^a-z0-9_#@/-]+$/g, ""); })
      .filter(function (w) { if (!w || seen[w]) return false; seen[w] = true; return true; })
      .slice(0, 8)
      .map(function (w) {
        var e = escapeRe(w);
        return {
          w: w,
          prefix: new RegExp("(?:^|[^a-z0-9])" + e),
          whole: new RegExp("(?:^|[^a-z0-9])" + e + "(?:$|[^a-z0-9])")
        };
      });
  }

  /* 0: no match, 1: inside a word, 2: start of a word, 3: whole word */
  function level(text, t) {
    if (text.indexOf(t.w) < 0) return 0;
    if (t.whole.test(text)) return 3;
    if (t.prefix.test(text)) return 2;
    return 1;
  }

  var W_TITLE = [0, 30, 70, 100];
  var W_HEAD = [0, 12, 28, 40];
  var W_DESC = [0, 4, 10, 14];
  var W_TEXT = [0, 2, 4, 6];

  function rank(terms, phrase) {
    var out = [];
    index.forEach(function (p) {
      var total = 0;
      var titleTotal = 0;
      var heads = p.hl.map(function () { return 0; });
      var chunks = p.xl.map(function () { return 0; });
      for (var i = 0; i < terms.length; i++) {
        var t = terms[i];
        var ts = W_TITLE[level(p.tl, t)];
        var hs = 0;
        for (var j = 0; j < p.hl.length; j++) {
          var hv = W_HEAD[level(p.hl[j], t)];
          heads[j] += hv;
          if (hv > hs) hs = hv;
        }
        var ds = W_DESC[level(p.dl, t)];
        var xs = 0;
        for (var k = 0; k < p.xl.length; k++) {
          var lv = level(p.xl[k], t);
          if (lv) {
            chunks[k] += lv;
            if (W_TEXT[lv] > xs) xs = W_TEXT[lv];
          }
        }
        var best = Math.max(ts, hs, ds, xs);
        if (!best) return; /* every word has to be somewhere on the page */
        titleTotal += ts;
        total += best + (ts + hs + ds + xs) * 0.1;
      }
      if (terms.length > 1) {
        if (p.tl.indexOf(phrase) >= 0) total += 60;
        else if (p.hl.some(function (h) { return h.indexOf(phrase) >= 0; })) total += 25;
        else if (p.xl.some(function (x) { return x.indexOf(phrase) >= 0; })) total += 6;
      }
      var head = -1;
      var headScore = 0;
      heads.forEach(function (s, j) { if (s > headScore) { headScore = s; head = j; } });
      if (headScore <= titleTotal) head = -1;
      out.push({ p: p, score: total, head: head, chunks: chunks });
    });
    out.sort(function (a, b) { return b.score - a.score || a.p.t.localeCompare(b.p.t); });
    return out.slice(0, 8);
  }

  function snippet(r, terms) {
    var p = r.p;
    var k = -1;
    if (r.head >= 0) {
      var anchor = p.h[r.head][1];
      for (var i = 0; i < p.x.length; i++) if (p.x[i][0] === anchor) { k = i; break; }
    }
    if (k < 0 || !r.chunks[k]) {
      var best = 0;
      k = -1;
      r.chunks.forEach(function (n, j) { if (n > best) { best = n; k = j; } });
    }
    if (k < 0) return p.d;
    var text = p.x[k][1];
    var low = p.xl[k];
    var pos = -1;
    terms.forEach(function (t) {
      var at = low.indexOf(t.w);
      if (at >= 0 && (pos < 0 || at < pos)) pos = at;
    });
    if (pos < 0) return p.d;
    var start = Math.max(0, pos - 60);
    if (start > 0) {
      var sp = text.indexOf(" ", start);
      if (sp >= 0 && sp < pos) start = sp + 1;
    }
    var end = Math.min(text.length, pos + 150);
    if (end < text.length) {
      var sp2 = text.lastIndexOf(" ", end);
      if (sp2 > pos) end = sp2;
    }
    return (start > 0 ? "…" : "") + text.slice(start, end) + (end < text.length ? "…" : "");
  }

  function highlight(node, text, terms) {
    if (!terms.length) { node.textContent = text; return; }
    var re = new RegExp("(" + terms.map(function (t) { return escapeRe(t.w); }).join("|") + ")", "gi");
    var last = 0;
    var m;
    while ((m = re.exec(text))) {
      if (!m[0].length) { re.lastIndex++; continue; }
      if (m.index > last) node.appendChild(d.createTextNode(text.slice(last, m.index)));
      node.appendChild(el("mark", "", m[0]));
      last = m.index + m[0].length;
    }
    if (last < text.length) node.appendChild(d.createTextNode(text.slice(last)));
  }

  function allPagesLink() {
    var link = $(".search-fallback");
    var a = el("a", "", "Browse all pages");
    a.href = link ? link.getAttribute("href") : "./";
    return a;
  }

  function Search(root) {
    var input = $(".search-input", root);
    var panel = $(".search-panel", root);
    var list = $(".search-list", root);
    var empty = $(".search-empty", root);
    var status = $("[data-search-status]", root);
    var items = [];
    var active = -1;
    var timer = 0;
    var seq = 0;

    function open() {
      panel.hidden = false;
      input.setAttribute("aria-expanded", "true");
    }
    function close() {
      panel.hidden = true;
      input.setAttribute("aria-expanded", "false");
      setActive(-1);
    }
    function setActive(i) {
      active = i;
      items.forEach(function (li, j) { li.setAttribute("aria-selected", j === i ? "true" : "false"); });
      if (i >= 0) {
        input.setAttribute("aria-activedescendant", items[i].id);
        items[i].scrollIntoView({ block: "nearest" });
      } else {
        input.removeAttribute("aria-activedescendant");
      }
    }
    function message(text) {
      list.textContent = "";
      items = [];
      empty.textContent = text + " ";
      empty.appendChild(allPagesLink());
      empty.hidden = false;
      open();
    }
    function render(results, terms, q) {
      list.textContent = "";
      items = results.map(function (r, i) {
        var li = el("li");
        li.id = list.id + "-" + i;
        li.setAttribute("role", "option");
        li.setAttribute("aria-selected", "false");
        var a = el("a");
        a.tabIndex = -1;
        var head = r.head >= 0 ? r.p.h[r.head] : null;
        a.href = r.p.u + (head ? "#" + head[1] : "");
        var title = el("span", "sr-title");
        highlight(title, r.p.t, terms);
        var path = el("span", "sr-path", r.p.s + (head ? " › " + head[0] : ""));
        var text = el("span", "sr-text");
        highlight(text, snippet(r, terms), terms);
        a.appendChild(title);
        a.appendChild(path);
        a.appendChild(text);
        li.appendChild(a);
        li.addEventListener("mousemove", function () { if (active !== i) setActive(i); });
        a.addEventListener("click", function () { close(); });
        list.appendChild(li);
        return li;
      });
      if (results.length) {
        empty.hidden = true;
        status.textContent = results.length + (results.length === 1 ? " result" : " results");
      } else {
        empty.textContent = "No pages match “" + q + "”. ";
        empty.appendChild(allPagesLink());
        empty.hidden = false;
        status.textContent = "No results";
      }
      open();
      setActive(results.length ? 0 : -1);
    }
    function run(then) {
      var q = input.value.trim();
      if (!q) {
        close();
        list.textContent = "";
        items = [];
        status.textContent = "";
        return;
      }
      var mine = ++seq;
      loadIndex().then(function () {
        if (mine !== seq) return;
        var terms = parseQuery(q);
        if (!terms.length) { close(); return; }
        render(rank(terms, q.toLowerCase().replace(/\s+/g, " ")), terms, q);
        if (then) then();
      }, function () {
        if (mine === seq) message("Search is not available right now.");
      });
    }
    function go(i) {
      var a = items[i] && $("a", items[i]);
      if (!a) return;
      close();
      window.location.href = a.href;
    }

    input.addEventListener("input", function () {
      window.clearTimeout(timer);
      timer = window.setTimeout(run, 60);
    });
    input.addEventListener("focus", function () {
      loadIndex().catch(function () { /* shown when searching */ });
      if (input.value.trim() && items.length) open();
    });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        if (panel.hidden) { run(); return; }
        if (!items.length) return;
        var step = e.key === "ArrowDown" ? 1 : -1;
        setActive((active + step + items.length) % items.length);
      } else if (e.key === "Enter") {
        e.preventDefault();
        window.clearTimeout(timer);
        if (!panel.hidden && active >= 0) go(active);
        else run(function () { if (items.length) go(0); });
      } else if (e.key === "Escape") {
        if (!panel.hidden) {
          e.preventDefault();
          close();
        } else if (input.value) {
          e.preventDefault();
          input.value = "";
          run();
        } else {
          root.dispatchEvent(new CustomEvent("search-escape", { bubbles: true }));
        }
      }
    });
    root.addEventListener("focusout", function (e) {
      if (!root.contains(e.relatedTarget)) close();
    });
    d.addEventListener("pointerdown", function (e) {
      if (!root.contains(e.target)) close();
    });

    return { root: root, input: input, run: run, close: close };
  }

  var searches = $$("[data-search]").map(Search);
  var headerSearch = searches.filter(function (s) { return s.root.classList.contains("search--header"); })[0];
  var pageSearch = searches.filter(function (s) { return s.root.classList.contains("search--hero"); })[0];
  var searchButton = $("[data-search-open]");

  function setHeaderSearch(on) {
    if (!headerSearch || !header) return;
    header.classList.toggle("search-open", on);
    if (searchButton) searchButton.setAttribute("aria-expanded", on ? "true" : "false");
    if (on) {
      closeMenu(false);
      headerSearch.input.focus();
    } else {
      headerSearch.close();
    }
  }
  if (searchButton) {
    searchButton.addEventListener("click", function () {
      setHeaderSearch(!header.classList.contains("search-open"));
    });
  }
  d.addEventListener("search-escape", function (e) {
    if (headerSearch && e.target === headerSearch.root && header.classList.contains("search-open")) {
      setHeaderSearch(false);
      if (searchButton) searchButton.focus();
    }
  });

  function focusSearch() {
    if (pageSearch) {
      pageSearch.input.focus();
      pageSearch.input.select();
      return true;
    }
    if (headerSearch) {
      if (compact.matches) setHeaderSearch(true);
      else { headerSearch.input.focus(); headerSearch.input.select(); }
      return true;
    }
    return false;
  }

  /* ------------------------------------------------------------ menu */

  var menuButton = $("[data-menu]");
  var sidebar = $("#w-sidebar");
  var menuIsOpen = false;

  function setInert(on) {
    ["#w-main", ".site-footer"].forEach(function (sel) {
      var node = $(sel);
      if (!node) return;
      if (on) node.setAttribute("inert", "");
      else node.removeAttribute("inert");
    });
  }
  function openMenu() {
    if (!sidebar || !menuButton) return;
    setHeaderSearch(false);
    menuIsOpen = true;
    sidebar.classList.add("is-open");
    body.classList.add("menu-open");
    menuButton.setAttribute("aria-expanded", "true");
    menuButton.setAttribute("aria-label", "Close menu");
    setInert(true);
    var current = $('a[aria-current="page"]', sidebar) || $(".tree summary", sidebar);
    if (current) current.focus();
  }
  function closeMenu(returnFocus) {
    if (!menuIsOpen) return;
    menuIsOpen = false;
    sidebar.classList.remove("is-open");
    body.classList.remove("menu-open");
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "Menu");
    setInert(false);
    if (returnFocus) menuButton.focus();
  }
  if (menuButton && sidebar) {
    menuButton.addEventListener("click", function () {
      if (menuIsOpen) closeMenu(true);
      else openMenu();
    });
    var mqHandler = function () { if (!narrow.matches) closeMenu(false); };
    if (narrow.addEventListener) narrow.addEventListener("change", mqHandler);
  }

  d.addEventListener("keydown", function (e) {
    if (e.defaultPrevented) return;
    var t = e.target;
    var typing = t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName));
    var slash = e.key === "/" && !typing && !e.ctrlKey && !e.metaKey && !e.altKey;
    var ctrlK = (e.key === "k" || e.key === "K") && (e.ctrlKey || e.metaKey) && !e.altKey;
    if (slash || ctrlK) {
      if (focusSearch()) e.preventDefault();
    } else if (e.key === "Escape" && menuIsOpen) {
      closeMenu(true);
    }
  });

  /* Keep the sections someone opened in the sidebar open on the next page */
  var OPEN_KEY = "aok-docs-open";
  var sections = $$(".tree-sec");
  var saved = readStore(OPEN_KEY);
  sections.forEach(function (det) {
    if (saved && saved.indexOf(det.getAttribute("data-sec")) >= 0) det.open = true;
    det.addEventListener("toggle", function () {
      writeStore(OPEN_KEY, sections.filter(function (s) { return s.open; })
        .map(function (s) { return s.getAttribute("data-sec"); }));
    });
  });

  /* ------------------------------------------------------------ code */

  var copyTemplate = $("#w-tpl-copy");

  function codeText(pre) {
    var clone = pre.cloneNode(true);
    $$(".gp", clone).forEach(function (n) { n.parentNode.removeChild(n); });
    return clone.textContent.replace(/\n$/, "");
  }
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(function () { return copyBySelection(text); });
    }
    return copyBySelection(text);
  }
  function copyBySelection(text) {
    return new Promise(function (resolve, reject) {
      var area = el("textarea", "sr-only");
      area.value = text;
      area.setAttribute("readonly", "");
      body.appendChild(area);
      area.select();
      var ok = false;
      try { ok = d.execCommand("copy"); } catch (e) { ok = false; }
      body.removeChild(area);
      if (ok) resolve(); else reject(new Error("copy"));
    });
  }
  if (copyTemplate) {
    $$(".code").forEach(function (block) {
      var bar = $(".code-bar", block);
      var pre = $("pre", block);
      if (!bar || !pre) return;
      var button = copyTemplate.content.firstElementChild.cloneNode(true);
      var label = $("span", button);
      var reset = 0;
      button.addEventListener("click", function () {
        copyText(codeText(pre)).then(function () {
          button.classList.add("is-done");
          label.textContent = "Copied";
          announce("Copied to the clipboard");
        }, function () {
          label.textContent = "Select and copy";
        });
        window.clearTimeout(reset);
        reset = window.setTimeout(function () {
          button.classList.remove("is-done");
          label.textContent = "Copy";
        }, 2000);
      });
      bar.appendChild(button);
    });
  }

  /* Wide code and tables scroll sideways; make those reachable by keyboard */
  function markScrollers() {
    $$(".code pre, .table-wrap").forEach(function (node) {
      var over = node.scrollWidth > node.clientWidth + 1;
      if (over && node.getAttribute("role") !== "region") {
        node.tabIndex = 0;
        node.setAttribute("role", "region");
        node.setAttribute("aria-label", node.tagName === "PRE" ? "Code" : "Table");
      } else if (!over && node.getAttribute("role") === "region") {
        node.removeAttribute("tabindex");
        node.removeAttribute("role");
        node.removeAttribute("aria-label");
      }
    });
  }
  var resizeTimer = 0;
  markScrollers();
  window.addEventListener("resize", function () {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(markScrollers, 150);
  });

  /* ------------------------------------------------------------ contents */

  var tocLinks = $$(".toc a, .toc-inline a");
  if (tocLinks.length) {
    var ids = [];
    tocLinks.forEach(function (a) {
      var id = decodeURIComponent(a.getAttribute("href").slice(1));
      if (ids.indexOf(id) < 0) ids.push(id);
    });
    var heads = ids.map(function (id) { return d.getElementById(id); }).filter(Boolean);
    var current = null;
    var ticking = false;
    var update = function () {
      ticking = false;
      var line = (header ? header.offsetHeight : 0) + 96;
      var now = null;
      for (var i = 0; i < heads.length; i++) {
        if (heads[i].getBoundingClientRect().top - line <= 0) now = heads[i].id;
        else break;
      }
      var doc = d.documentElement;
      if (heads.length && window.innerHeight + window.scrollY >= doc.scrollHeight - 4) {
        now = heads[heads.length - 1].id;
      }
      if (now === current) return;
      current = now;
      tocLinks.forEach(function (a) {
        var on = now !== null && a.getAttribute("href") === "#" + now;
        a.classList.toggle("is-active", on);
        if (on) a.setAttribute("aria-current", "location");
        else a.removeAttribute("aria-current");
      });
    };
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* ------------------------------------------------------------ 404 */

  if (body.classList.contains("kind-notfound") && pageSearch) {
    var brand = $(".brand");
    var base = brand ? brand.getAttribute("href") : "/";
    var path = window.location.pathname;
    try { path = decodeURIComponent(path); } catch (e) { /* keep it encoded */ }
    if (path.indexOf(base) === 0) path = path.slice(base.length);
    var words = path.replace(/\.html?$/i, "").split(/[\/_.\-+\s]+/)
      .filter(function (w) { return w.length > 1 && !/^\d+$/.test(w); })
      .slice(0, 5).join(" ");
    if (words) {
      pageSearch.input.value = words;
      /* show suggestions only when there are some */
      pageSearch.run(function () {
        if (!$(".search-list [role=option]", pageSearch.root)) pageSearch.close();
      });
    }
  }
})();
