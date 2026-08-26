# -*- coding: utf-8 -*-
"""Builds the procedure guide PDF for running a Blossom 360 review.

    python3.14 tools/build_procedure_guide.py

Needs python3.14 — this Mac's default python3 is 3.7, which reportlab 5 will not import.

The roster, the rater matrix, the rating scale, the lenses and the item counts are all
read from assessment_content.py rather than typed here, so the guide cannot drift from
the instrument it describes. Rebuild it whenever the content changes.
"""
import sys
sys.dont_write_bytecode = True

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle, CondPageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# reportlab 5 no longer ships the base-14 Type1 fonts. A style asking for "Helvetica-Bold"
# silently falls back to a wide, non-bold face and nothing errors — every <b> in the
# document just renders unbolded. Register Arial as a real family instead.
SUP = "/System/Library/Fonts/Supplemental/"
_FACES = [("Body", "Arial.ttf"), ("Body-Bold", "Arial Bold.ttf"),
          ("Body-Italic", "Arial Italic.ttf"), ("Body-BoldItalic", "Arial Bold Italic.ttf")]
if all(os.path.exists(SUP + f) for _, f in _FACES):
    for name, f in _FACES:
        pdfmetrics.registerFont(TTFont(name, SUP + f))
    pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold",
                                  italic="Body-Italic", boldItalic="Body-BoldItalic")
else:
    raise SystemExit("Arial not found in " + SUP + " — bold text would silently vanish")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from assessment_content import (PROFILES, ROSTER, RELATIONSHIPS, RELATIONSHIP_MAP, SCALE,
                                SCALE_NOTES, LENS_DEFS, CRITICAL_BUDGET, validate,
                                coverage_warnings)

ICLOUD = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/MacDocuments/"
                            "blossom/Employees/DeveloperAssessment")
OUT_DIR = os.environ.get("B360_GUIDE_DIR") or (
    ICLOUD if os.path.isdir(ICLOUD) else os.path.join(os.path.dirname(HERE), "workbooks"))
OUT = os.path.join(OUT_DIR, "ReviewProcedureGuide.pdf")

FORM_URL = "https://bryanvh1.github.io/blossom-360-5d3025/"
CONSOLE_URL = "https://bryanvh1.github.io/blossom-360-5d3025/console.html"

NAVY = colors.HexColor("#1B3A5C")
ACCENT = colors.HexColor("#2E6F8E")
INK = colors.HexColor("#1F2A37")
GREY = colors.HexColor("#6B7280")
LIGHT = colors.HexColor("#EAF1F5")
LINE = colors.HexColor("#C9D4DC")
AMBER_BG = colors.HexColor("#FDF0CF")
AMBER = colors.HexColor("#8A6100")

S = {
 "title": ParagraphStyle("title", fontName="Body-Bold", fontSize=22, leading=26,
                         textColor=NAVY, spaceAfter=4),
 "sub":   ParagraphStyle("sub", fontName="Body-Italic", fontSize=10.5, leading=14,
                         textColor=GREY, spaceAfter=16),
 "h1":    ParagraphStyle("h1", fontName="Body-Bold", fontSize=14.5, leading=18,
                         textColor=NAVY, spaceBefore=18, spaceAfter=7),
 "h2":    ParagraphStyle("h2", fontName="Body-Bold", fontSize=11.5, leading=15,
                         textColor=ACCENT, spaceBefore=12, spaceAfter=4),
 "body":  ParagraphStyle("body", fontName="Body", fontSize=10, leading=14.5,
                         textColor=INK, alignment=TA_LEFT, spaceAfter=7),
 "bullet": ParagraphStyle("bullet", fontName="Body", fontSize=10, leading=14.5,
                          textColor=INK, leftIndent=14, bulletIndent=3, spaceAfter=4),
 "small": ParagraphStyle("small", fontName="Body", fontSize=8.6, leading=11.6,
                         textColor=GREY, spaceAfter=6),
 "cell":  ParagraphStyle("cell", fontName="Body", fontSize=9, leading=12, textColor=INK),
 "cellb": ParagraphStyle("cellb", fontName="Body-Bold", fontSize=9, leading=12, textColor=INK),
 "cellh": ParagraphStyle("cellh", fontName="Body-Bold", fontSize=9, leading=12,
                         textColor=colors.white),
 "note":  ParagraphStyle("note", fontName="Body", fontSize=9.4, leading=13,
                         textColor=INK, leftIndent=8, rightIndent=8,
                         spaceBefore=4, spaceAfter=4),
}


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace("≥", "at least ").replace("≤", "at most ")
            .replace("→", "to").replace("×", "x"))


def P(t, s="body"):
    return Paragraph(esc(t) if "<" not in str(t) else str(t), S[s])


def B(items, s="bullet"):
    return [Paragraph(t if "<" in t else esc(t), S[s], bulletText="•") for t in items]


def table(rows, widths, header=True, align=None):
    data = []
    for i, row in enumerate(rows):
        out = []
        for cell in row:
            st = "cellh" if (header and i == 0) else "cell"
            out.append(cell if isinstance(cell, Paragraph) else Paragraph(esc(cell), S[st]))
        data.append(out)
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    cmds = [("GRID", (0, 0), (-1, -1), 0.5, LINE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
    if header:
        cmds += [("BACKGROUND", (0, 0), (-1, 0), ACCENT)]
    for a in (align or []):
        cmds.append(a)
    t.setStyle(TableStyle(cmds))
    return t


def callout(title, *paras):
    inner = [Paragraph("<b>%s</b>" % esc(title), S["note"])]
    inner += [Paragraph(t if "<" in t else esc(t), S["note"]) for t in paras]
    t = Table([[inner]], colWidths=[6.9 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMBER_BG),
        ("LINEBEFORE", (0, 0), (0, -1), 3, AMBER),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return t


def steps_table(rows):
    data = [[Paragraph("<b>%d</b>" % i, S["cellb"]),
             Paragraph("<b>%s</b><br/><font size=9 color='#1F2A37'>%s</font>"
                       % (esc(a), esc(b)), S["cell"])]
            for i, (a, b) in enumerate(rows, start=1)]
    t = Table(data, colWidths=[0.35 * inch, 6.55 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, LINE),
        ("TEXTCOLOR", (0, 0), (0, -1), ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return t


def decorate(canvas, doc):
    canvas.saveState()
    canvas.setFont("Body", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(0.8 * inch, 0.55 * inch, "Blossom 360 - Review Procedure Guide")
    canvas.drawRightString(7.7 * inch, 0.55 * inch, "Page %d" % doc.page)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(0.8 * inch, 0.72 * inch, 7.7 * inch, 0.72 * inch)
    canvas.restoreState()


def build():
    errs = validate()
    if errs:
        print("VALIDATION FAILED - not building:")
        for e in errs:
            print("  -", e)
        raise SystemExit(1)

    names = [r["name"] for r in ROSTER]
    role_of = {r["name"]: r["role"] for r in ROSTER}
    rel_label = dict(RELATIONSHIPS)
    any_prof = PROFILES[ROSTER[0]["profile"]]
    n_items = len(any_prof["items"])
    n_dims = len(any_prof["dimensions"])

    F = []
    F.append(P("Running an Employee Review", "title"))
    F.append(P("Blossom 360 - the procedure, start to finish. Generated from the live "
               "assessment definitions.", "sub"))

    # ---------------------------------------------------------------- overview
    F.append(P("What this is", "h1"))
    F.append(P("A 360-degree review: everyone who works closely with a person scores the same "
               "set of observable behaviours, that person scores themselves, and the results "
               "show both where they stand and where they and everyone else disagree."))
    F.append(P("Two web pages do the work. There is no server and no database. Nothing is "
               "transmitted anywhere at any point - a rater's answers become a short code they "
               "send you, and the results live only in your own browser. That is deliberate: "
               "assessment data never sits on a website where it could be found."))
    F.append(callout(
        "The one thing that will bite you",
        "Because results live in your browser, clearing your browsing data deletes them. "
        "Export a backup to Google Drive after every session of entering codes. Section 9 "
        "explains how, and Section 10 explains how to get it all back."))

    # ---------------------------------------------------------------- the links
    F.append(P("1. The two links", "h1"))
    F.append(table([
        ["Page", "Link", "Who uses it"],
        [Paragraph("<b>Rater form</b>", S["cellb"]), FORM_URL,
         "Everyone. This is the link you send out."],
        [Paragraph("<b>Console</b>", S["cellb"]), CONSOLE_URL,
         "You only. Where codes are entered and results are read."],
    ], [1.05 * inch, 3.3 * inch, 2.55 * inch]))
    F.append(Spacer(1, 6))
    F.append(P("Both work in any browser, on any device, and neither needs a login. The console "
               "link is not secret - anyone who opens it sees an empty console, because the data "
               "is in your browser and not on the page - but do not include it in the email you "
               "send raters. It invites people into the scoring view of an assessment they are a "
               "subject of."))
    F.append(callout(
        "Always use the same browser on the same machine",
        "Your results are stored per browser. Open the console in Chrome on your laptop and "
        "you will not see anything you entered in Safari, or on another computer. Pick one and "
        "bookmark it.",
        "<b>If you do have to use a different browser or a different machine:</b> before you "
        "start, go to Google Drive and import the latest backup, so you are working from "
        "current data. At the end of the session, export back to Google Drive so the next "
        "person - or the next machine - picks up where you left off. Sections 9 and 10 have "
        "the steps."))

    # ---------------------------------------------------------------- matrix
    F.append(P("2. Who rates whom", "h1"))
    F.append(P("Raters never choose their own relationship - the form fills it in from the "
               "matrix below and shows it read-only. A rater who is a peer one round and a "
               "direct report the next would break the comparison between rounds, and "
               "mis-filing themselves shifts the group averages."))
    F.append(P("Read a row as: on the form about this person, that rater appears as..."))

    hdr = [Paragraph("<b>Being rated</b>", S["cellh"])] + \
          [Paragraph("<b>%s</b>" % esc(n), S["cellh"]) for n in names]
    rows = [hdr]
    for ev in names:
        row = [Paragraph("<b>%s</b>" % esc(ev), S["cellb"])]
        for ra in names:
            if ra == ev:
                row.append(Paragraph("<font color='#6B7280'>Self</font>", S["cell"]))
            else:
                rel = RELATIONSHIP_MAP.get(ev, {}).get(ra)
                row.append(Paragraph(esc(rel_label[rel]) if rel else
                                     "<font color='#6B7280'>-</font>", S["cell"]))
        rows.append(row)
    w = [1.25 * inch] + [1.13 * inch] * len(names)
    F.append(table(rows, w, align=[("BACKGROUND", (0, 1), (0, -1), LIGHT)]))
    F.append(Spacer(1, 6))
    F.append(P("Every manager reads as direct report in the mirrored cell, and peer mirrors "
               "peer. A pair that is blank cannot rate each other at all - the form refuses the "
               "submission. Adding or changing a pairing is a small change to the definitions "
               "followed by a rebuild; it is not something a rater can do."))
    F.append(Spacer(1, 4))
    F.append(table(
        [["Person", "Role", "Rated by", "Scores received"]] +
        [[p["name"], role_of[p["name"]],
          ", ".join("%s (%s)" % (r, rel_label[rl].lower())
                    for r, rl in RELATIONSHIP_MAP.get(p["name"], {}).items()),
          str(len(RELATIONSHIP_MAP.get(p["name"], {})) + 1)]
         for p in ROSTER],
        [0.7 * inch, 1.45 * inch, 3.75 * inch, 1.0 * inch]))
    F.append(Spacer(1, 5))
    gaps = []
    for person in ROSTER:
        prof = PROFILES.get(person["profile"]) if person["profile"] else None
        if not prof:
            continue
        filled = {"self"} | set(RELATIONSHIP_MAP.get(person["name"], {}).values())
        empty = [rel_label[g].lower() for g in prof["relationships"] if g not in filled]
        if empty:
            gaps.append("%s has no %s" % (person["name"], " or ".join(empty)))
    F.append(P("Everyone also rates themselves; that self-score is what the blind-spot column "
               "measures against." +
               (" On the roster as it stands, " + "; ".join(gaps) +
                " - those groups simply do not appear on their forms." if gaps else ""),
               "small"))

    F.append(CondPageBreak(2.2 * inch))

    # ---------------------------------------------------------------- the form
    F.append(P("3. What a rater actually does", "h1"))
    F.append(P("The form takes about ten minutes. %d behaviours across %d dimensions, then "
               "three questions answered in their own words." % (n_items, n_dims)))
    F.append(table(
        [["Dimension", "What it asks"]] +
        [[d[1], d[2]] for d in any_prof["dimensions"]],
        [2.1 * inch, 4.8 * inch]))
    F.append(Spacer(1, 6))
    F.append(P("Every position has its own set of behaviours written for that job - a Chief "
               "Growth Officer is not scored on writing readable code. The dimensions above are "
               "the Developer's; the shape is the same for all five.", "small"))
    F.append(P("The three written questions matter more in the conversation than any score "
               "does. The numbers tell you where to look; these tell you what is going on."))
    F.append(Spacer(1, 2))
    F.extend(B([esc(q.split(". ", 1)[1] if q[:2].rstrip(".").isdigit() else q)
                for q in any_prof["openQuestions"]]))

    # ---------------------------------------------------------------- scale
    F.append(P("4. What the ratings mean", "h1"))
    F.append(P("Raters score each behaviour 1 to 5, or leave it as Not observed."))
    F.append(table(
        [["", "Meaning", "What it looks like"]] +
        [[(v or "blank"), nm, ds] for v, nm, ds in SCALE],
        [0.62 * inch, 1.5 * inch, 4.78 * inch],
        align=[("BACKGROUND", (0, 1), (0, -1), LIGHT)]))
    F.append(Spacer(1, 8))
    for lbl, txt in SCALE_NOTES:
        F.append(P("<b>%s</b> %s" % (esc(lbl), esc(txt))))
    F.append(callout(
        "Not observed is a feature, not a cop-out",
        "Blanks are ignored in the arithmetic. Guesses are not. Tell raters plainly that "
        "leaving something blank is better than inventing a score - it is the single easiest "
        "way to keep the numbers honest."))

    # ---------------------------------------------------------------- importance
    F.append(P("5. What importance means", "h1"))
    F.append(P("Every behaviour carries a weight of 1, 2 or 3 that says how much <b>the role</b> "
               "needs it. Importance is a definition of the job, not a score of the person. "
               "Raters never see it and never vote on it - you and John agree it in advance."))
    F.append(table([
        ["", "Weight", "Meaning"],
        ["3", "Critical", "The role fails without it. Deliberately scarce: exactly %d per "
                          "position." % CRITICAL_BUDGET],
        ["2", "Important", "Expected of the role. Most behaviours sit here."],
        ["1", "Helpful", "Good to have. Its absence is a nuisance, not a problem."],
    ], [0.45 * inch, 1.2 * inch, 5.25 * inch],
        align=[("BACKGROUND", (0, 1), (0, -1), LIGHT)]))
    F.append(Spacer(1, 8))
    F.append(P("The budget of %d criticals is the point. If everything is critical, nothing is - "
               "so to promote one behaviour to a 3 you have to demote another. Set the weights "
               "<b>before</b> any scores arrive. It is much harder to argue a weight up or down "
               "honestly once you can see who it would help." % CRITICAL_BUDGET))
    F.append(P("The same behaviour can carry different weights in different positions. Testing "
               "your own work before handing it off is critical for an associate developer and "
               "merely important for a senior one, because for a senior it is assumed. That is "
               "the instrument working, not an inconsistency.", "small"))
    F.append(P("Weights live in <b>ImportanceReview.xlsx</b>, in this folder - a tab per "
               "position, plus tabs for the metrics and the written questions. Mark it up with "
               "John, and the agreed changes get built back into the forms.", "small"))

    F.append(CondPageBreak(2.2 * inch))

    # ---------------------------------------------------------------- lenses
    F.append(P("6. The four lenses", "h1"))
    F.append(P("Alongside the dimensions, every behaviour is tagged with one of four lenses - "
               "the things John looks for in anyone, whatever the seat."))
    F.append(table(
        [["Lens", "Asks"]] + [[n, q] for _, n, q in LENS_DEFS],
        [1.85 * inch, 5.05 * inch]))
    F.append(Spacer(1, 6))
    F.append(P("Dimensions ask how someone is doing at a part of the job. Lenses ask what kind "
               "of thing is going wrong, and they cut across the dimensions on purpose. Each "
               "behaviour belongs to exactly one lens, so the four scores cover the whole set "
               "with nothing counted twice. The console shows them above the dimension table."))

    # ---------------------------------------------------------------- maths
    F.append(P("7. How the numbers work", "h1"))
    F.append(table([
        ["Term", "What it is"],
        [Paragraph("<b>Others</b>", S["cellb"]),
         "The average of everyone except the person themselves. Their self-score never lifts "
         "their own result."],
        [Paragraph("<b>Blind spot</b>", S["cellb"]),
         "Self minus Others. Plus 1.00 or more means they rate themselves materially higher "
         "than the people around them do. This is usually what lands in the conversation."],
        [Paragraph("<b>Gap score</b>", S["cellb"]),
         "Importance x (5 - Others). How far short it falls, weighted by how much the role "
         "needs it. Range 0 to 12."],
        [Paragraph("<b>Rank</b>", S["cellb"]),
         "The gap scores sorted, biggest first. The top five automatically become the "
         "development plan - nobody chooses them."],
    ], [1.15 * inch, 5.75 * inch]))
    F.append(Spacer(1, 8))
    F.append(P("Weighting by importance is what stops the plan filling up with things that "
               "scored badly but barely matter. A behaviour scored 2.5 that is critical outranks "
               "one scored 2.75 that is merely helpful, by a wide margin. A plain list of the "
               "lowest scores would have put them next to each other."))
    F.append(P("Blanks never count as zero. If nobody scored a behaviour, it has no average and "
               "is left out of the ranking entirely.", "small"))
    F.append(P("Ties are common with few raters and whole numbers. They break by importance, "
               "then blind spot, then item order - and the console tells you when items tie at "
               "the fifth slot, because which one makes the cut is then a judgement call rather "
               "than a result.", "small"))

    F.append(CondPageBreak(2.2 * inch))

    # ---------------------------------------------------------------- procedure
    F.append(P("8. Running a review, step by step", "h1"))
    F.append(steps_table([
     ("Agree the weights first",
      "Open ImportanceReview.xlsx with John and settle the importance of each behaviour for "
      "the position. Do this before anyone is asked for a score. If you change weights, the "
      "forms get rebuilt before you send them out."),
     ("Tell people what is happening",
      "Say who is being assessed, who is rating them, that it is not anonymous, and that "
      "scores and a summary of the comments go back to the person. People score honestly "
      "when they know the rules and generously when they are guessing at them."),
     ("Send the form link",
      "Send %s to each rater. They pick who they are rating and who they are; the "
      "relationship fills itself in. Ask for it back within a week." % FORM_URL),
     ("Have the person rate themselves too",
      "Same link, choosing their own name in both boxes. Ask them to do it before they see "
      "anyone else's, since the self-score is what the blind-spot column measures against."),
     ("Collect the codes",
      "When a rater finishes they get a short code and send it to you - by email or Slack, "
      "as plain text. Nothing is sent automatically; the code is their response. If somebody "
      "sends a code that arrives cut short or altered, the console will say so and you ask "
      "for it again."),
     ("Enter them in the console",
      "Open %s, choose the person, click Add a response, paste the codes - several at once, "
      "one per line - and save. The console checks each one and refuses anything answered "
      "against the wrong set of questions." % CONSOLE_URL),
     ("Back up straight away",
      "Click Export backup and put the file in Google Drive. Do this every time you enter "
      "codes, before you close the browser. See Section 9."),
     ("Read the results",
      "The Results tab gives the four lenses, the dimension scores by rater group, the radar "
      "chart and the blind spots. Read the written answers before the numbers - they explain "
      "what the numbers are pointing at."),
     ("Hold the conversation",
      "Lead with what should not change. Then the blind spots, framed as a disagreement about "
      "reality rather than a verdict. The person should leave knowing the five things on the "
      "plan and why those five."),
     ("Set baselines and targets",
      "For each of the five development items, agree what it is today and what it should be "
      "in 90 days. The Metric Library proposes a way to count each one. A metric nobody will "
      "actually keep is worse than none - swap it for one you will."),
     ("Save a snapshot",
      "On the Progression tab, save a snapshot labelled with the date. That is the baseline "
      "the next round is compared against."),
     ("Re-run at 90 and 180 days",
      "Same behaviours, same raters. Two points is an anecdote; the line is the evidence - "
      "for the person, and for any promotion decision."),
    ]))

    F.append(CondPageBreak(2.2 * inch))

    # ---------------------------------------------------------------- backup
    F.append(P("9. Saving your data to Google Drive", "h1"))
    F.append(P("Everything you enter lives in your browser's local storage on one machine. It "
               "survives closing the tab, quitting the browser and restarting the Mac. It does "
               "<b>not</b> survive clearing your browsing data, and it does not follow you to "
               "another computer. A backup is the only copy that does."))
    F.append(P("What a backup contains", "h2"))
    F.append(P("<b>Everything in your console</b> - every response for every person, the "
               "development plans, the snapshots and the metric readings. One JSON file. It is "
               "not one person's assessment, which matters when you decide what to call it and "
               "who to send it to."))
    F.append(P("What it is called", "h2"))
    F.append(P("The console names the file itself:"))
    F.append(Paragraph("<b>blossom-360_2026-08-26_1430_bryan.json</b>", S["body"]))
    F.append(P("Date, then the time in 24-hour form, then whose console it came from. The first "
               "time you export, it asks whose console this is and remembers the answer - the "
               "line under the buttons shows it and lets you change it."))
    F.append(P("Two exports can never collide, they sort oldest to newest in Drive, and the name "
               "says who to ask about it. Do <b>not</b> add the name of the person being reviewed: "
               "the file holds all five, and a file called \"frans\" invites someone to import it "
               "thinking it only touches Frans.", "small"))
    F.append(P("Method A - Google Drive for Desktop (recommended)", "h2"))
    F.append(P("If Drive is installed on the Mac it appears as an ordinary folder, and this "
               "becomes a two-second habit."))
    F.extend(B([
     "In the console, click <b>Export backup</b>. The file lands in your Downloads folder.",
     "Drag it into your Google Drive folder - make one called <b>blossom / 360 backups</b> and "
     "always use that one.",
     "Set the sharing on that folder once, in Drive, the normal way. Restrict it to yourself "
     "and John. It contains real scores and written comments about real people.",
    ]))
    F.append(P("You can also point the browser straight at that folder: in Chrome, Settings, "
               "Downloads, turn on \"Ask where to save each file\". Then Export backup prompts "
               "you and you choose the Drive folder - no dragging.", "small"))
    F.append(P("Method B - upload through the browser", "h2"))
    F.append(P("If Drive is not installed on the machine, the file still goes to Downloads. "
               "Open drive.google.com, open your 360 backups folder, and drag the file in - or "
               "use New, then File upload."))
    F.append(callout(
        "When to export",
        "Every time you finish entering codes, before you close the browser. That is the only "
        "moment new data exists, which makes it the only moment a backup is worth taking. "
        "Keep the dated files rather than overwriting - they are tiny, and being able to go "
        "back to last month's state has saved people before."))
    F.append(P("Because the name carries the time, exporting twice in one day gives you two "
               "files rather than a collision. Keep them both.", "small"))

    F.append(CondPageBreak(2.2 * inch))

    # ---------------------------------------------------------------- restore
    F.append(P("10. Getting it back", "h1"))
    F.append(P("If you open the console and it is empty - browsing data cleared, a new machine, "
               "a different browser, or you are simply looking at it somewhere new - the data "
               "is not lost as long as you have a backup."))
    F.append(steps_table([
     ("Get the file onto the machine",
      "From Google Drive, download the newest blossom-360_ file - they sort oldest to newest, "
      "so it is the one at the bottom. With Drive for Desktop it is already there in the "
      "folder. Note where it is."),
     ("Open the console",
      "Go to %s in the browser you intend to use from now on." % CONSOLE_URL),
     ("Click Import backup",
      "A file picker opens. Choose the backup file."),
     ("Confirm the replace",
      "It asks whether to replace everything currently in this browser with the contents of "
      "that file. Say yes."),
     ("Check it landed",
      "Pick a person and confirm the responses and dates look right. Then export a fresh "
      "backup, so this machine's copy is the current one going forward."),
    ]))
    F.append(Spacer(1, 8))
    F.append(callout(
        "Import replaces - it does not merge",
        "Importing wipes whatever is in that browser and puts the file's contents there "
        "instead. If the browser already holds responses that are not in the file - say you "
        "entered three codes this morning and the backup is from last week - export the "
        "current state first under a different name, or you will lose them."))
    F.append(P("This is also how you move to a new laptop, or hand a copy to John: export, put "
               "the file in the shared Drive folder, import at the other end. There is no sync - "
               "whoever imports last has their own separate copy from that point on, so decide "
               "between you who is holding the live one."))

    # ---------------------------------------------------------------- sharing
    F.append(P("11. Sharing with John", "h1"))
    F.append(P("Importing replaces; it never merges. There is no sync. That makes two people "
               "entering codes at the same time the one thing that can quietly destroy work, so "
               "the rule is simple:"))
    F.append(callout(
        "One live console at a time",
        "Bryan holds it. Every code comes to Bryan and Bryan enters all of them. John imports a "
        "copy whenever he wants to read results, and never exports. Nothing can be lost, and "
        "neither of you has to coordinate."))
    F.append(P("How John reads the results", "h2"))
    F.extend(B([
     "At the end of a session of entering codes, Bryan exports to the shared Drive folder.",
     "John downloads the newest file - they sort by date and time - and clicks Import backup.",
     "John reads. He does not enter codes, and he does not export.",
    ]))
    F.append(P("Why it has to work that way", "h2"))
    F.append(P("Suppose both consoles are live. John exports at nine and Bryan imports it. Bryan "
               "enters three of Frans's codes at ten. Meanwhile John, not knowing, enters two of "
               "Mark's. Bryan exports at eleven and John imports it - and John's two codes are "
               "gone. Nothing warns either of them, and the only evidence is a rater who "
               "eventually asks why their scores are missing."))
    F.append(P("If John does need to enter codes", "h2"))
    F.append(P("Pass the baton and say so out loud. He tells you he is taking it, imports the "
               "newest file, enters what he has, exports, and tells you he is done. You import "
               "that before you touch anything. The rule is not the file name - it is that only "
               "one console is being written to at any moment."))
    F.append(P("Set the sharing on the Drive folder to just the two of you. It holds real scores "
               "and written comments about real people.", "small"))

    # ---------------------------------------------------------------- troubleshooting
    F.append(P("12. If something goes wrong", "h1"))
    F.append(table([
        ["Symptom", "What it means and what to do"],
        ["The console is empty",
         "You are in a different browser or machine, or browsing data was cleared. Import your "
         "most recent backup - Section 10."],
        ["A code is refused as damaged or cut short",
         "It was altered in transit, usually by autocorrect turning characters into curly "
         "quotes. Ask for it again, pasted as plain text. Line breaks are fine; the console "
         "ignores them."],
        ["A code is refused as the wrong questions",
         "It was answered against an older version of the form. Ask the rater to fill it in "
         "again from the current link."],
        ["A rater says the form will not let them submit",
         "Either something is unanswered - it scrolls to the first one - or that pair is not "
         "in the matrix. If the pairing is genuinely needed, it has to be added to the "
         "definitions and rebuilt."],
        ["The Email it to Bryan button does nothing",
         "That button needs a mail program like Outlook or Apple Mail. Anyone using webmail "
         "should use Copy code and paste it into an email instead."],
        ["Someone filled the form in twice",
         "Same person, rater and date replaces the earlier one. A different date is kept as a "
         "second response and both get averaged in - remove the stale one with the Remove "
         "button on the rater coverage list."],
        ["John's entries vanished",
         "Both consoles were being written to at once and one import overwrote the other. "
         "Section 11 - one live console at a time. Recover from the newest export that still "
         "has them, if there is one."],
        ["The scores look too generous",
         "Almost always the scale drifting. Re-read the two notes in Section 4 to the group "
         "before the next round; most scores should be 3s and 4s."],
    ], [1.9 * inch, 5.0 * inch]))

    # ---------------------------------------------------------------- ground rules
    F.append(P("13. The ground rules", "h1"))
    F.extend(B([
     "<b>This is not anonymous, and everyone knows it.</b> Every response carries the rater's "
     "name. That is Blossom's choice: candid feedback attached to a name beats polite feedback "
     "from nobody. Say it up front rather than letting people work it out.",
     "<b>Scores go back to the person.</b> The numbers are shared and the written comments are "
     "summarised. The point is their development, not a file.",
     "<b>Importance is agreed before scores arrive.</b> Setting the bar after you can see who "
     "clears it is how a review becomes a negotiation.",
     "<b>The bar is the role's bar.</b> A 4 for an associate developer means strong for an "
     "associate developer, not as good as a lead. The same behaviour scored across two "
     "positions does not mean the same absolute thing.",
     "<b>Five development items, not fifteen.</b> Anything past five stops being a plan and "
     "becomes a performance file. If a sixth matters more later, retire one.",
     "<b>Count events, never adjectives.</b> \"Two items reopened\" is checkable. \"Quality "
     "improved\" is a debate.",
    ]))
    F.append(Spacer(1, 10))
    F.append(P("This guide is generated from the assessment definitions, so the roster, the "
               "matrix, the scale and the lenses above are always what the forms actually use. "
               "Rebuild it after any change with: python3.14 tools/build_procedure_guide.py",
               "small"))

    os.makedirs(OUT_DIR, exist_ok=True)
    doc = BaseDocTemplate(OUT, pagesize=LETTER,
                          leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                          topMargin=0.75 * inch, bottomMargin=0.85 * inch,
                          title="Blossom 360 - Review Procedure Guide",
                          author="Blossom")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=decorate)])
    doc.build(F)
    return OUT


if __name__ == "__main__":
    out = build()
    print("saved:", out)
