"""Inventory of one grade's question bank: what is there, how it is filed, and what is missing.

    python -X utf8 scripts/audit/grade_bank.py 3
    python -X utf8 scripts/audit/grade_bank.py 4

Reads data/bank/ and the built narration, lesson and figure files. Changes nothing.
Reports, for the grade: questions per source and difficulty; per topic of the tree, how many
questions, their difficulty spread and how many are real past-paper questions; how much is
unsorted and what labels the unsorted questions carry; how complete the teaching layer is
(hints, steps, per-option notes, narration, lesson, figure); answer-key spread; exact repeats.
"""
import collections
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


def load(path):
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return {}
    with io.open(full, encoding="utf-8") as f:
        return json.load(f)


def norm(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def main():
    grade = int(sys.argv[1])
    rows = bank.load_bank(grade)
    nodes = bank.tree_nodes(grade)
    names = {n["id"]: n["name"] for n in nodes}
    speech = load("src/data/questionSpeech/speech.json")
    teach = load("src/data/teach/scripts.json")
    figures = load("src/data/questionFigures/figures.json")

    print("GRADE %d: %d questions, %d topics in the tree" % (grade, len(rows), len(nodes)))
    pools = collections.Counter(q.get("topicId") for q in rows)
    print("  database pools: " + ", ".join("%s %d" % kv for kv in pools.most_common(30)))

    print("\nBy source")
    by_source = collections.Counter(q.get("source") or "(none)" for q in rows)
    for s, n in by_source.most_common():
        print("  %-28s %5d" % (s, n))
    diff = collections.Counter(q.get("difficulty") for q in rows)
    print("\nBy difficulty: " + ", ".join("%s %d (%d%%)" % (k, v, round(100.0 * v / max(1, len(rows)))) for k, v in diff.most_common()))

    def is_real(q):
        s = (q.get("source") or "").lower()
        return "final" in s or "official" in s or "pyq" in s or re.search(r"ipm_?20\d\d", s) is not None

    print("\nBy topic (tree order)        total  Easy  Med Hard  real  noHints noSteps")
    by_node = collections.defaultdict(list)
    for q in rows:
        by_node[q.get("node")].append(q)
    for n in nodes:
        qs = by_node.get(n["id"], [])
        d = collections.Counter(q.get("difficulty") for q in qs)
        print("  %-28s %5d %5d %4d %4d %5d %8d %7d" % (
            n["name"][:28], len(qs), d.get("Easy", 0), d.get("Medium", 0), d.get("Hard", 0),
            sum(1 for q in qs if is_real(q)),
            sum(1 for q in qs if not any(q.get("hints") or [])),
            sum(1 for q in qs if not (q.get("stepByStep") or []))))
    unsorted = by_node.get(None, [])
    print("  %-28s %5d   (%d%% of the grade)" % ("(no topic)", len(unsorted), round(100.0 * len(unsorted) / max(1, len(rows)))))

    if unsorted:
        print("\nUnsorted questions: by source, then their commonest labels")
        for s, n in collections.Counter(q.get("source") or "(none)" for q in unsorted).most_common(12):
            print("  %-28s %5d" % (s, n))
        labels = collections.Counter((q.get("subTopic") or "(blank)")[:60] for q in unsorted)
        print("  %d different labels; the 25 commonest:" % len(labels))
        for label, n in labels.most_common(25):
            print("     %5d  %s" % (n, label))

    def share(test):
        return "%5d (%d%%)" % (sum(1 for q in rows if test(q)), round(100.0 * sum(1 for q in rows if test(q)) / max(1, len(rows))))

    print("\nTeaching layer (of %d)" % len(rows))
    print("  has 3 hints          " + share(lambda q: len([h for h in (q.get("hints") or []) if h]) >= 3))
    print("  has no hint          " + share(lambda q: not any(q.get("hints") or [])))
    print("  has worked steps     " + share(lambda q: bool(q.get("stepByStep"))))
    print("  has per-option notes " + share(lambda q: any((q.get("misconceptions") or {}).values())))
    print("  has narration        " + share(lambda q: q["id"] in speech))
    print("  has a lesson         " + share(lambda q: q["id"] in teach))
    print("  has a figure         " + share(lambda q: q["id"] in figures))

    keys = collections.Counter(q.get("correctAnswer") for q in rows)
    print("\nAnswer key spread: " + ", ".join("%s %d%%" % (k, round(100.0 * keys.get(k, 0) / max(1, len(rows)))) for k in "ABCD"))
    worst = []
    for s in by_source:
        qs = [q for q in rows if (q.get("source") or "(none)") == s]
        top = collections.Counter(q.get("correctAnswer") for q in qs).most_common(1)[0]
        if len(qs) >= 40 and top[1] > 0.4 * len(qs):
            worst.append("%s: %s is right in %d%% of %d" % (s, top[0], round(100.0 * top[1] / len(qs)), len(qs)))
    for w in worst:
        print("  lopsided  " + w)

    seen = collections.defaultdict(list)
    for q in rows:
        seen[norm(q.get("questionText"))].append(q)
    repeats = [v for v in seen.values() if len(v) > 1]
    print("\nExact repeats of the same wording: %d groups, %d questions beyond the first" % (len(repeats), sum(len(v) - 1 for v in repeats)))
    clash = [v for v in repeats if len({next((o["text"] for o in q["options"] if o["id"] == q.get("correctAnswer")), None) for q in v}) > 1]
    print("  of which the copies disagree on the right answer: %d groups" % len(clash))
    for v in clash[:8]:
        print("     %s | %s" % (", ".join(q["id"] for q in v[:3]), (v[0].get("questionText") or "")[:80].replace("\n", " ")))

    short = [q for q in rows if len((q.get("questionText") or "").strip()) < 12]
    same_opts = [q for q in rows if len({norm(o["text"]) for o in q["options"]}) < 4]
    print("\nSuspect rows: %d with a question under 12 characters, %d with two options the same" % (len(short), len(same_opts)))


if __name__ == "__main__":
    main()
