"""Batch 5: worksheets B4 to B6: counting multiples, squares, HCF and LCM, equations."""
from c_lib import *

E = {}

# Counting multiples on a line whose ticks are the multiples.
E["EXT_G5_WS_B4_003"] = entry(
    figure=nl(60, 100, 5, points=[(60, "60"), (100, "100")], note="Count the multiples of 3 that lie between these"),
    steps=[
        nl(60, 102, 3, points=[(63, "first")], note="First one after 60: 63 = 3 × 21"),
        nl(60, 102, 3, points=[(63, "first"), (99, "last")], note="Last one before 100: 99 = 3 × 33"),
        nl(60, 102, 3, points=[(63, "first"), (99, "last")], note="From the 21st to the 33rd: 33 − 21 + 1 = 13"),
    ],
)
E["EXT_G5_WS_B4_004"] = entry(steps=[
    nl(8, 100, 4, points=[(12, "first")], note="First two-digit multiple: 12 = 4 × 3"),
    nl(8, 100, 4, points=[(12, "first"), (96, "last")], note="Last two-digit multiple: 96 = 4 × 24"),
    nl(8, 100, 4, points=[(12, "first"), (96, "last")], note="From the 3rd to the 24th: 24 − 3 + 1 = 22"),
])

# Squares.
E["EXT_G5_WS_B5_005"] = entry(steps=[
    None,
    pc("9801", "9 thousands, 8 hundreds, 0 tens, 1 unit", ["d1"]),
    pc("9801", "Place value of 8 = 8 × 100 = 800", ["d1"]),
])
E["EXT_G5_WS_B5_006"] = entry(steps=[
    None,
    pc("9409", "97 × 97 = 9409"),
    pc("9409", "The hundreds digit is 4", ["d1"]),
])
E["EXT_G5_WS_B5_014"] = entry(steps=[
    nl(360, 400, 1, points=[(361, "19 × 19"), (386, "386"), (400, "20 × 20")], note="386 lies between two square numbers"),
    nl(360, 400, 1, points=[(361, "19 × 19"), (386, "386")], hops=[(386, 361, "− 25")], note="Step down to 361: 386 − 361 = 25"),
    nl(360, 400, 1, points=[(361, "19 × 19"), (386, "386")], hops=[(386, 361, "− 25")], note="386 − 25 = 361, a square number"),
])
E["EXT_G5_WS_B5_015"] = entry(steps=[
    nl(1365, 1445, 5, points=[(1369, "37 × 37"), (1400, "1400"), (1444, "38 × 38")], note="1400 lies between two square numbers"),
    nl(1365, 1445, 5, points=[(1400, "1400"), (1444, "38 × 38")], hops=[(1400, 1444, "+ 44")], note="Step up to 1444: 1444 − 1400 = 44"),
    None,
])
E["EXT_G5_WS_B5_017"] = entry(steps=[
    ftree(588, "588 = 2 × 2 × 3 × 7 × 7", ["primes"]),
    ftree(588, "The 2s pair up and the 7s pair up. The 3 has no partner."),
    ftree(196, "588 ÷ 3 = 196 = 14 × 14"),
])
E["EXT_G5_WS_B5_019"] = entry(steps=[
    ftree(360, "3 × 4 × 5 × 6 = 360 = 2 × 2 × 2 × 3 × 3 × 5", ["primes"]),
    ftree(360, "One 2 and the 5 have no partner"),
    ftree(360, "Give each a partner: multiply by 2 × 5 = 10"),
])
E["EXT_G5_WS_B5_022"] = entry(steps=[
    nl(16, 36, 1, points=[(16, "4 × 4"), (36, "6 × 6")], note="The two ends are 16 and 36"),
    nl(16, 36, 1, points=[(16, "4 × 4"), (17, "first"), (35, "last"), (36, "6 × 6")], note="Between them: 17 up to 35",
       hl=["p1", "p2"]),
    nl(16, 36, 1, points=[(17, "first"), (35, "last")], note="35 − 17 + 1 = 19 numbers"),
])

# HCF and LCM: prime factors side by side.
_pf = lambda rows, note, hl=None: table(rows, note, hl, headers=["Number", "Prime factors"])
E["EXT_G5_WS_B6_001"] = entry(steps=[
    ftree(328, "328 = 2 × 2 × 2 × 41", ["primes"]),
    ftree(424, "424 = 2 × 2 × 2 × 53", ["primes"]),
    _pf([["328", "2 × 2 × 2 × 41"], ["424", "2 × 2 × 2 × 53"]], "Shared factors: 2 × 2 × 2 = 8"),
])
_a = [["27", "3 × 3 × 3"], ["72", "2 × 2 × 2 × 3 × 3"]]
E["EXT_G5_WS_B6_003"] = entry(steps=[
    _pf(_a, "Break both numbers into prime factors"),
    _pf(_a, "HCF = the shared factors: 3 × 3 = 9"),
    _pf(_a, "LCM = most of each prime: 8 × 27 = 216"),
    _pf(_a, "HCF + LCM = 9 + 216 = 225"),
])
E["EXT_G5_WS_B6_004"] = entry(steps=[
    _pf([["45", "3 × 3 × 5"], ["54", "2 × 3 × 3 × 3"]], "HCF = 3 × 3 = 9. LCM = 270"),
    None,
    None,
])
_b = [["12", "2 × 2 × 3"], ["36", "2 × 2 × 3 × 3"], ["120", "2 × 2 × 2 × 3 × 5"]]
E["EXT_G5_WS_B6_005"] = entry(steps=[
    _pf(_b, "Break all three numbers into prime factors"),
    _pf(_b, "Take the most 2s, the most 3s and the 5"),
    _pf(_b, "LCM = 8 × 9 × 5 = 360"),
])
_c = [["36", "2 × 2 × 3 × 3"], ["48", "2 × 2 × 2 × 2 × 3"]]
E["EXT_G5_WS_B6_007"] = entry(steps=[
    None,
    _pf(_c, "Take off the remainder 3 first: 36 and 48"),
    _pf(_c, "HCF = shared factors: 2 × 2 × 3 = 12"),
])
E["EXT_G5_WS_B6_008"] = entry(steps=[
    _pf([["8", "2 × 2 × 2"], ["10", "2 × 5"], ["12", "2 × 2 × 3"]], "LCM = 2 × 2 × 2 × 3 × 5 = 120"),
    None,
    None,
])

# Equations on a balance.
E["EXT_G5_WS_B6_013"] = entry(
    figure=balance("7a + 2b − 2a", "26", "Put b = 3, then find a"),
    steps=[
        balance("7a + 6 − 2a", "26", "2b becomes 2 × 3 = 6"),
        balance("5a + 6", "26", "7a − 2a = 5a"),
        balance("5a", "20", "Take 6 from both sides. a = 20 ÷ 5 = 4"),
    ],
)
E["EXT_G5_WS_B6_014"] = entry(steps=[
    None,
    None,
    balance("5 × 8 + 7", "8 × 8 − 17", "Both sides come to 47, so this one balances"),
    None,
])
E["EXT_G5_WS_B6_015"] = entry(
    figure=balance("2m + 1", "8", "Use this to find 4m + 5"),
    steps=[
        balance("2m", "7", "Take 1 from both sides"),
        balance("4m", "14", "Double both sides"),
        balance("4m + 5", "19", "Add 5 to both sides"),
    ],
)
E["EXT_G5_WS_B6_016"] = entry(
    figure=balance("2(3d + 4)", "4(5 − 2d) + 2", "Open the brackets on each side first"),
    steps=[
        balance("6d + 8", "4(5 − 2d) + 2", "Left side: 2 × 3d + 2 × 4", ["left"]),
        balance("6d + 8", "22 − 8d", "Right side: 20 − 8d + 2", ["right"]),
        balance("14d", "14", "Add 8d and take 8 from both sides: d = 1"),
        balance("14", "14", "Check with d = 1: both sides are 14"),
    ],
)
E["EXT_G5_WS_B6_017"] = entry(
    figure=balance("3p", "27", "p = q + r and r = 5. Find q × q."),
    steps=[
        balance("p", "9", "Share both sides into 3: p = 9"),
        balance("q + 5", "9", "p is q + r, so q = 4"),
        None,
    ],
)
E["EXT_G5_WS_B6_019"] = entry(
    figure=balance("2p + 3q", "0", "p = m + 3 and q = 5 − m"),
    steps=[
        balance("2(m + 3) + 3(5 − m)", "0", "Swap p and q for their values in m"),
        balance("2m + 6 + 15 − 3m", "0", "Open the brackets"),
        balance("21 − m", "0", "2m − 3m = −m and 6 + 15 = 21"),
        balance("21", "m", "So m = 21"),
    ],
)

def _xyz(note, hl=None):
    return bm([bar([seg("x", 1, "a"), seg("y", 1, "b")], brace="12"),
               bar([seg("y", 1, "b"), seg("z", 1, "c")], brace="16"),
               bar([seg("z", 1, "c"), seg("x", 1, "a")], brace="10")], note, hl)

E["EXT_G5_WS_B6_020"] = entry(
    figure=_xyz("Each letter appears in two of the bars"),
    steps=[
        _xyz("Add all three bars: 12 + 16 + 10"),
        _xyz("That is two of each letter: 2x + 2y + 2z = 38"),
        bm([bar([seg("x", 1, "a"), seg("y", 1, "b"), seg("z", 1, "c")], brace="19")], "Half of 38: x + y + z = 19"),
    ],
)

E["EXT_G5_WS_B7_007"] = entry(
    figure=balance("(b − 8)/42", "5/7", "What must b − 8 be?"),
    steps=[
        balance("7 × (b − 8)", "210", "Cross-multiply: 5 × 42 = 210"),
        balance("b − 8", "30", "Share both sides into 7"),
        balance("b", "38", "Add 8 to both sides"),
    ],
)
