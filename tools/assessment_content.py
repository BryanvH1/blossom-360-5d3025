# -*- coding: utf-8 -*-
"""
Single source of truth for the Blossom 360 assessments.

Each role is one module in profiles/ exporting META, DIMENSIONS, ITEMS and METRICS.
The spreadsheet builder (build_assessment.py) and the web pages (gen_data.py ->
assets/data.js) both read from here, so a change made once reaches all three.

To add a role:
  1. Copy a file in profiles/, rewrite META / DIMENSIONS / ITEMS / METRICS for that job.
  2. Add it to _MODULES below and point the person at it in ROSTER.
  3. Run gen_data.py (web) and build_assessment.py (spreadsheet).

Importance is 1 helpful / 2 important / 3 critical and describes what the ROLE needs.
It is a role definition set by the managers, not something raters vote on. Exactly
eight criticals per profile — the scarcity is the point; validate() enforces it.
"""

import os, sys
sys.dont_write_bytecode = True          # no stray __pycache__ in the repo
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles"))

import developer, developer_associate, cgo, ceo_visionary, integrator

_MODULES = [developer, developer_associate, cgo, ceo_visionary, integrator]

# ---------------------------------------------------------------- shared bits
# (value, short name, what it looks like)
SCALE = [
 ("5", "Exceptional",
       "Among the best you've seen at this, anywhere — not just at Blossom. You'd point a new hire "
       "at them to learn how it's done. Should be rare."),
 ("4", "Strong",
       "Consistently does this well. You don't think about it and you don't check up on it. "
       "A genuinely good score."),
 ("3", "Solid — meets the bar",
       "Does this reliably; occasionally needs a nudge or a reminder. This is the expected score, "
       "not a criticism. It means they are doing the job."),
 ("2", "Developing",
       "Inconsistent. Happens when prompted, or when things are calm, but you can't count on it "
       "under pressure. Not failing — just not yet reliable."),
 ("1", "Significant development needed",
       "Doesn't happen, or happens so rarely that other people work around it. Something has to "
       "change here."),
 ("", "Not observed",
      "You haven't seen enough to judge. Always better than a guess — blanks are ignored in the "
      "maths, guesses aren't."),
]

# Shown next to the scale. These are what stop the scores turning to mush.
SCALE_NOTES = [
 ("The bar is this role's bar.",
  "A 4 for an Associate Developer means \u201cstrong for an Associate Developer\u201d, not "
  "\u201cas good as a lead\u201d. The same behaviour scored across two roles does not mean the "
  "same absolute thing."),
 ("Most scores should be 3s and 4s.",
  "If you are handing out mostly 4s and 5s, you are probably rating how much you enjoy working "
  "with the person rather than the specific behaviour in front of you. 5s should be rare, and a 1 "
  "should mean something is genuinely wrong."),
]

OPEN_QS = [
 "1. What are they genuinely good at — what should not change?",
 "2. If they changed ONE thing, what would make the biggest difference?",
 "3. What would you need to see to be fully confident in them in this role?",
]

RELATIONSHIPS = [
    ("self",    "Self"),
    ("manager", "Manager"),
    ("peer",    "Peer"),
    ("report",  "Direct report"),
]

# ---------------------------------------------------------------- John's four lenses
# A second, coarser way of reading the same items. Every item belongs to exactly one
# lens, so the four lens scores are a partition of the thirty-six — nothing double
# counted, nothing left out. Dimensions answer "how is he doing at this part of the
# job"; lenses answer "what kind of thing is going wrong". They cut across each other
# on purpose: continuous improvement shows up in the feedback items as much as in the
# durability ones, and the lens tag is what catches that.
LENS_DEFS = [
 ("skill",      "Skill Set",
                "Can they actually do the job?"),
 ("ethic",      "Work Ethic",
                "Does the work land — finished, on the date given, to the standard?"),
 ("attitude",   "Attitude",
                "How do they take feedback, handle disagreement and treat the people around them?"),
 ("durability", "Durability & Improvement",
                "Does the fix hold, and does the standard rise?"),
]
LENS_KEYS = [k for k, _, _ in LENS_DEFS]

CRITICAL_BUDGET = 9

# What the mirror image of a relationship must be. If A says B is their manager,
# then B's entry for A must say "report" — otherwise the two forms disagree about
# the org chart and the group averages are computed off different structures.
INVERSE_RELATIONSHIP = {"manager": "report", "report": "manager", "peer": "peer"}

# ---------------------------------------------------------------- assembly
def _build(mod):
    p = dict(mod.META)
    p["dimensions"] = mod.DIMENSIONS
    p["items"] = mod.ITEMS
    p["metrics"] = mod.METRICS
    p["lenses"] = mod.LENSES
    p["scale"] = SCALE
    p["openQuestions"] = getattr(mod, "OPEN_QS", OPEN_QS)
    p.setdefault("relationships", ["self", "manager", "peer"])
    return p

PROFILES = {m.META["id"]: _build(m) for m in _MODULES}

# ---------------------------------------------------------------- who gets assessed
# "profile": None means no assessment has been defined for that role yet. The pages
# say so plainly rather than falling back to another role's questions.
ROSTER = [
    {"name": "Frans",  "role": "Developer",            "profile": "developer"},
    {"name": "Jeremy", "role": "Associate Developer",  "profile": "developer-associate"},
    {"name": "Bryan",  "role": "COO · Integrator",      "profile": "coo-cfo-integrator"},
    {"name": "John",   "role": "Chief Vision Officer / CEO", "profile": "ceo-visionary"},
    {"name": "Mark",   "role": "Chief Growth Officer", "profile": "cgo"},
]


def profile_for(name):
    """Return the profile dict for a person, or None if none is defined."""
    for p in ROSTER:
        if p["name"] == name:
            return PROFILES.get(p["profile"]) if p["profile"] else None
    return None


def validate():
    """Fail loudly on the mistakes that are easy to make and hard to notice."""
    problems = []
    valid_rel = {k for k, _ in RELATIONSHIPS}
    for pid, p in PROFILES.items():
        codes = [c for c, _, _ in p["items"]]
        dims = {d[0] for d in p["dimensions"]}
        if len(codes) != len(set(codes)):
            problems.append(f"{pid}: duplicate item codes")
        for c in codes:
            if c[0] not in dims:
                problems.append(f"{pid}: item {c} has no matching dimension")
            if c not in p["metrics"]:
                problems.append(f"{pid}: item {c} has no metric")
        for c in p["metrics"]:
            if c not in codes:
                problems.append(f"{pid}: metric {c} has no matching item")
        for c, t, i in p["items"]:
            if i not in (1, 2, 3):
                problems.append(f"{pid}: item {c} has importance {i}, must be 1-3")
        lensed = {}
        for lens, codes_in in p["lenses"].items():
            if lens not in LENS_KEYS:
                problems.append(f"{pid}: unknown lens '{lens}'")
            for c in codes_in:
                if c in lensed:
                    problems.append(f"{pid}: item {c} is tagged to both "
                                    f"'{lensed[c]}' and '{lens}' — each item gets exactly one lens")
                lensed[c] = lens
                if c not in codes:
                    problems.append(f"{pid}: lens '{lens}' lists {c}, which is not an item")
        for c in codes:
            if c not in lensed:
                problems.append(f"{pid}: item {c} has no lens")

        n_crit = sum(1 for _, _, i in p["items"] if i == 3)
        if n_crit != CRITICAL_BUDGET:
            problems.append(f"{pid}: {n_crit} criticals, budget is {CRITICAL_BUDGET}")
        for r in p["relationships"]:
            if r not in valid_rel:
                problems.append(f"{pid}: unknown relationship '{r}'")
        if "self" not in p["relationships"]:
            problems.append(f"{pid}: must include 'self' — the blind-spot column depends on it")
        for k in ("label", "formTitle", "consoleTitle"):
            if not p.get(k):
                problems.append(f"{pid}: missing {k}")
    names = {r["name"] for r in ROSTER}
    for evaluee, raters in RELATIONSHIP_MAP.items():
        if evaluee not in names:
            problems.append(f"relationship map: unknown person '{evaluee}'")
            continue
        prof = profile_for(evaluee)
        for rater, rel in raters.items():
            if rater not in names:
                problems.append(f"relationship map: {evaluee} <- unknown rater '{rater}'")
            if rel not in valid_rel:
                problems.append(f"relationship map: {evaluee}/{rater} has unknown relationship '{rel}'")
            elif prof and rel not in prof["relationships"]:
                problems.append(f"relationship map: {evaluee}/{rater} is '{rel}', "
                                f"but the {prof['label']} form does not offer that group")
            if rater == evaluee:
                problems.append(f"relationship map: {evaluee} lists themselves as a rater")
            # If the pair is mapped in both directions the two entries must be mirrors.
            back = RELATIONSHIP_MAP.get(rater, {}).get(evaluee)
            want = INVERSE_RELATIONSHIP.get(rel)
            if back and want and back != want:
                problems.append(
                    f"relationship map: {evaluee} says {rater} is a '{rel}', so {rater} "
                    f"must say {evaluee} is a '{want}' — it says '{back}'")

    seen = set()
    for r in ROSTER:
        if r["name"] in seen:
            problems.append(f"roster: duplicate name {r['name']}")
        seen.add(r["name"])
        if r["profile"] and r["profile"] not in PROFILES:
            problems.append(f"roster: {r['name']} points at unknown profile '{r['profile']}'")
    return problems


# ---------------------------------------------------------------- who rates whom
# Keyed by the person being evaluated, then by the rater: what that rater is TO them.
# The form fills the relationship in from this so it stays consistent between rounds —
# a rater who is a "peer" one round and a "report" the next breaks the trend line.
# A pair that is not listed here cannot be rated at all — the form refuses the
# submission — so this matrix, not the rater, is the definition of who rates whom.
RELATIONSHIP_MAP = {
    "John":   {"Bryan": "report",  "Mark": "peer",      "Frans": "report", "Jeremy": "report"},
    "Bryan":  {"John":  "manager", "Mark": "peer",      "Frans": "report", "Jeremy": "report"},
    "Mark":   {"John":  "peer",    "Bryan": "peer",     "Frans": "report", "Jeremy": "report"},
    "Frans":  {"John":  "manager", "Bryan": "manager",  "Mark": "manager", "Jeremy": "peer"},
    "Jeremy": {"John":  "manager", "Bryan": "manager",  "Mark": "manager", "Frans": "peer"},
}


def coverage_warnings():
    """Advisory, never fatal: places where the matrix is thinner than the profile expects.

    A rater group a profile offers but nobody fills is a blank column in the console
    and no column at all in the workbook. That is usually a real org fact (the CEO has
    no manager) rather than a mistake, so it is a note to read, not a build failure.
    """
    notes = []
    for r in ROSTER:
        prof = PROFILES.get(r["profile"]) if r["profile"] else None
        if not prof:
            notes.append(f"{r['name']}: no profile defined — cannot be assessed")
            continue
        mapped = RELATIONSHIP_MAP.get(r["name"], {})
        filled = {"self"} | set(mapped.values())
        empty = [g for g in prof["relationships"] if g not in filled]
        if empty:
            notes.append(f"{r['name']} ({prof['label']}): offers {'/'.join(empty)} "
                         f"but no rater is mapped to it")
        if len(mapped) < 2:
            notes.append(f"{r['name']}: only {len(mapped)} rater besides self — "
                         f"the averages will be thin and effectively attributable")
    return notes


def expected_relationship(evaluee, rater):
    """What `rater` is to `evaluee`, or None if the pair is not mapped."""
    if evaluee == rater:
        return "self"
    return RELATIONSHIP_MAP.get(evaluee, {}).get(rater)


if __name__ == "__main__":
    errs = validate()
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print("  -", e)
        raise SystemExit(1)
    print(f"{len(PROFILES)} profiles OK")
    for w in coverage_warnings():
        print("  note:", w)
    for pid, p in PROFILES.items():
        crit = [c for c, _, i in p["items"] if i == 3]
        split = " ".join(f"{k}:{len(p['lenses'].get(k, []))}" for k in LENS_KEYS)
        print(f"  {pid:22s} {len(p['items'])} items · criticals {','.join(crit)} · {split}")
    print("roster:")
    for r in ROSTER:
        print(f"  {r['name']:8s} {r['role']:34s} -> {r['profile']}")
