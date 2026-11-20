"""Rule-made lessons for the generated families in Grade 4 quadrilaterals.

Four wordings, one rule each: area of a rectangle, perimeter of a rectangle, area of a
square, perimeter of a square. Every line on the board is computed from the question's
numbers.
"""
import re

from g4_gr4_quads_lib import A, B, FIG, G, L, W, ask, figures, hpick, lesson, mark, note, ring

FIGS = figures("gr4_quads")

RECT_A = re.compile(r"^Find the (area|perimeter) of a rectangle with length (\d+) cm and (width|breadth) (\d+) cm\.$")
RECT_B = re.compile(r"^A rectangle is (\d+) cm long and (\d+) cm wide\. What is its (area|perimeter)\?$")
SQ_A = re.compile(r"^Find the (area|perimeter) of a square with side (\d+) cm\.$")
SQ_B = re.compile(r"^Each side of a square is (\d+) cm long\. What is the (area|perimeter) of the square\?$")


def fig_op(qid):
    spec = (FIGS.get(qid) or {}).get("figure")
    return [FIG("f1", spec)] if spec else []


def mult_beats(qid, a, b):
    """Beats that work out a × b on the board, in steps a 9-year-old can follow."""
    p = a * b
    if a <= 10 and b <= 10:
        if b <= 3 and b >= 2:
            rows = " + ".join([str(a)] * b)
            said = " plus ".join([str(a)] * b)
            return [B("%d times %d means %d lots of %d. %s makes %d." % (a, b, b, a, said, p),
                      W("m1", "%d × %d = %s" % (a, b, rows)), W("m2", "%s = %d" % (rows, p)))]
        return [B(hpick(qid, "tt", [
            "%d times %d is %d. That one is straight from the times tables." % (a, b, p),
            "From the times tables, %d times %d is %d." % (a, b, p)]),
            W("m1", "%d × %d = %d" % (a, b, p)))]
    if b == 10 or a == 10:
        other = a if b == 10 else b
        return [B("%d times %d is %d tens, and %d tens is %d." % (a, b, other, other, p),
                  W("m1", "%d × %d = %d" % (a, b, p)))]
    if b % 10 == 0:
        t = b // 10
        x = a * t
        return [
            B("%d is %d tens. So first we find %d times %d. That is %d." % (b, t, a, t, x),
              W("m1", "%d × %d = %d" % (a, t, x))),
            B("%d times %d is 10 times as big as that. So it is %d." % (a, b, p),
              W("m2", "%d × %d = %d" % (a, b, p)), note("m2", str(b), "%d tens" % t, "below")),
        ]
    if a % 10 == 0 and b <= 10:
        t = a // 10
        x = t * b
        return [
            B("%d is %d tens. So first we find %d times %d. That is %d." % (a, t, t, b, x),
              W("m1", "%d × %d = %d" % (t, b, x))),
            B("%d times %d is 10 times as big as that. So it is %d." % (a, b, p),
              W("m2", "%d × %d = %d" % (a, b, p)), note("m2", str(a), "%d tens" % t, "below")),
        ]
    # Split the bigger number into tens and ones.
    if b > 10:
        s, tens, ones = b, b - b % 10, b % 10
        p1, p2 = "%d × %d" % (a, tens), "%d × %d" % (a, ones)
        w1, w2 = "%d times %d" % (a, tens), "%d times %d" % (a, ones)
        x, y = a * tens, a * ones
    else:
        s, tens, ones = a, a - a % 10, a % 10
        p1, p2 = "%d × %d" % (tens, b), "%d × %d" % (ones, b)
        w1, w2 = "%d times %d" % (tens, b), "%d times %d" % (ones, b)
        x, y = tens * b, ones * b
    head = "%d × %d = " % (a, b)
    line = head + "%s + %s" % (p1, p2)
    # The number being split is the first or second number of "a × b".
    nth = ("%d × " % a).count(str(s)) + 1 if b > 10 else 1
    open_say = hpick(qid, "split", [
        "%d times %d is a big sum, so let's break it into two easy ones. Split %d into %d and %d." % (a, b, s, tens, ones),
        "%d times %d looks hard, but we can do it in two small parts. Think of %d as %d and %d." % (a, b, s, tens, ones),
        "Let's make %d times %d easier. We split %d into %d and %d, and do one part at a time." % (a, b, s, tens, ones),
    ])
    slips = []
    for cand in (p + 10, p - 10, p + 100, x):
        if cand > 0 and cand != p and str(cand) not in slips and len(slips) < 2:
            slips.append(str(cand))
    return [
        B(open_say, W("m1", line), note("m1", str(s), "%d + %d" % (tens, ones), "below", nth if nth > 1 else None)),
        B("%s is %d. And %s is %d. Now we put the two parts together. What is %d plus %d?" % (w1, x, w2, y, x, y),
          W("m2", "%s = %d" % (p1, x)), W("m3", "%s = %d" % (p2, y)),
          ask=ask(qid + "add", str(p), slips,
                  "Take it slowly, one place at a time. Let's write it down together.")),
        B(hpick(qid, "sum", ["%d plus %d makes %d.", "Add them up: %d plus %d is %d."]) % (x, y, p),
          W("m4", "%d + %d = %d" % (x, y, p))),
    ]


def rect_area(q, ln, wd, word):
    qid = q["id"]
    p = ln * wd
    adj = "wide" if word == "width" else "broad"
    beats = [
        B(hpick(qid, "open", [
            "Here is our rectangle. It is %d centimetres long and %d centimetres %s, and we want its area.",
            "Look at this rectangle: %d centimetres long and %d centimetres %s. Our job is to find its area.",
            "We have a rectangle, %d centimetres long and %d centimetres %s. How much space is inside it?",
        ]) % (ln, wd, adj),
            G("Rectangle: length %d cm, %s %d cm. Area = ?" % (ln, word, wd)), *fig_op(qid)),
        B("Area means the space inside. Picture the rectangle filled with little squares, each 1 centimetre wide. Which sum counts them all?",
          ask=ask(qid + "how", "%d × %d" % (ln, wd), ["%d + %d" % (ln, wd), "2 × (%d + %d)" % (ln, wd)],
                  "Adding the sides measures along the edges, not the inside. The little squares sit in %d rows of %d, so we multiply %d by %d." % (wd, ln, ln, wd))),
        B(hpick(qid, "why", [
            "The squares sit in %d rows, with %d in every row. So the area is length times %s." % (wd, ln, word),
            "There are %d rows of squares, and %d squares in each row. That is why area is length times %s." % (wd, ln, word),
        ]), L("f", "Area = length × %s" % word), mark("f", "×", "circle")),
    ]
    beats += mult_beats(qid, ln, wd)
    beats += [
        B(hpick(qid, "ans", [
            "So the area is %d square centimetres. We say square centimetres because we counted little squares.",
            "There it is: the area is %d square centimetres. Square centimetres, because area is counted in little squares.",
        ]) % p, A("a", "Area = %d cm²" % p, label=True), ring("a", str(p))),
        B("Let's check by going backwards. %d squares shared into %d rows gives %d in each row. It fits!" % (p, wd, ln),
          W("c", "%d ÷ %d = %d" % (p, wd, ln))),
        B(hpick(qid, "sum2", [
            "So, for the area of any rectangle: multiply the length by the %s, and give the answer in square units.",
            "Remember the plan. For area we multiply length by %s. Adding the sides is for the distance round the edge.",
        ]) % word),
    ]
    return lesson(beats, "rule")


def rect_perimeter(q, ln, wd, word):
    qid = q["id"]
    s = ln + wd
    p = 2 * s
    walk = "%d + %d + %d + %d" % (ln, wd, ln, wd)
    adj = "wide" if word == "width" else "broad"
    beats = [
        B(hpick(qid, "open", [
            "Here is our rectangle. It is %d centimetres long and %d centimetres %s, and we want its perimeter.",
            "Look at this rectangle: %d centimetres long and %d centimetres %s. Our job is to find its perimeter.",
            "We have a rectangle, %d centimetres long and %d centimetres %s. How far is it all the way round?",
        ]) % (ln, wd, adj),
            G("Rectangle: length %d cm, %s %d cm. Perimeter = ?" % (ln, word, wd)), *fig_op(qid)),
        B(hpick(qid, "ant", [
            "Perimeter is the distance all the way round the edge. Imagine an ant walking round the rectangle until it is back where it started.",
            "Perimeter means the distance right round the outside. Picture yourself walking along every edge, back to the start.",
        ]), L("f", "Perimeter = all the way round"), mark("f", "all the way round")),
        B("The walk goes along a length, then a %s, then another length and another %s. Which sum gives the whole walk?" % (word, word),
          ask=ask(qid + "how", walk, ["%d + %d" % (ln, wd), "%d × %d" % (ln, wd)],
                  "Look at the picture again. A rectangle has four sides: two lengths and two %ss. The walk must go along all four of them." % word)),
        B("Let's add one length and one %s first. %d plus %d is %d." % (word, ln, wd, s),
          W("l1", "%d + %d = %d" % (ln, wd, s))),
        B(hpick(qid, "trap", [
            "Careful: %d is only halfway round. There are two lengths and two %ss, so we double it. 2 times %d is %d." % (s, word, s, p),
            "Don't stop at %d. That is just one length and one %s, halfway round. Double it: 2 times %d is %d." % (s, word, s, p),
        ]), note("l1", str(s), "halfway round", "below"), W("l2", "2 × %d = %d" % (s, p))),
        B(hpick(qid, "ans", [
            "So the perimeter is %d centimetres. Plain centimetres this time, because a perimeter is a distance.",
            "There it is: the perimeter is %d centimetres. It is a length, so the unit is just centimetres.",
        ]) % p, A("a", "Perimeter = %d cm" % p, label=True), ring("a", str(p))),
        B("Let's check by walking all four sides, one at a time. %d, %d, %d, %d. Together they make %d." % (ln, wd, ln, wd, p),
          W("c", "%s = %d" % (walk, p))),
        B(hpick(qid, "sum2", [
            "So, for the perimeter of any rectangle: add the length and the %s, then double.",
            "Remember the plan. Length plus %s takes you halfway round. Double it for the whole perimeter.",
        ]) % word),
    ]
    return lesson(beats, "rule")


def square_area(q, s):
    qid = q["id"]
    p = s * s
    beats = [
        B(hpick(qid, "open", [
            "Here is our square. Each side is %d centimetres long, and we want its area.",
            "Look at this square. Every side is %d centimetres. Our job is to find its area.",
            "We have a square with sides of %d centimetres. How much space is inside it?",
        ]) % s, G("Square: side %d cm. Area = ?" % s), *fig_op(qid)),
        B("Area means the space inside. Picture the square filled with little squares, each 1 centimetre wide. Which sum counts them all?",
          ask=ask(qid + "how", "%d × %d" % (s, s) if s != 4 else "4 rows of 4",
                  ["4 × %d" % s, "%d + %d" % (s, s)] if s != 4 else ["4 + 4", "4 + 4 + 4"],
                  ("4 times the side goes round the edge. That is the perimeter. " if s != 4 else "Adding sides goes along the edge. ")
                  + "The little squares inside sit in %d rows of %d, so we multiply %d by %d." % (s, s, s, s))),
        B(hpick(qid, "why", [
            "A square is as wide as it is long. So there are %d rows, with %d little squares in every row. The area is side times side." % (s, s),
            "In a square the length and the width are the same. That gives %d rows of %d little squares. So area is side times side." % (s, s),
        ]), L("f", "Area = side × side"), mark("f", "×", "circle")),
    ]
    beats += mult_beats(qid, s, s)
    beats += [
        B(hpick(qid, "ans", [
            "So the area is %d square centimetres. We say square centimetres because we counted little squares.",
            "There it is: the area is %d square centimetres. Square centimetres, because area is counted in little squares.",
        ]) % p, A("a", "Area = %d cm²" % p, label=True), ring("a", str(p))),
        B("Let's check by going backwards. %d squares shared into %d rows gives %d in each row. It fits!" % (p, s, s),
          W("c", "%d ÷ %d = %d" % (p, s, s))),
        B(hpick(qid, "sum2", [
            "So, for the area of any square: multiply the side by itself, and give the answer in square units.",
            "Remember the plan. Side times side is the area. 4 times the side is the perimeter. Don't mix them up!",
        ])),
    ]
    return lesson(beats, "rule")


def square_perimeter(q, s):
    qid = q["id"]
    p = 4 * s
    walk = " + ".join([str(s)] * 4)
    beats = [
        B(hpick(qid, "open", [
            "Here is our square. Each side is %d centimetres long, and we want its perimeter.",
            "Look at this square. Every side is %d centimetres. Our job is to find its perimeter.",
            "We have a square with sides of %d centimetres. How far is it all the way round?",
        ]) % s, G("Square: side %d cm. Perimeter = ?" % s), *fig_op(qid)),
        B(hpick(qid, "ant", [
            "Perimeter is the distance all the way round the edge. Imagine an ant walking round the square until it is back where it started.",
            "Perimeter means the distance right round the outside. Picture yourself walking along every edge, back to the start.",
        ]), L("f", "Perimeter = all the way round"), mark("f", "all the way round")),
        B("A square has 4 sides, and they are all the same length. So which sum gives the whole walk?",
          ask=ask(qid + "how", "4 × %d" % s if s != 4 else "4 + 4 + 4 + 4",
                  ["%d × %d" % (s, s), "2 × %d" % s] if s != 4 else ["4 + 4", "4 + 4 + 4"],
                  "Count the sides of the square in the picture. There are 4 of them, each %d centimetres. So the walk is 4 lots of %d." % (s, s))),
        B("4 equal sides, so the perimeter is 4 times the side.", L("g", "Perimeter = 4 × side"), mark("g", "4", "circle")),
    ]
    if s <= 10:
        beats.append(B(hpick(qid, "tt4", [
            "4 lots of %d. From the times tables, 4 times %d is %d." % (s, s, p),
            "That is 4 lots of %d, and 4 times %d is %d." % (s, s, p)]),
            W("m1", "4 × %d = %d" % (s, p))))
    else:
        beats += mult_beats(qid, 4, s)
    beats += [
        B(hpick(qid, "ans", [
            "So the perimeter is %d centimetres. Plain centimetres, because a perimeter is a distance.",
            "There it is: the perimeter is %d centimetres. It is a length, so the unit is just centimetres.",
        ]) % p, A("a", "Perimeter = %d cm" % p, label=True), ring("a", str(p))),
        B("Let's check by walking the four sides one at a time. %s. Together they make %d." % (", ".join([str(s)] * 4), p),
          W("c", "%s = %d" % (walk, p))),
        B(hpick(qid, "sum2", [
            "So, for the perimeter of any square: multiply the side by 4.",
            "Remember the plan. 4 times the side is the perimeter. Side times side is the area. Don't mix them up!",
        ])),
    ]
    return lesson(beats, "rule")


def family(q):
    text = q["questionText"].strip()
    m = RECT_A.match(text)
    if m:
        kind, ln, word, wd = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
        return rect_area(q, ln, wd, word) if kind == "area" else rect_perimeter(q, ln, wd, word)
    m = RECT_B.match(text)
    if m:
        ln, wd, kind = int(m.group(1)), int(m.group(2)), m.group(3)
        return rect_area(q, ln, wd, "width") if kind == "area" else rect_perimeter(q, ln, wd, "width")
    m = SQ_A.match(text)
    if m:
        return square_area(q, int(m.group(2))) if m.group(1) == "area" else square_perimeter(q, int(m.group(2)))
    m = SQ_B.match(text)
    if m:
        return square_area(q, int(m.group(1))) if m.group(2) == "area" else square_perimeter(q, int(m.group(1)))
    return None


RULES = [family]
