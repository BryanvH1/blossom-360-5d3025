# Developer 360 — Blossom

Two static pages for running a 360 assessment on a developer moving toward lead developer.

- **`index.html`** — the rater form. Thirty behaviours, 1–5 plus "Not observed", three written questions.
  On submit it produces a short response code the rater sends back. Nothing is transmitted anywhere.
- **`console.html`** — the console for John and Bryan. Paste the codes in; it computes the scores,
  results, development plan, metric library and progression.

## No assessment data lives in this repository

The pages are the tool, not the data. Responses exist only in the browser that pasted them
(`localStorage`), so nobody's assessment is ever published to a URL. Use **Export backup** in the
console to keep a copy, and **Import backup** to restore it or move it to another machine.

Because the data is per-browser, John and Bryan each hold their own copy — share the export file
between you rather than expecting the console to sync.

## How the maths works

- `Gap = Importance × (5 − Others' average)`. The five highest gaps become the development plan.
- **Importance** is a role definition set by John and Bryan, not polled from raters. Eight of the thirty
  are "critical" — a deliberate budget, so the label means something.
- **Others** excludes the self-score, so nobody can lift their own result.
- **Blind spot** = self minus others. +1.00 or more means they rate themselves materially higher
  than the people around them do.
- Blank answers are ignored, never counted as zero.
- Ties on gap break by importance, then blind spot, then item order — identical in the web version and
  the Excel workbook. When several items tie at the fifth slot the console says so, because which one
  makes the cut is then a judgement call rather than a result.

## Keeping it in step with the workbook

`assets/data.js` is **generated** from `build_assessment.py` (the script that builds
`Developer_360_Assessment_v1.xlsx`). Edit the items, weights or metric library there and regenerate —
do not hand-edit `data.js`, or the spreadsheet and the web pages will drift apart.

## Note on scope

The thirty behaviours and their weights describe a **software developer becoming a lead developer**.
The roster dropdown lists the whole team for convenience, but pointing this instrument at a
non-developer would produce numbers that look objective and mean very little. Other roles need their
own item set first.
