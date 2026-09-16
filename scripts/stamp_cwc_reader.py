#!/usr/bin/env python3
"""Stamp the Creating with Claude reader-resources PDFs (site/downloads/cwc-reader/) per the downloads house rule.

Companion resources (ethics guide, before-you-hit-send, deep research, win tracker) use the same
companion_draw as stamp_downloads.py. The ten chapter quick-reference cards keep their own header
("CREATING WITH CLAUDE ... Chapter N Quick Reference") and get the standard footer: mark, copyright,
"Not for redistribution", page number. Originals stay in 16_With_Claude_Series/Toolkit/3-Reader-Resources/.

Usage: python scripts/stamp_cwc_reader.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stamp_downloads import stamp, companion_draw, MARK, COPY, MUTED, RULE, colors, ROOT
import datetime

READER = "downloads/cwc-reader"

def card_draw(i, n):
    def draw(c, w, h):
        m = 54
        c.setFillColor(colors.white); c.rect(0, 0, w, 37, stroke=0, fill=1)
        c.setStrokeColor(RULE); c.setLineWidth(0.6); c.line(m, 37, w - m, 37)
        c.drawImage(MARK, m, 18, width=16, height=16, mask="auto")
        c.setFont("Helvetica", 7); c.setFillColor(MUTED)
        c.drawString(m + 21, 23.5, COPY)
        c.drawRightString(w - m, 23.5, f"Page {i + 1}")
    return draw

if __name__ == "__main__":
    backup = os.path.join(ROOT, f"downloads_originals_{datetime.date.today().isoformat()}", "cwc-reader")
    for f in sorted(os.listdir(os.path.join(ROOT, "site", READER))):
        if not f.endswith(".pdf"): continue
        p = f"{READER}/{f}"
        draw = card_draw if "quick-reference" in f else companion_draw
        print(f"{p}: {stamp(p, draw, backup)} pages")
    print("originals in", backup)
