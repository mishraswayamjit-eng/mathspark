"""Figures for Grade 4 "Number System & Place Value" (gr4_numbers).

    python -X utf8 scripts/figures/authoring/g4_gr4_numbers.py            # build the part file
    python -X utf8 scripts/figures/authoring/g4_gr4_numbers.py --review   # also print every figure against its question

Writes data/question-figures/parts/g4-gr4_numbers.json.

By rule (numbers read from the question):
  - "In the number N, what is the place value of the digit d in the P place?"  -> place-value chart
  - "... the place value of a (in X place) is how many times the place value of b (in Y place)?"
  - "How many odd numbers are there from A to B?"                                -> number line
  - "Roman numeral for N"                                                        -> a table of parts that grows
Everything else is drawn one question at a time, below.

A chart is shown before answering only when reading the place is not itself the answer.
"""
import re
import sys

from g4_gr4_numbers_lib import Part, pc, table, line, step_texts, answer, ind
import validate

P = Part("gr4_numbers")

H4 = ["Th", "H", "T", "O"]
H5 = ["TTh", "Th", "H", "T", "O"]
H6 = ["L", "TTh", "Th", "H", "T", "O"]


def chart(number, idx=None, note=None):
    return pc(str(number), note=note, hl=["d%d" % i for i in idx] if idx else None)


def places(headers, cells, note=None):
    """A blank place-value chart being filled in. '?' marks a place not yet decided."""
    return table([[str(c) for c in cells]], headers=headers, note=note)


def spots(number, digit):
    return [i for i, c in enumerate(str(number)) if c == str(digit)]


# ── Rule: place value of a digit in a named place ────────────────────────────
POWER = {"units": 0, "ones": 0, "tens": 1, "hundreds": 2, "thousands": 3, "ten-thousands": 4}
SINGLE = re.compile(r"^In the number (\d+), what is the place value of the digit (\d) in the ([a-z-]+) place\?$")
RATIO = re.compile(r"^In the number (\d+), the place value of (\d) \(in ([a-z-]+) place\) is how many times "
                   r"the place value of (\d) \(in ([a-z-]+) place\)\?$")


def place_index(number, digit, place):
    i = len(number) - 1 - POWER[place]
    assert number[i] == digit, (number, digit, place)
    return i


def rule_single(q):
    m = SINGLE.match(q["questionText"])
    if not m:
        return False
    number, digit, place = m.groups()
    i = place_index(number, digit, place)
    texts = step_texts(q)
    before = chart(number, [i], "Place value of the marked digit = ?")
    if len(texts) == 2:
        working = re.search(r"Place value = (.+)$", texts[1]).group(1)
        steps = [chart(number, [i], "The %s is in the %s place" % (digit, place)),
                 chart(number, [i], working)]
    else:
        steps = [chart(number, [i], "Count the places from the right"), None,
                 chart(number, [i], "Here the %s stands for %s" % (digit, answer(q)))]
    P.add(q, before, steps, origin="rule")
    return True


def rule_ratio(q):
    m = RATIO.match(q["questionText"])
    if not m:
        return False
    number, d1, p1, d2, p2 = m.groups()
    hl = [place_index(number, d1, p1), place_index(number, d2, p2)]
    texts = step_texts(q)
    values = re.match(r"PV of \d = (\d+), PV of \d = (\d+)", texts[0])
    before = chart(number, hl, "Compare the place values of the two marked digits")
    steps = [chart(number, hl, "The marked digits stand for %s and %s" % values.groups()),
             chart(number, hl, texts[1].replace("Ratio = ", ""))]
    P.add(q, before, steps, origin="rule")
    return True


# ── Rule: counting odd or even numbers in a range ────────────────────────────
COUNT = re.compile(r"^How many (odd|even) numbers are there from (\d+) to (\d+)\?$")


def rule_count(q):
    m = COUNT.match(q["questionText"])
    if not m:
        return False
    kind, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
    if hi - lo > 40:
        return False
    texts = step_texts(q)
    first, last = [int(x) for x in re.match(r"First \w+: (\d+), Last \w+: (\d+)", texts[0]).groups()]
    before = line(lo, hi, 1, ticks="ends", note="Count the %s numbers from %d to %d" % (kind, lo, hi))
    pts = [(first, "first"), (last, "last")]
    steps = [line(lo, hi, 1, points=pts, ticks="ends", note="The first %s number is %d and the last is %d" % (kind, first, last)),
             line(lo, hi, 1, points=pts, ticks="ends", note=texts[1].replace("Count = ", ""))]
    P.add(q, before, steps, origin="rule")
    return True


# ── Rule: a number written as a Roman numeral, part by part ──────────────────
ROMAN = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
         (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def to_roman(n):
    out = ""
    for value, symbol in ROMAN:
        while n >= value:
            out += symbol
            n -= value
    return out


def roman_parts(n):
    parts = []
    for place in (1000, 100, 10, 1):
        d = (n // place) % 10
        if d:
            parts.append((d * place, to_roman(d * place)))
    return parts


def rule_roman(qid):
    """The parts table gains a column each time a step names that part and its numeral."""
    q = P.by_id[qid]
    n = int(re.search(r"\d{3,4}", q["questionText"]).group(0))
    assert to_roman(n) == answer(q), qid
    parts = roman_parts(n)
    seen, prev, steps = "", 0, []
    texts = step_texts(q)
    for i, t in enumerate(texts):
        seen += " " + t
        nums = validate.numbers_in(seen)
        k = 0
        for value, numeral in parts:
            if float(value) in nums and re.search(r"\b%s\b" % numeral, seen):
                k += 1
            else:
                break
        last = i == len(texts) - 1
        if k and (k != prev or last):
            # Once a step has split the whole number, keep every part on show, with "?" for numerals not found yet.
            shown = len(parts) if all(float(value) in nums for value, _ in parts) else k
            fig = table([[numeral if j < k else "?" for j, (_, numeral) in enumerate(parts[:shown])]],
                        headers=[str(value) for value, _ in parts[:shown]])
            if last and k == len(parts):
                fig["note"] = "Join the parts in order: %s" % to_roman(n)
            steps.append(fig)
        elif k == 0 and prev == 0 and all(float(value) in nums for value, _ in parts):
            # The step splits the number but names no numeral yet: show the parts, numerals still to find.
            steps.append(table([["?"] * len(parts)], headers=[str(value) for value, _ in parts],
                               note="Split the number into its parts"))
        else:
            steps.append(None)
        prev = k
    P.add(q, None, steps, origin="rule")


for _q in P.qs:
    rule_single(_q) or rule_ratio(_q) or rule_count(_q)

for _qid in ["EXT_G4_FP_2020_027", "EXT_G4_FP_2021_007", "EXT_G4_FP_2023_004", "EXT_G4_FP_2024_020",
             "PYQ_2016_Q33", "PYQ_2018_Q32", "PYQ_2019_Q23", "Q_CH01_005"]:
    rule_roman(_qid)


# ── Individually drawn ───────────────────────────────────────────────────────
A = P.add
U = "?"

# Hand-written chapter questions
A("Q_CH01_001", None, {
    0: chart(362489, [1], "Count from the right: the 6 is in the ten-thousands"),
    2: chart(362489, [1], "The 6 stands for 60,000")})
A("Q_CH01_002",
  line(99996, 100000, 1, points=[(99999, "99,999")], ticks="none", note="Successor = the very next number"),
  {0: line(99996, 100000, 1, points=[(99999, "99,999")], hops=[(99999, 100000, "+1")], ticks="none"),
   2: chart(100000, None, "1,00,000 is one lakh")})
_big = [["45,032"], ["45,302"], ["45,320"], ["45,203"]]
A("Q_CH01_003",
  table(_big, note="Line the numbers up and compare from the left"),
  {0: table(_big, note="All have 45 thousands, so compare the hundreds digits"),
   1: table(_big, hl=["r1", "r2"], note="The biggest hundreds digit is 3: 45,302 or 45,320"),
   2: chart(45302, [3], "45,302 has 0 tens"),
   3: chart(45320, [3], "45,320 has 2 tens, so it is the largest")})
_asc = [["5,432"], ["5,342"], ["5,423"], ["5,234"]]
A("Q_CH01_009",
  table(_asc, note="Line the numbers up and compare from the left"),
  {0: table(_asc, note="All have 5 thousands, so look at the hundreds"),
   1: table(_asc, hl=["r1", "r3"], note="5,234 has 2 hundreds: smallest. 5,342 has 3 hundreds: next"),
   2: table(_asc, hl=["r0", "r2"], note="Both have 4 hundreds. 2 tens is less than 3 tens"),
   3: table([["5,234"], ["5,342"], ["5,423"], ["5,432"]], note="In ascending order, smallest first")})
_valid = [["XL", "50 − 10 = 40"], ["IX", "10 − 1 = 9"], ["XIV", "10 + 4 = 14"]]
A("Q_CH01_013", None, {
    0: table(_valid, headers=["Roman", "Number"], note="Only I and X are placed before a bigger letter"),
    1: table(_valid + [["VX", "?"]], headers=["Roman", "Number"], hl=["r3"], note="V is never used to take away"),
    2: table(_valid + [["VX", "not valid"]], headers=["Roman", "Number"], hl=["r3"], note="5 is written simply as V")})
A("Q_CH01_004", None, {
    0: table([["CD", "XL", "IV"]], note="CD: C before D, so take 100 away from 500", hl=["r0"]),
    1: table([["CD", "XL", "IV"]], note="XL: X before L, so take 10 away from 50"),
    2: table([["CD", "XL", "IV"]], note="IV: I before V, so take 1 away from 5"),
    3: table([["CD", "XL", "IV"]], note="Add the three parts: CDXLIV is 444")})
A("Q_CH01_006",
  line(4500, 4600, 10, points=[(4567, "4,567")], ticks="none", note="Which hundred is 4,567 nearer to?"),
  {0: line(4500, 4600, 10, points=[(4500, "4,500"), (4567, "4,567"), (4600, "4,600")], ticks="none",
           note="4,567 lies between 4,500 and 4,600"),
   1: line(4500, 4600, 10, points=[(4500, "4,500"), (4567, None), (4600, "4,600")], hops=[(4567, 4600)], ticks="none",
           note="The tens digit is 6, which is 5 or more: round up"),
   2: line(4500, 4600, 10, points=[(4567, None), (4600, "4,600")], hops=[(4567, 4600)], ticks="none",
           hl=["p1"], note="4,567 rounds to 4,600")})
A("Q_CH01_007", None, {2: chart(54321678, None, "One digit in each place: 8 digits")})
A("Q_CH01_008",
  chart(30507, None, "What does each digit stand for?"),
  {0: chart(30507, [0], "The 3 stands for 30,000. The 0 thousands add nothing"),
   1: chart(30507, [2, 4], "The 5 stands for 500 and the 7 stands for 7")})
A("Q_CH01_010",
  places(H4, [U] * 4, "Place the digits 7, 0, 3 and 5"),
  {1: places(H4, [7, 5, 3, 0], "Biggest digit in the biggest place, then in order"),
   2: chart(7530)})
A("Q_CH01_011",
  line(9998, 10002, 1, points=[(10000, "10,000")], ticks="none", note="Predecessor = the number just before"),
  {0: line(9998, 10002, 1, points=[(10000, "10,000")], hops=[(10000, 9999, "−1")], ticks="none"),
   1: line(9998, 10002, 1, points=[(9999, "9,999"), (10000, None)], hops=[(10000, 9999, "−1")], ticks="none",
           hl=["p0"])})
A("Q_CH01_012",
  chart(4562, [1], "Place value of the 5 − face value of the 5 = ?"),
  {0: chart(4562, [1], "The 5 is in the hundreds place: it stands for 500"),
   1: chart(4562, [1], "The face value of 5 is just 5"),
   3: chart(4562, [1], "500 − 5 = 495")})
A("Q_CH01_014", None, {
    0: line(4000, 5000, 100, points=[(4891, "4,891"), (5000, "5,000")], hops=[(4891, 5000)], ticks="none",
            note="Hundreds digit 8 is 5 or more: 4,891 rounds up"),
    1: line(3000, 4000, 100, points=[(3000, "3,000"), (3207, "3,207")], hops=[(3207, 3000)], ticks="none",
            note="Hundreds digit 2 is less than 5: 3,207 rounds down")})
A("Q_CH01_015",
  chart(2345678, None, "Read each period with its name"),
  {0: chart(2345678, [0, 1], "23 is in the lakhs period"),
   1: chart(2345678, [2, 3], "45 is in the thousands period"),
   2: chart(2345678, [4, 5, 6], "678 is in the ones period")})
A("Q_CH01_016",
  line(11, 21, 1, ticks="ends", note="Count the even numbers between 11 and 21"),
  {1: line(11, 21, 1, points=[(12, "12"), (14, "14"), (16, "16"), (18, "18"), (20, "20")], ticks="ends"),
   2: line(11, 21, 1, points=[(12, "12"), (14, "14"), (16, "16"), (18, "18"), (20, "20")], ticks="ends",
           note="5 even numbers")})
A("Q_CH01_017",
  places(H5, [U] * 5, "Place the digits 9, 0, 3, 1 and 7"),
  {0: places(H5, [1, U, U, U, U], "A number cannot start with 0, so 1 goes first"),
   1: places(H5, [1, 0, 3, 7, 9], "The rest go from smallest to biggest"),
   2: chart(10379)})
A("Q_CH01_019", None, {3: chart(100000, None, "A 1 followed by five 0s: one lakh")})
A("Q_CH01_020", None, {
    0: table([["M", "CM", "XC", "IX"]], note="Split MCMXCIX into its parts"),
    1: table([["1000", "900", "90", "9"]], headers=["M", "CM", "XC", "IX"]),
    3: table([["1000", "900", "90", "9"]], headers=["M", "CM", "XC", "IX"], note="Add the parts: MCMXCIX is 1,999")})
# Q_CH01_021 (between 3,45,678 and 3,45,680) wants a number line, but the contract caps a number line at 1,00,000.
A("Q_CH01_022",
  chart(4372, [0, 2], "Place value of the 4 × face value of the 7 = ?"),
  {0: chart(4372, [0], "The 4 is in the thousands place: it stands for 4,000"),
   1: chart(4372, [2], "The face value of 7 is just 7"),
   3: chart(4372, [0, 2], "4,000 × 7 = 28,000")})
A("Q_CH01_023", None, {
    0: chart(10000000, None, "1 crore: a 1 followed by 7 zeros"),
    1: chart(50000000, None, "5 crore: the 1 becomes a 5, the zeros stay"),
    2: chart(50000000, [1, 2, 3, 4, 5, 6, 7], "5 crore has 7 zeros")})
A("Q_CH01_024",
  places(H5, [U] * 5, "Put each digit in its place"),
  {0: places(H5, [4, 0, 3, 0, 8]),
   2: chart(40308, None, "The number is 40,308")})
A("Q_CH01_027",
  chart(5000000, None, "The number just before is 1 less"),
  {1: chart(4999999, None, "49,99,999 is 1 less than 50,00,000")})
A("Q_CH01_028",
  places(H4, [U] * 4, "Place the digits 5, 3, 8 and 1"),
  {0: places(H4, [U, U, U, 8], "An even number ends in an even digit: only 8 is even"),
   1: places(H4, [5, 3, 1, 8], "The others go in front, biggest first"),
   2: chart(5318)})

# Authored Grade 4 questions
A("G4A_NUMBERS_001",
  places(H5, [U] * 5, "Place the digits 4, 0, 7, 2 and 9"),
  {0: places(H5, [U, 9, U, U, U], "9 goes in the thousands place"),
   1: places(H5, [2, 9, U, U, U], "The first place cannot be 0, so it takes 2"),
   2: places(H5, [2, 9, 0, 4, 7], "0, 4 and 7 go from smallest to greatest"),
   3: chart(29047)})
A("G4A_NUMBERS_003", None, {
    1: chart(726935, None, "Name the place of every digit"),
    2: chart(726935, [1], "Look at the digit in the ten-thousands place"),
    3: chart(726935, [1], "The digit is 2")})
A("G4A_NUMBERS_004",
  chart(30540000, None, "The number in the Indian place-value chart"),
  {0: chart(30540000, None, "Without commas it has eight digits: 30540000")})
A("G4A_NUMBERS_006", None, {
    0: table([["1000", "900", "40", "7"]], headers=["M", "CM", "XL", "VII"], note="Read MCMXLVII part by part"),
    2: table([["MM", "XX", "II"]], headers=["2000", "20", "2"], note="Write 2022 part by part")})
A("G4A_NUMBERS_007", None, {
    0: table([["XL", "40"], ["LX", "60"]], headers=["Roman", "Number"]),
    1: table([["XL", "40"], ["LX", "60"], ["XIV", "14"], ["XLIV", "44"]], headers=["Roman", "Number"]),
    2: table([["XIV", "14"], ["XL", "40"], ["XLIV", "44"], ["LX", "60"]], headers=["Roman", "Number"],
             note="In order, smallest first")})
A("G4A_NUMBERS_008",
  line(4600, 4800, 10, points=[(4700, "4,700")], ticks="none", note="Which numbers round to 4,700?"),
  {2: line(4600, 4800, 10, points=[(4700, "4,700"), (4750, "4,750"), (4800, "4,800")], hops=[(4750, 4800)],
           ticks="none", note="4,750 has tens digit 5, so it rounds up to 4,800"),
   3: line(4600, 4800, 10, points=[(4700, "4,700"), (4749, "4,749")], hops=[(4749, 4700)], ticks="none",
           hl=["p1"], note="4,749 is the greatest number that still rounds down")})
A("G4A_NUMBERS_009",
  chart(38462, None, "Round to the nearest thousand, and to the nearest ten"),
  {0: line(38000, 39000, 100, points=[(38000, "38,000"), (38462, "38,462")], hops=[(38462, 38000, "Anil")],
           ticks="none", note="Hundreds digit 4 is less than 5: round down to 38,000"),
   1: line(38460, 38470, 1, points=[(38460, "38,460"), (38462, None)], hops=[(38462, 38460, "Bina")],
           ticks="none", note="Ones digit 2 is less than 5: round down to 38,460")})
A("G4A_NUMBERS_010", None, {
    0: line(9998, 10001, 1, points=[(9999, "9,999")], hops=[(9999, 10000, "+1")], ticks="none",
            note="The successor of 9,999 is 10,000"),
    1: line(998, 1001, 1, points=[(1000, "1,000")], hops=[(1000, 999, "−1")], ticks="none",
            note="The predecessor of 1,000 is 999")})
A("G4A_NUMBERS_011",
  line(19997, 20001, 1, points=[(20000, "20,000")], ticks="none", note="20,000 is the successor: one more than the number"),
  {2: line(19997, 20001, 1, points=[(19998, "19,998"), (20000, "20,000")], ticks="none", hl=["p0"],
           note="The number itself sits between 19,998 and 20,000")})
A("G4A_NUMBERS_013",
  chart(46285, [1], "The marked 6 is replaced by 9"),
  {0: chart(46285, [1], "The 6 is in the thousands place: it stands for 6,000"),
   1: chart(46285, [1], "A 9 in the same place stands for 9,000"),
   3: chart(46285, [1], "9,000 − 6,000 = 3,000")})
A("G4A_NUMBERS_015",
  places(H5, [U] * 5, "Fill the places from the clues"),
  {0: places(H5, [3, U, 0, U, 9], "The greatest odd digit is 9"),
   3: chart(38049, None, "The thousands digit 8 is twice the tens digit 4")})
A("G4A_NUMBERS_016",
  places(H5, [U] * 5, "Smallest odd number, all digits different"),
  {0: places(H5, [1, 0, U, U, U]),
   1: places(H5, [1, 0, 2, 3, U]),
   2: places(H5, [1, 0, 2, 3, 5], "1 and 3 are used, so the smallest odd digit left is 5"),
   4: chart(10235)})
A("G4A_NUMBERS_017", None, {
    0: table([["99", "XCIX", "4"]], headers=["Number", "Roman", "Symbols"]),
    1: table([["99", "XCIX", "4"], ["98", "XCVIII", "6"]], headers=["Number", "Roman", "Symbols"]),
    2: table([["99", "XCIX", "4"], ["98", "XCVIII", "6"], ["78", "LXXVIII", "7"]], headers=["Number", "Roman", "Symbols"]),
    3: table([["99", "XCIX", "4"], ["98", "XCVIII", "6"], ["78", "LXXVIII", "7"], ["88", "LXXXVIII", "8"]],
             headers=["Number", "Roman", "Symbols"]),
    4: table([["99", "XCIX", "4"], ["98", "XCVIII", "6"], ["78", "LXXVIII", "7"], ["88", "LXXXVIII", "8"]],
             headers=["Number", "Roman", "Symbols"], hl=["r3"], note="88 needs the most symbols")})
A("G4A_NUMBERS_019",
  line(500, 700, 10, points=[(600, "600")], ticks="none", note="Which numbers round to 600?"),
  {0: line(500, 700, 10, points=[(550, "550"), (600, "600")], ticks="none", note="550 is the smallest that rounds up to 600"),
   1: line(500, 700, 10, points=[(550, "550"), (600, "600"), (649, "649")], ticks="none",
           note="649 is the greatest: 650 rounds to 700"),
   3: line(500, 700, 10, points=[(550, "550"), (600, "600"), (649, "649")], ticks="none",
           note="From 550 to 649 there are 100 whole numbers")})
A("G4A_NUMBERS_020", None, {
    0: line(340, 360, 1, points=[(345, "345"), (354, "354")], ticks="none", note="345 to 354 round to 350 to the nearest ten"),
    1: line(340, 360, 1, points=[(345, "345"), (350, "350"), (354, "354")], ticks="none",
            note="350 and above round to 400, not 300"),
    2: line(340, 360, 1, points=[(345, "345"), (349, "349")], ticks="none", note="345 to 349 fit both clues"),
    3: line(340, 360, 1, points=[(345, "345"), (349, "349")], ticks="none", hl=["p1"], note="The greatest is 349")})
A("G4A_NUMBERS_022", None, {
    0: line(4440, 4450, 1, points=[(4446, "4,446"), (4450, "4,450")], hops=[(4446, 4450)], ticks="none",
            note="Sana: to the nearest ten"),
    1: line(4400, 4500, 10, points=[(4450, "4,450"), (4500, "4,500")], hops=[(4450, 4500)], ticks="none",
            note="Sana: then to the nearest hundred"),
    2: line(4000, 5000, 100, points=[(4500, "4,500"), (5000, "5,000")], hops=[(4500, 5000)], ticks="none",
            note="Sana: then to the nearest thousand"),
    3: line(4000, 5000, 100, points=[(4000, "4,000"), (4446, "4,446")], hops=[(4446, 4000)], ticks="none",
            note="Ravi: straight to the nearest thousand")})
_pages = [["1 to 9", "9", "1"], ["10 to 99", "90", "2"], ["100 to 120", "21", "3"]]
_pages_h = ["Pages", "How many", "Digits each"]
A("G4A_NUMBERS_023", None, {
    0: table(_pages[:1], headers=_pages_h),
    1: table(_pages[:2], headers=_pages_h),
    2: table(_pages, headers=_pages_h),
    3: table(_pages, headers=_pages_h, note="Add the digits from the three groups")})
A("G4A_NUMBERS_026",
  chart(835264, None, "Which digits are worth more than 100 times their face value?"),
  {1: chart(835264, [4, 5], "The 6 is worth 10 times and the 4 only 1 time its face value"),
   2: chart(835264, [3], "The 2 stands for 200: exactly 100 times, so it is not counted"),
   3: chart(835264, [0, 1, 2], "8, 3 and 5 are worth more than 100 times their face value"),
   4: chart(835264, [0, 1, 2], "So 3 digits fit")})
A("G4A_NUMBERS_028",
  line(49900, 50000, 10, points=[(49950, "49,950")], ticks="none", note="When does the ten-thousands digit change?"),
  {0: line(49900, 50000, 10, points=[(49950, "49,950"), (50000, "50,000")], ticks="none",
           note="The digit 4 changes when the number reaches 50,000"),
   1: line(49900, 50000, 10, points=[(49950, "49,950"), (50000, "50,000")], hops=[(49950, 50000, "?")], ticks="none"),
   3: line(49900, 50000, 10, points=[(49950, "49,950"), (50000, "50,000")], hops=[(49950, 50000, "+50")], ticks="none",
           hl=["h0"])})
# A table holds at most 5 columns, so the 6-digit number is shown only once it is complete.
A("G4A_NUMBERS_029", None, {
    3: chart(888830, [4, 5], "8 fills the first four places, then 3 in the tens and 0 in the ones")})

# Past papers
A("PYQ_2016_Q05", None, {
    1: chart(576006, spots(576006, 6), "The 6s are worth 6000 and 6"),
    2: chart(567060, spots(567060, 6), "The 6s are worth 60000 and 60"),
    3: chart(657600, spots(657600, 6), "The 6s are worth 600000 and 600")})
A("PYQ_2016_Q40", None, {2: chart(101110, [1, 2], "Only one thousand, so the thousands period shows 01")})
A("PYQ_2017_Q31",
  chart(978652, [1, 4], "Place value of the 7 − place value of the 5 = ?"),
  {0: chart(978652, [1], "The 7 is in the ten-thousands place: 70000"),
   1: chart(978652, [4], "The 5 is in the tens place: 50"),
   3: chart(978652, [1, 4], "70000 − 50 = 69950")})
A("PYQ_2019_Q10", None, {
    0: chart(9743753, None, "The first number is 97,43,753"),
    2: chart(9694071, [2], "The difference: 9 is in the ten thousands place")})

A("EXT_G4_FP_2020_019",
  places(H5, [U] * 5, "Put each digit in its place"),
  {0: places(H5, [6, U, U, U, U], "The greatest place is the ten-thousands"),
   1: places(H5, [6, 9, 7, U, U]),
   2: places(H5, [6, 9, 7, 1, 5], "The least place is the ones"),
   3: chart(69715)})
A("EXT_G4_FP_2022_011",
  chart(702459, [1, 4], "Swap the marked digits, 0 and 5"),
  {0: chart(752409, [1, 4], "After the swap the number is 7,52,409")})
A("EXT_G4_FP_2022_012", None, {
    1: chart(47659, [0, 1], "7 thousands is more than 6 thousands: 47659 is the greatest"),
    2: chart(47659, [2], "The 6 is in the hundreds place"),
    3: chart(47659, [2], "The 6 stands for 600")})
A("EXT_G4_FP_2022_029", None, {
    0: table([["1000", "400", "40", "9"]], headers=["M", "CD", "XL", "IX"], note="The starting year, part by part"),
    1: table([["1000", "600", "60", "5"]], headers=["M", "DC", "LX", "V"], note="The closing year, part by part"),
    3: table([["CC", "X", "VI"]], headers=["200", "10", "6"], note="216 years is CCXVI")})
A("EXT_G4_FP_2023_019", None, {
    0: chart(34562, spots(34562, 6), "Here the 6 is in the tens place: worth 60"),
    1: chart(3342654, spots(3342654, 6), "Here the 6 is in the hundreds place: worth 600"),
    2: chart(4256402, spots(4256402, 6), "Here the 6 is in the thousands place: worth 6000")})
A("EXT_G4_FP_2024_004",
  chart(768459, [3, 4], "Compare the place values of the 4 and the 5"),
  {0: chart(768459, [3], "The 4 is in the hundreds place: 400"),
   1: chart(768459, [4], "The 5 is in the tens place: 50"),
   3: chart(768459, [3, 4], "400 is 8 times 50")})
A("EXT_G4_FP_2024_009", None, {
    0: chart(9999, None, "The greatest 4-digit number"),
    3: chart(10096, [3], "In the sum, the 9 is in the tens place: 90")})
A("EXT_G4_FP_2025_018",
  chart(86352, [1, 3], "Swap the marked digits, 6 and 5"),
  {0: chart(85362, [1, 3], "After the swap the number is 85362")})
A("EXT_G4_FP_2025_036", None, {
    2: table([["DCCC", "XC", "VII"]], headers=["800", "90", "7"], note="Split 897 into 800 + 90 + 7")})

P.write()
if "--review" in sys.argv:
    P.review()
if "--redo" in sys.argv:
    P.review(["Q_CH01_003", "Q_CH01_005", "Q_CH01_009", "Q_CH01_013"])
