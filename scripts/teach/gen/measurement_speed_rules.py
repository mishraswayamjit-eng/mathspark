"""Lessons by rule for the generated measurement-speed families.

Each rule takes a question and the regex match on its text and returns a lesson.
RULES at the bottom lists (pattern, rule). Run measurement_speed_build.py to write the part.
"""
import re

from measurement_speed_lib import (answer, beat, choose, fig, given, lab, lesson, mark, note, pick, ring, w)


# ── Bags: "N bags, each K kg G g. Total weight in grams?" ────────────────────

def bags(q, m):
    qid = q["id"]
    name, n, item, K, G = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
    kg_g = K * 1000
    one = kg_g + G
    a, b = n * kg_g, n * G
    total = a + b
    weight = "%d kg %d g" % (K, G)

    def bar(piece):
        return {"kind": "barModel",
                "bars": [{"segments": [{"units": 1, "label": piece} for _ in range(n)], "brace": "? grams"}],
                "note": "Each bag weighs %s" % weight}

    beats = []
    beats.append(beat(
        pick(qid, "open", [
            "%s has %d bags of %s, and each bag weighs %d kilograms %d grams. We want the weight of all the bags together, in grams." % (name, n, item, K, G),
            "Here are %d bags of %s. Every bag weighs %d kilograms %d grams, and %s wants the total weight in grams." % (n, item, K, G, name),
            "%d bags of %s, each one %d kilograms %d grams. Our job is to find what they weigh altogether, in grams." % (n, item, K, G),
        ]),
        given("q1", "%d bags of %s, each %s" % (n, item, weight)),
        given("q2", "Total weight = ? grams"),
        fig("f1", bar(weight if n <= 3 else "1 bag")),
    ))
    beats.append(beat(
        pick(qid, "units", [
            "Look at how one bag is written: kilograms and grams mixed together. The answer must be in grams, so we change the kilograms. How many grams make 1 kilogram?",
            "One bag is written in two units at once, kilograms and grams, and those do not mix. We want grams, so let's turn the kilograms into grams. How many grams are in 1 kilogram?",
        ]),
        mark("q1", "%d kg" % K),
        ask=choose(qid + "a1", "1000 grams", ["100 grams", "10 grams"],
                   "Kilo means a thousand. So 1 kilogram is 1000 grams."),
    ))
    beats.append(beat(
        pick(qid, "why", [
            "1 kilogram is 1000 grams. A gram is much smaller than a kilogram, so we need many more of them: that is why we multiply. %d times 1000 is %d grams." % (K, kg_g),
            "Grams are tiny next to kilograms, so the number has to grow: we multiply by 1000. %d kilograms is %d times 1000, which is %d grams." % (K, K, kg_g),
        ]),
        lab("f", "1 kg = 1000 g"),
        w("c1", "%d × 1000 = %d" % (K, kg_g)),
    ))
    beats.append(beat(
        pick(qid, "one", [
            "Now put back the %d grams that were already there. %d plus %d makes %d grams. That is one bag, all in grams." % (G, kg_g, G, one),
            "Do not lose the %d grams that came with it. %d plus %d is %d grams, so now one bag is written in a single unit." % (G, kg_g, G, one),
        ]),
        w("c2", "%d + %d = %d" % (kg_g, G, one)),
        lab("c3", "1 bag = %d g" % one),
        mark("c3", "%d g" % one, "box"),
        fig("f1", bar("%d g" % one)),
    ))
    beats.append(beat(
        "Every bag weighs %d grams, and there are %d of them. What shall we work out?" % (one, n),
        ask=choose(qid + "a2", "%d × %d" % (one, n), ["%d + %d" % (one, n), "%d × %d" % (kg_g, n)],
                   "There are %d bags, and each one is the full %d grams. So we need %d lots of %d: a multiplication." % (n, one, n, one)),
    ))
    if n == 2:
        split = "Doubling is easiest in two pieces. Double %d is %d, and double %d is %d." % (kg_g, a, G, b)
    else:
        split = pick(qid, "split", [
            "Let's multiply in two easy pieces. %d times %d is %d, and %d times %d is %d." % (n, kg_g, a, n, G, b),
            "A big multiplication is easier in two pieces. First %d times %d, which is %d. Then %d times %d, which is %d." % (n, kg_g, a, n, G, b),
        ])
    beats.append(beat(
        split,
        w("m0", "%d × %d = ?" % (one, n)),
        w("m1", "%d × %d = %d" % (n, kg_g, a)),
        w("m2", "%d × %d = %d" % (n, G, b)),
    ))
    beats.append(beat(
        "Add the two pieces: %d plus %d is %d. So the %d bags together weigh %d grams." % (a, b, total, n, total),
        w("m3", "%d + %d = %d" % (a, b, total)),
        answer("ans", "Total weight = %d g" % total),
        ring("ans", "%d g" % total),
    ))
    beats.append(beat(
        pick(qid, "check", [
            "Does that make sense? The kilograms alone gave %d grams, and our answer is a little more, because every bag has %d extra grams. Forgetting those extra grams is the slip to watch for." % (a, G),
            "Quick sense check. The kilograms on their own came to %d grams. Our %d is a bit bigger, thanks to the extra %d grams in every bag. Leaving those out is the classic slip." % (a, total, G),
        ]),
        mark("m1", "%d" % a, nth=(2 if ("%d" % a) in ("%d × %d" % (n, kg_g)) else None)),
    ))
    beats.append(beat(pick(qid, "sum", [
        "So the plan for mixed units: first write one bag in a single unit, here grams. Then multiply by the number of bags.",
        "Remember the order: get everything into one unit first, then do the multiplying. Units first, sums second.",
        "That is the whole method. Change the kilograms into grams, add the loose grams, then multiply by how many bags there are.",
    ])))
    return lesson("rule", beats)


# ── Glasses: "A drum holds V litres. How many glasses of g ml can be filled?" ─

def glasses(q, m):
    qid = q["id"]
    tub, V, g = m.group(1), int(m.group(2)), int(m.group(3))
    total = V * 1000
    n, left = divmod(total, g)

    beats = []
    beats.append(beat(
        pick(qid, "open", [
            "A %s holds %d litres of water, and each glass takes %d millilitres. How many glasses can we fill?" % (tub, V, g),
            "We have a %s with %d litres of water in it, and glasses that hold %d millilitres each. Let's find how many glasses it fills." % (tub, V, g),
        ]),
        given("q1", "%s: %d litres. Each glass: %d ml." % (tub.capitalize(), V, g)),
        given("q2", "Number of glasses = ?"),
        fig("f1", {"kind": "barModel", "bars": [{
            "segments": [{"units": 1, "label": "%d ml" % g}, {"units": 1, "label": "%d ml" % g},
                         {"units": 1, "label": "%d ml" % g}, {"units": 2, "label": "... ?", "tone": "unknown"}],
            "brace": "%d litres" % V}]}),
    ))
    beats.append(beat(
        pick(qid, "units", [
            "Look at the units first. The %s is in litres, the glass is in millilitres, and those two do not mix. Which shall we change?" % tub,
            "Before any sums, check the units. Litres for the %s, millilitres for the glass. They do not mix, so one of them has to change. Which one?" % tub,
        ]),
        mark("q1", "litres"), mark("q1", "ml"),
        ask=choose(qid + "a1", "change the litres into millilitres",
                   ["change the millilitres into litres", "leave them and divide %d by %d" % (V, g)],
                   "We can only compare amounts that are in the same unit. Changing the litres into millilitres keeps every number whole, so that is the friendly choice."),
    ))
    beats.append(beat(
        pick(qid, "why", [
            "1 litre is 1000 millilitres. A millilitre is much smaller, so we need many more of them, and that means multiply. %d times 1000 is %d millilitres." % (V, total),
            "Each litre is 1000 millilitres. Smaller unit, so more of them: we multiply by 1000. %d times 1000 gives %d millilitres in the %s." % (V, total, tub),
        ]),
        lab("f", "1 litre = 1000 ml"),
        w("c1", "%d × 1000 = %d" % (V, total)),
        lab("c2", "%d litres = %d ml" % (V, total)),
        mark("c2", "%d ml" % total, "box"),
    ))

    if left == 0:
        beats.append(beat(
            "Now both amounts are in millilitres. How do we find how many %d millilitre glasses fit into %d millilitres?" % (g, total),
            ask=choose(qid + "a2", "%d ÷ %d" % (total, g), ["%d × %d" % (total, g), "%d − %d" % (total, g)],
                       "We are sharing the water out into equal glasses. Finding how many equal groups fit is a division."),
        ))
        if 1000 % g == 0:
            per = 1000 // g
            beats.append(beat(
                pick(qid, "fact", [
                    "Dividing by %d is easy with one friendly fact: %d glasses of %d millilitres make exactly 1000. So every litre fills %d glasses." % (g, per, g, per),
                    "Here is a friendly fact to help. %d times %d is exactly 1000, so each litre of water fills %d glasses." % (g, per, per),
                ]),
                w("d0", "%d ÷ %d = ?" % (total, g)),
                w("d1", "%d × %d = 1000" % (g, per)),
                note("d1", "1000", "1 litre", "below"),
            ))
            beats.append(beat(
                "There are %d litres, with %d glasses from each one. %d times %d is %d. So %d glasses can be filled." % (V, per, V, per, n, n),
                w("d2", "%d × %d = %d" % (V, per, n)),
                w("d3", "%d ÷ %d = %d" % (total, g, n)),
                answer("ans", "%d glasses" % n),
                ring("ans", "%d glasses" % n),
            ))
        else:
            T, G = total // 100, g // 100
            beats.append(beat(
                "Both numbers end in two zeros, so we can make the division smaller. Take two zeros off each: %d divided by %d is the same as %d divided by %d." % (total, g, T, G),
                w("d1", "%d ÷ %d = %d ÷ %d" % (total, g, T, G)),
                mark("d1", "%d" % T, nth=2), mark("d1", "%d" % G, nth=2),
            ))
            beats.append(beat(
                "%d divided by %d is %d. So %d glasses can be filled." % (T, G, n, n),
                w("d2", "%d ÷ %d = %d" % (T, G, n)),
                answer("ans", "%d glasses" % n),
                ring("ans", "%d glasses" % n),
            ))
        beats.append(beat(
            "Check by pouring it back. %d glasses of %d millilitres is %d times %d, which is %d millilitres. That is the whole %s, with nothing left over." % (n, g, n, g, total, tub),
            w("chk", "%d × %d = %d" % (n, g, total)),
        ))
        beats.append(beat(pick(qid, "sum", [
            "So the plan: get both amounts into the same unit first, then divide to see how many fit.",
            "Remember the order. Same units first, here millilitres. Then divide the big amount by the size of one glass.",
        ])))
    else:
        T, G = total // 100, g // 100
        used = n * g
        beats.append(beat(
            "Now both are in millilitres, so we want to know how many lots of %d fit into %d. Take two zeros off each to make it friendlier: how many lots of %d fit into %d?" % (g, total, G, T),
            w("d0", "%d ÷ %d = %d ÷ %d" % (total, g, T, G)),
        ))
        beats.append(beat(
            "%d does not go into %d exactly. %d times %d is %d, and that is as close as we can get without going over." % (G, T, G, n, G * n),
            w("d1", "%d × %d = %d" % (G, n, G * n)),
        ))
        beats.append(beat(
            "So %d glasses use %d millilitres. Take that from %d, and %d millilitres are left over." % (n, used, total, left),
            w("d2", "%d × %d = %d" % (g, n, used)),
            w("d3", "%d = %d × %d + %d" % (total, g, n, left)),
            mark("d3", "+ %d" % left, "box"),
        ))
        beats.append(beat(
            "Here is the bit to think about. There are %d millilitres left in the %s. Can we count one more glass?" % (left, tub),
            ask=choose(qid + "a2", "No, a glass needs %d ml" % g, ["Yes, round up to %d" % (n + 1)],
                       "A glass only counts when it is full, and a full one needs %d millilitres. We have just %d left, so that last bit stays in the %s." % (g, left, tub)),
        ))
        beats.append(beat(
            "The leftover %d millilitres is not enough for another glass. So %d glasses can be filled." % (left, n),
            answer("ans", "%d glasses" % n),
            ring("ans", "%d glasses" % n),
        ))
        beats.append(beat(
            "Let's be sure. Glass number %d would bring the total to %d millilitres, and that is more than the %d the %s holds. So %d is right." % (n + 1, g * (n + 1), total, tub, n),
            w("chk", "%d × %d = %d" % (g, n + 1, g * (n + 1))),
            w("chk2", "%d > %d" % (g * (n + 1), total)),
        ))
        beats.append(beat(pick(qid, "sum", [
            "So the plan: same units first, then divide. And when something is left over, ask what the leftover means before you round.",
            "Remember: get both amounts into millilitres, see how many glasses fit, and never round up a glass that is not full.",
        ])))
    return lesson("rule", beats)


# ── Area and perimeter ───────────────────────────────────────────────────────

def times(x, y, pre):
    """Board lines and spoken words for x × y, split into friendly pieces when it is not a tables fact."""
    p = x * y
    if x <= 10 and y > 10:
        x, y = y, x
    whole = w(pre + "w", "%d × %d = %d" % (x, y, p))
    if (x <= 10 and y <= 10) or (y <= 10 and x % 10 == 0) or (y > 10 and y % 10 == 0):
        return [whole], "%d times %d is %d." % (x, y, p)
    if y <= 10:
        t, o = x // 10 * 10, x % 10
        a, b = t * y, o * y
        ops = [w(pre + "1", "%d × %d = %d" % (t, y, a)), w(pre + "2", "%d × %d = %d" % (o, y, b))]
        said = "Split %d into %d and %d. %d times %d is %d, and %d times %d is %d. Together that makes %d." % (x, t, o, t, y, a, o, y, b, p)
    else:
        t, o = y // 10 * 10, y % 10
        a, b = x * t, x * o
        ops = [w(pre + "1", "%d × %d = %d" % (x, t, a)), w(pre + "2", "%d × %d = %d" % (x, o, b))]
        said = "Split %d into %d and %d. %d times %d is %d, and %d times %d is %d. Together that makes %d." % (y, t, o, x, t, a, x, o, b, p)
    return ops + [w(pre + "3", "%d + %d = %d" % (a, b, p)), whole], said


def rect_area(q, L, W):
    qid = q["id"]
    A = L * W
    small = L <= 12 and W <= 12
    spec = {"kind": "rectangle", "length": "%d cm" % L, "breadth": "%d cm" % W, "inside": "Area = ?"}
    ops, said = times(L, W, "m")
    beats = [
        beat(pick(qid, "open", [
            "Here is a rectangle, %d centimetres long and %d centimetres wide. We want its area." % (L, W),
            "Our rectangle is %d centimetres long and %d centimetres wide. The question asks for its area." % (L, W),
        ]),
            given("q1", "Rectangle: length %d cm, width %d cm" % (L, W)), given("q2", "Area = ?"), fig("f1", spec)),
        beat("Area is the space inside the shape: how many little squares would cover it. Which rule gives us that?",
             ask=choose(qid + "a1", "length × width", ["length + width", "2 × (length + width)"],
                        "Adding the sides takes you along the edges, and that is the perimeter, the walk around. For the space inside we count rows of squares: length times width.")),
        beat("Picture little squares, 1 centimetre each way. Every row holds %d of them, and there are %d rows. %d rows of %d is %d times %d." % (L, W, W, L, L, W),
             lab("f", "Area = length × width"),
             *([fig("f1", dict(spec, grid={"cols": L, "rows": W}))] if small else [mark("f", "length × width")])),
        beat((said + " You can count the little squares in the picture to be sure.") if small and len(ops) == 1 else said, *ops),
        beat(pick(qid, "ans", [
            "So the area is %d square centimetres. We say square centimetres because we are counting little squares, not measuring along a line." % A,
            "That gives an area of %d square centimetres. Square centimetres, because area counts squares that cover the shape." % A,
        ]),
            answer("ans", "Area = %d sq cm" % A), ring("ans", "%d sq cm" % A)),
        beat("Check by undoing it. %d shared into %d rows gives %d in each row, and that is our length. It fits." % (A, W, L),
             w("chk", "%d ÷ %d = %d" % (A, W, L))),
        beat(pick(qid, "sum", [
            "So for the area of a rectangle, multiply the length by the width. If you catch yourself adding the sides, stop: that is the perimeter.",
            "Remember: area means the space inside, so multiply length by width. Adding the sides is for the walk around the edge.",
        ])),
    ]
    return lesson("rule", beats)


def rect_perimeter(q, L, W):
    qid = q["id"]
    s = L + W
    P = 2 * s
    beats = [
        beat(pick(qid, "open", [
            "Here is a rectangle, %d centimetres long and %d centimetres wide. We want its perimeter." % (L, W),
            "Our rectangle is %d centimetres long and %d centimetres wide, and the question asks for the perimeter." % (L, W),
        ]),
            given("q1", "Rectangle: length %d cm, width %d cm" % (L, W)), given("q2", "Perimeter = ?"),
            fig("f1", {"kind": "rectangle", "length": "%d cm" % L, "breadth": "%d cm" % W, "inside": "Perimeter = ?", "highlight": ["border"]})),
        beat("Perimeter is the distance all the way round, like an ant walking along the edge. Which sides does the ant walk along?",
             ask=choose(qid + "a1", "2 lengths and 2 widths", ["1 length and 1 width", "length × width"],
                        "Trace the edge with your finger: along the top, down the side, back along the bottom, up the other side. That is 2 lengths and 2 widths.")),
        beat("One length and one width take the ant halfway round. So we add them, then double.",
             lab("f", "Perimeter = 2 × (length + width)"), mark("f", "length + width")),
        beat("Halfway round first. %d plus %d is %d centimetres." % (L, W, s),
             w("c1", "%d + %d = %d" % (L, W, s)), note("c1", "%d" % s, "halfway round", "below", nth=(2 if ("%d" % s) in ("%d + %d" % (L, W)) else None))),
        beat("Careful: %d is only half the walk, and stopping here is the slip to watch for. Double it for the whole way round. 2 times %d is %d." % (s, s, P),
             w("c2", "2 × (%d + %d) = 2 × %d" % (L, W, s)), mark("c2", "%d + %d" % (L, W)), w("c3", "2 × %d = %d" % (s, P))),
        beat("So the perimeter is %d centimetres. Plain centimetres, because it is a distance along a line." % P,
             answer("ans", "Perimeter = %d cm" % P), ring("ans", "%d cm" % P)),
        beat("Check by walking it side by side. %d, then %d, then %d, then %d. That adds up to %d." % (L, W, L, W, P),
             w("chk", "%d + %d + %d + %d = %d" % (L, W, L, W, P))),
        beat(pick(qid, "sum", [
            "So for the perimeter of a rectangle: add the length and the width, then double.",
            "Remember: perimeter is the walk around. Length plus width gets you halfway, so double it.",
        ])),
    ]
    return lesson("rule", beats)


def rectangle(q, m):
    L, W = int(m.group(2)), int(m.group(3))
    return rect_area(q, L, W) if m.group(1) == "area" else rect_perimeter(q, L, W)


def square_area(q, s):
    qid = q["id"]
    A = s * s
    spec = {"kind": "rectangle", "square": True, "length": "%d cm" % s, "inside": "Area = ?"}
    ops, said = times(s, s, "m")
    beats = [
        beat(pick(qid, "open", [
            "Here is a square, and each side is %d centimetres. We want its area." % s,
            "Our shape is a square with sides of %d centimetres. The question asks for its area." % s,
        ]),
            given("q1", "Square: side %d cm" % s), given("q2", "Area = ?"), fig("f1", spec)),
        beat("Area is the space inside the shape: how many little squares would cover it. Which rule gives us that for a square?",
             ask=choose(qid + "a1", "side × side", ["4 × side", "side + side"],
                        "4 times the side is the walk around the edge, and that is the perimeter. For the space inside we count rows of little squares: side times side.")),
        beat("In a square every side is the same. So each row holds %d little squares, and there are %d rows as well. That is %d times %d." % (s, s, s, s),
             lab("f", "Area = side × side"),
             *([fig("f1", dict(spec, grid={"cols": s, "rows": s}))] if s <= 12 else [mark("f", "side × side")])),
        beat(("%d times %d is %d. That is a tables fact worth knowing by heart." % (s, s, A)) if len(ops) == 1 else said, *ops),
        beat("So the area is %d square centimetres. Careful: %d times %d means %d rows of %d. It is not the same as doubling %d." % (A, s, s, s, s, s),
             answer("ans", "Area = %d sq cm" % A), ring("ans", "%d sq cm" % A)),
        beat("Check by undoing it. %d shared into %d rows gives %d in each row. That is our side again." % (A, s, s),
             w("chk", "%d ÷ %d = %d" % (A, s, s))),
        beat(pick(qid, "sum", [
            "So for the area of a square, multiply the side by itself. 4 times the side is a different question, the perimeter.",
            "Remember: area of a square is side times side. Rows of little squares, all the same length.",
        ])),
    ]
    return lesson("rule", beats)


def square_perimeter(q, s):
    qid = q["id"]
    P = 4 * s
    if s <= 10:
        work = [w("c1", "4 × %d = %d" % (s, P))]
        said = "4 sides, each %d centimetres. 4 times %d is %d." % (s, s, P)
    else:
        work = [w("c0", "2 × %d = %d" % (s, 2 * s)), w("c0b", "2 × %d = %d" % (2 * s, P)), w("c1", "4 × %d = %d" % (s, P))]
        said = "4 times %d is easy if we double twice. Double %d is %d, and double %d is %d." % (s, s, 2 * s, 2 * s, P)
    beats = [
        beat(pick(qid, "open", [
            "Here is a square, and each side is %d centimetres. We want its perimeter." % s,
            "Our shape is a square with sides of %d centimetres, and the question asks for the perimeter." % s,
        ]),
            given("q1", "Square: side %d cm" % s), given("q2", "Perimeter = ?"),
            fig("f1", {"kind": "rectangle", "square": True, "length": "%d cm" % s, "inside": "Perimeter = ?", "highlight": ["border"]})),
        beat("Perimeter is the distance all the way round, like an ant walking along the edge. Which rule gives us that for a square?",
             ask=choose(qid + "a1", "4 × side", ["side × side", "2 × side"],
                        "Side times side counts the squares inside, and that is the area. For the walk around, count the sides: a square has 4, all the same length.")),
        beat("A square has 4 equal sides, and the ant walks along every one of them. So the perimeter is 4 times the side.",
             lab("f", "Perimeter = 4 × side"), mark("f", "4")),
        beat(said, *work),
        beat("So the perimeter is %d centimetres. Plain centimetres, because it is a distance along a line." % P,
             answer("ans", "Perimeter = %d cm" % P), ring("ans", "%d cm" % P)),
        beat("Check by walking round. %d, and %d, and %d, and %d. That adds up to %d." % (s, s, s, s, P),
             w("chk", "%d + %d + %d + %d = %d" % (s, s, s, s, P))),
        beat(pick(qid, "sum", [
            "So for the perimeter of a square, multiply the side by 4. Save side times side for when the question says area.",
            "Remember: perimeter is the walk around, and a square has 4 equal sides. So it is 4 times the side.",
        ])),
    ]
    return lesson("rule", beats)


def square(q, m):
    s = int(m.group(2))
    return square_area(q, s) if m.group(1) == "area" else square_perimeter(q, s)


# ── Convert a small unit to a bigger one ─────────────────────────────────────

UNIT = {"mm": "millimetres", "cm": "centimetres", "m": "metres", "km": "kilometres"}
ONE = {"mm": "millimetre", "cm": "centimetre", "m": "metre", "km": "kilometre"}
FACTOR = {("mm", "cm"): 10, ("cm", "m"): 100, ("m", "km"): 1000}
PICTURE = {
    ("mm", "cm"): "You can see it on your ruler: 10 tiny gaps inside every centimetre.",
    ("cm", "m"): "Think of a metre stick: it has 100 centimetres marked along it.",
    ("m", "km"): "The clue is in the name: kilo means a thousand.",
}


def convert(q, m):
    qid = q["id"]
    X, small, big = int(m.group(1)), m.group(2), m.group(3)
    f = FACTOR[(small, big)]
    Y = X // f
    other = 2 if 2 * f != X else 3
    beats = [
        beat(pick(qid, "open", [
            "We have %d %s, and we want to say the same length in %s." % (X, UNIT[small], UNIT[big]),
            "%d %s. Same length, new unit: we want it in %s." % (X, UNIT[small], UNIT[big]),
        ]),
            given("q1", "%d %s = ? %s" % (X, small, big))),
        beat("Start with the fact that links the two units. 1 %s is %d %s. %s" % (ONE[big], f, UNIT[small], PICTURE[(small, big)]),
             lab("f", "1 %s = %d %s" % (big, f, small)),
             fig("f1", {"kind": "table", "headers": [UNIT[big], UNIT[small]],
                        "rows": [["1", "%d" % f], ["%d" % other, "%d" % (other * f)], ["?", "%d" % X]], "highlight": ["r2"]})),
        beat("A %s is bigger than a %s. So will the number of %s be bigger or smaller than %d?" % (ONE[big], ONE[small], UNIT[big], X),
             ask=choose(qid + "a1", "smaller, so we divide by %d" % f, ["bigger, so we multiply by %d" % f],
                        "It takes %d %s to make just 1 %s. A bigger unit means fewer of them, so the number goes down: we divide." % (f, UNIT[small], ONE[big]))),
        beat(pick(qid, "div", [
            "Every %d %s make 1 %s, so we count how many lots of %d are in %d. %d divided by %d is %d." % (f, UNIT[small], ONE[big], f, X, X, f, Y),
            "We are bundling the %s into groups of %d, one group for each %s. %d divided by %d is %d." % (UNIT[small], f, ONE[big], X, f, Y),
        ]),
            w("c1", "%d ÷ %d = %d" % (X, f, Y)), mark("c1", "÷ %d" % f)),
        beat("So %d %s is the same length as %d %s." % (X, UNIT[small], Y, UNIT[big]),
             answer("ans", "%d %s = %d %s" % (X, small, Y, big)), ring("ans", "%d %s" % (Y, big))),
        beat("Check by going back the other way. %d %s, times %d, is %d %s. Just what we started with." % (Y, UNIT[big], f, X, UNIT[small]),
             w("chk", "%d × %d = %d" % (Y, f, X))),
        beat(pick(qid, "sum", [
            "So, small unit to a bigger unit: divide by how many small ones make one big one. Bigger unit, smaller number.",
            "Remember the idea, not just the rule. Bigger units mean fewer of them, so going up to a bigger unit we divide.",
        ])),
    ]
    return lesson("rule", beats)


# ── Speed, distance and time ─────────────────────────────────────────────────

def hop_line(S, n):
    """A road marked every S km, with one hop for each hour (drawn only for short trips)."""
    return {"kind": "numberLine", "min": 0, "max": S * n, "step": S,
            "hops": [{"from": S * i, "to": S * (i + 1), "label": "1 hour"} for i in range(n)]}


def find_time(q, m):
    qid = q["id"]
    thing, D, S = m.group(1), int(m.group(2)), int(m.group(3))
    T = D // S
    hops = [fig("f1", hop_line(S, T))] if T <= 6 else []
    beats = [
        beat("A %s travels %d kilometres at a speed of %d kilometres per hour. We want to know how long the journey takes." % (thing, D, S),
             given("q1", "%d km at %d km/hr" % (D, S)), given("q2", "Time = ?"),
             fig("f1", {"kind": "journey", "places": ["Start", "End"], "legs": [{"top": "%d km" % D, "bottom": "? hours"}],
                        "note": "%d km in every hour" % S})),
        beat("Speed tells us how far the %s goes in one hour. So %d kilometres per hour means: every hour, another %d kilometres." % (thing, S, S),
             lab("f", "%d km/hr means %d km in 1 hour" % (S, S)), mark("f", "1 hour")),
        beat("After 1 hour the %s has done %d kilometres, and the whole trip is %d. What are we really asking?" % (thing, S, D),
             ask=choose(qid + "a1", "how many %ds fit in %d" % (S, D), ["what is %d × %d" % (D, S), "what is %d − %d" % (D, S)],
                        "Each hour uses up %d kilometres of the road. So we count how many lots of %d fit into %d, and that is a division." % (S, S, D))),
        beat("Hop along the road, %d kilometres for every hour, until we reach %d. Counting the hops is the same as dividing the distance by the speed." % (S, D),
             lab("r", "Time = distance ÷ speed"), *hops),
        beat("%d divided by %d is %d. So the journey takes %d hours." % (D, S, T, T),
             w("c1", "%d ÷ %d = %d" % (D, S, T)), answer("ans", "Time = %d hours" % T), ring("ans", "%d hours" % T)),
        beat("Check it. %d hours, with %d kilometres in each one, is %d kilometres. That is the whole journey." % (T, S, D),
             w("chk", "%d × %d = %d" % (S, T, D))),
        beat("So when you know the distance and the speed, ask how many hours' worth of distance fit in. That is distance divided by speed."),
    ]
    return lesson("rule", beats)


def find_distance(q, m):
    qid = q["id"]
    thing, S, T = m.group(1), int(m.group(2)), int(m.group(3))
    D = S * T
    hops = [fig("f1", hop_line(S, T))] if T <= 6 else []
    beats = [
        beat("A %s travels at %d kilometres per hour for %d hours. We want to know how far it goes." % (thing, S, T),
             given("q1", "%d km/hr for %d hours" % (S, T)), given("q2", "Distance = ?"),
             fig("f1", {"kind": "journey", "places": ["Start", "End"], "legs": [{"top": "? km", "bottom": "%d hours" % T}],
                        "note": "%d km in every hour" % S})),
        beat("Speed tells us how far the %s goes in one hour. So %d kilometres per hour means: every hour, another %d kilometres." % (thing, S, S),
             lab("f", "%d km/hr means %d km in 1 hour" % (S, S)), mark("f", "1 hour")),
        beat("The %s keeps going for %d hours. How do we find the whole distance?" % (thing, T),
             ask=choose(qid + "a1", "%d × %d" % (S, T), ["%d + %d" % (S, T), "%d ÷ %d" % (S, T)],
                        "Every hour adds another %d kilometres. %d hours means %d lots of %d, so we multiply." % (S, T, T, S))),
        beat("One hop of %d kilometres for each hour. %d hops means %d times %d, which is %d kilometres." % (S, T, S, T, D),
             lab("r", "Distance = speed × time"), w("c1", "%d × %d = %d" % (S, T, D)), *hops),
        beat("So the %s covers %d kilometres." % (thing, D),
             answer("ans", "Distance = %d km" % D), ring("ans", "%d km" % D)),
        beat("Check it. Share %d kilometres over %d hours and you get %d kilometres in each hour. That is the speed we were given." % (D, T, S),
             w("chk", "%d ÷ %d = %d" % (D, T, S))),
        beat("So when you know the speed and the time, the distance is one hour's worth, taken once for every hour. Speed times time."),
    ]
    return lesson("rule", beats)


def find_speed(q, m):
    qid = q["id"]
    thing, D, T = m.group(1), int(m.group(2)), int(m.group(3))
    S = D // T
    bar = [fig("f1", {"kind": "barModel", "bars": [{"segments": [{"units": 1, "label": "1 hour"} for _ in range(T)], "brace": "%d km" % D}]})] if T <= 8 else []
    beats = [
        beat("A %s covers %d kilometres in %d hours. We want its speed." % (thing, D, T),
             given("q1", "%d km in %d hours" % (D, T)), given("q2", "Speed = ?"),
             fig("f1", {"kind": "journey", "places": ["Start", "End"], "legs": [{"top": "%d km" % D, "bottom": "%d hours" % T}],
                        "note": "? km in every hour"})),
        beat("Speed is just a short way of saying how far something goes in one hour. So we need one hour's share of the journey.",
             lab("f", "Speed = how far in 1 hour"), mark("f", "1 hour")),
        beat("The %d kilometres took %d hours, the same amount every hour. How do we find one hour's share?" % (D, T),
             ask=choose(qid + "a1", "%d ÷ %d" % (D, T), ["%d × %d" % (D, T), "%d − %d" % (D, T)],
                        "The %d kilometres are spread evenly over %d hours. To find one hour's share, we split %d into %d equal parts: a division." % (D, T, D, T))),
        beat("Cut the journey into %d equal pieces, one for each hour. %d divided by %d is %d." % (T, D, T, S),
             lab("r", "Speed = distance ÷ time"), w("c1", "%d ÷ %d = %d" % (D, T, S)), *bar),
        beat("So the %s goes %d kilometres in every hour. Its speed is %d kilometres per hour." % (thing, S, S),
             answer("ans", "Speed = %d km/hr" % S), ring("ans", "%d km/hr" % S)),
        beat("Check it. %d kilometres every hour, for %d hours, makes %d kilometres. That matches the journey." % (S, T, D),
             w("chk", "%d × %d = %d" % (S, T, D))),
        beat("So when you know the distance and the time, share the distance equally over the hours. Distance divided by time."),
    ]
    return lesson("rule", beats)


def average_speed(q, m):
    qid = q["id"]
    name, pro = m.group(1), m.group(8)
    d = [int(m.group(i)) for i in (2, 4, 6)]
    s = [int(m.group(i)) for i in (3, 5, 7)]
    t = [a // b for a, b in zip(d, s)]
    D, T = sum(d), sum(t)
    avg = D // T
    she = "she" if pro == "her" else "he"
    road = {"kind": "journey", "places": ["Start", "A", "B", "End"],
            "legs": [{"top": "%d km" % d[i], "bottom": "%d km/hr" % s[i]} for i in range(3)]}
    timed = {"kind": "journey", "places": ["Start", "A", "B", "End"],
             "legs": [{"top": "%d km" % d[i], "bottom": "%d hours" % t[i]} for i in range(3)]}
    beats = [
        beat("%s's trip has three parts, each at a different speed. We want %s average speed for the whole trip." % (name, pro),
             given("q1", "%d km at %d km/hr, %d km at %d km/hr," % (d[0], s[0], d[1], s[1])),
             given("q2", "then %d km at %d km/hr. Average speed = ?" % (d[2], s[2])),
             fig("f1", road)),
        beat("Average speed has a famous trap in it. Which of these do you think gives the average speed?",
             ask=choose(qid + "a1", "total distance ÷ total time", ["add the 3 speeds, then ÷ 3"],
                        "That is the trap. %s does not spend the same time at each speed, so the speeds do not count equally. Average speed is always the total distance divided by the total time." % she.capitalize())),
        beat("So we never just average the speeds. We need two totals: how far altogether, and how long altogether.",
             lab("f", "Average speed = total distance ÷ total time")),
        beat("Total distance first. %d plus %d plus %d is %d kilometres." % (d[0], d[1], d[2], D),
             w("c1", "%d + %d + %d = %d" % (d[0], d[1], d[2], D)), note("c1", "%d" % D, "total km", "below", nth=(2 if ("%d" % D) in [str(x) for x in d] else None))),
        beat("Now for the time. Each part has its own speed, so we time each part on its own. Time is distance divided by speed: how many hours' worth fit in.",
             lab("r", "Time = distance ÷ speed")),
        beat("%d divided by %d is %d hours. %d divided by %d is %d hours. And %d divided by %d is %d hours." % (d[0], s[0], t[0], d[1], s[1], t[1], d[2], s[2], t[2]),
             w("t1", "%d ÷ %d = %d" % (d[0], s[0], t[0])), w("t2", "%d ÷ %d = %d" % (d[1], s[1], t[1])), w("t3", "%d ÷ %d = %d" % (d[2], s[2], t[2])),
             fig("f1", timed)),
        beat("Add up the hours. %d plus %d plus %d is %d hours altogether." % (t[0], t[1], t[2], T),
             w("c2", "%d + %d + %d = %d" % (t[0], t[1], t[2], T)), note("c2", "= %d" % T, "total hours", "below")),
        beat("Now share the whole distance over the whole time. %d divided by %d is %d. So %s average speed is %d kilometres per hour." % (D, T, avg, pro, avg),
             w("c3", "%d ÷ %d = %d" % (D, T, avg)), answer("ans", "Average speed = %d km/hr" % avg), ring("ans", "%d km/hr" % avg)),
        beat("Check it. Going steadily at %d kilometres per hour for %d hours covers %d kilometres, exactly the whole trip." % (avg, T, D),
             w("chk", "%d × %d = %d" % (avg, T, D))),
        beat("So for average speed: total distance, divided by total time. Find the time for each part first, and never just average the speeds."),
    ]
    return lesson("rule", beats)


RULES = [
    (re.compile(r"^Convert (\d+) (mm|cm|m) to (cm|m|km)\.$"), convert),
    (re.compile(r"^A (\w+) travels (\d+) km at a speed of (\d+) km/hr\. How long does the journey take\?$"), find_time),
    (re.compile(r"^A (\w+) travels at (\d+) km/hr for (\d+) hours\. What distance does it cover\?$"), find_distance),
    (re.compile(r"^A (\w+) covers (\d+) km in (\d+) hours\. Find its speed\.$"), find_speed),
    (re.compile(r"^(\w+) covers (\d+) km at (\d+) km/hr, (\d+) km at (\d+) km/hr, and (\d+) km at (\d+) km/hr\. What is (his|her) average speed\?$"), average_speed),
    (re.compile(r"^Find the (area|perimeter) of a rectangle with length (\d+) cm and width (\d+) cm\.$"), rectangle),
    (re.compile(r"^Find the (area|perimeter) of a square with side (\d+) cm\.$"), square),
    (re.compile(r"^(\w+) has (\d+) bags of (\w+), each weighing (\d+) kg (\d+) g\. What is the total weight in grams\?$"), bags),
    (re.compile(r"^A (\w+) holds (\d+) litres of water\. How many glasses of (\d+) ml each can be filled\?$"), glasses),
]
