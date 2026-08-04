#!/usr/bin/env python3
"""Turn the two exam vocabulary lists into data/bank.txt.

    level | language | clue | answer;answer;...

An English clue often accepts several Hebrew translations; all are kept so the grid
builder can use whichever one interlocks best.

Difficulty comes from corpus word frequency (wordfreq), but not in a straight line.
Frequency is U-shaped here: a word nobody uses is hard, and a word everybody uses is
*also* hard when it appears on this list, because the sense being tested is not the
familiar one - את is a spade, בית is to domesticate, מעל is to embezzle. The easy words
sit in the middle of the frequency range. Definition length is kept as a small
secondary signal.

Inside each difficulty block the answer lengths are dealt round-robin across levels, so
no board is built entirely of two-letter words, which barely intersect anything.

Requires: python3 -m pip install --user wordfreq   (only to regenerate bank.txt)
"""
import re, pathlib
from wordfreq import zipf_frequency

root = pathlib.Path(__file__).parent
FIN = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}
letters = lambda a: "".join(FIN.get(c, c) for c in a).replace(" ", "")

def freq(text, lang):
    parts = [p for p in text.split() if p]
    return min(zipf_frequency(p, lang) for p in parts) if parts else 0.0

def hardness(f, trap_from, trap_span, trap_cap):
    rare = max(0.0, min(1.0, (6.0 - f) / 6.0))
    trap = max(0.0, min(trap_cap, (f - trap_from) / trap_span))
    return max(rare, trap)

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

def order(items, lang, trap):
    if lang == "he":
        core = [hardness(freq(x[1][0], "he"), *trap) for x in items]      # score the answer
    else:
        core = [hardness(freq(x[0], "en"), *trap) for x in items]         # score the clue
    extra = nz([min(len(x[0]), 90) for x in items])
    score = [0.8 * core[i] + 0.2 * extra[i] for i in range(len(items))]
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

hg = groups(order(he, "he", (4.2, 2.2, 0.85)))
eg = groups(order(en, "en", (5.6, 1.6, 0.55)))   # english traps are milder, senses are given
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
