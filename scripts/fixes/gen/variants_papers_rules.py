"""Rules for generated variants, part 1: thin solutions (HCF, ratio, proportion, area and perimeter).

Each rule takes a question and returns None (wording does not match), or a fix dict; it raises Skip
when the wording matches but the question must be left alone.
"""
import math
import re

from variants_papers_util import Skip, factors, listing, make_steps, matches, need_key, pick, prime_factors, step_texts


def rule_hcf(q):
    m = matches(q, r"Find the HCF of (\d+) and (\d+)\.")
    if not m:
        return None
    old = step_texts(q)
    if not (len(old) == 2 and re.fullmatch(r"Find factors of \d+ and \d+\.", old[0]) and re.fullmatch(r"HCF = \d+", old[1])):
        return None
    a, b = int(m.group(1)), int(m.group(2))
    h = math.gcd(a, b)
    need_key(q, h)
    fa, fb = factors(a), factors(b)
    if len(fa) <= 10 and len(fb) <= 10:
        common = [f for f in fa if f in fb]
        third = ("The only factor in both lists is 1." if common == [1]
                 else "The factors in both lists are %s. The largest of them is %d." % (listing(common), h))
        texts = [
            "List the factors of %d: %s." % (a, listing(fa)),
            "List the factors of %d: %s." % (b, listing(fb)),
            third,
            "So the HCF of %d and %d is %d." % (a, b, h),
        ]
    else:
        pa, pb = prime_factors(a), prime_factors(b)

        def product(n, ps):
            return "%d is itself a prime number" % n if len(ps) == 1 else "%d = %s" % (n, " × ".join(map(str, ps)))

        shared, rest = [], list(pb)
        for p in pa:
            if p in rest:
                shared.append(p)
                rest.remove(p)
        first = "Break each number into prime factors: %s, and %s." % (product(a, pa), product(b, pb))
        if not shared:
            texts = [first, "The two numbers share no prime factor, so the only number that divides both is 1.",
                     "So the HCF of %d and %d is 1." % (a, b)]
        elif len(shared) == 1:
            texts = [first, "The only prime factor they share is %d." % h, "So the HCF of %d and %d is %d." % (a, b, h)]
        else:
            texts = [first,
                     "Pick out the prime factors that appear in both: %s." % listing(shared),
                     "Multiply them: %s = %d." % (" × ".join(map(str, shared)), h),
                     "So the HCF of %d and %d is %d." % (a, b, h)]
    return {"steps": make_steps(q, texts), "why": "Both steps said nothing: no factors listed, only 'HCF = N'."}


def rule_ratio_share(q):
    if step_texts(q)[:1] != ["Identify the ratio parts and total."]:
        return None
    m = matches(q, r"(\w+) has (\d+) (\w+) and divides them in the ratio (\d+):(\d+)\. How many (\w+) are in the larger group\?")
    if m:
        total, noun, a, b = int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
        want, label = max(a, b), "larger group"
        if noun != m.group(6):
            raise Skip("two different nouns")
        ending = "So the larger group has %%d %s." % noun
    else:
        m = matches(q, r"Divide (\d+) in the ratio (\d+):(\d+)\. What is the smaller share\?")
        if not m:
            return None
        total, a, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        want, label, noun = min(a, b), "smaller share", ""
        ending = "So the smaller share is %d."
    parts = a + b
    if a == b or total % parts:
        raise Skip("the shares are equal or not whole")
    one = total // parts
    ans = want * one
    need_key(q, ans)
    texts = [
        "Add the ratio parts: %d + %d = %d equal parts in all." % (a, b, parts),
        "Find the size of one part: %d ÷ %d = %d." % (total, parts, one),
        "The %s is %d of these parts: %d × %d = %d." % (label, want, want, one, ans),
        ending % ans,
    ]
    return {"steps": make_steps(q, texts), "why": "Both steps said nothing ('Identify the ratio parts and total', 'Compute the answer')."}


PROPORTION_EXAMPLES = [
    "Try a smaller one: if 1 : 4 = 3 : x, the first term 1 was multiplied by 3 to make 3. Do the same to the second term: x = 4 × 3 = 12.",
    "Try a smaller one: if 2 : 3 = 4 : x, the first term 2 was multiplied by 2 to make 4. Do the same to the second term: x = 3 × 2 = 6.",
    "Try a smaller one: if 1 : 5 = 2 : x, the first term 1 was multiplied by 2 to make 2. Do the same to the second term: x = 5 × 2 = 10.",
]


def rule_proportion(q):
    m = matches(q, r"If (\d+) : (\d+) = (\d+) : x, find x\.")
    if not m:
        return None
    a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if c % a or c == a:
        raise Skip("the first terms are not a whole multiple apart")
    k = c // a
    x = b * k
    need_key(q, x)
    hints = [
        "The two ratios are equal. Whatever the first term was multiplied by, the second term must be multiplied by the same number.",
        "Look at the first terms: what do you multiply %d by to get %d? Then do the same to %d." % (a, c, b),
        pick(q, PROPORTION_EXAMPLES),
    ]
    texts = [
        "In a proportion the two ratios are equal, so both terms of %d : %d are multiplied by the same number." % (a, b),
        "Compare the first terms: %d ÷ %d = %d, so the first term was multiplied by %d." % (c, a, k, k),
        "Multiply the second term by %d as well: %d × %d = %d." % (k, b, k, x),
        "So x = %d." % x,
    ]
    return {"hints": hints, "steps": make_steps(q, texts),
            "why": "Hints were for sharing in a ratio ('Sum the ratio parts'), which does not apply to a proportion; both steps said nothing."}


SHAPE_EXAMPLES = {
    ("area", "rectangle"): [
        "Try a smaller one: a rectangle 5 cm long and 3 cm wide has an area of 5 × 3 = 15 sq.cm.",
        "Try a smaller one: a rectangle 4 cm long and 2 cm wide has an area of 4 × 2 = 8 sq.cm.",
        "Try a smaller one: a rectangle 7 cm long and 3 cm wide has an area of 7 × 3 = 21 sq.cm.",
    ],
    ("area", "square"): [
        "Try a smaller one: a square with side 4 cm has an area of 4 × 4 = 16 sq.cm.",
        "Try a smaller one: a square with side 3 cm has an area of 3 × 3 = 9 sq.cm.",
        "Try a smaller one: a square with side 6 cm has an area of 6 × 6 = 36 sq.cm.",
    ],
    ("perimeter", "rectangle"): [
        "Try a smaller one: a rectangle 5 cm long and 2 cm wide has a perimeter of 2 × (5 + 2) = 14 cm.",
        "Try a smaller one: a rectangle 4 cm long and 1 cm wide has a perimeter of 2 × (4 + 1) = 10 cm.",
        "Try a smaller one: a rectangle 8 cm long and 3 cm wide has a perimeter of 2 × (8 + 3) = 22 cm.",
    ],
    ("perimeter", "square"): [
        "Try a smaller one: a square with side 3 cm has a perimeter of 4 × 3 = 12 cm.",
        "Try a smaller one: a square with side 5 cm has a perimeter of 4 × 5 = 20 cm.",
        "Try a smaller one: a square with side 7 cm has a perimeter of 4 × 7 = 28 cm.",
    ],
}


def rule_area_perimeter(q):
    old = step_texts(q)
    if not (len(old) == 2 and old[0].startswith("Use the formula for") and old[1].startswith("Answer = ")):
        return None
    m = matches(q, r"Find the (area|perimeter) of a rectangle with length (\d+) cm and width (\d+) cm\.")
    if m:
        what, shape, l, w = m.group(1), "rectangle", int(m.group(2)), int(m.group(3))
    else:
        m = matches(q, r"Find the (area|perimeter) of a square with side (\d+) cm\.")
        if not m:
            return None
        what, shape, l = m.group(1), "square", int(m.group(2))
        w = l
    example = pick(q, SHAPE_EXAMPLES[(what, shape)], avoid=[l, w])
    if what == "area":
        ans = l * w
        unit = "sq.cm"
        if shape == "rectangle":
            hints = ["Area is the space inside the shape. For a rectangle, area = length × width.",
                     "Multiply the length, %d cm, by the width, %d cm." % (l, w), example]
            texts = ["Area of a rectangle = length × width.",
                     "Put in the numbers: %d × %d = %d." % (l, w, ans),
                     "So the area is %d sq.cm." % ans]
        else:
            hints = ["Area is the space inside the shape. For a square, area = side × side.",
                     "Every side is %d cm, so multiply %d by itself." % (l, l), example]
            texts = ["Area of a square = side × side.",
                     "Put in the numbers: %d × %d = %d." % (l, l, ans),
                     "So the area is %d sq.cm." % ans]
    else:
        unit = "cm"
        if shape == "rectangle":
            ans = 2 * (l + w)
            hints = ["Perimeter is the distance all the way round. A rectangle has two lengths and two widths.",
                     "Add the length and the width first: %d + %d. Then double it, because each appears twice." % (l, w), example]
            texts = ["Perimeter of a rectangle = 2 × (length + width).",
                     "Add the length and the width: %d + %d = %d." % (l, w, l + w),
                     "Double it: 2 × %d = %d." % (l + w, ans),
                     "So the perimeter is %d cm." % ans]
        else:
            ans = 4 * l
            hints = ["Perimeter is the distance all the way round. A square has 4 equal sides.",
                     "Each side is %d cm, and there are 4 of them. Multiply." % l, example]
            texts = ["Perimeter of a square = 4 × side, because all 4 sides are equal.",
                     "Put in the number: 4 × %d = %d." % (l, ans),
                     "So the perimeter is %d cm." % ans]
    need_key(q, ans)
    if not old[1].endswith(" " + unit):
        raise Skip("unit differs from the old solution")
    return {"hints": hints, "steps": make_steps(q, texts),
            "why": "Hints were a bare formula plus 'Plug in the given values'; steps said only 'Use the formula' and 'Answer = N'."}


RULES = [
    ("hcf-thin-steps", rule_hcf),
    ("ratio-share-thin-steps", rule_ratio_share),
    ("proportion-hints-and-steps", rule_proportion),
    ("area-perimeter-thin", rule_area_perimeter),
]
