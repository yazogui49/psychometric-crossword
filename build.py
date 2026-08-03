#!/usr/bin/env python3
"""Assemble index.html from the template and the word bank.

The template is body content only, so the same file can be published as a Claude
artifact (which supplies its own document shell). For the standalone file we wrap it
in a real document - without the viewport meta a phone renders the board at desktop
width. Regenerate data/bank.txt with make_bank.py after editing a source list.
"""
import pathlib

root = pathlib.Path(__file__).parent
bank = (root / "data/bank.txt").read_text(encoding="utf-8").strip()
body = (root / "template.html").read_text(encoding="utf-8").replace("__BANK__", bank)
assert "__BANK__" not in body

levels = len({l.split("|")[0] for l in bank.splitlines()})
doc = f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#1C1C1E">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-title" content="תשחץ">
</head>
<body>
{body}
</body>
</html>
"""
(root / "index.html").write_text(doc, encoding="utf-8")
print(f"index.html: {len(bank.splitlines())} entries across {levels} levels")
