# תשחץ פסיכומטרי

A Hebrew arrowword (תשחץ) built from the psychometric exam vocabulary — both the Hebrew
list and the English one. 359 levels that unlock one after another; each board carries the
level's 8 exam words plus mortar borrowed from neighbouring levels, so words recur.

Clues sit inside the grid with an arrow pointing at the answer, printed-puzzle style.
A Hebrew clue is a definition; an English clue is the word itself and the answer is its
Hebrew translation. Where a clue accepts several translations, the builder uses whichever
one interlocks best — the pattern above the grid shows the letter count.

## Layout
- `data/he_source.txt` — Hebrew list, `word|definition` (parsed from the source .docx)
- `data/en_source.txt` — English list, `word|translation;translation;…` (parsed from the source PDF)
- `data/bank.txt` — generated: `level|language|clue|answers`
- `make_bank.py` — rebuilds `bank.txt`: difficulty order, level grouping, length spreading
- `template.html` — the app; `__BANK__` is filled in at build time
- `index.html` — the built, self-contained page (open it directly in a browser)

## Build
```sh
python3 make_bank.py && python3 build.py
```

## Notes
- Boards are generated in the browser from a seed derived from the level number, so a given
  level is always the same puzzle. "ערבב מחדש" re-rolls the seed.
- Progress is stored in `localStorage` under `hebArrowword.v1`.
- Answers use the source lists' spelling, which is often defective (כתיב חסר): שסף, נכש, קלס.
