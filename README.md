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

## One assessment per role

Each role has its own **profile** — dimensions, behaviours, importance weights, metric library and
rater groups — as one module in `profiles/`. Choosing who is being evaluated swaps the questions and
retitles both pages.

| Person | Role | Profile | Raters |
|---|---|---|---|
| Frans | Developer | `developer` | self · manager · peer |
| Jeremy | Associate Developer | `developer-associate` | self · manager · peer |
| Bryan | COO / CFO · Integrator | `coo-cfo-integrator` | self · manager · peer · direct report |
| John | Chief Vision Officer / CEO | `ceo-visionary` | self · manager · peer · direct report |
| Mark | Chief Growth Officer | `cgo` | self · manager · peer · direct report |

The two leadership profiles are built on the EOS Visionary and Integrator seats, since that is how
Blossom already runs.

**To add or change a role:** edit the module in `profiles/`, list it in `_MODULES` and point the person
at it in `ROSTER` (both in `assessment_content.py`), then run `gen_data.py` (web) and
`build_assessment.py` (spreadsheet). `validate()` runs before `data.js` is written and fails the build
on a missing metric, an orphan item, a bad relationship, or a critical count that is not exactly eight.

Response codes carry the profile they were answered against. The console refuses a code whose profile
does not match the person's current one, so nobody can be scored against the wrong questions.

## Who rates whom

`RELATIONSHIP_MAP` in `assessment_content.py` records what each rater is to each person. The form
fills the relationship in from it so a rater does not drift between groups from one round to the
next — which would break the comparison — and the console flags in amber any response whose declared
relationship differs from the expected one. Pairs left out of the map are chosen by hand on the form.

## This is deliberately not anonymous

Every response carries the rater's name, and scores and comments are shared with the person being
rated. The form says so up front. That is Blossom's choice: candid feedback attached to a name,
rather than polite feedback from nobody.

## The spreadsheets are the fallback, not the primary

`workbooks/` holds a generated .xlsx per role. They support **self, manager and peer only** — there are
no direct-report columns, so the three leadership roles must be read in the web console. The workbook
remains useful offline and for the individual-contributor roles.
