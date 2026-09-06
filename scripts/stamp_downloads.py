#!/usr/bin/env python3
"""Stamp the existing site downloads with the Marque mark, copyright, and "Not for redistribution".

The five companion-resource PDFs (Creating with Claude) were generated without saved sources, so
this re-paints their header-right label and footer in place. The book samples and the board guide
get an added footer line only (their own copyright pages stay as they are).

Originals are copied to <project>/downloads_originals_<date>/ (project root — never deployed).

Usage: python scripts/stamp_downloads.py
"""
import datetime
import io
import os
import shutil

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SITE = os.path.join(ROOT, "site")
MARK = os.path.join(ROOT, "branding", "brand_assets", "web", "2A_Marque_Loz_Mark.png")
YEAR = "2026"
COPY = f"© {YEAR} Chris Thatcher  ·  Marque Publishing, LLC  ·  marquepublishing.com  ·  Not for redistribution"
RUST = colors.HexColor("#C4623A")
MUTED = colors.HexColor("#5A6470")
RULE = colors.HexColor("#D9D4CA")

COMPANIONS = [
    "downloads/ai-output-verification-checklist.pdf",
    "downloads/ai-readiness-self-assessment.pdf",
    "downloads/custom-instructions-builder.pdf",
    "downloads/prompt-library-starter-kit.pdf",
    "downloads/what-should-i-build-idea-generator.pdf",
]
BOARD_GUIDE = "10-cybersecurity-decisions.pdf"
SAMPLES = ["downloads/creating-with-claude-sample.pdf", "downloads/cyber-risk-sample.pdf"]


def overlay(w, h, draw):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    draw(c, w, h)
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def stamp(path, draw_for_page, backup_dir):
    src = os.path.join(SITE, path)
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy2(src, os.path.join(backup_dir, os.path.basename(path)))
    reader = PdfReader(src)
    writer = PdfWriter()
    n = len(reader.pages)
    for i, page in enumerate(reader.pages):
        w = float(page.mediabox.width); h = float(page.mediabox.height)
        draw = draw_for_page(i, n)
        if draw is not None:
            page.merge_page(overlay(w, h, draw))
        writer.add_page(page)
    writer.add_metadata({"/Author": "Chris Thatcher", "/Producer": "Marque Publishing"})
    with open(src, "wb") as f:
        writer.write(f)
    return n


def companion_draw(i, n):
    """Companion resources: margins 54pt. Repaint header-right label and the whole footer."""
    def draw(c, w, h):
        m = 54
        # header right: white-out "Companion Resource", redraw with the redistribution note
        c.setFillColor(colors.white); c.rect(w * 0.55, h - 58, w * 0.45 - m + 8, 24, stroke=0, fill=1)
        c.setFont("Helvetica", 9); c.setFillColor(MUTED)
        c.drawRightString(w - m, h - 44.9 + 0.5, "Companion Resource  ·  Not for redistribution")
        # footer: white-out below the footer rule, redraw with mark + copyright + page
        c.setFillColor(colors.white); c.rect(0, 0, w, 37, stroke=0, fill=1)
        c.setStrokeColor(RULE); c.setLineWidth(0.6); c.line(m, 37, w - m, 37)
        c.drawImage(MARK, m, 18, width=16, height=16, mask="auto")
        c.setFont("Helvetica", 7); c.setFillColor(MUTED)
        c.drawString(m + 21, 23.5, COPY)
        c.drawRightString(w - m, 23.5, f"Page {i + 1}")
    return draw


def board_guide_draw(i, n):
    """Board guide: dark cover page untouched; interior pages get a footer line beside the centered folio."""
    if i == 0:
        return None
    def draw(c, w, h):
        m = 72
        txt = f"© {YEAR} Chris Thatcher  ·  Marque Publishing, LLC  ·  Not for redistribution"
        c.setFont("Helvetica", 6.5); c.setFillColor(MUTED)
        tw = c.stringWidth(txt, "Helvetica", 6.5)
        c.drawImage(MARK, w - m - tw - 17, 33, width=13, height=13, mask="auto")
        c.drawRightString(w - m, 37.5, txt)
    return draw


def sample_draw(i, n):
    """Book samples: a tiny line at the foot of every page; nothing else touched."""
    def draw(c, w, h):
        c.setFont("Helvetica", 6); c.setFillColor(MUTED)
        c.drawCentredString(w / 2, 14, f"© {YEAR} Chris Thatcher  ·  Marque Publishing, LLC  ·  Preview copy  ·  Not for redistribution")
    return draw


if __name__ == "__main__":
    backup = os.path.join(ROOT, f"downloads_originals_{datetime.date.today().isoformat()}")
    for p in COMPANIONS:
        print(f"{p}: {stamp(p, companion_draw, backup)} pages")
    print(f"{BOARD_GUIDE}: {stamp(BOARD_GUIDE, board_guide_draw, backup)} pages")
    for p in SAMPLES:
        print(f"{p}: {stamp(p, sample_draw, backup)} pages")
    print("originals in", backup)
