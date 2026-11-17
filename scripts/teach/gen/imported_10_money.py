"""Money stories: start with some, some goes out, some comes in. And the same story told backwards."""
from imported_10_lib import ANS, ASK, B, FIG, GIVEN, L, M, N, RING, W, add, bar, bars, f, pick, take, total


# ── Start, spend, (more out), (some in): what is there now? ──────────────────

def spend(key, who, start, items, given, intro, ask_out, end, recap, outs=(), ins=(), add_trap=None, end_trap=None):
    """items: the prices paid. outs: (amount, ask, say) for money that leaves afterwards.
    ins: (amount, ask) for money that arrives afterwards. end: the closing sentence, with {ans}."""
    beats = [B(intro, GIVEN("q", given)), ASK(key, "a1", *ask_out)]

    lead = pick(key, "addlead", ["So add up what was spent.", "Add up the spending first.", "First, the total spent."])
    words, ops, tot, last = total(items, "s", "spent")
    beats.append(B(lead + " " + words[0].upper() + words[1:], *ops))
    if add_trap:
        beats.append(B(add_trap))

    for i, (amt, ask, say) in enumerate(outs):
        beats.append(ASK(key, "out%d" % i, *ask))
        new = tot + amt
        last = "o%d" % i
        beats.append(B(say.format(tot=tot, amt=amt, new=new),
                       W(last, "%s + %s = %s" % (f(tot), f(amt), f(new))), N(last, "= " + f(new), "gone altogether")))
        tot = new

    left = start - tot
    lead = pick(key, "sublead", ["Now take that away from the %d." % start,
                                 "Now take that from the %d %s started with." % (start, who)])
    beats += take(key, start, tot, "left", lead, None if ins else "answer", mark=(last, "= " + f(tot)))

    now = left
    if not ins:
        beats.append(B(end.format(ans=left), RING("left", "= " + f(left))))
    for i, (amt, ask) in enumerate(ins):
        beats.append(ASK(key, "in%d" % i, *ask))
        new = now + amt
        final = i == len(ins) - 1
        line = "%s + %s = %s" % (f(now), f(amt), f(new))
        beats.append(B("%d plus %d is %d. %s" % (now, amt, new, end.format(ans=new) if final else ""),
                       ANS("fin", line) if final else W("in%d" % i, line),
                       RING("fin", "= " + f(new)) if final else None))
        now = new
    if end_trap:
        beats.append(B(end_trap))

    if ins:
        amt = ins[-1][0]
        beats.append(B("Check by walking backwards. Take away the %d that came in, and we are at %d. Put back the %d that went out, and we are at %d, where %s began."
                       % (amt, left, tot, start, who),
                       W("c1", "%s − %s = %s" % (f(now), f(amt), f(left))), W("c2", "%s + %s = %s" % (f(left), f(tot), f(start)))))
    else:
        beats.append(B(pick(key, "check", [
            "Check by adding back. %d plus the %d that went out is %d, the money %s began with.",
            "Check it the other way. The %d left, plus the %d that went out, makes %d. That is what %s began with.",
        ]) % (left, tot, start, who), W("c1", "%s + %s = %s" % (f(left), f(tot), f(start)))))
    beats.append(B(recap))
    add(key, *beats)


SORT_RECAP = [
    "So in a money story, sort the amounts first. Add up what goes out, take it from the start, then add what comes in.",
    "So before any sums, decide which amounts go out and which come in. Take away the outs, add the ins.",
    "So read a money story twice. Once to sort the ins from the outs, and once to do the sums in order.",
]
PLAIN_RECAP = [
    "So for a what-is-left question: add up everything spent, then take that total from the money at the start.",
    "So total the spending first, then subtract once. One careful subtraction is easier than three.",
]


def gift_ask(left, amt, if_not):
    return ("So %d rupees are left after the shopping. Is that our final answer?" % left,
            "Not yet: add the %d" % amt, ["Yes, %d is the answer" % left, "Not yet: take away the %d" % amt], if_not)


spend("08d11006", "Priya", 500, [178, 145],
      "Had ₹500. Spent ₹178 and ₹145. Uncle gave ₹75.",
      "Priya takes 500 rupees to the Diwali mela. She buys ladoos for 178 and diyas for 145. Then her uncle gives her 75. How much does she have now?",
      ("Three amounts follow the 500. Which of them are money going out of Priya's purse?",
       "178 and 145", ["178, 145 and 75", "only 178"],
       "The ladoos and the diyas were bought, so 178 and 145 went out. The 75 came from her uncle, so that is money coming in."),
      "So Priya has {ans} rupees now.", SORT_RECAP[0],
      ins=[(75, gift_ask(177, 75, "Read the end of the story again. Her uncle gave her 75 rupees, and a gift is money coming in. It still has to be added."))])

spend("7576aebc", "Ravi", 500, [127, 89],
      "Had ₹500. Spent ₹127 and ₹89. Grandmother gave ₹75.",
      "Ravi goes to the Diwali mela with 500 rupees. He buys sparklers for 127 and diyas for 89. Then his grandmother gives him 75. How much does he have now?",
      ("Before any sums, sort the amounts. Which ones are money leaving Ravi's pocket?",
       "127 and 89", ["127, 89 and 75", "only 127"],
       "He paid for the sparklers and the diyas, so 127 and 89 went out. The 75 is a gift from his grandmother, so that one comes in."),
      "So Ravi has {ans} rupees now.", SORT_RECAP[1],
      ins=[(75, gift_ask(284, 75, "The story does not stop at the shopping. His grandmother gave him 75 rupees afterwards, and money coming in is added."))])

spend("bf9ee9bc", "Ravi", 500, [128, 97],
      "Had ₹500. Spent ₹128 and ₹97. Grandmother gave ₹75.",
      "Ravi has 500 rupees at the Diwali mela. Sparklers cost him 128 and diyas cost him 97. After that, his grandmother gives him 75 as a gift. How much does he have now?",
      ("Which of these amounts make Ravi's money smaller?",
       "128 and 97", ["128, 97 and 75", "all of them, and the 500 too"],
       "Spending makes money smaller, so the 128 and the 97 do that. The 75 from his grandmother makes it bigger."),
      "So Ravi has {ans} rupees now.", SORT_RECAP[2],
      ins=[(75, gift_ask(275, 75, "Look at the last thing that happened. Grandmother gave him 75 rupees, so his money went up by 75 after the shopping."))])

spend("3a892c05", "Priya", 500, [137, 218, 89],
      "Had ₹500. Spent ₹137, ₹218 and ₹89. Found ₹20.",
      "Priya has 500 rupees at the Diwali mela. She buys bangles for 137, ladoos for 218 and a diya set for 89. On the way home she finds 20 rupees. How much does she have now?",
      ("Four amounts follow the 500. Which of them are money going out?",
       "137, 218 and 89", ["all four of them", "only 137 and 218"],
       "The bangles, the ladoos and the diya set were all bought, so 137, 218 and 89 went out. The 20 was found, so that is money coming in."),
      "So Priya has {ans} rupees now.", SORT_RECAP[1],
      ins=[(20, gift_ask(56, 20, "Do not forget the walk home. She found 20 rupees, and found money is money coming in. So it is added."))])

spend("9c6bcc16", "Ravi", 500, [127, 89, 156],
      "Had ₹500. Spent ₹127, ₹89 and ₹156. Found ₹20.",
      "Ravi takes 500 rupees to the Diwali mela. He buys sparklers for 127, rangoli colours for 89 and sweets for 156. Going home, he finds 20 rupees and keeps it. How much does he have now?",
      ("Sort the amounts before adding anything. Which ones did Ravi pay out?",
       "127, 89 and 156", ["127, 89, 156 and 20", "only 127 and 89"],
       "He paid for sparklers, colours and sweets, so 127, 89 and 156 went out. The 20 he found came in."),
      "So Ravi has {ans} rupees now.", SORT_RECAP[0],
      ins=[(20, gift_ask(128, 20, "The story carries on after the mela. He found 20 rupees and kept it, so his money grows by 20."))])

spend("b3cd211a", "Ravi", 4750, [1285, 965],
      "Had ₹4,750. Spent ₹1,285 and ₹965. Uncle gave ₹1,200.",
      "Ravi's grandmother gives him 4750 rupees for Diwali. He spends 1285 on crackers and 965 on sweets. Then his uncle gives him 1200 more. How much does he have now?",
      ("Which amounts are money going out of Ravi's hands?",
       "1285 and 965", ["1285, 965 and 1200", "4750 and 1285"],
       "Crackers and sweets were paid for, so 1285 and 965 went out. The 4750 and the 1200 were both given to him, so they came in."),
      "So Ravi has {ans} rupees now.", SORT_RECAP[2],
      ins=[(1200, gift_ask(2500, 1200, "One more thing happened after the spending. His uncle gave him 1200 rupees, and that is money coming in."))])

spend("2bd94bfc", "Ankit's father", 1000, [245, 178, 367],
      "Bought for ₹245, ₹178 and ₹367. Paid with ₹1,000.",
      "At the book fair they buy a storybook for 245, a puzzle book for 178 and a colouring set for 367. Father pays with a 1000 rupee note. How much change comes back?",
      ("Change is what comes back out of the 1000. What must we know before we can find it?",
       "the total cost of all 3 things", ["the cost of the storybook only", "1000 plus the 3 prices"],
       "The shopkeeper adds up everything they bought and keeps all of it out of the note. So first we need the total of the 3 prices."),
      "So the change is {ans} rupees.", PLAIN_RECAP[0],
      add_trap="Careful with that adding. The ones make more than 10, and so do the tens, so there are carries to pass along. One missed carry and the change comes out a little off.")

spend("548a38da", "the family", 5000, [2475, 1368, 957],
      "Set aside ₹5,000. Spent ₹2,475, ₹1,368 and ₹957.",
      "Ravi's family set aside 5000 rupees for Diwali shopping. They buy firecrackers for 2475, sweets for 1368 and decorations for 957. How much is left?",
      ("They bought 3 kinds of things out of the 5000. What should we find first?",
       "the total of the 3 purchases", ["5000 plus the 3 purchases", "only the biggest purchase"],
       "Money left means the budget minus everything that was spent. So first add up all 3 purchases."),
      "So {ans} rupees are left.", PLAIN_RECAP[1],
      add_trap="Careful with the carries in that adding. Miss one and the total drifts, and then the money left drifts with it.")

spend("978019ae", "Rohan's father", 7500, [2475, 1368, 2157],
      "Had ₹7,500. Spent ₹2,475, ₹1,368 and ₹2,157.",
      "Rohan's father has 7500 rupees in his wallet. He buys firecrackers at 3 shops: 2475 at the first, 1368 at the second and 2157 at the third. How much is left in the wallet?",
      ("He paid at 3 different shops. Before we can see what is left, what do we need?",
       "the total spent at all 3 shops", ["the amount at the first shop only", "7500 plus the 3 amounts"],
       "All 3 payments came out of the same wallet. So add the 3 amounts to see how much left the wallet altogether."),
      "So {ans} rupees are left in the wallet.", PLAIN_RECAP[0],
      end_trap="Careful not to stop at 6000. That is the money that was spent. The question asks for the money that is left.")

spend("eef4d432", "grandfather", 1200, [345, 278, 467],
      "Had ₹1,200. Books cost ₹345, ₹278 and ₹467.",
      "Grandfather has 1200 rupees in his wallet. At the book fair he buys a storybook for 345, a puzzle book for 278 and a maths workbook for 467. How much does he have left?",
      ("3 books are paid for out of one wallet. What do we work out first?",
       "the total cost of the 3 books", ["the cost of the dearest book", "1200 plus the 3 prices"],
       "Every book was paid for from the same 1200. So first find what the 3 books cost together."),
      "So grandfather has {ans} rupees left.", PLAIN_RECAP[1],
      add_trap="Careful with the carries in that adding. The ones column and the tens column both go past 10.")

spend("0e2d6d8d", "Ravi's father", 7500, [2475, 1368, 2157],
      "Had ₹7,500. Spent ₹2,475, ₹1,368, ₹2,157. Bonus ₹500.",
      "Ravi's father has 7500 rupees. He buys firecrackers at 3 shops, for 2475, 1368 and 2157. Then he gives the helper a Diwali bonus of 500. How much is left in his wallet?",
      ("First the shopping. He paid at 3 shops, so what do we need?",
       "the total spent at the 3 shops", ["the amount at the last shop only", "7500 plus the 3 amounts"],
       "All 3 payments came from the same wallet. Add them to see how much the firecrackers cost altogether."),
      "So {ans} rupees are left in the wallet.",
      "So gather everything that leaves the wallet, the shopping and the bonus, into one total. Then subtract it once.",
      outs=[(500, ("After the shopping he gives the helper a bonus of 500. What does that do to the money in his wallet?",
                   "It goes out as well", ["It comes in, so the wallet grows", "Nothing: it is not shopping"],
                   "A bonus is money he hands to someone else. It leaves his wallet just as the shopping money did."),
             "So the bonus joins the money going out. {tot} plus {amt} is {new} gone altogether.")],
      end_trap="The trap is to stop after the 3 shops. That would leave 500 too much in the wallet, because the bonus was paid from it too.")

spend("c767e364", "Ravi's father", 7500, [2475, 1368, 2157],
      "Had ₹7,500. Spent ₹2,475, ₹1,368, ₹2,157. Gave Ravi ₹250.",
      "Ravi's father brings 7500 rupees to the market. He buys firecrackers at 3 shops, for 2475, 1368 and 2157. Then he gives Ravi 250 as pocket money. How much does father have left?",
      ("Start with the firecrackers. He paid at 3 shops, so what do we need?",
       "the total spent at the 3 shops", ["the amount at the first shop only", "7500 plus the 3 amounts"],
       "The 3 payments all came out of father's money. Add them to see what the firecrackers cost altogether."),
      "So father has {ans} rupees left.",
      "So ask whose money you are counting. Everything that leaves that person's hands goes into one total, and then you subtract once.",
      outs=[(250, ("Then he gives Ravi 250 as pocket money. We are counting father's money. What does the 250 do to it?",
                   "It goes out of father's money", ["It comes in, so add it", "Nothing: it stays in the family"],
                   "The pocket money moves from father to Ravi. We are counting what father has, so the 250 has left his hands."),
             "So the pocket money joins the money going out. {tot} plus {amt} is {new} gone altogether.")])

# ── Ravi: out, out, in, out ──────────────────────────────────────────────────

Q = "538cb8ab"
sub = take(Q, 5900, 2753, "left", "Money in, take away money out.", "answer", mark=("o2", "= 2,753"))
add(Q,
    B("Ravi gets 4750 rupees from his grandmother. He spends 1285 on crackers and 968 on sweets. His uncle gives him 1150. Later he donates 500. How much does he have now?",
      GIVEN("q", "Got ₹4,750. Spent ₹1,285, ₹968. Got ₹1,150. Gave ₹500.")),
    ASK(Q, "a1", "That is a lot of ins and outs, so let's sort them. Which amounts went out of Ravi's hands?",
        "1285, 968 and 500", ["1285 and 968 only", "1285, 968 and 1150"],
        "Crackers, sweets and the donation all left his hands: 1285, 968 and 500. The 1150 from his uncle came in."),
    B("Add up everything that came in. 4750 from grandmother plus 1150 from uncle is 5900.",
      W("in", "4,750 + 1,150 = 5,900"), N("in", "= 5,900", "money in")),
    B("Now everything that went out. 1285 plus 968 is 2253, and 500 more makes 2753.",
      W("o1", "1,285 + 968 = 2,253"), W("o2", "2,253 + 500 = 2,753"), N("o2", "= 2,753", "money out")),
    sub[0], sub[1],
    B("So Ravi has 3147 rupees now.", RING("left", "3,147")),
    B("Careful with the donation. It comes after the uncle's gift in the story, but it is still money going out. The order in the story does not change which way the money moves."),
    B("Check it in story order, step by step: take 1285, take 968, add 1150, take 500. The board shows it comes to 3147 again.",
      W("c", "4,750 − 1,285 − 968 + 1,150 − 500 = 3,147")),
    B("So when a story has many ins and outs, make two piles. Total the ins, total the outs, and subtract once."),
    )

# ── Ravi's donation: the missing amount in the middle ────────────────────────

Q = "1ec9d0ee"
sub = take(Q, 5000, 3520, "left", "Take that from his 5000.", mark=("s2", "= 3,520"))
add(Q,
    B("Ravi has 5000 rupees. He buys a saree for 1475, a bat for 1260 and sweets for 785. His uncle gives him 750. Then he donates some money, and has 1980 left. How much did he donate?",
      GIVEN("q", "Had ₹5,000. Spent ₹1,475, ₹1,260, ₹785. Got ₹750."), L("q2", "Donated ₹? and then had ₹1,980 left")),
    B("We cannot see the donation, so let's find how much he had just before it. First the shopping: 1475 plus 1260 is 2735, and 785 more makes 3520.",
      W("s1", "1,475 + 1,260 = 2,735"), W("s2", "2,735 + 785 = 3,520"), N("s2", "= 3,520", "spent")),
    sub[0], sub[1],
    B("Then his uncle's gift comes in. 1480 plus 750 is 2230. That is what Ravi held just before the donation.",
      W("b", "1,480 + 750 = 2,230"), N("b", "= 2,230", "before donating")),
    ASK(Q, "a1", "He had 2230 before the donation and 1980 after it. Which sum gives the donation?",
        "2230 − 1980", ["2230 + 1980", "1980 − 750"],
        "The donation is what disappeared between before and after. So it is the gap between 2230 and 1980, and a gap is a subtraction."),
    B("For 2230 minus 1980, counting up is easier than borrowing. From 1980 up to 2000 is 20, and from 2000 up to 2230 is 230 more.",
      W("u1", "1,980 + 20 = 2,000"), W("u2", "2,000 + 230 = 2,230")),
    B("20 plus 230 is 250. So he donated 250 rupees.",
      W("u3", "20 + 230 = 250"), ANS("ans", "2,230 − 1,980 = 250"), RING("ans", "250")),
    B("Careful not to leave out the uncle's 750. Without it, Ravi would seem to have less than 1980 before donating, and that cannot be."),
    B("Check the whole story forwards on the board: spend, spend, spend, add the gift, donate 250. It ends on 1980, just as it should.",
      W("c", "5,000 − 3,520 + 750 − 250 = 1,980")),
    B("So when the missing number is in the middle of a story, work up to the moment just before it, then compare before and after."),
    )

# ── How much more is needed? ─────────────────────────────────────────────────

Q = "0ee6cea0"
sub = take(Q, 4500, 4105, "ans", "", "answer", mark=("s2", "= 4,105"))
add(Q,
    B("Priya's piggy bank starts with 2450 rupees. She adds 375 in January, and her uncle drops in 1280 in February. A telescope costs 4500. How much more does she need?",
      GIVEN("q", "Has ₹2,450 + ₹375 + ₹1,280. Telescope costs ₹4,500.")),
    B("First, how much is in the piggy bank now? 2450 plus 375 is 2825, and 1280 more makes 4105.",
      W("s1", "2,450 + 375 = 2,825"), W("s2", "2,825 + 1,280 = 4,105"), N("s2", "= 4,105", "what she has")),
    ASK(Q, "a1", "She has 4105 and the telescope costs 4500. Which sum tells us how much more she needs?",
        "4500 − 4105", ["4500 + 4105", "4500 − 2450"],
        "How much more means the gap between what she has and what she needs. A gap is found by subtracting: the price, minus all her savings."),
    sub[0], sub[1],
    B("So Priya still needs 395 rupees.", RING("ans", "395")),
    B("Careful: all 3 amounts in the piggy bank are hers. Leave out the pocket money or her uncle's money, and she would seem to need far more than she does."),
    B("Check by adding on. 4105 plus 395 is 4500, exactly the price of the telescope.",
      W("c", "4,105 + 395 = 4,500")),
    B("So for a how-much-more question: total what you have, then subtract it from what you need."),
    )

Q = "5dd61b5e"
sub = take(Q, 1250, 1063, "ans", "How much more is the gap between the price and what they have.", "answer")
add(Q,
    B("Meena and Rohan want a cricket bat that costs 1250 rupees. Meena has saved 485, Rohan has saved 378, and their mother gives them 200. How much more do they need?",
      GIVEN("q", "Have ₹485 + ₹378 + ₹200. Bat costs ₹1,250.")),
    ASK(Q, "a1", "Whose money counts towards the bat?",
        "Meena's, Rohan's and mother's gift", ["only Meena's and Rohan's savings", "only mother's gift"],
        "They are buying the bat together, and mother's 200 is a gift to help with it. So all 3 amounts go into the pot."),
    B("So add all 3. 485 plus 378 is 863, and 200 more makes 1063.",
      W("s1", "485 + 378 = 863"), W("s2", "863 + 200 = 1,063"), N("s2", "= 1,063", "what they have")),
    sub[0],
    B("So they still need 187 rupees.", RING("ans", "187")),
    B("Here is the trap. Forget mother's 200, and the answer comes out 200 too big. Every rupee they have makes the gap smaller."),
    B("Check by adding on. 1063 plus 187 is 1250, the price of the bat.",
      W("c", "1,063 + 187 = 1,250")),
    B("So for a how-much-more question: put all the money you have together, then subtract it from the price."),
    )


# ── Told backwards: what was there at the start? ─────────────────────────────

def origin(key, intro, given, items, left, back_ask, brace, sum_say, check_say, recap, final=True, after=(), trap=None):
    """Spent (or gave away) `items`, still has `left`. Start = spent + left. `after` holds any later beats."""
    words, ops, tot, last = total(items, "s", "gone")
    base = tot + left
    a = max(0.5, round(10.0 * tot / base, 1))
    b = max(0.5, round(10.0 * left / base, 1))
    line = "%s + %s = %s" % (f(tot), f(left), f(base))
    beats = [
        B(intro, GIVEN("q", given)),
        B(pick(key, "lead", ["Start with what went out.", "First, total what went out."]) + " " + words[0].upper() + words[1:], *ops),
        ASK(key, "a1", back_ask[0].format(tot=tot, left=left), "%d + %d" % (tot, left),
            ["%d − %d" % (tot, left), "just %d" % tot], back_ask[1]),
        B(sum_say.format(tot=tot, left=left, base=base),
          FIG("bar", bars(bar([(a, "gone: " + f(tot), "a"), (b, "left: " + f(left), "b")], brace))),
          ANS("ans", line) if final else W("base", line),
          RING("ans", "= " + f(base)) if final else N("base", "= " + f(base), "before spending")),
    ]
    beats += list(after)
    if trap:
        beats.append(B(trap.format(tot=tot, left=left, base=base), M(last, "= " + f(tot))))
    if check_say:
        beats.append(B(check_say.format(tot=tot, left=left, base=base),
                       W("c", "%s − %s = %s" % (f(base), f(tot), f(left)))))
    beats.append(B(recap))
    add(key, *beats)


BACK_IFNOT = [
    "Every rupee she was given was either spent or is still there. So put those two piles back together: add them.",
    "Think of it backwards. What went out and what is left were once all together. To rebuild the start, add them.",
]

origin("619fc94d",
       "Priya's grandmother gives her some money for Pongal. She spends 2365 on clothes, 1480 on sweets and 955 on rangoli supplies, and still has 3200 left. How much was she given?",
       "Spent ₹2,365, ₹1,480 and ₹955. Still has ₹3,200.",
       [2365, 1480, 955], 3200,
       ("She spent {tot} and still has {left}. How do we get back to what she was given?", BACK_IFNOT[0]),
       "given = ?",
       "Look at the bar: the spent part and the left part together make the whole gift. {tot} plus {left} is {base}. Grandmother gave her {base} rupees.",
       "Check it forwards. Start with {base}, spend {tot}, and {left} is left. Just as the story says.",
       "So when you know what was spent and what is left, add them to find the start. Spending is undone by adding.",
       trap="Careful not to stop at {tot}. That is only the money she spent. The {left} in her piggy bank was part of the gift as well.")

origin("7c14587f",
       "Priya has a box of ladoos to share during Navratri. She gives away 168 on the first day, 245 on the second and 137 on the third. 150 are still in the box. How many were there at first?",
       "Gave away 168, 245 and 137 ladoos. 150 are left.",
       [168, 245, 137], 150,
       ("She gave away {tot} ladoos and {left} are still in the box. How do we find how many there were at first?",
        "Every ladoo was either given away or is still in the box. So put those two groups back together: add them."),
       "at first = ?",
       "The bar shows it: the ladoos given away and the ladoos left make the full box. {tot} plus {left} is {base}. There were {base} ladoos at first.",
       "Check it forwards. Start with {base}, give away {tot}, and {left} are left in the box. It fits.",
       "So to find how many there were at the start, add what went out to what is left.",
       trap="Careful not to stop at {tot}. Those are only the ladoos she gave away. The {left} still in the box were there at the start too.")

origin("c654dc44",
       "Ravi's grandmother gives him some money. Before spending, he lends 750 to Arjun. Then he spends 1275 on crackers, 850 on sweets and 1460 on clothes, and has 2165 left. How much was he given?",
       "Lent ₹750. Spent ₹1,275, ₹850, ₹1,460. Has ₹2,165.",
       [1275, 850, 1460], 2165,
       ("He spent {tot} and still has {left}. How do we get back to what he had before the shopping?", BACK_IFNOT[1]),
       "before shopping = ?",
       "The spent part and the left part together make what he had before the shopping. {tot} plus {left} is {base}.",
       None,
       "So to rebuild the start, add back everything that left: what was spent, what was lent, and what is still there.",
       final=False,
       after=[
           ASK("c654dc44", "a2", "So 5750 is what he had before the shopping. Is that everything grandmother gave him?",
               "No: add the 750 he lent", ["Yes, 5750 is the answer", "No: take away the 750"],
               "The 750 he lent to Arjun came out of grandmother's gift too, and it has not come back. So it has to be added on."),
           B("5750 plus 750 is 6500. Grandmother gave him 6500 rupees.",
             ANS("ans", "5,750 + 750 = 6,500"), RING("ans", "6,500")),
           B("That lent money is the trap. It is not spent and it is not in the piggy bank, so it is easy to lose. But it was part of the gift."),
           B("Check it forwards. From 6500, lend 750, then spend 3585, and 2165 is left. It matches.",
             W("c", "6,500 − 750 − 3,585 = 2,165")),
       ])

origin("d3d99cf4",
       "Ravi spends 1245 on firecrackers, 876 on sweets and 1389 on clothes, and has 2490 left. The money he began with included 500 from his uncle and 750 from his aunt. How much came from grandmother alone?",
       "Spent ₹1,245, ₹876, ₹1,389. Has ₹2,490 left.",
       [1245, 876, 1389], 2490,
       ("He spent {tot} and still has {left}. How do we get back to all the money he began with?", BACK_IFNOT[1]),
       "began with = ?",
       "The spent part and the left part together make everything he began with. {tot} plus {left} is {base}.",
       None,
       "So rebuild the whole starting amount first, by adding. Then take away the parts that came from other people.",
       final=False,
       after=[
           ASK("d3d99cf4", "a2", "He began with 6000. Did all of that come from grandmother?",
               "No: take off uncle's and aunt's", ["Yes, 6000 is the answer", "No: add uncle's and aunt's"],
               "The story says the 500 from his uncle and the 750 from his aunt were already inside that total. So they must come off."),
           B("Uncle and aunt together gave 500 plus 750, which is 1250.",
             L("q2", "The start includes uncle's ₹500 and aunt's ₹750"), W("u", "500 + 750 = 1,250")),
       ] + take("d3d99cf4", 6000, 1250, "ans", "Take that from the 6000.", "answer", mark=("u", "= 1,250")) + [
           B("So grandmother alone gave him 4750 rupees.", RING("ans", "4,750")),
           B("Check by putting the three gifts together. 4750 plus 500 plus 750 is 6000, everything he began with.",
             W("c", "4,750 + 500 + 750 = 6,000")),
       ])

origin("e013e536",
       "Ravi's piggy bank already held 1500 rupees from his birthday. Grandmother gives him some more for Diwali. He spends 1245, 876 and 1534, and 2345 is left. How much did grandmother give?",
       "Spent ₹1,245, ₹876, ₹1,534. Has ₹2,345 left.",
       [1245, 876, 1534], 2345,
       ("He spent {tot} and still has {left}. How do we get back to all the money he had before spending?", BACK_IFNOT[1]),
       "before spending = ?",
       "The spent part and the left part together make everything he had before spending. {tot} plus {left} is {base}.",
       None,
       "So rebuild the whole amount first, by adding. Then take away what was already there before the gift arrived.",
       final=False,
       after=[
           ASK("e013e536", "a2", "He had 6000 before spending. Was all of that grandmother's gift?",
               "No: take off his 1500 savings", ["Yes, 6000 is the answer", "No: add his 1500 savings"],
               "The piggy bank already held 1500 from his birthday. That part of the 6000 is his own, so it must come off."),
           B("6000 minus 1500 is 4500. Grandmother gave him 4500 rupees.",
             L("q2", "Already saved before Diwali: ₹1,500"), ANS("ans", "6,000 − 1,500 = 4,500"), RING("ans", "4,500")),
           B("That is the trap in this story: 6000 looks like a finished answer. But it mixes two things, the birthday savings and the gift."),
           B("Check it forwards. 1500 of savings plus the 4500 gift is 6000. Spend 3655, and 2345 is left.",
             W("c1", "1,500 + 4,500 = 6,000"), W("c2", "6,000 − 3,655 = 2,345")),
       ])
