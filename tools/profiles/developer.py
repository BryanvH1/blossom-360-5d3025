# -*- coding: utf-8 -*-
"""Developer — the lead-developer track. Frans."""

META = {
    "id": "developer",
    "label": "Developer",
    "formTitle": "Developer 360 — Rater Form",
    "consoleTitle": "Developer 360 — Console",
    "blurb": "Thirty-six observable behaviours · about ten minutes",
    "note": ("Weighted for a software developer moving toward lead developer: nine of the thirty-six "
             "are critical, and they lean on handover, transparency and mentoring."),
    # Jeremy is led by Frans in practice, and the person being mentored is the best judge
    # of the mentoring items — two of which are criticals here.
    "relationships": ["self", "manager", "peer"],
}

# Same three questions as every other profile — this override exists only to say "he",
# matching the pronoun used throughout this profile's items. The third question must stay
# word-for-word identical to the standard one or the answers stop being comparable.
OPEN_QS = [
 "1. What is he genuinely good at — what should not change?",
 "2. If he changed ONE thing, what would make the biggest difference?",
 "3. What would you need to see to be fully confident in them in this role "
 "and growing with the organization?",
]

DIMENSIONS = [
    ("A", "Delivery & Predictability",
     "Can the business plan around him?"),
    ("B", "Code & Technical Craft",
     "Is the work durable, or does it come back?"),
    ("C", "Communication & Transparency",
     "Do people know where things stand without chasing him?"),
    ("D", "Collaboration & Coachability",
     "Does feedback actually change anything?"),
    ("E", "Ownership & Lead Readiness",
     "Does he act like the outcome is his?"),
    ("F", "Durability & Improvement",
     "Does the fix hold, and does the standard rise?"),
]

ITEMS = [
 ("A1","Gives estimates that turn out to be close to reality",2),
 ("A2","Finishes what he starts before picking up new work",2),
 ("A3","Raises a delay or blocker early, before the date is missed",3),
 ("A4","Breaks large work into pieces that can be shipped and reviewed",1),
 ("A5","Delivers work that is genuinely done — tested, not \"done except…\"",3),
 ("A6","Negotiates scope changes openly rather than absorbing them silently",2),

 ("B1","Writes code others can read and change without asking him",3),
 ("B2","Tests his own work before handing it off",2),
 ("B3","Chooses the simple solution when the simple solution is enough",1),
 ("B4","Names and logs technical debt rather than hiding it",2),
 ("B5","Diagnoses production problems quickly and accurately, under pressure",2),
 ("B6","Keeps systems documented well enough that someone else could take over tomorrow",3),

 ("C1","Provides status without being asked for it",2),
 ("C2","Writes decisions and context down where others can find them",2),
 ("C3","Explains technical trade-offs so a non-developer can make the call",2),
 ("C4","Acknowledges messages and requests within an agreed time",1),
 ("C5","Says \"I'm stuck\" instead of going quiet",2),
 ("C6","Delivers bad news early and plainly",3),

 ("D1","Receives critical feedback without becoming defensive",2),
 ("D2","Acts on feedback — the same issue doesn't need raising twice",3),
 ("D3","Asks for help before burning significant time",2),
 ("D4","Executes a decision fully even when he argued against it",2),
 ("D5","Shares what he knows instead of holding it",2),
 ("D6","Keeps disagreements about the work, not the person",1),

 ("E1","Owns the outcome, not the ticket — follows through to working in production",3),
 ("E2","Thinks past his own task to what the product and customer need",2),
 ("E3","Reviews others' work in a way that raises the bar without discouraging",2),
 ("E4","Mentors — makes the other developers measurably better",3),
 ("E5","Anticipates risk and plans for it instead of reacting",2),
 ("E6","Can be handed an ambiguous problem and come back with a plan",2),

 ("F1","Fixes the cause, so the same problem does not come back",3),
 ("F2","Changes what let the failure happen, not just the thing that failed",2),
 ("F3","Comes back and pays down the shortcut once the pressure is off",2),
 ("F4","Chooses the option still right in a year when the deadline argues otherwise",2),
 ("F5","Removes the recurring manual step instead of repeating it",1),
 ("F6","Is visibly better at the craft than he was a year ago",2),
]

METRICS = {
 "A1":("% of issues finished within ±25% of the estimate he gave","≥ 70%","Manual tally / Linear estimate vs. actual","Monthly"),
 "A2":("Peak number of items in progress at one time during the week","≤ 2","Manual tally / Linear board snapshot","Weekly"),
 "A3":("% of missed dates where he gave a heads-up ≥1 day BEFORE the date","100%","Manual tally (John or Bryan logs each miss)","Monthly"),
 "A4":("% of work items closed within 5 working days of being started","≥ 80%","Manual tally / Linear cycle time","Monthly"),
 "A5":("Number of items reopened or bounced back after being called done","≤ 1 per month","Manual tally","Monthly"),
 "A6":("Number of scope changes discovered after the fact rather than agreed up front","0","Manual tally","Monthly"),

 "B1":("Questions others must ask him to understand or change his code","Trend down 50% in 90 days","Manual tally / GitHub review comments","Monthly"),
 "B2":("Defects found by someone else within 2 weeks of a release","≤ 2 per release","Manual tally","Per release"),
 "B3":("Times a reviewer flags a solution as more complex than the problem needs","≤ 1 per month","Manual tally / code review notes","Monthly"),
 "B4":("Tech-debt items he logs himself vs. items others discover","≥ 2 logged/month, ≥ 2:1 ratio","Manual tally / Linear backlog label","Monthly"),
 "B5":("Median time from a bug being reported to the cause being identified","≤ 1 business day","Manual tally","Monthly"),
 "B6":("% of systems he owns with a current one-page README/runbook a stranger could follow","100% by day 90","Manual checklist (list systems, tick off)","Monthly"),

 "C1":("% of weeks with a written status update posted without being asked","100%","Manual tally (count the weeks)","Weekly"),
 "C2":("Decisions written into a doc or issue comment","≥ 4 per month","Manual tally","Monthly"),
 "C3":("John/Bryan rate 1–5: \"I understood the trade-off well enough to decide\"","Average ≥ 4.0","Manual — one rating per explanation","Monthly"),
 "C4":("% of requests acknowledged within 1 business day","≥ 90%","Manual tally / spot check","Monthly"),
 "C5":("Stretches of >2 days stuck with no one told","0","Manual tally + his own log","Weekly"),
 "C6":("Surprises — problems leadership learned about only after the deadline","0","Manual tally","Monthly"),

 "D1":("% of feedback conversations the giver rates as \"received openly\"","≥ 90%","Manual — giver logs it same day","Per conversation"),
 "D2":("Pieces of feedback that had to be raised a second time","0 per quarter","Manual tally (keep a feedback log)","Monthly"),
 "D3":("Tasks where more than a day was lost before he asked for help","≤ 1 per month","Manual tally + his own log","Monthly"),
 "D4":("Closed decisions he reopens or relitigates","0","Manual tally","Monthly"),
 "D5":("Areas only Frans can support (bus factor of 1); knowledge-share sessions run","Trend to 0; ≥ 1 session/month","Manual — maintain a coverage list","Monthly"),
 "D6":("Disagreements that had to be escalated to John or Bryan","0","Manual tally","Monthly"),

 "E1":("% of his items that reach production working without someone else finishing them","≥ 95%","Manual tally","Monthly"),
 "E2":("Improvements or risks he raised outside his own assigned work","≥ 2 per month","Manual tally","Monthly"),
 "E3":("Work items he reviewed for others; median review turnaround","≥ 8/month; ≤ 1 business day","Manual tally / GitHub PR reviews","Monthly"),
 "E4":("Hours pairing or mentoring; peer-rated helpfulness 1–5","≥ 4 hrs/month; ≥ 4.0","Manual log + quarterly peer rating","Monthly / Quarterly"),
 "E5":("Unplanned firefights vs. risks he flagged in advance","Firefights trend down; ≥ 2 risks flagged/month","Manual tally","Monthly"),
 "E6":("% of ambiguous problems where he returned a written plan within 3 days, unprompted","100%","Manual tally","Per occurrence"),

 "F1":("Production issues that recur within 90 days of being called fixed","0","Manual — incident log","Monthly"),
 "F2":("Incidents whose follow-up changed the system, not only the instance","≥ 80%","Manual — incident log","Monthly"),
 "F3":("Logged shortcuts still open after 90 days","≤ 2","Tech debt list","Monthly"),
 "F4":("Deadline trade-offs where the durable option was chosen and said out loud","Majority","Manual tally","Quarterly"),
 "F5":("Recurring manual steps automated or removed","≥ 1 per quarter","Manual tally","Quarterly"),
 "F6":("Review comments still repeating a theme raised a year ago","Trending to 0","GitHub review history","Annually"),
}


# Which of John's four lenses each item answers to. Exactly one lens per item,
# so the four scores partition the thirty-six — nothing counted twice, nothing
# left out. Dimensions ask how he is doing at a part of the job; lenses ask what
# kind of thing is going wrong, and they deliberately cut across each other.
LENSES = {
 "skill":       ["A1", "A4", "B1", "B3", "B5", "C3", "E2", "E3", "E6"],
 "ethic":       ["A2", "A5", "B2", "C1", "C4", "E1"],
 "attitude":    ["A3", "A6", "C5", "C6", "D1", "D3", "D4", "D5", "D6"],
 "durability":  ["B4", "B6", "C2", "D2", "E4", "E5", "F1", "F2", "F3", "F4", "F5", "F6"],
}
