"""Are a grade's questions filed under the right topic? Reads data files only; changes nothing.

    python -X utf8 scripts/audit/topic_classification.py [grade] [--all]

A question reaches a topic when the topic's key (subTopicKey in src/data/topicTree.ts)
starts a word in the question's subTopic label (matchesSubTopicKey in
src/lib/sharedUtils.ts). For one grade (default 5) this reports:
  1. questions no topic can reach, by label, with the topic their text suggests, and
     the generated variants whose topic is only in their id;
  2. labels that reach more than one topic;
  3. for each topic, whether the practice ladder (src/lib/practice/ladder.ts rules:
     Warm-up = Easy, Build = Medium, Challenge = Hard, Exam = real past papers) has
     enough questions at each step, and whether its last step is real or exam-style;
  4. questions whose text does not look like their topic and does look like another;
  5. the real past-paper questions: how many reach no topic or several.
Lists are cut to the first few lines; --all prints them in full.
The text checks in part 4 are cheap word tests: a suspect is a question to read, not a verdict.
"""
import collections
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402  (scripts/bank/bank.py: the question bank, data/bank/)

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
GRADE = int(ARGS[0]) if ARGS else 5
SHOW_ALL = "--all" in sys.argv[1:]
PAST = re.compile(r"^(g\d_final_|g\d_mse_final_|g\d_mega_final_|mega_final_|previous_year_)(\d{4})$")
VARIANT_ID = re.compile(r"^VAR_G(\d+)_vary_(.+)_V\d+$")

# The ladder's numbers (src/lib/practice/ladder.ts).
NEEDED = 3          # right answers to finish a step
THIN = 6            # fewer fresh questions than this at a step is thin (14-day no-repeat)
EXAM_REAL_MIN = 3   # fewer real paper questions than this and the last step is "Exam-style"

# Generated variants carry their family in the id: VAR_G5_vary_<family>_V<n>.
# family -> the topic key it belongs to. Mirrors VARIANT_FAMILIES in ladder.ts.
VARIANT_FAMILY = {
    5: {
        "bodmas": "bodmas", "angles": "angle", "percentage": "money", "equation": "equation",
        "perimeter_area": "area", "hcf_lcm": "hcf", "simple_interest": "interest",
        "fraction_arithmetic": "fraction",
    },
}
# The label a repaired variant should carry (the wording the real papers use).
PROPOSED_LABEL = {
    "bodmas": "BODMAS", "angle": "Angles", "money": "Percentage (money)", "equation": "Equations",
    "area": "Area and perimeter", "hcf": "HCF and LCM", "interest": "Simple interest", "fraction": "Fractions",
}

# Broad: words a question of this topic nearly always has (tested on the text and the choices).
OWN = {
    "place value": r"place value|face value|digit|numeral|expanded|lakh|crore|million|thousand|hundred|ascending|descending|greatest|smallest|largest|round|successor|predecessor|roman|in words|in figures|number",
    "addition": r"\+|sum|add|subtract|difference|minus|total|altogether|left|more than|less than|−|\d\s*-\s*\d|remain|how many",
    "multiplication": r"×|\*|multipl|product|divid|÷|quotient|remainder|times|each|per\b|share|equal",
    "divisib": r"divisib|factor|multiple|prime|composite|even|odd|remainder|divid",
    "integer": r"integer|negative|[−-]\s*\d|below zero|number line|temperature|positive",
    "bodmas": r"simplif|bodmas|bracket|[(\[{]|[+−×÷*/-].*[+−×÷*/-]|value of|evaluate|solve|\bof\b",
    "square": r"square|√|root|perfect|\^2|²",
    "hcf": r"hcf|lcm|h\.c\.f|l\.c\.m|common|gcd|together|bell|largest|greatest|least|smallest|divisible|multiple|factor",
    "algebra": r"express|term|coefficient|variable|constant|[a-z]\s*[=+−-]|\d[a-z]\b|value of|simplif|polynomial",
    "equation": r"=|equation|solve|find|value of|unknown|number|age|sum",
    "fraction": r"fraction|\d\s*/\s*\d|\\frac|half|halves|third|quarter|fifth|numerator|denominator|mixed|improper|reciprocal|part|shaded",
    "decimal": r"decimal|\d\.\d|tenth|hundredth|point",
    "sequence": r"sequence|series|pattern|next|term|missing|\d\s*,\s*\d+\s*,|\.\.\.|…|_",
    "ratio": r"ratio|proportion|\d\s*:\s*\d|unitary|vari|cost|if \d|how many|how much|per\b|each|share|divide",
    "money": r"percent|%|rs\.?|₹|rupee|paise|money|cost|price|pay|paid|bill|discount|spend|spent|save|buy|bought",
    "percentage": r"percent|%|rs\.?|₹|rupee|profit|loss|discount|interest|rate",
    "profit": r"profit|loss|gain|c\.?p\.?|s\.?p\.?|cost price|selling price|sold|sell|bought|buy",
    "interest": r"interest|principal|rate|per annum|p\.a|amount|s\.i|year",
    "speed": r"speed|km|distance|hour|minute|second|time|train|travel|m/s|fast|walk|run|cover",
    "angle": r"angle|°|degree|line|parallel|perpendicular|acute|obtuse|reflex|complement|supplement|clock|ray|turn",
    "triangle": r"triangle|isosceles|equilateral|scalene|hypotenuse|vertex|vertices|sides",
    "area": r"area|perimeter|rectangle|square|length|breadth|side|cm|sq|m²|fence|boundary|circumference|tile|floor|field|wall",
    # The extra-practice topics (extra: true in the tree). "mixed" holds whatever no other
    # topic covers, so any text is its own.
    "counting": r"how many|digit|number|formed|count|multiple|even|odd|page",
    "measurement": r"\bkg\b|\bg\b|gram|litre|\bml\b|\bcm\b|\bmm\b|\bkm\b|\bm\b|metre|convert|weigh|capacity|length",
    "mixed": r".",
}
# Narrow: words that all but name a topic (tested on the question text only).
STRONG = {
    "place value": r"place value|face value|expanded form|number name|in words",
    "divisib": r"divisib|\bprime\b|composite number",
    "integer": r"\bintegers?\b",
    "bodmas": r"bodmas|simplify\s*:",
    "square": r"square root|perfect square|√|square of",
    "hcf": r"\bhcf\b|\blcm\b|h\.c\.f|l\.c\.m|highest common|lowest common|least common multiple",
    "algebra": r"algebraic|coefficient|like terms",
    "equation": r"\bequations?\b|solve for|solve\s*:",
    "fraction": r"fraction|numerator|denominator",
    "decimal": r"\bdecimals?\b",
    "sequence": r"sequence|series|next term|next number|pattern",
    "ratio": r"\bratio\b|proportion",
    "money": r"percent|\d\s*%",
    "percentage": r"percent|\d\s*%",
    "profit": r"profit|\bloss\b|selling price|cost price",
    "interest": r"simple interest|per annum|\bprincipal\b",
    "speed": r"\bspeed\b|km/h|kmph|km per hour",
    "angle": r"\bangles?\b|\d\s*°",
    "triangle": r"\btriangles?\b",
    "area": r"\barea\b|perimeter",
}
OWN_RE = dict((k, re.compile(v)) for k, v in OWN.items())
STRONG_RE = dict((k, re.compile(v)) for k, v in STRONG.items())


load_seed = bank.load_bank
matches = bank.matches  # same rule as matchesSubTopicKey: the key must start a word


EXTRA_NODE = re.compile(r"\{\s*id:\s*'([^']+)'[^}\n]*\bextra:\s*true")


def extra_node_ids():
    """Ids of the extra-practice topics (`extra: true` in src/data/topicTree.ts): not
    chapters of the real paper, so they hold no real paper questions by design."""
    with open(bank.TREE, encoding="utf-8") as f:
        return set(EXTRA_NODE.findall(f.read()))


def tree_nodes(grade):
    """The grade's topics that have a subTopicKey."""
    return [n for n in bank.tree_nodes(grade) if n["key"]]


def text_of(q):
    return (q.get("questionText") or "").lower()


def choices_of(q):
    out = []
    for o in q.get("options") or []:
        out.append(o.get("text", "") if isinstance(o, dict) else str(o))
    return " ".join(out).lower()


def looks_like(q, skip=()):
    """Topic keys the question text all but names, apart from those in `skip`."""
    t = text_of(q)
    return [k for k in sorted(STRONG_RE) if k not in skip and STRONG_RE[k].search(t)]


def short(label):
    return re.sub(r"^Grade \d+ \S+ ", "", label or "(none)")


def emh(rows):
    d = collections.Counter(r.get("difficulty") for r in rows)
    return "%d/%d/%d" % (d["Easy"], d["Medium"], d["Hard"])


def cut(rows, limit):
    rows = list(rows)
    if SHOW_ALL or len(rows) <= limit:
        return rows, 0
    return rows[:limit], len(rows) - limit


def main():
    nodes = tree_nodes(GRADE)
    if not nodes:
        print("GRADE %d has no topics with a subTopicKey in the tree (Grade 4 uses chapter topics): nothing to check" % GRADE)
        return
    keys = [n["key"] for n in nodes]
    extra_ids = extra_node_ids()
    extra_keys = [n["key"] for n in nodes if n["id"] in extra_ids]
    name_of = dict((n["key"], n["name"]) for n in nodes)
    db_ids = sorted(set(n["db"] for n in nodes))
    pool = [q for q in load_seed() if q.get("topicId") in db_ids]
    hit = dict((q["id"], [k for k in keys if matches(q.get("subTopic"), k)]) for q in pool)
    is_real = dict((q["id"], bool(PAST.match(str(q.get("source"))))) for q in pool)
    family = VARIANT_FAMILY.get(GRADE, {})

    def variant_key(q):
        m = VARIANT_ID.match(q["id"])
        return family.get(m.group(2)) if m and int(m.group(1)) == GRADE else None

    print("GRADE %d: %d questions in the bank (%s), %d topics, %d distinct labels" % (
        GRADE, len(pool), ", ".join(db_ids), len(nodes), len(set(q.get("subTopic") for q in pool))))

    # ── 1 ────────────────────────────────────────────────────────────────────
    none = [q for q in pool if not hit[q["id"]]]
    print("\n1. QUESTIONS NO TOPIC CAN REACH: %d of %d (%d of them real paper questions)" % (
        len(none), len(pool), sum(1 for q in none if is_real[q["id"]])))
    by_label = collections.defaultdict(list)
    for q in none:
        by_label[q.get("subTopic")].append(q)
    print("   %-42s %4s  %-9s %4s  %s" % ("label", "n", "E/M/H", "real", "what the text suggests"))
    rows, more = cut(sorted(by_label.items(), key=lambda kv: -len(kv[1])), 30)
    for label, qs in rows:
        guess = collections.Counter()
        for q in qs:
            names = looks_like(q)
            guess[names[0] if len(names) == 1 else ("several" if names else "nothing")] += 1
        print("   %-42s %4d  %-9s %4d  %s" % (
            short(label)[:42], len(qs), emh(qs), sum(1 for q in qs if is_real[q["id"]]),
            ", ".join("%s %d" % (k, n) for k, n in guess.most_common(4))))
    if more:
        print("   ... and %d more labels (--all)" % more)

    print("\n   GENERATED VARIANTS WHOSE TOPIC IS ONLY IN THEIR ID (VAR_G%d_vary_<family>_V<n>)" % GRADE)
    fam = collections.defaultdict(list)
    for q in pool:
        m = VARIANT_ID.match(q["id"])
        if m and int(m.group(1)) == GRADE:
            fam[m.group(2)].append(q)
    if not fam:
        print("   none")
    repairable = 0
    for name in sorted(fam, key=lambda f: -len(fam[f])):
        qs = fam[name]
        unreached = [q for q in qs if not hit[q["id"]]]
        key = family.get(name)
        if key:
            label = "Grade %d — %s" % (GRADE, PROPOSED_LABEL.get(key, key))
            reach = [k for k in keys if matches(label, k)]
            agree = sum(1 for q in qs if key in looks_like(q) or (key in OWN_RE and OWN_RE[key].search(text_of(q) + " " + choices_of(q))))
            verdict = "OK" if reach == [key] else "CHECK: that label reaches %s" % (reach or "no topic")
            repairable += len(unreached) if reach == [key] else 0
            print("   %-20s %4d (%3d unreached, %s)  -> %-9s as '%s'  [%s; text agrees for %d of %d]" % (
                name, len(qs), len(unreached), emh(qs), key, label, verdict, agree, len(qs)))
        else:
            print("   %-20s %4d (%3d unreached, %s)  -> NO FAMILY RULE: add one to VARIANT_FAMILY here and in ladder.ts" % (
                name, len(qs), len(unreached), emh(qs)))
    print("   relabelling these by family would make %d questions reachable" % repairable)

    # ── 2 ────────────────────────────────────────────────────────────────────
    several = [q for q in pool if len(hit[q["id"]]) > 1]
    print("\n2. LABELS THAT REACH MORE THAN ONE TOPIC: %d questions (each is served, and counted, in every topic listed)" % len(several))
    by_label = collections.defaultdict(list)
    for q in several:
        by_label[q.get("subTopic")].append(q)
    rows, more = cut(sorted(by_label.items(), key=lambda kv: -len(kv[1])), 25)
    for label, qs in rows:
        print("   %-46s %4d  -> %s" % (short(label)[:46], len(qs), " + ".join(hit[qs[0]["id"]])))
    if more:
        print("   ... and %d more labels (--all)" % more)

    # ── 3 ────────────────────────────────────────────────────────────────────
    print("\n3. THE PRACTICE LADDER, TOPIC BY TOPIC (a step needs %d right; under %d questions is thin; 0 = step skipped)" % (NEEDED, THIN))
    print("   counts are by label, with generated variants reached by id shown after '+'")
    print("   %-30s %-10s %8s %8s %8s  %-18s %s" % ("topic", "key", "warm-up", "build", "challng", "real exam (E/M/H)", "notes"))
    for n in nodes:
        key = n["key"]
        mine = [q for q in pool if key in hit[q["id"]]]
        extra = [q for q in pool if key not in hit[q["id"]] and variant_key(q) == key]
        real = [q for q in mine if is_real[q["id"]]]
        cells, notes = [], []
        for d, step in (("Easy", "warm-up"), ("Medium", "build"), ("Hard", "challenge")):
            a = sum(1 for q in mine if not is_real[q["id"]] and q.get("difficulty") == d)
            b = sum(1 for q in extra if q.get("difficulty") == d)
            cells.append("%d+%d" % (a, b) if b else "%d" % a)
            if a + b == 0:
                notes.append("no %s" % step)
            elif a + b < THIN:
                notes.append("thin %s" % step)
        if not mine and not extra:
            notes = ["NO QUESTIONS: no ladder, practice has nothing to serve"]
        elif n["id"] in extra_ids:
            notes.append("extra practice: exam-style by design" if not real else "EXTRA PRACTICE HOLDS %d REAL PAPER QUESTIONS" % len(real))
        elif len(real) < EXAM_REAL_MIN:
            notes.append("EXAM-STYLE ONLY (%d real)" % len(real))
        elif len(real) < THIN:
            notes.append("thin exam")
        print("   %-30s %-10s %8s %8s %8s  %3d (%-9s)    %s" % (
            n["name"][:30], key, cells[0], cells[1], cells[2], len(real), emh(real), "; ".join(notes)))

    # ── 4 ────────────────────────────────────────────────────────────────────
    print("\n4. LOOKS MIS-FILED: the text has none of its own topic's words and all but names another topic")
    print("   ('unclear' = none of its own topic's words, and no other topic named either)")
    total = 0
    for n in nodes:
        key = n["key"]
        if key not in OWN_RE:
            print("   %-30s no word test written for key '%s'" % (n["name"][:30], key))
            continue
        mine = [q for q in pool if key in hit[q["id"]]]
        suspects, unclear = [], 0
        for q in mine:
            own = hit[q["id"]]
            body = text_of(q) + " " + choices_of(q)
            if any(k in OWN_RE and OWN_RE[k].search(body) for k in own):
                continue
            other = looks_like(q, skip=own)
            if other:
                suspects.append((q, other))
            else:
                unclear += 1
        total += len(suspects)
        if not mine:
            continue
        print("   %-30s %4d checked, %3d suspect, %3d unclear" % (n["name"][:30], len(mine), len(suspects), unclear))
        rows, more = cut(suspects, 8)
        for q, other in rows:
            print("      %-26s '%s' looks like %s: %s" % (
                q["id"], short(q.get("subTopic"))[:28], "/".join(other), re.sub(r"\s+", " ", q.get("questionText") or "")[:70]))
        if more:
            print("      ... and %d more (--all)" % more)
    print("   suspects in all: %d" % total)

    # ── 5 ────────────────────────────────────────────────────────────────────
    real = [q for q in pool if is_real[q["id"]]]
    print("\n5. REAL PAST-PAPER QUESTIONS: %d held; %d reach no topic, %d reach several" % (
        len(real), sum(1 for q in real if not hit[q["id"]]), sum(1 for q in real if len(hit[q["id"]]) > 1)))
    if extra_keys:
        print("   in an extra-practice topic (%s): %d (must be 0: extra practice is not part of the real paper)" % (
            ", ".join(extra_keys), sum(1 for q in real if any(k in extra_keys for k in hit[q["id"]]))))
    lost = collections.Counter(short(q.get("subTopic")) for q in real if not hit[q["id"]])
    for label, c in lost.most_common():
        print("   reaches no topic: %-40s %3d" % (label[:40], c))
    per = collections.Counter()
    for q in real:
        for k in hit[q["id"]]:
            per[k] += 1
    print("   per topic: %s" % ", ".join("%s %d" % (name_of[k][:18], per[k]) for k in sorted(keys, key=lambda k: -per[k])))


if __name__ == "__main__":
    main()
