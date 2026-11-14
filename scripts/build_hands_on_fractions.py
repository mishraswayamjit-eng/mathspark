"""Author and verify the hands-on fraction lessons (pilot, Grades 4-5).

Writes src/data/handsOn/fractions.json. Run:  python scripts/build_hands_on_fractions.py

Every figure is a shape cut into pieces on a whole-number grid. A piece is worth
its area, so nothing about its value is typed by hand. Before the file is
written, this script proves that:
  - the pieces of each figure exactly fill its outline (no gap, no overlap in area),
  - every "colour n/d" task can be done with the pieces on screen,
  - every picture on an explanation screen shows exactly the fraction on its label,
  - no child-facing line uses a word the tone rule bans.
"""
import io
import json
import os
import re
from fractions import Fraction

OUT = os.path.join(os.path.dirname(__file__), "..", "src", "data", "handsOn", "fractions.json")


# ── Figures ──────────────────────────────────────────────────────────────────

def rect(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def grid(cols, rows, by_column=False):
    cells = []
    if by_column:
        for c in range(cols):
            for r in range(rows):
                cells.append(rect(c, r, c + 1, r + 1))
    else:
        for r in range(rows):
            for c in range(cols):
                cells.append(rect(c, r, c + 1, r + 1))
    return cells


def quadrant_triangles():
    out = []
    for (x, y) in [(0, 0), (2, 0), (0, 2), (2, 2)]:
        out.append([[x, y], [x + 2, y], [x + 2, y + 2]])
        out.append([[x, y], [x + 2, y + 2], [x, y + 2]])
    return out


FIGURES = {
    "bar4": {"w": 4, "h": 1, "pieces": grid(4, 1)},
    # Four equal parts of two different shapes.
    "sq4mix": {"w": 4, "h": 4, "pieces": [rect(0, 0, 2, 2), rect(0, 2, 2, 4), rect(2, 0, 3, 4), rect(3, 0, 4, 4)]},
    "sq8tri": {"w": 4, "h": 4, "pieces": quadrant_triangles()},
    "tri4": {
        "w": 4, "h": 4, "outline": [[0, 4], [4, 4], [2, 0]],
        "pieces": [[[2, 0], [3, 2], [1, 2]], [[0, 4], [2, 4], [1, 2]], [[2, 4], [4, 4], [3, 2]], [[1, 2], [3, 2], [2, 4]]],
    },
    "grid6": {"w": 3, "h": 2, "pieces": grid(3, 2)},
    # One half and two quarters.
    "half_q": {"w": 4, "h": 4, "pieces": [rect(0, 0, 2, 4), rect(2, 0, 4, 2), rect(2, 2, 4, 4)]},
    "sq4": {"w": 4, "h": 4, "pieces": [rect(0, 0, 2, 2), rect(0, 2, 2, 4), rect(2, 0, 4, 2), rect(2, 2, 4, 4)]},
    # A window: one long pane (worth three) above nine small panes.
    "window12": {"w": 3, "h": 4, "pieces": [rect(0, 0, 3, 1)] + [rect(c, r, c + 1, r + 1) for r in range(1, 4) for c in range(3)]},
    "window12split": {"w": 3, "h": 4, "pieces": grid(3, 4)},
    # Parts of three sizes: 4/8, 2/8, 1/8, 1/8.
    "sq8mix": {"w": 4, "h": 4, "pieces": [rect(0, 2, 4, 4), rect(0, 0, 2, 2), [[2, 0], [4, 0], [4, 2]], [[2, 0], [4, 2], [2, 2]]]},
    # Sixteenths: 8, 4, 2, 1, 1.
    "steps16": {"w": 4, "h": 4, "pieces": [rect(0, 2, 4, 4), rect(0, 0, 2, 2), rect(2, 0, 4, 1), rect(2, 1, 3, 2), rect(3, 1, 4, 2)]},
    "cols4": {"w": 4, "h": 2, "pieces": [rect(c, 0, c + 1, 2) for c in range(4)]},
    "grid8": {"w": 4, "h": 2, "pieces": grid(4, 2, by_column=True)},
    "grid12": {"w": 4, "h": 3, "pieces": grid(4, 3, by_column=True)},
    "bar10": {"w": 5, "h": 2, "pieces": grid(5, 2, by_column=True)},
}


# ── Lessons ──────────────────────────────────────────────────────────────────

def do(figure, n, d, prompt, say, why):
    return {"kind": "do", "figure": figure, "target": [n, d], "prompt": prompt, "say": say, "why": why}


def see(text, say, show):
    return {"kind": "see", "text": text, "say": say,
            "show": [{"figure": f, "shaded": s, "label": lab} for (f, s, lab) in show]}


def check(figure, n, d, prompt, why):
    return {"kind": "check", "figure": figure, "target": [n, d], "prompt": prompt, "why": why}


LESSONS = [
    {
        "id": "fr-equal-parts",
        "title": "Equal parts",
        "blurb": "What the top and bottom numbers of a fraction count",
        "grades": [4, 5],
        "screens": [
            do("bar4", 1, 4, "Colour 1/4 of the bar.",
               "Tap a part to colour it. Tap it again to clear it.",
               "The bar is cut into 4 equal parts. One of those parts is 1/4 of the bar."),
            do("bar4", 3, 4, "Colour 3/4 of the bar.",
               "Same bar. This time, take three parts.",
               "Each part is 1/4 of the bar. Three of them make 3/4."),
            do("sq4mix", 2, 4, "Colour 2/4 of the square.",
               "These parts have different shapes. Look at their sizes.",
               "A small square and a tall strip cover the same amount of the big square. Each is 1/4, so any two parts make 2/4."),
            see("Parts can have different shapes and still be equal. Every part here is 1/4 of the square, so any two of them make 2/4.",
                "Three ways to colour it, and every one is 2/4.",
                [("sq4mix", [0, 1], "2/4"), ("sq4mix", [0, 2], "2/4"), ("sq4mix", [2, 3], "2/4")]),
            do("sq8tri", 3, 8, "Colour 3/8 of the square.",
               "Now the square is cut into 8 equal parts.",
               "The square is cut into 8 equal triangles. Any three of them make 3/8."),
            do("sq8tri", 5, 8, "Colour 5/8 of the square.",
               "It does not matter which five you choose.",
               "Five of the 8 equal parts make 5/8, wherever they sit in the square."),
            see("The bottom number says how many equal parts make the whole. The top number says how many of them you take.",
                "That is all a fraction is.",
                [("bar4", [0, 1, 2], "3/4"), ("sq8tri", [0, 1, 2, 3, 4], "5/8")]),
            check("tri4", 3, 4, "Colour 3/4 of the triangle.",
                  "The big triangle is cut into 4 equal small triangles. Three of them make 3/4."),
            check("grid6", 5, 6, "Colour 5/6 of the rectangle.",
                  "There are 6 equal parts. Five of them make 5/6."),
            check("sq8tri", 7, 8, "Colour 7/8 of the square.",
                  "There are 8 equal parts. Seven of them make 7/8, so only one part stays white."),
        ],
    },
    {
        "id": "fr-big-and-small-parts",
        "title": "Big parts and small parts",
        "blurb": "Find a fraction when the parts are different sizes",
        "grades": [4, 5],
        "screens": [
            do("half_q", 1, 4, "Colour 1/4 of the square.",
               "This square has one big part and two small ones.",
               "Four of the small squares would fill the whole square, so one small square is 1/4."),
            do("half_q", 3, 4, "Colour 3/4 of the square.",
               "You will need the big part this time. How much is it worth?",
               "The big part is the same size as two small squares, so it is worth 2/4. With one small square, that makes 3/4."),
            see("Cut the big part into two equal pieces and you can count them: 3 of the 4 equal parts are coloured.",
                "Here is what you just did.",
                [("half_q", [0, 1], "3/4"), ("sq4", [0, 1, 2], "3/4")]),
            do("window12", 5, 12, "Colour 5/12 of the window.",
               "Look at the small panes first. How many of them would fill the whole window?",
               "Twelve small panes would fill the window, so each one is 1/12. The long pane at the top is the size of 3 small panes, so it is worth 3/12."),
            do("window12", 1, 4, "Colour 1/4 of the window.",
               "There is more than one way to do this one.",
               "1/4 of 12 panes is 3 panes. You can colour three small panes, or the long pane, which is the same size as three."),
            see("3/12 and 1/4 cover the same amount of the window. Fractions that name the same amount are called equivalent fractions.",
                "Same amount, two names.",
                [("window12", [0], "1/4"), ("window12split", [0, 1, 2], "3/12")]),
            do("sq8mix", 3, 8, "Colour 3/8 of the square.",
               "Parts of three sizes now. Start with the smallest: what fraction is one triangle?",
               "Think in eighths. Each triangle is 1/8, the small square is 2/8 and the long part is 4/8. The small square and one triangle make 3/8."),
            see("When the parts are different sizes, ask how many of the smallest part would fill the whole. Then count in those.",
                "That works for any shape.",
                [("sq8mix", [1, 2], "3/8"), ("sq8tri", [0, 1, 2], "3/8")]),
            check("steps16", 3, 16, "Colour 3/16 of the square.",
                  "Sixteen of the smallest squares would fill the whole square, so each is 1/16. The parts are worth 8, 4, 2, 1 and 1 sixteenths. A 2 and a 1 make 3/16."),
            check("steps16", 9, 16, "Colour 9/16 of the square.",
                  "The biggest part is 8/16. One of the smallest squares makes it 9/16."),
            check("steps16", 3, 4, "Colour 3/4 of the square.",
                  "3/4 of 16 is 12, so we need 12/16. The 8/16 part and the 4/16 part together make 12/16."),
        ],
    },
    {
        "id": "fr-same-amount",
        "title": "Same amount, different names",
        "blurb": "Meet equivalent fractions by colouring them",
        "grades": [4, 5],
        "screens": [
            do("grid8", 1, 2, "Colour 1/2 of the rectangle.",
               "There are 8 equal parts here and no halves marked. Can you still do it?",
               "Half of 8 parts is 4 parts, so 4/8 is the same amount as 1/2."),
            do("grid8", 1, 4, "Colour 1/4 of the rectangle.",
               "Now a quarter of the same rectangle.",
               "A quarter of 8 parts is 2 parts, so 2/8 is the same amount as 1/4."),
            do("grid8", 3, 4, "Colour 3/4 of the rectangle.",
               "Each quarter is two parts. So three quarters is...",
               "Each quarter is 2 parts, so three quarters is 6 parts. 3/4 is the same amount as 6/8."),
            see("3/4 and 6/8 are the same amount. Multiply the top and the bottom of 3/4 by 2 and you get 6/8.",
                "Every part was cut in two, so there are twice as many parts and you take twice as many.",
                [("cols4", [0, 1, 2], "3/4"), ("grid8", [0, 1, 2, 3, 4, 5], "6/8")]),
            do("grid12", 2, 3, "Colour 2/3 of the rectangle.",
               "Twelve parts this time. First find one third.",
               "One third of 12 parts is 4 parts, so two thirds is 8 parts. 2/3 is the same amount as 8/12."),
            do("grid12", 5, 6, "Colour 5/6 of the rectangle.",
               "One sixth of 12 parts is how many parts?",
               "One sixth of 12 parts is 2 parts, so five sixths is 10 parts. 5/6 is the same amount as 10/12."),
            see("To give a fraction a different bottom number, multiply or divide the top and the bottom by the same number. The amount stays the same.",
                "The shape never changed. Only the name did.",
                [("grid12", [0, 1, 2, 3, 4, 5, 6, 7], "2/3 = 8/12"), ("grid12", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "5/6 = 10/12")]),
            check("bar10", 2, 5, "Colour 2/5 of the rectangle.",
                  "One fifth of 10 parts is 2 parts, so two fifths is 4 parts. 2/5 is the same amount as 4/10."),
            check("grid12", 3, 4, "Colour 3/4 of the rectangle.",
                  "One quarter of 12 parts is 3 parts, so three quarters is 9 parts. 3/4 is the same amount as 9/12."),
            check("bar10", 1, 2, "Colour 1/2 of the rectangle.",
                  "Half of 10 parts is 5 parts. 1/2 is the same amount as 5/10."),
        ],
    },
]


# ── Verification ─────────────────────────────────────────────────────────────

def area2(points):
    """Twice the area of a polygon: a whole number when the corners are on the grid."""
    total = 0
    for i in range(len(points)):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % len(points)]
        total += x0 * y1 - x1 * y0
    return abs(total)


def reachable(values, goal):
    sums = {0}
    for v in values:
        sums |= {s + v for s in sums if s + v <= goal}
    return goal in sums


BANNED = re.compile(r"\b(wrong|incorrect|failed|fail|error)\b", re.I)


def verify():
    problems = []
    areas = {}
    for name, fig in FIGURES.items():
        outline = fig.get("outline") or rect(0, 0, fig["w"], fig["h"])
        parts = [area2(p) for p in fig["pieces"]]
        if min(parts) <= 0:
            problems.append("%s: a piece has no area" % name)
        if sum(parts) != area2(outline):
            problems.append("%s: pieces cover %s, outline is %s" % (name, sum(parts), area2(outline)))
        for piece in fig["pieces"]:
            for (x, y) in piece:
                if not (0 <= x <= fig["w"] and 0 <= y <= fig["h"]):
                    problems.append("%s: corner outside the figure" % name)
        areas[name] = parts

    ids = set()
    for lesson in LESSONS:
        if lesson["id"] in ids:
            problems.append("duplicate lesson id %s" % lesson["id"])
        ids.add(lesson["id"])
        kinds = [s["kind"] for s in lesson["screens"]]
        first_check = kinds.index("check") if "check" in kinds else len(kinds)
        if "check" not in kinds or any(k != "check" for k in kinds[first_check:]):
            problems.append("%s: skill-check screens must come last" % lesson["id"])
        for i, screen in enumerate(lesson["screens"]):
            where = "%s screen %d" % (lesson["id"], i + 1)
            for key in ("prompt", "say", "why", "text"):
                if key in screen and BANNED.search(screen[key]):
                    problems.append("%s: banned word in %s" % (where, key))
            if screen["kind"] in ("do", "check"):
                parts = areas.get(screen["figure"])
                if parts is None:
                    problems.append("%s: unknown figure" % where)
                    continue
                n, d = screen["target"]
                goal = Fraction(n, d) * sum(parts)
                if not (0 < n < d) or goal.denominator != 1 or not reachable(parts, int(goal)):
                    problems.append("%s: %d/%d cannot be coloured on %s" % (where, n, d, screen["figure"]))
                if "%d/%d" % (n, d) not in screen["prompt"]:
                    problems.append("%s: prompt does not name %d/%d" % (where, n, d))
            else:
                for item in screen["show"]:
                    parts = areas.get(item["figure"])
                    if parts is None:
                        problems.append("%s: unknown figure" % where)
                        continue
                    if len(set(item["shaded"])) != len(item["shaded"]) or any(k >= len(parts) for k in item["shaded"]):
                        problems.append("%s: bad shaded list" % where)
                        continue
                    shown = Fraction(sum(parts[k] for k in item["shaded"]), sum(parts))
                    for (a, b) in re.findall(r"(\d+)/(\d+)", item["label"]):
                        if Fraction(int(a), int(b)) != shown:
                            problems.append("%s: label %s/%s but picture shows %s" % (where, a, b, shown))
    return problems


def main():
    problems = verify()
    if problems:
        for p in problems:
            print("PROBLEM:", p)
        raise SystemExit(1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"topic": "Fractions", "figures": FIGURES, "lessons": LESSONS}, f, ensure_ascii=False, indent=1)
        f.write("\n")
    tasks = sum(1 for l in LESSONS for s in l["screens"] if s["kind"] != "see")
    print("verified %d figures, %d lessons, %d tasks -> %s" % (len(FIGURES), len(LESSONS), tasks, os.path.normpath(OUT)))


if __name__ == "__main__":
    main()
