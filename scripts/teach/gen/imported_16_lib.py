"""Helpers for the imported-16 lessons (profit and loss stories, number patterns).

Board ops are plain dicts in the shape of src/lib/teach/types.ts. The three rules
here (ap_term, ap_list_sum, ap_sum) teach a pattern that grows by the same amount
each time, computing every number they write or say.
"""
import hashlib


# ── Board ops ────────────────────────────────────────────────────────────────

def W(id, text, tone=None):
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    return op


def LB(id, text, tone=None):
    op = {"op": "write", "id": id, "text": text, "label": True}
    if tone:
        op["tone"] = tone
    return op


def GIVEN(id, text):
    return LB(id, text, "given")


def ANS(id, text):
    return W(id, text, "answer")


def ANSL(id, text):
    return LB(id, text, "answer")


def _target(text, nth=1):
    t = {"text": str(text)}
    if nth != 1:
        t["nth"] = nth
    return t


def MARK(line, text, shape="circle", nth=1):
    return {"op": "mark", "line": line, "target": _target(text, nth), "shape": shape}


def CIRC(line, text, nth=1):
    return MARK(line, text, "circle", nth)


def UL(line, text, nth=1):
    return MARK(line, text, "underline", nth)


def BOX(line, text, nth=1):
    return MARK(line, text, "box", nth)


def NOTE(line, target, text, place="below", nth=1):
    return {"op": "note", "line": line, "target": _target(target, nth), "text": str(text), "place": place}


def STRIKE(line, target, note=None, nth=1):
    op = {"op": "strike", "line": line, "target": _target(target, nth)}
    if note:
        op["note"] = note
    return op


def CHOOSE(choices, answer, if_not):
    return {"kind": "choose", "choices": choices, "answer": answer, "ifNot": if_not}


def B(say, *ops, **kw):
    beat = {"say": say}
    if ops:
        beat["board"] = list(ops)
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def LESSON(*beats):
    return {"origin": "authored", "beats": list(beats)}


def pick(qid, salt, options):
    """A stable choice among a few phrasings."""
    h = int(hashlib.md5((qid + "|" + salt).encode("utf-8")).hexdigest(), 16)
    return options[h % len(options)]


def last_nth(text, sub):
    """The nth of the last place `sub` appears in `text` (counted as str.count does)."""
    pos = text.rfind(sub)
    n = 0
    i = text.find(sub)
    while i != -1:
        n += 1
        if i >= pos:
            return n
        i = text.find(sub, i + len(sub))
    return max(n, 1)


def item_nth(items, idx):
    """In the list written as 'a, b, c', which occurrence of item idx's text is item idx itself."""
    text = ", ".join(str(x) for x in items)
    sub = str(items[idx])
    pos = len(", ".join(str(x) for x in items[:idx])) + (2 if idx else 0)
    return last_nth(text[:pos + len(sub)], sub)


def ANSC(id, text, ring):
    """An answer line with its result ringed."""
    return [ANS(id, text), CIRC(id, str(ring), last_nth(text, str(ring)))]


def placed(qid, salt, right, others):
    """Choices with the right one put at a stable place. Returns (choices, index)."""
    at = pick(qid, salt, list(range(len(others) + 1)))
    choices = list(others)
    choices.insert(at, right)
    assert len(set(choices)) == len(choices), choices
    return choices, at


def plus_line(nums):
    return " + ".join(str(x) for x in nums)


def said(nums):
    nums = [str(x) for x in nums]
    if len(nums) == 1:
        return nums[0]
    return ", ".join(nums[:-1]) + " and " + nums[-1]


# ── Shared pieces of the pattern rules ───────────────────────────────────────

def _jump_beat(qid, terms, each, place, places, shown, d):
    a, t1, t2 = terms[0], terms[1], terms[2]
    if shown >= 3:
        return B(pick(qid, "jump", [
            "First, the jump. %d minus %d is %d, and %d minus %d is %d as well. So %s.",
            "Start with how the pattern grows. %d minus %d is %d, and %d minus %d is %d too. So %s.",
        ]) % (t1, a, d, t2, t1, d, each),
            W("d1", "%d − %d = %d" % (t1, a, d)), W("d2", "%d − %d = %d" % (t2, t1, d)))
    return B("The story tells us the jump: %s. So the %s go %d, %d, %d, and so on." % (each, places, a, t1, t2),
             LB("d1", "%d, %d, %d, …   (+ %d each time)" % (a, t1, t2, d)))


def _pair_ask(qid, terms, d):
    a, last = terms[0], terms[-1]
    s = a + last
    choices, at = placed(qid, "pair", "%d again" % s, ["more than %d" % s, "less than %d" % s])
    return CHOOSE(choices, at,
                  "%d is %d more than %d, and %d is %d less than %d. One goes up by %d and the other comes down by %d, "
                  "so the total stays the same." % (terms[1], d, a, terms[-2], d, last, d, d))


def _check_beat(qid, terms, places):
    n = len(terms)
    h = (n + 1) // 2
    s1, s2 = sum(terms[:h]), sum(terms[h:])
    l1 = "%s = %d" % (plus_line(terms[:h]), s1)
    l2 = "%s = %d" % (plus_line(terms[h:]), s2)
    l3 = "%d + %d = %d" % (s1, s2, s1 + s2)
    assert len(l1) <= 60 and len(l2) <= 60, (l1, l2)
    say = pick(qid, "check", [
        "Let's check the slow way. The first %d %s add up to %d, the other %d add up to %d, and %d plus %d is %d. It matches.",
        "Check by plain adding. The first %d %s come to %d, the other %d come to %d, and %d plus %d is %d. Same total.",
    ]) % (h, places, s1, n - h, s2, s1, s2, s1 + s2)
    return B(say, W("c1", l1), W("c2", l2), W("c3", l3))


# ── Rule: the term in a far-off place ────────────────────────────────────────

def ap_term(qid, intro, given, terms, n, place, each, ending):
    """terms: the ones the question shows. n: the place asked for."""
    a, d = terms[0], terms[1] - terms[0]
    assert all(terms[i + 1] - terms[i] == d for i in range(len(terms) - 1))
    full = [a + i * d for i in range(n)]
    last = full[-1]
    j = (n - 1) * d
    t1, t2 = terms[1], terms[2]
    P = place.capitalize()
    beats = [B(intro, GIVEN("q", given))]

    choices, at = placed(qid, "grow", "add %d" % d, ["add %d" % a, "add %d" % t1])
    beats.append(B(pick(qid, "growsay", [
        "Before we jump ahead, look at how the pattern grows. What happens from one %s to the next?" % place,
        "Don't rush to %s %d yet. First, what is the rule that takes us from one %s to the next?" % (place, n, place),
    ]), ask=CHOOSE(choices, at,
                   "Look at the gap between neighbours, not at the numbers themselves. How far is it from %d up to %d?" % (a, t1))))
    beats.append(B("%d minus %d is %d, and %d minus %d is %d too. So %s." % (t1, a, d, t2, t1, d, each),
                   W("d1", "%d − %d = %d" % (t1, a, d)), W("d2", "%d − %d = %d" % (t2, t1, d)),
                   NOTE("q", "%d, %d" % (a, t1), "+ %d" % d), NOTE("q", "%d, %d" % (t1, t2), "+ %d" % d)))

    choices, at = placed(qid, "jumps", "%d jumps" % (n - 1), ["%d jumps" % n, "%d jumps" % (n + 1)])
    beats.append(B("%s 1 is %d. To get from %s 1 to %s %d, how many jumps of %d do we make?" % (P, a, place, place, n, d),
                   ask=CHOOSE(choices, at,
                              "Count the jumps, not the %ss. From %s 1 to %s 2 is 1 jump, and to %s 3 is 2 jumps. "
                              "The jumps are always one fewer than the %s number." % (place, place, place, place, place))))
    beats.append(B("So we need %d minus 1, which is %d jumps. And %d jumps of %d is %d times %d, which is %d." % (
        n, n - 1, n - 1, d, n - 1, d, j),
        W("j1", "%d − 1 = %d" % (n, n - 1)), NOTE("j1", str(n - 1), "jumps", "below", last_nth("%d − 1 = %d" % (n, n - 1), str(n - 1))),
        W("j2", "%d × %d = %d" % (n - 1, d, j))))
    line = "%d + %d = %d" % (a, j, last)
    beats.append(B("Now add that %d to the %d we started with. %d plus %d is %d. %s" % (j, a, a, j, last, ending),
                   *ANSC("ans", line, last)))
    over = a + n * d
    beats.append(B(pick(qid, "trap", [
        "Here is the trap: making %d jumps, just because it is %s %d. That gives %d, which is really %s %d.",
        "Careful with the jumps. Making %d of them, because it is %s %d, gives %d. But that is %s %d.",
    ]) % (n, place, n, over, place, n + 1),
        W("t", "%d + %d × %d = %d" % (a, n, d, over)),
        NOTE("t", str(over), "%s %d" % (place, n + 1), "below", last_nth("%d + %d × %d = %d" % (a, n, d, over), str(over)))))
    rest = full[len(terms):]
    listing = ", ".join(str(x) for x in full)
    beats.append(B("Check by counting on, %d at a time, from %d: %s. That is %s %d, and it lands on %d." % (
        d, terms[-1], ", ".join(str(x) for x in rest), place, n, last),
        LB("c", listing), CIRC("c", str(last), last_nth(listing, str(last)))))
    beats.append(B(pick(qid, "sum", [
        "So when a pattern grows by the same amount each time: find the jump, count the jumps, which are one fewer than the place you want, multiply, and add to the start.",
        "So the plan is: find the jump, remember the jumps are one fewer than the place number, multiply the two, and add that to the first number.",
    ])))
    return LESSON(*beats)


# ── Rule: a short total (5 to 7 terms), written out and paired ───────────────

def ap_list_sum(qid, intro, given, a, d, n, place, places, each, ending, shown=3,
                options=(), aside=None, tail=None, summary=None):
    assert 5 <= n <= 7 and d > 0
    terms = [a + i * d for i in range(n)]
    last = terms[-1]
    s = a + last
    total = sum(terms)
    k = n // 2
    final = tail is None
    beats = [B(intro, GIVEN("q", given))]
    if aside:
        beats.append(aside)
    if shown >= 3:
        beats.append(_jump_beat(qid, terms, each, place, places, shown, d))
    else:
        beats.append(B("The story tells us the jump: %s." % each, LB("d1", "+ %d each %s" % (d, place))))

    choices, at = placed(qid, "need", "All %d amounts" % n, ["Only the amount for %s %d" % (place, n), "Only the amounts in the story"])
    beats.append(B(pick(qid, "needsay", [
        "The question asks for a total. What do we need before we can add anything up?",
        "We are after a total here. So what must we find first?",
    ]), ask=CHOOSE(choices, at,
                   "A total means every %s put together. The story only tells us some of them, so first we find all %d." % (place, n))))
    new = terms[shown:]
    listing = ", ".join(str(x) for x in terms)
    beats.append(B("Keep adding %d each time: %s. Now we have all %d." % (d, ", ".join(str(x) for x in new), n),
                   LB("list", listing)))
    in_opts = str(last) in [o.replace("₹", "").strip() for o in options]
    beats.append(B("Careful: %d is only %s %d%s. We want all %d %s together." % (
        last, place, n, ", and it is one of the choices" if in_opts else "", n, places),
        UL("list", str(last), last_nth(listing, str(last))), NOTE("list", str(last), "%s %d only" % (place, n), "below", last_nth(listing, str(last)))))
    beats.append(B("Here is a quick way to add them. Pair the first with the last: %d plus %d is %d. Now the second with the second last, %d and %d. What will they make?" % (
        a, last, s, terms[1], terms[-2]),
        W("p1", "%d + %d = %d" % (a, last, s)), ask=_pair_ask(qid, terms, d)))
    if n == 6:
        beats.append(B("%d plus %d is %d too, and so is %d plus %d. That is 3 pairs, each worth %d." % (
            terms[1], terms[4], s, terms[2], terms[3], s),
            W("p2", "%d + %d = %d" % (terms[1], terms[4], s)), W("p3", "%d + %d = %d" % (terms[2], terms[3], s))))
        line = "3 × %d = %d" % (s, total)
        say = "3 times %d is %d. %s" % (s, total, ending)
        beats.append(B(say, *(ANSC("tot", line, total) if final else [W("tot", line)])))
    else:
        mid = terms[k]
        assert 2 * mid == s
        if n == 7:
            beats.append(B("%d plus %d is %d too, and so is %d plus %d. That is 3 pairs worth %d, and the %d in the middle is left on its own." % (
                terms[1], terms[5], s, terms[2], terms[4], s, mid),
                W("p2", "%d + %d = %d" % (terms[1], terms[5], s)), W("p3", "%d + %d = %d" % (terms[2], terms[4], s)),
                BOX("list", str(mid), item_nth(terms, k))))
        else:
            beats.append(B("%d plus %d is %d too. That is 2 pairs worth %d, and the %d in the middle is left on its own." % (
                terms[1], terms[3], s, s, mid),
                W("p2", "%d + %d = %d" % (terms[1], terms[3], s)),
                BOX("list", str(mid), item_nth(terms, k))))
        line = "%d + %d = %d" % (k * s, mid, total)
        say = "%d times %d is %d, and %d plus the %d in the middle is %d. %s" % (k, s, k * s, k * s, mid, total, ending)
        beats.append(B(say, W("pk", "%d × %d = %d" % (k, s, k * s)), *(ANSC("tot", line, total) if final else [W("tot", line)])))
    beats.append(_check_beat(qid, terms, places))
    if tail:
        beats += tail
    beats.append(B(summary or pick(qid, "sum", [
        "So for a total like this: find the jump, write out every number, then pair them from the outside in and add.",
        "So the plan is: find the jump, list every number, and pair first with last to make the adding easy.",
    ])))
    return LESSON(*beats)


# ── Rule: a long total, from the last term and pairs ─────────────────────────

def ap_sum(qid, intro, given, a, d, n, place, places, each, ending, shown=3,
           options=(), trap=None, tail=None, summary=None):
    assert n >= 8
    terms = [a + i * d for i in range(n)]
    last = terms[-1]
    j = (n - 1) * d
    s = a + last
    total = sum(terms)
    final = tail is None
    beats = [B(intro, GIVEN("q", given))]
    beats.append(_jump_beat(qid, terms, each, place, places, shown, d))

    choices, at = placed(qid, "jumps", "%d jumps" % (n - 1), ["%d jumps" % n, "%d jumps" % (n + 1)])
    beats.append(B(pick(qid, "asksay", [
        "Adding %d numbers one by one is slow, so we will use a shortcut. For it we need the last one, %s %d. How many jumps of %d is that from %s 1?",
        "There are %d numbers to add, so let's find a quicker way. First we need %s %d, the last one. How many jumps of %d away from %s 1 is it?",
    ]) % (n, place, n, d, place),
        ask=CHOOSE(choices, at,
                   "Count the jumps, not the %s. From %s 1 to %s 2 is 1 jump, and to %s 3 is 2 jumps. "
                   "The jumps are always one fewer than the %s number." % (places, place, place, place, place))))
    jl = "%d − 1 = %d" % (n, n - 1)
    beats.append(B("%d minus 1 is %d jumps. And %d jumps of %d is %d." % (n, n - 1, n - 1, d, j),
                   W("j1", jl), NOTE("j1", str(n - 1), "jumps", "below", last_nth(jl, str(n - 1))),
                   W("j2", "%d × %d = %d" % (n - 1, d, j))))
    ll = "%d + %d = %d" % (a, j, last)
    beats.append(B("Add that to %s 1. %d plus %d is %d, so %s %d is %d." % (place, a, j, last, place, n, last),
                   W("l", ll), NOTE("l", str(last), "%s %d" % (place, n), "below", last_nth(ll, str(last)))))
    in_opts = str(last) in [o.replace("₹", "").strip() for o in options]
    beats.append(B(trap or ("Careful: %d is only %s %d%s. We want all %d %s together." % (
        last, place, n, ", and it is one of the choices" if in_opts else "", n, places)),
        UL("l", str(last), last_nth(ll, str(last)))))
    listing = "%d, %d, %d, … %d, %d, %d" % (terms[0], terms[1], terms[2], terms[-3], terms[-2], terms[-1])
    beats.append(B(pick(qid, "pairsay", [
        "Here is the shortcut. Pair the first with the last: %d plus %d is %d. Now pair the second with the second last, %d and %d. What will they make?",
        "Now the clever part. Put the first and the last together: %d plus %d is %d. Then take the second and the second last, %d and %d. What will they make?",
    ]) % (a, last, s, terms[1], terms[-2]),
        LB("list", listing), W("p1", "%d + %d = %d" % (a, last, s)), ask=_pair_ask(qid, terms, d)))
    beats.append(B(pick(qid, "every", [
        "%d plus %d is %d as well. Every pair, working inwards, makes %d.",
        "%d plus %d is %d too. Keep pairing inwards and every pair makes %d.",
    ]) % (terms[1], terms[-2], s, s), W("p2", "%d + %d = %d" % (terms[1], terms[-2], s))))
    k = n // 2
    if n % 2 == 0:
        line = "%d × %d = %d" % (k, s, total)
        beats.append(B("%d numbers make %d pairs, and each pair is worth %d. %d times %d is %d. %s" % (n, k, s, k, s, total, ending),
                       W("h", "%d ÷ 2 = %d" % (n, k)), *(ANSC("tot", line, total) if final else [W("tot", line)])))
    else:
        mid = terms[k]
        assert 2 * mid == s
        beats.append(B("%d numbers make %d pairs, with one number left over in the middle. %d pairs of %d is %d." % (n, k, k, s, k * s),
                       LB("h", "%d numbers = %d pairs + 1 in the middle" % (n, k)), W("pk", "%d × %d = %d" % (k, s, k * s))))
        beats.append(B("The middle one sits exactly halfway between %d and %d, so it is half of %d, which is %d." % (a, last, s, mid),
                       W("mid", "%d ÷ 2 = %d" % (s, mid))))
        line = "%d + %d = %d" % (k * s, mid, total)
        beats.append(B("%d plus %d is %d. %s" % (k * s, mid, total, ending),
                       *(ANSC("tot", line, total) if final else [W("tot", line)])))
    beats.append(_check_beat(qid, terms, places))
    if tail:
        beats += tail
    beats.append(B(summary or pick(qid, "sum", [
        "So for a long total: find the last number, pair the first with the last, and multiply by the number of pairs.",
        "So the plan for a long total is: work out the last number, add it to the first, and multiply by how many pairs there are.",
        "So remember the shortcut: last number first, then first plus last, then times the number of pairs.",
    ])))
    return LESSON(*beats)
