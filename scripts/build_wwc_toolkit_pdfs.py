#!/usr/bin/env python3
"""Build the Writing with Claude toolkit PDFs in the Marque companion-resource style.

House style (matches the existing site downloads, plus the brand mark + copyright they lacked):
  Helvetica, rust accent (#C4623A), header band "WRITING WITH CLAUDE | Companion Resource",
  footer: Marque lozenge mark + "(c) 2026 Chris Thatcher . Marque Publishing, LLC . marquepublishing.com" + page.

Layout rules:
  * Every "##" section is a card: it starts on a new page.
  * A card is auto-fitted to ONE page by stepping the type size down (100% -> 80%). If it still
    won't fit, it runs to a second page and breaks only between "###" blocks (never inside one).
  * Tables never split across pages. Paragraphs never leave widows or orphans. Headings stay
    with the content that follows them.

Usage:
  python scripts/build_wwc_toolkit_pdfs.py <appendix.md> <editorial_brief.md> <cover_brief.md> <out_dir>
"""
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, PageBreak, ListFlowable, ListItem, HRFlowable, Image,
)

HERE = os.path.dirname(os.path.abspath(__file__))
MARK_PNG = os.path.join(HERE, "..", "branding", "brand_assets", "web", "2A_Marque_Loz_Mark.png")
YEAR = "2026"
COPYRIGHT = f"© {YEAR} Chris Thatcher  ·  Marque Publishing, LLC  ·  marquepublishing.com  ·  Not for redistribution"

RUST = colors.HexColor("#C4623A")
INK = colors.HexColor("#1B2430")
MUTED = colors.HexColor("#5A6470")
OLIVE = colors.HexColor("#7A7A5C")
RULE = colors.HexColor("#D9D4CA")
TABLE_HEAD = colors.HexColor("#F3EFE7")
CODE_BG = colors.HexColor("#F5F1EA")

PAGE_W, PAGE_H = letter
MARGIN = 0.85 * inch
TOP = 1.0 * inch
BOTTOM = 0.95 * inch
AVAIL_W = PAGE_W - 2 * MARGIN
AVAIL_H = PAGE_H - TOP - BOTTOM


def make_styles(k=1.0):
    """All type sizes scaled by k so a card can be shrunk to fit one page."""
    def ps(name, **kw):
        return ParagraphStyle(name, allowWidows=0, allowOrphans=0, **kw)
    S = {}
    S["body"] = ps("body", fontName="Helvetica", fontSize=10 * k, leading=14.5 * k, textColor=INK, spaceAfter=7 * k)
    S["lead"] = ps("lead", fontName="Helvetica-Oblique", fontSize=10.5 * k, leading=15.5 * k, textColor=MUTED, spaceAfter=10 * k)
    S["h1"] = ps("h1", fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=INK, spaceAfter=6)
    S["sub"] = ps("sub", fontName="Helvetica", fontSize=13, leading=17, textColor=MUTED, spaceAfter=14)
    S["part"] = ps("part", fontName="Helvetica-Bold", fontSize=18 * k, leading=22 * k, textColor=INK, spaceBefore=6 * k, spaceAfter=8 * k, keepWithNext=1)
    S["h2"] = ps("h2", fontName="Helvetica-Bold", fontSize=15 * k, leading=19 * k, textColor=RUST, spaceBefore=4 * k, spaceAfter=6 * k, keepWithNext=1)
    S["h3"] = ps("h3", fontName="Helvetica-Bold", fontSize=11 * k, leading=14 * k, textColor=OLIVE, spaceBefore=8 * k, spaceAfter=3 * k, keepWithNext=1)
    S["quote"] = ps("quote", fontName="Helvetica", fontSize=10 * k, leading=14.5 * k, textColor=INK, leftIndent=14 * k)
    S["bullet"] = ps("bullet", fontName="Helvetica", fontSize=10 * k, leading=14.5 * k, textColor=INK, spaceAfter=3 * k)
    S["cell"] = ps("cell", fontName="Helvetica", fontSize=8.8 * k, leading=11.5 * k, textColor=INK)
    S["cellhead"] = ps("cellhead", fontName="Helvetica-Bold", fontSize=8.8 * k, leading=11.5 * k, textColor=INK)
    S["code"] = ps("code", fontName="Courier", fontSize=8.5 * k, leading=11 * k, textColor=INK, backColor=CODE_BG,
                   leftIndent=8, rightIndent=8, borderPadding=6, spaceBefore=4 * k, spaceAfter=10 * k)
    S["k"] = k
    return S


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s, k=1.0):
    s = esc(s)
    s = s.replace(" -- ", " — ").replace("--", "—")
    s = re.sub(r"`([^`]+)`", rf'<font face="Courier" size="{8.5 * k:.1f}">\1</font>', s)
    s = re.sub(r"\*\*\*(.+?)\*\*\*", r"<b><i>\1</i></b>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<i>\1</i>", s)
    return s


def parse_table(lines):
    rows = []
    for ln in lines:
        ln = ln.strip()
        if re.match(r"^\|?\s*:?-{3,}", ln):
            continue
        rows.append([c.strip() for c in ln.strip("|").split("|")])
    return rows


def table_flowable(rows, S):
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    if ncol == 2:
        widths = [AVAIL_W * 0.32, AVAIL_W * 0.68]
    else:
        maxlen = [max(len(r[c]) for r in rows) for c in range(ncol)]
        weights = [max(14, min(m, 60)) for m in maxlen]
        tot = sum(weights)
        widths = [AVAIL_W * w / tot for w in weights]
    data = [[Paragraph(inline(c, S["k"]), S["cellhead"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    pad = 5 * S["k"]
    t = Table(data, colWidths=widths, repeatRows=1, splitByRow=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, RUST),
        ("LINEBELOW", (0, 1), (-1, -1), 0.4, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


# ---------------------------------------------------------------- markdown -> blocks

def split_sections(md):
    """Return (preamble_lines, [(part_title|None, h2_title, lines)]) — a card per '##'."""
    lines = md.split("\n")
    pre, cards = [], []
    cur_part = None
    part_intro = []
    cur = None
    seen_part = False
    for ln in lines:
        s = ln.strip()
        if s.startswith("# "):
            cur_part = s[2:].strip()
            part_intro = []
            seen_part = True
            if cur is not None:
                cards.append(cur); cur = None
            continue
        if s.startswith("## "):
            if cur is not None:
                cards.append(cur)
            # the part's intro lines ride at the top of its first card
            cur = [cur_part, s[3:].strip(), [], list(part_intro)]
            cur_part = None; part_intro = []
            continue
        if cur is None:
            (part_intro if seen_part else pre).append(ln)
        else:
            cur[2].append(ln)
    if cur is not None:
        cards.append(cur)
    return pre, cards


def lines_to_flowables(lines, S):
    """Body lines (no headings above ###) -> list of 'blocks'. Each block is a list of flowables
    that must stay together (an ### heading plus everything under it until the next ###)."""
    k = S["k"]
    blocks = [[]]
    para = []
    i = 0

    def cur():
        return blocks[-1]

    def flush_para():
        nonlocal para
        if para:
            cur().append(Paragraph(inline(" ".join(x.strip() for x in para), k), S["body"]))
            para = []

    while i < len(lines):
        ln = lines[i]; s = ln.strip()
        if not s:
            flush_para(); i += 1; continue
        if s.startswith("### "):
            flush_para()
            blocks.append([Paragraph(inline(s[4:].strip(), k), S["h3"])])
            i += 1; continue
        if s.startswith("```"):
            flush_para(); block = []; i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i]); i += 1
            i += 1
            cur().append(Paragraph("<br/>".join(esc(b) for b in block).replace(" ", "&nbsp;"), S["code"]))
            continue
        if s in ("* * *", "---", "***"):
            flush_para()
            cur().append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceBefore=4 * k, spaceAfter=8 * k))
            i += 1; continue
        if s.startswith("|"):
            flush_para(); block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i]); i += 1
            rows = parse_table(block)
            if rows:
                cur().append(table_flowable(rows, S)); cur().append(Spacer(1, 8 * k))
            continue
        if re.match(r"^\s*[-*]\s+", ln) or re.match(r"^\s*\d+\.\s+", ln):
            flush_para(); items = []
            numbered = bool(re.match(r"^\s*\d+\.\s+", ln))
            while i < len(lines) and (re.match(r"^\s*[-*]\s+", lines[i]) or re.match(r"^\s*\d+\.\s+", lines[i])):
                txt = re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i]); j = i + 1
                while j < len(lines) and lines[j].strip() and not re.match(r"^\s*([-*]|\d+\.)\s+", lines[j]) and not lines[j].strip().startswith(("|", "#", ">", "```")):
                    txt += " " + lines[j].strip(); j += 1
                items.append(ListItem(Paragraph(inline(txt, k), S["bullet"]), leftIndent=14 * k))
                i = j
            cur().append(ListFlowable(items, bulletType="1" if numbered else "bullet", start="1" if numbered else None,
                                      bulletFontName="Helvetica", bulletFontSize=9 * k, bulletColor=RUST, leftIndent=14 * k))
            cur().append(Spacer(1, 4 * k))
            continue
        if s.startswith(">"):
            flush_para(); block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip()[1:].strip()); i += 1
            qt = Table([[Paragraph(inline(" ".join(b for b in block if b), k), S["quote"])]], colWidths=[AVAIL_W])
            qt.setStyle(TableStyle([("LINEBEFORE", (0, 0), (0, -1), 2, RUST), ("LEFTPADDING", (0, 0), (-1, -1), 4),
                                    ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
            cur().append(qt); cur().append(Spacer(1, 6 * k))
            continue
        para.append(ln); i += 1
    flush_para()
    return [b for b in blocks if b]


_DUMMY_CANVAS = None


def _dummy_canvas():
    global _DUMMY_CANVAS
    if _DUMMY_CANVAS is None:
        import io
        from reportlab.pdfgen.canvas import Canvas
        _DUMMY_CANVAS = Canvas(io.BytesIO(), pagesize=letter)
    return _DUMMY_CANVAS


def measure(flowables):
    h = 0
    cv = _dummy_canvas()
    for f in flowables:
        f.canv = cv
        w, fh = f.wrap(AVAIL_W, AVAIL_H * 10)
        h += fh + getattr(f, "getSpaceBefore", lambda: 0)() + getattr(f, "getSpaceAfter", lambda: 0)()
    return h


def build_card(part_title, h2_title, lines, intro=None, allow_two_pages=True):
    """Fit a card to one page by stepping the scale down; fall back to clean multi-page."""
    for k in (1.0, 0.95, 0.9, 0.86, 0.82, 0.78):
        S = make_styles(k)
        head = []
        if part_title:
            head.append(Paragraph(inline(part_title, k), S["part"]))
            head.append(HRFlowable(width="100%", thickness=1.2, color=RUST, spaceBefore=0, spaceAfter=8 * k))
            if intro and any(l.strip() for l in intro):
                head += [x for b in lines_to_flowables(intro, S) for x in b]
        head.append(Paragraph(inline(h2_title, k), S["h2"]))
        blocks = lines_to_flowables(lines, S)
        flat = head + [f for b in blocks for f in b]
        if measure(flat) <= AVAIL_H:
            return [KeepTogether(flat)], k, 1
    # does not fit one page even at 78%: use 100% and keep each ### block whole
    S = make_styles(0.92)
    head = []
    if part_title:
        head.append(Paragraph(inline(part_title, 0.92), S["part"]))
        head.append(HRFlowable(width="100%", thickness=1.2, color=RUST, spaceBefore=0, spaceAfter=8))
        if intro and any(l.strip() for l in intro):
            head += [x for b in lines_to_flowables(intro, S) for x in b]
    head.append(Paragraph(inline(h2_title, 0.92), S["h2"]))
    blocks = lines_to_flowables(lines, S)
    out = [KeepTogether(head + blocks[0])] if blocks else head
    for b in blocks[1:]:
        # a block taller than a page (a long table) must be allowed to split by row
        if measure(b) > AVAIL_H:
            out.extend(b)
        else:
            out.append(KeepTogether(b))
    return out, 0.92, 2


def on_page_factory(kicker):
    def on_page(canvas, doc):
        canvas.saveState()
        # header band
        canvas.setFont("Helvetica-Bold", 9); canvas.setFillColor(RUST)
        canvas.drawString(MARGIN, PAGE_H - 0.62 * inch, kicker)
        canvas.setFont("Helvetica", 9); canvas.setFillColor(MUTED)
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.62 * inch, "Companion Resource  ·  Not for redistribution")
        canvas.setStrokeColor(RULE); canvas.setLineWidth(0.6)
        canvas.line(MARGIN, PAGE_H - 0.72 * inch, PAGE_W - MARGIN, PAGE_H - 0.72 * inch)
        # footer: mark + copyright + page
        canvas.line(MARGIN, 0.74 * inch, PAGE_W - MARGIN, 0.74 * inch)
        if os.path.exists(MARK_PNG):
            canvas.drawImage(MARK_PNG, MARGIN, 0.40 * inch, width=0.26 * inch, height=0.26 * inch, mask="auto")
        canvas.setFont("Helvetica", 7.5); canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN + 0.34 * inch, 0.48 * inch, COPYRIGHT)
        canvas.drawRightString(PAGE_W - MARGIN, 0.48 * inch, f"Page {doc.page}")
        canvas.restoreState()
    return on_page


def build(md_path, out_path, title, subtitle, lead, kicker="WRITING WITH CLAUDE", cards=True):
    md = open(md_path, encoding="utf-8").read()
    md = re.sub(r"^\*Draft v\d+ --.*?\*\n", "", md, count=1, flags=re.M | re.S)
    S1 = make_styles(1.0)

    doc = BaseDocTemplate(out_path, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=TOP, bottomMargin=BOTTOM,
                          title=title, author="Chris Thatcher", subject="Writing with Claude companion resource")
    frame = Frame(MARGIN, BOTTOM, AVAIL_W, AVAIL_H, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page_factory(kicker))])

    story = [Spacer(1, 10), Paragraph(inline(title), S1["h1"])]
    if subtitle:
        story.append(Paragraph(inline(subtitle), S1["sub"]))
    story.append(HRFlowable(width="100%", thickness=1.2, color=RUST, spaceBefore=2, spaceAfter=12))
    if lead:
        story.append(Paragraph(inline(lead), S1["lead"]))
    story.append(Paragraph(f"Copyright © {YEAR} Chris Thatcher. Published by Marque Publishing, LLC. "
                           "Free for readers of <i>Writing with Claude</i>. Not for resale or redistribution.", S1["lead"]))

    pre, sections = split_sections(md)
    report = []
    if not cards:
        # briefs: one flowing document, headings kept with content, tables whole
        for f in [x for b in lines_to_flowables(pre, S1) for x in b]:
            story.append(f)
        for part, h2, lines, intro in sections:
            blocks = lines_to_flowables(lines, S1)
            h = Paragraph(inline(h2), S1["h2"])
            if blocks:
                story.append(KeepTogether([h] + blocks[0]))
                for blk in blocks[1:]:
                    story.append(KeepTogether(blk) if measure(blk) <= AVAIL_H else blk[0])
            else:
                story.append(h)
    else:
        # preamble (the appendix intro) stays on the title page; drop its own H1
        pre = [l for l in pre if not l.strip().startswith("# ")]
        for f in [x for b in lines_to_flowables(pre, S1) for x in b]:
            story.append(f)
        for part, h2, lines, intro in sections:
            story.append(PageBreak())
            flows, k, pages = build_card(part, h2, lines, intro)
            story.extend(flows)
            report.append((h2, k, pages))
    doc.build(story)
    return report


if __name__ == "__main__":
    appendix, ed_brief, cv_brief, out_dir = sys.argv[1:5]
    rep = build(appendix, f"{out_dir}/writing-with-claude-reference-guides.pdf",
                "The Machine: Quick Reference Guides",
                "Every file in your project, and a guide for every chapter's build",
                "The book's appendix, for readers of *Writing with Claude* who signed up at marquepublishing.com. "
                "Part One is the artifact reference, one card per file. Part Two is the chapter-by-chapter process guide, "
                "one card per chapter. Print them, mark them up, give them to Claude.")
    for h2, k, pages in rep:
        print(f"  {h2:<48} scale {k:.2f}  {'1 page' if pages == 1 else 'multi-page'}")
    build(ed_brief, f"{out_dir}/editorial-brief-template.pdf", "Editorial Brief",
          "Fill-in template — write it before you talk to an editor", None, cards=False)
    build(cv_brief, f"{out_dir}/cover-brief-template.pdf", "Cover Brief",
          "Fill-in template — write it before you look at a single image", None, cards=False)
    print("built 3 PDFs in", out_dir)
