"""Lessons by rule for the two generated families in gr4_units.

    bags     "<name> has N bags of <stuff>, each weighing K kg G g. What is the total weight in grams?"
    glasses  "A <vessel> holds L litres of water. How many glasses of M ml each can be filled?"

Each rule reads the numbers from the question, works out every line, and adapts the words.
"""
import re

from g4_units_lib import a, b, c, g, l, n, option_texts, pick, u, w

BAGS = re.compile(r"(\w+) has (\d+) bags of (\w+), each weighing (\d+) kg (\d+) g\. What is the total weight in grams\?")
GLASSES = re.compile(r"A (\w+) holds (\d+) litres of water\. How many glasses of (\d+) ml each can be filled\?")


def bags(q):
    m = BAGS.fullmatch(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    name, stuff = m.group(1), m.group(3)
    nb, k, gr = int(m.group(2)), int(m.group(4)), int(m.group(5))
    k000 = k * 1000
    one = k000 + gr
    pa, pb = k000 * nb, gr * nb
    total = pa + pb
    trap = str(one) in option_texts(q)

    open_say = pick(qid, "open", [
        "%s has %d bags of %s. Each bag weighs %d kilograms %d grams. We want the weight of all the bags, in grams." % (name, nb, stuff, k, gr),
        "Here are %d bags of %s, and each one weighs %d kilograms %d grams. Our job is to find the total weight in grams." % (nb, stuff, k, gr),
        "%s is carrying %d bags of %s. Every bag weighs %d kilograms %d grams. How many grams is that altogether?" % (name, nb, stuff, k, gr),
    ])
    one_say = "Now add on the %d grams. One bag weighs %d grams." % (gr, one)
    if trap:
        one_say += pick(qid, "trap", [
            " Careful: %d is one of the choices, but that is only one bag." % one,
            " Don't stop here, though. %d is just one bag, and it is sitting in the choices to catch us." % one,
        ])
    times_say = ("There are 2 bags, so we need %d times 2. That is doubling. Let's do it in two easy parts." % one) if nb == 2 else \
        ("There are %d bags, so we need %d times %d. Let's do it in two easy parts." % (nb, one, nb))
    end_say = pick(qid, "end", [
        "The plan to remember: change everything into the small unit first, then multiply.",
        "So when kilograms and grams are mixed, make it all grams first. Then multiply by the number of bags.",
        "Two steps did it: one bag into grams, then times the number of bags. You can use that every time.",
    ])
    return [
        b(open_say, g("q", "%d bags, each %d kg %d g. Total in grams?" % (nb, k, gr))),
        b(pick(qid, "plan", [
            "The answer has to be in grams, but each bag is given in kilograms and grams. So what shall we do first?",
            "Each bag's weight mixes two units, kilograms and grams. What is a good first step?",
            "We want grams at the end. Right now each bag is in kilograms and grams. Where shall we begin?",
        ]),
          ask=c("change one bag into grams", ["multiply %d by %d" % (k, nb), "add %d and %d" % (k, gr)],
                "Kilograms and grams are mixed up here. If we turn one bag into grams first, the rest is one easy multiplication.")),
        b("1 kilogram is 1000 grams. So %d kilograms is %d grams." % (k, k000),
          u("q", "%d kg" % k), l("f", "1 kg = 1000 g"), w("c1", "%d × 1000 = %d" % (k, k000))),
        b(one_say, w("c2", "%d + %d = %d" % (k000, gr, one)), n("c2", str(one), "one bag", "below")),
        b(times_say, w("t", "%d × %d = ?" % (one, nb))),
        b("First the thousands. What is %d times %d?" % (k000, nb),
          ask=c(str(pa), [str(k * nb * 100), str(k000 + nb)],
                "Work out %d times %d first. Then put the three zeros back on the end." % (k, nb))),
        b("%d times %d is %d. And %d times %d is %d." % (k000, nb, pa, gr, nb, pb),
          w("p1", "%d × %d = %d" % (k000, nb, pa)), w("p2", "%d × %d = %d" % (gr, nb, pb))),
        b("Put the two parts together. %d plus %d makes %d. So the %d bags weigh %d grams." % (pa, pb, total, nb, total),
          w("s", "%d + %d = %d" % (pa, pb, total)), a("ans", "%d g" % total)),
        b(end_say),
    ]


def glasses(q):
    m = GLASSES.fullmatch(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    vessel, litres, ml = m.group(1), int(m.group(2)), int(m.group(3))
    total = litres * 1000
    beats = [
        b(pick(qid, "open", [
            "A %s holds %d litres of water. Each glass takes %d millilitres. How many glasses can we fill?" % (vessel, litres, ml),
            "We have a %s with %d litres of water, and glasses that hold %d millilitres each. Let's find how many glasses it fills." % (vessel, litres, ml),
        ]), g("q", "%d litres. Glasses of %d ml. How many?" % (litres, ml))),
        b(pick(qid, "plan", [
            "One amount is in litres and the other is in millilitres. What must we do before we share the water out?",
            "Look at the units: litres for the %s, millilitres for the glasses. So what is our first job?" % vessel,
            "Litres and millilitres do not match yet. What should we do first?",
        ]),
          ask=c("make both millilitres", ["divide %d by %d" % (litres, ml), "multiply %d by %d" % (litres, ml)],
                "We cannot match litres against millilitres straight away. Let's turn the litres into millilitres, so both are in the same unit.")),
        b("1 litre is 1000 millilitres. So %d litres is %d millilitres." % (litres, total),
          u("q", "%d litres" % litres), l("f", "1 litre = 1000 ml"), w("c1", "%d × 1000 = %d" % (litres, total))),
    ]
    if 1000 % ml == 0:
        per = 1000 // ml
        count = litres * per
        beats += [
            b("Now think about just 1 litre, which is 1000 millilitres. How many glasses of %d does it fill?" % ml,
              ask=c(str(per), [str(per + 1), str(per * 2)],
                    "Count up in steps of %d until you reach 1000. The number of steps is the number of glasses." % ml)),
            b("%d glasses of %d make 1000. So every litre fills %d glasses." % (per, ml, per),
              w("c2", "%d × %d = 1000" % (per, ml)), n("c2", "1000", "1 litre", "below")),
            b("We have %d litres, and each one fills %d glasses. %d times %d is %d." % (litres, per, litres, per, count),
              w("c3", "%d × %d = %d" % (litres, per, count))),
            b("So %d glasses can be filled." % count, a("ans", "%d glasses" % count)),
            b("Let's check. %d glasses of %d millilitres make %d millilitres. That is the whole %s, so it fits." % (count, ml, total, vessel),
              w("ck", "%d × %d = %d" % (count, ml, total))),
            b(pick(qid, "end", [
                "Remember: make the units the same first, then see how many lots fit.",
                "So the plan is: same units first, then count how many glasses fit in.",
                "Litres into millilitres first, then share. That plan works for every question like this.",
            ])),
        ]
        return beats
    if total % 100 or ml % 100:
        return None
    small_total, small_ml = total // 100, ml // 100
    count, left = divmod(small_total, small_ml)
    used = count * ml
    spare = total - used
    tens, ones = count // 10 * 10, count % 10
    if tens and ones:
        near_say = "%d times %d is %d, and %d times %d is %d more. So %d times %d is %d. How much of the %d is left over?" % (
            small_ml, tens, small_ml * tens, small_ml, ones, small_ml * ones, small_ml, count, count * small_ml, small_total)
        near_ops = [w("c3a", "%d × %d = %d" % (small_ml, tens, small_ml * tens)),
                    w("c3b", "%d × %d = %d" % (small_ml, ones, small_ml * ones)),
                    w("c3", "%d × %d = %d" % (small_ml, count, count * small_ml))]
    else:
        near_say = "%d times %d is %d. So how much of the %d is left over?" % (small_ml, count, count * small_ml, small_total)
        near_ops = [w("c3", "%d × %d = %d" % (small_ml, count, count * small_ml))]
    beats += [
        b("Now, how many lots of %d fit into %d? Take two zeros off both numbers. It is the same as %d divided by %d." % (ml, total, small_total, small_ml),
          w("c2", "%d ÷ %d = %d ÷ %d" % (total, ml, small_total, small_ml))),
        b(near_say, *near_ops,
          ask=c(str(left), ["0", str(left + 1)],
                "Count on from %d up to %d. That little bit is what is left over." % (count * small_ml, small_total))),
        b("So %d glasses get filled, and a little water is left. %d times %d is %d, which leaves %d millilitres." % (count, ml, count, used, spare),
          w("c4", "%d × %d = %d" % (ml, count, used)), w("c5", "%d − %d = %d" % (total, used, spare))),
        b("Careful here: %d millilitres is not enough for another glass of %d. So we do not count it." % (spare, ml),
          u("c5", "= %d" % spare)),
        b("So %d full glasses can be filled." % count, a("ans", "%d glasses" % count)),
        b("Remember: make the units the same first, then see how many full lots fit. A part of a glass does not count."),
    ]
    return beats


RULES = [bags, glasses]


def rule_lessons(questions):
    out = {}
    for q in questions:
        for rule in RULES:
            beats = rule(q)
            if beats:
                out[q["id"]] = beats
                break
    return out
