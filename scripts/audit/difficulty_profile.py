"""Difficulty profile of one or more grades, for comparing them.

    python -X utf8 scripts/audit/difficulty_profile.py 5 4

For each grade: the share of Easy / Medium / Hard overall, by kind of source, and by topic;
and, for the real past papers, how the label moves with a question's position on the paper
(the real papers run from easier to harder). Reads the bank; changes nothing.
"""
import collections
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bank"))
import bank  # noqa: E402

LEVELS = ("Easy", "Medium", "Hard")
REAL = re.compile(r"^(g\d_final_|g\d_mse_final_|g\d_mega_final_|mega_final_|previous_year_)\d{4}$")


def kind(q):
    s = q.get("source") or ""
    if REAL.match(s):
        return "real past papers"
    if s in ("hand_crafted", "g4_authored", "ipm_textbook", "pdf_extracted") or "worksheet" in s:
        return {"ipm_textbook": "textbook", "pdf_extracted": "worksheets", "hand_crafted": "hand-written", "g4_authored": "newly written"}.get(s, "worksheets")
    return "generated"


def share(qs):
    c = collections.Counter(q.get("difficulty") for q in qs)
    n = max(1, len(qs))
    return "%3d%% %3d%% %3d%%" % tuple(round(100.0 * c[l] / n) for l in LEVELS)


def position(q):
    m = re.search(r"(?:_Q|_)(\d{1,3})$", q["id"])
    return int(m.group(1)) if m else None


def main():
    for grade in [int(a) for a in sys.argv[1:]] or [5, 4]:
        rows = bank.load_bank(grade)
        names = {n["id"]: n["name"] for n in bank.tree_nodes(grade)}
        print("\nGRADE %d  (%d questions)                 Easy  Med Hard    n" % (grade, len(rows)))
        print("  %-34s %s %5d" % ("all", share(rows), len(rows)))
        by_kind = collections.defaultdict(list)
        for q in rows:
            by_kind[kind(q)].append(q)
        for k, qs in sorted(by_kind.items(), key=lambda kv: -len(kv[1])):
            print("  %-34s %s %5d" % (k, share(qs), len(qs)))
        real = by_kind.get("real past papers", [])
        thirds = collections.defaultdict(list)
        for q in real:
            p = position(q)
            if p:
                thirds["questions 1-13" if p <= 13 else "questions 14-26" if p <= 26 else "questions 27-40"].append(q)
        print("  real papers by position on the paper:")
        for k in ("questions 1-13", "questions 14-26", "questions 27-40"):
            if thirds.get(k):
                print("    %-32s %s %5d" % (k, share(thirds[k]), len(thirds[k])))
        print("  by topic:")
        by_node = collections.defaultdict(list)
        for q in rows:
            by_node[q.get("node")].append(q)
        for node, name in names.items():
            if by_node.get(node):
                r = [q for q in by_node[node] if kind(q) == "real past papers"]
                print("    %-32s %s %5d   real: %s (%d)" % (name[:32], share(by_node[node]), len(by_node[node]), share(r) if r else "-", len(r)))


if __name__ == "__main__":
    main()
