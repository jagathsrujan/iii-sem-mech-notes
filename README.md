# III Sem Mech Notes

Study notes for the III semester B.Tech Mechanical Engineering exams (UVCE, scheme 2026): Strength of Materials, Thermal Engineering, Material Science and Engineering, and Manufacturing Technology.

**Read the notes:** https://jagathsrujan.github.io/iii-sem-mech-notes/

Each unit has:

- **Concepts** with labelled diagrams, formula boxes, real photos, flashcards and a self-check quiz.
- **Theory questions** with model answers in exam format.
- **Numericals** with step-by-step solutions (Practice mode shows one step at a time) and practice problems.
- **Interactive widgets**: SFD/BMD of a beam, torsion, Mohr's circle, Carnot engine, VCR cycle, unit cells, lever rule, Merchant circle and others.
- **A study tracker**: target time and due date for each section, with a stopwatch. On this site, progress saves in your browser only.

Units are added as they are written and checked. Topics follow the 2026 syllabus; old question papers are used only as practice questions.

## How it is built

- `content/<unit>.html` — one HTML fragment per unit (formulas written in TeX).
- `units.json` — units, syllabus text, target minutes and due dates.
- `build.py` — lints each unit (`lint.py`) and converts every TeX formula to SVG (`tools/tex2svg.js`, MathJax 3), so the page needs no maths library at run time.
- `publish.py` — builds `docs/` (served by GitHub Pages) from the units listed in `published.json`.
- `NOTES_SPEC.md` — the writing and diagram rules every unit follows.

Rebuild: `cd tools && npm install && cd .. && python3 publish.py --no-push`

## Credits

Photos are from Wikimedia Commons and keep their own licences; see [CREDITS.md](CREDITS.md). Notes written with the help of Claude (Anthropic).
