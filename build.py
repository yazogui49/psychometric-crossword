#!/usr/bin/env python3
"""Assemble index.html from the template and the word banks."""
import pathlib
root = pathlib.Path(__file__).parent
words = (root / "data/allwords.txt").read_text(encoding="utf-8").strip()
conn  = (root / "data/conn.txt").read_text(encoding="utf-8").strip()
html  = (root / "template.html").read_text(encoding="utf-8")
out   = html.replace("__WORDS__", words).replace("__CONN__", conn)
assert "__WORDS__" not in out and "__CONN__" not in out
(root / "index.html").write_text(out, encoding="utf-8")
print(f"index.html: {len(words.splitlines())} exam entries, {len(conn.splitlines())} connectors")
