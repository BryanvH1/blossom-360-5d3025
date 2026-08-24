# Blossom 360

Two static pages for running 360 assessments across the roster — one profile per role.

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
workbooks/          GENERATED .xlsx per person — untracked, rebuild any time
```

## Keeping it in step with the workbooks

`tools/assessment_content.py` is the single source of truth. Two scripts read it, and both run
`validate()` first and refuse to write anything if it fails:

| Script | Writes | Run it from the repo root |
|---|---|---|
| `tools/gen_data.py` | `assets/data.js` (these pages) | `python3 tools/gen_data.py` |
| `tools/build_assessment.py` | `workbooks/*.xlsx` (one per person) | `python3 tools/build_assessment.py [Name ...]` |

Edit the items, weights or metric library in `tools/profiles/` and run both. Do not hand-edit
`data.js` or the workbooks, or the spreadsheet and the web pages will drift apart.

The workbooks are build artefacts and are not tracked — `.gitignore` excludes `*.xlsx`, which also
means a workbook someone has filled in with real scores can never be committed by accident. Set
`B360_WORKBOOKS` to write them somewhere else:

```
B360_WORKBOOKS=~/Documents/360-workbooks python3 tools/build_assessment.py
```

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
who reports to whom, or a critical count that is not exactly eight.

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
