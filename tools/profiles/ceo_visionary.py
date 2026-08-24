# -*- coding: utf-8 -*-
"""Chief Vision Officer / CEO. John.

Built around the EOS Visionary seat, since that is how Blossom already runs. The
weighting reflects the two failure modes that actually sink a Visionary-led company:
direction that keeps moving, and ideas that arrive faster than they can be absorbed.
"""

META = {
    "id": "ceo-visionary",
    "label": "Chief Vision Officer / CEO",
    "formTitle": "Chief Vision Officer 360 — Rater Form",
    "consoleTitle": "Chief Vision Officer 360 — Console",
    "blurb": "Thirty-six observable behaviours · about ten minutes",
    "note": ("Built around the EOS Visionary seat. The criticals are weighted toward a stable, "
             "repeatable direction and toward ideas being filtered and finished — the two places "
             "a Visionary most often costs the company more than they add."),
    "relationships": ["self", "manager", "peer", "report"],
}

DIMENSIONS = [
    ("A", "Vision & Direction",      "Is it clear where we are going, and why?"),
    ("B", "Strategic Judgement",     "Are the big calls right, and made in time?"),
    ("C", "Culture & People",        "Is this a place good people stay?"),
    ("D", "External & Relationships","Do they open doors the company could not open itself?"),
    ("E", "Discipline & Follow-through", "Do the ideas become things, or just more ideas?"),
    ("F", "Durability & Improvement",
     "Does the fix hold, and does the company get stronger?"),
]

ITEMS = [
 ("A1", "States where Blossom is going in terms anyone here can repeat", 3),
 ("A2", "Keeps the direction stable long enough to be executed against", 3),
 ("A3", "Connects day-to-day work to the longer-term goal", 1),
 ("A4", "Makes the priorities clear when everything feels urgent", 2),
 ("A5", "Explains a change in direction with the reasoning behind it", 2),
 ("A6", "Sets goals that stretch the company without breaking it", 2),

 ("B1", "Makes the big calls in time rather than letting them drift", 3),
 ("B2", "Faces uncomfortable facts about the business honestly", 3),
 ("B3", "Weighs evidence over instinct when the stakes are high", 2),
 ("B4", "Understands the economics well enough to choose between options", 2),
 ("B5", "Knows which decisions are theirs and which belong to someone else", 2),
 ("B6", "Says plainly when a call they made turned out wrong", 2),

 ("C1", "Holds people to the standard they set for themselves", 2),
 ("C2", "Deals with a people problem rather than working around it", 2),
 ("C3", "Gives credit outward and takes responsibility inward", 2),
 ("C4", "Makes it safe to bring them bad news", 3),
 ("C5", "Invests in the growth of the leadership team", 2),
 ("C6", "Absorbs pressure rather than passing it straight to the team", 2),

 ("D1", "Opens doors the company could not open without them", 2),
 ("D2", "Represents Blossom credibly to growers, handlers and partners", 2),
 ("D3", "Builds relationships that outlast a single deal", 1),
 ("D4", "Brings back intelligence the company can act on", 2),
 ("D5", "Negotiates deals that still look right a year later", 2),
 ("D6", "Brings others into a relationship rather than holding it alone", 1),

 ("E1", "Finishes the initiatives they start, or kills them out loud", 3),
 ("E2", "Filters their own ideas before handing them to the team", 3),
 ("E3", "Lets decisions stay decided", 3),
 ("E4", "Works through the process the team relies on rather than around it", 2),
 ("E5", "Prepares for the meetings they ask others to prepare for", 1),
 ("E6", "Follows through on what they commit to internally", 2),

 ("F1","Solves the underlying problem rather than the symptom in front of them",3),
 ("F2","Makes calls that will still look right in three years",2),
 ("F3","Builds the company so it does not depend on them personally",2),
 ("F4","Invests in capability that only pays off after this year",2),
 ("F5","Changes the system after a failure rather than the person",1),
 ("F6","Holds the company to a rising standard rather than a fixed one",2),
]

METRICS = {
 "A1": ("Team members who can state the company's direction consistently, unprompted", "100% of staff", "Manual — ask each person once a quarter", "Quarterly"),
 "A2": ("Changes of stated strategic direction", "≤ 1 per year", "Manual — dated log of stated direction", "Quarterly"),
 "A3": ("Rocks or projects with no stated line to the longer-term goal", "0", "Manual — quarterly plan review", "Quarterly"),
 "A4": ("Occasions the team reported being unable to tell what came first", "0", "Manual — asked at the monthly check-in", "Monthly"),
 "A5": ("Direction changes announced with written reasoning", "100%", "Manual tally", "Per occurrence"),
 "A6": ("Quarterly Rocks completed", "≥ 80%", "EOS scorecard / ClickUp", "Quarterly"),

 "B1": ("Decisions still open past their agreed decide-by date", "0", "Manual — decision log with dates", "Monthly"),
 "B2": ("Bad-news items he raised himself vs. ones others had to surface", "≥ 1:1", "Manual tally", "Quarterly"),
 "B3": ("Major decisions with the evidence written down before deciding", "≥ 80%", "Manual — decision log", "Quarterly"),
 "B4": ("Can state current runway, margin and burn without preparing", "Correct within 10%", "Manual — spot check", "Quarterly"),
 "B5": ("Decisions he made that belonged to someone else's seat", "≤ 1 per quarter", "Manual tally", "Quarterly"),
 "B6": ("Reversed calls acknowledged openly to the team", "100%", "Manual tally", "Per occurrence"),

 "C1": ("Standards he asked of others that he also met himself", "100% of spot checks", "Manual — leadership review", "Quarterly"),
 "C2": ("Known people problems still unaddressed after 30 days", "0", "Manual — people review", "Monthly"),
 "C3": ("Public credit given for wins vs. blame assigned for losses", "≥ 3:1", "Manual tally", "Quarterly"),
 "C4": ("Team rate 1–5: \"I can bring John a problem early without cost\"", "Average ≥ 4.0", "Anonymous pulse where possible", "Quarterly"),
 "C5": ("Documented development conversations with each leader", "≥ 1 per quarter each", "Manual log", "Quarterly"),
 "C6": ("Urgent requests passed straight to the team within 24h of arriving", "≤ 2 per month", "Manual tally", "Monthly"),

 "D1": ("Introductions or opportunities only he could have created", "≥ 2 per quarter", "Manual tally", "Quarterly"),
 "D2": ("Negative feedback about how Blossom was represented", "0", "Manual tally", "Quarterly"),
 "D3": ("Key relationships still active a year after the first deal", "≥ 80%", "Manual — relationship list review", "Annually"),
 "D4": ("External insights brought back that became a decision or work item", "≥ 1 per month", "Manual tally", "Monthly"),
 "D5": ("Deals renegotiated or regretted within 12 months", "0", "Manual review", "Annually"),
 "D6": ("Key relationships with a second Blossom person involved", "≥ 70%", "Manual — relationship list", "Quarterly"),

 "E1": ("Initiatives started that were finished or formally killed", "100% resolved within 2 quarters", "Manual — initiative log", "Quarterly"),
 "E2": ("New ideas handed to the team per week", "≤ 3, each with a stated priority", "Manual tally", "Weekly"),
 "E3": ("Closed decisions he reopened", "≤ 1 per quarter", "Manual — decision log", "Monthly"),
 "E4": ("Requests made outside the agreed planning and meeting rhythm", "≤ 2 per month", "Manual tally", "Monthly"),
 "E5": ("Meetings he called and arrived prepared for", "100%", "Manual — attendee rating", "Monthly"),
 "E6": ("Internal commitments met by the date given", "≥ 90%", "Manual — commitment log", "Monthly"),

 "F1":("Recurring problems escalated to them more than twice in a year","0","Manual — issues list","Quarterly"),
 "F2":("Major decisions reviewed at 12 months and still judged right","≥ 80%","Manual — decision log","Annually"),
 "F3":("Areas where the company would stall if they were away a month","0","Manual — leadership review","Quarterly"),
 "F4":("Spend or time committed to capability beyond the current year","≥ 10% of leadership time","Manual review","Quarterly"),
 "F5":("Failures followed by a system change rather than only a conversation","≥ 80%","Manual — post-mortem log","Quarterly"),
 "F6":("Standards raised and restated in the last year","≥ 2","Manual review","Annually"),
}


# Which of John's four lenses each item answers to. Exactly one lens per item,
# so the four scores partition the thirty-six — nothing counted twice, nothing
# left out. Dimensions ask how he is doing at a part of the job; lenses ask what
# kind of thing is going wrong, and they deliberately cut across each other.
LENSES = {
 "skill":       ["A1", "A4", "A5", "A6", "B3", "B4", "B5", "D1", "D2", "D4", "D5"],
 "ethic":       ["B1", "E1", "E4", "E5", "E6"],
 "attitude":    ["B2", "B6", "C1", "C2", "C3", "C4", "C6", "E2", "E3"],
 "durability":  ["A2", "A3", "C5", "D3", "D6", "F1", "F2", "F3", "F4", "F5", "F6"],
}
