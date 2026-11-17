"""Area and perimeter, part 1: a shape with a piece taken out (and what the rest costs or needs)."""
from imported_02_lib import ANS, B, FIG, GIVEN, L, M, N, W, choose, lesson, num

LESSONS = {}
P = "AIGEN_grade5_"

SQM = "square metres"
SQCM = "square centimetres"


def clean(v):
    """Tidy a product of decimals (60.75 * 120 -> 7290)."""
    v = round(v, 6)
    return int(v) if v == int(v) else v


def last(line, target):
    """nth for the last time `target` appears on `line`."""
    return line.count(target)


def split_times(lid, a, b, hi, words=None):
    """a × b worked as a × hi + a × (b − hi). Returns (board ops, what to say, product)."""
    lo = clean(b - hi)
    p1, p2, p = clean(a * hi), clean(a * lo), clean(a * b)
    ops = [W(lid + "a", "%s × %s = %s" % (num(a), num(hi), num(p1))),
           W(lid + "b", "%s × %s = %s" % (num(a), num(lo), num(p2))),
           W(lid, "%s × %s = %s + %s = %s" % (num(a), num(b), num(p1), num(p2), num(p)))]
    say = words or "Split the %s into %s and %s. %s times %s is %s, and %s times %s is %s. Together, %s" % (
        num(b), num(hi), num(lo), num(a), num(hi), num(p1), num(a), num(lo), num(p2), num(p))
    return ops, say, p


def rect(length, breadth, inside=None, square=False):
    spec = {"kind": "rectangle", "length": length, "breadth": breadth}
    if inside:
        spec["inside"] = inside
    if square:
        spec["square"] = True
    return spec


def side_ask(c, what, measure):
    """Ask for the area of a square of side c; the slips are the perimeter and doubling."""
    s = num(c)
    length = "%s %s" % (s, measure[:-1] if c == 1 else measure)
    if c == 2:
        choices, answer = ["2 × 4 = 8", "2 × 2 = 4"], 1
    else:
        choices = ["%s × 4 = %s" % (s, num(clean(c * 4))), "%s × %s = %s" % (s, s, num(clean(c * c))),
                   "%s + %s = %s" % (s, s, num(clean(c + c)))]
        answer = 1
    return B("Now the %s. It is a square with a side of %s. What is its area?" % (what, length),
             ask=choose(choices, answer,
                        "%s times 4 is the distance all the way round the square. For the space inside it, we multiply side by side." % s))


def takeaway(intro, given, fig, wname, a, b, pname, c, d, unit, plan,
             whole_hi=None, piece_ask=False, piece_say=None, piece_ops=None,
             sub_say=None, sub_ops=None, final=False):
    """The beats up to 'whole area − piece area'. Returns (beats, whole, piece, rest)."""
    A, Pc = clean(a * b), clean(c * d)
    R = clean(A - Pc)
    beats = [B(intro, GIVEN("q", given[0]), *([L("q%d" % i, g) for i, g in enumerate(given[1:], 2)] + [FIG("f1", fig)]))]
    beats.append(plan)

    if a != b:
        lead = "The area of a rectangle is length times breadth."
    elif "square" in wname:
        lead = "The area of a square is side times side."
    else:
        lead = "The %s is a square, so its area is side times side." % wname
    if whole_hi:
        ops, words, _ = split_times("w", a, b, whole_hi)
        beats.append(B("%s For the %s: %s." % (lead, wname, words[0].lower() + words[1:]), *ops))
        beats.append(B("So the %s has an area of %s %s." % (wname, num(A), unit),
                       N("w", num(A), wname, nth=last(ops[-1]["text"], num(A)))))
    else:
        line = "%s × %s = %s" % (num(a), num(b), num(A))
        beats.append(B("%s For the %s, %s times %s is %s %s." % (lead, wname, num(a), num(b), num(A), unit),
                       W("w", line), N("w", num(A), wname, nth=last(line, num(A)))))

    pline = "%s × %s = %s" % (num(c), num(d), num(Pc))
    pnote = N("p", num(Pc), pname, nth=last(pline, num(Pc)))
    if piece_say:
        beats.append(B(piece_say, *((piece_ops or []) + [W("p", pline), pnote])))
    elif piece_ask:
        beats.append(side_ask(c, pname, "metres" if unit == SQM else "centimetres"))
        beats.append(B("%s times %s is %s. So the %s covers %s %s." % (num(c), num(c), num(Pc), pname, num(Pc), unit),
                       W("p", pline), pnote))
    elif c == d:
        beats.append(B("Now the %s. It is a square, so its area is side times side: %s times %s is %s %s."
                       % (pname, num(c), num(c), num(Pc), unit), W("p", pline), pnote))
    else:
        beats.append(B("Now the %s. %s times %s is %s, so it covers %s %s." % (pname, num(c), num(d), num(Pc), num(Pc), unit),
                       W("p", pline), pnote))

    rline = "%s − %s = %s" % (num(A), num(Pc), num(R))
    say = sub_say or "Now take the %s away from the %s. %s minus %s is %s %s." % (pname, wname, num(A), num(Pc), num(R), unit)
    ops = list(sub_ops or [])
    if final:
        ops += [ANS("r", rline), M("r", num(R), "circle", last(rline, num(R)))]
    else:
        ops += [W("r", rline)]
    beats.append(B(say, *ops))
    return beats, A, Pc, R


def add_back(A, Pc, R, words):
    return B(words, W("c", "%s + %s = %s" % (num(R), num(Pc), num(A))))


# ── Just the area that is left ───────────────────────────────────────────────

beats, A, Pc, R = takeaway(
    "Riya's card is 24 centimetres long and 18 centimetres wide. A square photo of side 10 centimetres sits in the middle, and glitter paper covers the rest.",
    ["Card 24 cm × 18 cm, square photo of side 10 cm", "Glitter paper = ?"],
    rect("24 cm", "18 cm", "photo: side 10 cm"),
    "card", 24, 18, "photo", 10, 10, SQCM,
    B("How do we find the part that gets glitter paper?",
      ask=choose(["card area + photo area", "card area − photo area", "just the photo area"], 1,
                 "The photo covers up part of the card, and no glitter goes there. So the photo's area must come off the card's area.")),
    whole_hi=10, piece_ask=True, final=True)
LESSONS[P + "12e17c4c-46ad-4382-a6a0-9ad8e7881076"] = lesson(*(beats + [
    add_back(A, Pc, R, "Check by adding back. 332 plus 100 is 432, the whole card."),
    B("Two slips to avoid. 432 is the whole card, photo and all. And 84 is the distance round the card, its perimeter, not its area.",
      W("t", "2 × (24 + 18) = 84")),
    B("For any shape with a piece covered up: the whole area, minus the covered piece."),
]))

beats, A, Pc, R = takeaway(
    "Priya's rangoli is a rectangle, 15 centimetres long and 8 centimetres wide. A small rectangle, 5 centimetres by 3 centimetres, is cut from one corner for a diya.",
    ["Rangoli 15 cm × 8 cm, corner cut out: 5 cm × 3 cm", "Area with coloured powder = ?"],
    rect("15 cm", "8 cm", "cut out: 5 × 3"),
    "rangoli", 15, 8, "cut-out", 5, 3, SQCM,
    B("How do we find the area that gets coloured powder?",
      ask=choose(["15 × 8 + 5 × 3", "15 × 8 − 5 × 3", "15 × 8 only"], 1,
                 "The corner piece is cut out for the diya, so no powder goes there. Its area has to come off the big rectangle.")),
    final=True)
LESSONS[P + "2f271f17-776d-443e-9029-37b5526035e1"] = lesson(*(beats + [
    add_back(A, Pc, R, "Check by putting the corner back. 105 plus 15 is 120, the full rectangle."),
    B("Careful with the two 15s here. One is the length of the rangoli. The other is the area of the cut-out, 5 times 3. They only happen to match."),
    B("And never add the piece on. Cutting a corner out makes a shape smaller: whole area, minus the piece."),
]))

beats, A, Pc, R = takeaway(
    "Riya's card is 18 centimetres long and 12 centimetres wide. A square golden sticker of side 5 centimetres goes in the centre. How much of the card is still showing?",
    ["Card 18 cm × 12 cm, square sticker of side 5 cm", "Area not covered = ?"],
    rect("18 cm", "12 cm", "sticker: side 5 cm"),
    "card", 18, 12, "sticker", 5, 5, SQCM,
    B("The sticker hides part of the card. So the part still showing is the card's area, take away the sticker's area.",
      L("plan", "Not covered = card − sticker")),
    whole_hi=10, piece_ask=True, final=True)
LESSONS[P + "2f3e11f6-8afa-42cc-a0d7-b1b22d92b341"] = lesson(*(beats + [
    add_back(A, Pc, R, "Check by adding back. 191 plus 25 is 216, the whole card."),
    B("The slip here is to take away just 5, the side of the sticker. A side is a length. We must take an area away from an area."),
    B("So: find both areas first, then subtract the small one from the big one."),
]))

beats, A, Pc, R = takeaway(
    "Ananya's rangoli is 12 centimetres long and 8 centimetres wide. She cuts a small rectangle, 4 centimetres by 3 centimetres, out of one corner for a diya.",
    ["Rangoli 12 cm × 8 cm, corner cut out: 4 cm × 3 cm", "Area left = ?"],
    rect("12 cm", "8 cm", "cut out: 4 × 3"),
    "rangoli", 12, 8, "cut-out", 4, 3, SQCM,
    B("A piece is being cut away. Which sum gives the area that is left?",
      ask=choose(["12 × 8 − 4 × 3", "12 × 8 + 4 × 3", "12 × 8 only"], 0,
                 "Cutting a corner out makes the rangoli smaller. So the area of the cut-out piece comes off the area of the full rectangle.")),
    final=True)
LESSONS[P + "3490db5c-1ed7-4cc8-8343-99d4c3c4d933"] = lesson(*(beats + [
    add_back(A, Pc, R, "Check by putting the corner back. 84 plus 12 is 96, the full rectangle."),
    B("Notice that 96 is one of the choices. That is the rangoli before the corner was cut. Read to the end of the question before you stop."),
    B("The method: area of the whole shape, minus the area of the piece cut away."),
]))

beats, A, Pc, R = takeaway(
    "Meera's rangoli is a square, 14 centimetres on each side. A mirror, 8 centimetres long and 5 centimetres wide, sits in the centre. How much rangoli can we still see?",
    ["Square rangoli of side 14 cm, mirror 8 cm × 5 cm", "Area not covered = ?"],
    rect("14 cm", "14 cm", "mirror: 8 × 5", square=True),
    "rangoli", 14, 14, "mirror", 8, 5, SQCM,
    B("The mirror hides part of the rangoli. Which plan finds the part we can still see?",
      ask=choose(["rangoli area − mirror area", "rangoli area + mirror area", "mirror area only"], 0,
                 "The mirror sits on top of the rangoli and covers some of it. So the mirror's area comes off the rangoli's area.")),
    whole_hi=10, final=True)
LESSONS[P + "70b6e4ec-4222-43c5-83c1-5bdbab90304b"] = lesson(*(beats + [
    add_back(A, Pc, R, "Check by adding back. 156 plus 40 is 196, the whole square."),
    B("One trap: taking away 8 plus 5, which is 13, as if the mirror were only its edges. The mirror covers an area, 8 times 5.",
      W("t", "8 + 5 = 13")),
    B("So: side times side for the square, length times breadth for the mirror, then subtract."),
]))

beats, A, Pc, R = takeaway(
    "A large square rangoli has a side of 20 centimetres. A smaller square, of side 12 centimetres, sits in the middle. Coloured powder fills the space between them.",
    ["Large square of side 20 cm, small square of side 12 cm", "Area between the squares = ?"],
    rect("20 cm", "20 cm", "square: side 12 cm", square=True),
    "large square", 20, 20, "small square", 12, 12, SQCM,
    B("The powder goes between the two squares. So we want the area of the large square, take away the area of the small one.",
      L("plan", "Powder = large square − small square")),
    piece_ask=True,
    sub_say="Now take the small square away from the large one. 400 minus 100 is 300, and 300 minus 44 is 256 square centimetres.",
    sub_ops=[W("s1", "400 − 100 = 300"), W("s2", "300 − 44 = 256")], final=True)
LESSONS[P + "73cf3a7b-eb15-45c3-b2e1-b98b97c6974c"] = lesson(*(beats + [
    add_back(A, Pc, R, "Check by adding back. 256 plus 144 is 400, the large square."),
    B("A tempting shortcut is to subtract the sides first: 20 minus 12 is 8, and 8 times 8 is 64. That is far too small. Find each area, then subtract.",
      W("t", "8 × 8 = 64")),
    B("So for a shape inside a shape: big area, minus small area."),
]))

beats, A, Pc, R = takeaway(
    "Priya wants to cover a wall with rangoli paper. The wall is 8 metres long and 5 metres wide. A window, 2 metres long and 1 metre wide, is not covered.",
    ["Wall 8 m × 5 m, window 2 m × 1 m", "Paper needed = ?"],
    rect("8 m", "5 m", "window: 2 m × 1 m"),
    "wall", 8, 5, "window", 2, 1, SQM,
    B("Which part of the wall actually needs paper?",
      ask=choose(["the wall and the window", "the wall without the window", "only the window"], 1,
                 "Paper goes on the wall, but not over the window. So we find the wall's area and take the window's area off.")),
    final=True)
LESSONS[P + "a87f8d98-9bd5-446c-a9d1-a0b60c9f6ec8"] = lesson(*(beats + [
    add_back(A, Pc, R, "Check by adding back. 38 plus 2 is 40, the whole wall."),
    B("One of the choices is 37. That comes from taking away 2 plus 1, which is 3. But a window's area is length times breadth, 2 times 1.",
      W("t", "40 − (2 + 1) = 37")),
    B("So: area of the wall, minus the area of the part you skip."),
]))

beats, A, Pc, R = takeaway(
    "Arjun is painting a wall that is 8 metres long and 5 metres tall. In the middle is a square window with a side of 2 metres, which he does not paint.",
    ["Wall 8 m × 5 m, square window of side 2 m", "Area to paint = ?"],
    rect("8 m", "5 m", "window: side 2 m"),
    "wall", 8, 5, "window", 2, 2, SQM,
    B("Arjun paints the wall but not the window. So the area to paint is the wall's area, take away the window's area.",
      L("plan", "To paint = wall − window")),
    piece_ask=True, final=True)
LESSONS[P + "ba446241-34aa-4ec7-bc0c-29506f6cc1a3"] = lesson(*(beats + [
    add_back(A, Pc, R, "Check by adding back. 36 plus 4 is 40, the whole wall."),
    B("The slip to watch is taking away 2, the side of the window, and not 4, its area. And never add the window on: that would give 44.",
      W("t", "40 + 4 = 44")),
    B("So: area of the wall, minus the area of the window."),
]))


# ── The area that is left, then its cost ─────────────────────────────────────

def cost_beats(R, rate, unit_one, hi=None, words=None, who=None):
    """Ask how to price R units at `rate` rupees each, then work it out and ring the answer."""
    total = clean(R * rate)
    if R == int(R):
        miss = "Every one of the %s %ss costs %s rupees. %s lots of %s is a multiplication." % (
            num(R), unit_one, num(rate), num(R), num(rate))
    else:
        miss = "We pay %s rupees for every %s, and there are %s of them. So many lots of %s is a multiplication." % (
            num(rate), unit_one, num(R), num(rate))
    ask = B("Each %s costs %s rupees. How do we find the cost of %s %ss?" % (unit_one, num(rate), num(R), unit_one),
            ask=choose(["%s + %s" % (num(R), num(rate)), "%s ÷ %s" % (num(R), num(rate)), "%s × %s" % (num(R), num(rate))], 2, miss))
    if hi:
        ops, say, _ = split_times("m", R, rate, hi, words)
        ops[-1]["tone"] = "answer"
        line = ops[-1]["text"]
        work = B(say + " rupees.", *(ops + [M("m", num(total), "circle", last(line, num(total)))]))
    else:
        line = "%s × %s = %s" % (num(R), num(rate), num(total))
        work = B("%s times %s is %s. %s spends %s rupees." % (num(R), num(rate), num(total), who, num(total)),
                 ANS("m", line), M("m", num(total), "circle", last(line, num(total))))
    return [ask, work]


beats, A, Pc, R = takeaway(
    "Riya's room is 12 metres long and 8 metres wide. A square rangoli of side 3 metres sits in one corner. The rest of the floor gets paint that costs 45 rupees for each square metre.",
    ["Room 12 m × 8 m, square rangoli of side 3 m", "Paint: ₹45 per sq. m. Cost = ?"],
    rect("12 m", "8 m", "rangoli: side 3 m"),
    "room", 12, 8, "rangoli", 3, 3, SQM,
    B("Paint is paid for by the square metre. So first we need the number of square metres that get painted: the room, without the rangoli.",
      L("plan", "Painted area = room − rangoli")),
    piece_ask=True)
LESSONS[P + "0c769cf5-835c-4728-af0b-bd4e0da4db6d"] = lesson(*(beats + cost_beats(R, 45, "square metre", hi=40) + [
    B("If we forget the rangoli and paint the whole floor, it is 96 times 45, which is 4,320. That is one of the choices, waiting to catch us.",
      W("t", "96 × 45 = 4,320")),
    B("Area first, then cost: find the area that really gets painted, and multiply by the price of 1 square metre."),
]))

beats, A, Pc, R = takeaway(
    "Priya's floor is 12 metres long and 8 metres wide, with a square rangoli of side 3 metres in the centre. She paints everything except the rangoli, at 15 rupees for each square metre.",
    ["Floor 12 m × 8 m, square rangoli of side 3 m", "Paint: ₹15 per sq. m. Cost = ?"],
    rect("12 m", "8 m", "rangoli: side 3 m"),
    "floor", 12, 8, "rangoli", 3, 3, SQM,
    B("The cost depends on how much floor is painted. That is the whole floor, take away the square under the rangoli.",
      L("plan", "Painted area = floor − rangoli")),
    piece_ask=True)
LESSONS[P + "121d3f62-a051-44fb-ac6e-cfa6b8b4e92e"] = lesson(*(beats + cost_beats(
    R, 15, "square metre", hi=10,
    words="15 is 10 and 5. 87 times 10 is 870. 87 times 5 is half of that, 435. Together, 1,305") + [
    B("The choice 1,260 is waiting for anyone who takes 12 away for the rangoli. 12 is 3 times 4, the distance round it. Its area is 3 times 3, which is 9.",
      W("t1", "96 − 12 = 84"), W("t2", "84 × 15 = 1,260")),
    B("Find the painted area first. Then every square metre costs the same, so multiply."),
]))

beats, A, Pc, R = takeaway(
    "Meera's card is 24 centimetres long and 18 centimetres wide. A square photo of side 10 centimetres is pasted in the centre. Glitter paint for the rest costs 2 rupees for each square centimetre.",
    ["Card 24 cm × 18 cm, square photo of side 10 cm", "Glitter paint: ₹2 per sq. cm. Cost = ?"],
    rect("24 cm", "18 cm", "photo: side 10 cm"),
    "card", 24, 18, "photo", 10, 10, SQCM,
    B("Before any cost, we need an area. Which area gets glitter paint?",
      ask=choose(["card area + photo area", "card area only", "card area − photo area"], 2,
                 "No glitter goes on the photo. So the photo's area has to come off the card's area.")),
    whole_hi=10)
LESSONS[P + "92e372bf-c825-4e22-8008-475abab77069"] = lesson(*(beats + cost_beats(R, 2, "square centimetre", who="Meera") + [
    B("If you forget the photo, you get 432 times 2, which is 864. But no glitter goes on the photo.",
      W("t", "432 × 2 = 864")),
    B("So: the area that is really painted, times the price of 1 square centimetre."),
]))

beats, A, Pc, R = takeaway(
    "Priya's floor is 12 metres long and 8 metres wide. A square pillar of side 2 metres stands in one corner. Tiles for the rest of the floor cost 15 rupees for each square metre.",
    ["Floor 12 m × 8 m, square pillar of side 2 m", "Tiles: ₹15 per sq. m. Cost = ?"],
    rect("12 m", "8 m", "pillar: side 2 m"),
    "floor", 12, 8, "pillar", 2, 2, SQM,
    B("Tiles cannot go under the pillar. So the area to tile is the floor, take away the square where the pillar stands.",
      L("plan", "Area to tile = floor − pillar")),
    piece_ask=True)
LESSONS[P + "9b1b91fa-2688-4680-be8b-6e5a7824d12d"] = lesson(*(beats + cost_beats(
    R, 15, "square metre", hi=10,
    words="15 is 10 and 5. 92 times 10 is 920. 92 times 5 is half of that, 460. Together, 1,380") + [
    B("Two traps. Taking away 8, the distance round the pillar, leads to 1,320. Forgetting the pillar leads to 1,440. Both are among the choices.",
      W("t1", "88 × 15 = 1,320"), W("t2", "96 × 15 = 1,440")),
    B("So: floor area, minus pillar area, and only then the price."),
]))

PILLAR_SAY = ("Now the pillar. It is a square, so side times side: 1.5 times 1.5. "
              "1 times 1.5 is 1.5, and half of 1.5 is 0.75. Together, 2.25 square metres.")
PILLAR_OPS = [W("p1", "1 × 1.5 = 1.5"), W("p2", "0.5 × 1.5 = 0.75"), W("p3", "1.5 + 0.75 = 2.25")]
PILLAR_SUB = "Take the pillar away from the floor. 63 minus 2 is 61, and 0.25 more off leaves 60.75 square metres."
PILLAR_SUB_OPS = [W("s1", "63 − 2 = 61"), W("s2", "61 − 0.25 = 60.75")]

beats, A, Pc, R = takeaway(
    "Arjun's kitchen floor is 9 metres long and 7 metres wide. A square pillar of side 1.5 metres takes up one corner. Tiles for the rest cost 120 rupees for each square metre.",
    ["Kitchen 9 m × 7 m, square pillar of side 1.5 m", "Tiles: ₹120 per sq. m. Cost = ?"],
    rect("9 m", "7 m", "pillar: side 1.5 m"),
    "floor", 9, 7, "pillar", 1.5, 1.5, SQM,
    B("Before the cost, we need an area. Which area needs tiles?",
      ask=choose(["floor + pillar", "floor − pillar", "pillar only"], 1,
                 "Tiles cannot go where the pillar stands. So the pillar's area comes off the floor's area.")),
    piece_say=PILLAR_SAY, piece_ops=list(PILLAR_OPS), sub_say=PILLAR_SUB, sub_ops=list(PILLAR_SUB_OPS))
LESSONS[P + "ab9fa105-f0a7-421b-a019-753633cff300"] = lesson(*(beats + cost_beats(R, 120, "square metre", hi=100) + [
    B("Forget the pillar and you get 63 times 120, which is 7,560. That is one of the choices. But tiles do not go under a pillar.",
      W("t", "63 × 120 = 7,560")),
    B("So: the area that really gets tiles, times the price of 1 square metre."),
]))


# ── The area that is left, then how many tiles or cans ───────────────────────

beats, A, Pc, R = takeaway(
    "Ravi's kitchen floor is 9 metres long and 7 metres wide. In the middle is a square pillar of side 1.5 metres. Each tile covers 0.25 square metres. How many tiles for the rest of the floor?",
    ["Kitchen 9 m × 7 m, square pillar of side 1.5 m", "Each tile covers 0.25 sq. m. How many tiles?"],
    rect("9 m", "7 m", "pillar: side 1.5 m"),
    "floor", 9, 7, "pillar", 1.5, 1.5, SQM,
    B("Two jobs. First find the area that needs tiles: the floor, take away the pillar. Then see how many tiles fill it.",
      L("plan", "Area to tile = floor − pillar")),
    piece_say=PILLAR_SAY, piece_ops=list(PILLAR_OPS), sub_say=PILLAR_SUB, sub_ops=list(PILLAR_SUB_OPS))
LESSONS[P + "05f02aa9-2a3e-4a32-a969-0489f2a4e277"] = lesson(*(beats + [
    B("Each tile covers 0.25 of a square metre. That is a quarter. So how many tiles cover 1 whole square metre?",
      ask=choose(["25", "4", "0.25"], 1,
                 "0.25 is one quarter, and 4 quarters make a whole. So 4 tiles cover 1 square metre.")),
    B("4 tiles for every square metre. So we need 60.75 times 4. 60 times 4 is 240, and 0.75 times 4 is 3. That makes 243 tiles.",
      W("k1", "4 × 0.25 = 1"), W("k2", "60 × 4 = 240"), W("k3", "0.75 × 4 = 3"),
      ANS("k", "60.75 ÷ 0.25 = 243"), M("k", "243", "circle")),
    B("Check: 243 tiles, each a quarter of a square metre, cover 243 divided by 4, which is 60.75. Just right.",
      W("c", "243 ÷ 4 = 60.75")),
    B("If you forget the pillar, you get 63 times 4, which is 252 tiles. 9 of those would have nowhere to go.",
      W("t", "63 × 4 = 252")),
    B("So: area to cover, divided by the area of 1 tile. Dividing by a quarter is the same as multiplying by 4."),
]))

beats, A, Pc, R = takeaway(
    "Riya's floor is 12 metres long and 8 metres wide. A square rangoli mat of side 3 metres lies in the centre. She paints the rest, and 1 can of paint covers 15 square metres. How many cans?",
    ["Floor 12 m × 8 m, square mat of side 3 m", "1 can covers 15 sq. m. How many cans?"],
    rect("12 m", "8 m", "mat: side 3 m"),
    "floor", 12, 8, "mat", 3, 3, SQM,
    B("Before we can count cans, we need the area that gets painted: the floor, take away the mat.",
      L("plan", "Painted area = floor − mat")),
    piece_ask=True)
LESSONS[P + "479434d4-e1db-40c5-bd0b-8dc65aa1efe9"] = lesson(*(beats + [
    B("Now the cans. Each one covers 15 square metres. Let's count up: 5 cans cover 75, and 6 cans cover 90.",
      W("k1", "15 × 5 = 75"), W("k2", "15 × 6 = 90")),
    B("Riya has 87 square metres to paint. How many cans must she buy?",
      W("k3", "87 − 75 = 12"),
      ask=choose(["5 cans", "6 cans", "87 cans"], 1,
                 "5 cans reach only 75 square metres, so 12 square metres of floor would stay bare. She cannot buy part of a can, so she needs the next whole can.")),
    B("6 cans. The sixth can will only be partly used, but she still has to buy it.",
      ANS("a", "Cans needed = 6", True), M("a", "6", "circle")),
    B("That is the trap in this question. 87 divided by 15 is 5 and a bit, and it is tempting to say 5. When you are buying whole cans, a bit over means 1 more can."),
    B("So: find the area, divide by what 1 can covers, and round up if there is anything left over."),
]))

beats, A, Pc, R = takeaway(
    "Ravi's father is painting a wall, 6 metres long and 4 metres high. A square window of side 1 metre is not painted. 1 can of paint covers 5 square metres. How many cans must he buy?",
    ["Wall 6 m × 4 m, square window of side 1 m", "1 can covers 5 sq. m. How many cans?"],
    rect("6 m", "4 m", "window: side 1 m"),
    "wall", 6, 4, "window", 1, 1, SQM,
    B("First we need an area. Which area gets painted?",
      ask=choose(["wall + window", "wall − window", "wall only"], 1,
                 "No paint goes on the window. So the window's area comes off the wall's area.")),
    piece_say="Now the window. It is a square of side 1, so its area is 1 times 1, which is just 1 square metre.")
LESSONS[P + "e0f58b33-8f10-4705-99cb-16d829fcb807"] = lesson(*(beats + [
    B("Now the cans. Each one covers 5 square metres. 4 cans cover 20, and 5 cans cover 25.",
      W("k1", "5 × 4 = 20"), W("k2", "5 × 5 = 25")),
    B("The wall needs 23 square metres of paint. How many cans?",
      W("k3", "23 − 20 = 3"),
      ask=choose(["4 cans", "5 cans", "23 cans"], 1,
                 "4 cans cover only 20 square metres. That leaves 3 square metres of wall with no paint, and a shop will not sell part of a can.")),
    B("5 cans. The last one will not be used up, but it is needed.",
      ANS("a", "Cans needed = 5", True), M("a", "5", "circle")),
    B("Watch for two slips. 23 is the area, not the number of cans. And 4 is what you get by ignoring the leftover, which leaves the wall unfinished."),
    B("So: area to paint, divided by what 1 can covers. If it does not divide exactly, buy 1 more."),
]))

beats, A, Pc, R = takeaway(
    "Riya's bedroom is 12 metres long and 9 metres wide. A carpet, 8 metres by 5 metres, lies in the centre. The rest of the floor gets square tiles of side 50 centimetres. How many tiles?",
    ["Room 12 m × 9 m, carpet 8 m × 5 m", "Square tiles of side 50 cm. How many?"],
    rect("12 m", "9 m", "carpet: 8 m × 5 m"),
    "room", 12, 9, "carpet", 8, 5, SQM,
    B("Which part of the floor gets tiles?",
      ask=choose(["room + carpet", "room − carpet", "carpet only"], 1,
                 "Tiles go on the bare floor, not under the carpet. So the carpet's area comes off the room's area.")))
LESSONS[P + "3a609c88-0621-47d8-b866-16edb84e694e"] = lesson(*(beats + [
    B("Now the tiles. Careful: the room is measured in metres, but the tile is in centimetres. 50 centimetres is half a metre, so 2 tiles fit along 1 metre.",
      L("k1", "50 cm + 50 cm = 100 cm = 1 m")),
    B("So how many tiles cover 1 whole square metre?",
      FIG("f2", {"kind": "grid", "rows": 2, "cols": 2, "note": "1 square metre"}),
      ask=choose(["2", "4", "50"], 1,
                 "2 tiles fit along the metre, and 2 rows fit down it. 2 rows of 2 makes 4 tiles.")),
    B("4 tiles for each square metre, and there are 68 square metres. 60 times 4 is 240, and 8 times 4 is 32. That makes 272 tiles.",
      W("k2", "60 × 4 = 240"), W("k3", "8 × 4 = 32"), ANS("k", "68 × 4 = 272"), M("k", "272", "circle")),
    B("Two slips to watch. Saying 2 tiles for a square metre forgets the second row. And tiling under the carpet gives 108 times 4, which is 432.",
      W("t", "108 × 4 = 432")),
    B("So: make the units match, find how many tiles fill 1 square metre, then multiply by the area."),
]))

beats, A, Pc, R = takeaway(
    "Riya's room is 12 metres long and 8 metres wide, with a square rangoli of side 3 metres in one corner. The rest of the floor gets small square tiles of side 50 centimetres. How many tiles?",
    ["Room 12 m × 8 m, square rangoli of side 3 m", "Square tiles of side 50 cm. How many?"],
    rect("12 m", "8 m", "rangoli: side 3 m"),
    "room", 12, 8, "rangoli", 3, 3, SQM,
    B("Two jobs. First the area to tile: the room, take away the rangoli. Then count how many tiles fill it.",
      L("plan", "Area to tile = room − rangoli")),
    piece_ask=True)
LESSONS[P + "938739a9-0383-4487-970b-3198c1924aea"] = lesson(*(beats + [
    B("Now one tile. Its side is 50 centimetres, which is 0.5 of a metre. So its area is 0.5 times 0.5. What is that?",
      L("k0", "50 cm = 0.5 m"),
      ask=choose(["0.25", "1", "2.5"], 0,
                 "Half of a half is a quarter. And a quarter, written as a decimal, is 0.25.")),
    B("0.25 of a square metre, a quarter. So 4 tiles cover 1 whole square metre.",
      W("k1", "0.5 × 0.5 = 0.25"), W("k2", "4 × 0.25 = 1")),
    B("87 square metres, with 4 tiles in each. 80 times 4 is 320, and 7 times 4 is 28. That makes 348 tiles.",
      W("k3", "80 × 4 = 320"), W("k4", "7 × 4 = 28"), ANS("k", "87 × 4 = 348"), M("k", "348", "circle")),
    B("The big trap is the units. If you divide 87 by 50, you are mixing metres with centimetres. Always change the tile into metres first."),
    B("And remember the rangoli. Without taking it away you would get 96 times 4, which is 384.",
      W("t", "96 × 4 = 384")),
    B("So: area to tile, in square metres, times the number of tiles in 1 square metre."),
]))

beats, A, Pc, R = takeaway(
    "Riya's room is 12 metres long and 8 metres wide. A square rangoli mat of side 3 metres sits in one corner. Tiles cover the rest, and each tile covers 500 square centimetres. How many tiles?",
    ["Room 12 m × 8 m, square mat of side 3 m", "Each tile covers 500 sq. cm. How many tiles?"],
    rect("12 m", "8 m", "mat: side 3 m"),
    "room", 12, 8, "mat", 3, 3, SQM,
    B("Two jobs. First the area to tile: the room, take away the mat. Then see how many tiles are needed.",
      L("plan", "Area to tile = room − mat")),
    piece_ask=True)
LESSONS[P + "46c8ae29-a5b7-437c-ae3e-616613f7a121"] = lesson(*(beats + [
    B("Here is the catch. The floor is in square metres, but the tile is in square centimetres. How many square centimetres are there in 1 square metre?",
      ask=choose(["100", "1,000", "10,000"], 2,
                 "A square metre is 100 centimetres long and 100 centimetres wide. 100 rows of 100 makes 10,000.")),
    B("10,000. A square metre is 100 centimetres each way, and 100 times 100 is 10,000.",
      W("k1", "100 × 100 = 10,000"), L("k0", "1 sq. m = 10,000 sq. cm")),
    B("So how many tiles fit in 1 square metre? 10,000 divided by 500 is 20.",
      W("k2", "10,000 ÷ 500 = 20")),
    B("20 tiles for each square metre, and 87 square metres to cover. 87 times 2 is 174, so 87 times 20 is 1,740 tiles.",
      W("k3", "87 × 2 = 174"), ANS("k", "87 × 20 = 1,740"), M("k", "1,740", "circle")),
    B("Check the long way. 87 square metres is 87 times 10,000 square centimetres. Divide that by 500 and we get 1,740 again.",
      W("c1", "87 × 10,000 = 8,70,000"), W("c2", "8,70,000 ÷ 500 = 1,740")),
    B("See the 174 we met on the way? It is one of the choices. It catches anyone who thinks a square metre is only 1,000 square centimetres."),
    B("When the units do not match, change one of them first. And for area, 1 square metre is 10,000 square centimetres, not 100."),
]))

beats, A, Pc, R = takeaway(
    "Priya's kitchen floor is 8 metres by 6 metres, with a square pillar of side 1 metre in the centre. The rest gets square tiles of side 25 centimetres, at 12 rupees a tile. What is the cost?",
    ["Floor 8 m × 6 m, square pillar of side 1 m", "Tiles of side 25 cm, ₹12 each. Cost = ?"],
    rect("8 m", "6 m", "pillar: side 1 m"),
    "floor", 8, 6, "pillar", 1, 1, SQM,
    B("There are three jobs here: the area to tile, the number of tiles, and the cost. Which one has to come first?",
      ask=choose(["the cost", "the number of tiles", "the area to tile"], 2,
                 "We cannot price the tiles until we have counted them, and we cannot count them until we know how much floor they cover. So the area comes first.")),
    piece_say="The pillar is a square of side 1, so its area is 1 times 1, which is just 1 square metre.")
LESSONS[P + "65379f85-e849-4fde-8113-e6a098a7febf"] = lesson(*(beats + [
    B("Now the tiles. Each is 25 centimetres wide, and 4 of them make 100 centimetres, which is 1 metre. So 4 tiles fit along a metre.",
      W("k1", "4 × 25 = 100")),
    B("How many tiles cover 1 whole square metre?",
      FIG("f2", {"kind": "grid", "rows": 4, "cols": 4, "note": "1 square metre"}),
      ask=choose(["4", "8", "16"], 2,
                 "4 tiles fit along the metre, and 4 rows fit down it. 4 rows of 4 makes 16.")),
    B("16 tiles for each square metre, and 47 square metres. 47 times 10 is 470, and 47 times 6 is 282. Together, 752 tiles.",
      W("k2", "47 × 10 = 470"), W("k3", "47 × 6 = 282"), W("k", "47 × 16 = 470 + 282 = 752")),
    B("Last job, the cost. 752 tiles at 12 rupees each. 752 times 10 is 7,520, and 752 times 2 is 1,504. Together, 9,024 rupees.",
      W("m1", "752 × 10 = 7,520"), W("m2", "752 × 2 = 1,504"),
      ANS("m", "752 × 12 = 7,520 + 1,504 = 9,024"), M("m", "9,024", "circle")),
    B("If you forget the pillar, 48 times 16 is 768 tiles, and the bill comes to 9,216. That is one of the choices, so take care.",
      W("t1", "48 × 16 = 768"), W("t2", "768 × 12 = 9,216")),
    B("A long question is just short jobs in a row: area, then tiles, then cost. Finish one before starting the next."),
]))
