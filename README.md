# Blossom 360

Two static pages for running 360 assessments across the roster — one profile per role.

- **`index.html`** — the rater form. Thirty-six behaviours, 1–5 plus "Not observed", three written questions.
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
- **Importance** is a role definition set by John and Bryan, not polled from raters. Nine of the thirty-six
  are "critical" — a deliberate budget, so the label means something.
- **Others** excludes the self-score, so nobody can lift their own result.
- **Blind spot** = self minus others. +1.00 or more means they rate themselves materially higher
  than the people around them do.
- Blank answers are ignored, never counted as zero.
- Ties on gap break by importance, then blind spot, then item order — identical in the web version and
  the Excel workbook. When several items tie at the fifth slot the console says so, because which one
  makes the cut is then a judgement call rather than a result.

## What is where

```
index.html          the rater form
console.html        the console for reading results
assets/data.js      GENERATED — never hand-edit
tools/              the Python that generates everything
  assessment_content.py   roster, rater matrix, scale, validation
  profiles/               one module per role
  build_assessment.py     writes the workbooks
  gen_data.py             writes assets/data.js
  build_importance_review.py  writes the review spreadsheet
  build_procedure_guide.py    writes the procedure guide PDF
workbooks/          GENERATED .xlsx per person — untracked, rebuild any time
```

The review spreadsheet and the procedure guide are written to
`blossom/Employees/DeveloperAssessment/` in iCloud rather than into the repo, since they get opened,
printed and marked up away from a checkout.

## Keeping it in step with the workbooks

`tools/assessment_content.py` is the single source of truth. Three scripts read it, and each runs
`validate()` first and refuses to write anything if it fails:

| Script | Writes | Run it from the repo root |
|---|---|---|
| `tools/gen_data.py` | `assets/data.js` (these pages) | `python3 tools/gen_data.py` |
| `tools/build_assessment.py` | `workbooks/*.xlsx` (one per person) | `python3 tools/build_assessment.py [Name ...]` |
| `tools/build_importance_review.py` | `ImportanceReview.xlsx` (for reviewing weights, metrics and the written questions) | `python3 tools/build_importance_review.py` |
| `tools/build_procedure_guide.py` | `ReviewProcedureGuide.pdf` (how to run a review) | `python3.14 tools/build_procedure_guide.py` |

The guide needs **python3.14** — the default `python3` here is 3.7, which cannot import reportlab 5.
It also registers Arial explicitly: reportlab 5 dropped the base-14 Type1 fonts, and a style asking
for Helvetica-Bold silently renders unbolded rather than erroring.

`build_importance_review.py` **overwrites its output in place**. Rename a marked-up copy before
rebuilding, or the notes in it are gone.

Edit the items, weights or metric library in `tools/profiles/` and run both. Do not hand-edit
`data.js` or the workbooks, or the spreadsheet and the web pages will drift apart.

The workbooks are build artefacts and are not tracked — `.gitignore` excludes `*.xlsx`, which also
means a workbook someone has filled in with real scores can never be committed by accident. Set
`B360_WORKBOOKS` to write them somewhere else:

```
B360_WORKBOOKS=~/Documents/360-workbooks python3 tools/build_assessment.py
```

## Bump `?v=` when the item set changes

`index.html` and `console.html` load their assets as `assets/data.js?v=3`. The version exists
because a browser holding a cached `data.js` would render one item set against a scorer expecting
another — a rater would fill in the wrong form and only find out when the console refused the code.

**Raise the number in both HTML files whenever `data.js` or `core.js` changes shape.** Wording fixes
do not need it; adding, removing or renumbering items does.

## The four lenses

Alongside the six dimensions, every behaviour is tagged with one of four lenses — the things John
looks for in anyone, whatever the seat:

| Lens | Asks |
|---|---|
| **Skill Set** | Can they actually do the job? |
| **Work Ethic** | Does the work land — finished, on the date given, to the standard? |
| **Attitude** | How do they take feedback, handle disagreement and treat the people around them? |
| **Durability & Improvement** | Does the fix hold, and does the standard rise? |

Dimensions ask *how is he doing at this part of the job*. Lenses ask *what kind of thing is going
wrong*, and they cut across the dimensions deliberately — continuous improvement shows up in the
feedback items as much as in the durability ones, and the tag is what catches that.

Each item carries **exactly one** lens, so the four scores are a partition of the thirty-six: nothing
counted twice, nothing left out. `validate()` enforces it. The tags live in `LENSES` at the bottom of
each profile module, and moving an item between lenses is a one-line edit and a rebuild.

The sixth dimension, **Durability & Improvement**, is the only place the fourth lens has a dedicated
home — the other three were already well covered by the original five dimensions. Its F1 is a
critical in every profile, which is why the budget is nine rather than eight.

## One assessment per role

Each role has its own **profile** — dimensions, behaviours, importance weights, metric library and
rater groups — as one module in `tools/profiles/`. Choosing who is being evaluated swaps the questions and
retitles both pages.

| Person | Role | Profile | Who rates them |
|---|---|---|---|
| Frans | Developer | `developer` | John, Bryan, Mark (managers) · Jeremy (peer) |
| Jeremy | Associate Developer | `developer-associate` | John, Bryan, Mark (managers) · Frans (peer) |
| Bryan | COO · Integrator | `coo-cfo-integrator` | John (manager) · Mark (peer) · Frans, Jeremy (reports) |
| John | Chief Vision Officer / CEO | `ceo-visionary` | Mark (peer) · Bryan, Frans, Jeremy (reports) |
| Mark | Chief Growth Officer | `cgo` | John, Bryan (peers) · Frans, Jeremy (reports) |

Everyone also rates themselves. Neither John nor Mark has a manager above them on the roster, so that
group does not appear on their forms — `coverage_warnings()` prints a note about each, so an empty
group is a decision you can see rather than a silent gap.

The two leadership profiles are built on the EOS Visionary and Integrator seats, since that is how
Blossom already runs.

**To add or change a role:** edit the module in `tools/profiles/`, list it in `_MODULES` and point the
person at it in `ROSTER` (both in `tools/assessment_content.py`), then run `tools/gen_data.py` (web)
and `tools/build_assessment.py` (spreadsheets). `validate()` runs first and fails the build on a
missing metric, an orphan item, a bad relationship, a rater matrix that disagrees with itself about
who reports to whom, a critical count that is not exactly nine, or an item that is missing a
lens or carries two.

Response codes carry the profile they were answered against. The console refuses a code whose profile
does not match the person's current one, so nobody can be scored against the wrong questions.

## Who rates whom

`RELATIONSHIP_MAP` in `tools/assessment_content.py` records what each rater is to each person. **The rater
is never asked** — the form derives the relationship from the matrix and shows it read-only. It is not
theirs to choose: a rater who is a peer one round and a report the next breaks the comparison, and
mis-filing themselves shifts the group averages.

A pair that is not in the matrix cannot be rated at all — the form says so and will not accept a
submission. That makes the matrix the definition of who rates whom, and keeps it under the
administrator's control rather than the rater's. Adding a pairing is one line in `RELATIONSHIP_MAP`
followed by a rebuild — and it must be added in both directions, since `validate()` rejects a matrix
where A calls B a manager but B does not call A a report.

## This is deliberately not anonymous

Every response carries the rater's name, and scores and comments are shared with the person being
rated. The form says so up front. That is Blossom's choice: candid feedback attached to a name,
rather than polite feedback from nobody.

## The spreadsheets are the fallback, not the primary

`workbooks/` holds a generated .xlsx per person, named for the role. Each one carries **one column per
named rater** — self, managers, peers and direct reports, in that order — taken from
`RELATIONSHIP_MAP`, so every seat gets exactly the raters it actually has rather than a fixed grid of
"Peer 1…Peer 4". Group averages, the radar chart and the blind-spot ranking all size themselves to
that column set.

The workbooks compute the same numbers as the console, by the same tie-break rules, and are the
offline route when the web pages are inconvenient.
