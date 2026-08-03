#!/usr/bin/env python3
"""Assemble index.html from the template and the word banks.

The template is body content only, so that the same file can be published as a
Claude artifact (which supplies its own document shell). For the standalone file
we wrap it in a real document - without the viewport meta a phone renders the
board at desktop width.
"""
import pathlib

root = pathlib.Path(__file__).parent
words = (root / "data/allwords.txt").read_text(encoding="utf-8").strip()
conn = (root / "data/conn.txt").read_text(encoding="utf-8").strip()
body = (root / "template.html").read_text(encoding="utf-8")
body = body.replace("__WORDS__", words).replace("__CONN__", conn)
assert "__WORDS__" not in body and "__CONN__" not in body

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
print(f"index.html: {len(words.splitlines())} exam entries, {len(conn.splitlines())} connectors")
