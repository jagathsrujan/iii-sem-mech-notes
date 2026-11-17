# Exam notes — fragment spec (read all of it before you write)

You write ONE unit of exam notes for a 3rd-semester B.Tech Mechanical student at UVCE Bengaluru (exams 2–9 Dec 2026). The notes are read on a laptop and a phone inside a web app that loads your file into a page. The student must be able to learn the unit from your notes alone, answer 10-mark theory questions, draw the sketches, and solve the numericals.

Everything is in one build folder; call it `$SITE` (the absolute path is in your brief). Run `ls $SITE` first. If it fails, stop and report.

## 1. Scope rules (from the student, non-negotiable)

- The **2026 syllabus** (`$SITE/_src/syllabus-2026.txt`) decides the topics. Your unit's syllabus text is also in `$SITE/units.json`. Cover every topic named there.
- **Old question papers** (`$SITE/_src/papers/*.txt`, schemes UG-2022 and CBCS) are **reference only**: use them as practice questions on syllabus topics. Skip old questions on topics the 2026 syllabus does not list (for example thermal stresses in SoM, fuels and combustion in Thermal). The text in these files comes from a scan; figures are missing and numbers can be garbled — repair obvious OCR errors, and if a figure is missing, rewrite the problem so it is complete without the figure (and draw the figure yourself).
- **2026 question banks** (`$SITE/_src/qb-mse-2026.txt`, `$SITE/_src/qb-mt-2026.txt`) and the **MSE assignment** (`$SITE/_src/assignment-mse-2026.txt`) are current teacher material. Your unit lists its question numbers in `units.json` (`qb`, `assignment`). Answer **every** listed question as a theory question, even where the syllabus does not name the topic. Follow the teacher's values (e.g. eutectoid 0.8 % C).
- **Existing notes** from the student's internal tests are in `$SITE/_src/internals/` (HTML). Reuse their correct content and diagrams ideas; do not copy their CSS.

## 2. Length budget (the student has a time limit)

`units.json` gives your unit `targets` (minutes the student has for each part) and `budget` (concept words, number of theory questions, solved and practice numericals). Stay inside the budget: the visible concept text should fit the word range; put extra depth in collapsed model answers (`<details class="answer">`). If the unit has no `numericals` target, do not write a numericals section.

## 3. Language

- Explanations: clear, simple English. Short sentences (aim ≤ 20 words), active voice, one idea per paragraph, bullet lists for 3+ items.
- Definitions, statements of laws and model answers: standard textbook / exam wording that earns marks. Model answers are structured like a top-scoring exam answer: definition → neat labelled sketch → explanation in points → advantages / limitations / applications as the question asks.
- Units and numbers: SI units, figures with units (e.g. 200 GPa, 12 mm).

## 4. Output files

1. `$SITE/content/<unit-id>.html` — the fragment (UTF-8).
2. `$SITE/manifest/<unit-id>.json` — a JSON array with one object per photo you use (see §8). Write `[]` if you use none.
3. Photos in `$SITE/img/` named `<unit-id>-<slug>.jpg` (or `.png`).
4. Your own working files (scripts, renders) go in `$SITE/_work/<unit-id>/` only.

Write only these files. Do not touch other units' files, `units.json`, this spec, or anything outside `$SITE`.

## 5. Fragment structure (exact)

The file is an HTML **fragment**: no `<!doctype>`, `<html>`, `<head>`, `<body>`, `<script>`, `<style>`, `<link>`, `<iframe>`, no `on…=` attributes, no `style=` attributes. The app supplies all CSS and JS.

```html
<section class="unit" data-unit="sm-u1">
  <header class="unit-head">
    <p class="eyebrow">Strength of Materials · Unit 1</p>
    <h1>Simple Stresses and Strains</h1>
    <p class="lede">2–3 sentences: what this unit is about and why it matters.</p>
    <ul class="syl">  <!-- one <li> per syllabus topic, in syllabus words --></ul>
  </header>

  <section class="part" id="sm-u1-concepts" data-part="concepts">
    <h2>Concepts</h2>
    <!-- topics as <h3 id="sm-u1-c-<slug>">, explanations, figures, formula boxes, callouts, tables, flashcards -->
    <!-- end with a self-check quiz: -->
    <div class="quiz" id="sm-u1-quiz"> … 6–10 .mcq blocks … </div>
  </section>

  <section class="part" id="sm-u1-theory" data-part="theory">
    <h2>Theory questions</h2>
    <article class="q" id="sm-u1-q1" data-marks="10">
      <h3>Q1. Question text as asked</h3>
      <p class="q-src">MSE QB Q5 · Assignment A4 · Nov-Dec 2025 Q2(b)</p>
      <p class="q-hint">One line: what the examiner wants.</p>
      <details class="answer"><summary>Model answer</summary> … </details>
    </article>
  </section>

  <section class="part" id="sm-u1-numericals" data-part="numericals">
    <h2>Numericals</h2>
    <p class="method">Short method box: general steps for this type.</p>
    <article class="num" id="sm-u1-n1">
      <h3>N1. Problem statement (complete, with all data)</h3>
      <p class="q-src">Based on Jan 2025 Q1(b)</p>
      <figure class="fig">…optional SVG…</figure>
      <ol class="steps"><li>Step with formula…</li>…</ol>
      <p class="final">Answer: σ = 159.2 N/mm², δ = 0.25 mm</p>
    </article>
    <h3 id="sm-u1-practice">Practice problems</h3>
    <article class="num practice" id="sm-u1-p1"><h3>P1. …</h3><p class="final">Answer: …</p></article>
  </section>
</section>
```

Rules:
- Every `id` in the file starts with `<unit-id>-` and is unique.
- `q-src` names real sources: `MSE QB Q5`, `MT QB Q27`, `Assignment A3`, or an old paper like `Nov-Dec 2025 Q3(b)` / `Jan 2025` / `Nov 2024` / `Jun-Jul 2024` / `Aug-Sep 2023` / `Jan 2023 (CBCS)`. For MSE and MT, every QB and assignment number listed for your unit must appear in a `q-src` in exactly this form (`MSE QB Q12`, `MT QB Q7`, `Assignment A3`). Several numbers may share one question if they ask the same thing. If you write a question yourself, use `q-src` "Syllabus topic".
- Theory questions: for SoM and Thermal, take them from the old papers (syllabus topics only) and add syllabus topics they miss.
- Numericals: `ol.steps` — each `<li>` is one step the student writes in the exam (formula → substitution → result with unit). The app reveals steps one by one. `p.final` holds the boxed answer. Practice problems have only the statement and `p.final`.

## 6. Building blocks you may use (the app styles and animates these)

- Formula box: `<div class="formula">\[ \sigma = \frac{P}{A} \]<p class="where">where P = load (N), A = area (mm²)</p></div>`
- Maths: TeX for MathJax. Inline `\( … \)`, display `\[ … \]`. In HTML text escape `<` as `&lt;`, `>` as `&gt;`, `&` as `&amp;` (inside TeX too). Use `\text{}` for words in formulas.
- Callouts: `<aside class="note">`, `<aside class="tip">` (memory trick), `<aside class="warn">` (common mistake), `<aside class="exam">` (exam pattern / how marks are given), `<aside class="real">` (real-world example). Start each with `<b>Title.</b>`.
- Table: `<div class="tbl"><table><thead>…</thead><tbody>…</tbody></table></div>`
- Flashcards (key terms): `<dl class="cards"><dt>Term</dt><dd>Definition</dd>…</dl>` (6–12 cards per unit, inside Concepts).
- MCQ: `<div class="mcq" data-answer="b"><p class="stem">Question?</p><ol class="opts"><li>opt a</li><li>opt b</li><li>opt c</li><li>opt d</li></ol><p class="why">Why b is right.</p></div>` (answer letter a–d).
- Interactive widget: `<div class="widget" data-widget="NAME"></div>` — only the names listed for your unit in `units.json` `widgets` (the app implements them). Put each one once, in the matching concept section, with one sentence before it saying what to try. Widgets: `taper-bar` (extension of tapered bar calculator), `stress-strain` (mild-steel curve with labelled points), `beam-ss` (simply supported beam, point load + UDL → live SFD/BMD), `torsion` (solid/hollow shaft: T, d, L, G → τ, θ, power), `mohr` (σx, σy, τxy → Mohr's circle, principal stresses), `carnot` (T_H, T_L → efficiency, COP), `vcr` (h1–h4 → RE, work, COP, TR), `unit-cells` (SC/BCC/FCC/HCP → n, CN, a–r relation, APF), `lever-rule` (Fe–C tie line → phase fractions), `merchant` (Fc, Ft, α, t1, t2 → φ, μ, F, N, Fs).

## 7. Diagrams (inline SVG) — the most important part

Every sketch the exam may ask for must be a clear, labelled, exam-style line drawing that the student can copy. Typical unit: 8–15 figures.

```html
<figure class="fig" id="sm-u1-f-taper">
  <svg viewBox="0 0 640 260" role="img" aria-label="Tapered circular bar under axial load">
    <defs><marker id="sm-u1-arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="solid"/></marker></defs>
    <path d="…" class="ln"/>
    <line … class="ln thin" marker-end="url(#sm-u1-arw)"/>
    <text x="…" y="…" class="lbl">d₁</text>
  </svg>
  <figcaption>Fig. 1.3 — Tapered bar: diameter changes linearly from d₁ to d₂.</figcaption>
</figure>
```

- **No literal colours anywhere in SVG** (no `fill="#…"`, `stroke="red"`, `rgb(`, no `style=`). Use only these classes (the app colours them for light and dark themes): `ln` (main line, stroke), `thin`, `thick`, `dash` (dashed), `hid` (hidden/dash-dot centre line), `acc` (accent stroke), `acc2` (second accent stroke), `fill-soft`, `fill-acc`, `fill-acc2`, `fill-hatch` (section hatching — the app defines the pattern; use `class="fill-hatch"` on a closed shape), `solid` (filled with text colour, for arrowheads, dots), `lbl` (label text), `lbl-sm`, `lbl-b` (bold), `lbl-acc`. `fill="none"` and `stroke="none"` are allowed.
- Marker / pattern / gradient ids start with your unit id.
- viewBox width 560–720; text size is set by the classes (≈ 14 px at full width); keep labels ≥ 10 units from edges and from each other; never let text overlap lines.
- Graphs (stress–strain, S-N, creep, TTT, Fe–C, P-h, T-s, SFD/BMD): draw axes with arrowheads, label axes with quantity and unit, mark key points.
- **Check every SVG by rendering it**: save each SVG as a standalone file with a white background and a black `currentColor` substitute, then render it to PNG (e.g. `python3 -c "import pymupdf; d=pymupdf.open('f.svg'); d[0].get_pixmap(dpi=96).save('f.png')"`, or `rsvg-convert`/`qlmanage` if present) and LOOK at the PNG with your Read tool. Fix overlaps, clipped text and wrong geometry. Do this for every figure before you finish.

## 8. Real-world photos (Wikimedia Commons only)

The student approved downloading free-licence photos from Wikimedia Commons. Use 2–4 per unit where a photo helps (machines, test rigs, fracture surfaces, microstructures, real components, plants). Never a photo as a replacement for an exam sketch.

- Search with the Commons API, raster files only (jpg/png):
  `curl -s -A "UVCEExamNotes/1.0 (educational study notes)" "https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6&gsrlimit=10&gsrsearch=<terms>&prop=imageinfo&iiprop=url|extmetadata|mime&iiurlwidth=1000"`
  Use the same generic User-Agent for every request. Never put any personal detail in a request.
- Accept only these licences (extmetadata `LicenseShortName`): Public domain, CC0, CC BY (any version), CC BY-SA (any version). Reject everything else and anything without a licence.
- Download the **thumbnail** (`thumburl`, ≤ 1000 px wide) into `$SITE/_work/<unit-id>/dl/`, then re-encode with PIL into `$SITE/img/<unit-id>-<slug>.jpg`: RGB, max 1000 px wide, JPEG quality 80, ≤ 250 KB. Run Python with `-I`. Never execute or open downloaded files any other way.
- Open each final image with your Read tool and confirm it shows what your caption says. Discard it if not.
- Markup: `<figure class="photo"><img src="img/<file>" alt="what it shows" width="W" height="H" loading="lazy"><figcaption>Caption. <span class="credit">Photo: <Author> · <Licence> · Wikimedia Commons</span></figcaption></figure>` (W×H = real pixel size).
- Manifest entry: `{"file": "img/<file>", "commons_page": "https://commons.wikimedia.org/wiki/File:…", "author": "…", "license": "CC BY-SA 4.0", "license_url": "…", "caption": "…"}`. Strip HTML from the author field.

## 9. Numericals must be correct

- Recompute every solved numerical and every practice answer with Python (in `$SITE/_work/<unit-id>/`). Your final numbers must match the script to 3 significant figures. Keep the script.
- **Thermal property data:** do not use steam-table or refrigerant-table values from memory. Either (a) use values given in `$SITE/_src/internals/te-notes.html`, or (b) write the problem so the statement gives the needed enthalpies / entropies / specific volumes, or (c) if you must quote a table value, add `<aside class="warn"><b>Check.</b> Confirm this value in your steam tables.</aside>`.
- Use the unit system of the examiner (N, mm, N/mm², kN, kN·m, kJ/kg, K). State g = 9.81 m/s² where used.

## 10. Preview — never use the browser pane

The student watches the browser pane. **Never open anything in it** (no `file://`, no localhost, no Claude_Browser tools, no local web server). To see your unit as the student will see it, run:

`python3 $SITE/preview.py <unit-id>`

It converts every TeX formula to a rendered SVG (exactly what the build does), applies the app's CSS and writes `$SITE/_work/<unit-id>/preview/page-NN.png`. Look at the pages with your Read tool. Formulas that are not valid TeX make it print `TEXERR` — fix them. Never leave TeX commands outside `\( \)` / `\[ \]` (the lint fails on them): the student must never see raw code like `\frac{P}{A}`.

When the scanned paper loses a figure or a number, rebuild the problem and add `<aside class="note"><b>Data note.</b> …what you assumed…</aside>` (as the pilot unit did).

A finished example of the expected quality is `$SITE/content/sm-u1.html` (SoM Unit 1). Read part of it before you start, to match its structure, depth and figure style.

## 11. Before you finish

1. Run the lint: `python3 $SITE/lint.py <unit-id>` and fix every ERROR. Read the WARN lines and fix what is real.
2. Run `python3 $SITE/preview.py <unit-id>` and look at every page; confirm you looked at every SVG, formula and photo.
3. Report back in ≤ 15 lines: file sizes, counts (figures, photos, theory Qs, solved, practice, MCQs, cards), concept word count, anything you could not do, and any source question you skipped (with reason).
