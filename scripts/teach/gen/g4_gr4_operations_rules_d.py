"""Rule lessons for the generated word-problem families (Grade 4 operations)."""
from g4_gr4_operations_common import (B, W, ANSR, GIVEN, M, pick, ask_of, times_work, lesson)


def unit_cost(q, n, things, total, thing):
    """If n things cost Rs.total, what is the cost of one thing?"""
    qid = q["id"]
    each = total // n
    beats = [B("Here is what we know. %d %s cost %d rupees altogether. We want the cost of just one %s." % (n, things, total, thing),
               GIVEN("q", "%d %s cost %d rupees" % (n, things, total), label=True), W("q2", "1 %s costs ?" % thing, label=True))]
    beats.append(B("Every %s costs the same. So how do we find the cost of one?" % thing,
                   ask=ask_of(qid, "a1", "%d ÷ %d" % (total, n), ["%d + %d" % (total, n), "%d × %d" % (total, n)],
                              "We are sharing %d rupees equally among %d %s. Sharing equally means dividing." % (total, n, things))))
    beats.append(B("Sharing %d rupees equally among %d %s is a division. %d divided by %d." % (total, n, things, total, n),
                   W("d", "%d ÷ %d = ?" % (total, n))))
    beats.append(B(pick(qid, "think", ["To divide, think of times. %d times what number makes %d?",
                                       "Here is a handy trick: turn it into a times question. %d times what makes %d?"]) % (n, total),
                   W("t", "%d × ? = %d" % (n, total))))
    if each == 9 and n > 10:
        beats.append(B("Try 10 first, because it is easy. %d times 10 is %d. That is a little too big." % (n, n * 10),
                       W("t10", "%d × 10 = %d" % (n, n * 10))))
        beats.append(B("It is too big by exactly one lot of %d, because %d take away %d is %d. So we need 9 lots, not 10." % (n, n * 10, n, total),
                       W("t9", "%d − %d = %d" % (n * 10, n, total)), W("tt", "%d × 9 = %d" % (n, total))))
    elif n <= 10:
        beats.append(B("Say the %d times table until you reach %d. %d times %d is %d. There it is." % (n, total, n, each, total),
                       W("tt", "%d × %d = %d" % (n, each, total)), M("tt", "× %d" % each, "underline")))
    else:
        say, ops = times_work(n, each, "tt")
        beats.append(B("Let us try %d. " % each + say + " That is exactly what we need.", *ops))
    beats.append(B("So %d divided by %d is %d. One %s costs %d rupees." % (total, n, each, thing, each),
                   *ANSR("ans", "%d ÷ %d = %d" % (total, n, each), str(each))))
    beats.append(B("Does that make sense? One %s must cost much less than all %d together, and %d is much less than %d. Yes." % (thing, n, each, total)))
    beats.append(B(pick(qid, "sum", ["So when you know the cost of many and want the cost of one, divide the total by how many there are.",
                                     "The plan: the cost of one is the total cost divided by the number of things."])))
    return lesson(*beats, origin="rule")


def think_number(q, n, a, b):
    """Think of a number n. Multiply it by a and add b."""
    qid = q["id"]
    p = n * a
    r = p + b
    beats = [B("Here is a little number game. Start with %d. Multiply it by %d. Then add %d." % (n, a, b),
               GIVEN("q", "Start with %d.  × %d  then  + %d" % (n, a, b), label=True))]
    beats.append(B("There are two jobs to do. Which one comes first?",
                   ask=ask_of(qid, "a1", "%d × %d" % (n, a), ["%d + %d" % (a, b), "%d + %d" % (n, b)],
                              "Do the jobs in the order they are given. The first job is to multiply %d by %d. The adding comes after." % (n, a))))
    say, ops = times_work(n, a, "p")
    beats.append(B("First job: multiply. " + say, *ops))
    beats.append(B("Careful now. The add %d is done to our new number, %d. It is not added to the %d we multiplied by." % (b, p, a),
                   M("p", str(p), "circle", ops[-1]["text"].count(str(p)))))
    beats.append(B("Second job: add %d. %d plus %d is %d." % (b, p, b, r), *ANSR("ans", "%d + %d = %d" % (p, b, r), str(r))))
    beats.append(B("Let us write the whole game on one line. %d times %d, plus %d, equals %d." % (n, a, b, r),
                   W("all", "%d × %d + %d = %d" % (n, a, b, r))))
    beats.append(B(pick(qid, "sum", ["So follow the instructions one at a time, in the order they are given.",
                                     "One job at a time, in order. Multiply first, then add."])))
    return lesson(*beats, origin="rule")


def total_cost(q, name, n, things, price):
    """Name buys n things at Rs.price each. What is the total cost?"""
    qid = q["id"]
    p = n * price
    beats = [B("%s buys %d %s, and each one costs %d rupees. We want the total cost." % (name, n, things, price),
               GIVEN("q", "%d %s at %d rupees each" % (n, things, price), label=True), W("q2", "Total cost = ?", label=True))]
    beats.append(B("Every one of the %d %s costs %d rupees. Which sum gives the total?" % (n, things, price),
                   ask=ask_of(qid, "a1", "%d × %d" % (n, price), ["%d + %d" % (n, price)],
                              "Adding %d and %d would mix up %s and rupees. We need %d lots of %d rupees, and lots of means multiply." % (n, price, things, n, price))))
    beats.append(B("We need %d lots of %d. That is a times sum." % (n, price), W("t", "%d × %d = ?" % (n, price))))
    if n > 10 and price > 10:
        t, o = n - n % 10, n % 10
        beats.append(B("%d is 10 and %d. So work out 10 lots first, then %s." % (n, o, "1 more lot" if o == 1 else "the other %d lots" % o),
                       W("sp", "%d = %d + %d" % (n, t, o))))
        beats.append(B("10 lots of %d is %d. And %s." % (price, 10 * price, "1 more lot is just %d" % price if o == 1 else "%d times %d is %d" % (o, price, o * price)),
                       W("pa", "10 × %d = %d" % (price, 10 * price)), W("pb", "%d × %d = %d" % (o, price, o * price))))
        beats.append(B("Add the two parts. %d and %d make %d." % (10 * price, o * price, p),
                       W("p", "%d + %d = %d" % (10 * price, o * price, p))))
        lead = ""
    else:
        say, ops = times_work(n, price, "p")
        lead = ""
        if len(ops) > 1:
            beats.append(B(say, *ops))
        else:
            lead = say + " "
    beats.append(B(lead + "So the total cost is %d rupees." % p, *ANSR("ans", "%d × %d = %d" % (n, price, p), str(p))))
    beats.append(B("Does that make sense? %d %s must cost a lot more than one, and %d is a lot more than %d. Yes." % (n, things, p, price)))
    beats.append(B(pick(qid, "sum", ["So when every item costs the same, the total is the number of items times the price of one.",
                                     "The plan: number of things, times the price of each."])))
    return lesson(*beats, origin="rule")


def percent_sale(q, name, thing, cost, pct, kind):
    """Bought for Rs.cost, sold at a profit/loss of pct%. Selling price?"""
    qid = q["id"]
    part = cost * pct // 100
    sp = cost + part if kind == "profit" else cost - part
    sym = "+" if kind == "profit" else "−"
    beats = [B("%s pays %d rupees for the %s, then sells it at a %s of %d percent. We want the selling price." % (name, cost, thing, kind, pct),
               GIVEN("q", "Cost %d rupees, %s %d%%" % (cost, kind, pct), label=True), W("q2", "Selling price = ?", label=True))]
    if cost == 100:
        beats.append(B("Percent means out of every 100. So %d percent means %d rupees for every 100 rupees." % (pct, pct),
                       M("q", "%d%%" % pct, "underline"), W("pc", "% means out of 100", label=True)))
        beats.append(B("The %s cost exactly 100 rupees. So the %s is %d rupees." % (thing, kind, part), W("p", "%d%% of %d = %d" % (pct, cost, part))))
    elif pct == 10:
        beats.append(B("Percent means out of every 100. 10 out of 100 is one tenth. So 10 percent of a number is the number divided by 10.",
                       M("q", "%d%%" % pct, "underline"), W("pc", "% means out of 100", label=True)))
        beats.append(B("%d divided by 10 is %d. So the %s is %d rupees." % (cost, part, kind, part),
                       W("pa", "%d ÷ 10 = %d" % (cost, part)), W("p", "%d%% of %d = %d" % (pct, cost, part))))
    elif pct == 25:
        half = cost // 2
        beats.append(B("Percent means out of every 100. 25 out of 100 is one quarter. To find a quarter, halve the number, then halve it again.",
                       M("q", "%d%%" % pct, "underline"), W("pc", "% means out of 100", label=True)))
        beats.append(B("Half of %d is %d. Half of %d is %d. So the %s is %d rupees." % (cost, half, half, part, kind, part),
                       W("pa", "%d ÷ 2 = %d" % (cost, half)), W("pb", "%d ÷ 2 = %d" % (half, part)), W("p", "%d%% of %d = %d" % (pct, cost, part))))
    else:
        return None
    if kind == "profit":
        if_not = "A profit means %s gets more money back than was paid. So the %d is added to the cost." % (name, part)
        others = ["%d − %d" % (cost, part), "%d × %d" % (cost, part)]
        why = "A profit means selling for more than the cost. So add the profit to the cost."
    else:
        if_not = "A loss means %s gets less money back than was paid. So the %d is taken away from the cost." % (name, part)
        others = ["%d + %d" % (cost, part), "%d ÷ %d" % (cost, part)]
        why = "A loss means selling for less than the cost. So take the loss away from the cost."
    beats.append(B("Now, the selling price. Which sum do we need?",
                   ask=ask_of(qid, "a1", "%d %s %d" % (cost, sym, part), others, if_not)))
    beats.append(B(why, W("f", "Selling price = cost %s %s" % (sym, kind), label=True)))
    beats.append(B("%d %s %d is %d. So the selling price is %d rupees." % (cost, "plus" if kind == "profit" else "take away", part, sp, sp),
                   *ANSR("ans", "%d %s %d = %d" % (cost, sym, part, sp), str(sp))))
    beats.append(B("Careful with the trap. %d is only the %s. The question asks for the selling price, which is %d." % (part, kind, sp)))
    beats.append(B("So find the %s first, then %s the cost." % (kind, "add it to" if kind == "profit" else "take it away from")))
    return lesson(*beats, origin="rule")
