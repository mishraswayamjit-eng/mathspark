#!/usr/bin/env python3
"""
Author the Grade-5 "Fraction Sense" Concept Trainer SOURCE JSON.

This script BUILDS the source dict (modules + questions) in Python so that every
fraction answer is COMPUTED with `fractions.Fraction` — never hand-typed — and
then writes `scripts/sources/fractions-g5-source.json`.

Feed the output to the shared generator/validator:

    python scripts/generate_trainer.py scripts/sources/fractions-g5-source.json

The generator reshapes it into `data/concept-trainers/fractions-g5.json` and
recomputes every item's `verify` spec (the math gate).

Design: a Concept Trainer item trains the *reasoning structure* of a concept.
Each item = short story -> THREE thinking-step MCQs (each wrong option names a
real misconception drawn from the IPM seed extract) -> a picture -> a worked
solution. 10 modules x 8 items = 80 items, Core -> Stretch, numbers escalating
beyond Grade 4 (7, 9, 11, 12, 16, ... and real reductions like 187/136).

NON-NEGOTIABLE tone: warm & encouraging; never "wrong / incorrect / failed /
error"; wrong-option feedback is a gentle teaching moment that NAMES the
misconception.
"""

import json
import os
from fractions import Fraction
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "sources", "fractions-g5-source.json")


# ── fraction helpers (every answer is computed, never guessed) ───────────────

def F(n, d=1):
    return Fraction(n, d)


def fs(f: Fraction) -> str:
    """Canonical short string: 'n' if integer else lowest-terms 'n/d'."""
    f = Fraction(f)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def mixed(f: Fraction) -> str:
    """Mixed-number string '4 1/5' (or 'n' / 'n/d' when not a mixed number)."""
    f = Fraction(f)
    if f.denominator == 1:
        return str(f.numerator)
    if abs(f.numerator) < f.denominator:
        return fs(f)
    sign = "-" if f < 0 else ""
    a = abs(f)
    whole = a.numerator // a.denominator
    rem = a - whole
    return f"{sign}{whole} {rem.numerator}/{rem.denominator}"


def unreduced(n: int, d: int) -> str:
    """Literal 'n/d' (NOT reduced) — for showing an equivalent-fraction build."""
    return f"{n}/{d}"


def dec(f: Fraction, places=3) -> str:
    """Short decimal for gentle 'about 0.73' feedback."""
    return f"{float(f):.{places}f}".rstrip("0").rstrip(".")


# ── tiny builders to keep every item uniform ─────────────────────────────────

def opt(text, correct, feedback):
    return {"text": text, "correct": correct, "feedback": feedback}


def stage(prompt, hint, options, key=None):
    s = {"prompt": prompt, "hint": hint, "options": options}
    if key:
        s["key"] = key
    return s


QUESTIONS = []


def item(id, module, title, story, answer, stages, worked,
         verify=None, model=None, unit=None, check=None, explain=None):
    assert len(stages) == 3, f"{id}: need exactly 3 stages"
    for st in stages:
        assert len(st["options"]) == 3, f"{id}: each stage needs exactly 3 options"
        assert sum(1 for o in st["options"] if o["correct"]) == 1, \
            f"{id}: each stage needs exactly 1 correct option"
        for o in st["options"]:
            assert o["feedback"].strip(), f"{id}: empty feedback"
    assert "\\" not in answer and "{" not in answer, f"{id}: answer has latex chars"
    q = {
        "id": id, "module": module, "title": title, "story": story,
        "answer": answer, "stages": stages, "worked": worked,
    }
    if verify:
        q["verify"] = verify
    if model:
        q["model"] = model
    if unit:
        q["unit"] = unit
    if check:
        q["check"] = check
    if explain:
        q["explain"] = explain
    QUESTIONS.append(q)


# =============================================================================
# MODULE 1 — Name the whole (denominator = number of EQUAL parts)
# =============================================================================

M1 = dict(
    id=1, title="Name the whole",
    desc="Read a fraction as EQUAL parts of a named whole; the denominator counts the equal parts.",
    level="Core",
    rule="A fraction a/b means: cut the whole into b EQUAL parts, then take a of them.",
    teach=[
        "The denominator is the number of equal parts the whole is cut into.",
        "The numerator is how many of those equal parts we keep.",
        "If the parts are not equal, the picture does not show a fraction yet.",
    ],
    contrast=["Equal parts make a fraction", "Unequal parts do NOT make a fraction"],
    transfer="You will reuse 'name the whole' in every later module — percentages too.",
)


def _bare(name):
    """Drop a leading article so 'The complete ...' reads naturally."""
    low = name.strip()
    for art in ("A ", "An ", "The "):
        if low.startswith(art):
            return low[len(art):]
    return low


def m1_item(n, title, whole_name, total, shaded, part_word):
    bare = _bare(whole_name)
    f = F(shaded, total)
    ans = fs(f)
    item(
        id=f"m1-{n}", module=1, title=title,
        story=f"{whole_name} is cut into {total} equal parts. {shaded} of the parts are {part_word}. What fraction is {part_word}?",
        answer=ans,
        stages=[
            stage(
                "What is the WHOLE here (what equals 1)?",
                "The whole is the full thing before we cut it.",
                [
                    opt(f"The complete {bare} (all {total} parts together)", True,
                        f"Yes — the whole is the complete thing, all {total} equal parts together."),
                    opt(f"Just the {shaded} {part_word} parts", False,
                        "That is only the part we keep, not the whole. The whole is everything."),
                    opt(f"The number {shaded}, because it is said first", False,
                        "A count of parts is not the whole; the whole is the full shape."),
                ], key="whole",
            ),
            stage(
                "What number goes on the BOTTOM (the denominator)?",
                "The denominator counts the EQUAL parts the whole is cut into.",
                [
                    opt(f"{total} — the number of equal parts", True,
                        f"Right — the whole is in {total} equal parts, so the denominator is {total}."),
                    opt(f"{shaded} — the number we keep", False,
                        "That is the numerator, not the denominator. Bottom = total equal parts."),
                    opt(f"{total - shaded} — the parts left over", False,
                        "That counts the leftover parts, not the total parts the whole was cut into."),
                ], key="denominator",
            ),
            stage(
                "What number goes on TOP (the numerator)?",
                "The numerator is how many equal parts match the question.",
                [
                    opt(f"{shaded} — the {part_word} parts", True,
                        f"Yes — {shaded} parts are {part_word}, so the top number is {shaded}."),
                    opt(f"{total} — all the parts", False,
                        "All parts together make the whole (that would be {}/{}=1).".format(total, total)),
                    opt(f"{total - shaded} — the other parts", False,
                        f"Those are the parts that are NOT {part_word}. We want the {part_word} ones."),
                ], key="numerator",
            ),
        ],
        worked=[
            f"The whole is the complete {whole_name.lower()}, cut into {total} equal parts.",
            f"Denominator = {total} (equal parts).",
            f"Numerator = {shaded} ({part_word} parts).",
            f"So the fraction is {shaded}/{total} = {ans}.",
        ],
        verify={"op": "simplify", "args": [unreduced(shaded, total)]},
        model={"type": "parts", "total": total, "shaded": shaded,
               "label": f"{shaded} of {total} equal parts are {part_word}"},
        check=f"{part_word.capitalize()} parts + other parts = {shaded} + {total - shaded} = {total} (the whole).",
        explain="Why must the parts be EQUAL before the bottom number counts them?",
    )


m1_item(1, "A ribbon in equal parts", "A ribbon", 8, 3, "red")
m1_item(2, "Slices of a cake", "A cake", 6, 5, "eaten")
m1_item(3, "A chocolate bar", "A chocolate bar", 9, 4, "shared")
m1_item(4, "Beads on a string", "A string of beads", 12, 7, "blue")
m1_item(5, "A long wall", "A wall", 11, 6, "painted")
m1_item(6, "A garden strip", "A garden strip", 7, 2, "planted")
m1_item(7, "A number line jump", "A number line from 0 to 1", 16, 9, "coloured")
m1_item(8, "Parts of a pizza", "A pizza", 12, 5, "topped")


# =============================================================================
# MODULE 2 — Part & complement from a figure (part + complement = whole)
# =============================================================================

M2 = dict(
    id=2, title="Part and its complement",
    desc="From a figure, read shaded vs unshaded; a part and its complement add to the whole.",
    level="Core",
    rule="shaded/total + unshaded/total = total/total = 1.",
    teach=[
        "Count the shaded parts, then the unshaded parts — together they make the whole.",
        "If the question asks for UNSHADED, do not give the shaded count by mistake.",
        "The two fractions always add to 1.",
    ],
    contrast=["shaded = the filled parts", "unshaded (complement) = the empty parts"],
    transfer="This 'part + complement' idea becomes 'percent + its complement' later.",
)


def m2_item(n, title, context, total, shaded, ask):
    """ask = 'shaded' or 'unshaded'."""
    want_count = shaded if ask == "shaded" else total - shaded
    other_count = total - want_count
    f = F(want_count, total)
    ans = fs(f)
    item(
        id=f"m2-{n}", module=2, title=title,
        story=f"{context} is divided into {total} equal parts; {shaded} parts are shaded. Write the {ask.upper()} portion as a fraction.",
        answer=ans,
        stages=[
            stage(
                "How many parts make the WHOLE figure?",
                "Count every equal part, shaded and unshaded together.",
                [
                    opt(f"{total} parts", True,
                        f"Yes — all {total} equal parts together make the whole, so the denominator is {total}."),
                    opt(f"{shaded} parts", False,
                        "That counts only the shaded parts, not the whole figure."),
                    opt(f"{total - shaded} parts", False,
                        "That counts only the unshaded parts, not the whole figure."),
                ], key="whole",
            ),
            stage(
                f"How many parts are {ask.upper()}?",
                "Match the parts to what the question asks — shaded OR unshaded.",
                [
                    opt(f"{want_count} parts", True,
                        f"Right — {want_count} parts are {ask}."),
                    opt(f"{other_count} parts", False,
                        f"Careful — those are the {'unshaded' if ask == 'shaded' else 'shaded'} parts. "
                        f"The question asks for the {ask} ones."),
                    opt(f"{total} parts", False,
                        "All parts together are the whole, not just the part asked for."),
                ], key="part",
            ),
            stage(
                "Which fraction answers the question?",
                "Put the matching count on top and the total on the bottom.",
                [
                    opt(f"{want_count}/{total}", True,
                        f"Yes — {want_count} out of {total} equal parts is {want_count}/{total} = {ans}."),
                    opt(f"{other_count}/{total}", False,
                        f"That is the {'unshaded' if ask == 'shaded' else 'shaded'} share — the complement, not what was asked."),
                    opt(f"{total}/{want_count}", False,
                        "The bottom must be the total parts; this flips top and bottom."),
                ], key="fraction",
            ),
        ],
        worked=[
            f"Whole = {total} equal parts.",
            f"{ask.capitalize()} parts = {want_count}.",
            f"So the {ask} portion is {want_count}/{total} = {ans}.",
            f"Check: shaded {shaded}/{total} + unshaded {total - shaded}/{total} = {total}/{total} = 1.",
        ],
        verify={"op": "simplify", "args": [unreduced(want_count, total)]},
        model={"type": "parts", "total": total, "shaded": shaded,
               "label": f"{shaded} shaded, {total - shaded} unshaded (asked: {ask})"},
        check=f"{want_count}/{total} + {other_count}/{total} = {total}/{total} = 1.",
        explain="Why do a part and its complement always add up to exactly 1?",
    )


# mirrors the real seed item: 8 parts, 5 shaded, ASK unshaded -> 3/8
m2_item(1, "Reading the unshaded part", "A rectangle", 8, 5, "unshaded")
m2_item(2, "Reading the shaded part", "A strip", 8, 3, "shaded")
m2_item(3, "Unshaded of a grid", "A grid", 10, 7, "unshaded")
m2_item(4, "Shaded of a bar", "A bar", 9, 4, "shaded")
m2_item(5, "Unshaded of a circle", "A circle", 12, 5, "unshaded")
m2_item(6, "Shaded of a window", "A window pane", 16, 9, "shaded")
m2_item(7, "Unshaded of a flag", "A flag", 7, 2, "unshaded")
m2_item(8, "Shaded of a quilt", "A quilt", 11, 6, "shaded")


# =============================================================================
# MODULE 3 — Equivalent fractions (multiply/divide top & bottom by the SAME)
# =============================================================================

M3 = dict(
    id=3, title="Equivalent fractions",
    desc="Make equal fractions by multiplying or dividing numerator AND denominator by the same number.",
    level="Core",
    rule="a/b = (a x k)/(b x k): multiply BOTH by the same k (never add).",
    teach=[
        "Multiplying top and bottom by the same number keeps the value the same.",
        "You are really multiplying by k/k = 1.",
        "Adding the same number to top and bottom changes the value — that is the trap.",
    ],
    contrast=["x same number: value stays equal", "+ same number: value changes"],
    transfer="Equivalent fractions let you build common denominators later.",
)


def m3_item(n, title, a, b, k):
    nn, dd = a * k, b * k
    ans = unreduced(nn, dd)  # the equivalent (unreduced) fraction
    wrong_add = unreduced(a + k, b + k)  # the "added the same number" trap
    item(
        id=f"m3-{n}", module=3, title=title,
        story=f"Write a fraction equal to {a}/{b} that has {dd} on the bottom.",
        answer=ans,
        stages=[
            stage(
                f"To turn the bottom {b} into {dd}, what do you do?",
                f"Find the number that {b} is multiplied by to reach {dd}.",
                [
                    opt(f"Multiply by {k} (since {b} x {k} = {dd})", True,
                        f"Yes — {b} x {k} = {dd}, so the multiplier is {k}."),
                    opt(f"Add {dd - b} (since {b} + {dd - b} = {dd})", False,
                        "Adding changes the value. Equivalent fractions come from MULTIPLYING."),
                    opt(f"Multiply by {dd} ", False,
                        f"That would make the bottom {b * dd}, far too big. Use the factor {k}."),
                ], key="factor",
            ),
            stage(
                "What must you do to the TOP to keep the fraction equal?",
                "Whatever you do to the bottom, do the SAME to the top.",
                [
                    opt(f"Multiply the top by {k} too", True,
                        f"Right — multiply top and bottom by the same {k}; that is multiplying by {k}/{k} = 1."),
                    opt(f"Leave the top as {a}", False,
                        "Changing only the bottom changes the value — the fraction would no longer be equal."),
                    opt(f"Add {k} to the top", False,
                        "Mixing 'multiply bottom, add top' breaks the equality. Multiply BOTH."),
                ], key="same",
            ),
            stage(
                "Which fraction is equal to the original?",
                f"Compute {a} x {k} over {b} x {k}.",
                [
                    opt(ans, True,
                        f"Yes — {a} x {k} = {nn} and {b} x {k} = {dd}, giving {ans}."),
                    opt(wrong_add, False,
                        f"This came from ADDING {k} to each — {wrong_add} is not equal to {a}/{b}."),
                    opt(unreduced(nn, b), False,
                        "Only the top was multiplied here; the bottom must change too."),
                ], key="result",
            ),
        ],
        worked=[
            f"{b} x {k} = {dd}, so the multiplier is {k}.",
            f"Multiply the top by the same {k}: {a} x {k} = {nn}.",
            f"So {a}/{b} = {nn}/{dd}.",
        ],
        verify={"op": "equiv", "args": [fs(F(a, b)) if F(a, b).denominator != 1 else unreduced(a, b), k]},
        model={"type": "mapping", "rows": [[f"{a}/{b}", "original"], [ans, f"x {k} top & bottom"]]},
        check=f"{nn}/{dd} divided by {k}/{k} returns {a}/{b}.",
        explain="Why does multiplying top and bottom by the same number not change the value?",
    )


m3_item(1, "Build to twelfths", 3, 4, 3)
m3_item(2, "Build to tenths", 2, 5, 2)
m3_item(3, "Build to sixteenths", 3, 8, 2)
m3_item(4, "Build to twenty-firsts", 2, 7, 3)
m3_item(5, "Build to twenty-fourths", 5, 6, 4)
m3_item(6, "Build to thirty-thirds", 3, 11, 3)
m3_item(7, "Build to forty-fifths", 4, 9, 5)
m3_item(8, "Build to forty-eighths", 7, 12, 4)


# =============================================================================
# MODULE 4 — Lowest terms via GCD (divide top & bottom by their GCD)
# =============================================================================

M4 = dict(
    id=4, title="Lowest terms",
    desc="Reduce a fraction fully by dividing numerator and denominator by their greatest common divisor.",
    level="Core",
    rule="Divide top and bottom by their GCD once to reach lowest terms.",
    teach=[
        "The GCD is the biggest number that divides BOTH top and bottom.",
        "Divide both by the GCD in one clean step to reach lowest terms.",
        "Do not flip the fraction or stop after a partial reduction.",
    ],
    contrast=["Full reduction uses the GCD", "Partial reduction leaves a common factor behind"],
    transfer="Lowest-terms answers are the standard form your mock tests expect.",
)


def m4_item(n, title, a, b):
    g = gcd(a, b)
    ra, rb = a // g, b // g
    ans = fs(F(a, b))
    recip = unreduced(rb, ra) if ra != 0 else "0"
    item(
        id=f"m4-{n}", module=4, title=title,
        story=f"Write {a}/{b} in its lowest form.",
        answer=ans,
        stages=[
            stage(
                f"What is the greatest number that divides BOTH {a} and {b}?",
                "Look for the biggest shared factor (the GCD).",
                [
                    opt(f"{g}", True,
                        f"Yes — {g} divides both: {a} ÷ {g} = {ra} and {b} ÷ {g} = {rb}."),
                    opt(f"{max(2, g // 2 if g > 1 else 2)}", False,
                        "That divides both, but it is not the GREATEST — you would reduce only part way."),
                    opt("1", False,
                        "1 always divides, but these numbers share a bigger factor, so use the GCD."),
                ], key="gcd",
            ),
            stage(
                f"Divide BOTH numbers by {g}. What do you get?",
                "Divide the top and the bottom by the same GCD.",
                [
                    opt(f"{ra}/{rb}", True,
                        f"Right — {a} ÷ {g} = {ra} and {b} ÷ {g} = {rb}."),
                    opt(recip, False,
                        "This flipped the fraction upside down — that is a reciprocal, not a reduction."),
                    opt(f"{ra}/{b}", False,
                        "Only the top was divided; divide the bottom by the SAME GCD too."),
                ], key="divide",
            ),
            stage(
                "Is the result already in lowest terms?",
                "Check whether the new top and bottom still share a factor.",
                [
                    opt(f"Yes — {ans} cannot be reduced further", True,
                        f"Correct — {ra} and {rb} share only 1, so {ans} is fully reduced."),
                    opt("No — keep halving a few more times", False,
                        f"After dividing by the GCD {g} once, nothing more divides both numbers."),
                    opt("Flip it to be safe", False,
                        "Flipping changes the value; lowest terms keeps the same value."),
                ], key="check",
            ),
        ],
        worked=[
            f"GCD of {a} and {b} is {g}.",
            f"{a} ÷ {g} = {ra}; {b} ÷ {g} = {rb}.",
            f"So {a}/{b} = {ans} in lowest terms.",
        ],
        verify={"op": "simplify", "args": [unreduced(a, b)]},
        model={"type": "mapping", "rows": [[f"{a}/{b}", "start"], [f"÷ {g} ÷ {g}", "both"], [ans, "lowest terms"]]},
        check=f"{ra} and {rb} have no common factor except 1.",
        explain="Why does dividing by the GCD (and not a smaller factor) finish the job in one step?",
    )


# includes the real seed trap 187/136 -> 11/8
m4_item(1, "Halve and halve again", 12, 16)
m4_item(2, "A tidy third", 15, 45)
m4_item(3, "Share a factor", 18, 24)
m4_item(4, "The famous 187/136", 187, 136)
m4_item(5, "Reduce by nine", 27, 36)
m4_item(6, "Reduce by seven", 35, 56)
m4_item(7, "Reduce by eleven", 44, 99)
m4_item(8, "A bigger reduce", 84, 120)


# =============================================================================
# MODULE 5 — Compare fractions (common denominator / cross-multiply)
# =============================================================================

M5 = dict(
    id=5, title="Compare fractions",
    desc="Decide which fraction is greater using a common denominator or cross-multiplying.",
    level="Core",
    rule="Compare a/b and c/d by comparing a x d with c x b (cross products).",
    teach=[
        "A bigger bottom number does NOT mean a bigger fraction.",
        "Give both fractions the same denominator, then compare the tops.",
        "Or cross-multiply: a x d versus c x b.",
    ],
    contrast=["Same bottom: compare tops", "Different bottoms: cross-multiply"],
    transfer="Comparing by common denominator leads straight into adding unlike fractions.",
)


def m5_item(n, title, a, b, c, d):
    """Which of a/b, c/d is greater?"""
    f1, f2 = F(a, b), F(c, d)
    larger = f1 if f1 > f2 else f2
    ans = fs(larger)
    cross1, cross2 = a * d, c * b  # a/b vs c/d
    item(
        id=f"m5-{n}", module=5, title=title,
        story=f"Which is greater, {a}/{b} or {c}/{d}?",
        answer=ans,
        stages=[
            stage(
                "Can we compare the bottom numbers directly?",
                "A larger denominator means smaller pieces, not a larger fraction.",
                [
                    opt("No — a bigger bottom does not mean a bigger fraction", True,
                        "Right — with more pieces each piece is smaller, so the bottom alone cannot decide."),
                    opt(f"Yes — {b if b > d else d} is bigger, so that fraction wins", False,
                        "That is the classic trap: a bigger denominator makes each part SMALLER."),
                    opt("Yes — just compare the tops and ignore the bottoms", False,
                        "Tops alone only work when the bottoms already match."),
                ], key="trap",
            ),
            stage(
                "Cross-multiply. Compare which two products?",
                f"For {a}/{b} vs {c}/{d}, use {a} x {d} and {c} x {b}.",
                [
                    opt(f"{a} x {d} = {cross1} and {c} x {b} = {cross2}", True,
                        f"Yes — {cross1} vs {cross2} tells us which fraction is greater."),
                    opt(f"{a} x {c} and {b} x {d}", False,
                        "Cross-multiplying pairs each TOP with the OTHER bottom, not top-with-top."),
                    opt(f"{a} + {d} and {c} + {b}", False,
                        "Comparison uses products across, not sums."),
                ], key="cross",
            ),
            stage(
                "So which fraction is greater?",
                "The fraction above the larger cross product is greater.",
                [
                    opt(ans, True,
                        f"Yes — since {cross1} {'>' if cross1 > cross2 else '<'} {cross2}, {ans} is greater."),
                    opt(fs(f2 if larger == f1 else f1), False,
                        "That matches the smaller cross product, so it is the smaller fraction."),
                    opt("They are equal", False,
                        f"The cross products {cross1} and {cross2} differ, so the fractions are not equal."),
                ], key="decide",
            ),
        ],
        worked=[
            f"Cross-multiply: {a} x {d} = {cross1}, and {c} x {b} = {cross2}.",
            f"Since {cross1} {'>' if cross1 > cross2 else '<'} {cross2}, the greater fraction is {ans}.",
        ],
        verify={"op": "larger", "args": [fs(f1), fs(f2)]},
        model={"type": "mapping", "rows": [[f"{a}/{b}", f"cross {cross1}"], [f"{c}/{d}", f"cross {cross2}"], [ans, "greater"]]},
        check=f"As decimals: {dec(f1)} vs {dec(f2)} — the larger confirms {ans}.",
        explain="Why does cross-multiplying give the same answer as a common denominator?",
    )


m5_item(1, "Thirds versus fifths", 3, 5, 2, 3)
m5_item(2, "Don't trust the big bottom", 3, 4, 7, 9)
m5_item(3, "Close call", 5, 8, 7, 12)
m5_item(4, "Sevenths and ninths", 5, 7, 6, 9)
m5_item(5, "Elevenths in play", 7, 11, 9, 16)
m5_item(6, "Near one-half", 5, 9, 6, 11)
m5_item(7, "Twelfths duel", 7, 12, 9, 16)
m5_item(8, "Bigger than one", 9, 8, 11, 12)


# =============================================================================
# MODULE 6 — Add / subtract LIKE fractions (same denominator)
# =============================================================================

M6 = dict(
    id=6, title="Add and subtract like fractions",
    desc="Add or subtract fractions with the SAME denominator by working only on the numerators.",
    level="Core",
    rule="a/d ± b/d = (a ± b)/d — keep the denominator, combine the tops.",
    teach=[
        "Same-size pieces add by counting: 3 eighths + 2 eighths = 5 eighths.",
        "The denominator stays the same — you are not making new piece sizes.",
        "Adding the denominators is the trap; the piece size does not change.",
    ],
    contrast=["Combine the TOPS", "Keep the SAME bottom"],
    transfer="Once bottoms match, adding is easy — that is why unlike fractions get a common bottom first.",
)


def m6_item(n, title, a, b, d, op):
    """op '+' or '-' on a/d, b/d."""
    if op == "+":
        res = F(a + b, d)
        topword = f"{a} + {b} = {a + b}"
        verify = {"op": "add", "args": [unreduced(a, d), unreduced(b, d)]}
    else:
        res = F(a - b, d)
        topword = f"{a} - {b} = {a - b}"
        verify = {"op": "sub", "args": [unreduced(a, d), unreduced(b, d)]}
    ans = fs(res)
    topnum = a + b if op == "+" else a - b
    raw = unreduced(topnum, d)
    # Distractors guaranteed distinct from `ans` (map_step strips whitespace, so
    # trailing-space differentiation does NOT work — the text itself must differ).
    bottom_trap = f"{topnum}/{d + d}"  # "added the bottoms too" — denom d+d never equals d
    if raw != ans:
        reduce_trap = raw            # unreduced form (only exists when it reduces)
        reduce_fb = "This left it unreduced; always give the lowest-terms answer when it reduces."
    else:
        reduce_trap = f"{a}/{d}"     # "kept only the first fraction" — never equals the combined ans
        reduce_fb = "That is only the first fraction — you must combine both tops over the shared bottom."
    item(
        id=f"m6-{n}", module=6, title=title,
        story=f"Work out {a}/{d} {op} {b}/{d}.",
        answer=ans,
        stages=[
            stage(
                "The bottoms are the same. What stays the same in the answer?",
                "Same-size pieces keep their size.",
                [
                    opt(f"The denominator stays {d}", True,
                        f"Right — the pieces are already {d}ths, so the bottom stays {d}."),
                    opt(f"The bottom becomes {d + d}", False,
                        "Adding the bottoms is the trap — the piece size does not change when bottoms match."),
                    opt(f"The bottom becomes {d * d}", False,
                        "Multiplying the bottoms is not needed when they are already equal."),
                ], key="bottom",
            ),
            stage(
                f"What do you do with the tops ({a} and {b})?",
                f"{'Add' if op == '+' else 'Subtract'} the numerators.",
                [
                    opt(f"{topword}", True,
                        f"Yes — {'add' if op == '+' else 'subtract'} the tops: {topword}."),
                    opt(f"{a} x {b} = {a * b}", False,
                        "Multiplying the tops is not what adding/subtracting asks for."),
                    opt(f"keep {a} and drop {b}", False,
                        "Both pieces count; you must combine the two tops."),
                ], key="top",
            ),
            stage(
                "Put it together (and reduce if you can). The answer is:",
                "Top result over the shared bottom, then simplify.",
                [
                    opt(ans, True,
                        f"Yes — {raw}{' = ' + ans if raw != ans else ''}."),
                    opt(bottom_trap, False,
                        "That changed the bottom — keep the shared denominator, only the top changes."),
                    opt(reduce_trap, False, reduce_fb),
                ], key="combine",
            ),
        ],
        worked=[
            f"Bottoms already match at {d}.",
            f"Combine the tops: {topword}.",
            f"So {a}/{d} {op} {b}/{d} = {raw}" + (f" = {ans}." if raw != ans else "."),
        ],
        verify=verify,
        model={"type": "parts", "total": d, "shaded": min(a, d) if op == "-" else min(a + b, d),
               "label": f"{a} {op} {b} over {d}"},
        check=f"{raw} as a value is {dec(res)}.",
        explain="Why does the denominator stay the same when the pieces are already equal size?",
    )


m6_item(1, "Add eighths", 3, 2, 8, "+")
m6_item(2, "Add ninths", 4, 2, 9, "+")
m6_item(3, "Subtract sevenths", 6, 2, 7, "-")
m6_item(4, "Add twelfths", 5, 7, 12, "+")
m6_item(5, "Subtract elevenths", 9, 4, 11, "-")
m6_item(6, "Add to more than one", 7, 6, 8, "+")
m6_item(7, "Subtract sixteenths", 11, 3, 16, "-")
m6_item(8, "Add fifteenths", 7, 8, 15, "+")


# =============================================================================
# MODULE 7 — Add / subtract UNLIKE fractions (LCD first)
# =============================================================================

M7 = dict(
    id=7, title="Add and subtract unlike fractions",
    desc="Give unlike fractions a common denominator (the LCM), then combine the numerators.",
    level="Core",
    rule="Rewrite both over the LCM of the bottoms, then add/subtract the tops.",
    teach=[
        "Different-size pieces cannot be counted together until they match.",
        "Use the LCM of the bottoms as the common denominator.",
        "Adding across without a common bottom (top+top over bottom+bottom) is the trap.",
    ],
    contrast=["Common denominator first", "Never add across unlike bottoms"],
    transfer="This is the heart of fraction arithmetic in equations and word problems.",
)


def lcm(x, y):
    return x * y // gcd(x, y)


def m7_item(n, title, a, b, c, d, op):
    """op '+' or '-' on a/b, c/d (unlike)."""
    L = lcm(b, d)
    ka, kc = L // b, L // d
    na, nc = a * ka, c * kc
    if op == "+":
        res = F(na + nc, L)
        combined = f"{na} + {nc} = {na + nc}"
        verify = {"op": "add", "args": [unreduced(a, b), unreduced(c, d)]}
    else:
        res = F(na - nc, L)
        combined = f"{na} - {nc} = {na - nc}"
        verify = {"op": "sub", "args": [unreduced(a, b), unreduced(c, d)]}
    ans = fs(res)
    raw = unreduced(na + nc if op == "+" else na - nc, L)
    trap = unreduced(a + c if op == "+" else a - c, b + d)  # add-across trap
    # Unreduced distractor must differ from `ans` in TEXT (map_step strips spaces),
    # so when the result does not reduce we swap in a distinct misconception.
    if raw != ans:
        unred_trap = raw
        unred_fb = "That is the right value but left unreduced; give the lowest-terms form."
    else:
        unred_trap = f"{na}/{L}"
        unred_fb = "That is only the first fraction's new top — add the second new top as well."
    item(
        id=f"m7-{n}", module=7, title=title,
        story=f"Work out {a}/{b} {op} {c}/{d}.",
        answer=ans,
        stages=[
            stage(
                f"The bottoms {b} and {d} differ. What common denominator do you use?",
                f"Use the LCM of {b} and {d}.",
                [
                    opt(f"{L} (the LCM of {b} and {d})", True,
                        f"Right — {L} is the smallest number both {b} and {d} divide into."),
                    opt(f"{b + d}", False,
                        "Adding the bottoms does not give a common denominator; use the LCM."),
                    opt(f"{b * d if b * d != L else b * d + 1}", False,
                        f"{b}x{d} is a common denominator but not the smallest — the LCM {L} is tidier."
                        if b * d != L else "That is one more than the LCM — use the exact LCM."),
                ], key="lcd",
            ),
            stage(
                f"Rewrite both fractions over {L}. Which pair is right?",
                f"Multiply {a}/{b} by {ka}/{ka} and {c}/{d} by {kc}/{kc}.",
                [
                    opt(f"{na}/{L} and {nc}/{L}", True,
                        f"Yes — {a}/{b} = {na}/{L} and {c}/{d} = {nc}/{L}."),
                    opt(f"{a}/{L} and {c}/{L}", False,
                        "Only the bottoms were changed; the tops must be scaled by the same factor."),
                    opt(f"{na}/{L} and {c}/{L}", False,
                        "The second top was not scaled — multiply its top by its own factor too."),
                ], key="rewrite",
            ),
            stage(
                "Now combine the tops over the common bottom. The answer is:",
                f"{'Add' if op == '+' else 'Subtract'} the new tops over {L}, then reduce.",
                [
                    opt(ans, True,
                        f"Yes — {combined}, giving {raw}" + (f" = {ans}." if raw != ans else ".")),
                    opt(trap, False,
                        "This added across (top+top over bottom+bottom) — unlike fractions need a common bottom first."),
                    opt(unred_trap, False, unred_fb),
                ], key="combine",
            ),
        ],
        worked=[
            f"LCM of {b} and {d} is {L}.",
            f"{a}/{b} = {na}/{L} and {c}/{d} = {nc}/{L}.",
            f"Combine tops: {combined} over {L} = {raw}" + (f" = {ans}." if raw != ans else "."),
        ],
        verify=verify,
        model={"type": "mapping", "rows": [[f"{a}/{b}", f"{na}/{L}"], [f"{c}/{d}", f"{nc}/{L}"], [ans, "answer"]]},
        check=f"As a value: {dec(res)}.",
        explain="Why must the pieces be the same size (common denominator) before we can combine the tops?",
    )


# first mirrors the classic 1/4 + 2/3
m7_item(1, "Quarters and thirds", 1, 4, 2, 3, "+")
m7_item(2, "Halves and fifths", 1, 2, 2, 5, "+")
m7_item(3, "Thirds minus quarters", 2, 3, 1, 4, "-")
m7_item(4, "Sixths and eighths", 5, 6, 3, 8, "+")
m7_item(5, "Fifths minus sixths", 4, 5, 2, 6, "-")
m7_item(6, "Ninths and sixths", 2, 9, 1, 6, "+")
m7_item(7, "Twelfths and eighths", 7, 12, 1, 8, "-")
m7_item(8, "Sevenths and halves", 3, 7, 1, 2, "+")


# =============================================================================
# MODULE 8 — Mixed <-> improper (whole x denom + num)
# =============================================================================

M8 = dict(
    id=8, title="Mixed and improper fractions",
    desc="Convert between a mixed number and an improper fraction using whole x denominator + numerator.",
    level="Core",
    rule="w n/d = (w x d + n)/d; reverse by dividing to get whole and remainder.",
    teach=[
        "To go to improper: multiply the whole by the denominator, then add the numerator.",
        "To go to mixed: divide the top by the bottom — quotient is the whole, remainder is the new top.",
        "Adding the whole straight onto the numerator is the trap.",
    ],
    contrast=["whole x denom + num = new top", "Keep the SAME denom"],
    transfer="Improper form makes multiplying and dividing mixed numbers simple.",
)


def m8_item(n, title, w, a, d):
    """Mixed w a/d -> improper."""
    top = w * d + a
    ans = unreduced(top, d)
    trap = unreduced(w + a, d)  # added whole to numerator
    item(
        id=f"m8-{n}", module=8, title=title,
        story=f"Write the mixed number {w} {a}/{d} as an improper fraction.",
        answer=ans,
        stages=[
            stage(
                f"First, how many {d}ths are in the whole number {w}?",
                f"Each whole is {d} of the {d}ths.",
                [
                    opt(f"{w} x {d} = {w * d}", True,
                        f"Right — {w} wholes is {w} x {d} = {w * d} of the {d}ths."),
                    opt(f"{w} + {d} = {w + d}", False,
                        "Each whole holds {}ths, so we MULTIPLY by {}, not add.".format(d, d)),
                    opt(f"{w}", False,
                        "That counts wholes, not {}ths. Turn each whole into {} pieces first.".format(d, d)),
                ], key="wholes",
            ),
            stage(
                f"Now add the numerator {a}. What is the new top?",
                f"Add the {a} leftover {d}ths to the {w * d}.",
                [
                    opt(f"{w * d} + {a} = {top}", True,
                        f"Yes — {w * d} + {a} = {top} {d}ths."),
                    opt(f"{w} + {a} = {w + a}", False,
                        "That adds the whole straight onto the numerator — the trap. Convert the whole first."),
                    opt(f"{w * d} x {a} = {w * d * a}", False,
                        "We add the leftover pieces, we do not multiply them in."),
                ], key="add",
            ),
            stage(
                "What is the denominator of the improper fraction?",
                "The piece size does not change.",
                [
                    opt(f"Still {d}", True,
                        f"Right — the pieces are still {d}ths, so {w} {a}/{d} = {ans}."),
                    opt(f"{w * d}", False,
                        "The bottom stays the piece size {}; it does not become the big count.".format(d)),
                    opt(f"{d + a}", False,
                        "The denominator is unchanged by the numerator; it stays {}.".format(d)),
                ], key="denom",
            ),
        ],
        worked=[
            f"{w} x {d} = {w * d}.",
            f"{w * d} + {a} = {top}.",
            f"Keep the bottom {d}: {w} {a}/{d} = {ans}.",
        ],
        verify={"op": "to_improper", "args": [f"{w} {a}/{d}"]},
        model={"type": "parts", "total": d, "shaded": a,
               "label": f"{w} wholes ({w}x{d}) + {a} extra = {top} {d}ths"},
        check=f"{ans} divided back: {top} ÷ {d} = {w} remainder {a}, i.e. {w} {a}/{d}.",
        explain="Why do we multiply the whole by the denominator before adding the numerator?",
    )


def m8_mixed_item(n, title, top, d):
    """Improper top/d -> mixed."""
    w = top // d
    rem = top - w * d
    ans = f"{w} {rem}/{d}"
    trap = f"{d} {rem}/{w}" if w != 0 else f"{rem}/{d}"
    item(
        id=f"m8-{n}", module=8, title=title,
        story=f"Write the improper fraction {top}/{d} as a mixed number.",
        answer=ans,
        stages=[
            stage(
                f"How many whole groups of {d} are in {top}?",
                f"Divide {top} by {d}; the quotient is the whole number.",
                [
                    opt(f"{top} ÷ {d} = {w} (remainder {rem})", True,
                        f"Right — {d} goes into {top} exactly {w} times with {rem} left over."),
                    opt(f"{top} ÷ {d} = {w + 1}", False,
                        f"{d} x {w + 1} = {d * (w + 1)}, which is more than {top}; the whole part is {w}."),
                    opt(f"{top} - {d} = {top - d}", False,
                        "Subtracting once only removes a single group; divide to count all the groups."),
                ], key="whole",
            ),
            stage(
                "What is the remainder (the leftover pieces)?",
                f"Leftover = {top} - {w} x {d}.",
                [
                    opt(f"{rem}", True,
                        f"Yes — {top} - {w} x {d} = {rem} leftover {d}ths."),
                    opt(f"{d - rem}", False,
                        "That counts the pieces still needed to reach the next whole, not the leftover."),
                    opt("0", False,
                        f"{top} is not an exact multiple of {d}; there are {rem} pieces left over."),
                ], key="rem",
            ),
            stage(
                "Put the mixed number together:",
                "Whole number, then remainder over the SAME denominator.",
                [
                    opt(ans, True,
                        f"Yes — {w} wholes and {rem}/{d} left over is {ans}."),
                    opt(trap, False,
                        "The whole and the bottom got swapped — keep the denominator {} on the bottom.".format(d)),
                    opt(f"{w} {rem}/{top}", False,
                        "The leftover stays over the piece size {}, not over the big top.".format(d)),
                ], key="build",
            ),
        ],
        worked=[
            f"{top} ÷ {d} = {w} remainder {rem}.",
            f"Whole = {w}; leftover = {rem}/{d}.",
            f"So {top}/{d} = {ans}.",
        ],
        verify={"op": "to_mixed", "args": [unreduced(top, d)]},
        model={"type": "parts", "total": d, "shaded": rem,
               "label": f"{w} full groups of {d} + {rem} leftover"},
        check=f"{w} x {d} + {rem} = {top}, back to {top}/{d}.",
        explain="Why does the remainder become the new numerator over the same denominator?",
    )


# mirrors the real seed: numerator 21, denominator 16 less -> 21/5 -> 4 1/5
m8_item(1, "Into fifths", 4, 1, 5)
m8_item(2, "Into quarters", 3, 3, 4)
m8_item(3, "Into eighths", 2, 5, 8)
m8_item(4, "Into sevenths", 5, 2, 7)
m8_mixed_item(5, "Back to a mixed number", 21, 5)
m8_mixed_item(6, "Twelfths to mixed", 29, 12)
m8_mixed_item(7, "Ninths to mixed", 47, 9)
m8_mixed_item(8, "Elevenths to mixed", 50, 11)


# =============================================================================
# MODULE 9 — Fraction OF a quantity ("of" = x)
# =============================================================================

M9 = dict(
    id=9, title="A fraction of a quantity",
    desc="Find a fraction OF a number: divide by the denominator, then multiply by the numerator.",
    level="Core",
    rule="a/b of N = (N ÷ b) x a — share into b, take a shares.",
    teach=[
        "'of' means multiply: a/b of N = a/b x N.",
        "Divide N by the denominator to find one share, then take 'numerator' shares.",
        "Dividing by the numerator only (ignoring the denominator) is the trap.",
    ],
    contrast=["÷ by denominator = one share", "x by numerator = how many shares"],
    transfer="Fraction-of-a-quantity is exactly how percentages of amounts work.",
)


def m9_item(n, title, a, b, N, noun, story=None):
    assert N % b == 0, f"m9-{n}: {N} not divisible by {b}"
    share = N // b
    res = share * a  # == Fraction(a,b)*N as integer
    assert Fraction(a, b) * N == res
    ans = str(res)
    trap = str(N // a) if N % a == 0 else fs(F(N, a))  # divided by numerator only
    if story is None:
        story = f"There are {N} {noun} in all. {a}/{b} of them are special. How many are special?"
    item(
        id=f"m9-{n}", module=9, title=title,
        story=story,
        answer=ans,
        stages=[
            stage(
                f"To find {a}/{b} of {N}, what is ONE share (one {b}th)?",
                f"Divide {N} into {b} equal shares.",
                [
                    opt(f"{N} ÷ {b} = {share}", True,
                        f"Right — one {b}th of {N} is {N} ÷ {b} = {share}."),
                    opt(f"{N} ÷ {a} = {N // a if N % a == 0 else round(N / a, 2)}", False,
                        "That divided by the NUMERATOR; one share comes from dividing by the denominator."),
                    opt(f"{N} - {b} = {N - b}", False,
                        "Finding a share is division into equal parts, not subtraction."),
                ], key="share",
            ),
            stage(
                f"How many of those shares do we take?",
                f"Take the numerator, {a}, of the shares.",
                [
                    opt(f"{a} shares", True,
                        f"Yes — the numerator {a} tells how many {b}ths to take."),
                    opt(f"{b} shares", False,
                        f"Taking all {b} shares would give back the whole {N}; take just {a}."),
                    opt(f"1 share", False,
                        f"One share is only {share}; the numerator {a} says take {a} of them."),
                ], key="count",
            ),
            stage(
                "So how many are in the asked part?",
                f"Multiply one share by {a}.",
                [
                    opt(ans, True,
                        f"Yes — {share} x {a} = {res} {noun}."),
                    opt(trap, False,
                        "This used the share from dividing by the numerator, so it misses the real count."),
                    opt(str(N), False,
                        f"That is ALL the {noun}; only {a}/{b} of them are asked for."),
                ], key="answer",
            ),
        ],
        worked=[
            f"One {b}th of {N} is {N} ÷ {b} = {share}.",
            f"Take {a} shares: {share} x {a} = {res}.",
            f"So {a}/{b} of {N} = {res}.",
        ],
        verify={"op": "of", "args": [fs(F(a, b)), str(N)]},
        model={"type": "groups",
               "caps": [share] * b,
               "labels": [("take" if i < a else "leave") for i in range(b)],
               "target": str(res),
               "capLabel": f"{b} shares of {share}; take {a}"},
        unit=noun,
        check=f"Asked part {res} + rest {N - res} = {N} {noun} in all.",
        explain="Why does 'of' mean multiply, and why divide by the denominator first?",
    )


# contexts echo the seed (money, students, marbles ...)
m9_item(1, "Three-quarters of a bag", 3, 4, 40, "marbles",
        story="A bag has 40 marbles. 3/4 of them are blue. How many marbles are blue?")
m9_item(2, "Two-fifths of the class", 2, 5, 45, "students",
        story="A class has 45 students. 2/5 of them joined the art club. How many students joined?")
m9_item(3, "Five-sixths of the beads", 5, 6, 54, "beads",
        story="A box has 54 beads. 5/6 of them are round. How many beads are round?")
m9_item(4, "Four-ninths of the plants", 4, 9, 63, "plants",
        story="A nursery has 63 plants. 4/9 of them are flowering. How many are flowering?")
m9_item(5, "Seven-twelfths of the tiles", 7, 12, 60, "tiles",
        story="A floor uses 60 tiles. 7/12 of them are white. How many tiles are white?")
m9_item(6, "Three-sevenths of the books", 3, 7, 49, "books",
        story="A shelf holds 49 books. 3/7 of them are story books. How many are story books?")
m9_item(7, "Five-elevenths of the stamps", 5, 11, 66, "stamps",
        story="An album has 66 stamps. 5/11 of them are foreign. How many stamps are foreign?")
m9_item(8, "Nine-sixteenths of the cards", 9, 16, 80, "cards",
        story="A pack has 80 cards. 9/16 of them are number cards. How many are number cards?")


# =============================================================================
# MODULE 10 — Equations & word problems (Stretch)
# =============================================================================

M10 = dict(
    id=10, title="Fraction equations and word problems",
    desc="Solve missing-number fraction equations and word problems by working back from the whole.",
    level="Stretch",
    rule="Name the whole, write the fraction relationship, then solve for the unknown.",
    teach=[
        "In 'remaining = whole - known fractions', the leftover count pins down the whole.",
        "For like-fraction equations, scale the single term up to the target.",
        "For numerator-defined-by-denominator problems, build the numerator from the rule first.",
    ],
    contrast=["Find the WHOLE from the leftover", "Then take the asked fraction of it"],
    transfer="This is the reasoning IPM word problems reward most.",
)


# ---- m10-1: library / lab / playground word problem (seed B7_032) ----
def m10_library():
    # 3/7 library, 2/7 lab, remaining 14 = 2/7 -> whole 49; library = 3/7*49 = 21
    whole = 49
    lib = Fraction(3, 7) * whole
    assert lib == 21
    item(
        id="m10-1", module=10, title="Library, lab, playground",
        story="In a class, 3/7 of the students went to the library and 2/7 went to the science lab. The remaining 14 students went to the playground. How many went to the library?",
        answer=str(int(lib)),
        stages=[
            stage(
                "What fraction of the class went to the playground?",
                "The three groups together make the whole (7/7).",
                [
                    opt("2/7 (since 7/7 - 3/7 - 2/7 = 2/7)", True,
                        "Right — 3/7 + 2/7 = 5/7 left, so 2/7 remain for the playground."),
                    opt("5/7", False,
                        "5/7 is the part that went to library and lab TOGETHER, not the remainder."),
                    opt("1/7", False,
                        "Subtract both known fractions from 7/7: 7/7 - 3/7 - 2/7 = 2/7, not 1/7."),
                ], key="remainder",
            ),
            stage(
                "14 students are 2/7 of the class. What is the WHOLE class?",
                "If 2/7 is 14, one 7th is 14 ÷ 2.",
                [
                    opt("49 students (14 ÷ 2 x 7)", True,
                        "Yes — one 7th is 14 ÷ 2 = 7, so the whole is 7 x 7 = 49."),
                    opt("28 students (14 x 2)", False,
                        "That doubled the remainder; instead find one 7th first, then scale to 7 sevenths."),
                    opt("98 students (14 x 7)", False,
                        "14 is TWO sevenths, not one, so multiply one 7th (which is 7) by 7, giving 49."),
                ], key="whole",
            ),
            stage(
                "How many went to the library (3/7 of 49)?",
                "One 7th is 7; take 3 of them.",
                [
                    opt("21 students (3 x 7)", True,
                        "Yes — 3/7 of 49 is 3 x 7 = 21 students."),
                    opt("14 students", False,
                        "14 is the playground group (2/7), not the library group (3/7)."),
                    opt("7 students", False,
                        "7 is just one 7th; the library share is 3 sevenths, so 3 x 7 = 21."),
                ], key="library",
            ),
        ],
        worked=[
            "Playground = 7/7 - 3/7 - 2/7 = 2/7.",
            "2/7 of the class = 14, so one 7th = 7 and the whole = 49.",
            "Library = 3/7 of 49 = 3 x 7 = 21 students.",
        ],
        verify={"op": "of", "args": ["3/7", "49"]},
        model={"type": "groups",
               "caps": [7, 7, 7, 7, 7, 7, 7],
               "labels": ["lib", "lib", "lib", "lab", "lab", "play", "play"],
               "target": "21",
               "capLabel": "7 sevenths of 7; library takes 3"},
        unit="students",
        check="21 library + 14 lab + 14 playground = 49 students.",
        explain="Why does the leftover count tell us the size of the whole class?",
    )


m10_library()


# ---- m10-2: water tank (seed B7_030) 4/7 full, 120 L fills it -> total 280 ----
def m10_tank():
    # remaining to fill = 3/7 = 120 -> one 7th = 40 -> total = 280
    total = 280
    assert Fraction(3, 7) * total == 120
    item(
        id="m10-2", module=10, title="Filling the water tank",
        story="A water tank is 4/7 full. It needs 120 litres more to fill completely. What is the total capacity of the tank?",
        answer=str(total),
        stages=[
            stage(
                "What fraction of the tank is still EMPTY?",
                "Full is 7/7; subtract the part already filled.",
                [
                    opt("3/7 (since 7/7 - 4/7 = 3/7)", True,
                        "Right — 4/7 is full, so 3/7 is still empty."),
                    opt("4/7", False,
                        "4/7 is the FILLED part; the empty part is what the 120 litres will fill."),
                    opt("1/7", False,
                        "7/7 - 4/7 = 3/7, not 1/7."),
                ], key="empty",
            ),
            stage(
                "120 litres fill the empty 3/7. How big is one 7th?",
                "One 7th = 120 ÷ 3.",
                [
                    opt("40 litres (120 ÷ 3)", True,
                        "Yes — 3 sevenths hold 120 litres, so one 7th is 40 litres."),
                    opt("360 litres (120 x 3)", False,
                        "That multiplied instead of dividing; one of the 3 sevenths is 120 ÷ 3 = 40."),
                    opt("120 litres", False,
                        "120 litres fill THREE sevenths together, so one 7th is smaller."),
                ], key="oneseventh",
            ),
            stage(
                "What is the TOTAL capacity (7 sevenths)?",
                "Multiply one 7th by 7.",
                [
                    opt("280 litres (40 x 7)", True,
                        "Yes — 7 x 40 = 280 litres total capacity."),
                    opt("160 litres (40 x 4)", False,
                        "That is only the filled 4/7; the whole tank is all 7 sevenths."),
                    opt("240 litres", False,
                        "Recount: one 7th is 40, and 7 x 40 = 280, not 240."),
                ], key="total",
            ),
        ],
        worked=[
            "Empty part = 7/7 - 4/7 = 3/7.",
            "3/7 = 120 litres, so one 7th = 120 ÷ 3 = 40 litres.",
            "Total = 7 x 40 = 280 litres.",
        ],
        verify={"op": "of", "args": ["3/7", "280"]},  # recomputes the 120 that pins the whole -> answer 120? no
        model={"type": "groups",
               "caps": [40, 40, 40, 40, 40, 40, 40],
               "labels": ["full", "full", "full", "full", "empty", "empty", "empty"],
               "target": "280",
               "capLabel": "7 sevenths of 40 litres = 280"},
        unit="litres",
        check="Filled 4/7 = 160 L and empty 3/7 = 120 L; 160 + 120 = 280 L.",
        explain="Why does the 'litres needed' describe the EMPTY fraction, not the full one?",
    )


# NOTE: the tank's displayed answer is the TOTAL (280). We verify the 120-litre
# relationship (3/7 of 280 = 120) with a dedicated check item below to keep the
# math-gate honest; the headline item is verified structurally. To keep near-100%
# gate coverage we instead attach a verify that recomputes the answer 280 from the
# fraction relationship is not directly an op, so we verify via 'of' producing 120
# would mismatch 280. We therefore DO NOT attach verify here (documented as a
# word-problem whose final answer is not a single fraction op). See report.
# -> remove the verify we tentatively added:
def _fix_tank():
    m10_tank()
    QUESTIONS[-1].pop("verify", None)


_fix_tank()


# ---- m10-3: Ajay bank balance (seed B7_031) 2700 = 3/5 -> total 4500 -> balance 2/5 = 1800 ----
def m10_bank():
    total = 4500
    assert Fraction(3, 5) * total == 2700
    balance = int(Fraction(2, 5) * total)  # 1800
    item(
        id="m10-3", module=10, title="Ajay's bank balance",
        story="Ajay withdrew Rs. 2700, which is 3/5 of the money in his account. What is the balance left after the withdrawal?",
        answer=str(balance),
        stages=[
            stage(
                "Rs. 2700 is 3/5 of the total. What is one 5th?",
                "One 5th = 2700 ÷ 3.",
                [
                    opt("Rs. 900 (2700 ÷ 3)", True,
                        "Right — 3 fifths are 2700, so one 5th is 2700 ÷ 3 = 900."),
                    opt("Rs. 8100 (2700 x 3)", False,
                        "That multiplied; one of the 3 fifths is 2700 ÷ 3 = 900."),
                    opt("Rs. 2700", False,
                        "2700 covers THREE fifths together, so one 5th is smaller."),
                ], key="fifth",
            ),
            stage(
                "What fraction of the money is LEFT after withdrawing 3/5?",
                "Whole is 5/5; subtract the withdrawn 3/5.",
                [
                    opt("2/5", True,
                        "Yes — 5/5 - 3/5 = 2/5 remains in the account."),
                    opt("3/5", False,
                        "3/5 is what was taken OUT; the balance is what stays in."),
                    opt("5/5", False,
                        "After a withdrawal the whole amount is no longer there; 2/5 remains."),
                ], key="leftfrac",
            ),
            stage(
                "So what is the balance (2/5 of the total)?",
                "One 5th is 900; take 2 of them.",
                [
                    opt("Rs. 1800 (2 x 900)", True,
                        "Yes — 2/5 of the total is 2 x 900 = Rs. 1800."),
                    opt("Rs. 4500", False,
                        "4500 is the TOTAL before withdrawal, not the balance left."),
                    opt("Rs. 900", False,
                        "900 is one fifth; the balance is TWO fifths, so 2 x 900 = 1800."),
                ], key="balance",
            ),
        ],
        worked=[
            "2700 is 3/5, so one 5th = 2700 ÷ 3 = 900, and the total = 5 x 900 = 4500.",
            "Balance fraction = 5/5 - 3/5 = 2/5.",
            "Balance = 2/5 of 4500 = 2 x 900 = Rs. 1800.",
        ],
        verify={"op": "of", "args": ["2/5", "4500"]},
        model={"type": "groups",
               "caps": [900, 900, 900, 900, 900],
               "labels": ["out", "out", "out", "left", "left"],
               "target": "1800",
               "capLabel": "5 fifths of 900; 2 left in"},
        unit="rupees",
        check="Withdrawn 2700 + balance 1800 = 4500 (the whole).",
        explain="Why is the balance the COMPLEMENT (2/5), not the withdrawn 3/5?",
    )


m10_bank()


# ---- m10-4: like-fraction equation (seed B7_021) x/7 four times = 48/28 -> x = 3 ----
def m10_likeeq():
    # x/7 + x/7 + x/7 + x/7 = 48/28 ; 4x/7 = 12/7 -> x = 3
    rhs = Fraction(48, 28)  # = 12/7
    assert rhs == Fraction(12, 7)
    # 4x/7 = 12/7 -> 4x = 12 -> x = 3
    x = 3
    assert Fraction(4 * x, 7) == rhs
    item(
        id="m10-4", module=10, title="The repeated numerator",
        story="The same number fills every box: box/7 + box/7 + box/7 + box/7 = 48/28. What number is the box?",
        answer=str(x),
        stages=[
            stage(
                "Simplify the right side, 48/28, to lowest terms.",
                "Divide top and bottom by their GCD.",
                [
                    opt("12/7 (48 ÷ 4 and 28 ÷ 4)", True,
                        "Right — the GCD of 48 and 28 is 4, giving 12/7."),
                    opt("24/14", False,
                        "That only divided by 2 — keep going: 24/14 = 12/7 in lowest terms."),
                    opt("48/28 is already lowest", False,
                        "Both 48 and 28 are even, so it can still be reduced to 12/7."),
                ], key="rhs",
            ),
            stage(
                "Add the four like fractions on the left. What do you get?",
                "Same bottom 7, so add the tops: box four times.",
                [
                    opt("4 x box / 7", True,
                        "Yes — four copies of box/7 is (4 x box)/7."),
                    opt("box / 28", False,
                        "Adding like fractions keeps the bottom 7; it does not become 7 x 4 = 28 on top of one box."),
                    opt("box / 7 (only one counts)", False,
                        "All four terms count; together they make (4 x box)/7."),
                ], key="left",
            ),
            stage(
                "Solve (4 x box)/7 = 12/7. What is box?",
                "Same bottom, so 4 x box = 12.",
                [
                    opt("3 (since 4 x 3 = 12)", True,
                        "Yes — 4 x box = 12, so box = 3."),
                    opt("12 (the whole top)", False,
                        "12 is 4 x box, not box itself; divide by 4 to get 3."),
                    opt("48", False,
                        "48 was before simplifying; after reducing, 4 x box = 12, so box = 3."),
                ], key="solve",
            ),
        ],
        worked=[
            "48/28 = 12/7 (divide by GCD 4).",
            "Left side = (4 x box)/7.",
            "So 4 x box = 12, giving box = 3.",
        ],
        verify={"op": "simplify", "args": ["12/7"]},  # confirms 48/28 reduces to 12/7, the pivot
        model={"type": "mapping", "rows": [["48/28", "12/7"], ["4 x box = 12", "box = 3"]]},
        check="Check: 4 x (3/7) = 12/7 = 48/28.",
        explain="Why can we compare only the tops once both sides share the denominator 7?",
    )


# m10-4's headline answer is '3' but the verify op proves the 12/7 pivot. To keep
# the math gate pointed at the item's OWN answer, retarget: we instead verify that
# the solved value satisfies the equation via a value we CAN express — use 'of' is
# not applicable. We keep the simplify-pivot verify but note the gate then checks
# answer=='3' against simplify('12/7')=='12/7' which MISMATCHES. So drop verify and
# rely on structure (documented).
def _fix_likeeq():
    m10_likeeq()
    QUESTIONS[-1].pop("verify", None)


_fix_likeeq()


# ---- m10-5: numerator defined by denominator (seed B7_002) -> 21/5 = 4 1/5 ----
def m10_numdef():
    # numerator 21, denominator is 16 less than numerator -> 21/5 -> mixed 4 1/5
    num, den = 21, 21 - 16
    ans = mixed(F(num, den))  # "4 1/5"
    assert ans == "4 1/5"
    item(
        id="m10-5", module=10, title="Numerator tells the denominator",
        story="The numerator of a fraction is 21. The denominator is 16 less than the numerator. Write the fraction as a mixed number.",
        answer=ans,
        stages=[
            stage(
                "What is the denominator?",
                "Denominator = numerator - 16.",
                [
                    opt("5 (21 - 16)", True,
                        "Right — 16 less than 21 is 21 - 16 = 5."),
                    opt("16 (the difference word)", False,
                        "16 is the amount you subtract, not the denominator itself."),
                    opt("37 (21 + 16)", False,
                        "'16 less than' means subtract 16, not add it."),
                ], key="den",
            ),
            stage(
                "So the fraction is 21/5. Is it proper or improper?",
                "Compare the top with the bottom.",
                [
                    opt("Improper — 21 is bigger than 5", True,
                        "Yes — the top is larger than the bottom, so 21/5 is improper and makes a mixed number."),
                    opt("Proper — fractions are always under 1", False,
                        "Not always; when the top exceeds the bottom the fraction is more than 1."),
                    opt("It equals exactly 4", False,
                        "21 ÷ 5 is 4 with a remainder, so it is 4 and a bit, not exactly 4."),
                ], key="kind",
            ),
            stage(
                "Convert 21/5 to a mixed number:",
                "21 ÷ 5 = whole remainder.",
                [
                    opt("4 1/5 (21 ÷ 5 = 4 r 1)", True,
                        "Yes — 5 goes into 21 four times with 1 left over, so 4 1/5."),
                    opt("4 1/16 (using 16)", False,
                        "16 was only the difference; the denominator is 5, so the leftover is over 5."),
                    opt("1 4/5 (digits swapped)", False,
                        "That is 9/5, far too small; 21/5 is 4 1/5."),
                ], key="convert",
            ),
        ],
        worked=[
            "Denominator = 21 - 16 = 5.",
            "Fraction = 21/5 (improper, since 21 > 5).",
            "21 ÷ 5 = 4 remainder 1, so 21/5 = 4 1/5.",
        ],
        verify={"op": "to_mixed", "args": ["21/5"]},
        model={"type": "parts", "total": 5, "shaded": 1,
               "label": "4 full fifths-groups + 1 leftover fifth"},
        check="4 x 5 + 1 = 21, back to 21/5.",
        explain="Why does 'the denominator is 16 less than the numerator' set the bottom, not the leftover?",
    )


m10_numdef()


# ---- m10-6: missing numerator in a sum (seed B7_016) 6 + box/8 = 7 3/8 -> 11 ----
def m10_missing():
    # 6 + box/8 = 7 3/8 -> box/8 = 1 3/8 = 11/8 -> box = 11
    target = Fraction(7, 1) + Fraction(3, 8) - Fraction(6)  # 11/8
    assert target == Fraction(11, 8)
    box = 11
    item(
        id="m10-6", module=10, title="Find the missing numerator",
        story="Find the number for the box: 6 + box/8 = 7 3/8.",
        answer=str(box),
        stages=[
            stage(
                "Subtract 6 from both sides. What must box/8 equal?",
                "7 3/8 - 6 leaves the fractional part plus one whole.",
                [
                    opt("1 3/8", True,
                        "Right — 7 3/8 - 6 = 1 3/8, so box/8 = 1 3/8."),
                    opt("3/8", False,
                        "That dropped the extra whole; 7 3/8 - 6 is 1 3/8, not just 3/8."),
                    opt("13/8 written as 1 5/8", False,
                        "7 3/8 - 6 = 1 3/8 exactly; recheck the whole-number part."),
                ], key="isolate",
            ),
            stage(
                "Write 1 3/8 as an improper fraction over 8.",
                "1 whole = 8/8.",
                [
                    opt("11/8 (8/8 + 3/8)", True,
                        "Yes — 1 = 8/8, so 1 3/8 = 8/8 + 3/8 = 11/8."),
                    opt("4/8 (1 + 3)", False,
                        "You cannot add the whole straight onto the numerator; 1 = 8/8 first."),
                    opt("3/8", False,
                        "That ignored the whole number 1; include 8/8 as well."),
                ], key="improper",
            ),
            stage(
                "So box/8 = 11/8. What is box?",
                "Same bottom means the tops match.",
                [
                    opt("11", True,
                        "Yes — equal bottoms, so box = 11."),
                    opt("8", False,
                        "8 is the denominator, not the numerator we are solving for."),
                    opt("3", False,
                        "3 is only the leftover eighths; the whole adds 8 more, giving 11."),
                ], key="read",
            ),
        ],
        worked=[
            "6 + box/8 = 7 3/8, so box/8 = 7 3/8 - 6 = 1 3/8.",
            "1 3/8 = 8/8 + 3/8 = 11/8.",
            "Same denominator 8, so box = 11.",
        ],
        model={"type": "parts", "total": 8, "shaded": 3,
               "label": "1 whole (8/8) + 3/8 = 11/8"},
        check="6 + 11/8 = 6 + 1 3/8 = 7 3/8.",
        explain="Why must we turn the whole number into eighths before reading the numerator?",
    )


m10_missing()


# ---- m10-7: Siddhi's exercise time (seed B7_029) 3/5 in 24 min -> full 40 min -> 11:40 ----
def m10_time():
    # 3/5 of the work takes 24 min -> one 5th = 8 min -> full = 40 min
    full = 40
    assert Fraction(3, 5) * full == 24
    item(
        id="m10-7", module=10, title="When will Siddhi finish?",
        story="Siddhi finishes 3/5 of her maths exercise in 24 minutes. She started at 11:00 am. At what time will she finish the whole exercise?",
        answer="11:40 am",
        stages=[
            stage(
                "3/5 of the work took 24 minutes. How long is one 5th?",
                "One 5th = 24 ÷ 3.",
                [
                    opt("8 minutes (24 ÷ 3)", True,
                        "Right — 3 fifths took 24 minutes, so one 5th is 8 minutes."),
                    opt("72 minutes (24 x 3)", False,
                        "That multiplied; one of the 3 fifths is 24 ÷ 3 = 8 minutes."),
                    opt("24 minutes", False,
                        "24 minutes covers THREE fifths together, so one fifth is less."),
                ], key="onefifth",
            ),
            stage(
                "How many minutes for the WHOLE exercise (5 fifths)?",
                "Multiply one 5th by 5.",
                [
                    opt("40 minutes (8 x 5)", True,
                        "Yes — 5 x 8 = 40 minutes for the full exercise."),
                    opt("24 minutes", False,
                        "24 minutes is only 3/5 of the work, not all of it."),
                    opt("32 minutes (8 x 4)", False,
                        "That is only 4 fifths; the whole is 5 fifths, so 8 x 5 = 40."),
                ], key="whole",
            ),
            stage(
                "She started at 11:00 am. When does she finish?",
                "Add 40 minutes to 11:00.",
                [
                    opt("11:40 am", True,
                        "Yes — 11:00 + 40 minutes = 11:40 am."),
                    opt("11:24 am", False,
                        "11:24 is when only 3/5 is done (24 minutes), not the whole exercise."),
                    opt("12:40 pm", False,
                        "That added an extra hour; the full task is 40 minutes, not 1 hour 40."),
                ], key="clock",
            ),
        ],
        worked=[
            "3/5 took 24 minutes, so one 5th = 24 ÷ 3 = 8 minutes.",
            "Whole exercise = 5 x 8 = 40 minutes.",
            "11:00 am + 40 minutes = 11:40 am.",
        ],
        verify={"op": "of", "args": ["3/5", "40"]},  # 3/5 of 40 = 24, the given time
        model={"type": "groups",
               "caps": [8, 8, 8, 8, 8],
               "labels": ["done", "done", "done", "left", "left"],
               "target": "40",
               "capLabel": "5 fifths of 8 min = 40 min"},
        unit="(clock time)",
        check="24 min done (3/5) + 16 min left (2/5) = 40 min total.",
        explain="Why does finding one 5th first let us scale up to the whole time?",
    )


# m10-7 answer is a clock time '11:40 am', not a fraction op result. The verify
# 'of 3/5 of 40 = 24' proves the time relationship but 24 != '11:40 am'. Drop it.
def _fix_time():
    m10_time()
    QUESTIONS[-1].pop("verify", None)


_fix_time()


# ---- m10-8: garden plants (seed B7_033) 2/9 roses,1/9 sun,4/9 mari, 30 hibiscus ----
def m10_garden():
    # remaining = 9/9 - 2/9 -1/9 -4/9 = 2/9 = 30 -> whole = 135
    whole = 135
    assert Fraction(2, 9) * whole == 30
    sun_mari = int((Fraction(1, 9) + Fraction(4, 9)) * whole)  # 5/9 * 135 = 75
    assert sun_mari == 75
    item(
        id="m10-8", module=10, title="Counting garden plants",
        story="In a garden, 2/9 of the plants are roses, 1/9 are sunflowers and 4/9 are marigolds. The remaining 30 plants are hibiscus. How many sunflowers and marigolds are there in all?",
        answer=str(sun_mari),
        stages=[
            stage(
                "What fraction of the plants are hibiscus (the remainder)?",
                "Subtract the three named fractions from 9/9.",
                [
                    opt("2/9 (9/9 - 2/9 - 1/9 - 4/9)", True,
                        "Right — 2/9 + 1/9 + 4/9 = 7/9, leaving 2/9 for hibiscus."),
                    opt("7/9", False,
                        "7/9 is the roses+sunflowers+marigolds together, not the hibiscus remainder."),
                    opt("1/9", False,
                        "9/9 - 7/9 = 2/9, not 1/9."),
                ], key="remainder",
            ),
            stage(
                "30 hibiscus are 2/9 of the garden. How many plants in all?",
                "One 9th = 30 ÷ 2, then x 9.",
                [
                    opt("135 (30 ÷ 2 x 9)", True,
                        "Yes — one 9th is 30 ÷ 2 = 15, so the whole is 15 x 9 = 135."),
                    opt("270 (30 x 9)", False,
                        "30 is TWO ninths, not one; find one 9th (15) first, then x 9."),
                    opt("60 (30 x 2)", False,
                        "That doubled the remainder; the whole is far bigger — 135 plants."),
                ], key="whole",
            ),
            stage(
                "How many are sunflowers AND marigolds (1/9 + 4/9 of 135)?",
                "That is 5/9 of 135; one 9th is 15.",
                [
                    opt("75 (5 x 15)", True,
                        "Yes — 5/9 of 135 is 5 x 15 = 75 plants."),
                    opt("30 (just the roses count)", False,
                        "30 is the hibiscus group; sunflowers + marigolds are 5 ninths, giving 75."),
                    opt("15 (one ninth)", False,
                        "One 9th is 15; together sunflowers and marigolds are 5 ninths, so 75."),
                ], key="combine",
            ),
        ],
        worked=[
            "Hibiscus fraction = 9/9 - 2/9 - 1/9 - 4/9 = 2/9.",
            "2/9 = 30, so one 9th = 15 and the whole = 9 x 15 = 135.",
            "Sunflowers + marigolds = (1/9 + 4/9) of 135 = 5/9 x 135 = 75.",
        ],
        verify={"op": "of", "args": ["5/9", "135"]},
        model={"type": "groups",
               "caps": [15, 15, 15, 15, 15, 15, 15, 15, 15],
               "labels": ["rose", "rose", "sun", "mari", "mari", "mari", "mari", "hib", "hib"],
               "target": "75",
               "capLabel": "9 ninths of 15; sun+mari take 5"},
        unit="plants",
        check="Roses 30 + (sun+mari) 75 + hibiscus 30 = 135 plants.",
        explain="Why does the hibiscus remainder unlock the size of the whole garden?",
    )


m10_garden()


# =============================================================================
# ASSEMBLE & WRITE
# =============================================================================

MODULES = [M1, M2, M3, M4, M5, M6, M7, M8, M9, M10]

SOURCE = {
    "slug": "fractions-g5",
    "title": "Fraction Sense · Grade 5",
    "concept": "Fractions",
    "gradeRange": [5, 5],
    "modules": MODULES,
    "questions": QUESTIONS,
}


def main():
    # sanity: 10 modules, 8 items each = 80
    counts = {}
    for q in QUESTIONS:
        counts[q["module"]] = counts.get(q["module"], 0) + 1
    assert len(MODULES) == 10, f"expected 10 modules, got {len(MODULES)}"
    for m in range(1, 11):
        assert counts.get(m, 0) == 8, f"module {m} has {counts.get(m, 0)} items (want 8)"
    assert len(QUESTIONS) == 80, f"expected 80 items, got {len(QUESTIONS)}"

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(SOURCE, f, ensure_ascii=False, indent=2)
        f.write("\n")

    verifiable = sum(1 for q in QUESTIONS if "verify" in q)
    print(f"wrote {OUT}")
    print(f"  {len(MODULES)} modules, {len(QUESTIONS)} items")
    print(f"  {verifiable}/{len(QUESTIONS)} items carry a math-gate verify spec")


if __name__ == "__main__":
    main()
