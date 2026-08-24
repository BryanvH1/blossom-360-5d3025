# -*- coding: utf-8 -*-
"""Associate Developer — establishing competence, not yet leading. Jeremy.

Shares most behaviours with the Developer profile, because they are simply what good
development work looks like. What differs is the WEIGHTING and the E dimension: an
associate is not accountable for mentoring or for the handover of whole systems, and
the behaviours that decide whether they grow — asking early, applying feedback the
next time — carry far more weight than they do for someone on the lead track.
"""

META = {
    "id": "developer-associate",
    "label": "Associate Developer",
    "formTitle": "Associate Developer 360 — Rater Form",
    "consoleTitle": "Associate Developer 360 — Console",
    "blurb": "Thirty-six observable behaviours · about ten minutes",
    "note": ("Weighted for someone establishing competence, not for someone moving into a lead role. "
             "The criticals are about learning speed and not going quiet, rather than mentoring or handover."),
    "relationships": ["self", "manager", "peer"],
}

DIMENSIONS = [
    ("A", "Delivery & Predictability", "Can the team plan around them?"),
    ("B", "Code & Technical Craft",    "Is the work durable, or does it come back?"),
    ("C", "Communication & Transparency", "Do people know where things stand without chasing them?"),
    ("D", "Collaboration & Coachability", "Does feedback actually change anything?"),
    ("E", "Ownership & Growth",       "Are they getting better, and do they own their work?"),
    ("F", "Durability & Improvement",
     "Does the fix hold, and are they getting better?"),
]

ITEMS = [
 ("A1", "Gives estimates that turn out to be close to reality", 2),
 ("A2", "Finishes what they start before picking up new work", 2),
 ("A3", "Raises a delay or blocker early, before the date is missed", 3),
 ("A4", "Breaks large work into pieces that can be shipped and reviewed", 2),
 ("A5", "Delivers work that is genuinely done — tested, not \"done except…\"", 3),
 ("A6", "Negotiates scope changes openly rather than absorbing them silently", 1),

 ("B1", "Writes code others can read and change without asking them", 3),
 ("B2", "Tests their own work before handing it off", 3),
 ("B3", "Chooses the simple solution when the simple solution is enough", 2),
 ("B4", "Names and logs technical debt rather than hiding it", 1),
 ("B5", "Diagnoses problems methodically rather than changing things at random", 2),
 ("B6", "Leaves enough of a trail that someone else could pick the work up", 2),

 ("C1", "Provides status without being asked for it", 2),
 ("C2", "Writes down what they learned so the next person does not relearn it", 2),
 ("C3", "Explains technical trade-offs so a non-developer can make the call", 1),
 ("C4", "Acknowledges messages and requests within an agreed time", 2),
 ("C5", "Says \"I'm stuck\" instead of going quiet", 3),
 ("C6", "Delivers bad news early and plainly", 2),

 ("D1", "Receives critical feedback without becoming defensive", 2),
 ("D2", "Acts on feedback — the same issue doesn't need raising twice", 3),
 ("D3", "Asks for help before burning significant time", 3),
 ("D4", "Executes a decision fully even when they argued against it", 2),
 ("D5", "Shares what they know instead of holding it", 2),
 ("D6", "Keeps disagreements about the work, not the person", 1),

 ("E1", "Owns the outcome, not the ticket — follows through to working in production", 2),
 ("E2", "Thinks past their own task to what the product and customer need", 2),
 ("E3", "Applies review feedback the next time, not only this time", 3),
 ("E4", "Comes away understanding why something worked, not just that it did", 2),
 ("E5", "Flags something that looks wrong even when it isn't theirs to fix", 2),
 ("E6", "Given an ambiguous problem, comes back with the questions that sharpen it", 2),

 ("F1","Fixes the cause, not just the thing in front of them",3),
 ("F2","Asks why it broke, not only how to make it work again",2),
 ("F3","Says when they have taken a shortcut rather than leaving it to be found",2),
 ("F4","Goes back and tidies work they know was rushed",2),
 ("F5","Suggests a better way of doing something they were shown",1),
 ("F6","Is measurably more capable than three months ago",2),
]

METRICS = {
 "A1": ("% of tasks finished within ±50% of the estimate given", "≥ 50%, rising", "Manual tally / Linear estimate vs. actual", "Monthly"),
 "A2": ("Peak number of items in progress at one time during the week", "≤ 2", "Manual tally / Linear board snapshot", "Weekly"),
 "A3": ("% of missed dates where a heads-up came ≥1 day BEFORE the date", "100%", "Manual tally (whoever assigned the work logs it)", "Monthly"),
 "A4": ("% of tasks closed within 5 working days of being started", "≥ 70%", "Manual tally / Linear cycle time", "Monthly"),
 "A5": ("Items reopened or bounced back after being called done", "≤ 2 per month", "Manual tally", "Monthly"),
 "A6": ("Scope changes discovered after the fact rather than agreed up front", "0", "Manual tally", "Monthly"),

 "B1": ("Review comments asking what the code does or why", "Trend down 40% in 90 days", "Manual tally / GitHub review comments", "Monthly"),
 "B2": ("Defects the reviewer finds that a self-test would have caught", "≤ 1 per week", "Manual tally at review", "Weekly"),
 "B3": ("Times a reviewer flags a solution as more complex than the problem needs", "≤ 2 per month", "Manual tally / review notes", "Monthly"),
 "B4": ("Shortcuts they flagged themselves vs. ones the reviewer found", "≥ 1:1", "Manual tally", "Monthly"),
 "B5": ("Bugs where the fix addressed the cause rather than the symptom", "≥ 80%", "Manual tally at review", "Monthly"),
 "B6": ("% of finished tasks with a note explaining what changed and why", "≥ 90%", "Manual checklist / PR description", "Monthly"),

 "C1": ("% of weekdays with a short written update posted unprompted", "≥ 90%", "Manual tally", "Weekly"),
 "C2": ("Notes or docs written from something newly learned", "≥ 2 per month", "Manual tally", "Monthly"),
 "C3": ("Explanations a non-developer rated 1–5 as \"I understood the trade-off\"", "Average ≥ 3.5", "Manual — one rating per explanation", "Monthly"),
 "C4": ("% of requests acknowledged within 1 business day", "≥ 90%", "Manual tally / spot check", "Monthly"),
 "C5": ("Stretches of more than half a day stuck with no one told", "0", "Self-logged + confirmed at standup", "Weekly"),
 "C6": ("Problems leadership learned about only after the deadline", "0", "Manual tally", "Monthly"),

 "D1": ("% of feedback conversations the giver rates as \"received openly\"", "≥ 90%", "Manual — giver logs it same day", "Per conversation"),
 "D2": ("Pieces of feedback that had to be raised a second time", "0 per quarter", "Manual tally (keep a feedback log)", "Monthly"),
 "D3": ("Tasks where more than 4 hours were lost before asking for help", "0", "Self-logged time-to-ask", "Weekly"),
 "D4": ("Closed decisions reopened or relitigated", "0", "Manual tally", "Monthly"),
 "D5": ("Times they answered someone else's question rather than deflecting it", "≥ 4 per month", "Manual tally", "Monthly"),
 "D6": ("Disagreements that had to be escalated", "0", "Manual tally", "Monthly"),

 "E1": ("% of their items that reach production without someone else finishing them", "≥ 85%", "Manual tally", "Monthly"),
 "E2": ("Questions asked about the customer or product before starting a task", "≥ 2 per month", "Manual tally", "Monthly"),
 "E3": ("Repeat review comments — the same correction given twice", "0 per month", "Manual tally / GitHub review comments", "Monthly"),
 "E4": ("Can explain a past fix a month later without looking it up", "≥ 80% of spot checks", "Manual — ask at the monthly check-in", "Monthly"),
 "E5": ("Problems raised that were outside their assigned work", "≥ 1 per month", "Manual tally", "Monthly"),
 "E6": ("Ambiguous tasks where they returned clarifying questions before building", "100%", "Manual tally", "Per occurrence"),

 "F1":("Issues they closed that had to be reopened for the same cause","0","Linear / manual tally","Monthly"),
 "F2":("Fixes where they can explain the cause, not just the change","≥ 90%","Manual — ask at review","Monthly"),
 "F3":("Shortcuts they flagged themselves vs. ones found in review","≥ 2:1","Manual tally","Monthly"),
 "F4":("Rushed work returned to and cleaned up within the next sprint","≥ 80%","Manual tally","Monthly"),
 "F5":("Suggested improvements to an existing way of working","≥ 1 per quarter","Manual tally","Quarterly"),
 "F6":("Work he can now take unsupervised that needed help three months ago","Growing each quarter","Manual — capability list","Quarterly"),
}


# Which of John's four lenses each item answers to. Exactly one lens per item,
# so the four scores partition the thirty-six — nothing counted twice, nothing
# left out. Dimensions ask how he is doing at a part of the job; lenses ask what
# kind of thing is going wrong, and they deliberately cut across each other.
LENSES = {
 "skill":       ["A1", "A4", "B1", "B3", "B5", "C3", "E2", "E6"],
 "ethic":       ["A2", "A5", "B2", "B6", "C1", "C4", "E1"],
 "attitude":    ["A3", "A6", "C5", "C6", "D1", "D3", "D4", "D5", "D6", "E5"],
 "durability":  ["B4", "C2", "D2", "E3", "E4", "F1", "F2", "F3", "F4", "F5", "F6"],
}
