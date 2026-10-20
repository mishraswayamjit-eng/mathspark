#!/usr/bin/env python3
"""
Author the Grade-4 "Fraction Sense" Concept Trainer SOURCE JSON.

This single self-contained script BUILDS the source dict (8 modules x 8 items)
in Python so that every fraction answer is COMPUTED with `fractions.Fraction`
(correct by construction - never a typed guess), then writes
`scripts/sources/fractions-g4-source.json`.

Run the generator afterwards to reshape + math-verify + emit the app JSON:

    python scripts/generate_trainer.py scripts/sources/fractions-g4-source.json

Design
------
A Concept Trainer item = story -> THREE thinking-step MCQs (each wrong option
names a REAL misconception, mined from the 348 IPM Grade-4 seed questions in
`scripts/sources/_seed-extract-fractions-grade4.json`) -> a picture -> a worked
solution. We attach a `verify` spec to every computable item so
`generate_trainer.py` recomputes the answer and asserts equality (the math-gate).

Tone is warm and kid-safe. Wrong-option feedback is always a gentle teaching
moment - never "wrong/incorrect/failed/error".
"""

import json
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "sources", "fractions-g4-source.json")


# ── fraction helpers: mirror generate_trainer.py's formatting EXACTLY ─────────
# so our authored `answer` always equals what the math-gate recomputes.

def F(s) -> Fraction:
    """Parse '3/8', '21/5', '4 1/5' (mixed) or 7 into a Fraction."""
    if isinstance(s, int):
        return Fraction(s)
    text = str(s).strip()
    if " " in text:  # mixed number "4 1/5"
        whole, frac = text.split(None, 1)
        f = Fraction(frac)
        sign = -1 if whole.strip().startswith("-") else 1
        return Fraction(int(whole)) + sign * f
    return Fraction(text)


def ffrac(f: Fraction) -> str:
    """Lowest-terms 'n/d', or 'n' for integers - matches fmt_frac."""
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


def fmixed(f: Fraction) -> str:
    """Mixed-number form '4 1/5' - matches fmt_mixed."""
    if f.denominator == 1:
        return str(f.numerator)
    if abs(f.numerator) < f.denominator:
        return ffrac(f)
    sign = "-" if f < 0 else ""
    a = abs(f)
    whole = a.numerator // a.denominator
    rem = a - whole
    return f"{sign}{whole} {rem.numerator}/{rem.denominator}"


def raw(n, d) -> str:
    """An UNREDUCED 'n/d' string (used for equiv distractors/answers)."""
    return f"{n}/{d}"


def equiv_str(frac: str, k: int) -> str:
    """Unreduced equivalent '(a*k)/(b*k)' - matches compute('equiv')."""
    f = F(frac)
    return f"{f.numerator * k}/{f.denominator * k}"


# ── tiny builders ────────────────────────────────────────────────────────────

def o(text, correct, feedback):
    return {"text": str(text), "correct": bool(correct), "feedback": feedback}


def stage(prompt, hint, options, key=None):
    s = {"prompt": prompt, "hint": hint, "options": options}
    if key:
        s["key"] = key
    return s


MODULES = []
QUESTIONS = []


def add_module(mid, title, desc, level, rule, teach, contrast, transfer):
    MODULES.append({
        "id": mid, "title": title, "desc": desc, "level": level,
        "rule": rule, "teach": teach, "contrast": contrast, "transfer": transfer,
    })


def add_item(kw):
    QUESTIONS.append(kw)


def build_source():
    build_modules()
    build_module1()
    build_module2()
    build_module3()
    build_module4()
    build_module5()
    build_module6()
    build_module7()
    build_module8()
    return {
        "slug": "fractions-g4",
        "title": "Fraction Sense \u00b7 Grade 4",
        "concept": "Fractions",
        "gradeRange": [4, 4],
        "modules": MODULES,
        "questions": QUESTIONS,
    }


def build_modules():
    add_module(
        1, "Name the whole",
        "Identify the whole, then read a fraction as equal parts OF that whole.",
        "Core",
        "A fraction a/b means the whole is cut into b EQUAL parts and we take a of them.",
        [
            "Always start by naming the whole: 'The whole is all 8 slices' or 'the whole is the chocolate bar'.",
            "The bottom number (denominator) tells how many EQUAL parts the whole is cut into.",
            "The top number (numerator) tells how many of those equal parts we are talking about.",
        ],
        [
            "3 of 8 equal slices = 3/8.",
            "If the parts are NOT equal, you cannot name a simple fraction yet.",
        ],
        "Draw a bar, cut it into 6 equal parts, shade 5. Which fraction did you make?",
    )
    add_module(
        2, "Part and the rest",
        "Shaded + unshaded = the whole, so the two parts always add back to 1.",
        "Core",
        "If a/b is shaded then (b-a)/b is unshaded, and a/b + (b-a)/b = 1 (the whole).",
        [
            "The shaded part and the leftover part together ALWAYS make the whole whole.",
            "Read the question slowly: does it ask for the shaded part or the part that is left?",
            "Same denominator for both parts - only the top numbers share out the whole.",
        ],
        [
            "Shaded 3/8 means 5/8 is unshaded.",
            "Give what is LEFT when a story says 'gives away' - that is the complement.",
        ],
        "A pizza has 10 equal slices and 7 are eaten. Write the eaten part and the part left.",
    )
    add_module(
        3, "Equivalent fractions",
        "Multiply (or divide) the top AND bottom by the SAME number to rename a fraction.",
        "Core",
        "a/b = (a*k)/(b*k): scaling top and bottom by the same k keeps the value the same.",
        [
            "To rename a fraction, multiply the top and the bottom by the SAME number.",
            "You can also go smaller by dividing top and bottom by the same number (simplify).",
            "Adding the same number to top and bottom does NOT keep the value - that changes it.",
        ],
        [
            "3/4 = 6/8 = 9/12 (times 2, times 3).",
            "3/4 is NOT 4/5 - you may not add 1 to top and bottom.",
        ],
        "Find three fractions equal to 1/2 by scaling. What do you multiply by each time?",
    )
    add_module(
        4, "Compare fractions",
        "Same denominator: compare the tops. Different: rename to a common denominator first.",
        "Core",
        "With equal denominators the larger numerator wins; otherwise make the denominators match.",
        [
            "If the bottoms are the same, the bigger TOP number is the bigger fraction.",
            "If the bottoms differ, rename both to a common denominator, THEN compare the tops.",
            "A bigger bottom number does NOT mean a bigger fraction - it means smaller equal parts.",
        ],
        [
            "3/8 < 5/8 (same bottom, bigger top wins).",
            "1/8 < 2/5 even though 8 > 5 - bigger denominator means SMALLER slices.",
        ],
        "Compare 2/3 and 3/5 by giving both the denominator 15. Which is greater?",
    )
    add_module(
        5, "Add and subtract LIKE fractions",
        "Same denominator: add or subtract the tops and keep the bottom the same.",
        "Core",
        "a/d +/- b/d = (a +/- b)/d - the denominator (the size of each part) never changes.",
        [
            "When the bottoms match, add (or subtract) only the TOP numbers.",
            "Keep the SAME bottom - the size of each equal part has not changed.",
            "Never add the bottoms together - 1/6 + 4/6 is not 5/12.",
        ],
        [
            "4/8 + 3/8 = 7/8 (tops add, bottom stays 8).",
            "7/9 - 2/9 = 5/9 (tops subtract, bottom stays 9).",
        ],
        "Fill a 10-part bar: 3/10 then 4 more tenths. How many tenths now?",
    )
    add_module(
        6, "Add and subtract UNLIKE fractions",
        "Rename to a common denominator FIRST, then add or subtract the tops.",
        "Stretch",
        "To combine a/b and c/d, rewrite both over a common denominator, then add/subtract tops.",
        [
            "You cannot add across different bottoms - first give both fractions the same bottom.",
            "Use a denominator both bottoms divide into (a common multiple).",
            "Once the bottoms match, add or subtract only the tops.",
        ],
        [
            "1/2 + 1/4 = 2/4 + 1/4 = 3/4.",
            "1/2 + 1/3 is NOT 2/5 - rename to sixths first: 3/6 + 2/6 = 5/6.",
        ],
        "Rewrite 1/3 and 1/4 over 12, then add. What common denominator did you use?",
    )
    add_module(
        7, "Mixed and improper fractions",
        "Mixed to improper: whole*bottom + top. Improper to mixed: divide to find the whole.",
        "Stretch",
        "w a/b = (w*b + a)/b; and n/b = (n//b) and remainder/b as a mixed number.",
        [
            "To make an improper fraction, multiply the whole by the bottom, THEN add the top.",
            "Keep the same bottom number the whole way through.",
            "Do not just stick the whole in front of the top - 2 3/5 is not 23/5.",
        ],
        [
            "4 1/5 = (4*5 + 1)/5 = 21/5.",
            "23/5 = 4 remainder 3 = 4 3/5.",
        ],
        "Turn 3 2/7 into an improper fraction, then turn it back. Did you return to the start?",
    )
    add_module(
        8, "Fraction OF a quantity",
        "'of' means multiply: split the whole into bottom parts, then take top parts.",
        "Stretch",
        "a/b OF q = split q into b equal groups (q/b), then take a groups (a * q/b).",
        [
            "'of' tells you to multiply the fraction by the quantity.",
            "Divide the quantity by the BOTTOM to make one equal part, then take TOP of them.",
            "Do not divide by the top only - that skips the bottom (the number of parts).",
        ],
        [
            "3/4 of 40 = (40/4) * 3 = 10 * 3 = 30.",
            "2/3 of 90 = (90/3) * 2 = 30 * 2 = 60.",
        ],
        "Find 2/5 of 30 by first finding 1/5 of 30. What is one-fifth first?",
    )


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 1 - Name the whole
# ─────────────────────────────────────────────────────────────────────────────

def _name_whole_item(code, title, story, total, shaded, whole_name, part_name,
                     wrong_whole, label):
    """Build a 'name the whole' item. answer = shaded/total (unreduced, as read
    straight off the picture) with no verify op (purely conceptual naming)."""
    answer = raw(shaded, total)
    return dict(
        id=code, module=1, title=title, story=story,
        answer=answer,
        stages=[
            stage(
                "What is the whole in this story?",
                f"The whole is {whole_name} - the full group before we pick any part.",
                [
                    o(whole_name, True,
                      f"Yes - the whole is {whole_name}, all of it together."),
                    o(part_name, False,
                      "That is the PART we are naming, not the whole it comes from."),
                    o(wrong_whole, False,
                      "That is a number from the story, but it is not the whole group."),
                ],
                key="whole",
            ),
            stage(
                "How many EQUAL parts is the whole cut into?",
                f"Count every equal part, shaded and not: there are {total}.",
                [
                    o(f"{total} equal parts", True,
                      f"Right - all {total} equal parts make the bottom number."),
                    o(f"{shaded} equal parts", False,
                      "That is only the shaded parts. The bottom counts EVERY equal part."),
                    o("The parts are not equal, so we cannot say", False,
                      "In this picture the parts ARE equal, so we can count them."),
                ],
                key="denominator",
            ),
            stage(
                "Which fraction names the shaded part?",
                f"Top = shaded ({shaded}); bottom = all equal parts ({total}).",
                [
                    o(answer, True,
                      f"Yes - {shaded} shaded out of {total} equal parts is {answer}."),
                    o(raw(total, shaded), False,
                      "The top and bottom are swapped. Top is the shaded count, bottom is the total."),
                    o(raw(shaded, shaded + total), False,
                      "The bottom should be the TOTAL equal parts, not shaded added to total."),
                ],
                key="fraction",
            ),
        ],
        worked=[
            f"The whole is {whole_name}.",
            f"It is cut into {total} equal parts, so the bottom number is {total}.",
            f"{shaded} of those parts are shaded, so the top number is {shaded}.",
            f"The shaded fraction is {answer}.",
        ],
        check=f"Shaded {answer} and the bottom {total} counts every equal part.",
        explain="Why must the parts be equal before we write a fraction?",
        model={"type": "parts", "total": total, "shaded": shaded, "label": label},
        # math-gate: the fraction read off the figure must equal shaded/total exactly
        # (equiv with k=1 returns the unreduced 'shaded/total' string).
        verify={"op": "equiv", "args": [answer, 1]},
    )


def build_module1():
    add_item(_name_whole_item(
        "m1-1", "A chocolate bar", "A chocolate bar is split into 4 equal squares. Riya eats 1 square.",
        4, 1, "all 4 equal squares of the bar", "the 1 square Riya eats",
        "4 bars", "1/4 of the bar is eaten"))
    add_item(_name_whole_item(
        "m1-2", "Pizza slices", "A pizza is cut into 8 equal slices. 3 slices have mushrooms.",
        8, 3, "all 8 equal slices of the pizza", "the 3 mushroom slices",
        "8 pizzas", "3/8 of the pizza has mushrooms"))
    add_item(_name_whole_item(
        "m1-3", "Garden beds", "A garden is divided into 6 equal beds. Roses grow in 5 beds.",
        6, 5, "all 6 equal beds in the garden", "the 5 rose beds",
        "5 gardens", "5/6 of the garden grows roses"))
    add_item(_name_whole_item(
        "m1-4", "Ribbon pieces", "A ribbon is cut into 5 equal pieces. Dev uses 2 pieces.",
        5, 2, "all 5 equal pieces of ribbon", "the 2 pieces Dev uses",
        "5 ribbons", "2/5 of the ribbon is used"))
    add_item(_name_whole_item(
        "m1-5", "A fruit tray", "A tray holds 10 equal spaces. 7 spaces have apples.",
        10, 7, "all 10 equal spaces on the tray", "the 7 apple spaces",
        "10 trays", "7/10 of the tray holds apples"))
    add_item(_name_whole_item(
        "m1-6", "Window panes", "A window has 12 equal glass panes. 5 panes are frosted.",
        12, 5, "all 12 equal panes of the window", "the 5 frosted panes",
        "12 windows", "5/12 of the window is frosted"))
    add_item(_name_whole_item(
        "m1-7", "A board of stickers", "A sheet has 3 equal rows. Maya fills 2 rows with stars.",
        3, 2, "all 3 equal rows on the sheet", "the 2 star rows",
        "3 sheets", "2/3 of the sheet has stars"))
    add_item(_name_whole_item(
        "m1-8", "Counting blocks", "A strip is built from 12 equal blocks. 11 blocks are blue.",
        12, 11, "all 12 equal blocks in the strip", "the 11 blue blocks",
        "11 strips", "11/12 of the strip is blue"))


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 2 - Part and the rest (complement)
# ─────────────────────────────────────────────────────────────────────────────

def _complement_item(code, title, story, total, shaded, shaded_name, rest_name):
    """Shaded a/total; asked for the UNSHADED complement (b-a)/total.
    verify: sub[1, shaded/total] simplified = complement."""
    rest = total - shaded
    shaded_frac = raw(shaded, total)
    ans_frac = Fraction(rest, total)          # reduced leftover
    answer = ffrac(ans_frac)
    # distractor: giving the SHADED part instead of the leftover (the classic seed trap)
    shaded_reduced = ffrac(Fraction(shaded, total))
    return dict(
        id=code, module=2, title=title, story=story,
        answer=answer,
        stages=[
            stage(
                "What fraction is shaded (the part we are told about)?",
                f"Shaded parts over all parts: {shaded} out of {total}.",
                [
                    o(shaded_frac, True,
                      f"Yes - {shaded} of {total} equal parts are shaded, that is {shaded_frac}."),
                    o(raw(rest, total), False,
                      "That is the leftover part, not the shaded part the story gives us."),
                    o(raw(shaded, rest), False,
                      "The bottom must be ALL equal parts ({}), not just the leftover ones.".format(total)),
                ],
                key="shaded",
            ),
            stage(
                "The whole is 1. How do we find the part that is NOT shaded?",
                "Take the whole and subtract the shaded part: 1 - shaded.",
                [
                    o(f"1 - {shaded_frac}", True,
                      "Yes - the leftover is the whole minus the shaded part."),
                    o(f"1 + {shaded_frac}", False,
                      "Adding makes more than one whole. The rest is a PART of the same whole."),
                    o(f"{shaded_frac} again", False,
                      "That repeats the shaded part. We want the part that is LEFT."),
                ],
                key="setup",
            ),
            stage(
                f"So what fraction is {rest_name}?",
                f"{total} parts minus {shaded} shaded leaves {rest} parts.",
                [
                    o(answer, True,
                      f"Yes - {rest} of {total} parts are left, which is {answer}."),
                    o(shaded_reduced if shaded_reduced != answer else shaded_frac, False,
                      "That is the SHADED amount. Re-read: we were asked for the part left over."),
                    o(raw(rest, shaded) if shaded != 0 else raw(rest, total), False,
                      "The bottom stays the total number of equal parts, not the shaded count."),
                ],
                key="rest",
            ),
        ],
        worked=[
            f"The whole is cut into {total} equal parts.",
            f"Shaded part = {shaded}/{total}.",
            f"Leftover = whole - shaded = 1 - {shaded_frac} = {rest}/{total}.",
            f"In lowest terms that is {answer}.",
        ],
        check=f"Shaded {shaded_frac} and leftover {answer} add back to the whole, 1.",
        explain="Why do the shaded and leftover parts always share the same bottom number?",
        model={"type": "parts", "total": total, "shaded": shaded,
               "label": f"{shaded_frac} shaded, {rest}/{total} left"},
        verify={"op": "sub", "args": ["1", shaded_frac]},
    )


def build_module2():
    add_item(_complement_item("m2-1", "Coloured squares",
        "A grid of 8 equal squares has 3 squares coloured. The rest are plain.",
        8, 3, "coloured", "plain (not coloured)"))
    add_item(_complement_item("m2-2", "Eaten and left",
        "A chocolate bar has 10 equal pieces. 7 pieces are eaten.",
        10, 7, "eaten", "still left"))
    add_item(_complement_item("m2-3", "Painted fence",
        "A fence has 6 equal planks. 2 planks are painted so far.",
        6, 2, "painted", "not yet painted"))
    add_item(_complement_item("m2-4", "Full seats",
        "A bench has 5 equal seats. 4 seats are full.",
        5, 4, "full", "empty"))
    add_item(_complement_item("m2-5", "Read pages",
        "A short book has 12 equal sections. Aarav has read 5 sections.",
        12, 5, "already read", "still to read"))
    add_item(_complement_item("m2-6", "Ripe mangoes",
        "A basket holds 4 equal rows of mangoes. 1 row is ripe.",
        4, 1, "ripe", "not ripe yet"))
    add_item(_complement_item("m2-7", "Finished beads",
        "A bracelet plan has 3 equal parts. 2 parts are threaded.",
        3, 2, "threaded", "not threaded yet"))
    add_item(_complement_item("m2-8", "Solved puzzles",
        "A puzzle book has 10 equal pages. Meera solved 3 pages.",
        10, 3, "solved", "not solved yet"))


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 3 - Equivalent fractions
# ─────────────────────────────────────────────────────────────────────────────

def _equiv_item(code, title, story, a, b, k):
    """Rename a/b by scaling by k. answer = UNREDUCED (a*k)/(b*k).
    verify: equiv[a/b, k]. The 'add k to both' misconception distractor is a+k/b+k."""
    base = raw(a, b)
    answer = equiv_str(base, k)          # (a*k)/(b*k) unreduced
    add_wrong = raw(a + k, b + k)        # classic 'added the same number' error
    top_only = raw(a * k, b)             # scaled top only
    return dict(
        id=code, module=3, title=title, story=story,
        answer=answer,
        stages=[
            stage(
                f"We want to rewrite {base} with bottom {b * k}. What do we do to the bottom?",
                f"{b} times what gives {b * k}? That same move must happen to the top.",
                [
                    o(f"Multiply the bottom by {k}", True,
                      f"Yes - {b} x {k} = {b * k}, so we scale by {k}."),
                    o(f"Add {k} to the bottom", False,
                      f"Adding changes the value. {b} + {k} is not a scaling of {b}."),
                    o(f"Multiply the bottom by {k + 1}", False,
                      f"That would give {b * (k + 1)}, not {b * k}. Check the target bottom."),
                ],
                key="scale",
            ),
            stage(
                "To keep the SAME value, what must we do to the top?",
                "Whatever we do to the bottom, we do the SAME to the top.",
                [
                    o(f"Multiply the top by {k} too", True,
                      f"Yes - scale top and bottom by the same {k} to keep the value."),
                    o(f"Add {k} to the top", False,
                      "Adding the same number to top and bottom changes the fraction's value."),
                    o("Leave the top as it is", False,
                      "Changing only the bottom makes a different fraction, not an equal one."),
                ],
                key="same",
            ),
            stage(
                f"So {base} is equal to which fraction?",
                f"Top: {a} x {k} = {a * k}. Bottom: {b} x {k} = {b * k}.",
                [
                    o(answer, True,
                      f"Yes - {a} x {k} over {b} x {k} is {answer}, equal to {base}."),
                    o(add_wrong, False,
                      f"This added {k} to both. Equivalent fractions come from multiplying, not adding."),
                    o(top_only, False,
                      "Only the top was scaled. Both top and bottom must scale by the same number."),
                ],
                key="result",
            ),
        ],
        worked=[
            f"Start with {base}.",
            f"Multiply the bottom by {k}: {b} x {k} = {b * k}.",
            f"Multiply the top by the same {k}: {a} x {k} = {a * k}.",
            f"So {base} = {answer}.",
        ],
        check=f"{answer} scales back down by {k} to {base}, so they are equal.",
        explain="Why does multiplying top and bottom by the same number keep the value?",
        model={"type": "mapping", "rows": [[base, answer], ["x" + str(k) + " top", "x" + str(k) + " bottom"]]},
        verify={"op": "equiv", "args": [base, k]},
    )


def build_module3():
    add_item(_equiv_item("m3-1", "Halves to quarters",
        "A cake is cut in 2 equal halves, then every half is cut again into 2.", 1, 2, 2))
    add_item(_equiv_item("m3-2", "Thirds to sixths",
        "A ribbon shows 1/3. We cut each third into 2 equal bits.", 1, 3, 2))
    add_item(_equiv_item("m3-3", "Fourths to eighths",
        "A pizza shows 3/4. Each quarter is sliced into 2.", 3, 4, 2))
    add_item(_equiv_item("m3-4", "Fifths to tenths",
        "A strip shows 2/5. Each fifth is split into 2 equal parts.", 2, 5, 2))
    add_item(_equiv_item("m3-5", "Match to twelfths",
        "A chart shows 3/4 and we want the same value in twelfths.", 3, 4, 3))
    add_item(_equiv_item("m3-6", "Fill the twenty-fifths",
        "A grid shows 3/5. We rename it over 25.", 3, 5, 5))
    add_item(_equiv_item("m3-7", "Sixths into twelfths",
        "A tray shows 5/6. We rename it over 12.", 5, 6, 2))
    add_item(_equiv_item("m3-8", "Eighths into thirty-seconds",
        "A board shows 7/8. We rename it over 32.", 7, 8, 4))


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 4 - Compare fractions
# ─────────────────────────────────────────────────────────────────────────────

def _compare_item(code, title, story, fa, fb, same_denom):
    """Which is greater, fa or fb? answer = the greater (reduced). verify: larger."""
    a, b = F(fa), F(fb)
    greater = fa if a > b else fb
    ans = ffrac(max(a, b))
    lcm = a.denominator * b.denominator // _gcd(a.denominator, b.denominator)
    an = a.numerator * (lcm // a.denominator)
    bn = b.numerator * (lcm // b.denominator)
    bigger_denom = fa if a.denominator > b.denominator else fb
    if same_denom:
        setup = stage(
            "The bottoms are the same. How do we compare?",
            "Equal parts of the same size - so just compare the TOP numbers.",
            [
                o("Compare the top numbers; bigger top wins", True,
                  "Yes - same size parts, so more parts (bigger top) means a bigger fraction."),
                o("Compare the bottom numbers", False,
                  "The bottoms are equal here, so they cannot decide it - look at the tops."),
                o("The bigger bottom is always bigger", False,
                  "A bigger bottom means smaller slices, not a bigger fraction."),
            ],
            key="method",
        )
    else:
        setup = stage(
            "The bottoms are different. What is the first move?",
            "Give both fractions a common bottom before comparing.",
            [
                o(f"Rename both over a common denominator ({lcm})", True,
                  f"Yes - over {lcm} we can compare fairly."),
                o("Just pick the one with the bigger bottom", False,
                  "A bigger bottom means smaller slices - it does NOT win automatically."),
                o("Just pick the one with the bigger top", False,
                  "Tops only compare fairly once the bottoms match."),
            ],
            key="method",
        )
    if same_denom:
        third = stage(
            f"So which is greater, {fa} or {fb}?",
            "Same bottom - the bigger top number is the bigger fraction.",
            [
                o(greater, True, f"Yes - {greater} has the bigger top over the same bottom."),
                o(fb if greater == fa else fa, False,
                  "That one has the smaller top over the same bottom, so it is smaller."),
                o("They are equal", False,
                  "The tops are different over the same bottom, so they are not equal."),
            ],
            key="pick",
        )
    else:
        third = stage(
            f"Over {lcm}: {fa} = {an}/{lcm} and {fb} = {bn}/{lcm}. Which is greater?",
            "Now the bottoms match, so compare the new tops.",
            [
                o(greater, True,
                  f"Yes - {max(an, bn)}/{lcm} is bigger, so {greater} is the greater fraction."),
                o(bigger_denom if bigger_denom != greater else (fb if greater == fa else fa), False,
                  "Watch out - the bigger bottom often tricks us, but smaller slices can mean a smaller value."),
                o("They are equal", False,
                  f"{an}/{lcm} and {bn}/{lcm} are different, so the fractions are not equal."),
            ],
            key="pick",
        )
    return dict(
        id=code, module=4, title=title, story=story,
        answer=ans,
        stages=[
            stage(
                "Before comparing, check: are the bottom numbers the same?",
                f"Look at the denominators of {fa} and {fb}.",
                [
                    o("Yes, the bottoms are the same" if same_denom else "No, the bottoms are different",
                      True, "Good check - that tells us which method to use."),
                    o("No, the bottoms are different" if same_denom else "Yes, the bottoms are the same",
                      False, "Look again at the two bottom numbers."),
                    o("The tops tell us the bottoms", False,
                      "The top numbers do not decide the bottoms - read the denominators."),
                ],
                key="check",
            ),
            setup,
            third,
        ],
        worked=(
            [f"Both have the same bottom.", f"Compare the tops: {greater} has the bigger top.",
             f"So {greater} is greater."] if same_denom else
            [f"Rename both over {lcm}.", f"{fa} = {an}/{lcm}, {fb} = {bn}/{lcm}.",
             f"{max(an, bn)}/{lcm} is bigger, so {greater} is greater."]
        ),
        check=f"The greater fraction is {ans}.",
        explain="Why can a fraction with a bigger bottom number be the SMALLER fraction?",
        model={"type": "bar", "share": 50, "whole": f"compare {fa} and {fb}",
               "left": f"{fa}", "right": f"{fb}"},
        verify={"op": "larger", "args": [fa, fb]},
    )


def _gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def build_module4():
    add_item(_compare_item("m4-1", "Same bottom, pick bigger",
        "Two juice jugs are marked 3/8 full and 5/8 full. Which has more?",
        "3/8", "5/8", True))
    add_item(_compare_item("m4-2", "Sevenths race",
        "Two snails crawl 2/7 and 5/7 of a path. Which went further?",
        "5/7", "2/7", True))
    add_item(_compare_item("m4-3", "Tenths of a tank",
        "One tank is 7/10 full, another is 4/10 full. Which is fuller?",
        "7/10", "4/10", True))
    add_item(_compare_item("m4-4", "Tiny slices trick",
        "Is 1/8 of a pizza more than 2/5 of the same pizza?",
        "1/8", "2/5", False))
    add_item(_compare_item("m4-5", "Which is greater",
        "A recipe uses 3/5 cup and another uses 1/8 cup. Which is more?",
        "3/5", "1/8", False))
    add_item(_compare_item("m4-6", "Ribbon lengths",
        "One ribbon is 2/3 metre, another is 1/5 metre. Which is longer?",
        "2/3", "1/5", False))
    add_item(_compare_item("m4-7", "Thirds and sixths",
        "Is 6/7 of a cake more than 2/3 of the same cake?",
        "6/7", "2/3", False))
    add_item(_compare_item("m4-8", "Fifths and sevenths",
        "A walk is 5/7 done; a jog is 1/3 done. Which is further along?",
        "5/7", "1/3", False))


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 5 - Add / subtract LIKE fractions
# ─────────────────────────────────────────────────────────────────────────────

def _raw_parts(s):
    """Return (numerator, denominator) EXACTLY as written (no reducing)."""
    n, d = str(s).split("/")
    return int(n), int(d)


def _like_item(code, title, story, fa, fb, op, total):
    """op in {add, sub}. Same denominator. answer reduced. verify: add/sub.

    We read the numerators/denominators AS WRITTEN (not via Fraction, which would
    reduce e.g. 4/8 -> 1/2 and break the 'same bottom' narrative). The final
    answer is still recomputed+reduced by the math-gate's add/sub op."""
    na, d = _raw_parts(fa)
    nb, d2 = _raw_parts(fb)
    assert d == d2, f"{code}: like-fractions need equal written bottoms"
    a, b = F(fa), F(fb)
    if op == "add":
        res = a + b
        sign = "+"
        combined = na + nb
    else:
        res = a - b
        sign = "-"
        combined = na - nb
    answer = ffrac(res)
    keep_denom = raw(combined, d)                 # tops combined, bottom kept (pre-simplify)
    # Wrong A: "added the bottoms too" (classic like-fraction misconception).
    wrong_bottom = raw(combined, d + d)
    # Wrong B: prefer the unsimplified correct-top-over-correct-bottom form when it
    # differs from the final answer; otherwise show "bottoms doubled AND halved tops"
    # style slip. Both are guaranteed distinct from the answer and from wrong_bottom.
    if keep_denom != answer and keep_denom != wrong_bottom:
        wrong_second = keep_denom
        wrong_second_fb = (False, "Close - that is right before simplifying. Reduce it to lowest terms.")
    elif fa != answer and fa != wrong_bottom:
        # answer already in lowest terms: use the "kept one fraction unchanged" slip.
        wrong_second = fa
        wrong_second_fb = (False, f"That is just one of the fractions - we still have to {op} the second one.")
    else:
        # last resort: "doubled the bottom AND the top" slip, always distinct.
        wrong_second = raw(combined * 2, d + d)
        wrong_second_fb = (False, "Both the top and the bottom were doubled - only work the tops, keep the bottom.")
    return dict(
        id=code, module=5, title=title, story=story,
        answer=answer,
        stages=[
            stage(
                "Are the bottom numbers the same?",
                f"Both fractions have bottom {d}.",
                [
                    o(f"Yes, both are {d}", True,
                      "Good - with matching bottoms we work on the tops only."),
                    o("No, they are different", False,
                      f"Look again - both bottoms are {d}."),
                    o("We must add the bottoms first", False,
                      "We never add the bottoms - equal parts stay the same size."),
                ],
                key="check",
            ),
            stage(
                f"What happens to the bottom number when we {op} these?",
                "Same size parts, so the bottom stays exactly the same.",
                [
                    o(f"It stays {d}", True,
                      f"Yes - the size of each part does not change, so the bottom stays {d}."),
                    o(f"It becomes {d + d}", False,
                      "That adds the bottoms. The parts did not get smaller, so keep the bottom."),
                    o("It disappears", False,
                      "We still have fraction parts, so we still need the bottom number."),
                ],
                key="denominator",
            ),
            stage(
                f"So what is {fa} {sign} {fb}?",
                f"{sign.replace('+','Add').replace('-','Subtract')} the tops: {na} {sign} {nb} = {combined}; keep bottom {d}.",
                [
                    o(answer, True,
                      f"Yes - {na} {sign} {nb} = {combined} over {d}, which is {answer}."),
                    o(wrong_bottom, False,
                      "This changed the bottom too. Keep the bottom the same and only work the tops."),
                    o(wrong_second, wrong_second_fb[0], wrong_second_fb[1]),
                ],
                key="result",
            ),
        ],
        worked=[
            f"The bottoms match ({d}), so keep the bottom {d}.",
            f"Work the tops: {na} {sign} {nb} = {combined}.",
            f"That gives {combined}/{d}.",
            f"In lowest terms that is {answer}.",
        ],
        check=f"The parts stayed size 1/{d} the whole way, giving {answer}.",
        explain="Why do we keep the bottom the same when the parts are the same size?",
        model={"type": "parts", "total": total, "shaded": min(total, max(0, int(res * total))),
               "label": f"{fa} {sign} {fb} = {answer}"},
        verify={"op": op, "args": [fa, fb]},
    )


def build_module5():
    add_item(_like_item("m5-1", "Add eighths",
        "A jar fills 4/8 then another 3/8 of juice.", "4/8", "3/8", "add", 8))
    add_item(_like_item("m5-2", "Add sixths",
        "Dev reads 1/6 of a story, then 4/6 more.", "1/6", "4/6", "add", 6))
    add_item(_like_item("m5-3", "Add ninths",
        "A path is painted 7/9, then 4/9 extra of a second path.", "7/9", "4/9", "add", 9))
    add_item(_like_item("m5-4", "Add to a half",
        "A cup holds 3/8, then 1/8 more is poured in.", "3/8", "1/8", "add", 8))
    add_item(_like_item("m5-5", "Subtract tenths",
        "A tank is 9/10 full and 6/10 is used.", "9/10", "6/10", "sub", 10))
    add_item(_like_item("m5-6", "Subtract sevenths",
        "A ribbon is 6/7 long and 2/7 is cut off.", "6/7", "2/7", "sub", 7))
    add_item(_like_item("m5-7", "Subtract twelfths",
        "A chart shows 11/12 and 5/12 is erased.", "11/12", "5/12", "sub", 12))
    add_item(_like_item("m5-8", "Add tenths over one",
        "A pitcher fills 6/10, then 6/10 more into a bigger jug.", "6/10", "6/10", "add", 10))


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 6 - Add / subtract UNLIKE fractions
# ─────────────────────────────────────────────────────────────────────────────

def _unlike_item(code, title, story, fa, fb, op):
    """Different denominators. Rename to common denom, then add/sub. verify add/sub."""
    a, b = F(fa), F(fb)
    lcm = a.denominator * b.denominator // _gcd(a.denominator, b.denominator)
    # "multiply the bottoms" over-shoot: a valid but non-minimal common bottom.
    # Guarantee it differs from lcm (and the "added bottoms" distractor) for a
    # clean 3-option step even when one denominator already IS the lcm.
    prod_denom = a.denominator * b.denominator
    sum_denom = a.denominator + b.denominator
    if prod_denom == lcm or prod_denom == sum_denom:
        prod_denom = lcm * 2
    an = a.numerator * (lcm // a.denominator)
    bn = b.numerator * (lcm // b.denominator)
    if op == "add":
        res = a + b
        sign = "+"
        across_wrong = raw(a.numerator + b.numerator, a.denominator + b.denominator)
        combined_top = an + bn
    else:
        res = a - b
        sign = "-"
        across_wrong = raw(a.numerator - b.numerator, a.denominator - b.denominator) \
            if a.denominator - b.denominator != 0 else raw(a.numerator - b.numerator, lcm)
        combined_top = an - bn
    answer = ffrac(res)
    common_form = raw(combined_top, lcm)
    return dict(
        id=code, module=6, title=title, story=story,
        answer=answer,
        stages=[
            stage(
                "The bottoms are different. Can we work the tops straight away?",
                "Not yet - the parts are different sizes until we make a common bottom.",
                [
                    o("No - first give both the same bottom", True,
                      "Right - different size parts cannot be combined until they match."),
                    o(f"Yes - just do {a.numerator} {sign} {b.numerator} over {a.denominator} {sign} {b.denominator}", False,
                      "That combines across different bottoms, which changes the sizes unfairly."),
                    o("Yes - keep the bigger bottom and work the tops", False,
                      "Both fractions must be renamed, not just one kept as it is."),
                ],
                key="check",
            ),
            stage(
                f"What common bottom works for {a.denominator} and {b.denominator}?",
                f"A number both {a.denominator} and {b.denominator} divide into is {lcm}.",
                [
                    o(str(lcm), True,
                      f"Yes - {lcm} works because {a.denominator} and {b.denominator} both divide it."),
                    o(str(a.denominator + b.denominator), False,
                      f"Adding the bottoms gives {a.denominator + b.denominator}, but {b.denominator} may not divide it evenly."),
                    o(str(prod_denom), False,
                      f"Multiplying the bottoms gives {prod_denom} - it works, but {lcm} is the smaller, simpler common bottom here."),
                ],
                key="common",
            ),
            stage(
                f"Rename: {fa} = {an}/{lcm}, {fb} = {bn}/{lcm}. What is {fa} {sign} {fb}?",
                f"Now work the tops: {an} {sign} {bn} = {combined_top}, keep bottom {lcm}.",
                [
                    o(answer, True,
                      f"Yes - {an} {sign} {bn} = {combined_top} over {lcm}, which is {answer}."),
                    o(across_wrong, False,
                      "This combined across the different bottoms instead of renaming first."),
                    o(common_form if common_form != answer else raw(combined_top, lcm + 1), False,
                      ("Good setup - now simplify to lowest terms." if common_form != answer
                       else "Check the common bottom - it should be {}.".format(lcm))),
                ],
                key="result",
            ),
        ],
        worked=[
            f"The bottoms differ, so rename over {lcm}.",
            f"{fa} = {an}/{lcm} and {fb} = {bn}/{lcm}.",
            f"Work the tops: {an} {sign} {bn} = {combined_top}, giving {combined_top}/{lcm}.",
            f"In lowest terms that is {answer}.",
        ],
        check=f"Both parts are now size 1/{lcm}, giving {answer}.",
        explain="Why must the parts be the same size before we add or subtract them?",
        model={"type": "mapping", "rows": [[fa, f"{an}/{lcm}"], [fb, f"{bn}/{lcm}"]]},
        verify={"op": op, "args": [fa, fb]},
    )


def build_module6():
    add_item(_unlike_item("m6-1", "Half plus a quarter",
        "A glass gets 1/2 of water, then 1/4 more.", "1/2", "1/4", "add"))
    add_item(_unlike_item("m6-2", "Third plus a sixth",
        "A path is 1/3 paved, then 1/6 more is paved.", "1/3", "1/6", "add"))
    add_item(_unlike_item("m6-3", "Half plus a third",
        "A jar fills 1/2, then 1/3 more of a smaller pour.", "1/2", "1/3", "add"))
    add_item(_unlike_item("m6-4", "Quarter plus a sixth",
        "A wall is 1/4 painted, then 1/6 more.", "1/4", "1/6", "add"))
    add_item(_unlike_item("m6-5", "Half minus a third",
        "A tank is 1/2 full and 1/3 is used.", "1/2", "1/3", "sub"))
    add_item(_unlike_item("m6-6", "Three-quarters minus a half",
        "A ribbon is 3/4 metre and 1/2 metre is cut off.", "3/4", "1/2", "sub"))
    add_item(_unlike_item("m6-7", "Five-sixths minus a third",
        "A bottle is 5/6 full and 1/3 is poured out.", "5/6", "1/3", "sub"))
    add_item(_unlike_item("m6-8", "Two-thirds minus a quarter",
        "A sheet is 2/3 coloured and 1/4 is rubbed out.", "2/3", "1/4", "sub"))


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 7 - Mixed <-> improper
# ─────────────────────────────────────────────────────────────────────────────

def _ordinal_parts(den):
    """Plural name of a 1/den part: 'halves', 'thirds', ... else 'parts of {den}'."""
    names = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths",
             7: "sevenths", 8: "eighths", 9: "ninths", 10: "tenths", 12: "twelfths"}
    return names.get(den, f"parts of size 1/{den}")


def _to_improper_item(code, title, story, whole, num, den):
    """Mixed w num/den -> improper. answer = (w*den+num)/den (reduced by fmt_frac,
    but we choose den so it does not reduce). verify to_improper."""
    mixed = f"{whole} {num}/{den}"
    val = F(mixed)
    answer = ffrac(val)                       # improper, lowest terms
    stick_wrong = f"{whole}{num}/{den}"       # 2 3/5 -> 23/5 (stick whole in front)
    add_to_top_wrong = raw(whole + num, den)  # added whole to the top
    improper_top = whole * den + num
    return dict(
        id=code, module=7, title=title, story=story,
        answer=answer,
        stages=[
            stage(
                f"To make {mixed} improper, what do we multiply first?",
                "Multiply the whole number by the bottom.",
                [
                    o(f"The whole {whole} times the bottom {den}", True,
                      f"Yes - {whole} x {den} = {whole * den} is how many {_ordinal_parts(den)} are in the wholes."),
                    o(f"The whole {whole} times the top {num}", False,
                      "We multiply the whole by the BOTTOM, not the top."),
                    o(f"Just write {whole} in front of {num}", False,
                      f"That gives {stick_wrong}, which is not the same value."),
                ],
                key="multiply",
            ),
            stage(
                f"Now add the top. What is {whole * den} + {num}?",
                f"Add the existing top {num} to {whole * den}.",
                [
                    o(str(improper_top), True,
                      f"Yes - {whole * den} + {num} = {improper_top} parts in total."),
                    o(str(whole + num), False,
                      f"That added the whole to the top directly, skipping the x {den} step."),
                    o(str(whole * den), False,
                      "That forgot to add the leftover top number from the mixed fraction."),
                ],
                key="addtop",
            ),
            stage(
                f"So {mixed} as an improper fraction is...?",
                f"Top {improper_top} over the same bottom {den}.",
                [
                    o(answer, True,
                      f"Yes - {improper_top}/{den} is {mixed} written as an improper fraction."),
                    o(stick_wrong, False,
                      f"That just stuck {whole} in front of {num}. We must do whole x bottom + top."),
                    o(add_to_top_wrong, False,
                      "That added the whole straight onto the top without multiplying by the bottom."),
                ],
                key="result",
            ),
        ],
        worked=[
            f"Multiply whole by bottom: {whole} x {den} = {whole * den}.",
            f"Add the top: {whole * den} + {num} = {improper_top}.",
            f"Keep the bottom {den}.",
            f"So {mixed} = {answer}.",
        ],
        check=f"{answer} divides back to {whole} remainder {num}, which is {mixed}.",
        explain="Why do we multiply the whole by the bottom before adding the top?",
        verify={"op": "to_improper", "args": [mixed]},
    )


def _to_mixed_item(code, title, story, num, den):
    """Improper num/den -> mixed. answer = mixed string. verify to_mixed."""
    improper = raw(num, den)
    val = Fraction(num, den)
    answer = fmixed(val)
    whole = num // den
    rem = num - whole * den
    swap_wrong = f"{rem} {whole}/{den}" if rem else str(whole)   # swapped whole and remainder
    return dict(
        id=code, module=7, title=title, story=story,
        answer=answer,
        stages=[
            stage(
                f"How many whole groups of {den} are in {num}?",
                f"Divide: {num} divided by {den}.",
                [
                    o(f"{whole} wholes", True,
                      f"Yes - {den} goes into {num} {whole} times."),
                    o(f"{whole + 1} wholes", False,
                      f"{den} x {whole + 1} = {den * (whole + 1)}, which is too many."),
                    o(f"{num} wholes", False,
                      f"That ignores the grouping by {den}. Divide {num} by {den} first."),
                ],
                key="divide",
            ),
            stage(
                f"What is left over after {whole} whole groups?",
                f"{num} - {whole} x {den} = {rem}.",
                [
                    o(f"{rem} parts left", True,
                      f"Yes - {num} - {whole * den} = {rem} parts remain."),
                    o(f"{den} parts left", False,
                      "A full group would be swapped into another whole - the remainder is smaller than the bottom."),
                    o("0 parts left", False,
                      f"{num} is not an exact multiple of {den}, so some parts remain."),
                ],
                key="remainder",
            ),
            stage(
                f"So {improper} as a mixed number is...?",
                f"{whole} wholes and {rem}/{den} left over.",
                [
                    o(answer, True,
                      f"Yes - {whole} and {rem}/{den} is {answer}."),
                    o(swap_wrong, False,
                      "The whole and the leftover got swapped. The whole count goes first."),
                    o(raw(whole, den), False,
                      "The leftover top should be the remainder, not the whole count."),
                ],
                key="result",
            ),
        ],
        worked=[
            f"Divide {num} by {den}: {whole} wholes.",
            f"Remainder: {num} - {whole * den} = {rem}.",
            f"Write the leftover as {rem}/{den}.",
            f"So {improper} = {answer}.",
        ],
        check=f"{whole} x {den} + {rem} = {num}, so {answer} is {improper}.",
        explain="Why does the remainder become the new top of the fraction part?",
        verify={"op": "to_mixed", "args": [improper]},
    )


def build_module7():
    add_item(_to_improper_item("m7-1", "Two and a third", "A baker has 2 whole cakes and 1/3 of another.", 2, 1, 3))
    add_item(_to_improper_item("m7-2", "One and two-fifths", "A jug holds 1 whole litre and 2/5 more.", 1, 2, 5))
    add_item(_to_improper_item("m7-3", "Three and a quarter", "A ribbon is 3 whole metres and 1/4 metre.", 3, 1, 4))
    add_item(_to_improper_item("m7-4", "Two and three-sevenths", "A tray has 2 full boxes and 3/7 of one.", 2, 3, 7))
    add_item(_to_mixed_item("m7-5", "Seven halves", "A recipe needs 7/2 cups of flour.", 7, 2))
    add_item(_to_mixed_item("m7-6", "Eleven thirds", "A rope is 11/3 metres long.", 11, 3))
    add_item(_to_mixed_item("m7-7", "Nine quarters", "A tank holds 9/4 buckets of water.", 9, 4))
    add_item(_to_mixed_item("m7-8", "Seventeen fifths", "A wall needs 17/5 tins of paint.", 17, 5))


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 8 - Fraction OF a quantity
# ─────────────────────────────────────────────────────────────────────────────

def _of_item(code, title, story, fa, qty, unit, ask_left):
    """a/b OF qty. If ask_left, answer = (1 - a/b) of qty (the leftover). verify of."""
    frac = F(fa)
    one_part = qty // frac.denominator
    taken = frac * qty
    taken_int = int(taken)
    if ask_left:
        want = Fraction(1) - frac
        want_frac_str = ffrac(want)
        answer_val = want * qty
        answer = ffrac(answer_val)
        verify = {"op": "of", "args": [want_frac_str, str(qty)]}
        third_prompt = f"So how many {unit} are LEFT (not given away)?"
        taken_desc = f"given away = {fa} of {qty} = {taken_int}"
        ans_desc = f"left = {qty} - {taken_int} = {answer}"
    else:
        answer_val = taken
        answer = ffrac(answer_val)
        verify = {"op": "of", "args": [fa, str(qty)]}
        third_prompt = f"So what is {fa} of {qty} {unit}?"
        taken_desc = ""
        ans_desc = f"{fa} of {qty} = {answer}"
    num = frac.numerator
    den = frac.denominator
    divide_by_top_wrong = qty // num if num and qty % num == 0 else round(qty / num)
    # "one equal part" distractors, guaranteed distinct from one_part and from qty.
    if num > 1 and divide_by_top_wrong not in (one_part, qty):
        onepart_wrong = divide_by_top_wrong
        onepart_wrong_fb = f"That divided by the TOP ({num}). We divide by the bottom to make one equal part."
    else:
        onepart_wrong = qty * den                      # multiplied instead of divided
        onepart_wrong_fb = f"That multiplied by {den} instead of dividing - one part is SMALLER than the whole."

    # Result-step distractors, each guaranteed distinct from the answer.
    answer_num = int(answer)                            # all module-8 answers are whole numbers
    if ask_left:
        # Wrong A: gave the GIVEN-AWAY amount instead of what is left.
        result_wrong_a = str(taken_int)
        result_wrong_a_fb = "That is the amount given AWAY - we were asked how many are LEFT."
        # Wrong B: just one equal part (or the whole, if one_part clashes).
        cand = one_part
        if cand == answer_num or cand == taken_int:
            cand = qty
            result_wrong_b_fb = "That is the whole starting amount - some was given away, so less is left."
        else:
            result_wrong_b_fb = "That is only one equal part, not the full leftover amount."
        result_wrong_b = str(cand)
    else:
        # Wrong A: only ONE equal part (forgot to take 'num' of them).
        cand_a = one_part
        if cand_a == answer_num:
            cand_a = qty
        result_wrong_a = str(cand_a)
        result_wrong_a_fb = f"That is only ONE equal part - take {num} parts for {fa}."
        # Wrong B: divided by the top instead of the bottom.
        cand_b = divide_by_top_wrong
        if cand_b == answer_num or str(cand_b) == result_wrong_a:
            cand_b = qty * den
        result_wrong_b = str(cand_b)
        result_wrong_b_fb = "That used the top as the divider. Divide by the bottom, then take the top parts."
    return dict(
        id=code, module=8, title=title, story=story,
        answer=answer, unit=unit,
        stages=[
            stage(
                f"'{fa} of {qty}' - what does the word 'of' tell us to do?",
                "'of' means multiply the fraction by the quantity.",
                [
                    o("Multiply the fraction by the quantity", True,
                      "Yes - a fraction OF an amount means we multiply."),
                    o("Add the fraction to the quantity", False,
                      "'of' is not adding - it takes a part of the amount."),
                    o("Subtract the top from the quantity", False,
                      "'of' is not subtracting - it shares the amount into equal parts."),
                ],
                key="meaning",
            ),
            stage(
                f"First find ONE equal part: {qty} divided into {frac.denominator} parts is...?",
                f"Divide by the BOTTOM: {qty} divided by {frac.denominator}.",
                [
                    o(f"{one_part} {unit}", True,
                      f"Yes - one part is {qty} divided by {frac.denominator} = {one_part}."),
                    o(f"{onepart_wrong} {unit}", False, onepart_wrong_fb),
                    o(f"{qty} {unit}", False,
                      "That is the whole amount, not one equal part of it."),
                ],
                key="onepart",
            ),
            stage(
                third_prompt,
                (f"Take {num} parts: {num} x {one_part}. " if not ask_left
                 else f"Given away is {num} x {one_part} = {taken_int}; the rest is left."),
                [
                    o(answer, True,
                      f"Yes - {ans_desc}."),
                    o(result_wrong_a, False, result_wrong_a_fb),
                    o(result_wrong_b, False, result_wrong_b_fb),
                ],
                key="result",
            ),
        ],
        worked=(
            [f"'of' means multiply.",
             f"One part: {qty} divided by {frac.denominator} = {one_part}.",
             taken_desc,
             ans_desc] if ask_left else
            [f"'of' means multiply.",
             f"One part: {qty} divided by {frac.denominator} = {one_part}.",
             f"Take {num} parts: {num} x {one_part} = {taken_int}.",
             f"So {fa} of {qty} = {answer}."]
        ),
        check=f"The answer {answer} fits within the whole of {qty} {unit}.",
        explain="Why do we divide by the bottom before multiplying by the top?",
        model={"type": "groups", "caps": [frac.denominator], "labels": [f"{qty} {unit}"],
               "target": f"{fa} of {qty}", "capLabel": "equal parts"},
        verify=verify,
    )


def build_module8():
    add_item(_of_item("m8-1", "Half of the marbles", "Dev has 30 marbles and gives 1/3 of them away.",
        "1/3", 30, "marbles", True))
    add_item(_of_item("m8-2", "Quarter of a set", "Riya has 60 marbles and gives 1/4 of them away.",
        "1/4", 60, "marbles", True))
    add_item(_of_item("m8-3", "Three-quarters of forty", "Meera has 40 stickers; 3/4 of them are stars.",
        "3/4", 40, "stickers", False))
    add_item(_of_item("m8-4", "Two-thirds of ninety", "A box has 90 beads and 2/3 are red.",
        "2/3", 90, "beads", False))
    add_item(_of_item("m8-5", "Give away four-fifths", "Dev has 40 marbles and gives 4/5 of them away.",
        "4/5", 40, "marbles", True))
    add_item(_of_item("m8-6", "Three-eighths of a bag", "A bag has 48 sweets and 3/8 are lemon.",
        "3/8", 48, "sweets", False))
    add_item(_of_item("m8-7", "Two-fifths of thirty", "A garden has 30 plants and 2/5 are roses.",
        "2/5", 30, "plants", False))
    add_item(_of_item("m8-8", "Five-sixths of a crate", "A crate has 24 apples and 5/6 are ripe.",
        "5/6", 24, "apples", False))


def main():
    src = build_source()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(src, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {OUT}")
    print(f"  {len(MODULES)} modules, {len(QUESTIONS)} items")


if __name__ == "__main__":
    main()
