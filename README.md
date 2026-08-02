# תשחץ פסיכומטרי

A Hebrew arrowword (תשחץ) built from the psychometric-exam vocabulary list.
122 levels that unlock one after another, ~35 answers per board.

## Layout
- `data/words.txt` — single-word entries, `word|definition`
- `data/phrases.txt` — multi-word idioms, same format
- `data/allwords.txt` — the two above, merged and deduped (the exam bank)
- `data/conn.txt` — everyday connector words used only as grid mortar
- `template.html` — the app; `__WORDS__` / `__CONN__` are filled in at build time
- `index.html` — the built, self-contained page (open it directly in a browser)

## Build
```sh
python3 build.py
```

## Editing the vocabulary
Add or fix a line in `data/words.txt` (or `phrases.txt`), re-merge, rebuild:
```sh
cat data/words.txt data/phrases.txt | sort -u > data/allwords.txt
python3 build.py
```
Levels are ordered by difficulty at load time, so adding words reshuffles which
level a word lands in.

## Notes
- Boards are generated in the browser from a seed derived from the level number,
  so a given level is always the same puzzle. "ערבב מחדש" re-rolls the seed.
- Progress is stored in `localStorage` under `hebArrowword.v1`.
