"""The 'greatest equal groups' questions of batch 08: one builder, fed each question's numbers.

Every board line is computed from the numbers. The story words (who, what, the container)
come from the spec written for each question in imported_08_specs.py.
"""
from imported_08_lib import (ANS, B, FIG, G, M, N, W, GIVEN, and_list, choose, factor_line, h, hcf, how_often,
                             lesson, pick, placed, primes_of, shared_runs, times_words)


def _divs(nums, H, idxs, names=None):
    """'84 divided by 12 is 7, and 60 divided by 12 is 5' for the chosen piles."""
    parts = []
    for i in idxs:
        s = "%d divided by %d is %d" % (nums[i], H, nums[i] // H)
        if names:
            s += " " + names[i]
        parts.append(s)
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + ", and " + parts[-1]


def _div_lines(nums, H, idxs, prefix):
    return [W("%s%d" % (prefix, i), "%d ÷ %d = %d" % (nums[i], H, nums[i] // H)) for i in idxs]


def front(spec):
    """Beats up to and including the HCF. Returns (beats, H)."""
    qid, nums = spec["id"], spec["nums"]
    k = len(nums)
    H = hcf(nums)
    both = "both" if k == 2 else "all three"
    nums_txt = and_list(nums)
    facs = [primes_of(n) for n in nums]
    shared = primes_of(H)

    beats = [B(spec["intro"], GIVEN("q", spec["given"], True))]

    # Ask 1: a factor or a multiple?
    if h(qid, "a1") % 2 == 0:
        choices, idx = placed(qid, "a1p", "the highest common factor",
                              ["the lowest common multiple", "the numbers added together"])
        beats.append(B(
            "%s So %s has to divide %s exactly. We want the greatest number that does. What is it called?"
            % (spec["why"], spec["thing"], nums_txt),
            ask=choose(choices, idx,
                       "A common multiple is at least as big as the biggest of these numbers, so it could never divide "
                       "them all. We need a factor of %s numbers, and the greatest one: the highest common factor." % both)))
        beats.append(B("So our job is to find the highest common factor of %s." % nums_txt,
                       W("p", "Find the HCF of %s" % nums_txt, label=True), M("p", "HCF")))
    else:
        choices, idx = placed(qid, "a1p", "a factor of %s" % both, ["a multiple of %s" % both])
        beats.append(B(
            "%s So %s has to divide %s exactly. Is that a factor of these numbers, or a multiple of them?"
            % (spec["why"], spec["thing"], nums_txt),
            ask=choose(choices, idx,
                       "A multiple of these numbers is at least as big as the biggest of them, so it cannot divide them "
                       "all exactly. A number that divides exactly is a factor.")))
        beats.append(B("A factor of %s, and we want the greatest one. So we need the highest common factor of %s."
                       % (both, nums_txt),
                       W("p", "Find the HCF of %s" % nums_txt, label=True), M("p", "HCF")))

    # Prime factors, one number per beat.
    opener = pick(qid, "f0", ["Let's break each number into its prime factors, smallest first.",
                              "We split each number into primes, starting with the smallest.",
                              "The sure way is prime factors. Break each number down, smallest prime first."])
    for i, n in enumerate(nums):
        line = W("f%d" % i, factor_line(n)[0])
        said = "%d is %s." % (n, times_words(facs[i]))
        if i == 0:
            beats.append(B("%s %s" % (opener, said), line,
                           FIG("tree", {"kind": "factorTree", "number": n, "highlight": ["primes"]})))
        elif i == k - 1:
            beats.append(B("And %s" % said, line))
        else:
            beats.append(B("Next, %s" % said, line))

    # Ask 2: the trap. Either a prime that appears a different number of times, or one missing from a list.
    uneven = [p for p in sorted(set(shared)) if len({f.count(p) for f in facs}) > 1]
    missing = [p for p in sorted({p for f in facs for p in f}) if p not in shared]
    extra = ""
    if uneven:
        p = uneven[0]
        counts = [f.count(p) for f in facs]
        low = min(counts)
        seen = ["in %d it appears %s" % (n, how_often(c)) for n, c in zip(nums, counts)]
        if k == 2:
            where = "I%s, and %s." % (seen[0][1:], seen[1])
        else:
            where = "I%s, %s, and %s." % (seen[0][1:], seen[1], seen[2])
        distinct = sorted(set(counts))
        others = [c for c in distinct if c != low]
        if len(distinct) < 3:
            others.append(low + max(counts))
        choices, idx = placed(qid, "a2p", how_often(low), [how_often(c) for c in others])
        lowest = nums[counts.index(low)]
        beats.append(B(
            "Now count how many times %d appears. %s How many times can %d go into the highest common factor?" % (p, where, p),
            ask=choose(choices, idx,
                       "A common factor has to fit inside every one of the numbers. In %d, %d appears only %s, so %s is all we can take."
                       % (lowest, p, how_often(low), how_often(low)))))
        if missing:
            q = missing[0]
            lacks = [n for n, f in zip(nums, facs) if q not in f][0]
            extra = " And %d is not a factor of %d, so it stays out." % (q, lacks)
    else:
        p = [q for q in facs[0] if q not in shared][0] if [q for q in facs[0] if q not in shared] else missing[0]
        has = [n for n, f in zip(nums, facs) if p in f][0]
        lacks = [n for n, f in zip(nums, facs) if p not in f][0]
        choices, idx = placed(qid, "a2p", "No, it must be in %s lists" % both, ["Yes, it is a prime factor"])
        beats.append(B(
            "Now look at the %d. It is a factor of %d, but not of %d. Does %d go into the highest common factor?" % (p, has, lacks, p),
            ask=choose(choices, idx,
                       "A common factor has to divide every number. %d does not divide %d, so it stays out." % (p, lacks))))
        extra = " Every other prime is missing from at least one list."

    marks = []
    for i, n in enumerate(nums):
        runs = shared_runs(n, shared)
        if len(runs) == 1:
            marks.append(M("f%d" % i, runs[0][0], "underline", runs[0][1]))
        else:
            marks.append(G("f%d" % i, runs, "shared"))
    beats.append(B("So we mark only what %s lists share: %s.%s" % (both, and_list(shared), extra), *marks))

    hline = "%s = %d" % (" × ".join(str(p) for p in shared), H)
    beats.append(B("%s %s is %d. So the highest common factor is %d."
                   % (pick(qid, "mul", ["Multiply them together.", "Now multiply the shared primes."]), times_words(shared), H, H),
                   W("h", hline), M("h", "= %d" % H, "box"), N("h", "= %d" % H, "HCF")))
    return beats, H


def coprime(qs, H, tail):
    return "And %s have no common factor bigger than 1, %s" % (and_list(qs), tail)


# ── Sharing piles into equal bags, boxes, kits ───────────────────────────────

def share(spec):
    qid, nums = spec["id"], spec["nums"]
    k = len(nums)
    beats, H = front(spec)
    qs = [n // H for n in nums]
    cont, cont1, who, items = spec["cont"], spec["cont1"], spec["who"], spec["items"]
    inside = spec.get("inside", "in")
    want = spec["want"]
    kind = want[0]
    everyone = list(range(k))

    if kind == "count":
        beats.append(B("That is our answer. %s can make %d %s." % (who, H, cont),
                       ANS("ans", spec["ans"], True), M("ans", str(H), "circle")))
        beats.append(B("Check. %s. Nothing is left over." % _divs(nums, H, everyone),
                       *_div_lines(nums, H, everyone, "c")))
        beats.append(B(coprime(qs, H, "so no greater number of %s would work." % cont)))
        end = ["So for the greatest number of equal %s, find the highest common factor of the piles." % cont,
               "Remember the plan: prime factors, keep only what every list shares, and multiply. That gives the greatest number of equal %s." % cont]

    elif kind in ("per", "peronly"):
        i = want[1]
        others = [j for j in everyone if j != i]
        if kind == "per":
            beats.append(B("So %s can make %d %s. Next, the question asks how many %s go %s each one."
                           % (who, H, cont, items[i], inside)))
        else:
            beats.append(B("So there are %d %s. But that is not the answer yet. The question asks how many %s go %s each one."
                           % (H, cont, items[i], inside)))
        j = others[0]
        beats.append(B("Careful to share out the %d %s, not the %d %s. %d divided by %d is %d."
                       % (nums[i], items[i], nums[j], items[j], nums[i], H, qs[i]),
                       W("d", "%d ÷ %d = %d" % (nums[i], H, qs[i])), M("d", "= %d" % qs[i])))
        if kind == "per":
            beats.append(B("So the answer is %d %s, with %d %s %s each." % (H, cont, qs[i], items[i], inside),
                           ANS("ans", spec["ans"], True), M("ans", spec["ans"], "circle")))
        else:
            beats.append(B("So each %s gets %d %s." % (cont1, qs[i], items[i]),
                           ANS("ans", spec["ans"], True), M("ans", str(qs[i]), "circle")))
        beats.append(B("Check the other pile%s. %s. Nothing is left over."
                       % ("s" if len(others) > 1 else "", _divs(nums, H, others)),
                       *_div_lines(nums, H, others, "c")))
        beats.append(B(coprime(qs, H, "so %d really is the greatest number of %s." % (H, cont))))
        end = ["So for the greatest number of equal %s, find the highest common factor. Then divide the pile you are asked about by it." % cont,
               "The plan: prime factors, keep what every list shares, multiply. Then one division tells you what goes %s each %s." % (inside, cont1)]

    elif kind == "both":
        beats.append(B("So %s can make %d %s. Now share out each pile." % (who, H, cont)))
        beats.append(B("%s." % _divs(nums, H, everyone, items), *_div_lines(nums, H, everyone, "d")))
        beats.append(B("So the answer is %d %s, with %s %s each."
                       % (H, cont, and_list(["%d %s" % (q, it) for q, it in zip(qs, items)]), inside),
                       ANS("ans", spec["ans"], True), M("ans", spec["ans"], "circle")))
        beats.append(B("Check by multiplying back. %s. Nothing is left over."
                       % and_list(["%d times %d is %d" % (H, q, n) for q, n in zip(qs, nums)]),
                       *[W("c%d" % j, "%d × %d = %d" % (H, qs[j], nums[j])) for j in everyone]))
        beats.append(B(coprime(qs, H, "so %d really is the greatest number of %s." % (H, cont))))
        end = ["So for the greatest number of equal %s, find the highest common factor. Then divide each pile by it." % cont]

    else:  # total, totalonly: how many things in one bag
        noun = want[1]
        T = sum(qs)
        if kind == "total":
            beats.append(B("So %s can make %d %s. Now let's fill one %s." % (who, H, cont, cont1)))
        else:
            beats.append(B("So there are %d %s. But that is not the answer yet. We are asked what goes into one %s." % (H, cont, cont1)))
        beats.append(B("%s." % _divs(nums, H, everyone, items), *_div_lines(nums, H, everyone, "d")))
        sum_txt = " plus ".join(str(q) for q in qs)
        beats.append(B("Careful: we want the %s in one %s, so we add these small shares, not the big piles. %s is %d."
                       % (noun, cont1, sum_txt, T),
                       W("s", "%s = %d" % (" + ".join(str(q) for q in qs), T)), M("s", "= %d" % T)))
        if kind == "total":
            beats.append(B("So the answer is %d %s, with %d %s in each." % (H, cont, T, noun),
                           ANS("ans", spec["ans"], True), M("ans", spec["ans"], "circle")))
        else:
            beats.append(B("So each %s holds %d %s." % (cont1, T, noun),
                           ANS("ans", spec["ans"], True), M("ans", str(T), "circle")))
        whole = sum(nums)
        beats.append(B("Check. %d %s of %d is %d %s. And %s is %d too."
                       % (H, cont, T, whole, noun, " plus ".join(str(n) for n in nums), whole),
                       W("c1", "%d × %d = %d" % (H, T, whole)),
                       W("c2", "%s = %d" % (" + ".join(str(n) for n in nums), whole))))
        end = ["So find the highest common factor for the number of %s, divide each pile by it, then add up what one %s holds." % (cont, cont1)]

    beats.append(B(pick(qid, "end", end)))
    return lesson(*beats)


# ── Cutting lengths (or weights) into equal pieces ───────────────────────────

def cut(spec):
    qid, nums = spec["id"], spec["nums"]
    k = len(nums)
    beats, H = front(spec)
    qs = [n // H for n in nums]
    piece, pieces, unit = spec["piece"], spec["pieces"], spec["unit"]
    each_is = spec["each_is"] % H
    want = spec["want"]
    kind = want[0]
    everyone = list(range(k))
    both = "both" if k == 2 else "all three"

    if kind == "len":
        beats.append(B("So %s. That is our answer." % each_is, ANS("ans", spec["ans"], True), M("ans", str(H), "circle")))
        beats.append(B("Check. %s. Nothing is left over." % _divs(nums, H, everyone),
                       *_div_lines(nums, H, everyone, "c")))
        beats.append(B(coprime(qs, H, "so no bigger %s would fit %s." % (piece, both))))
        end = [spec["end"]]
    else:
        T = sum(qs)
        whole = sum(nums)
        if kind == "lentotal":
            beats.append(B("So %s. Now count the %s." % (each_is, pieces)))
        else:
            beats.append(B("So %s. But that is not the answer yet. We still have to count the %s." % (each_is, pieces)))
        beats.append(B("%s." % _divs(nums, H, everyone), *_div_lines(nums, H, everyone, "d")))
        beats.append(B("Careful: the %s come from %s, so we add them all. %s is %d."
                       % (pieces, spec["sources"], " plus ".join(str(q) for q in qs), T),
                       W("s", "%s = %d" % (" + ".join(str(q) for q in qs), T)), M("s", "= %d" % T)))
        check = B("Check. %d %s of %d %s make %d %s. And %s is %d too."
                  % (T, pieces, H, unit, whole, unit, " plus ".join(str(n) for n in nums), whole),
                  W("c1", "%d × %d = %d" % (T, H, whole)),
                  W("c2", "%s = %d" % (" + ".join(str(n) for n in nums), whole)))
        if kind == "lentotal":
            beats.append(B("So %s, and there are %d %s in all." % (each_is, T, pieces),
                           ANS("ans", spec["ans"], True), M("ans", spec["ans"], "circle")))
            beats.append(check)
        elif kind == "total":
            beats.append(B("So there are %d %s in all." % (T, pieces),
                           ANS("ans", spec["ans"], True), M("ans", str(T), "circle")))
            beats.append(check)
        else:  # cost
            rate = want[1]
            beats.append(check)
            beats.append(B("Each %s costs %d rupees. %d %s cost %d times %d, which is %d rupees."
                           % (piece, rate, T, pieces, T, rate, T * rate),
                           ANS("ans", "%d × %d = %d" % (T, rate, T * rate)), M("ans", "= %d" % (T * rate), "circle")))
            if spec.get("extra"):
                beats.append(B(spec["extra"]))
        end = [spec["end"]]

    beats.append(B(pick(qid, "end", end)))
    return lesson(*beats)


# ── Square tiles on a rectangular floor ──────────────────────────────────────

def tile(spec):
    qid, nums = spec["id"], spec["nums"]
    beats, H = front(spec)
    a, b = nums[0] // H, nums[1] // H
    T = a * b
    beats.append(B("So the biggest square tile has a side of %d centimetres.%s"
                   % (H, "" if spec["want"] == "sidecount" else " But the question asks how many tiles.")))
    beats.append(B("Along the %d side, %d divided by %d is %d tiles. Along the %d side, %d divided by %d is %d tiles."
                   % (nums[0], nums[0], H, a, nums[1], nums[1], H, b),
                   W("d0", "%d ÷ %d = %d" % (nums[0], H, a)), W("d1", "%d ÷ %d = %d" % (nums[1], H, b)),
                   FIG("floor", {"kind": "grid", "rows": min(a, b), "cols": max(a, b)})))
    beats.append(B("Careful: that is %d rows of %d tiles, so we multiply. Adding would only count two edges. %d times %d is %d."
                   % (min(a, b), max(a, b), a, b, T),
                   W("s", "%d × %d = %d" % (a, b, T)), M("s", "= %d" % T)))
    if spec["want"] == "sidecount":
        beats.append(B("So the tile side is %d centimetres, and %d tiles are needed." % (H, T),
                       ANS("ans", spec["ans"], True), M("ans", spec["ans"], "circle")))
    else:
        beats.append(B("So %d tiles are needed." % T, ANS("ans", spec["ans"], True), M("ans", str(T), "circle")))
    beats.append(B("Check. %d tiles of %d make %d, and %d tiles of %d make %d. The floor is covered exactly."
                   % (a, H, nums[0], b, H, nums[1]),
                   W("c0", "%d × %d = %d" % (a, H, nums[0])), W("c1", "%d × %d = %d" % (b, H, nums[1]))))
    beats.append(B("So the biggest square tile is the highest common factor of the two sides. Then count the tiles along each side and multiply."))
    return lesson(*beats)


BUILDERS = {"share": share, "cut": cut, "tile": tile}


def build(spec):
    return BUILDERS[spec["kind"]](spec)
