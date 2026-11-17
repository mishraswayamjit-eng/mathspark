"""Lines written by hand for the imported Grade 5 money-percent questions, keyed by question id.

Keys inside a question: "q", "o0".."o3" (options), "h0".."h2" (hints), "s0".. (steps).
Anything not listed here is produced by the rules in money_percent_imported_rules.py.
More hand-written lines are in money_percent_imported2.py and later files; all are merged here.
"""
_SIMILAR = "Here's a similar problem: "

LINES = {
    # Algebra inside a hint: brackets and equation chains need breaths the rules cannot place.
    "AIGEN_grade5_13ec64a9-af2a-471b-88ae-9949ae5230a8": {
        "h2": _SIMILAR + "Suppose 10,000 rupees is split into two parts at 4 percent and 6 percent for 2 years, "
              "and total interest is 1,040 rupees. If part at 6 percent is x, then: "
              "open bracket, 10000 minus x, close bracket, times 4 times 2, divided by 100. "
              "Plus x times 6 times 2, divided by 100. That equals 1040. "
              "So 800 minus 0.08 x plus 0.12 x equals 1040. So 0.04 x equals 240. So x equals 6,000 rupees. "
              "Try the same approach for Ravi's problem!",
    },
    "AIGEN_grade5_3c453b93-e940-4a3d-a934-5cfd3c2b8138": {
        "h2": _SIMILAR + "Suppose 10,000 rupees is split between two banks at 4 percent and 6 percent for 3 years, "
              "and total interest is 1,560 rupees. If Bank A gets x rupees, then: x times 4 times 3, divided by 100. "
              "Plus, open bracket, 10000 minus x, close bracket, times 6 times 3, divided by 100. That equals 1560. "
              "Solving: 12 x over 100, plus, open bracket, 180000 minus 18 x, close bracket, over 100, equals 1560. "
              "So 180000 minus 6 x equals 156000. So 6 x equals 24000. So x equals 4,000 rupees in Bank A.",
        "s0": "Let the amount deposited in Bank A equal x rupees. Then the amount in Bank B equals 12,000 minus x rupees.",
    },
    "AIGEN_grade5_3e15386d-9911-43db-ab57-cd74fcf5aedf": {
        "h1": "Write the Simple Interest formula for both. Meena's simple interest equals 5000 times 8 times t, divided by 100. "
              "And Ravi's simple interest equals 5000 times 12 times, open bracket, t minus 1, close bracket, divided by 100. "
              "Since total amounts are equal, their interests must also be equal, same principal.",
        "h2": _SIMILAR + "Suppose Amit deposits 2,000 rupees at 6 percent and Priya deposits 2,000 rupees at 10 percent. "
              "Priya keeps money for 2 years less than Amit. If both get the same amount: "
              "2000 times 6 times t, divided by 100, equals 2000 times 10 times, open bracket, t minus 2, close bracket, divided by 100. "
              "So 6 t equals 10 t minus 20. So 4 t equals 20. So t equals 5. "
              "So Amit kept for 5 years, Priya for 3 years. Check: Amit gets 600 rupees interest, Priya gets 600 rupees interest.",
        "s0": "Let Meena's deposit duration be t years. Since Ravi withdrew 1 year earlier, Ravi's duration is t minus 1 years.",
    },
    "AIGEN_grade5_920aaa2e-8349-4ebb-a6fd-560e990c98ef": {
        "h1": "Let the amount in the 8 percent account be x rupees. Then the amount in the 5 percent account is 12000 minus x rupees. "
              "Write: open bracket, 12000 minus x, close bracket, times 5 times 3, divided by 100, "
              "equals x times 8 times 3, divided by 100.",
        "h2": _SIMILAR + "Suppose 10,000 rupees is split into two parts at 4 percent and 6 percent simple interest for 2 years, "
              "earning equal interest. Let the part at 6 percent be y. "
              "Then, open bracket, 10000 minus y, close bracket, times 4 times 2, divided by 100, "
              "equals y times 6 times 2, divided by 100. This gives 80000 minus 8 y equals 12 y, so 20 y equals 80000, and y equals 4000. "
              "The 6 percent part is 4,000 rupees and the 4 percent part is 6,000 rupees. Use the same method for your problem!",
        # The source runs two sentences together ("= ₹1107.69 They match!").
        "s9": "So Ravi deposited approximately 4,615.38 rupees in the 8 percent account and 7,384.62 rupees in the 5 percent account. "
              "Let's verify: simple interest one equals 7384.62 times 5 times 3, divided by 100, which is 1107.69 rupees. "
              "And simple interest two equals 4615.38 times 8 times 3, divided by 100, which is 1107.69 rupees. They match!",
    },
    # The source has no full stop after "mela"; the voice needs the pause.
    "AIGEN_grade5_56c0860d-a2c4-406a-a113-e9ecedba89a4": {
        "q": "Arjun saved 4,000 rupees from selling lemonade at his school's Diwali mela. "
             "He deposited this amount in a bank that offers simple interest at 5 percent per year. "
             "After 3 years, he wants to use the total amount, principal plus interest, to buy a cricket bat. "
             "How much money will Arjun have after 3 years?",
    },
    "AIGEN_grade5_9d213c43-daf5-4358-8a6f-e4ca823aa429": {
        "s4": "This gives T equals 0, which means the only time their interests are equal is at the very start, "
              "when both have earned 0 rupees. Since Priya earns 280 rupees per year and Ravi earns 270 rupees per year, "
              "Priya's interest is always more than Ravi's for any T greater than 0. "
              "So they can never earn equal interest after depositing!",
    },
}


def _merge():
    import importlib
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    for name in ("money_percent_imported2", "money_percent_imported3", "money_percent_imported4"):
        if not os.path.exists(os.path.join(here, name + ".py")):
            continue
        mod = importlib.import_module(name)
        for qid, lines in mod.LINES.items():
            LINES.setdefault(qid, {}).update(lines)


_merge()
