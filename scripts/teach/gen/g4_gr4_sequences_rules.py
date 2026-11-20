"""Lessons by rule for the generated families in gr4_sequences.

Three wordings:
  "Find the next number in the sequence: a, b, c, ?"            (same jump each time)
  "In an arithmetic sequence starting a, b, c, ..., find the nth term."
  "Find the next number: a, b, c, ?"                             (multiply each time)
Each rule reads the numbers from the question, computes every line and returns
beats, or None if the question is not of that wording.
"""
import re

from g4_gr4_sequences_lib import (ans, b, ch, fig, g, jumps, lab, mk, nt, ordinal, pick, qfig, seq, w)

TOPIC = "gr4_sequences"
GENERATED = ("PH3_", "VAR", "BOOST")


def _labelled_line(qid, d):
    """The question's own number line, with the size written on each hop."""
    spec = qfig(TOPIC, qid)
    if not spec or spec.get("kind") != "numberLine" or not spec.get("hops"):
        return None
    for hop in spec["hops"]:
        hop["label"] = "+%d" % d
    spec["note"] = "Every jump is the same size"
    return fig("f1", spec)


def _two_others(right, candidates):
    out = []
    for c in candidates:
        if c != right and c not in out and c > 0:
            out.append(c)
    return out[:2]


# ── "Find the next number in the sequence: 20, 35, 50, 65, ?" ────────────────

def next_same_jump(q):
    if not q["id"].startswith(GENERATED):
        return None
    m = re.match(r"^Find the next number in the sequence: ([\d, ]+), \?$", q["questionText"].strip())
    if not m:
        return None
    t = [int(x) for x in m.group(1).split(",")]
    d = t[1] - t[0]
    if len(t) < 3 or d <= 0 or any(t[i + 1] - t[i] != d for i in range(len(t) - 1)):
        return None
    qid = q["id"]
    last, nxt = t[-1], t[-1] + d
    spoken = ", ".join(str(x) for x in t)
    k = len(t)

    open_say = pick(qid, "open", [
        "Here is our pattern: %s, and then a gap. Let's find the number that fills it." % spoken,
        "Look at this list of numbers. %s. One more number is hiding at the end." % spoken,
        "Our numbers go %s. What comes next? Let's find out together." % spoken,
    ])
    ask1 = pick(qid, "ask1", [
        "Good pattern hunters look at the jumps. How big is the jump from %d to %d?" % (t[0], t[1]),
        "Start with the first two numbers. How far is it from %d up to %d?" % (t[0], t[1]),
        "To find the rule, we measure a jump. How much bigger is %d than %d?" % (t[1], t[0]),
    ])
    others1 = [str(x) for x in _two_others(d, [d + 1, d - 1, 2 * d, t[1]])]
    same_say = pick(qid, "same", [
        "Is it the same every time? %d minus %d is %d again. Every jump in this pattern is %d." % (t[2], t[1], d, d),
        "Now check the next pair. %d minus %d is %d as well. The jump never changes: it is always %d." % (t[2], t[1], d, d),
        "One jump is not enough to be sure. %d minus %d is also %d. So the rule is: add %d each time." % (t[2], t[1], d, d),
    ])
    ask2 = pick(qid, "ask2", [
        "So how do we get the number after %d?" % last,
        "We know the rule now. What do we do to %d to get the next number?" % last,
    ])
    end_say = pick(qid, "end", [
        "So here is the plan for a pattern like this. Find the jump between neighbours, check it stays the same, then add it once more.",
        "Remember the three moves. Measure a jump, check the other jumps match, then make one more jump from the last number.",
        "That is how we crack a pattern like this. Find the jump, make sure it never changes, and add it to the last number.",
    ])

    return [
        b(open_say, g("l1", seq(t, "?"), True)),
        b(ask1, ask=ch(str(d), others1,
                       "Count on from %d up to %d. %d take away %d leaves %d." % (t[0], t[1], t[1], t[0], d))),
        b("%d minus %d is %d. So the first jump is plus %d." % (t[1], t[0], d, d),
          w("l2", "%d − %d = %d" % (t[1], t[0], d)), nt("l1", ",", "+%d" % d), _labelled_line(qid, d)),
        b(same_say, w("l3", "%d − %d = %d" % (t[2], t[1], d)), jumps("l1", ["+%d" % d] * (k - 2), first=2)),
        b(ask2, ask=ch("add %d to %d" % (d, last), ["double %d" % last, "add %d to %d" % (2 * d, last)],
                       "This pattern grows by adding, and the jump is always %d. So we add %d to %d, just once." % (d, d, last))),
        b("%d plus %d is %d. So the next number is %d." % (last, d, nxt, nxt),
          ans("l4", "%d + %d = %d" % (last, d, nxt), str(nxt))),
        b("Quick check. From %d to %d is a jump of %d, the same as all the others. It fits." % (last, nxt, d),
          nt("l1", ",", "+%d" % d, "below", k), mk("l1", "?", "box")),
        b(end_say),
    ]


# ── "In an arithmetic sequence starting 6, 12, 18, ..., find the 10th term." ──

def nth_term(q):
    if not q["id"].startswith(GENERATED):
        return None
    m = re.match(r"^In an arithmetic sequence starting (\d+), (\d+), (\d+), \.\.\., find the (\d+)(?:st|nd|rd|th) term\.$",
                 q["questionText"].strip())
    if not m:
        return None
    a, t2, t3, n = (int(x) for x in m.groups())
    d = t2 - a
    if d <= 0 or t3 - t2 != d or n < 4:
        return None
    qid = q["id"]
    jumps_n = n - 1
    total = jumps_n * d
    answer = a + total
    nth = ordinal(n)

    open_say = pick(qid, "open", [
        "Our pattern starts %d, %d, %d, and keeps going. A term is just a number in the pattern. We want the %s one." % (a, t2, t3, nth),
        "This pattern begins %d, %d, %d, and goes on and on. Each number in it is called a term. We are after the %s term." % (a, t2, t3, nth),
    ])
    jump_say = pick(qid, "jump", [
        "First, the jump. %d minus %d is %d, and %d minus %d is %d too. So each term is %d more than the one before." % (t2, a, d, t3, t2, d, d),
        "How does it grow? %d minus %d is %d. %d minus %d is %d again. So we add %d every time." % (t2, a, d, t3, t2, d, d),
    ])
    ask_jumps = pick(qid, "askj", [
        "We could keep adding %d all the way, but that is slow. To go from the 1st term to the %s term, how many jumps do we make?" % (d, nth),
        "Let's take a short cut and count the jumps. From the 1st term to the %s term, how many jumps are there?" % nth,
    ])
    trap_say = pick(qid, "trap", [
        "Careful here, this is the trap. The 1st term is already there before any jump. So we need 1 fewer jump than %d. That is %d jumps." % (n, jumps_n),
        "This is where many children slip. The 1st term needs no jump at all. So the jumps are 1 fewer than %d, which is %d." % (n, jumps_n),
    ])
    end_say = pick(qid, "end", [
        "So for any term far along a pattern: find the jump, make 1 fewer jump than the term number, and add them to the 1st term.",
        "Here is the plan to keep. Find the jump. Count 1 fewer jump than the term number. Multiply, then add the 1st term.",
    ])

    beats = [
        b(open_say, g("l1", "%d, %d, %d, ..." % (a, t2, t3), True), g("l1b", "%s term = ?" % nth, True)),
        b(jump_say, w("l2", "%d − %d = %d" % (t2, a, d)), w("l3", "%d − %d = %d" % (t3, t2, d)),
          jumps("l1", ["+%d" % d, "+%d" % d]), _labelled_line(qid, d)),
        b(ask_jumps, ask=ch(str(jumps_n), [str(n), str(n + 1)],
                            "Count on your fingers. From the 1st term to the 2nd is 1 jump. From the 1st to the 3rd is 2 jumps. The jumps are always 1 fewer than the term number.")),
        b(trap_say, w("l4", "%d − 1 = %d" % (n, jumps_n)), lab("l4b", "%d jumps of %d" % (jumps_n, d))),
        b("Let's test that on a term we can see. The 3rd term should be the 1st term plus 2 jumps. %d plus 2 times %d is %d. It matches." % (a, d, t3),
          w("l5", "%d + 2 × %d = %d" % (a, d, t3))),
    ]
    tens, ones = (jumps_n // 10) * 10, jumps_n % 10
    if jumps_n > 12 and ones:
        p1, p2 = tens * d, ones * d
        beats.append(b("Now, %d jumps of %d. That is easier in two parts. %d times %d is %d, and %d times %d is %d." % (jumps_n, d, tens, d, p1, ones, d, p2),
                       w("l6", "%d × %d = %d" % (tens, d, p1)), w("l7", "%d × %d = %d" % (ones, d, p2))))
        beats.append(b("%d plus %d makes %d. So %d jumps of %d carry us %d forward." % (p1, p2, total, jumps_n, d, total),
                       w("l8", "%d × %d = %d" % (jumps_n, d, total))))
    else:
        beats.append(b("Now, %d jumps of %d. %d times %d is %d. So the jumps carry us %d forward." % (jumps_n, d, jumps_n, d, total, total),
                       w("l8", "%d × %d = %d" % (jumps_n, d, total))))
    beats += [
        b("We have %d from the jumps. What do we do with it?" % total,
          ask=ch("add it to the 1st term, %d" % a, ["nothing, %d is the answer" % total, "add it to %d" % t3],
                 "The jumps begin at the 1st term, which is %d. So the %d must be added on to %d." % (a, total, a))),
        b("%d plus %d is %d. So the %s term is %d." % (a, total, answer, nth, answer),
          ans("l9", "%d + %d = %d" % (a, total, answer), str(answer))),
        b(end_say),
    ]
    return beats


# ── "Find the next number: 3, 6, 12, 24, 48, ?" ──────────────────────────────

def next_multiply(q):
    if not q["id"].startswith(GENERATED):
        return None
    m = re.match(r"^Find the next number: ([\d, ]+), \?$", q["questionText"].strip())
    if not m:
        return None
    t = [int(x) for x in m.group(1).split(",")]
    if len(t) < 3 or t[0] <= 0 or t[1] % t[0]:
        return None
    r = t[1] // t[0]
    if r < 2 or any(t[i + 1] != t[i] * r for i in range(len(t) - 1)):
        return None
    qid = q["id"]
    last, nxt = t[-1], t[-1] * r
    spoken = ", ".join(str(x) for x in t)
    j = [t[i + 1] - t[i] for i in range(len(t) - 1)]
    shown = j[:3]
    times_word = "double" if r == 2 else "%d times" % r

    open_say = pick(qid, "open", [
        "Here is our pattern: %s, and then a gap. Let's work out what comes next." % spoken,
        "Look at these numbers. %s. They grow fast! One more is hiding at the end." % spoken,
    ])
    if len(shown) == 3:
        jump_say = "Let's try the jumps first. They are %d, then %d, then %d. The jump keeps changing, so this is not a plain adding pattern." % tuple(shown)
    else:
        jump_say = "Let's try the jumps first. They are %d and then %d. The jump changes, so this is not a plain adding pattern." % tuple(shown)
    ask_say = pick(qid, "ask", [
        "The jumps did not help. So let's think about multiplying. Which rule works for every step?",
        "When adding does not fit, try times. Which of these rules works at every step?",
    ])
    lines = [w("m1", "%d × %d = %d" % (t[0], r, t[1])), w("m2", "%d × %d = %d" % (t[1], r, t[2]))]
    rule_say = "%d times %d is %d. %d times %d is %d." % (t[0], r, t[1], t[1], r, t[2])
    if len(t) >= 4:
        lines.append(w("m3", "%d × %d = %d" % (t[2], r, t[3])))
        rule_say += " %d times %d is %d." % (t[2], r, t[3])
    rule_say += " Each number is %s the one before." % times_word
    end_say = pick(qid, "end", [
        "So when the jumps keep changing, try multiplying. Find what each number is multiplied by, then do it once more.",
        "Keep this in mind. If adding does not fit a pattern, test times. Find the multiplier, then use it on the last number.",
    ])

    beats = [
        b(open_say, g("l1", seq(t, "?"), True)),
        b(jump_say, jumps("l1", ["+%d" % x for x in shown])),
        b(ask_say, ask=ch("multiply by %d each time" % r, ["add %d each time" % j[0], "add %d each time" % j[1]],
                          "Adding %d works for the first step, but not for the next one. Multiplying works every time: %d times %d is %d, and %d times %d is %d." % (j[0], t[0], r, t[1], t[1], r, t[2]))),
        b(rule_say, lines),
    ]
    if last >= 100:
        hundreds, rest = (last // 100) * 100, last % 100
        p1, p2 = hundreds * r, rest * r
        beats.append(b("So the next number is %d times %d. Let's do it in two parts. %d times %d is %d, and %d times %d is %d." % (last, r, hundreds, r, p1, rest, r, p2),
                       w("m4", "%d × %d = %d" % (hundreds, r, p1)), w("m5", "%d × %d = %d" % (rest, r, p2))))
        beats.append(b("%d plus %d makes %d. So the next number is %d." % (p1, p2, nxt, nxt),
                       ans("m6", "%d × %d = %d" % (last, r, nxt), str(nxt))))
    else:
        beats.append(b("So we multiply the last number by %d. %d times %d is %d. The next number is %d." % (r, last, r, nxt, nxt),
                       ans("m6", "%d × %d = %d" % (last, r, nxt), str(nxt))))
    beats += [
        b("Let's check by going backwards. %d divided by %d takes us back to %d. It fits." % (nxt, r, last),
          w("m7", "%d ÷ %d = %d" % (nxt, r, last)), mk("l1", "?", "box")),
        b(end_say),
    ]
    return beats


RULES = [next_same_jump, nth_term, next_multiply]
