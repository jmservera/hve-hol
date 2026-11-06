#!/usr/bin/env python3
"""
Build the static HTML pages of the HVE hands-on workshop guide.

    python tools/build_site.py

Reads tools/content.py and writes the pages to docs/. Uses only the Python standard
library (Python 3.8+). The stylesheet and script in docs/assets/ are edited by hand.
After building, every internal link and #anchor is checked.
"""
import html
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as C  # noqa: E402

DOCS = os.path.join(os.path.dirname(HERE), "docs")

KIND_LABEL = {
    "core": "Core task",
    "parallel": "Parallel task",
    "intermission": "Waiting-time task",
    "backup": "Backup",
    "info": "",
}

ICONS = {
    "info": '<circle cx="12" cy="12" r="9.5"/><path d="M12 11v6M12 7.5v.01"/>',
    "next": '<path d="M4 12h15M13 6l6 6-6 6"/>',
    "wait": '<path d="M6 3h12M6 21h12M7 3v3.5L12 12l-5 5.5V21M17 3v3.5L12 12l5 5.5V21"/>',
    "tip": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.7.5 1.1 1.3 1.1 2.2h5c0-.9.4-1.7 1.1-2.2A6 6 0 0 0 12 3z"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="9.5"/><path d="M12 7v5l3.5 2"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
}


def icon(name, cls="icon"):
    return ('<svg class="%s" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" '
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</svg>'
            % (cls, ICONS[name]))


# ---------------------------------------------------------------------------
# Inline formatting: `code`, **bold**, [text](url), line breaks
# ---------------------------------------------------------------------------
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def esc(text):
    return html.escape(text or "", quote=True)


def is_external(url):
    return url.startswith(("http://", "https://"))


def anchor(url, label_html, cls=None):
    """label_html must already be escaped."""
    classes = [c for c in (cls,) if c]
    attrs = 'href="%s"' % esc(url)
    if is_external(url):
        classes.append("ext")
        attrs += ' target="_blank" rel="noopener noreferrer"'
        label_html += '<span class="sr-only"> (opens in a new tab)</span>'
    if classes:
        attrs += ' class="%s"' % " ".join(classes)
    return "<a %s>%s</a>" % (attrs, label_html)


def fmt(text):
    if not text:
        return ""
    out = []
    for part in re.split(r"(`[^`]+`)", text):
        if len(part) >= 2 and part[0] == "`" and part[-1] == "`":
            out.append("<code>%s</code>" % html.escape(part[1:-1], quote=False))
            continue
        s = html.escape(part, quote=False)
        s = LINK_RE.sub(lambda m: anchor(html.unescape(m.group(2)), m.group(1)), s)
        s = BOLD_RE.sub(r"<strong>\1</strong>", s)
        s = s.replace("\n", "<br>")
        out.append(s)
    return "".join(out)


def plain(text):
    """Text without inline markup (for titles, aria-labels and descriptions)."""
    text = LINK_RE.sub(lambda m: m.group(1), text or "")
    return text.replace("**", "").replace("`", "").replace("\n", " ")


def pretty_url(url):
    p = urlsplit(url)
    host = p.netloc.replace("www.", "")
    path = p.path.rstrip("/")
    full = host + path
    if len(full) <= 52:
        return full
    segments = [s for s in path.split("/") if s]
    return "%s/…/%s" % (host, segments[-1]) if segments else host


# ---------------------------------------------------------------------------
# Page model
# ---------------------------------------------------------------------------
PAGES = C.PAGES
BY_SLUG = {p["slug"]: p for p in PAGES}


def href(slug):
    return "index.html" if slug == "index" else "%s.html" % slug


def nav_badge(page):
    kind = page["kind"]
    num = page.get("num")
    if num:
        return '<span class="badge badge-%s" aria-hidden="true">%s</span>' % (kind, esc(num))
    return '<span class="badge badge-dot" aria-hidden="true"></span>'


def nav_label(page):
    label = esc(page["nav"])
    if page.get("num") and page["kind"] in ("core", "parallel", "backup"):
        label = '<span class="sr-only">Exercise %s: </span>%s' % (esc(page["num"]), label)
    return label


def full_title(page):
    if page.get("num") and page["kind"] in ("core", "parallel", "backup"):
        return "Exercise %s · %s" % (page["num"], page["title"])
    if page["kind"] == "intermission":
        return "Intermission %s · %s" % (page["num"], page["title"])
    return page["title"]


# ---------------------------------------------------------------------------
# Block renderers
# ---------------------------------------------------------------------------
class Ctx:
    def __init__(self, page):
        self.page = page
        self.first_template = True
        self.tips_count = 0


def render_blocks(blocks, ctx):
    return "\n".join(render_block(b, ctx) for b in blocks)


def r_brief(b, ctx):
    return (
        '<section class="brief" id="brief" aria-label="Brief">\n'
        '<div class="objective"><span class="label">Objective</span><p>%s</p></div>\n'
        '<dl class="meta">\n'
        '<div class="meta-input"><dt>Input</dt><dd>%s</dd></div>\n'
        '<div class="meta-best"><dt>Best use</dt><dd>%s</dd></div>\n'
        '<div class="meta-roles"><dt>%s</dt><dd>%s</dd></div>\n'
        '</dl>\n</section>'
        % (fmt(b["objective"]), fmt(b["input"]), fmt(b["best_use"]), esc(b["roles_label"]), fmt(b["roles"]))
    )


def r_work(b, ctx):
    steps = "\n".join("<li><p>%s</p></li>" % fmt(s) for s in b["steps"])
    items = []
    for i, h in enumerate(b["handin"]):
        items.append(
            '<li><label><input type="checkbox" data-key="handin-%d"><span>%s</span></label></li>' % (i, fmt(h))
        )
    return (
        '<div class="work">\n'
        '<section class="steps-wrap" aria-label="Steps"><h2 class="mini-head">Steps</h2>\n'
        '<ol class="steps">\n%s\n</ol></section>\n'
        '<section class="handin" aria-label="Hand in"><h2 class="handin-head">Hand in</h2>\n'
        '<ul>\n%s\n</ul>\n<p class="handin-note">Tick items as your team hands them in.</p></section>\n'
        '</div>' % (steps, "\n".join(items))
    )


def r_section(b, ctx):
    lead = '<p class="lead">%s</p>' % fmt(b["lead"]) if b.get("lead") else ""
    return (
        '<header class="section-head" id="%s">\n<p class="eyebrow">%s</p>\n<h2>%s</h2>\n%s</header>'
        % (esc(b["id"]), esc(b["eyebrow"]), fmt(b["title"]), lead)
    )


def cell_html(cell, row_label, col_label, editable):
    if cell is None or isinstance(cell, dict):
        hint = cell.get("ph") if isinstance(cell, dict) else None
        aria = ", ".join(x for x in (plain(row_label), plain(col_label)) if x) or "Entry"
        if not editable:
            return "<td>%s</td>" % esc(hint or "")
        hint_attr = ' data-ph="%s"' % esc(hint) if hint else ""
        return '<td class="fill" contenteditable="true" spellcheck="true" aria-label="%s"%s></td>' % (
            esc(aria), hint_attr)
    return "<td>%s</td>" % fmt(cell)


def grid_table(spec, editable, label):
    head = spec["head"]
    row_header = spec.get("row_header")
    cls = "grid" + (" " + spec["cls"] if spec.get("cls") else "") + (" tpl-table" if editable else "")
    th = []
    for i, h in enumerate(head):
        if h == "" and i == 0:
            th.append('<td class="corner"></td>')
        else:
            th.append('<th scope="col">%s</th>' % fmt(h))
    rows_html = []
    for row in spec["rows"]:
        row_cls = ""
        if isinstance(row, dict):
            row_cls = ' class="%s"' % esc(row.get("cls", ""))
            row = row["cells"]
        cells = []
        row_label = row[0] if row_header and isinstance(row[0], str) else ""
        for j, cell in enumerate(row):
            col_label = head[j] if j < len(head) else ""
            if j == 0 and row_header and isinstance(cell, str):
                cells.append('<th scope="row">%s</th>' % fmt(cell))
            else:
                cells.append(cell_html(cell, row_label, col_label, editable))
        rows_html.append("<tr%s>%s</tr>" % (row_cls, "".join(cells)))
    return (
        '<div class="table-wrap" role="region" aria-label="%s" tabindex="0">\n<table class="%s">\n'
        "<thead><tr>%s</tr></thead>\n<tbody>\n%s\n</tbody>\n</table>\n</div>"
        % (esc(plain(label)), cls, "".join(th), "\n".join(rows_html))
    )


def storage_note(ctx):
    if not ctx.first_template:
        return ""
    ctx.first_template = False
    return '<p class="storage-note">%s<span>%s</span></p>' % (icon("info"), fmt(C.SITE["storage_note"]))


def tpl_actions():
    return (
        '<div class="tpl-actions">'
        '<button type="button" class="btn" data-action="copy-md">Copy as Markdown</button>'
        '<button type="button" class="btn btn-quiet" data-action="clear">Clear</button>'
        "</div>"
    )


def r_template(b, ctx, store=None):
    note = '<p class="tpl-note">%s</p>' % fmt(b["note"]) if b.get("note") else ""
    store_attr = ' data-store="%s"' % esc(store) if store else ""
    return (
        '%s<div class="tpl" id="tpl-%s" data-tpl="%s"%s>\n<div class="tpl-head"><h3>%s</h3>%s</div>\n%s\n%s</div>'
        % (storage_note(ctx), esc(b["id"]), esc(b["id"]), store_attr, fmt(b["label"]), tpl_actions(),
           grid_table(b, True, b["label"]), note)
    )


def r_table(b, ctx):
    cap = '<p class="table-caption">%s</p>' % fmt(b["caption"]) if b.get("caption") else ""
    return '<div class="static-table">%s%s</div>' % (cap, grid_table(b, False, b.get("caption") or "Table"))


def r_runwith(b, ctx):
    items = b["items"]
    if len(items) == 1 and not items[0][0]:
        body = "<p>%s</p>" % fmt(items[0][1])
    else:
        lis = []
        for label, text in items:
            lead = "<strong>%s:</strong> " % esc(label) if label else ""
            lis.append("<li>%s%s</li>" % (lead, fmt(text)))
        body = '<ul class="run-list">%s</ul>' % "".join(lis)
    return '<div class="box box-run"><p class="label">%s</p>%s</div>' % (esc(b["label"]), body)


def links_list(items):
    lis = []
    for label, url in items:
        lis.append("<li>%s</li>" % anchor(url, esc(label)))
    return '<ul class="links">%s</ul>' % "".join(lis)


def r_links(b, ctx):
    return '<div class="links-block"><p class="label">%s</p>%s</div>' % (esc(b["label"]), links_list(b["items"]))


def r_done(b, ctx):
    return '<div class="done"><span class="label">%sDone when</span><p>%s</p></div>' % (
        icon("check"), fmt(b["text"]))


def r_tips(b, ctx):
    ctx.tips_count += 1
    tid = "tips" if ctx.tips_count == 1 else "tips-%d" % ctx.tips_count
    lis = "".join("<li>%s</li>" % fmt(t) for t in b["items"])
    return '<aside class="tips" id="%s" aria-label="%s"><p class="label">%s%s</p><ul>%s</ul></aside>' % (
        tid, esc(b["label"]), icon("tip"), esc(b["label"]), lis)


def r_callout(b, ctx):
    acts = ""
    if b.get("actions"):
        acts = '<p class="callout-actions">%s</p>' % " ".join(
            anchor(h, esc(l), cls="btn btn-small") for l, h in b["actions"])
    ico = {"wait": "wait", "info": "info", "next": "next"}[b["kind"]]
    return (
        '<div class="callout callout-%s">%s<div class="callout-body"><p class="callout-title">%s</p><p>%s</p>%s'
        "</div></div>" % (b["kind"], icon(ico, "icon callout-icon"), fmt(b["title"]), fmt(b["text"]), acts)
    )


def r_banner(b, ctx):
    return '<p class="banner banner-%s">%s</p>' % (b.get("kind", "navy"), fmt(b["text"]))


def r_code(b, ctx):
    cid = "code-" + (b.get("id") or "snippet")
    cap = '<figcaption>%s</figcaption>' % fmt(b["caption"]) if b.get("caption") else "<figcaption></figcaption>"
    return (
        '<figure class="code"><div class="code-head">%s<button type="button" class="btn btn-small" '
        'data-copy-code="%s">Copy</button></div><pre id="%s"><code>%s</code></pre></figure>'
        % (cap, cid, cid, html.escape(b["text"], quote=False))
    )


def r_p(b, ctx):
    cls = ' class="%s"' % b["cls"] if b.get("cls") else ""
    return "<p%s>%s</p>" % (cls, fmt(b["text"]))


def r_list(b, ctx):
    title = '<p class="label">%s</p>' % fmt(b["title"]) if b.get("title") else ""
    cls = "bullets" + (" " + b["cls"] if b.get("cls") else "")
    return '%s<ul class="%s">%s</ul>' % (title, cls, "".join("<li>%s</li>" % fmt(i) for i in b["items"]))


def r_cols(b, ctx):
    cls = "cols" + (" " + b["cls"] if b.get("cls") else "")
    inner = "".join('<div class="col">%s</div>' % render_blocks(col, ctx) for col in b["cols"])
    return '<div class="%s">%s</div>' % (cls, inner)


def r_numbered(b, ctx):
    lis = []
    for i, item in enumerate(b["items"], 1):
        if isinstance(item, tuple):
            body = '<div><p class="num-title">%s</p><p>%s</p></div>' % (fmt(item[0]), fmt(item[1]))
        else:
            body = "<div><p>%s</p></div>" % fmt(item)
        lis.append('<li><span class="n" aria-hidden="true">%d</span>%s</li>' % (i, body))
    cls = "numbered" + (" " + b["cls"] if b.get("cls") else "")
    return '<ol class="%s">%s</ol>' % (cls, "".join(lis))


def r_roles(b, ctx):
    cards = "".join('<li class="role"><h3>%s</h3><p>%s</p></li>' % (fmt(t), fmt(d)) for t, d in b["items"])
    return '<ul class="roles">%s</ul>' % cards


def r_timer(b, ctx):
    return ('<div class="timer">%s<p><span class="timer-value">%s</span> <span class="timer-unit">%s</span></p>'
            "<p>%s</p></div>" % (icon("clock"), esc(b["value"]), esc(b["unit"]), fmt(b["text"])))


def r_checklist(b, ctx):
    lis = "".join("<li>%s<span>%s</span></li>" % (icon("check", "icon tick"), fmt(i)) for i in b["items"])
    return '<div class="checklist"><h3>%s</h3><ul>%s</ul></div>' % (fmt(b["title"]), lis)


def r_cardlist(b, ctx):
    cards = []
    for title, text, link in b["items"]:
        body = "<p>%s</p>" % fmt(text) if text else ""
        lk = '<p class="mini-link">%s</p>' % anchor(link[1], esc(link[0])) if link else ""
        cards.append('<div class="mini-card"><p class="mini-title">%s</p>%s%s</div>' % (fmt(title), body, lk))
    return '<div class="cardlist"><h3>%s</h3>%s</div>' % (fmt(b["title"]), "".join(cards))


def r_runtimes(b, ctx):
    cards = []
    for rt in b["items"]:
        tag = '<span class="pill pill-exp">%s</span>' % esc(rt["tag"]) if rt.get("tag") else ""
        pts = "".join("<li>%s</li>" % fmt(p) for p in rt["points"])
        best = ('<p class="best"><span class="label">Best for</span>%s</p>' % fmt(rt["best"])) if rt.get(
            "best") else ""
        cards.append(
            '<div class="runtime"><div class="runtime-head"><h3>%s</h3>%s</div><p class="runtime-sub">%s</p>'
            "<ul>%s</ul>%s</div>" % (esc(rt["name"]), tag, fmt(rt["sub"]), pts, best)
        )
    return '<div class="runtimes">%s</div>' % "".join(cards)


def r_refcard(b, ctx):
    sub = '<p class="ref-sub">%s</p>' % fmt(b["sub"]) if b.get("sub") else ""
    lis = []
    for label, text in b["items"]:
        lead = "<strong>%s</strong> " % fmt(label) if label else ""
        lis.append("<li>%s%s</li>" % (lead, fmt(text)))
    return '<div class="refcard"><h3>%s</h3>%s<ul>%s</ul></div>' % (fmt(b["title"]), sub, "".join(lis))


def r_refcode(b, ctx):
    return '<div class="refcard"><h3>%s</h3><pre class="tree">%s</pre></div>' % (
        fmt(b["title"]), html.escape(b["text"], quote=False))


def r_intermissions(b, ctx):
    cards = []
    for p in PAGES:
        if p["kind"] not in ("intermission", "backup"):
            continue
        when = p["eyebrow"].split(" · ")[1] if p["kind"] == "intermission" else "Only if your team finishes early"
        title = "Intermission %s" % p["num"] if p["kind"] == "intermission" else "Backup · Exercise %s" % p["num"]
        cards.append(
            '<a class="int-card int-%s" href="%s"><span class="badge badge-%s" aria-hidden="true">%s</span>'
            '<span class="int-text"><span class="int-when">%s</span><strong>%s</strong><span>%s</span></span></a>'
            % (p["kind"], href(p["slug"]), p["kind"], esc(p["num"]), esc(when), esc(title), esc(p["title"]))
        )
    return ('<section class="int-block" aria-label="Intermissions"><h2 class="mini-head">Intermissions and backup'
            '</h2><div class="int-grid">%s</div></section>' % "".join(cards))


def r_round(b, ctx):
    num = esc(b["num"])
    evidence = "".join("<li>%s</li>" % fmt(item) for item in b["evidence"])
    return (
        '<section aria-labelledby="round-%s">\n<h3 id="round-%s">Round %s · %s</h3>\n'
        '<p class="lead">%s</p>\n'
        '<p>Write your answer in the <a href="#tpl-round-answers">answer sheet</a> or on paper. '
        'Take 90 seconds; wait for the facilitator before opening the reveal.</p>\n'
        '<details class="reveal" id="reveal-%s">\n'
        '<summary>%s<span><strong>Reveal · %s</strong><span class="reveal-hint">'
        'Open after answering, then score your original answer.</span></span></summary>\n'
        '<div class="reveal-body"><p class="caveat">'
        'Illustrative example · fictional client and system · not a recorded run</p>\n'
        '<ul class="bullets">%s</ul>\n'
        '<p class="banner banner-soft"><strong>Human decision:</strong> %s</p></div>\n'
        '</details>\n</section>'
        % (num, num, num, fmt(b["step"]), fmt(b["question"]), num, icon("eye", "icon reveal-icon"),
           fmt(b["title"]), evidence, fmt(b["human"]))
    )


def r_shared_ab(b, ctx):
    s = C.SHARED_AB
    parts = [
        r_section({"id": "toolkit", "eyebrow": s["eyebrow"], "title": s["title"]}, ctx),
        r_callout({"kind": "info", "title": "One hand-in for Intermissions A and B", "text": b["fill"] + " " +
                   s["shared_note"], "actions": []}, ctx),
        r_template(dict(s["trace"], id="trace", label="Template 1 · Trace from source to artefact"), ctx,
                   store="intermissions-ab:trace"),
        r_runwith({"label": "Run it with", "items": [(None, s["run_with"])]}, ctx),
        r_rules({"items": s["rules"]}, ctx),
        r_template(dict(s["loop"], id="operations-loop", label="Template 2 · Operations loop",
                        note=s["loop_note"]), ctx, store="intermissions-ab:loop"),
        r_done({"text": s["done"]}, ctx),
    ]
    return "\n".join(parts)


def r_example(b, ctx):
    return '<div class="box box-example"><p class="label">%s</p><p>%s</p></div>' % (esc(b["title"]), fmt(b["text"]))


def r_note(b, ctx):
    return '<p class="note-line"><strong>%s:</strong> %s</p>' % (esc(b["label"]), fmt(b["text"]))


def r_chips(b, ctx):
    style = b.get("style", "plain")
    lis = "".join("<li>%s</li>" % fmt(i) for i in b["items"])
    return '<div class="chips chips-%s"><p class="label">%s</p><ul>%s</ul></div>' % (style, esc(b["title"]), lis)


def r_rules(b, ctx):
    lis = "".join("<li>%s</li>" % fmt(i) for i in b["items"])
    return '<div class="box box-rules"><p class="label">Rules</p><ul>%s</ul></div>' % lis


def r_lenses(b, ctx):
    lis = "".join('<li><p class="lens-name">%s</p><p>%s</p></li>' % (esc(n), fmt(q)) for n, q in b["items"])
    return '<div class="lenses"><p class="label">%s</p><ul>%s</ul></div>' % (esc(b["title"]), lis)


def r_canvas(b, ctx):
    cells = []
    for num, title in b["items"]:
        cells.append(
            '<div class="canvas-cell" data-md="%s · %s"><p class="canvas-title"><span class="n" aria-hidden="true">'
            '%s</span><span>%s</span></p><div class="canvas-fill fill" contenteditable="true" spellcheck="true" '
            'aria-label="%s"></div></div>' % (esc(num), esc(plain(title)), esc(num), fmt(title), esc(plain(title)))
        )
    return (
        '%s<div class="tpl tpl-canvas" id="tpl-%s" data-tpl="%s" data-kind="canvas">\n<div class="tpl-head"><h3>%s'
        "</h3>%s</div>\n<div class=\"canvas\">%s</div>\n</div>"
        % (storage_note(ctx), esc(b["id"]), esc(b["id"]), esc(b["label"]), tpl_actions(), "".join(cells))
    )


def r_formula(b, ctx):
    return '<div class="formula"><p class="formula-main">%s</p><p>%s</p></div>' % (fmt(b["text"]), fmt(b["sub"]))


def r_h3(b, ctx):
    idattr = ' id="%s"' % esc(b["id"]) if b.get("id") else ""
    return "<h3%s>%s</h3>" % (idattr, fmt(b["text"]))


def r_resources(b, ctx):
    return render_resources_body()


RENDERERS = {
    "brief": r_brief, "work": r_work, "section": r_section, "template": r_template, "table": r_table,
    "runwith": r_runwith, "links": r_links, "done": r_done, "tips": r_tips, "callout": r_callout,
    "banner": r_banner, "code": r_code, "p": r_p, "list": r_list, "cols": r_cols, "numbered": r_numbered,
    "roles": r_roles, "timer": r_timer, "checklist": r_checklist, "cardlist": r_cardlist,
    "runtimes": r_runtimes, "refcard": r_refcard, "refcode": r_refcode, "intermissions": r_intermissions,
    "round": r_round, "shared_ab": r_shared_ab, "example": r_example, "note": r_note, "chips": r_chips,
    "rules": r_rules, "lenses": r_lenses, "canvas": r_canvas, "formula": r_formula, "h3": r_h3,
    "resources": r_resources,
}


def render_block(b, ctx):
    try:
        return RENDERERS[b["type"]](b, ctx)
    except KeyError as exc:
        raise SystemExit("Unknown block type %r on page %s" % (b.get("type"), ctx.page["slug"])) from exc


# ---------------------------------------------------------------------------
# Resources page
# ---------------------------------------------------------------------------
def res_items(items):
    lis = []
    for title, url, desc in items:
        d = '<span class="res-desc">%s</span>' % fmt(desc) if desc else ""
        lis.append(
            '<li data-res-item><a class="res-link" href="%s" target="_blank" rel="noopener noreferrer">'
            '<span class="res-title">%s</span><span class="res-url">%s</span>%s'
            '<span class="sr-only"> (opens in a new tab)</span></a></li>'
            % (esc(url), esc(title), esc(pretty_url(url)), d)
        )
    return '<ul class="res-grid">%s</ul>' % "".join(lis)


def collect_links(page):
    found = []

    def add(label, url):
        if is_external(url) and (label, url) not in found:
            found.append((label, url))

    def walk(blocks):
        for b in blocks:
            t = b.get("type")
            if t == "links":
                for label, url in b["items"]:
                    add(label, url)
            elif t == "cardlist":
                for _, _, link in b["items"]:
                    if link:
                        add(link[0], link[1])
            elif t == "cols":
                for col in b["cols"]:
                    walk(col)

    walk(page["blocks"])
    return found


def collect_templates(page):
    found = []

    def walk(blocks):
        for b in blocks:
            t = b.get("type")
            if t in ("template", "canvas"):
                found.append((plain(b["label"]), b["id"]))
            elif t == "shared_ab":
                found.append(("Template 1 · Trace from source to artefact", "trace"))
                found.append(("Template 2 · Operations loop", "operations-loop"))
            elif t == "cols":
                for col in b["cols"]:
                    walk(col)

    walk(page["blocks"])
    return found


def step_name(p):
    if p.get("num") and p["kind"] in ("core", "parallel", "backup"):
        return "Exercise %s · %s" % (p["num"], p["nav"])
    return p["nav"]


def render_resources_body():
    out = ['<p class="lead">Every link from the guide in one place. Links open in a new tab.</p>']
    toc = [(s["id"], s["title"]) for s in C.RESOURCES] + [
        (C.ACCELERATORS["id"], "Accelerators"), ("by-exercise", "Links by exercise"), ("templates", "Templates")]
    out.append(
        '<div class="res-tools"><label for="res-filter">Filter links</label>'
        '<input id="res-filter" type="search" autocomplete="off" placeholder="Type to filter, e.g. Azure DevOps, Work IQ, squad">'
        '<span id="res-count" class="res-count" aria-live="polite"></span></div>'
    )
    out.append('<nav class="res-toc" aria-label="Resource sections"><ul>%s</ul></nav>' % "".join(
        '<li><a href="#%s">%s</a></li>' % (i, esc(t)) for i, t in toc))
    for sec in C.RESOURCES:
        out.append('<section class="res-section" id="%s" data-res-section><h2>%s</h2>' % (sec["id"],
                                                                                        esc(sec["title"])))
        if "items" in sec:
            out.append(res_items(sec["items"]))
        for grp in sec.get("groups", []):
            out.append('<div class="res-group" data-res-group><h3>%s</h3>%s</div>' % (esc(grp["title"]),
                                                                                    res_items(grp["items"])))
        out.append("</section>")
    a = C.ACCELERATORS
    how = "".join('<li><p class="acc-step">%s</p><p>%s</p></li>' % (esc(t), fmt(d)) for t, d in a["how"])
    feat = "".join('<li data-res-item><p class="acc-name">%s</p><p>%s</p></li>' % (esc(n), fmt(d))
                   for n, d in a["featured"])
    out.append(
        '<section class="res-section" id="%s" data-res-section><h2>%s</h2><p>%s</p>'
        '<div class="acc-grid"><div><h3>How accelerators work</h3><ol class="acc-how">%s</ol></div>'
        '<div><h3>Featured accelerators</h3><ul class="res-grid res-grid-one"><li data-res-item>'
        '<a class="res-link" href="%s" target="_blank" rel="noopener noreferrer"><span class="res-title">%s</span>'
        '<span class="res-url">%s</span><span class="res-desc">Full catalogue</span>'
        '<span class="sr-only"> (opens in a new tab)</span></a></li></ul>'
        '<ul class="acc-featured">%s</ul></div></div><p class="banner banner-soft">%s</p></section>'
        % (a["id"], esc(a["title"]), fmt(a["intro"]), how, esc(a["featured_link"][1]), esc(a["featured_link"][0]),
           esc(pretty_url(a["featured_link"][1])), feat, fmt(a["in_workshop"]))
    )
    rows = []
    for p in PAGES:
        found = collect_links(p)
        if not found:
            continue
        rows.append('<tr data-res-item><th scope="row"><a href="%s">%s</a></th><td>%s</td></tr>' % (
            href(p["slug"]), esc(step_name(p)), links_list(found)))
    out.append(
        '<section class="res-section" id="by-exercise" data-res-section><h2>Links by exercise</h2>'
        '<div class="table-wrap" role="region" aria-label="Links by exercise" tabindex="0"><table class="grid by-ex">'
        '<thead><tr><th scope="col">Step</th><th scope="col">Links</th></tr></thead><tbody>%s</tbody></table></div>'
        "</section>" % "".join(rows)
    )
    rows = []
    for p in PAGES:
        found = collect_templates(p)
        if not found:
            continue
        lis = "".join('<li><a href="%s#tpl-%s">%s</a></li>' % (href(p["slug"]), esc(i), esc(l)) for l, i in found)
        rows.append('<tr data-res-item><th scope="row"><a href="%s">%s</a></th><td><ul class="tpl-list">%s</ul></td>'
                    "</tr>" % (href(p["slug"]), esc(step_name(p)), lis))
    out.append(
        '<section class="res-section" id="templates" data-res-section><h2>Hand-in templates</h2>'
        "<p>%s</p>"
        '<div class="table-wrap" role="region" aria-label="Hand-in templates" tabindex="0"><table class="grid by-ex">'
        '<thead><tr><th scope="col">Step</th><th scope="col">Templates</th></tr></thead><tbody>%s</tbody></table>'
        "</div></section>" % (fmt(C.SITE["storage_note"]), "".join(rows))
    )
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Page chrome
# ---------------------------------------------------------------------------
def head(title, description, page_id, body_cls):
    # Keep keys stable even when the browser has the previous site.js cached.
    storage_page = BY_SLUG.get(page_id, {}).get("storage_slug", page_id)
    return (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="color-scheme" content="light dark">\n'
        "<title>%s</title>\n"
        '<meta name="description" content="%s">\n'
        '<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">\n'
        '<link rel="stylesheet" href="assets/site.css">\n'
        '<script src="assets/site.js" defer></script>\n'
        "</head>\n"
        '<body class="%s" data-page="%s">\n'
        '<a class="skip-link" href="#main">Skip to content</a>\n'
        % (esc(title), esc(description), body_cls, esc(storage_page))
    )


def topbar(with_menu):
    menu = (
        '<button type="button" class="nav-toggle" aria-controls="sidebar" aria-expanded="false">%s'
        '<span>Steps</span></button>' % icon("menu")
    ) if with_menu else ""
    return (
        '<header class="topbar">\n%s'
        '<a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">HVE</span>'
        '<span class="brand-text">%s<small>%s</small></span></a>\n'
        '<nav class="toplinks" aria-label="Quick links">'
        '<a href="index.html#guide">Guide</a><a href="agenda.html">Agenda</a>'
        '<a href="index.html#intermissions">Intermissions</a><a href="scorecard.html">Scorecard</a>'
        '<a href="resources.html" class="keep">Resources</a></nav>\n</header>\n'
        % (menu, esc(C.SITE["name"]), esc(C.SITE["tagline"]))
    )


def sidebar(current):
    groups = []
    for g in C.GROUPS:
        items = []
        for p in PAGES:
            if p["group"] != g["name"]:
                continue
            cur = ' aria-current="page"' if p["slug"] == current else ""
            items.append('<li><a href="%s"%s>%s<span class="nav-label">%s</span></a></li>' % (
                href(p["slug"]), cur, nav_badge(p), nav_label(p)))
            if p["slug"] == "resources":
                items.append('<li><a href="resources.html#templates"><span class="badge badge-dot" aria-hidden="true">'
                             '</span><span class="nav-label">Hand-in templates</span></a></li>')
        groups.append('<div class="nav-group"><h2>%s</h2><ul>%s</ul></div>' % (esc(g["name"]), "".join(items)))
    return (
        '<aside class="sidebar" id="sidebar">\n<nav class="side-nav" aria-label="Exercise guide">\n'
        '<a class="side-home" href="index.html">← Guide home</a>\n%s\n</nav>\n</aside>\n'
        '<div class="scrim" hidden></div>\n' % "\n".join(groups)
    )


def footer():
    return (
        '<footer class="site-footer"><p>%s</p><p class="muted">%s</p></footer>\n</body>\n</html>\n'
        % (esc(C.SITE["footer"]), fmt(C.SITE["footer_note"]))
    )


def jump_nav(page):
    links = []
    for b in page["blocks"]:
        t = b.get("type")
        if t == "brief":
            links.append(("brief", "Brief"))
        elif t == "section" and b.get("jump"):
            links.append((b["id"], b["jump"]))
        elif t == "shared_ab":
            links.append(("toolkit", "Hand-in and toolkit"))
    if page["kind"] != "info" and any(b.get("type") == "tips" for b in page["blocks"]):
        links.append(("tips", "Tips"))
    if len(links) < 2:
        return ""
    return '<nav class="jump" aria-label="On this page"><span>On this page</span>%s</nav>' % "".join(
        '<a href="#%s">%s</a>' % (i, esc(l)) for i, l in links)


def pager(i):
    prev_p = PAGES[i - 1] if i > 0 else None
    next_p = PAGES[i + 1] if i + 1 < len(PAGES) else None
    parts = []
    if prev_p:
        parts.append('<a class="prev" href="%s" rel="prev"><span class="dir">← Previous</span><span class="ttl">%s'
                     "</span></a>" % (href(prev_p["slug"]), esc(step_name(prev_p))))
    else:
        parts.append('<a class="prev" href="index.html" rel="prev"><span class="dir">← Back to</span>'
                     '<span class="ttl">Guide home</span></a>')
    if next_p:
        parts.append('<a class="next" href="%s" rel="next"><span class="dir">Next →</span><span class="ttl">%s'
                     "</span></a>" % (href(next_p["slug"]), esc(step_name(next_p))))
    return '<nav class="pager" aria-label="Previous and next step">%s</nav>' % "".join(parts)


def render_page(i, page):
    ctx = Ctx(page)
    body = render_blocks(page["blocks"], ctx)
    kind = page["kind"]
    tag = ('<p class="tags"><span class="tag tag-%s">%s</span><span class="tag tag-group">%s</span></p>'
           % (kind, esc(KIND_LABEL[kind]), esc(page["group"]))) if KIND_LABEL.get(kind) else ""
    title = full_title(page)
    html_out = [
        head("%s · HVE workshop guide" % plain(title), plain(page["summary"]), page["slug"],
             "page page-%s kind-%s" % (page["slug"], kind)),
        topbar(True),
        '<div class="layout">\n',
        sidebar(page["slug"]),
        '<main id="main" class="content" tabindex="-1">\n',
        '<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html#guide">Guide</a><span aria-hidden="true">'
        "›</span><span>%s</span></nav>\n" % esc(page["group"]),
        '<header class="page-head">\n<p class="eyebrow">%s</p>\n<h1>%s</h1>\n%s%s</header>\n'
        % (esc(page["eyebrow"]), fmt(page["title"]), tag, jump_nav(page)),
        body,
        "\n" + pager(i) + "\n",
        "</main>\n</div>\n",
        footer(),
    ]
    return "".join(html_out)


HERO_ART = """<svg class="hero-art" viewBox="0 0 900 520" preserveAspectRatio="xMaxYMid slice" aria-hidden="true" focusable="false">
<defs>
<linearGradient id="hs1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2dd4bf" stop-opacity="0"/><stop offset=".55" stop-color="#3b82f6" stop-opacity=".9"/><stop offset="1" stop-color="#5eead4"/></linearGradient>
<linearGradient id="hs2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f59e0b" stop-opacity="0"/><stop offset=".7" stop-color="#f59e0b" stop-opacity=".75"/><stop offset="1" stop-color="#fbbf24" stop-opacity=".25"/></linearGradient>
<linearGradient id="hp" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b6fe0" stop-opacity=".55"/><stop offset="1" stop-color="#1e3a8a" stop-opacity=".08"/></linearGradient>
<linearGradient id="hp2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2dd4bf" stop-opacity=".05"/><stop offset="1" stop-color="#2dd4bf" stop-opacity=".45"/></linearGradient>
</defs>
<g fill="url(#hp)">
<polygon points="560,110 860,40 900,70 600,150"/>
<polygon points="620,330 880,290 900,330 660,372"/>
<polygon points="500,222 830,205 812,238 480,252"/>
<polygon points="700,160 900,130 900,160 720,190"/>
</g>
<polygon fill="url(#hp2)" points="420,268 900,250 900,262 430,276"/>
<g fill="none" stroke-linecap="round">
<path d="M40 300 C 300 292, 540 262, 900 254" stroke="url(#hs1)" stroke-width="3"/>
<path d="M20 322 C 330 304, 570 288, 900 300" stroke="url(#hs1)" stroke-width="1.6" opacity=".75"/>
<path d="M70 282 C 340 270, 570 226, 900 176" stroke="url(#hs1)" stroke-width="1.4" opacity=".6"/>
<path d="M90 344 C 360 334, 610 344, 900 392" stroke="url(#hs1)" stroke-width="1.2" opacity=".5"/>
<path d="M110 306 C 380 300, 610 306, 900 338" stroke="url(#hs2)" stroke-width="1.6"/>
<path d="M140 262 C 400 242, 650 170, 900 112" stroke="url(#hs2)" stroke-width="1" opacity=".7"/>
<path d="M160 330 C 430 340, 650 380, 900 452" stroke="url(#hs1)" stroke-width="1" opacity=".4"/>
</g>
<g fill="#5eead4">
<circle cx="380" cy="270" r="2.2" opacity=".8"/><circle cx="430" cy="300" r="1.6" opacity=".6"/>
<circle cx="470" cy="248" r="2" opacity=".7"/><circle cx="520" cy="318" r="1.4" opacity=".5"/>
<circle cx="345" cy="312" r="1.4" opacity=".5"/><circle cx="560" cy="262" r="2.4" opacity=".8"/>
</g>
<g fill="#f59e0b"><circle cx="410" cy="330" r="1.8" opacity=".7"/><circle cx="505" cy="290" r="1.5" opacity=".6"/>
<rect x="590" y="226" width="5" height="5" transform="rotate(45 592 228)" opacity=".8"/></g>
</svg>"""


def render_home():
    h = C.HOME
    out = [head("%s · %s" % (C.SITE["name"], C.SITE["tagline"]), h["lead"], "index", "home"), topbar(False)]
    out.append(
        '<header class="hero">\n%s\n<div class="hero-inner">\n<p class="kicker">%s</p>\n'
        '<h1>%s<span class="h1-sub">%s</span></h1>\n<p class="hero-lead">%s</p>\n'
        '<p class="cta"><a class="btn btn-primary" href="%s">Start the step-by-step guide</a>'
        '<a class="btn btn-ghost" href="#guide">Jump to an exercise</a>'
        '<a class="btn btn-ghost" href="resources.html">Resources</a></p>\n</div>\n</header>\n'
        % (HERO_ART, esc(h["kicker"]), esc(h["title"]), esc(h["title_line2"]), esc(h["lead"]), href(PAGES[0]["slug"]))
    )
    out.append('<main id="main" class="home-main" tabindex="-1">\n')
    goals = "".join('<li><span class="n" aria-hidden="true">%d</span><p>%s</p></li>' % (i, fmt(g))
                    for i, g in enumerate(h["goals"], 1))
    out.append(
        '<section class="home-today" aria-labelledby="today-h">\n<p class="eyebrow">Today</p>\n'
        '<h2 id="today-h">This is not another presentation</h2>\n'
        '<div class="today-grid"><div><p class="label">%s</p><ol class="goals">%s</ol></div>'
        '<div class="north-star"><p class="label">North-star outcome</p><p>%s</p></div></div>\n'
        '<p class="banner banner-soft">%s</p>\n</section>\n' % (esc(h["goals_title"]), goals, fmt(h["north_star"]),
                                                                fmt(h["quote"]))
    )
    how = "".join('<li><p class="how-title">%s</p><p>%s</p></li>' % (fmt(t), fmt(d)) for t, d in h["how_to_use"])
    out.append('<section class="home-how" aria-labelledby="how-h"><h2 id="how-h">How to use this guide</h2>'
               '<ul class="how">%s</ul><p class="storage-note">%s<span>%s</span></p></section>\n'
               % (how, icon("info"), fmt(C.SITE["storage_note"])))
    cards = []
    for g in C.GROUPS:
        steps = []
        for p in PAGES:
            if p["group"] != g["name"]:
                continue
            kind_txt = KIND_LABEL.get(p["kind"]) or ""
            kind_html = '<span class="tag tag-%s">%s</span>' % (p["kind"], esc(kind_txt)) if kind_txt else ""
            steps.append(
                '<li><a class="step-link" href="%s">%s<span class="step-text"><span class="step-title">%s</span>'
                '<span class="step-sum">%s</span>%s</span></a></li>'
                % (href(p["slug"]), nav_badge(p), nav_label(p), esc(p["summary"]), kind_html)
            )
            if p["slug"] == "resources":
                steps.append(
                    '<li><a class="step-link" href="resources.html#templates"><span class="badge badge-dot" '
                    'aria-hidden="true"></span><span class="step-text"><span class="step-title">Hand-in templates'
                    '</span><span class="step-sum">Every fill-in template, by exercise.</span></span></a></li>')
        cards.append('<div class="group-card"><h3>%s<span>%s</span></h3><ol class="step-list">%s</ol></div>'
                     % (esc(g["name"]), esc(g["note"]), "".join(steps)))
    out.append('<section id="guide" class="home-index" aria-labelledby="guide-h"><p class="eyebrow">Index</p>'
               '<h2 id="guide-h">The step-by-step guide</h2><div class="index-grid">%s</div></section>\n'
               % "".join(cards))
    out.append('<section id="intermissions" class="home-int" aria-labelledby="int-h"><p class="eyebrow">While agents '
               'run</p><h2 id="int-h">Intermissions</h2><p>Nobody watches a progress bar. Pick up an intermission '
               'while your agents work, or see <a href="while-agents-run.html">seven things to do while agents run'
               "</a>.</p>%s</section>\n" % r_intermissions({}, None).replace(
                   '<h2 class="mini-head">Intermissions and backup</h2>', ""))
    res = "".join('<li><a href="resources.html#%s">%s</a></li>' % (i, esc(t)) for i, t in
                  [(s["id"], s["title"]) for s in C.RESOURCES] +
                  [("accelerators", "Accelerators"), ("by-exercise", "Links by exercise"),
                   ("templates", "Hand-in templates")])
    out.append('<section class="home-res" aria-labelledby="res-h"><p class="eyebrow">Materials</p>'
               '<h2 id="res-h">Resources</h2><p>All links for the day are on one page, grouped by topic.</p>'
               '<ul class="res-toc-home">%s</ul></section>\n' % res)
    out.append("</main>\n")
    out.append(footer())
    return "".join(out)


def render_404():
    out = [head("Page not found · HVE workshop guide", "Page not found", "404", "page-404"), topbar(False)]
    out.append('<main id="main" class="content narrow" tabindex="-1"><p class="eyebrow">404</p><h1>Page not found</h1>'
               '<p>That page does not exist. Go back to the <a href="index.html">guide home</a> or the '
               '<a href="resources.html">resources</a>.</p></main>\n')
    out.append(footer())
    return "".join(out)


# ---------------------------------------------------------------------------
# Link check
# ---------------------------------------------------------------------------
class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs = set(), []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("a", "link") and "href" in a:
            self.hrefs.append(a["href"])
        if tag == "script" and "src" in a:
            self.hrefs.append(a["src"])


def check_links(files):
    parsed = {}
    for name in files:
        c = Collector()
        with open(os.path.join(DOCS, name), encoding="utf-8") as fh:
            c.feed(fh.read())
        parsed[name] = c
    problems = []
    for name, c in parsed.items():
        for h in c.hrefs:
            if is_external(h) or h.startswith(("mailto:",)):
                continue
            path, _, frag = h.partition("#")
            target = path or name
            if not os.path.exists(os.path.join(DOCS, target)):
                problems.append("%s: missing file %s" % (name, h))
            elif frag and target in parsed and frag not in parsed[target].ids:
                problems.append("%s: missing anchor %s" % (name, h))
    return problems


def write(name, text):
    with open(os.path.join(DOCS, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def main():
    os.makedirs(DOCS, exist_ok=True)
    files = []
    write("index.html", render_home())
    files.append("index.html")
    for i, p in enumerate(PAGES):
        name = href(p["slug"])
        write(name, render_page(i, p))
        files.append(name)
    write("404.html", render_404())
    files.append("404.html")
    open(os.path.join(DOCS, ".nojekyll"), "w").close()
    problems = check_links(files)
    print("Built %d pages in %s" % (len(files), DOCS))
    if problems:
        print("Link problems:")
        for prob in problems:
            print("  - " + prob)
        sys.exit(1)
    print("All internal links and anchors resolve.")


if __name__ == "__main__":
    main()
