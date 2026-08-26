# -*- coding: utf-8 -*-
"""Builds the two quick-reference cards.

    python3.14 tools/build_quick_reference.py

    RaterQuickReference.pdf     one page, for the people filling in a form
    ConsoleQuickReference.pdf   two pages, for whoever runs the console

Needs python3.14 — this Mac's default python3 is 3.7, which reportlab 5 will not import.
The scale, the roster and the links come from assessment_content.py, so the cards cannot
describe a form that no longer exists.
"""
import sys
sys.dont_write_bytecode = True

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle, CondPageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# reportlab 5 dropped the base-14 Type1 fonts: a style asking for "Helvetica-Bold" falls
# back to a non-bold face and nothing errors. Register Arial as a real family instead.
SUP = "/System/Library/Fonts/Supplemental/"
_FACES = [("Body", "Arial.ttf"), ("Body-Bold", "Arial Bold.ttf"),
          ("Body-Italic", "Arial Italic.ttf"), ("Body-BoldItalic", "Arial Bold Italic.ttf")]
if not all(os.path.exists(SUP + f) for _, f in _FACES):
    raise SystemExit("Arial not found in " + SUP + " — bold text would silently vanish")
for _n, _f in _FACES:
    pdfmetrics.registerFont(TTFont(_n, SUP + _f))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold",
                              italic="Body-Italic", boldItalic="Body-BoldItalic")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from assessment_content import (PROFILES, ROSTER, SCALE, OPEN_QS as DEFAULT_OPEN_QS,
                                validate)

ICLOUD = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/MacDocuments/"
                            "blossom/Employees/DeveloperAssessment")
OUT_DIR = os.environ.get("B360_GUIDE_DIR") or (
    ICLOUD if os.path.isdir(ICLOUD) else os.path.join(os.path.dirname(HERE), "workbooks"))

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
GREEN_BG = colors.HexColor("#E4F0E2")

S = {
 "title": ParagraphStyle("title", fontName="Body-Bold", fontSize=16.5, leading=19,
                         textColor=NAVY, spaceAfter=2),
 "sub":   ParagraphStyle("sub", fontName="Body-Italic", fontSize=9.2, leading=12,
                         textColor=GREY, spaceAfter=7),
 "h":     ParagraphStyle("h", fontName="Body-Bold", fontSize=10.5, leading=13,
                         textColor=ACCENT, spaceBefore=5.5, spaceAfter=2.5),
 "body":  ParagraphStyle("body", fontName="Body", fontSize=8.8, leading=11.6,
                         textColor=INK, spaceAfter=4),
 "small": ParagraphStyle("small", fontName="Body", fontSize=8, leading=10.6,
                         textColor=GREY, spaceAfter=4),
 "cell":  ParagraphStyle("cell", fontName="Body", fontSize=8.4, leading=11, textColor=INK),
 "cellb": ParagraphStyle("cellb", fontName="Body-Bold", fontSize=8.4, leading=11, textColor=INK),
 "cellh": ParagraphStyle("cellh", fontName="Body-Bold", fontSize=8.4, leading=11,
                         textColor=colors.white),
 "note":  ParagraphStyle("note", fontName="Body", fontSize=8.6, leading=11.4, textColor=INK,
                         leftIndent=7, rightIndent=7, spaceBefore=3, spaceAfter=3),
 "step":  ParagraphStyle("step", fontName="Body", fontSize=8.8, leading=11.6, textColor=INK),
}


def brief(desc):
    """First sentence of a scale description, or the first two if one is very short."""
    parts = [p.strip() for p in desc.split(". ") if p.strip()]
    out = parts[0]
    if len(out) < 55 and len(parts) > 1:
        out += ". " + parts[1]
    return out.rstrip(".") + "."


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace("≥", "at least ").replace("≤", "at most ").replace("→", "to"))


def P(t, s="body"):
    return Paragraph(t if "<" in str(t) else esc(t), S[s])


def bullets(items, s="body"):
    st = ParagraphStyle("b_" + s, parent=S[s], leftIndent=12, bulletIndent=2, spaceAfter=3)
    return [Paragraph(t if "<" in t else esc(t), st, bulletText="•") for t in items]


def table(rows, widths, header=True, extra=None, zebra=False):
    data = []
    for i, row in enumerate(rows):
        out = []
        for c in row:
            st = "cellh" if (header and i == 0) else "cell"
            if isinstance(c, Paragraph):
                out.append(c)
            else:
                # same convention as P() and bullets(): a cell carrying markup is passed
                # through, anything else is escaped
                out.append(Paragraph(c if "<" in str(c) else esc(c), S[st]))
        data.append(out)
    t = Table(data, colWidths=widths, hAlign="LEFT")
    cmds = [("GRID", (0, 0), (-1, -1), 0.5, LINE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 2.6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6)]
    if header:
        cmds.append(("BACKGROUND", (0, 0), (-1, 0), ACCENT))
    if zebra:
        for r in range(1 if header else 0, len(data)):
            if r % 2 == (1 if header else 0):
                cmds.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#F7FAFC")))
    for c in (extra or []):
        cmds.append(c)
    t.setStyle(TableStyle(cmds))
    return t


def box(title, *paras, tone="amber", width=6.9):
    inner = [Paragraph("<b>%s</b>" % esc(title), S["note"])]
    inner += [Paragraph(t if "<" in t else esc(t), S["note"]) for t in paras]
    t = Table([[inner]], colWidths=[width * inch], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMBER_BG if tone == "amber" else GREEN_BG),
        ("LINEBEFORE", (0, 0), (0, -1), 3, AMBER if tone == "amber" else ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def numbered(rows, num_w=0.3, total=6.9):
    data = [[Paragraph("<b>%d</b>" % i, S["cellb"]),
             Paragraph("<b>%s</b> %s" % (esc(a), esc(b)), S["step"])]
            for i, (a, b) in enumerate(rows, start=1)]
    t = Table(data, colWidths=[num_w * inch, (total - num_w) * inch], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINE),
        ("TEXTCOLOR", (0, 0), (0, -1), ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4)]))
    return t


def footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Body", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(0.75 * inch, 0.45 * inch, text)
        canvas.drawRightString(7.75 * inch, 0.45 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def render(path, flow, foot):
    doc = BaseDocTemplate(path, pagesize=LETTER,
                          leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                          topMargin=0.6 * inch, bottomMargin=0.65 * inch,
                          title=foot, author="Blossom")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="b")
    doc.addPageTemplates([PageTemplate(id="m", frames=[frame], onPage=footer(foot))])
    doc.build(flow)
    return path


# =====================================================================
def rater_card():
    any_prof = PROFILES[ROSTER[0]["profile"]]
    n_items = len(any_prof["items"])
    F = []
    F.append(P("Filling in a 360 - Quick Reference", "title"))
    F.append(P("Blossom - about ten minutes - everything you need is on this page", "sub"))

    F.append(P("What to do", "h"))
    F.append(numbered([
     ("Open the form and say who you are rating, and who you are.",
      FORM_URL + " - two dropdowns at the top. Your relationship fills itself in; you do not "
      "choose it."),
     ("Score %d behaviours, 1 to 5." % n_items,
      "Or tick Not observed. See the scale below."),
     ("Answer the three written questions.",
      "In your own words. These matter more than the numbers."),
     ("Click Generate my response code.",
      "It will not let you through with anything unanswered, and tells you what is missing."),
     ("Click Copy code, then paste it into an email or Slack message to Bryan.",
      "The code IS your response. Nothing is sent until you send it."),
    ]))

    F.append(P("What the scores mean", "h"))
    F.append(table(
        [["", "", "What it looks like"]] + [[(v or "blank"), nm, brief(ds)] for v, nm, ds in SCALE],
        [0.5 * inch, 1.35 * inch, 5.05 * inch],
        extra=[("BACKGROUND", (0, 1), (0, -1), LIGHT)]))

    F.append(Spacer(1, 3))
    F.append(box("Most scores should be 3s and 4s",
                 "A 3 means they are doing the job - the expected score, not a criticism. Mostly "
                 "4s and 5s usually means you are rating how much you enjoy working with someone. "
                 "And Not observed beats a guess: blanks are ignored in the maths, guesses are not.",
                 tone="green"))

    F.append(P("The three written questions", "h"))
    F.extend(bullets([esc(q.split(". ", 1)[1] if q[:2].rstrip(".").isdigit() else q)
                      for q in DEFAULT_OPEN_QS]))
    F.append(P("The third is sometimes worded for the specific role - answer what the form in "
               "front of you asks.", "small"))

    F.append(P("Worth knowing before you start", "h"))
    F.append(table([
        ["This is not anonymous",
         "Your name goes with your answers and the scores are shared with the person. Written "
         "answers are summarised, not passed on verbatim."],
        ["The bar is that person's role",
         "A 4 for an associate developer means strong for an associate developer - not as good as "
         "a lead. You are scoring against their job, not against each other."],
        ["Score behaviour, not personality",
         "Every item is something you can point at. If you cannot think of an occasion, that is "
         "what Not observed is for."],
    ], [1.5 * inch, 5.4 * inch], header=False, zebra=True))

    F.append(P("If something goes wrong", "h"))
    F.append(table([
        ["The form will not submit",
         "Something is unanswered - it scrolls you to the first one. Use Not observed if you "
         "cannot judge it. If it says you are not set up to rate that person, tell Bryan."],
        ["The Email it to Bryan button does nothing",
         "It needs Outlook or Apple Mail. On webmail, use Copy code and paste it into an email."],
        ["You are told the code arrived damaged",
         "Something reformatted it in transit. Redo the form and send the code as plain text, not "
         "inside a formatted document."],
    ], [2.15 * inch, 4.75 * inch], header=False, zebra=True))

    return render(os.path.join(OUT_DIR, "RaterQuickReference.pdf"), F,
                  "Blossom 360 - Rater Quick Reference   |   Questions to Bryan. "
                  "Please send your code back within a week.")


# =====================================================================
def console_card():
    F = []
    F.append(P("Using the Console - Quick Reference", "title"))
    F.append(P("Blossom 360 - for whoever is entering codes and reading results", "sub"))

    F.append(P("The screen, top to bottom", "h"))
    F.append(table([
        ["Person dropdown",
         "Who you are looking at. Everything on every tab follows this. Their role shows "
         "underneath."],
        ["Add a response",
         "Opens the paste box for entering rater codes."],
        ["Export backup / Import backup",
         "Your only safety net. See the back of this card."],
        ["This console belongs to...",
         "Your name, used in backup filenames so anyone can see where a file came from. Click "
         "change to edit it."],
        ["Rater coverage",
         "Who has returned a code and who has not, with the date. Each row has a Remove button "
         "for deleting a response."],
        ["The five tabs",
         "Scores, Results, Development Plan, Metric Library, Progression - below."],
    ], [1.75 * inch, 5.15 * inch], header=False, zebra=True))

    F.append(P("What each tab shows", "h"))
    F.append(table([
        ["Tab", "What is on it", "What you use it for"],
        ["Scores", "Every behaviour, each rater's score, the group averages, blind spot, gap and "
                   "rank. Written answers underneath.",
                   "The raw detail. Read the written answers first."],
        ["Results", "The four lenses, then dimension scores by rater group, the radar chart and "
                    "the five biggest blind spots.",
                    "The headline read. Start here."],
        ["Development Plan", "The top five items by gap, with a suggested metric. Baseline, "
                             "90-day target, cadence and owner are editable.",
                             "Fill in with the person in the room. Saves as you type."],
        ["Metric Library", "A proposed way to count every behaviour, not just the five.",
                           "Swapping in a metric you will actually keep."],
        ["Progression", "Snapshots over time, the trend chart, and the metric readings table.",
                        "Save a snapshot each round. Two points is an anecdote."],
    ], [1.15 * inch, 3.15 * inch, 2.6 * inch], zebra=True))

    F.append(P("Entering codes", "h"))
    F.append(numbered([
     ("Pick the person", "in the dropdown at the top."),
     ("Click Add a response.", "A paste box opens."),
     ("Paste the codes.", "Several at once is fine - one per line. Line breaks inside a code do "
                          "not matter."),
     ("Click Save.", "It reports how many were added, and names any it refused and why."),
     ("Check Rater coverage.", "Confirm the people you expected are now listed."),
     ("Export a backup.", "Before you close the browser. Every time."),
    ]))
    F.append(Spacer(1, 4))
    F.append(table([
        ["A code is refused as damaged or cut short",
         "Reformatted in transit, usually autocorrect. Ask for it again as plain text."],
        ["A code is refused as the wrong questions",
         "Answered against an older version of the form. Ask them to redo it from the current link."],
        ["Someone submitted twice",
         "Same person, rater and date replaces the earlier one. A different date is kept as a "
         "second response and both get averaged in - Remove the stale one."],
    ], [2.4 * inch, 4.5 * inch], header=False, zebra=True))

    F.append(CondPageBreak(3.2 * inch))

    F.append(P("Backing up - the part that matters", "h"))
    F.append(P("Your results live in this browser on this machine. They survive closing the tab "
               "and restarting the Mac. They do <b>not</b> survive clearing your browsing data, "
               "and they do not follow you to another computer."))
    F.append(table([
        ["Export backup",
         "Writes one file containing <b>everything in your console</b> - all five people, plans, "
         "snapshots and readings. It names itself: "
         "<b>blossom-360_2026-08-26_1430_bryan.json</b>. Put it in the shared Google Drive folder."],
        ["Import backup",
         "<b>Replaces</b> everything in this browser with the file's contents. It never merges. "
         "It tells you how many responses are coming in - read that number before you confirm."],
    ], [1.3 * inch, 5.6 * inch], header=False))
    F.append(Spacer(1, 5))
    F.append(box("Export every time you finish entering codes",
                 "That is the only moment new data exists, which makes it the only moment a backup "
                 "is worth taking. Keep the dated files rather than replacing them - they are tiny."))
    F.append(Spacer(1, 4))
    F.append(box("One live console at a time",
                 "Bryan holds it and enters every code. John imports a copy to read results and "
                 "never exports. If both consoles are written to at once, one import silently "
                 "overwrites the other's work and nothing warns either of you.",
                 "Switching browser or machine? Import the newest backup from Drive before you "
                 "start, and export back to Drive when you finish."))

    F.append(P("Restoring after a wipe", "h"))
    F.append(numbered([
     ("Download the newest blossom-360_ file", "from the shared Drive folder - they sort oldest "
                                               "to newest."),
     ("Open the console", "in the browser you intend to keep using."),
     ("Click Import backup", "and choose that file."),
     ("Confirm.", "Check the response count it quotes looks right."),
     ("Spot-check a person,", "then export a fresh backup so this machine holds the current copy."),
    ]))

    F.append(P("The numbers, in one line each", "h"))
    F.append(table([
        ["Others", "Everyone except the person themselves. Their self-score never lifts their own "
                   "result."],
        ["Blind spot", "Self minus Others. Plus 1.00 or more means they rate themselves materially "
                       "higher than everyone else does."],
        ["Gap", "Importance x (5 - Others). How far short it falls, weighted by how much the role "
                "needs it."],
        ["Rank", "Gaps sorted. The top five become the development plan automatically."],
    ], [0.95 * inch, 5.95 * inch], header=False, zebra=True))

    F.append(Spacer(1, 5))
    F.append(P("Console: %s  -  Rater form: %s" % (CONSOLE_URL, FORM_URL), "small"))
    F.append(P("Fuller detail is in the Review Procedure Guide, in the same folder as this card.",
               "small"))
    return render(os.path.join(OUT_DIR, "ConsoleQuickReference.pdf"), F,
                  "Blossom 360 - Console Quick Reference")


if __name__ == "__main__":
    errs = validate()
    if errs:
        print("VALIDATION FAILED - not building:")
        for e in errs:
            print("  -", e)
        raise SystemExit(1)
    os.makedirs(OUT_DIR, exist_ok=True)
    print("saved:", rater_card())
    print("saved:", console_card())
