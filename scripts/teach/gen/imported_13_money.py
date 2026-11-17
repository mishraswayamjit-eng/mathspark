"""Batch 13: money stories with a percent in them.

Three story shapes come up again and again, so each has one builder that is fed
the question's numbers and words and computes every board line:
  pct_first   a percent of the money, then a fixed amount
  fixed_first a fixed amount, then a percent of what is left
  two_pct     a percent, then a percent of what is left (and perhaps one more step)
"""
from imported_13_lib import ANS, B, D, GIVEN, M, N, P, RING, W, ask, lesson, mon, paise_words, pick, rs

LESSONS = {}


# ── Turning a percent into rupees ────────────────────────────────────────────

def pct(qid, p, base, id, lead, label):
    """Beats that find p% of base the way a child would, and the value.

    The result line has id `id`; its value carries a small note, `label`.
    """
    p = int(p)
    base = D(base)
    v = base * p / 100
    b, vv = mon(base), mon(v)
    lead = (lead + " ") if lead else ""

    def done(text):
        return [W(id, text), N(id, "= " + vv, label, nth=text.count("= " + vv))]

    if p == 50:
        text = "50%% of %s = %s ÷ 2 = %s" % (b, b, vv)
        return [B("%s50 percent is one half, and half of %s is %s." % (lead, b, vv), *done(text))], v
    if p == 25 and v == v.to_integral_value():
        text = "25%% of %s = %s ÷ 4 = %s" % (b, b, vv)
        say = pick(qid, id + "q", [
            "%s25 percent is one quarter, so we divide by 4. %s divided by 4 is %s.",
            "%s25 percent is a quarter, 1 of 4 equal parts. So we want %s divided by 4, which is %s.",
        ]) % (lead, b, vv)
        return [B(say, *done(text))], v
    if p == 25:
        h = base / 2
        text = "25%% of %s = %s ÷ 2 = %s" % (b, mon(h), vv)
        return [
            B("%s25 percent is one quarter. To find a quarter, halve, and then halve again: half of %s is %s." % (lead, b, mon(h)),
              W(id + "h", "%s ÷ 2 = %s" % (b, mon(h)))),
            B("And half of %s is %s. That is %s." % (mon(h), vv, paise_words(v).replace(" rupees ", " rupees and ")),
              W(id, text), N(id, "= " + vv, label, nth=text.count("= " + vv)),
              W(id + "w", "%s = %s" % (rs(v), paise_words(v)), True)),
        ], v
    if p == 10:
        text = "10%% of %s = %s ÷ 10 = %s" % (b, b, vv)
        return [B("%s10 percent is one tenth, so we divide by 10. %s divided by 10 is %s." % (lead, b, vv), *done(text))], v
    if p in (20, 30, 40):
        k = p // 10
        t = mon(base / 10)
        text = "%d%% of %s = %d × %s = %s" % (p, b, k, t, vv)
        first = pick(qid, id + "t", [
            "%sFind 10 percent first, because that is easy: one tenth. %s divided by 10 is %s.",
            "%sStart small, with 10 percent. That is one tenth, so %s divided by 10 is %s.",
        ]) % (lead, b, t)
        second = pick(qid, id + "k", [
            "%d percent is %d lots of 10 percent. %d times %s is %s.",
            "Now build up. %d percent is %d times as much, and %d times %s is %s.",
        ]) % (p, k, k, t, vv)
        return [B(first, W(id + "t", "10%% of %s = %s" % (b, t))), B(second, *done(text))], v
    # Any other percent: find 1% first.
    u = mon(base / 100)
    text = "%d%% of %s = %d × %s = %s" % (p, b, p, u, vv)
    return [
        B("%sPercent means out of 100. So find 1 percent first: %s divided by 100 is %s." % (lead, b, u),
          W(id + "u", "1%% of %s = %s ÷ 100 = %s" % (b, b, u))),
        B("%d percent is %d of those. %d times %s is %s." % (p, p, p, u, vv), *done(text)),
    ], v


# ── A percent of the money, then a fixed amount ──────────────────────────────

def pct_first(qid, who, intro, given, S, p, first, t1, t2, f=None, items=None, n1=None, n2=None,
              verb1="went on", gone="is money that has been spent", after1=None, closing=None):
    S = D(S)
    if items:
        count, price, things = items
        f = D(count) * D(price)
    f = D(f)
    a = S * p / 100
    mid = S - a
    left = mid - f
    s, av, mv, fv, lv = mon(S), mon(a), mon(mid), mon(f), mon(left)

    if pick(qid, "ask1", [0, 1]) == 0:
        opening = B(first + " Is that the same as %d rupees?" % p,
                    W("m", "%d%% = %d out of every 100" % (p, p), True),
                    ask=ask("No: it is a share of the %s" % rs(S), ["Yes: take %s away" % rs(p)],
                            "Percent means out of every 100. So %d percent is %d rupees from every 100 rupees, and %s has more than 100. It is a share of the whole %s." % (p, p, who, s)))
    else:
        opening = B(first + " What must we find before we can subtract anything?",
                    ask=ask("how many rupees %d%% of %s is" % (p, s),
                            ["%s − %d" % (s, p), "nothing: we can subtract straight away"],
                            "%d percent is not %d rupees. It is a share of the %s, so first we must turn that share into rupees." % (p, p, s)))

    work, _ = pct(qid, p, S, "p", "", n1 or t1.replace("the ", "", 1))
    beats = [B(intro, GIVEN("q", given, True)), opening] + work
    beats.append(B("So %s rupees %s %s. What do we do with that %s?" % (av, verb1, t1, av),
                   ask=ask("take it away from %s" % s, ["nothing: %s is the answer" % av, "add it to %s" % s],
                           "That %s %s. The question asks what is left, so it comes off the %s." % (av, gone, s))))
    beats.append(B("%s minus %s is %s. That is what %s has %s." % (s, av, mv, who, after1 or ("after " + t1)),
                   W("s1", "%s − %s = %s" % (s, av, mv))))
    if items:
        beats.append(B("Next, %s: %d of them at %s rupees each. %d times %s is %s." % (t2, count, mon(price), count, mon(price), fv),
                       W("i", "%d × %s = %s" % (count, mon(price), fv)), N("i", "= " + fv, n2 or things)))
        beats.append(B("Take that away too: %s minus %s is %s. So %s has %s rupees left." % (mv, fv, lv, who, lv),
                       ANS("a", "%s − %s = %s" % (mv, fv, rs(left))), RING("a", rs(left))))
    else:
        beats.append(B("Then %s: %s minus %s is %s. So %s has %s rupees left." % (t2, mv, fv, lv, who, lv),
                       ANS("a", "%s − %s = %s" % (mv, fv, rs(left))), RING("a", rs(left))))
    beats.append(B("Check: %s for %s, %s for %s, and %s left over. Together they make %s, all the money from the start." % (
        av, t1, fv, t2, lv, s), W("c", "%s + %s + %s = %s" % (av, fv, lv, s))))
    beats.append(B(closing or pick(qid, "close", [
        "So with a percent in a money story: turn the percent into rupees first, then take away everything that was spent.",
        "The plan: find the percent as an amount of rupees, then subtract each thing that was spent, one at a time.",
        "Remember: a percent is a share, not a number of rupees. Change it into rupees, and the rest is plain subtraction.",
    ])))
    return lesson(*beats)


LESSONS[P + "41d5719f-7015-4013-acad-ae4e3ff983b6"] = pct_first(
    P + "41d5719f", "Arjun",
    "Arjun is given 750 rupees. He spends 40 percent of it on a cricket bat, and then 120 rupees on cricket balls. How much does he have left?",
    "₹750. 40% on a bat, then ₹120 on balls.", 750, 40,
    "The bat cost 40 percent of the money.", "the bat", "the cricket balls", f=120, n1="bat")

LESSONS[P + "47c823d7-cf82-4c7f-bb5a-ff6d5018232e"] = pct_first(
    P + "47c823d7", "Samira",
    "Samira has 500 rupees at the Holi fair. She spends 40 percent on water balloons and colours, and then 75 rupees on gujiya. How much is left?",
    "₹500. 40% on balloons and colours, ₹75 on gujiya.", 500, 40,
    "The balloons and colours took 40 percent of her money.", "the balloons and colours", "the gujiya", f=75, n1="balloons, colours")

LESSONS[P + "564c2f73-d05c-42b5-a029-9f2fbcccbd59"] = pct_first(
    P + "564c2f73", "Pooja",
    "Pooja is given 900 rupees. She spends 30 percent on a salwar suit, and then 135 rupees on a box of jalebi. How much does she have left?",
    "₹900. 30% on a suit, then ₹135 on jalebi.", 900, 30,
    "The salwar suit cost 30 percent of the money.", "the salwar suit", "the jalebi", f=135, n1="suit")

LESSONS[P + "80fcbd7d-dc32-47f5-aed1-53356d70258f"] = pct_first(
    P + "80fcbd7d", "Kavya",
    "Kavya saved 1,200 rupees. She spends 25 percent of it on a storybook, and then gives 150 rupees to her brother. How much does she have left?",
    "₹1,200. 25% on a storybook, ₹150 to her brother.", 1200, 25,
    "The storybook cost 25 percent of her savings.", "the storybook", "the gift to her brother", f=150, n1="storybook")

LESSONS[P + "961784d1-eef0-482f-9709-42bd7ae234c5"] = pct_first(
    P + "961784d1", "Sanya",
    "Sanya is given 500 rupees. She spends 35 percent on a jhumka set, and then 80 rupees on a box of kaju katli. How much does she have left?",
    "₹500. 35% on jhumkas, then ₹80 on kaju katli.", 500, 35,
    "The jhumka set cost 35 percent of her money.", "the jhumka set", "the kaju katli", f=80, n1="jhumkas")

LESSONS[P + "9c324687-60cd-4e23-ac2c-e25e0afcb538"] = pct_first(
    P + "9c324687", "Deepa",
    "Deepa has 360 rupees for her art project. She spends 25 percent on paint brushes, and then 95 rupees on a sketch pad. How much is left?",
    "₹360. 25% on brushes, then ₹95 on a sketch pad.", 360, 25,
    "The paint brushes cost 25 percent of the money.", "the paint brushes", "the sketch pad", f=95, n1="brushes")

LESSONS[P + "a65eca9e-d42d-4aa8-9d1a-e89afed624bb"] = pct_first(
    P + "a65eca9e", "Kavya",
    "Kavya is given 400 rupees. She spends 25 percent on rangoli powders, and then 90 rupees on a box of ladoos. How much does she have left?",
    "₹400. 25% on rangoli powders, ₹90 on ladoos.", 400, 25,
    "The rangoli powders cost 25 percent of the gift.", "the rangoli powders", "the ladoos", f=90, n1="rangoli powders")

LESSONS[P + "b5ebd9fb-4dd8-463e-aa40-e03f2c039ce4"] = pct_first(
    P + "b5ebd9fb", "Kiran",
    "Kiran is given 900 rupees. He spends 20 percent on a rakhi gift set, and then 180 rupees on a box of kaju katli. How much does he have left?",
    "₹900. 20% on a gift set, ₹180 on kaju katli.", 900, 20,
    "The gift set cost 20 percent of the money.", "the gift set", "the kaju katli", f=180, n1="gift set",
    closing="Did you spot that both things cost 180 rupees? That was just chance. The plan stays the same: percent into rupees first, then subtract each thing.")

LESSONS[P + "e217c8f7-5bd1-487e-a8c4-e581dea4bc8f"] = pct_first(
    P + "e217c8f7", "Amit",
    "Amit has 450 rupees at the Navratri mela. He spends 20 percent on a dandiya set, and then 110 rupees on snacks. How much does he have left?",
    "₹450. 20% on a dandiya set, ₹110 on snacks.", 450, 20,
    "The dandiya set cost 20 percent of his money.", "the dandiya set", "the snacks", f=110, n1="dandiya set")

LESSONS[P + "319c3185-ce17-4b9a-b681-79b100a1d81d"] = pct_first(
    P + "319c3185", "Deepa",
    "Deepa is given 800 rupees. She spends 35 percent of it on a salwar kameez, and then buys 4 hair clips at 30 rupees each. How much is left?",
    "₹800. 35% on a salwar kameez. 4 clips at ₹30.", 800, 35,
    "The salwar kameez cost 35 percent of the money.", "the salwar kameez", "the hair clips",
    items=(4, 30, "hair clips"), n1="salwar kameez",
    closing="So: percent into rupees first, then subtract it. And when several things are bought at one price, multiply to get their cost before you subtract.")

LESSONS[P + "9a193d9f-f88d-424f-a5f7-564c229fd691"] = pct_first(
    P + "9a193d9f", "Kavya",
    "Kavya is given 1,200 rupees. She saves 25 percent in her piggy bank. From the rest she buys 8 packets of sparklers at 45 rupees each. How much is left?",
    "₹1,200. Saves 25%. 8 packets at ₹45 each.", 1200, 25,
    "Kavya puts 25 percent of the money in her piggy bank.", "the piggy bank", "the sparklers",
    items=(8, 45, "sparklers"), n1="saved", verb1="went into", gone="is money put away in the piggy bank",
    after1="after saving",
    closing="So: turn the percent into rupees, take it off, and then take off what was spent. Money saved and money spent both leave the purse.")


# ── A fixed amount, then a percent of what is left ───────────────────────────

def fixed_first(qid, who, intro, given, S, f, t1, p, t2, rest_words, n2=None, cost="cost", closing=None):
    S, f = D(S), D(f)
    R = S - f
    s, fv, r = mon(S), mon(f), mon(R)
    line_r = "%s − %s = %s" % (s, fv, r)
    work, b = pct(qid, p, R, "p", "", n2 or t2.replace("the ", "", 1))
    left = R - b
    bv, lv = mon(b), mon(left)
    whole = left == left.to_integral_value()
    beats = [
        B(intro, GIVEN("q", given, True)),
        B(pick(qid, "first", [
            "Go in the order of the story. First %s: %s minus %s is %s.",
            "Follow the story, one step at a time. First comes %s. %s minus %s is %s.",
        ]) % (t1, s, fv, r), W("r", line_r), N("r", "= " + r, "money left")),
        B("Next, %s %s %d percent of %s. %d percent of which amount?" % (t2, cost, p, rest_words, p),
          ask=ask("%s, the money left" % r, ["%s, the money at the start" % s, "%s, the price of %s" % (fv, t1)],
                  "Listen to the words again: %d percent of %s. After %s, %s has %s. So the percent is taken from %s, not from %s." % (
                      p, rest_words, t1, who, r, r, s))),
        B("That is the trap in this question: taking the percent of %s. But only %s is left, so we want %d percent of %s." % (s, r, p, r),
          M("r", "= " + r, "box")),
    ] + work
    last_say = "So %s %s %s rupees. Take that from the %s." % (t2, cost, bv, r)
    if whole:
        beats.append(B(last_say + " %s minus %s leaves %s with %s rupees." % (r, bv, who, lv),
                       ANS("a", "%s − %s = %s" % (r, bv, rs(left))), RING("a", rs(left))))
    else:
        beats.append(B(last_say + " %s minus %s leaves %s, which is %s." % (r, bv, lv, paise_words(left).replace(" rupees ", " rupees and ")),
                       ANS("a", "%s − %s = %s" % (r, bv, rs(left))), RING("a", rs(left)),
                       W("aw", "%s = %s" % (rs(left), paise_words(left)), True)))
    beats.append(B("Check: %s for %s, %s for %s, and %s left. Add them, and we are back at %s." % (fv, t1, bv, t2, lv, s),
                   W("c", "%s + %s + %s = %s" % (fv, bv, lv, s))))
    beats.append(B(closing or pick(qid, "close", [
        "When a story says a percent of the money left, find what is left first. The percent is always taken from that.",
        "So: follow the story in order, and always ask, percent of what? Here it was the money left, not the money at the start.",
    ])))
    return lesson(*beats)


LESSONS[P + "487eff09-bb59-41f7-b4ec-b4f3ad05ab93"] = fixed_first(
    P + "487eff09", "Vikram",
    "Vikram goes to a book fair with 750 rupees. He buys an encyclopedia for 300 rupees, and then spends 20 percent of his remaining money on bookmarks. How much is left?",
    "₹750. Book ₹300. Then 20% of the rest.", 750, 300, "the encyclopedia", 20, "the bookmarks", "his remaining money")

LESSONS[P + "60a5eead-ea7a-4c98-9424-d010b06d1afa"] = fixed_first(
    P + "60a5eead", "Farhan",
    "Farhan has 350 rupees. He buys a cricket cap for 80 rupees, and then spends 25 percent of the remaining money on samosas. How much does he have left?",
    "₹350. Cap ₹80. Then 25% of the rest.", 350, 80, "the cap", 25, "the samosas", "the remaining money",
    closing="When a story says a percent of the remaining money, find what remains first. And do not worry if the answer has paise in it: money often does.")

LESSONS[P + "6c57d8cc-3e3c-49e8-b5ce-e9c43f37a749"] = fixed_first(
    P + "6c57d8cc", "Neha",
    "Neha goes to a Pongal fair with 600 rupees. She buys kolam stencils for 150 rupees, and then spends 20 percent of the money she has left on juice and snacks. How much remains?",
    "₹600. Stencils ₹150. Then 20% of the rest.", 600, 150, "the stencils", 20, "the juice and snacks", "the money she has left",
    n2="juice, snacks")

LESSONS[P + "ca7ef302-364f-4678-9615-8ee267f16ce2"] = fixed_first(
    P + "ca7ef302", "Arjun",
    "Arjun goes to a stationery shop with 250 rupees. He buys a geometry box for 90 rupees, and then spends 40 percent of the money he has left on coloured pens. How much remains?",
    "₹250. Box ₹90. Then 40% of the rest.", 250, 90, "the geometry box", 40, "the pens", "the money he has left")

LESSONS[P + "cd864b47-6c82-4efb-a819-785e8ae30e0a"] = fixed_first(
    P + "cd864b47", "Ravi",
    "Ravi goes to a cricket match with 400 rupees. His ticket costs 120 rupees, and then he spends 25 percent of the remaining money on snacks. How much is left?",
    "₹400. Ticket ₹120. Then 25% of the rest.", 400, 120, "the ticket", 25, "the snacks", "the remaining money")

LESSONS[P + "ea70992b-c890-41a2-8c48-2006935776cc"] = fixed_first(
    P + "ea70992b", "Aditya",
    "Aditya goes to a kite festival with 650 rupees. He buys a kite for 200 rupees, and then spends 30 percent of the money he has left on kite string. How much remains?",
    "₹650. Kite ₹200. Then 30% of the rest.", 650, 200, "the kite", 30, "the kite string", "the money he has left")
