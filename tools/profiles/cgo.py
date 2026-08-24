# -*- coding: utf-8 -*-
"""Chief Growth Officer. Mark.

Weighted for an early-stage company where the cost of an over-promised deal or a
surprise miss is far higher than the cost of a slightly smaller number.
"""

META = {
    "id": "cgo",
    "label": "Chief Growth Officer",
    "formTitle": "Chief Growth Officer 360 — Rater Form",
    "consoleTitle": "Chief Growth Officer 360 — Console",
    "blurb": "Thirty-six observable behaviours · about ten minutes",
    "note": ("Weighted for growth at a small company: a forecast people can plan against and a promise "
             "the company can keep matter more here than raw activity."),
    "relationships": ["self", "manager", "peer", "report"],
}

DIMENSIONS = [
    ("A", "Pipeline & Revenue",        "Is growth happening, and can we see it coming?"),
    ("B", "Customer & Market Insight", "Do we understand the grower better because of them?"),
    ("C", "Go-to-Market Execution",    "Do plans turn into signed customers?"),
    ("D", "Communication & Leadership","Does the rest of the company know what is happening, and why?"),
    ("E", "Judgement & Accountability","Do they own the number?"),
    ("F", "Durability & Improvement",
     "Does the growth compound, or does it start again each quarter?"),
]

ITEMS = [
 ("A1", "Builds a pipeline the company can forecast from, not a list of hopes", 3),
 ("A2", "Hits the revenue commitments they sign up to", 2),
 ("A3", "Flags a miss early enough that the company can respond", 3),
 ("A4", "Prioritises the accounts that actually move the number", 2),
 ("A5", "Knows the unit economics of the deals they bring in", 2),
 ("A6", "Grows the accounts we already have, not only new logos", 2),

 ("B1", "Brings back what growers actually said, not what confirms the plan", 3),
 ("B2", "Turns customer conversations into something the product team can act on", 2),
 ("B3", "Positions honestly against the competition", 2),
 ("B4", "Spots a shift in the market before it shows up in the numbers", 1),
 ("B5", "Knows which customers are at risk before they churn", 2),
 ("B6", "Separates one loud customer from a real pattern", 2),

 ("C1", "Turns a strategy into a plan with dates and owners", 2),
 ("C2", "Follows through on what they promised a customer", 3),
 ("C3", "Runs a repeatable process rather than improvising each deal", 1),
 ("C4", "Builds materials the rest of the team can actually use", 1),
 ("C5", "Kills what isn't working instead of defending it", 2),
 ("C6", "Checks with product and support before promising something", 2),

 ("D1", "Gives the leadership team an honest read, including the bad parts", 3),
 ("D2", "Sets clear expectations with the people they lead", 2),
 ("D3", "Represents Blossom well in front of customers and the industry", 1),
 ("D4", "Listens to pushback without needing to win", 2),
 ("D5", "Shares context so others can act without them", 2),
 ("D6", "Develops the people who work with them", 2),

 ("E1", "Owns the number — no excuses when it misses", 3),
 ("E2", "Makes decisions at the pace the business needs", 2),
 ("E3", "Says no to deals that are wrong for Blossom", 3),
 ("E4", "Only promises what the company can actually deliver", 3),
 ("E5", "Changes course on evidence rather than defending a position", 2),
 ("E6", "Thinks past this quarter to where growth comes from next year", 2),

 ("F1","Builds growth that compounds rather than a run of one-off wins",3),
 ("F2","Fixes the reason a deal was lost, not just the deal",2),
 ("F3","Chooses the customer we can keep over the one we can close this quarter",2),
 ("F4","Invests in next year's pipeline while still delivering this quarter's",2),
 ("F5","Leaves an account in better shape than they found it",1),
 ("F6","Can point to how they are better at this than a year ago",2),
]

METRICS = {
 "A1": ("Forecast accuracy — closed revenue vs. the forecast given 90 days earlier", "Within ±20%", "Manual — record each forecast, compare at close", "Quarterly"),
 "A2": ("Revenue against the committed number", "≥ 95% of commitment", "Finance / CRM", "Monthly"),
 "A3": ("% of misses flagged before the period closed rather than after", "100%", "Manual tally", "Quarterly"),
 "A4": ("% of selling time spent on the named target accounts", "≥ 70%", "Manual — weekly time or activity review", "Monthly"),
 "A5": ("Deals closed where CAC and expected margin were known before signing", "100%", "Manual checklist at signature", "Per deal"),
 "A6": ("Net revenue retention on existing accounts", "≥ 100%", "Finance / billing", "Quarterly"),

 "B1": ("Grower conversations logged with verbatim notes, not summaries", "≥ 8 per month", "Manual — shared notes doc", "Monthly"),
 "B2": ("Customer insights handed to product that became work items", "≥ 2 per month", "Manual tally / Linear", "Monthly"),
 "B3": ("Competitive claims that survived a fact check", "100%", "Manual — spot check by John or Bryan", "Quarterly"),
 "B4": ("Market shifts called in advance that later proved out", "≥ 1 per year", "Manual — keep a dated prediction log", "Quarterly"),
 "B5": ("Churned accounts that had been flagged at risk beforehand", "≥ 80%", "Manual — maintain a risk list", "Quarterly"),
 "B6": ("Requests escalated as \"a pattern\" that turned out to be one customer", "≤ 1 per quarter", "Manual tally", "Quarterly"),

 "C1": ("% of GTM initiatives with a named owner and a date at kickoff", "100%", "Manual checklist", "Monthly"),
 "C2": ("Customer commitments met by the date promised", "≥ 95%", "Manual — log every commitment made", "Monthly"),
 "C3": ("% of deals that followed the defined stages", "≥ 80%", "CRM / manual", "Quarterly"),
 "C4": ("Sales materials others used without asking him to redo them", "≥ 80% of assets", "Manual tally", "Quarterly"),
 "C5": ("Initiatives formally stopped after failing their test", "≥ 1 per quarter", "Manual tally", "Quarterly"),
 "C6": ("Promises made to customers without checking product or support first", "0", "Manual tally", "Monthly"),

 "D1": ("Leadership rate the honesty of the growth update 1–5", "Average ≥ 4.0", "Manual — one rating per update", "Monthly"),
 "D2": ("Direct reports who can state their top three priorities unprompted", "100%", "Manual — ask at the monthly check-in", "Monthly"),
 "D3": ("Customer or partner complaints about how Blossom was represented", "0", "Manual tally", "Quarterly"),
 "D4": ("Decisions where he changed position after internal pushback", "≥ 1 per quarter", "Manual tally", "Quarterly"),
 "D5": ("Deals or accounts only he can speak to", "Trend to 0", "Manual — maintain a coverage list", "Quarterly"),
 "D6": ("Documented development conversations with each report", "≥ 1 per month each", "Manual log", "Monthly"),

 "E1": ("Misses reported with a cause and a corrective action, not a reason", "100%", "Manual — review each miss", "Monthly"),
 "E2": ("Decisions still open past their agreed decide-by date", "0", "Manual — keep a decision log", "Monthly"),
 "E3": ("Deals declined on fit, and the reason recorded", "≥ 1 per quarter", "Manual tally", "Quarterly"),
 "E4": ("Signed commitments the company could not deliver on time", "0", "Manual tally", "Quarterly"),
 "E5": ("Positions changed on new evidence vs. defended past it", "≥ 2:1", "Manual — decision log review", "Quarterly"),
 "E6": ("Named growth bets for next year with a first step under way", "≥ 2 live at all times", "Manual — plan review", "Quarterly"),

 "F1":("Revenue from repeat and expansion vs. net new each quarter","Repeat share rising","CRM","Quarterly"),
 "F2":("Losses with a written reason and a change made as a result","≥ 80%","CRM — loss reasons","Quarterly"),
 "F3":("Customers signed in the last year still active","≥ 90%","CRM","Quarterly"),
 "F4":("Pipeline created for periods beyond the current quarter","≥ 30% of new pipeline","CRM","Monthly"),
 "F5":("Accounts whose health score improved while they owned them","Majority","CRM / manual review","Quarterly"),
 "F6":("Named capabilities they have added, with evidence","≥ 2 per year","Manual — development log","Annually"),
}


# Which of John's four lenses each item answers to. Exactly one lens per item,
# so the four scores partition the thirty-six — nothing counted twice, nothing
# left out. Dimensions ask how he is doing at a part of the job; lenses ask what
# kind of thing is going wrong, and they deliberately cut across each other.
LENSES = {
 "skill":       ["A1", "A4", "A5", "B2", "B3", "B4", "B5", "B6", "C1", "C3", "C4", "D2", "E2"],
 "ethic":       ["A2", "C2", "C6", "E1", "E4"],
 "attitude":    ["A3", "B1", "D1", "D3", "D4", "E5"],
 "durability":  ["A6", "C5", "D5", "D6", "E3", "E6", "F1", "F2", "F3", "F4", "F5", "F6"],
}
