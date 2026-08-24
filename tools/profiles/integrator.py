# -*- coding: utf-8 -*-
"""COO · Integrator. Bryan.

Built around the EOS Integrator seat: LMA, removing obstacles, holding the plan
together and being the filter and truth-teller for the Visionary. The E dimension
is the Visionary–Integrator pairing itself, which is where this seat succeeds or
fails regardless of how well the rest is done.
"""

META = {
    "id": "coo-cfo-integrator",
    "label": "COO · Integrator",
    "formTitle": "COO · Integrator 360 — Rater Form",
    "consoleTitle": "COO · Integrator 360 — Console",
    "blurb": "Thirty-six observable behaviours · about ten minutes",
    "note": ("Built around the EOS Integrator seat. The criticals sit on accountability, removing "
             "obstacles, a forecast people can plan against, and the honesty of the partnership "
             "with the Visionary."),
    "relationships": ["self", "manager", "peer", "report"],
}

DIMENSIONS = [
    ("A", "Execution & Accountability", "Does the plan actually happen?"),
    ("B", "Financial Stewardship",      "Do we know our numbers, and act on them?"),
    ("C", "Leading the Team",           "Are people clear, capable and held to it?"),
    ("D", "Operating Rhythm",           "Does the business run on a system rather than heroics?"),
    ("E", "Partnership with the Visionary", "Does the Visionary–Integrator pair actually work?"),
    ("F", "Durability & Improvement",
     "Does the fix hold, and does the business get easier to run?"),
]

ITEMS = [
 ("A1", "Turns the quarterly plan into owned, dated commitments", 2),
 ("A2", "Holds people to what they signed up for, kindly and consistently", 3),
 ("A3", "Removes the obstacle rather than escalating it", 3),
 ("A4", "Closes out the quarter honestly — what hit, what didn't, why", 2),
 ("A5", "Says no, or not now, to work that isn't the priority", 2),
 ("A6", "Meets his own commitments to the standard he expects of others", 2),

 ("B1", "Knows the numbers well enough to answer without preparing", 2),
 ("B2", "Gives leadership a forecast they can plan against", 3),
 ("B3", "Flags a cash or margin problem early", 3),
 ("B4", "Ties spending decisions back to the plan", 2),
 ("B5", "Keeps the books and reporting current enough to be useful", 1),
 ("B6", "Explains the financial picture so non-finance people can decide", 2),

 ("C1", "Makes sure everyone knows what they own", 2),
 ("C2", "Has the hard conversation when performance slips", 3),
 ("C3", "Develops the people who report to him", 2),
 ("C4", "Resolves friction between people rather than letting it sit", 2),
 ("C5", "Listens well enough that people bring him problems early", 2),
 ("C6", "Puts people in seats that actually fit them", 1),

 ("D1", "Runs meetings worth the time they take", 2),
 ("D2", "Keeps a consistent cadence rather than reacting week to week", 2),
 ("D3", "Documents how things work so the company doesn't depend on memory", 2),
 ("D4", "Measures the handful of things that actually indicate health", 2),
 ("D5", "Simplifies process that has stopped earning its keep", 1),
 ("D6", "Pushes decisions to the level closest to the work", 1),

 ("E1", "Filters and sequences the Visionary's ideas without killing momentum", 3),
 ("E2", "Disagrees privately and commits publicly", 2),
 ("E3", "Translates vision into something the team can execute", 2),
 ("E4", "Tells John what he needs to hear, not what is comfortable", 3),
 ("E5", "Keeps the leadership team aligned behind one plan", 3),
 ("E6", "Protects the organisation from whiplash without blocking change", 2),

 ("F1","Fixes the process that caused the problem, not just this instance",3),
 ("F2","Chooses the sustainable fix over the quick patch, and says which he is choosing",2),
 ("F3","Builds the business so it runs without him in the room",2),
 ("F4","Protects next year's capacity while still hitting this quarter's plan",2),
 ("F5","Follows up to confirm a fix actually held",1),
 ("F6","Raises the standard the business is held to over time",2),
]

METRICS = {
 "A1": ("% of quarterly Rocks with a single named owner and a due date at kickoff", "100%", "ClickUp / EOS Rocks list", "Quarterly"),
 "A2": ("Missed commitments where the conversation happened within a week", "100%", "Manual tally", "Monthly"),
 "A3": ("Median days from an obstacle being raised to being cleared", "≤ 5 business days", "Manual — obstacle log / IDS list", "Monthly"),
 "A4": ("Quarter-close reviews naming what missed and why", "100%", "Manual — written quarterly review", "Quarterly"),
 "A5": ("Non-priority requests accepted into the quarter after it started", "≤ 2", "Manual tally", "Quarterly"),
 "A6": ("His own commitments met by the date given", "≥ 95%", "Manual — commitment log", "Monthly"),

 "B1": ("Spot checks on cash, runway, margin and AR answered correctly unprepared", "≥ 90%", "Manual — John spot checks", "Quarterly"),
 "B2": ("Forecast vs. actual on cash and revenue", "Within ±10%", "Finance", "Monthly"),
 "B3": ("Cash or margin problems flagged ≥60 days before they would bite", "100%", "Manual review", "Quarterly"),
 "B4": ("Spend approved without a stated link to the plan", "0", "Manual — approval log", "Monthly"),
 "B5": ("Days after month end that the books are closed and reported", "≤ 10", "Finance calendar", "Monthly"),
 "B6": ("Leadership rate 1–5: \"I understood the numbers well enough to decide\"", "Average ≥ 4.0", "Manual — one rating per review", "Monthly"),

 "C1": ("Team members who can state what they own unprompted", "100%", "Manual — ask each quarter", "Quarterly"),
 "C2": ("Performance issues still unaddressed 30 days after being recognised", "0", "Manual — people review", "Monthly"),
 "C3": ("Documented development conversations with each report", "≥ 1 per month each", "Manual log", "Monthly"),
 "C4": ("Unresolved interpersonal issues carried more than one quarter", "0", "Manual — IDS list review", "Quarterly"),
 "C5": ("Problems that reached him early vs. after they became urgent", "≥ 3:1", "Manual tally", "Quarterly"),
 "C6": ("Role changes in the last year that improved fit", "Net positive", "Manual review", "Annually"),

 "D1": ("Attendees rate each recurring meeting 1–5 on worth the time", "Average ≥ 4.0", "Manual — rating at close of meeting", "Monthly"),
 "D2": ("Scheduled leadership meetings held as planned", "≥ 90%", "Calendar review", "Quarterly"),
 "D3": ("Core processes with a current written description", "100% of the top 10", "Manual checklist", "Quarterly"),
 "D4": ("Scorecard measures reviewed weekly and acted on when off-track", "100%", "EOS scorecard", "Weekly"),
 "D5": ("Process steps removed or simplified", "≥ 1 per quarter", "Manual tally", "Quarterly"),
 "D6": ("Decisions escalated to him that the owner could have made", "≤ 2 per month", "Manual tally", "Monthly"),

 "E1": ("Visionary ideas triaged with a stated yes / not now / no within a week", "100%", "Manual — idea log", "Monthly"),
 "E2": ("Occasions he undercut a decision publicly after agreeing to it", "0", "Manual tally", "Quarterly"),
 "E3": ("Team can state how the current quarter connects to the vision", "≥ 80% of staff", "Manual — ask each quarter", "Quarterly"),
 "E4": ("Uncomfortable truths raised with John, logged at the time", "≥ 1 per month", "Manual log", "Monthly"),
 "E5": ("Leadership team giving the same answer on the current priorities", "100%", "Manual — ask each separately", "Quarterly"),
 "E6": ("Direction changes absorbed without a mid-quarter replan", "≥ 80%", "Manual tally", "Quarterly"),

 "F1":("Issues raised in IDS that had already been raised in a previous quarter","0","EOS issues list","Quarterly"),
 "F2":("Patches applied without a stated plan to make them permanent","0","Manual tally","Monthly"),
 "F3":("Weeks the business ran to plan while he was away","100% of weeks away","Manual review","Annually"),
 "F4":("Quarters where next-year capacity was cut to make the current number","0","Manual review","Quarterly"),
 "F5":("Fixes revisited 60 days later to confirm they held","≥ 80%","Manual — fix log","Monthly"),
 "F6":("Scorecard measures whose target was raised in the last year","≥ 3","EOS scorecard","Annually"),
}


# Which of John's four lenses each item answers to. Exactly one lens per item,
# so the four scores partition the thirty-six — nothing counted twice, nothing
# left out. Dimensions ask how he is doing at a part of the job; lenses ask what
# kind of thing is going wrong, and they deliberately cut across each other.
LENSES = {
 "skill":       ["B1", "B2", "B4", "B5", "B6", "C6", "D1", "D4", "E1", "E3", "E5"],
 "ethic":       ["A1", "A2", "A3", "A4", "A6", "C1", "D2"],
 "attitude":    ["A5", "B3", "C2", "C4", "C5", "E2", "E4"],
 "durability":  ["C3", "D3", "D5", "D6", "E6", "F1", "F2", "F3", "F4", "F5", "F6"],
}
