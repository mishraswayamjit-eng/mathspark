#!/usr/bin/env python3
"""
Author the Grade-6 "Fraction Sense" Concept Trainer SOURCE JSON.

Every fraction answer is COMPUTED with `fractions.Fraction` so no number is
hallucinated — the generator's math-gate recomputes the `verify` spec on each
item and asserts it equals the authored `answer`. This script only BUILDS the
source dict and writes `scripts/sources/fractions-g6-source.json`.

Then run:
    python scripts/generate_trainer.py scripts/sources/fractions-g6-source.json

Grade-6 arc (10 modules x 8 items):
  1  Name the whole
  2  Part & complement from a figure
  3  Equivalent fractions & odd-one-out
  4  Lowest terms via GCD
  5  Compare & order fractions
  6  Add/subtract LIKE fractions
  7  Add/subtract UNLIKE fractions (LCD)
  8  Mixed <-> improper & mixed arithmetic
  9  Fraction OF a quantity & multiply/divide fractions
 10  Averages, series & algebraic fraction equations (Stretch)
"""

import json
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "sources", "fractions-g6-source.json")


# ── formatting helpers (mirror generate_trainer.py so answers match) ─────────

def F(s):
    """Parse '3/8', '11/8', '4 1/5', 7 into a Fraction."""
    if isinstance(s, int):
        return Fraction(s)
    text = str(s).strip()
    if " " in text:
        whole, frac = text.split(None, 1)
        f = Fraction(frac)
        sign = -1 if whole.strip().startswith("-") else 1
        return Fraction(int(whole)) + sign * f
    return Fraction(text)


def ff(f):
    """Canonical lowest-terms string: integers as 'n', else 'n/d'."""
    f = f if isinstance(f, Fraction) else F(f)
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


def fm(f):
    """Mixed-number string '4 1/5' (or 'n'/'n/d')."""
    f = f if isinstance(f, Fraction) else F(f)
    if f.denominator == 1:
        return str(f.numerator)
    if abs(f.numerator) < f.denominator:
        return ff(f)
    sign = "-" if f < 0 else ""
    a = abs(f)
    whole = a.numerator // a.denominator
    rem = a - whole
    return f"{sign}{whole} {rem.numerator}/{rem.denominator}"


# ── tiny builders ────────────────────────────────────────────────────────────

def opt(text, correct, feedback):
    return {"text": text, "correct": correct, "feedback": feedback}


def stage(prompt, hint, options, key=None):
    s = {"prompt": prompt, "hint": hint, "options": options}
    if key:
        s["key"] = key
    return s


QUESTIONS = []
_counter = {}


def item(module, title, story, answer, stages, worked,
         check=None, explain=None, model=None, verify=None, unit=None):
    _counter[module] = _counter.get(module, 0) + 1
    code = f"m{module}-{_counter[module]}"
    q = {
        "id": code,
        "module": module,
        "title": title,
        "story": story,
        "answer": answer,
        "stages": stages,
        "worked": worked,
    }
    if unit:
        q["unit"] = unit
    if check:
        q["check"] = check
    if explain:
        q["explain"] = explain
    if model:
        q["model"] = model
    if verify:
        q["verify"] = verify
    QUESTIONS.append(q)


# =============================================================================
# MODULE 1 — Name the whole
# =============================================================================

def module1():
    M = 1
    # Each: a share of a named whole; answer = part amount (an integer).
    rows = [
        ("Priya's marbles", "Priya has 30 marbles. She gives 1/3 of them to a friend. How many marbles does she give away?",
         "30", "1/3", "marbles", "her bag"),
        ("Chess club", "A class has 40 children. 1/4 of them join the chess club. How many children join chess?",
         "40", "1/4", "children", "a class"),
        ("Pencils in a box", "A box holds 24 pencils. 3/8 of the pencils are red. How many pencils are red?",
         "24", "3/8", "pencils", "a box"),
        ("Pages read", "A storybook has 60 pages. Raj has read 2/5 of it. How many pages has he read?",
         "60", "2/5", "pages", "the book"),
        ("Share of rupees", "Meera has 80 rupees. She spends 3/4 of it on a book. How many rupees does she spend?",
         "80", "3/4", "rupees", "her money"),
        ("Ripe mangoes", "A crate holds 36 mangoes. 5/6 of them are ripe. How many are ripe?",
         "36", "5/6", "mangoes", "the crate"),
        ("Full water tank", "A tank holds 48 litres. It is 5/8 full. How many litres are in it?",
         "48", "5/8", "litres", "the tank"),
        ("Stickers given", "Arjun has 45 stickers. He gives 2/9 of them away. How many does he give away?",
         "45", "2/9", "stickers", "his collection"),
    ]
    for title, story, whole, share, unit, wholename in rows:
        W = int(whole)
        sh = F(share)
        part = ff(sh * W)
        comp = ff((1 - sh) * W)
        story_q = story
        wrong_whole = str(sh.numerator)  # mistakes the numerator for the whole
        st1 = stage(
            "What amount stands for the whole (everything we start with)?",
            f"Complete: the whole is all {unit} we begin with.",
            [
                opt(f"All {W} {unit} in {wholename}", True,
                    f"Yes — the whole is every one of the {W} {unit} we start with."),
                opt(f"Just the {share} we take away", False,
                    "That is the share we act on, not the whole we measure it against."),
                opt(f"The number {wrong_whole} because it is on top of the fraction", False,
                    "The top number counts parts of the share — it is not the size of the whole."),
            ], key="whole")
        st2 = stage(
            f"What does {share} of the whole mean here?",
            "A fraction cuts the whole into equal parts; the top number counts how many.",
            [
                opt(f"Cut {W} into {sh.denominator} equal parts, then take {sh.numerator}", True,
                    f"Right — split into {sh.denominator} equal groups and keep {sh.numerator} of them."),
                opt(f"Just subtract {sh.numerator} from {W}", False,
                    "A fraction is not subtraction — it splits into equal parts first."),
                opt(f"Add {sh.numerator} and {sh.denominator} to the whole", False,
                    "The two numbers of a fraction are a part-count and a part-size, not amounts to add on."),
            ], key="meaning")
        st3 = stage(
            f"Which calculation finds {share} of {W}?",
            "part = (fraction) x whole.",
            [
                opt(f"({sh.numerator}/{sh.denominator}) x {W} = {part}", True,
                    f"Exactly — ({share}) x {W} = {part} {unit}."),
                opt(f"{W} - {sh.denominator} = {W - sh.denominator}", False,
                    "That subtracts the bottom number as if it were an amount in the story."),
                opt(f"{W} / {sh.numerator} = {ff(F(W) / sh.numerator)}", False,
                    "Dividing only by the top number ignores how many parts we keep."),
            ], key="equation")
        item(M, title, story_q, part,
             [st1, st2, st3],
             worked=[
                 f"The whole is all {W} {unit} in {wholename}.",
                 f"{share} means split {W} into {sh.denominator} equal parts, then take {sh.numerator}.",
                 f"One part is {W}/{sh.denominator} = {ff(F(W)/sh.denominator)} {unit}.",
                 f"So {share} of {W} = ({sh.numerator}/{sh.denominator}) x {W} = {part} {unit}.",
             ],
             check=f"The two shares add back to the whole: {part} + {comp} = {W}.",
             explain="Name the whole first, then the share. The whole is what 'the whole fraction' (1) stands for.",
             model={"type": "parts", "total": sh.denominator, "shaded": sh.numerator,
                    "label": f"{share} of {W} {unit} = {part} {unit}"},
             verify={"op": "of", "args": [share, whole]}, unit=unit)


# =============================================================================
# MODULE 2 — Part & complement from a figure
# =============================================================================

def module2():
    M = 2
    rows = [
        ("Shaded strip", 8, 3, "squares"),
        ("Window panes", 6, 5, "panes"),
        ("Garden beds", 10, 7, "beds"),
        ("Chocolate bar", 12, 5, "pieces"),
        ("Coloured flags", 9, 4, "flags"),
        ("Parking spaces", 10, 3, "spaces"),
        ("Fruit tray", 8, 5, "cups"),
        ("Tiled wall", 12, 7, "tiles"),
    ]
    for title, total, shaded, unit in rows:
        part = ff(Fraction(shaded, total))
        comp = ff(Fraction(total - shaded, total))
        story = (f"A strip is cut into {total} equal {unit}. {shaded} of them are shaded. "
                 f"What fraction is shaded, and what fraction is left plain?")
        st1 = stage(
            "What is the whole, written as a fraction?",
            "All the equal parts together make one whole.",
            [
                opt(f"{total}/{total} (all {total} {unit})", True,
                    f"Yes — all {total} equal {unit} together are the whole, {total}/{total} = 1."),
                opt(f"{shaded}/{total} (only the shaded part)", False,
                    "That is one part of the whole, not the whole itself."),
                opt(f"{total}/1 (just the number {total})", False,
                    "The denominator must show the equal parts the whole is cut into."),
            ], key="whole")
        st2 = stage(
            "What fraction is shaded?",
            "Top = shaded parts, bottom = total equal parts.",
            [
                opt(f"{shaded}/{total}", True,
                    f"Right — {shaded} shaded out of {total} equal parts is {shaded}/{total}."),
                opt(f"{total}/{shaded}", False,
                    "That flips the fraction — the total goes on the bottom, not the top."),
                opt(f"{shaded}/{total - shaded}", False,
                    "The bottom must be the TOTAL parts, not just the plain ones."),
            ], key="shaded")
        st3 = stage(
            "What fraction is left plain (the complement)?",
            "Shaded + plain = the whole = 1.",
            [
                opt(f"{total - shaded}/{total}", True,
                    f"Yes — {total} - {shaded} = {total - shaded} plain, so {total - shaded}/{total}."),
                opt(f"{shaded}/{total}", False,
                    "That repeats the shaded part; the plain part is what is left over."),
                opt(f"{total - shaded}/{shaded}", False,
                    "The bottom must be the TOTAL parts, not just the shaded ones."),
            ], key="complement")
        item(M, title, story, part,
             [st1, st2, st3],
             worked=[
                 f"The whole is {total} equal {unit}: {total}/{total} = 1.",
                 f"Shaded: {shaded} of {total} parts = {shaded}/{total}.",
                 f"Plain: {total} - {shaded} = {total - shaded} parts = {total - shaded}/{total}.",
                 f"In lowest terms the shaded share is {part}.",
             ],
             check=f"Shaded + plain = {shaded}/{total} + {total - shaded}/{total} = {total}/{total} = 1.",
             explain="A figure makes the denominator visible: it is the number of equal parts you can count.",
             model={"type": "parts", "total": total, "shaded": shaded,
                    "label": f"{shaded}/{total} shaded, {total - shaded}/{total} plain"},
             verify={"op": "simplify", "args": [f"{shaded}/{total}"]})


# =============================================================================
# MODULE 3 — Equivalent fractions & odd-one-out
# =============================================================================

def module3():
    M = 3
    # (a) missing-number equivalents (mirror "3/8 = ?/40")
    miss = [
        ("Filling a bigger grid", "3/8", 40),
        ("Same share, new bottom", "3/5", 30),
        ("Matching the recipe", "1/2", 10),
        ("Equal slices", "2/3", 12),
    ]
    for title, frac, newden in miss:
        f = F(frac)
        k = newden // f.denominator
        newnum = f.numerator * k
        equivstr = f"{newnum}/{newden}"
        story = (f"Fill in the missing number so the fractions are equal: {frac} = ?/{newden}. "
                 f"The two fractions must name the SAME share.")
        st1 = stage(
            f"How do we turn the bottom {f.denominator} into {newden}?",
            "Find what you multiply the denominator by.",
            [
                opt(f"Multiply by {k} (because {f.denominator} x {k} = {newden})", True,
                    f"Yes — {f.denominator} x {k} = {newden}."),
                opt(f"Add {newden - f.denominator} (because {f.denominator} + {newden - f.denominator} = {newden})", False,
                    "Equivalent fractions scale by MULTIPLYING, not adding, both numbers."),
                opt(f"Multiply by {newden} (ignore the old {f.denominator})", False,
                    f"That overshoots — {f.denominator} x {newden} is far bigger than {newden}."),
            ], key="scale")
        st2 = stage(
            "What must we do to the top number to keep the share equal?",
            "Whatever you do to the bottom, do the SAME to the top.",
            [
                opt(f"Multiply the top by {k} too", True,
                    f"Right — multiply BOTH by {k} so the share stays the same."),
                opt("Leave the top number unchanged", False,
                    "Scaling only the bottom shrinks the share — both parts must scale together."),
                opt(f"Add {k} to the top", False,
                    "Equivalent fractions multiply both numbers by the same factor, they do not add."),
            ], key="top")
        st3 = stage(
            "What is the missing top number?",
            f"Top = {f.numerator} x {k}.",
            [
                opt(f"{newnum}", True,
                    f"Yes — {f.numerator} x {k} = {newnum}, so {frac} = {equivstr}."),
                opt(f"{f.numerator}", False,
                    "That left the top unchanged; it must scale by the same factor as the bottom."),
                opt(f"{f.numerator + k}", False,
                    "That added the factor instead of multiplying by it."),
            ], key="answer")
        item(M, title, story, equivstr,
             [st1, st2, st3],
             worked=[
                 f"Bottom: {f.denominator} x {k} = {newden}.",
                 f"Top must scale the same way: {f.numerator} x {k} = {newnum}.",
                 f"So {frac} = {equivstr} — the same share written on a bigger scale.",
             ],
             check=f"{equivstr} back in lowest terms: {ff(F(equivstr))} = {frac}.",
             explain="Multiplying top and bottom by the same number does not change the share, only how it is written.",
             model={"type": "mapping", "rows": [[frac, equivstr], ["x" + str(k) + " top", "x" + str(k) + " bottom"]]},
             verify={"op": "equiv", "args": [frac, k]})

    # (b) odd-one-out among equivalents (mirror the real seed stem)
    oddrows = [
        ("Which does not belong?", ["10/15", "12/30", "14/35", "16/40", "24/60"]),
        ("Spot the stranger", ["2/3", "4/6", "6/9", "8/16", "10/15"]),
        ("One is different", ["3/4", "6/8", "9/12", "10/15", "15/20"]),
        ("Find the odd fraction", ["1/4", "2/8", "3/12", "4/20", "5/20"]),
    ]
    for title, lst in oddrows:
        from collections import Counter
        reduced = [ff(F(x)) for x in lst]
        cnt = Counter(reduced)
        common = cnt.most_common(1)[0][0]
        odd_idx = next(i for i, r in enumerate(reduced) if r != common)
        odd = lst[odd_idx]
        other = next(x for i, x in enumerate(lst) if i != odd_idx)
        story = (f"All but one of these name the same share. Which fraction does NOT belong? "
                 f"{', '.join(lst)}.")
        st1 = stage(
            "How do we test if fractions name the same share?",
            "Put each in lowest terms and compare.",
            [
                opt("Simplify each one to its lowest terms, then see which is different", True,
                    "Yes — equal fractions reduce to the very same lowest-terms fraction."),
                opt("Pick the one with the biggest numbers", False,
                    "Big numbers can still be equal (like 24/60). Size of the numbers does not decide."),
                opt("Pick the one with the smallest bottom number", False,
                    "A small denominator does not mean it is the odd one; reduce them all first."),
            ], key="method")
        st2 = stage(
            f"What do the matching fractions reduce to?",
            "Divide top and bottom of each by their common factor.",
            [
                opt(f"{common}", True,
                    f"Right — most of them reduce to {common}."),
                opt(f"{ff(F(odd))}", False,
                    f"That is only what {odd} reduces to — the stranger, not the group."),
                opt(common.split('/')[1] + "/" + common.split('/')[0] if '/' in common else common + "/1", False,
                    "That flips the fraction — the top stays on top when you reduce."),
            ], key="common")
        st3 = stage(
            "So which fraction does NOT belong?",
            f"The group shares {common}; the odd one does not.",
            [
                opt(f"{odd}", True,
                    f"Yes — {odd} reduces to {ff(F(odd))}, not {common}, so it is the stranger."),
                opt(f"{other}", False,
                    f"{other} reduces to {common}, so it belongs with the group."),
                opt("They are all equal", False,
                    "One of them reduces differently — look again at each in lowest terms."),
            ], key="odd")
        item(M, title, story, odd,
             [st1, st2, st3],
             worked=[
                 "Write each fraction in lowest terms by dividing out the common factor.",
                 f"Most of them become {common}.",
                 f"{odd} becomes {ff(F(odd))}, which is different.",
                 f"So {odd} is the odd one out.",
             ],
             check=f"{other} = {common} but {odd} = {ff(F(odd))}.",
             explain="Equivalent fractions share one lowest-terms form; the stranger reduces to something else.",
             model={"type": "mapping", "rows": [[x, ff(F(x))] for x in lst]})


# =============================================================================
# MODULE 4 — Lowest terms via GCD
# =============================================================================

def module4():
    M = 4
    import math
    rows = [
        ("Reducing a score", "18/24"),
        ("Simplest slices", "16/40"),
        ("Tidy the fraction", "24/36"),
        ("Lowest terms", "30/45"),
        ("Shrink it down", "42/56"),
        ("Simplify the share", "27/45"),
        ("Cut it to size", "20/50"),
        ("Neatest form", "36/48"),
    ]
    for title, frac in rows:
        f = F(frac)
        n, d = int(frac.split("/")[0]), int(frac.split("/")[1])
        g = math.gcd(n, d)
        reduced = ff(f)
        halfn, halfd = n // 2, d // 2  # a tempting "only divided by 2 once" trap when g>2
        story = (f"Write {frac} in its lowest terms (simplest form). "
                 f"That means dividing the top and bottom by their greatest common factor.")
        st1 = stage(
            f"What is the greatest common factor (GCF) of {n} and {d}?",
            "The biggest number that divides BOTH exactly.",
            [
                opt(f"{g}", True,
                    f"Yes — {g} divides both {n} and {d} exactly, and nothing larger does."),
                opt(f"{min(n, d)}", False,
                    f"{min(n, d)} does not divide the other number exactly, so it cannot be the common factor."),
                opt("1 (fractions can't be reduced)", False,
                    "Many fractions share a bigger factor than 1 — check 2, 3, and so on."),
            ], key="gcf")
        st2 = stage(
            f"Divide both by {g}. What do you get?",
            "Divide the top AND the bottom by the GCF.",
            [
                opt(f"{n // g}/{d // g} = {reduced}", True,
                    f"Right — {n}/{g} = {n // g} and {d}/{g} = {d // g}, giving {reduced}."),
                opt(f"{n - g}/{d - g}", False,
                    "Simplifying DIVIDES both numbers, it does not subtract from them."),
                opt(f"{halfn}/{halfd}" if g != 2 else f"{n}/{d // g}", False,
                    ("Dividing only by 2 does not finish the job when a bigger factor exists."
                     if g != 2 else "Both the top and the bottom must be divided, not just one.")),
            ], key="divide")
        st3 = stage(
            "Is the result already in lowest terms?",
            "It is lowest terms when the only common factor of top and bottom is 1.",
            [
                opt(f"Yes — {reduced} cannot be reduced further", True,
                    f"Correct — {ff(f)} has no common factor above 1, so it is simplest form."),
                opt("No, keep dividing by 2 forever", False,
                    "Once the GCF is 1 you stop — further dividing would break the equality."),
                opt(f"No, flip it to {d // g}/{n // g}", False,
                    "Flipping changes the value; simplest form keeps the same share."),
            ], key="done")
        item(M, title, story, reduced,
             [st1, st2, st3],
             worked=[
                 f"Greatest common factor of {n} and {d} is {g}.",
                 f"Divide both by {g}: {n}/{g} = {n // g}, {d}/{g} = {d // g}.",
                 f"So {frac} = {reduced} in lowest terms.",
             ],
             check=f"{n // g} and {d // g} share no factor above 1.",
             explain="Dividing top and bottom by the same number keeps the share but makes the writing simplest.",
             model={"type": "parts", "total": f.denominator, "shaded": f.numerator,
                    "label": f"{frac} = {reduced} (same shaded area, fewer pieces)"},
             verify={"op": "simplify", "args": [frac]})


# =============================================================================
# MODULE 5 — Compare & order fractions
# =============================================================================

def module5():
    M = 5
    # mostly from real "Which is greater" seed stems
    rows = [
        ("Which is greater?", "2/4", "2/3"),
        ("Bigger slice", "1/3", "3/4"),
        ("Compare shares", "3/4", "7/8"),
        ("Who ran further?", "2/5", "4/8"),
        ("Pick the larger", "4/6", "7/8"),
        ("Smaller bottom trap", "1/7", "1/5"),
        ("Equal or not?", "4/8", "2/6"),
        ("Order two shares", "5/6", "1/7"),
    ]
    for title, a, b in rows:
        fa, fb = F(a), F(b)
        lcd = (fa.denominator * fb.denominator) // __import__("math").gcd(fa.denominator, fb.denominator)
        na = fa.numerator * (lcd // fa.denominator)
        nb = fb.numerator * (lcd // fb.denominator)
        if fa > fb:
            bigger, big_reason = a, f"{na}/{lcd} > {nb}/{lcd}"
        elif fb > fa:
            bigger, big_reason = b, f"{nb}/{lcd} > {na}/{lcd}"
        else:
            bigger, big_reason = "equal", f"{na}/{lcd} = {nb}/{lcd}"
        story = (f"Which is greater, {a} or {b}? Give both the same bottom number first, "
                 f"then compare the tops.")
        st1 = stage(
            "Why can't we just compare the tops right now?",
            "The denominators are different, so the parts are different sizes.",
            [
                opt("The bottoms differ, so the parts are different sizes", True,
                    "Right — a part of a fifth is not the same size as a part of a third."),
                opt("The bigger bottom number is always the bigger fraction", False,
                    "A bigger bottom means SMALLER parts, so this is a common trap."),
                opt("The bigger top number is always the bigger fraction", False,
                    "Only true when the bottoms match — here they don't yet."),
            ], key="why")
        st2 = stage(
            f"Rewrite both with the common bottom {lcd}. What do you get?",
            "Scale each fraction up to the common denominator.",
            [
                opt(f"{a} = {na}/{lcd} and {b} = {nb}/{lcd}", True,
                    f"Yes — both now have bottom {lcd}, so the tops are comparable."),
                opt(f"{a} = {fa.numerator}/{lcd} and {b} = {fb.numerator}/{lcd}", False,
                    "You changed only the bottoms; the tops must scale by the same factor too."),
                opt(f"{a} = {na}/{fa.denominator} and {b} = {nb}/{fb.denominator}", False,
                    "Keep the common bottom; don't put the old denominators back."),
            ], key="common")
        if bigger == "equal":
            correct_opt = opt("They are equal", True, f"Right — {big_reason}.")
            wrongs = [opt(a, False, f"Check again: {big_reason}, so neither is larger."),
                      opt(b, False, f"Check again: {big_reason}, so neither is larger.")]
        else:
            smaller = b if bigger == a else a
            correct_opt = opt(bigger, True, f"Yes — {big_reason}, so {bigger} is greater.")
            wrongs = [opt(smaller, False, f"That is the smaller share: {big_reason}."),
                      opt("They are equal", False, f"Not equal — {big_reason}.")]
        st3 = stage(
            "So which is greater?",
            "Bigger top (with equal bottoms) = bigger fraction.",
            [correct_opt] + wrongs, key="pick")
        ans = bigger
        it_kwargs = dict(
            worked=[
                f"Common bottom of {fa.denominator} and {fb.denominator} is {lcd}.",
                f"{a} = {na}/{lcd}, {b} = {nb}/{lcd}.",
                f"Compare tops: {big_reason}.",
                (f"So {bigger} is greater." if bigger != "equal" else "So the two shares are equal."),
            ],
            check=f"With bottom {lcd}: {na} vs {nb}.",
            explain="Fractions are only comparable when the parts are the same size — that is why we match denominators.",
            model={"type": "mapping", "rows": [[a, f"{na}/{lcd}"], [b, f"{nb}/{lcd}"]]},
        )
        if bigger == "equal":
            it_kwargs["verify"] = {"op": "compare", "args": [a, b]}
            ans = "="  # compare op returns the '=' symbol
            story = story.replace("Which is greater", "Compare")
        else:
            it_kwargs["verify"] = {"op": "larger", "args": [a, b]}
            # the generator's `larger` op returns the lowest-terms form, so the
            # authored answer must match that canonical string.
            ans = ff(max(fa, fb))
        item(M, title, story, ans, [st1, st2, st3], **it_kwargs)


# =============================================================================
# MODULE 6 — Add/subtract LIKE fractions
# =============================================================================

def module6():
    M = 6
    rows = [
        ("Same-bottom add", "add", "3/5", "2/5"),
        ("Pizza slices", "add", "4/8", "4/8"),
        ("Filling the tenths", "add", "2/10", "5/10"),
        ("Twelfths together", "add", "4/12", "5/12"),
        ("What is left", "sub", "7/8", "3/8"),
        ("Drink the juice", "sub", "9/10", "4/10"),
        ("Ribbon left", "sub", "5/6", "2/6"),
        ("Ninths remaining", "sub", "7/9", "2/9"),
    ]
    for title, op, a, b in rows:
        fa, fb = F(a), F(b)
        d = fa.denominator
        na, nb = fa.numerator, fb.numerator
        if op == "add":
            raw_top = na + nb
            res = ff(fa + fb)
            story = f"Add {a} + {b}. The bottoms are the same, so add only the tops."
            verb, sym = "add", "+"
        else:
            raw_top = na - nb
            res = ff(fa - fb)
            story = f"Subtract {a} - {b}. The bottoms match, so subtract only the tops."
            verb, sym = "subtract", "-"
        st1 = stage(
            "The bottom numbers are the same. What does that tell us?",
            "Equal bottoms mean the parts are the same size.",
            [
                opt("The parts are the same size, so we can combine the tops directly", True,
                    "Yes — same-size parts can be counted together."),
                opt("We must first find a new common bottom", False,
                    "The bottoms already match, so no new denominator is needed."),
                opt("We should multiply the bottoms together", False,
                    "That is for unlike fractions; equal bottoms stay as they are."),
            ], key="like")
        st2 = stage(
            f"What happens to the bottom number when we {verb}?",
            "The size of each part does not change.",
            [
                opt(f"It stays {d}", True,
                    f"Right — the parts are still {d}ths, so the bottom stays {d}."),
                opt(f"It becomes {d + d} (add the bottoms)", False,
                    "Adding the bottoms is the classic slip — the part-size does not change."),
                opt(f"It becomes {d * d}", False,
                    "Multiplying the bottoms changes the part-size; here it must stay the same."),
            ], key="bottom")
        st3 = stage(
            f"So what is {a} {sym} {b}?",
            f"Tops: {na} {sym} {nb}; bottom stays {d}.",
            [
                opt(f"{res}", True,
                    f"Yes — {na} {sym} {nb} = {raw_top} over {d}, which is {res}."),
                opt(f"{na}{sym.replace('-', '-')}{nb}".replace("+", "+") and f"{raw_top}/{d + d}", False,
                    "That added the bottoms too — keep the bottom at " + str(d) + "."),
                opt(f"{raw_top}/{d}" if ff(Fraction(raw_top, d)) != f"{raw_top}/{d}" else f"{raw_top + 1}/{d}", False,
                    ("Good tops, but remember to simplify to lowest terms."
                     if ff(Fraction(raw_top, d)) != f"{raw_top}/{d}" else
                     "Re-add the tops carefully.")),
            ], key="result")
        item(M, title, story, res,
             [st1, st2, st3],
             worked=[
                 f"Same bottom {d}, so {verb} the tops: {na} {sym} {nb} = {raw_top}.",
                 f"Keep the bottom {d}: {raw_top}/{d}.",
                 f"In lowest terms that is {res}.",
             ],
             check=f"The bottom never changed from {d}.",
             explain="Like fractions share the same part-size, so you count the parts (tops) and keep the size (bottom).",
             model={"type": "parts", "total": d, "shaded": min(abs(raw_top), d),
                    "label": f"{a} {sym} {b} = {res}"},
             verify={"op": op, "args": [a, b]})


# =============================================================================
# MODULE 7 — Add/subtract UNLIKE fractions (LCD)
# =============================================================================

def module7():
    M = 7
    import math
    rows = [
        ("Unlike bottoms", "add", "1/2", "1/3"),
        ("Mixing thirds and sixths", "add", "1/3", "1/6"),
        ("Quarters and eighths", "add", "1/4", "3/8"),
        ("Fifths and tenths", "add", "2/5", "3/10"),
        ("Take away a smaller part", "sub", "3/4", "1/6"),
        ("Half minus a third", "sub", "1/2", "1/3"),
        ("Difference of shares", "sub", "5/6", "1/4"),
        ("Tenths from a half", "sub", "1/2", "3/10"),
    ]
    for title, op, a, b in rows:
        fa, fb = F(a), F(b)
        lcd = fa.denominator * fb.denominator // math.gcd(fa.denominator, fb.denominator)
        na = fa.numerator * (lcd // fa.denominator)
        nb = fb.numerator * (lcd // fb.denominator)
        if op == "add":
            res = ff(fa + fb)
            raw = na + nb
            sym, verb = "+", "add"
        else:
            res = ff(fa - fb)
            raw = na - nb
            sym, verb = "-", "subtract"
        wrong_add_bottoms = f"{fa.numerator + fb.numerator}/{fa.denominator + fb.denominator}"
        story = f"Work out {a} {sym} {b}. The bottoms are different, so find a common bottom first."
        st1 = stage(
            "Why can't we combine the tops straight away?",
            "Different bottoms mean the parts are different sizes.",
            [
                opt("The parts are different sizes, so they must be made equal first", True,
                    "Right — you cannot count unequal parts together."),
                opt(f"We can just do {wrong_add_bottoms}", False,
                    "Adding tops and bottoms separately is the most common fraction slip — it changes the value."),
                opt("We compare them instead of combining", False,
                    "The task is to combine, but first the parts must be the same size."),
            ], key="why")
        st2 = stage(
            f"What is the least common bottom (LCD) of {fa.denominator} and {fb.denominator}?",
            "Smallest number both bottoms divide into.",
            [
                opt(f"{lcd}", True,
                    f"Yes — {lcd} is the smallest number both {fa.denominator} and {fb.denominator} divide into."),
                opt(f"{fa.denominator + fb.denominator}", False,
                    "Adding the bottoms rarely gives a common bottom; use the least common multiple."),
                opt(f"{fa.denominator * fb.denominator}" if lcd != fa.denominator * fb.denominator else f"{lcd * 2}", False,
                    ("That is A common bottom but not the LEAST one; a smaller one works."
                     if lcd != fa.denominator * fb.denominator else
                     "Too big — look for the smallest shared multiple.")),
            ], key="lcd")
        st3 = stage(
            f"Rewrite and {verb}: {na}/{lcd} {sym} {nb}/{lcd} = ?",
            f"Combine the tops over {lcd}, then simplify.",
            [
                opt(f"{res}", True,
                    f"Yes — {na} {sym} {nb} = {raw} over {lcd}, which simplifies to {res}."),
                opt(wrong_add_bottoms, False,
                    "That combined tops and bottoms separately instead of using the common bottom."),
                opt(f"{raw}/{lcd}" if ff(Fraction(raw, lcd)) != f"{raw}/{lcd}" else f"{raw}/{lcd * 2}", False,
                    ("Right tops, but simplify to lowest terms."
                     if ff(Fraction(raw, lcd)) != f"{raw}/{lcd}" else
                     "Keep the common bottom " + str(lcd) + ".")),
            ], key="result")
        item(M, title, story, res,
             [st1, st2, st3],
             worked=[
                 f"LCD of {fa.denominator} and {fb.denominator} is {lcd}.",
                 f"{a} = {na}/{lcd}, {b} = {nb}/{lcd}.",
                 f"{verb.capitalize()} the tops: {na} {sym} {nb} = {raw}, over {lcd} = {raw}/{lcd}.",
                 f"In lowest terms: {res}.",
             ],
             check=f"Both parts are now {lcd}ths before combining.",
             explain="Unlike fractions need a shared part-size (the LCD) before the tops can be combined.",
             model={"type": "mapping", "rows": [[a, f"{na}/{lcd}"], [b, f"{nb}/{lcd}"], [f"{a} {sym} {b}", res]]},
             verify={"op": op, "args": [a, b]})


# =============================================================================
# MODULE 8 — Mixed <-> improper & mixed arithmetic
# =============================================================================

def module8():
    M = 8
    # (a) mixed -> improper
    to_imp = [
        ("Mixed to top-heavy", "2 3/4"),
        ("Write as improper", "3 1/5"),
        ("Top-heavy form", "1 5/6"),
        ("Improper please", "4 2/3"),
    ]
    for title, mixed in to_imp:
        f = F(mixed)
        whole = int(mixed.split()[0])
        fracpart = mixed.split()[1]
        d = int(fracpart.split("/")[1])
        n = int(fracpart.split("/")[0])
        imp = ff(f)  # improper (already not reducible normally)
        top = whole * d + n
        story = f"Write the mixed number {mixed} as an improper (top-heavy) fraction."
        st1 = stage(
            f"How many {d}ths are in the whole number {whole}?",
            f"Each whole is {d} of the {d}ths.",
            [
                opt(f"{whole} x {d} = {whole * d}", True,
                    f"Yes — {whole} wholes make {whole * d} {d}ths."),
                opt(f"{whole} + {d} = {whole + d}", False,
                    "Count how many parts fit in each whole — that is multiply, not add."),
                opt(f"{whole}", False,
                    "That counts the wholes, not how many small parts they contain."),
            ], key="wholes")
        st2 = stage(
            f"Now add the extra {fracpart}. What is the new top?",
            f"Total {d}ths = whole-{d}ths + {n}.",
            [
                opt(f"{whole * d} + {n} = {top}", True,
                    f"Right — {whole * d} + {n} = {top} {d}ths."),
                opt(f"{whole * d}", False,
                    f"Don't forget the extra {n} {d}ths from the fraction part."),
                opt(f"{whole} + {n} = {whole + n}", False,
                    "That added the whole and the top directly, skipping the part-count."),
            ], key="top")
        st3 = stage(
            "What is the improper fraction?",
            f"Put the total over {d}.",
            [
                opt(f"{top}/{d}", True,
                    f"Yes — {mixed} = {top}/{d}."),
                opt(f"{d}/{top}", False,
                    "That flips it — the total count goes on top, the part-size on the bottom."),
                opt(f"{top}/{whole}", False,
                    f"The bottom must stay the part-size {d}, not the whole number."),
            ], key="answer")
        item(M, title, story, f"{top}/{d}",
             [st1, st2, st3],
             worked=[
                 f"{whole} wholes = {whole} x {d} = {whole * d} {d}ths.",
                 f"Add the {n} extra {d}ths: {whole * d} + {n} = {top}.",
                 f"So {mixed} = {top}/{d}.",
             ],
             check=f"Back to mixed: {top}/{d} = {fm(f)}.",
             explain="A mixed number just groups improper {d}ths into wholes plus a leftover.".replace("{d}", str(d)),
             model={"type": "groups",
                    "caps": [d] * whole + [n],
                    "labels": [f"1 whole = {d}/{d}"] * whole + [f"the {fracpart} part"],
                    "target": f"{mixed} = how many {d}ths in all?",
                    "capLabel": f"{' + '.join([str(d)] * whole + [str(n)])} = {top}, so {top}/{d}"},
             verify={"op": "to_improper", "args": [mixed]})

    # (b) improper -> mixed  &  mixed addition
    to_mix = [
        ("Top-heavy to mixed", "11/4"),
        ("Share it out", "17/5"),
    ]
    for title, imp in to_mix:
        f = F(imp)
        n, d = int(imp.split("/")[0]), int(imp.split("/")[1])
        whole = n // d
        rem = n - whole * d
        mixedans = fm(f)
        story = f"Write the improper fraction {imp} as a mixed number."
        st1 = stage(
            f"How many whole groups of {d} fit into {n}?",
            f"Divide {n} by {d}.",
            [
                opt(f"{whole} (because {whole} x {d} = {whole * d})", True,
                    f"Yes — {d} fits into {n} exactly {whole} times."),
                opt(f"{d} ", False,
                    "That is the part-size, not how many whole groups fit."),
                opt(f"{n}", False,
                    "That is the whole top; we want how many groups of " + str(d) + " it holds."),
            ], key="wholes")
        st2 = stage(
            "What is left over after the whole groups?",
            f"Leftover = {n} - {whole} x {d}.",
            [
                opt(f"{rem} parts (so {rem}/{d})", True,
                    f"Right — {n} - {whole * d} = {rem}, giving {rem}/{d}."),
                opt("Nothing is left over", False,
                    f"{n} is not an exact multiple of {d}, so there is a remainder."),
                opt(f"{d - rem}/{d}", False,
                    "That is the part needed to reach the NEXT whole, not the leftover."),
            ], key="rem")
        st3 = stage(
            "What is the mixed number?",
            f"Whole part and the leftover fraction together.",
            [
                opt(f"{mixedans}", True,
                    f"Yes — {imp} = {mixedans}."),
                opt(f"{whole}/{rem}", False,
                    "Write it as whole number then a fraction, not as a new fraction."),
                opt(f"{rem} {whole}/{d}", False,
                    "The whole-number part and the fraction's top got swapped."),
            ], key="answer")
        item(M, title, story, mixedans,
             [st1, st2, st3],
             worked=[
                 f"{d} goes into {n} a total of {whole} times ({whole} x {d} = {whole * d}).",
                 f"Leftover: {n} - {whole * d} = {rem}, so {rem}/{d}.",
                 f"So {imp} = {mixedans}.",
             ],
             check=f"Back to improper: {mixedans} = {ff(f)}.",
             explain="An improper fraction packs leftover parts into whole groups plus a remainder.",
             model={"type": "groups",
                    "caps": [d] * whole + ([rem] if rem else []),
                    "labels": [f"group of {d}"] * whole + ([f"leftover {rem}/{d}"] if rem else []),
                    "target": f"{imp} = {whole} wholes + {rem}/{d}?",
                    "capLabel": f"{whole} x {d} + {rem} = {n}, so {mixedans}"},
             verify={"op": "to_mixed", "args": [imp]})

    # (c) adding mixed numbers
    add_mixed = [
        ("Add two mixed numbers", "1 1/2", "2 1/4"),
        ("Totalling lengths", "2 2/3", "1 1/6"),
    ]
    for title, a, b in add_mixed:
        fa, fb = F(a), F(b)
        res = fm(fa + fb)          # mixed, for teaching
        res_imp = ff(fa + fb)      # improper, the generator's `add` canonical form
        import math as _m
        d = fa.denominator * fb.denominator // _m.gcd(fa.denominator, fb.denominator)
        story = f"Add the mixed numbers {a} + {b}."
        st1 = stage(
            "What is a safe first step with mixed numbers?",
            "Either add wholes and fractions separately, or turn both improper.",
            [
                opt("Add the whole parts, then add the fraction parts", True,
                    "Yes — handle the wholes and the fraction pieces, then recombine."),
                opt("Add the whole of one to the fraction of the other", False,
                    "Keep like with like: wholes with wholes, parts with parts."),
                opt("Just add the top numbers and ignore the wholes", False,
                    "The whole numbers are real amounts — they can't be dropped."),
            ], key="plan")
        st2 = stage(
            f"Give the fraction parts a common bottom ({d}). What do they become?",
            "Match the part-sizes before adding the fraction pieces.",
            [
                opt(f"{ff(F(fa - int(a.split()[0])) )} and {ff(F(fb - int(b.split()[0])) )} -> common bottom {d}", True,
                    f"Right — rewrite both fraction parts over {d}, then add."),
                opt(f"Leave them as they are and add tops", False,
                    "Different bottoms must be matched first, just like unlike fractions."),
                opt(f"Multiply the fraction parts together", False,
                    "Adding means combining parts, not multiplying them."),
            ], key="common")
        st3 = stage(
            f"What is the total {a} + {b}?",
            "Add wholes, add the matched fraction parts, simplify.",
            [
                opt(f"{res} (that is {res_imp})", True,
                    f"Yes — the sum is {res}, which is {res_imp} as an improper fraction."),
                opt(f"{int(a.split()[0]) + int(b.split()[0])}", False,
                    "That added only the whole numbers and dropped the fraction parts."),
                opt(f"{fm(fa + fb + 1)}", False,
                    "That is one whole too many — re-add carefully."),
            ], key="answer")
        item(M, title, story, res_imp,
             [st1, st2, st3],
             worked=[
                 f"Wholes: {int(a.split()[0])} + {int(b.split()[0])} = {int(a.split()[0]) + int(b.split()[0])}.",
                 f"Fraction parts over {d}, then added.",
                 f"Total: {a} + {b} = {res} = {res_imp}.",
             ],
             check=f"As improper: {ff(fa)} + {ff(fb)} = {res_imp}.",
             explain="Mixed-number addition keeps wholes with wholes and matches the fraction part-sizes.",
             model={"type": "mapping",
                    "rows": [[a, ff(fa)], [b, ff(fb)], [f"{a} + {b}", f"{res} = {res_imp}"]]},
             verify={"op": "add", "args": [a, b]})


# =============================================================================
# MODULE 9 — Fraction OF a quantity & multiply/divide fractions
# =============================================================================

def module9():
    M = 9
    # (a) fraction OF a quantity
    of_rows = [
        ("Fraction of marbles", "2/3", "30", "marbles"),
        ("Of the pages", "3/4", "40", "pages"),
        ("Of the money", "5/8", "48", "rupees"),
    ]
    for title, frac, qty, unit in of_rows:
        f = F(frac)
        q = int(qty)
        res = ff(f * q)
        story = f"Find {frac} of {qty} {unit}. Remember: 'of' means multiply."
        st1 = stage(
            "What does the word 'of' tell us to do?",
            "'of' between a fraction and an amount means multiply.",
            [
                opt("Multiply the fraction by the amount", True,
                    "Yes — 'a fraction OF an amount' means fraction x amount."),
                opt("Add the fraction and the amount", False,
                    "'of' is not addition; it scales the amount by the fraction."),
                opt("Divide the amount by the top number", False,
                    "Dividing only by the top ignores how many parts we keep."),
            ], key="of")
        st2 = stage(
            f"What is one {f.denominator}th of {qty}?",
            f"Split {qty} into {f.denominator} equal groups.",
            [
                opt(f"{qty} / {f.denominator} = {ff(Fraction(q, f.denominator))}", True,
                    f"Right — one part is {qty} / {f.denominator} = {ff(Fraction(q, f.denominator))}."),
                opt(f"{qty} x {f.denominator} = {q * f.denominator}", False,
                    "To split into parts we divide by the bottom, not multiply."),
                opt(f"{qty} - {f.denominator} = {q - f.denominator}", False,
                    "Splitting is division, not subtraction."),
            ], key="onepart")
        st3 = stage(
            f"So what is {frac} of {qty}?",
            f"Take {f.numerator} of those parts.",
            [
                opt(f"{res}", True,
                    f"Yes — {f.numerator} parts of {ff(Fraction(q, f.denominator))} = {res} {unit}."),
                opt(f"{ff(Fraction(q, f.denominator))}", False,
                    f"That is only ONE part; we need {f.numerator} of them."),
                opt(f"{f.numerator * q}", False,
                    "That multiplied by the top but skipped dividing by the bottom — split into parts first."),
            ], key="answer")
        item(M, title, story, res,
             [st1, st2, st3],
             worked=[
                 f"'of' means multiply: {frac} x {qty}.",
                 f"One {f.denominator}th of {qty} is {qty} / {f.denominator} = {ff(Fraction(q, f.denominator))}.",
                 f"Take {f.numerator} of them: {res} {unit}.",
             ],
             check=f"({f.numerator}/{f.denominator}) x {qty} = {res}.",
             explain="A fraction OF a quantity scales the quantity — split into equal parts, then take the top-number of them.",
             model={"type": "parts", "total": f.denominator, "shaded": f.numerator,
                    "label": f"{frac} of {qty} = {res}"},
             verify={"op": "of", "args": [frac, qty]}, unit=unit)

    # (b) multiply two fractions
    mul_rows = [
        ("Multiply fractions", "2/3", "3/5"),
        ("Half of three-quarters", "1/2", "3/4"),
    ]
    for title, a, b in mul_rows:
        fa, fb = F(a), F(b)
        res = ff(fa * fb)
        story = f"Multiply {a} x {b}."
        st1 = stage(
            "How do we multiply two fractions?",
            "Top times top, bottom times bottom.",
            [
                opt("Multiply the tops together and the bottoms together", True,
                    "Yes — tops x tops over bottoms x bottoms."),
                opt("Find a common bottom first", False,
                    "Common bottoms are for adding; multiplying does not need them."),
                opt("Flip the second fraction and multiply", False,
                    "Flipping is for DIVISION, not multiplication."),
            ], key="rule")
        st2 = stage(
            f"What is {fa.numerator} x {fb.numerator} over {fa.denominator} x {fb.denominator}?",
            "Multiply straight across.",
            [
                opt(f"{fa.numerator * fb.numerator}/{fa.denominator * fb.denominator}", True,
                    f"Right — {fa.numerator * fb.numerator} over {fa.denominator * fb.denominator}."),
                opt(f"{fa.numerator + fb.numerator}/{fa.denominator + fb.denominator}", False,
                    "That added instead of multiplied the numbers."),
                opt(f"{fa.numerator * fb.numerator}/{fa.denominator}", False,
                    "That multiplied the tops but kept just one bottom; multiply the bottoms too."),
            ], key="across")
        st3 = stage(
            "Simplify to lowest terms. What is the answer?",
            "Divide out any common factor.",
            [
                opt(f"{res}", True,
                    f"Yes — {a} x {b} = {res}."),
                opt(f"{fa.numerator * fb.numerator}/{fa.denominator * fb.denominator}" if res != f"{fa.numerator*fb.numerator}/{fa.denominator*fb.denominator}" else f"{fa.numerator*fb.numerator+1}/{fa.denominator*fb.denominator}", False,
                    ("That is correct before simplifying — reduce it to lowest terms."
                     if res != f"{fa.numerator*fb.numerator}/{fa.denominator*fb.denominator}" else
                     "Multiply the tops again carefully.")),
                opt(f"{ff(fa + fb)}", False,
                    "That added the fractions instead of multiplying them."),
            ], key="answer")
        item(M, title, story, res,
             [st1, st2, st3],
             worked=[
                 f"Tops: {fa.numerator} x {fb.numerator} = {fa.numerator * fb.numerator}.",
                 f"Bottoms: {fa.denominator} x {fb.denominator} = {fa.denominator * fb.denominator}.",
                 f"So {a} x {b} = {ff(fa * fb)} = {res}.",
             ],
             check=f"{res} is already in lowest terms.",
             explain="Multiplying fractions means taking a part of a part — tops x tops, bottoms x bottoms.",
             model={"type": "mapping",
                    "rows": [
                        [f"{a} x {b}", "multiply straight across"],
                        [f"{fa.numerator}x{fb.numerator} / {fa.denominator}x{fb.denominator}",
                         f"{fa.numerator * fb.numerator}/{fa.denominator * fb.denominator}"],
                        ["lowest terms", res],
                    ]},
             verify={"op": "mul", "args": [a, b]})

    # (c) divide fractions (invert & multiply)
    div_rows = [
        ("Divide fractions", "3/4", "1/2"),
        ("How many halves?", "2/3", "1/6"),
        ("Share the ribbon", "5/6", "5/12"),
    ]
    for title, a, b in div_rows:
        fa, fb = F(a), F(b)
        res = ff(fa / fb)
        recip = ff(Fraction(fb.denominator, fb.numerator))
        story = f"Divide {a} / {b}. To divide, multiply by the reciprocal (flip the second fraction)."
        st1 = stage(
            f"What is the reciprocal of {b}?",
            "Flip the top and bottom of the fraction you divide BY.",
            [
                opt(f"{recip}", True,
                    f"Yes — flip {b} to get {recip}."),
                opt(f"{b}", False,
                    "Dividing needs the FLIPPED second fraction, not the same one."),
                opt(f"{ff(-fb)}", False,
                    "Reciprocal means flip, not change the sign."),
            ], key="reciprocal")
        st2 = stage(
            "What do we do after flipping the second fraction?",
            "Division becomes multiplication by the reciprocal.",
            [
                opt(f"Multiply: {a} x {recip}", True,
                    f"Right — {a} / {b} becomes {a} x {recip}."),
                opt(f"Still divide: {a} / {recip}", False,
                    "Once flipped, we MULTIPLY — the flip already handled the division."),
                opt(f"Add: {a} + {recip}", False,
                    "Division turns into multiplication by the reciprocal, not addition."),
            ], key="switch")
        st3 = stage(
            "What is the answer in lowest terms?",
            f"Multiply {a} x {recip} and simplify.",
            [
                opt(f"{res}", True,
                    f"Yes — {a} / {b} = {res}."),
                opt(f"{ff(fa * fb)}", False,
                    "That multiplied without flipping — remember to invert the divisor first."),
                opt(f"{ff(fb / fa)}", False,
                    "That flipped the wrong fraction; keep the first as it is."),
            ], key="answer")
        item(M, title, story, res,
             [st1, st2, st3],
             worked=[
                 f"Reciprocal of {b} is {recip}.",
                 f"{a} / {b} = {a} x {recip}.",
                 f"= {ff(fa / fb)} = {res}.",
             ],
             check=f"{res} x {b} = {ff(F(res) * fb)} = {a}.",
             explain="Dividing by a fraction asks 'how many of it fit?' — flip and multiply to count them.",
             model={"type": "mapping",
                    "rows": [
                        [f"{a} / {b}", "flip the divisor"],
                        [f"{a} x {recip}", "multiply by the reciprocal"],
                        ["answer", res],
                    ]},
             verify={"op": "mul", "args": [a, recip]})


# =============================================================================
# MODULE 10 — Averages, series & algebraic fraction equations (Stretch)
# =============================================================================

def module10():
    M = 10

    # (a) average of two fractions (real seed: avg of 1/2 and 1/6)
    avg_rows = [
        ("Average of two shares", "1/2", "1/6"),
        ("Midpoint fraction", "1/3", "1/5"),
        ("Average again", "3/4", "1/4"),
    ]
    for title, a, b in avg_rows:
        fa, fb = F(a), F(b)
        s = fa + fb
        avg = s / 2
        res = ff(avg)
        story = (f"Find the average of {a} and {b}. "
                 f"Average = add them, then divide by 2.")
        st1 = stage(
            "What is the first step to average two numbers?",
            "Add them together first.",
            [
                opt(f"Add them: {a} + {b} = {ff(s)}", True,
                    f"Yes — {a} + {b} = {ff(s)}."),
                opt(f"Multiply them: {a} x {b} = {ff(fa * fb)}", False,
                    "Averaging adds first, it does not multiply the two values."),
                opt(f"Subtract them: {a} - {b} = {ff(fa - fb)}", False,
                    "The difference is not the average — we add, then halve."),
            ], key="add")
        st2 = stage(
            "What do we do with the sum to get the average?",
            "Divide the sum by 2 (because there are 2 numbers).",
            [
                opt("Divide the sum by 2 (multiply by 1/2)", True,
                    "Right — two numbers, so split the total into 2 equal shares."),
                opt("Divide the sum by the two bottom numbers", False,
                    "We divide by how MANY numbers there are (2), not by the denominators."),
                opt("Leave the sum as the answer", False,
                    "The sum is a total; the average shares it between the two numbers."),
            ], key="halve")
        st3 = stage(
            "What is the average?",
            f"({ff(s)}) x 1/2.",
            [
                opt(f"{res}", True,
                    f"Yes — ({ff(s)}) / 2 = {res}."),
                opt(f"{ff(s)}", False,
                    "That is the sum, not yet halved."),
                opt(f"{ff(fa * fb)}", False,
                    "That is the product; averaging uses the sum, then halves."),
            ], key="answer")
        item(M, title, story, res,
             [st1, st2, st3],
             worked=[
                 f"Add: {a} + {b} = {ff(s)}.",
                 f"Divide by 2 (there are 2 numbers): {ff(s)} x 1/2 = {res}.",
             ],
             check=f"{res} sits exactly between {a} and {b}.",
             explain="An average of two values is their total shared equally between the two.",
             model={"type": "mapping",
                    "rows": [
                        ["add", f"{a} + {b} = {ff(s)}"],
                        ["halve", f"{ff(s)} / 2 = {res}"],
                        ["average", res],
                    ]},
             verify={"op": "mul", "args": [ff(s), "1/2"]})

    # (b) fraction series / nth term (real seed: 1/6,1/4,1/3,5/12,... 10th term)
    #   The pattern: numerators of n/12 reduced. term_k = k+1 over 12 (reduced).
    #   1/6=2/12, 1/4=3/12, 1/3=4/12, 5/12=5/12 -> term_k = (k+1)/12.
    series_rows = [
        ("Tenth term of a series", [F("1/6"), F("1/4"), F("1/3"), F("5/12")], 10, 12, lambda k: Fraction(k + 1, 12)),
        ("Pattern of fifths", [F("2/5"), F("3/5"), F("4/5"), F("1")], 6, 5, lambda k: Fraction(k + 1, 5)),
    ]
    for title, shown, n, base, termfn in series_rows:
        res = ff(termfn(n))
        shown_str = ", ".join(ff(x) for x in shown)
        unreduced = ", ".join(f"{i + 2}/{base}" for i in range(len(shown)))
        st1 = stage(
            "What hidden pattern links these terms?",
            "Rewrite each with the same bottom to see the tops count up.",
            [
                opt(f"Each has bottom {base}: the series is {unreduced}, ... (tops go up by 1)", True,
                    f"Yes — written over {base}, the tops are {', '.join(str(i + 2) for i in range(len(shown)))}, ... counting up by 1."),
                opt("The fractions are doubling each time", False,
                    "Check by matching bottoms — the tops rise by 1, they do not double."),
                opt("There is no pattern", False,
                    "Rewrite over a common bottom and the steady pattern appears."),
            ], key="pattern")
        st2 = stage(
            f"Over the common bottom {base}, what is the top of the {n}th term?",
            "The 1st top is 2, so the kth top is k + 1.",
            [
                opt(f"{n + 1} (top = position + 1)", True,
                    f"Right — the {n}th top is {n} + 1 = {n + 1}."),
                opt(f"{n}", False,
                    "The tops start at 2, not 1, so the nth top is n + 1."),
                opt(f"{n * 2}", False,
                    "The tops rise by 1 each time, not by doubling."),
            ], key="nthtop")
        st3 = stage(
            f"So what is the {n}th term, in lowest terms?",
            f"{n + 1}/{base}, then simplify.",
            [
                opt(f"{res}", True,
                    f"Yes — {n + 1}/{base} = {res}."),
                opt(f"{n + 1}/{base}" if res != f"{n + 1}/{base}" else f"{n}/{base}", False,
                    ("That is correct before simplifying — reduce to lowest terms."
                     if res != f"{n + 1}/{base}" else
                     "Recount the position: the nth top is n + 1.")),
                opt(f"{base}/{n + 1}", False,
                    "That flipped the fraction; the counted top goes on top."),
            ], key="answer")
        item(M, title,
             f"A series runs {shown_str}, ... Find the {n}th term. Look for a common bottom.",
             res, [st1, st2, st3],
             worked=[
                 f"Rewrite over {base}: {unreduced}, ...",
                 f"The tops are 2, 3, 4, ... so the kth top is k + 1.",
                 f"The {n}th term is {n + 1}/{base} = {res}.",
             ],
             check=f"Position {n} -> top {n + 1} over {base}.",
             explain="A fraction series hides a steady pattern once every term shares one bottom.",
             model={"type": "mapping", "rows": [[str(i + 1), f"{i + 2}/{base}"] for i in range(len(shown))] + [[str(n), res]]},
             verify={"op": "simplify", "args": [f"{n + 1}/{base}"]})

    # (c) algebraic fraction equations (real seed: Q/4 + Q/6 = Q/12 + 15)
    #   Solve for Q. answer is an integer.
    #   Q/4 + Q/6 - Q/12 = 15 ; LCD 12 -> 3Q + 2Q - Q = 180 -> 4Q = 180 -> Q = 45.
    def solve_eq1():
        # coefficients as fractions of Q on left minus right = const
        # (1/4 + 1/6 - 1/12) Q = 15
        coeff = Fraction(1, 4) + Fraction(1, 6) - Fraction(1, 12)
        Q = Fraction(15) / coeff
        return coeff, Q

    coeff, Q = solve_eq1()
    story = "Solve for Q: Q/4 + Q/6 = Q/12 + 15. Clear the fractions first."
    st1 = stage(
        "What common bottom clears all the fractions in Q/4, Q/6, Q/12?",
        "Smallest number that 4, 6 and 12 all divide into.",
        [
            opt("12", True,
                "Yes — 4, 6 and 12 all divide into 12, so multiply every term by 12."),
            opt("22 (add the bottoms)", False,
                "Adding the bottoms does not give a common multiple; use the LCM, 12."),
            opt("48 (multiply all bottoms)", False,
                "48 works but is not the LEAST — 12 is smaller and cleaner."),
        ], key="lcd")
    st2 = stage(
        "Multiply every term by 12. What does the equation become?",
        "12 x Q/4 = 3Q, 12 x Q/6 = 2Q, 12 x Q/12 = Q, 12 x 15 = 180.",
        [
            opt("3Q + 2Q = Q + 180", True,
                "Right — each term scales: 3Q + 2Q = Q + 180."),
            opt("4Q + 6Q = 12Q + 180", False,
                "Multiplying by 12 DIVIDES out each bottom; you do not multiply by the bottoms."),
            opt("Q + Q = Q + 180", False,
                "Each term scales by 12/bottom, giving 3Q, 2Q and Q, not plain Q."),
        ], key="clear")
    st3 = stage(
        "Solve 3Q + 2Q = Q + 180 for Q.",
        "Combine the Q terms, then isolate Q.",
        [
            opt(f"Q = {ff(Q)}", True,
                f"Yes — 5Q - Q = 180, so 4Q = 180 and Q = {ff(Q)}."),
            opt("Q = 90", False,
                "Check: 5Q - Q = 4Q = 180 gives Q = 45, not 90."),
            opt("Q = 36", False,
                "Recombine: 3Q + 2Q = 5Q, then subtract Q to get 4Q = 180."),
        ], key="answer")
    item(M, "Solve a fraction equation", story, ff(Q),
         [st1, st2, st3],
         worked=[
             "Multiply every term by the common bottom 12.",
             "3Q + 2Q = Q + 180.",
             "5Q - Q = 180, so 4Q = 180.",
             f"Q = 180 / 4 = {ff(Q)}.",
         ],
         check=f"Check: {ff(Q)}/4 + {ff(Q)}/6 = {ff(F(ff(Q)) / 4 + F(ff(Q)) / 6)}, and {ff(Q)}/12 + 15 = {ff(F(ff(Q)) / 12 + 15)}.",
         explain="Clearing fractions turns a messy fraction equation into a simple whole-number one.",
         model={"type": "mapping",
                "rows": [
                    ["equation", "Q/4 + Q/6 = Q/12 + 15"],
                    ["x12 (clear)", "3Q + 2Q = Q + 180"],
                    ["solve", f"4Q = 180, Q = {ff(Q)}"],
                ]},
         verify={"op": "simplify", "args": [ff(Q)]})

    # second algebraic one: simpler, "Q/2 + Q/3 = 20" -> (5/6)Q = 20 -> Q = 24
    coeff2 = Fraction(1, 2) + Fraction(1, 3)
    Q2 = Fraction(20) / coeff2
    story2 = "Solve for Q: Q/2 + Q/3 = 20."
    s1 = stage(
        "What common bottom clears Q/2 and Q/3?",
        "Smallest number both 2 and 3 divide into.",
        [
            opt("6", True, "Yes — 2 and 3 both divide into 6."),
            opt("5 (add the bottoms)", False, "Adding bottoms is not a common multiple; use 6."),
            opt("1", False, "1 does not clear the fractions; you need the LCM of 2 and 3."),
        ], key="lcd")
    s2 = stage(
        "Multiply every term by 6. What results?",
        "6 x Q/2 = 3Q, 6 x Q/3 = 2Q, 6 x 20 = 120.",
        [
            opt("3Q + 2Q = 120", True, "Right — 3Q + 2Q = 120."),
            opt("2Q + 3Q = 20", False, "The 20 also scales by 6, becoming 120."),
            opt("Q + Q = 120", False, "The terms scale to 3Q and 2Q, not plain Q."),
        ], key="clear")
    s3 = stage(
        "Solve 3Q + 2Q = 120.",
        "Combine, then divide.",
        [
            opt(f"Q = {ff(Q2)}", True, f"Yes — 5Q = 120, so Q = {ff(Q2)}."),
            opt("Q = 40", False, "5Q = 120 gives Q = 24, not 40."),
            opt("Q = 60", False, "Combine 3Q + 2Q = 5Q, then divide 120 by 5."),
        ], key="answer")
    item(M, "Another fraction equation", story2, ff(Q2),
         [s1, s2, s3],
         worked=[
             "Multiply every term by 6: 3Q + 2Q = 120.",
             "5Q = 120.",
             f"Q = 120 / 5 = {ff(Q2)}.",
         ],
         check=f"Check: {ff(Q2)}/2 + {ff(Q2)}/3 = {ff(F(ff(Q2)) / 2 + F(ff(Q2)) / 3)}.",
         explain="The same 'clear the fractions' move solves any Q-over-number equation.",
         model={"type": "mapping",
                "rows": [
                    ["equation", "Q/2 + Q/3 = 20"],
                    ["x6 (clear)", "3Q + 2Q = 120"],
                    ["solve", f"5Q = 120, Q = {ff(Q2)}"],
                ]},
         verify={"op": "simplify", "args": [ff(Q2)]})


# =============================================================================
# modules metadata
# =============================================================================

MODULES = [
    {
        "id": 1, "title": "Name the whole", "level": "Core",
        "desc": "Identify what one whole stands for, then find a fractional share of it.",
        "rule": "A fraction is a share of a named whole: split into equal parts, take the top-number of them.",
        "teach": [
            "Always start by naming the whole: '1 (the whole) is all 30 marbles / 40 children / 60 pages'.",
            "The bottom number cuts the whole into equal parts; the top number counts how many you take.",
            "part = (top/bottom) x whole.",
        ],
        "contrast": ["1/3 of 30 = 10.", "1/3 of 60 = 20.", "Same share, different whole, different amount."],
        "transfer": "Write two stories where 1/4 of the whole is 10. What must the whole be in each?",
    },
    {
        "id": 2, "title": "Part & complement from a figure", "level": "Core",
        "desc": "Read a shaded figure: name the whole, the shaded part, and the plain complement.",
        "rule": "In a figure the bottom number is the count of equal parts; shaded + plain = 1.",
        "teach": [
            "Count every equal part to get the bottom number.",
            "Count the shaded parts to get the top number.",
            "The complement is the whole minus the shaded part.",
        ],
        "contrast": ["3 shaded of 8 -> 3/8 shaded, 5/8 plain.", "They add back to 8/8 = 1."],
        "transfer": "Shade a strip so the plain part is 2/5. How many of 5 parts stay shaded?",
    },
    {
        "id": 3, "title": "Equivalent fractions & odd-one-out", "level": "Core",
        "desc": "Build equal fractions by scaling both numbers, and spot the fraction that does not belong.",
        "rule": "Multiply or divide top and bottom by the SAME number to keep the share equal.",
        "teach": [
            "Scaling both numbers by the same factor does not change the share.",
            "To test if fractions are equal, reduce each to lowest terms.",
            "The odd one out reduces to a different lowest-terms fraction.",
        ],
        "contrast": ["2/3 = 4/6 = 6/9.", "8/16 = 1/2, which is the stranger among thirds."],
        "transfer": "Write three fractions equal to 3/4, then one that only looks similar but isn't.",
    },
    {
        "id": 4, "title": "Lowest terms via GCD", "level": "Core",
        "desc": "Simplify a fraction by dividing top and bottom by their greatest common factor.",
        "rule": "Lowest terms: divide out the GCF until top and bottom share no factor above 1.",
        "teach": [
            "Find the greatest common factor of the top and bottom.",
            "Divide BOTH by it in one clean step.",
            "Stop when the only shared factor is 1.",
        ],
        "contrast": ["18/24 -> divide by 6 -> 3/4.", "Dividing only by 2 would leave 9/12, not finished."],
        "transfer": "Simplify 20/50 two ways: dividing by 2 then 5, or by 10 at once.",
    },
    {
        "id": 5, "title": "Compare & order fractions", "level": "Core",
        "desc": "Compare fractions by matching denominators; beware 'bigger bottom = bigger'.",
        "rule": "Give a common bottom, then the bigger top wins.",
        "teach": [
            "Unlike bottoms mean unlike part-sizes — match them first.",
            "A bigger bottom means SMALLER parts, not a bigger fraction.",
            "With equal bottoms, compare the tops.",
        ],
        "contrast": ["1/5 vs 1/7: fifths are bigger, so 1/5 > 1/7.", "The bigger bottom is the smaller share."],
        "transfer": "Order 2/3, 3/4, 5/6 from smallest to largest using bottom 12.",
    },
    {
        "id": 6, "title": "Add & subtract like fractions", "level": "Core",
        "desc": "Combine fractions that already share a bottom by working only on the tops.",
        "rule": "Same bottom: add or subtract the tops, keep the bottom, then simplify.",
        "teach": [
            "Equal bottoms mean equal-size parts you can count together.",
            "Combine the tops; the bottom never changes.",
            "Simplify the result to lowest terms.",
        ],
        "contrast": ["3/5 + 2/5 = 5/5 = 1.", "Writing 5/10 would wrongly add the bottoms."],
        "transfer": "Find two eighths that add to exactly 1.",
    },
    {
        "id": 7, "title": "Add & subtract unlike fractions", "level": "Stretch",
        "desc": "Combine fractions with different bottoms by first finding the least common denominator.",
        "rule": "Unlike bottoms: rewrite over the LCD, then combine the tops.",
        "teach": [
            "Different bottoms must be matched before combining.",
            "Use the least common multiple of the bottoms as the LCD.",
            "Never add tops and bottoms separately.",
        ],
        "contrast": ["1/2 + 1/3 = 3/6 + 2/6 = 5/6.", "2/5 is NOT the answer — that adds tops and bottoms."],
        "transfer": "Add 1/4 + 1/6 by first finding the LCD of 4 and 6.",
    },
    {
        "id": 8, "title": "Mixed and improper fractions", "level": "Stretch",
        "desc": "Convert between mixed numbers and improper fractions and add mixed numbers.",
        "rule": "Improper top = whole x bottom + part-top; mixed = whole groups + leftover.",
        "teach": [
            "Mixed to improper: wholes x bottom, add the part-top, keep the bottom.",
            "Improper to mixed: divide top by bottom for the whole, remainder over the bottom.",
            "Add mixed numbers by matching fraction bottoms, then combining wholes and parts.",
        ],
        "contrast": ["2 3/4 = 11/4.", "11/4 = 2 3/4, since 4 goes into 11 twice with 3 left."],
        "transfer": "Turn 17/5 into a mixed number, then back again.",
    },
    {
        "id": 9, "title": "Fraction of a quantity, multiply & divide", "level": "Stretch",
        "desc": "Use 'of' = multiply, multiply fractions straight across, and divide by flipping.",
        "rule": "'of' and 'x' both multiply; to divide, multiply by the reciprocal.",
        "teach": [
            "'A fraction OF an amount' means fraction x amount.",
            "Multiply fractions: tops x tops over bottoms x bottoms.",
            "Divide fractions: flip the divisor and multiply.",
        ],
        "contrast": ["2/3 of 30 = 20.", "3/4 / 1/2 = 3/4 x 2 = 3/2 — flip, don't forget."],
        "transfer": "Work out 1/2 of 3/4 two ways: as 'of' and as multiply.",
    },
    {
        "id": 10, "title": "Averages, series & fraction equations", "level": "Stretch",
        "desc": "Average fractions, find the nth term of a fraction series, and solve Q-over-number equations.",
        "rule": "Average = sum / count; a series hides a steady pattern; clear fractions to solve for Q.",
        "teach": [
            "Average of fractions: add them, then divide by how many there are.",
            "A fraction series becomes clear once every term shares one bottom.",
            "Solve fraction equations by multiplying every term by the common bottom.",
        ],
        "contrast": ["Average of 1/2 and 1/6 = (2/3) / 2 = 1/3.", "Q/2 + Q/3 = 20 -> 3Q + 2Q = 120 -> Q = 24."],
        "transfer": "Solve Q/4 + Q/6 = Q/12 + 15 by clearing with bottom 12.",
    },
]


def build_source():
    module1(); module2(); module3(); module4(); module5()
    module6(); module7(); module8(); module9(); module10()
    return {
        "slug": "fractions-g6",
        "title": "Fraction Sense \u00b7 Grade 6",
        "concept": "Fractions",
        "gradeRange": [6, 6],
        "modules": MODULES,
        "questions": QUESTIONS,
    }


def main():
    src = build_source()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(src, f, ensure_ascii=False, indent=2)
        f.write("\n")
    n_items = len(src["questions"])
    n_verify = sum(1 for q in src["questions"] if q.get("verify"))
    print(f"wrote {OUT}")
    print(f"  {len(src['modules'])} modules, {n_items} items, {n_verify} with verify spec")


if __name__ == "__main__":
    main()
