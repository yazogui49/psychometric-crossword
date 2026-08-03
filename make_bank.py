#!/usr/bin/env python3
"""Turn the two exam vocabulary lists into data/bank.txt.

    level | language | clue | answer;answer;...

An English clue often accepts several Hebrew translations; all are kept so the grid
builder can use whichever one interlocks best. Difficulty leans on how much explaining
a word needs rather than on how long the answer is - sorting by length alone buries all
the two-letter words in level 1, and words that short barely intersect anything.
Inside each difficulty block the answer lengths are dealt round-robin across levels so
no board is made entirely of short words.
"""
import re, pathlib

root = pathlib.Path(__file__).parent
FIN = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}
letters = lambda a: "".join(FIN.get(c, c) for c in a).replace(" ", "")

he, en = [], []
for line in (root / "data/he_source.txt").read_text(encoding="utf-8").splitlines():
    w, d = line.split("|", 1)
    w = re.sub(r"[^א-ת ]", "", w).strip()
    if 2 <= len(letters(w)) <= 11 and len(d.strip()) > 2:
        he.append((d.strip(), [w]))
for line in (root / "data/en_source.txt").read_text(encoding="utf-8").splitlines():
    c, a = line.split("|", 1)
    if "..." in c or "…" in c:            # sentence patterns, not answerable words
        continue
    ans = [x for x in a.split(";") if x and len(letters(x)) >= 2]
    if ans:
        en.append((c.strip(), ans))

nz = lambda v: [(x - min(v)) / ((max(v) - min(v)) or 1) for x in v]
def order(items, weights):
    a = nz([len(letters(x[1][0])) for x in items])
    b = nz([min(len(x[0]), 90) for x in items])
    wa, wb = weights
    score = [wa * a[i] + wb * b[i] for i in range(len(items))]
    return [items[i] for i in sorted(range(len(items)), key=lambda i: score[i])]

def groups(seq, per=4, per_block=6):
    out = []
    for i in range(0, len(seq), per * per_block):
        block = sorted(seq[i:i + per * per_block], key=lambda x: len(letters(x[1][0])))
        buckets = [[] for _ in range(per_block)]
        for k, item in enumerate(block):
            buckets[k % per_block].append(item)
        out += [b for b in buckets if b]
    return out

hg = groups(order(he, (0.15, 0.85)))
eg = groups(order(en, (0.15, 0.85)))
levels, i, j = [], 0, 0
while i < len(hg) or j < len(eg):
    lvl = []
    if i < len(hg):
        lvl += [("he",) + x for x in hg[i]]; i += 1
    if j < len(eg):
        lvl += [("en",) + x for x in eg[j]]; j += 1
    if i >= len(hg) and j < len(eg):       # hebrew exhausted: fill the level with english
        lvl += [("en",) + x for x in eg[j]]; j += 1
    if len(lvl) >= 5:
        levels.append(lvl)

with (root / "data/bank.txt").open("w", encoding="utf-8") as f:
    for n, lvl in enumerate(levels):
        for lang, clue, ans in lvl:
            clue = clue.replace("|", "/").replace("`", "'").strip()
            f.write(f"{n}|{lang}|{clue}|{';'.join(x.replace('|', '/') for x in ans)}\n")
print(f"bank.txt: {sum(len(l) for l in levels)} entries, {len(levels)} levels")
