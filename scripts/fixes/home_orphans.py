"""Give every Grade 5 question that belongs to no topic a home.

    python -X utf8 scripts/fixes/home_orphans.py             # show what would change
    python -X utf8 scripts/fixes/home_orphans.py --samples   # ... with sample texts for each rule
    python -X utf8 scripts/fixes/home_orphans.py --write     # write the bank (data/bank/)

273 Grade 5 questions sat in data/bank/grade5/_unsorted.json: no topic key reached their
label (python -X utf8 scripts/audit/topic_classification.py 5 --all). The owner approved
three extra-practice topics for them (src/data/topicTree.ts, `extra: true`: not chapters of
the real paper, never in a mock test):

    gr5_counting      Counting & Number Formation   key "counting"
    gr5_measurement   Measurement                   key "measurement"
    gr5_mixed         Mixed Problem Solving         key "mixed"

Each orphan goes to the first rule below that fits it:
  1. TEXT_RULES: a label whose questions are of two kinds, told apart by their text;
  2. EXAM_RULES: a label whose questions clearly are an existing exam topic. A label is here
     only when its text is that topic's own work, in most cases because a real past-paper
     question of the same shape already sits in that topic (noted beside the rule);
  3. EXTRA_RULES: counting and measurement labels;
  4. MIXED_LABELS: everything else, to Mixed Problem Solving.
A label in none of the tables stops the script: add a rule for it.

The app still finds a topic's questions through the label (matchesSubTopicKey: the topic's
key must start a word in it), so each question gets `node` AND a label that its topic's key
reaches and no other key does. The old label stays readable inside the new one, in brackets.

EXISTING_RELABELS: six questions already filed under an exam topic carried a label with a
word the new keys reach ("Counting square numbers", "Improper to mixed fractions"), so the
app would have served them in an extra topic as well. They get a label without that word;
their `node` does not change.

Only `node` and `subTopic` change. Question text, options, answers, hints and steps are not
touched: the script checks this, and that no other question changes at all, before writing.
Running it again changes nothing. Afterwards run
    python -X utf8 scripts/speech/rehome.py --write
(narration is grouped by label) and the checks in scripts/bank/README.md.
"""
import argparse
import collections
import copy
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402  (scripts/bank/bank.py: the question bank, data/bank/)

POOL = "grade5"
PREFIX = "Grade 5 — "
EXTRA_NODES = ("gr5_counting", "gr5_measurement", "gr5_mixed")
PAST = re.compile(r"^(g\d_final_|g\d_mse_final_|g\d_mega_final_|mega_final_|previous_year_)(\d{4})$")

COUNTING = "Counting and number formation"
MIXED = "Mixed problem solving"

# 1. (old label, what the question text must match, node, new label)
TEXT_RULES = [
    # "Find the sum of first 14 even numbers." is a series, as "Sum of sequences" already is.
    (COUNTING, re.compile(r"^Find the sum of first \d+ (odd|even|natural) numbers\.?$"),
     "gr5_sequences", "Sum of sequences"),
    # "Find the area of a rectangle with length 23 cm and width 13 cm."
    ("Measurement", re.compile(r"^Find the (area|perimeter) of a (rectangle|square) with "),
     "gr5_area", "Area and perimeter"),
]

# 2. old label -> (node, new label). The comment is why the text is that exam topic.
EXAM_RULES = {
    # Equations: "Solve: 4x + 14 = 42"; "If x+y=12, y+z=16, z+x=10, find x+y+z."
    "Substitution": ("gr5_equations", "Equations (substitution)"),
    "System": ("gr5_equations", "Equations (system)"),
    "Multi-variable": ("gr5_equations", "Equations (multi-variable)"),
    "Rearrangement": ("gr5_equations", "Equations (rearrangement)"),
    # Divisibility, Factors & Primes: properties of primes and of multiples.
    "Prime digits": ("gr5_divisibility", "Divisibility (prime digits)"),
    "Prime number properties": ("gr5_divisibility", "Divisibility (prime number properties)"),
    "Number theory": ("gr5_divisibility", "Divisibility (number theory)"),
    # HCF & LCM: "The GCD and LCM of two numbers are 12 and 240 ..."; "smallest number which
    # when divided by 8, 10 and 12 leaves remainder 3".
    "Finding number": ("gr5_hcflcm", "HCF and LCM (finding number)"),
    "LCM remainders": ("gr5_hcflcm", "HCF and LCM (LCM remainders)"),
    # Square Numbers & Roots: "6² + Z² = 10². Find the value of Z."
    "Pythagorean relationship": ("gr5_squares", "Squares and square roots (Pythagorean relationship)"),
    # Ratio, Proportion & Variation (unitary method). Same shape as the real paper's
    # EXT_G5_FP_2019_009 (rice for 20 people in a week), EXT_G5_FP_2016_007 (overtime wage),
    # EXT_G5_FP_2019_029 (toys in 18 seconds).
    "Proportion": ("gr5_variation", "Ratio and proportion (proportion)"),
    "Wage calculation": ("gr5_variation", "Ratio and proportion (wage calculation)"),
    "Rate problems": ("gr5_variation", "Ratio and proportion (rate problems)"),
    # Addition & Subtraction. "Simultaneous conditions" is the real paper's EXT_G5_FP_2016_002
    # (three bags of apples); "Cryptarithmetic addition" is already in this topic.
    "Combined operations": ("gr5_operations1", "Addition and subtraction (combined operations)"),
    "Cryptarithmetic subtraction": ("gr5_operations1", "Addition and subtraction (cryptarithmetic subtraction)"),
    "Simultaneous conditions": ("gr5_operations1", "Addition and subtraction (simultaneous conditions)"),
    # Multiplication & Division: whole-number products, quotients and remainders. Real paper
    # questions of the same shape in this topic: EXT_G5_FP_2024_022 (find the divisor),
    # EXT_G5_FP_2020_033 (remainder of X + Y), EXT_G5_FP_2017_025 (which can be the product),
    # EXT_G5_FP_2019_013 (replace 4 mangoes by 3 apples).
    "Division": ("gr5_operations2", "Multiplication and division"),
    "Division relationship": ("gr5_operations2", "Multiplication and division (division relationship)"),
    "Finding the divisor": ("gr5_operations2", "Multiplication and division (finding the divisor)"),
    "Finding missing factor": ("gr5_operations2", "Multiplication and division (finding missing factor)"),
    "Difference of products": ("gr5_operations2", "Multiplication and division (difference of products)"),
    "Product properties": ("gr5_operations2", "Multiplication and division (product properties)"),
    "Product digit analysis": ("gr5_operations2", "Multiplication and division (product digit analysis)"),
    "Division error correction": ("gr5_operations2", "Multiplication and division (division error correction)"),
    "Operation error correction": ("gr5_operations2", "Multiplication and division (operation error correction)"),
    "Division with remainder": ("gr5_operations2", "Multiplication and division (division with remainder)"),
    "Remainder arithmetic": ("gr5_operations2", "Multiplication and division (remainder arithmetic)"),
    "Replacement word problem": ("gr5_operations2", "Multiplication and division (replacement word problem)"),
}

# 3. old label -> (node, new label). A label the key already reaches is kept as it is.
EXTRA_RULES = {
    COUNTING: ("gr5_counting", COUNTING),
    "Counting and forming numbers": ("gr5_counting", "Counting and forming numbers"),
    "Counting multiples": ("gr5_counting", "Counting multiples"),
    "Counting digits": ("gr5_counting", "Counting digits"),
    "Counting numbers": ("gr5_counting", "Counting numbers"),
    "Forming numbers": ("gr5_counting", COUNTING + " (forming numbers)"),
    "Measurement": ("gr5_measurement", "Measurement"),
}

# 4. old labels that go to Mixed Problem Solving as "Mixed problem solving (<old label>)".
MIXED_LABELS = [
    "Age problems", "Average", "Word problems", "Cost problems", "Equal distribution",
    "Error correction in accounts", "Sets and Venn diagrams", "Combinations", "Position problems",
    "Logical reasoning", "Even and odd number patterns", "Even/odd number patterns",
    "Even/odd number properties", "Odd/even number properties", "Odd/even combinations",
    "Number properties", "Consecutive even number sums", "Consecutive odd numbers",
    "Consecutive multiples", "Sum of consecutive numbers", "Sum of odd numbers",
    "Units digit patterns", "Doubling/exponential growth", "Unit conversion chain",
    "Division word problem", "Remainder problems",
]

# Questions already in an exam topic whose label a new key would also reach.
# id -> (the label it has, the label it gets). The node stays.
EXISTING_RELABELS = {
    "EXT_G5_WS_B3_010": ("Counting and multiplication", "Multiplication with a count"),
    "EXT_G5_WS_B7_004": ("Fractions and counting", "Fractions with a count"),
    "EXT_G5_WS_B5_020": ("Counting square numbers", "How many square numbers"),
    "EXT_G5_WS_B5_021": ("Counting even squares", "How many even squares"),
    "EXT_G5_WS_B5_022": ("Counting between squares", "How many between squares"),
    "EXT_G5_WS_B7_002": ("Improper to mixed fractions", "Converting improper fractions"),
}


def lower_first(label):
    return label[:1].lower() + label[1:]


def home_for(q):
    """(node, new label without the 'Grade 5 — ' opening, which table) for an orphan."""
    label = q.get("subTopic") or ""
    short = label[len(PREFIX):] if label.startswith(PREFIX) else label
    text = (q.get("questionText") or "").strip()
    for old, pattern, node, new in TEXT_RULES:
        if short == old and pattern.match(text):
            return node, new, "text"
    if short in EXAM_RULES:
        return EXAM_RULES[short] + ("exam",)
    if short in EXTRA_RULES:
        return EXTRA_RULES[short] + ("extra",)
    if short in MIXED_LABELS:
        return "gr5_mixed", "%s (%s)" % (MIXED, lower_first(short)), "mixed"
    return None


def reached(q, nodes):
    return [n["id"] for n in bank.candidate_nodes(q, nodes)]


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--samples", action="store_true", help="print up to three question texts for each rule")
    args = parser.parse_args()

    nodes = bank.tree_nodes()
    known = bank.node_by_id(nodes)
    for node_id in EXTRA_NODES:
        if node_id not in known:
            raise SystemExit("%s is not in src/data/topicTree.ts: add the node first" % node_id)

    questions = bank.load_bank()
    before = dict((q["id"], copy.deepcopy(q)) for q in questions)
    reached_before = dict((q["id"], reached(q, nodes)) for q in questions if q.get("topicId") == POOL)

    moves = collections.defaultdict(list)       # (old label, node, new label, table) -> questions
    relabels = []
    no_rule = collections.Counter()
    for q in questions:
        if q.get("topicId") != POOL:
            continue
        if q["id"] in EXISTING_RELABELS:
            old, new = EXISTING_RELABELS[q["id"]]
            if q.get("subTopic") == PREFIX + old:
                q["subTopic"] = PREFIX + new
                relabels.append((q, old, new))
            elif q.get("subTopic") != PREFIX + new:
                raise SystemExit("%s: label is %r, expected %r" % (q["id"], q.get("subTopic"), PREFIX + old))
            continue
        if q.get("node") is not None:
            continue
        home = home_for(q)
        if home is None:
            no_rule[q.get("subTopic")] += 1
            continue
        node, new, table = home
        old = q.get("subTopic")
        q["node"] = node
        q["subTopic"] = PREFIX + new
        moves[(old, node, PREFIX + new, table)].append(q)
    if no_rule:
        raise SystemExit("NO RULE for these labels, nothing written:\n  %s" % "\n  ".join(
            "%3d  %s" % (n, label) for label, n in no_rule.most_common()))

    # ── Checks: nothing but node and subTopic changed, and only where meant ────
    problems = []
    moved_ids = set(q["id"] for qs in moves.values() for q in qs)
    relabelled_ids = set(q["id"] for q, _, _ in relabels)
    for q in questions:
        old = before[q["id"]]
        for k in set(old) | set(q):
            if k not in ("node", "subTopic") and old.get(k) != q.get(k):
                problems.append("%s: %s changed" % (q["id"], k))
        if q["id"] in moved_ids:
            if old.get("node") is not None:
                problems.append("%s: had node %s already" % (q["id"], old.get("node")))
            if PAST.match(str(q.get("source"))):
                problems.append("%s: a real paper question (%s) would move" % (q["id"], q.get("source")))
        elif q["id"] in relabelled_ids:
            if old.get("node") != q.get("node"):
                problems.append("%s: node changed on a relabel" % q["id"])
        elif old != q:
            problems.append("%s: changed but is not in any rule" % q["id"])
        if q.get("topicId") != POOL:
            continue
        now = reached(q, nodes)
        if q.get("node") is None:
            problems.append("%s: still has no node" % q["id"])
        elif q["id"] in moved_ids or q["id"] in relabelled_ids:
            if now != [q["node"]]:
                problems.append("%s: label %r reaches %s, not only %s" % (q["id"], q["subTopic"], now or "no topic", q["node"]))
        else:
            # An untouched question: the new keys must not reach it, the old ones as before.
            if now != reached_before[q["id"]]:
                problems.append("%s: label %r now reaches %s (was %s)" % (q["id"], q["subTopic"], now, reached_before[q["id"]]))
            if [n for n in now if n in EXTRA_NODES and n != q["node"]]:
                problems.append("%s: label %r is reached by an extra topic but its node is %s" % (q["id"], q["subTopic"], q["node"]))
    if problems:
        raise SystemExit("%d PROBLEMS, nothing written\n  %s" % (len(problems), "\n  ".join(problems[:80])))

    # ── Report ───────────────────────────────────────────────────────────────
    order = {"text": 0, "exam": 1, "extra": 2, "mixed": 3}
    print("%-5s %-4s %-34s -> %-17s %s" % ("table", "n", "old label", "node", "new label"))
    for (old, node, new, table), qs in sorted(moves.items(), key=lambda kv: (order[kv[0][3]], kv[0][1], -len(kv[1]), kv[0][0])):
        print("%-5s %-4d %-34s -> %-17s %s" % (table, len(qs), old[len(PREFIX):], node, new[len(PREFIX):]))
        if args.samples:
            for q in qs[:3]:
                print("           %s: %s" % (q["id"], re.sub(r"\s+", " ", q["questionText"])[:200]))
    for q, old, new in relabels:
        print("label %-4d %-34s -> %-17s %s   (%s, node unchanged)" % (1, old, q["node"], new, q["id"]))
    per_node = collections.Counter()
    for (old, node, new, table), qs in moves.items():
        per_node[node] += len(qs)
    print("\n%d orphans homed:" % sum(per_node.values()))
    for node in sorted(per_node, key=lambda n: (n not in EXTRA_NODES, -per_node[n])):
        print("  %4d  %-17s %s%s" % (per_node[node], node, known[node]["name"], "  (extra practice)" if node in EXTRA_NODES else ""))
    print("%d questions of exam topics relabelled so that no extra topic's key reaches them" % len(relabels))
    left = sum(1 for q in questions if q.get("topicId") == POOL and q.get("node") is None)
    print("Grade 5 questions without a topic after this: %d" % left)

    if not args.write:
        print("nothing written (use --write)")
        return
    changed = bank.save_bank(questions)
    print("wrote %d bank files under %s" % (len(changed), os.path.relpath(bank.BANK, ROOT)))


if __name__ == "__main__":
    main()
