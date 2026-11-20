"""gr4_numbers, written per question: Roman numerals (writing and reading a numeral)."""
from g4_gr4_numbers_lib import A, FIG, G, Q, U, W, b, table

L = {}

LETTERS = table(["M", "D", "C", "L", "X"], [[1000, 500, 100, 50, 10]], note="and V = 5, I = 1")

_ROMAN = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
          (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def to_roman(n):
    out = ""
    for v, r in _ROMAN:
        while n >= v:
            out += r
            n -= v
    return out


def spell(r):
    return " ".join(r)


def explain(v):
    """One spoken sentence on how a place part (like 900, 80, 6) is written."""
    r = to_roman(v)
    base = 1
    while base * 10 <= v:
        base *= 10
    d = v // base
    unit = {1: "", 10: " tens", 100: " hundreds", 1000: " thousands"}[base]
    one = {1: "", 10: " ten", 100: " hundred", 1000: " thousand"}[base]
    if d in (4, 9):
        return "%d is %d less than %d, so the smaller letter goes in front: %s." % (v, base, (d + 1) * base, spell(r))
    if d == 1:
        return "%d is simply %s." % (v, r)
    if d == 5:
        return "%d is simply %s." % (v, r)
    if d in (2, 3):
        return "%d is %d lots of %d, so we write %s." % (v, d, base, spell(r))
    more = d - 5
    return "%d is %d and %d more%s, so we write %s." % (v, 5 * base, more, one if more == 1 else unit, spell(r))


def roman_write(n, key, wrong, ifnot, trap):
    """Lesson for 'write n in Roman numerals'. `key` is the part the child is asked about."""
    parts = []
    for i, ch in enumerate(str(n)):
        v = int(ch) * 10 ** (len(str(n)) - 1 - i)
        if v:
            parts.append(v)
    ans = "".join(to_roman(v) for v in parts)
    assert ans == to_roman(n)
    said = ", ".join(str(v) for v in parts[:-1]) + " and %d" % parts[-1]
    beats = [
        b("We need to write %d the Roman way. Romans had no place seats like ours, so first we break the number into parts." % n,
          G("%d in Roman numerals = ?" % n)),
        b("Split it by place: %s." % said, W("%d = %s" % (n, " + ".join(str(v) for v in parts)))),
        b("Here are the 7 Roman letters and what each one is worth. Keep them in view.", FIG(LETTERS)),
    ]
    rest = []

    def flush():
        while rest:
            two = rest[:2]
            del rest[:2]
            say = " ".join(explain(v) for v in two)
            if len(say) > 230:
                rest.insert(0, two[1])
                two = two[:1]
                say = explain(two[0])
            beats.append(b(say, *[W("%d = %s" % (v, to_roman(v))) for v in two]))

    for v in parts:
        if v == key:
            flush()
            beats.append(b("Now the %d. How do the Romans write %d?" % (v, v), Q([to_roman(v)] + wrong, ifnot)))
            beats.append(b(explain(v), W("%d = %s" % (v, to_roman(v)))))
        else:
            rest.append(v)
    flush()
    beats.append(b("Now join the parts in order, biggest first: %s." % ", ".join(spell(to_roman(v)) for v in parts), A(ans)))
    beats.append(trap if isinstance(trap, tuple) else b(trap))
    beats.append(b("So the plan for any number: split it by place, write each part in Roman letters, then join them from left to right."))
    return beats


L["EXT_G4_FP_2020_027"] = roman_write(
    1945, 900, ["MC", "DCCCC"],
    "C in front of M takes 100 away from 1000, which leaves 900. C after M would add 100 on instead.",
    b("Careful with the tens as well. X before L is 40. Turn them round to L X and you have made 60.", W("XL = 40     LX = 60")))

L["EXT_G4_FP_2021_007"] = roman_write(
    1946, 40, ["XXXX", "LX"],
    "A letter is never written 4 times in a row. So for 40 we think 10 less than 50, and write X before L.",
    "Order matters too. The 1000 comes first, so the numeral starts with M, and only then C M for the 900.")

L["PYQ_2016_Q33"] = roman_write(
    1946, 900, ["MC", "DCCCC"],
    "C in front of M takes 100 away from 1000, which leaves 900. C after M would add 100 on instead.",
    b("Check the tens carefully. X X X is only 30. For 40 we need X L.", W("XXX = 30     XL = 40")))

L["EXT_G4_FP_2023_004"] = roman_write(
    2349, 40, ["LX", "XXXX"],
    "X before L means 10 less than 50, which is 40. And a letter is never written 4 times in a row.",
    "And notice the 300. It is simply three Cs. The take away trick is only for the 4s and the 9s.")

L["EXT_G4_FP_2024_020"] = roman_write(
    1896, 90, ["LXXXX", "CX"],
    "90 is 10 less than 100, so the X goes in front of the C. A letter is never written 4 times in a row.",
    b("Watch the last part too. V I is 6, but I V is 4. One letter out of place changes the number.", W("VI = 6     IV = 4")))

L["PYQ_2018_Q32"] = roman_write(
    1789, 700, ["CCD", "CCCCCCC"],
    "700 is 500 and 2 more hundreds. The big letter D comes first, and then the two Cs.",
    "The trap here is to write each digit on its own: 1, 7, 8, 9. Roman numerals show the full value of each part, like 1000 and 700.")

L["PYQ_2019_Q23"] = roman_write(
    1997, 90, ["LXXXX", "CX"],
    "A letter can repeat only 3 times, so L X X X X is not allowed. 90 is 10 less than 100: X before C.",
    "The same rule made our 900. Not D C C C C, but C before M. Short and neat.")

L["Q_CH01_005"] = roman_write(
    789, 80, ["LXX", "XC"],
    "80 is 50 and 3 more tens. So we write L, and then three Xs.",
    b("Count the Xs carefully. L X X is only 70, and X C is 90.", W("LXX = 70     XC = 90")))


# ── Reading a numeral ────────────────────────────────────────────────────────

L["Q_CH01_004"] = [
    b("Here is a Roman numeral: C D X L I V. We need to turn it into our own numbers.", G("CDXLIV = ?", name="g")),
    b("Here is what each Roman letter is worth.", FIG(LETTERS)),
    b("The secret: when a smaller letter stands before a bigger one, we take it away. This numeral is made of 3 pairs like that.",
      U("CD", on="g"), U("XL", on="g"), U("IV", on="g")),
    b("Take the first pair. C is 100 and D is 500, and the C comes first. So what is C D worth?",
      Q(["400", "600", "500"], "The smaller letter is in front, so we take it away: 500 minus 100 is 400.")),
    b("500 minus 100 is 400. So C D is 400.", W("CD:  500 − 100 = 400", lab=True)),
    b("The next pairs work the same way. X L is 50 minus 10, which is 40. I V is 5 minus 1, which is 4.",
      W("XL:  50 − 10 = 40", lab=True), W("IV:  5 − 1 = 4", lab=True)),
    b("Now add the three parts: 400 and 40 and 4.", W("400 + 40 + 4 = 444")),
    b("So C D X L I V is 444.", A("444")),
    b("Careful: if you add every pair instead of taking away, each part comes out too big. Smaller letter in front means take away."),
]

L["Q_CH01_020"] = [
    b("Here is a long Roman numeral: M C M X C I X. Let us turn it into our own numbers, one part at a time.",
      G("MCMXCIX = ?", name="g")),
    b("Here is what each Roman letter is worth.", FIG(LETTERS)),
    b("First find the pairs where a smaller letter stands before a bigger one. Those are take away pairs: C M, X C and I X.",
      U("CM", on="g"), U("XC", on="g"), U("IX", on="g")),
    b("The M at the front stands alone, so it is 1000. Next comes C M. C is 100 and M is 1000. What is C M worth?",
      Q(["900", "1100", "1000"], "The smaller letter C is in front, so we take it away: 1000 minus 100 is 900.")),
    b("1000 minus 100 is 900. So far we have 1000 and 900.", W("M = 1000"), W("CM:  1000 − 100 = 900", lab=True)),
    b("X C is 100 minus 10, which is 90. I X is 10 minus 1, which is 9.",
      W("XC:  100 − 10 = 90", lab=True), W("IX:  10 − 1 = 9", lab=True)),
    b("Now add the four parts.", W("1000 + 900 + 90 + 9 = 1999")),
    b("So M C M X C I X is 1,999.", A("1,999")),
    b("Careful with X C. It is 90, not 40. 40 would be X L, with an L for 50.", W("XC = 90     XL = 40")),
    b("So the plan: find the take away pairs, work out each part, then add the parts."),
]
