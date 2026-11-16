"""Look over a file of database-only questions before any of them enter the bank.

    python -X utf8 -I scripts/bank/review_import.py <export file> [--list <label or source>]

The export comes from the seed screen ("Download database-only questions"). This reads it
as data only and changes nothing. It reports where the questions came from, which topic
each would belong to, and what the mechanical checks find: shape, answer key, repeats
(inside the file and against the bank), decorative emoji, missing hints and steps.
It cannot tell whether a keyed answer is right: that needs each question worked.
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)
import bank  # noqa: E402

EMOJI = re.compile(u"[\U0001F000-\U0001FAFF☀-➿️]")


def norm(text):
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())


def problems_of(q):
    out = []
    opts = q.get("options")
    if not isinstance(opts, list) or len(opts) != 4:
        out.append("not four options")
    else:
        texts = [str(o.get("text", "")).strip() if isinstance(o, dict) else "" for o in opts]
        if any(not t for t in texts):
            out.append("an empty option")
        if len(set(norm(t) for t in texts)) < 4:
            out.append("two options the same")
    if q.get("correctAnswer") not in ("A", "B", "C", "D"):
        out.append("answer key is not A-D")
    if not (q.get("questionText") or "").strip():
        out.append("no question text")
    if q.get("difficulty") not in ("Easy", "Medium", "Hard"):
        out.append("odd difficulty")
    if EMOJI.search(q.get("questionText") or ""):
        out.append("emoji in the question")
    if not [h for h in (q.get("hints") or []) if str(h).strip()]:
        out.append("no hints")
    if not (q.get("stepByStep") or []):
        out.append("no steps")
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit(__doc__)
    with io.open(args[0], encoding="utf-8") as f:
        data = json.load(f)
    rows = data.get("questions") if isinstance(data, dict) else data
    if not isinstance(rows, list):
        raise SystemExit("No list of questions in that file.")
    wanted = sys.argv[sys.argv.index("--list") + 1] if "--list" in sys.argv else None

    in_bank = bank.load_bank()
    bank_ids = set(q["id"] for q in in_bank)
    bank_text = collections.defaultdict(list)
    for q in in_bank:
        bank_text[norm(q.get("questionText"))].append(q["id"])

    print("file: %s  (%d questions; exported %s; grade %s)" % (
        os.path.basename(args[0]), len(rows), data.get("exportedAt") if isinstance(data, dict) else "?",
        data.get("grade") if isinstance(data, dict) else "?"))
    print("already in the bank by id: %d" % sum(1 for q in rows if q.get("id") in bank_ids))

    by_source = collections.Counter(q.get("source") for q in rows)
    by_pool = collections.Counter(q.get("topicId") for q in rows)
    print("\nBY SOURCE: " + ", ".join("%s=%d" % kv for kv in by_source.most_common()))
    print("BY POOL:   " + ", ".join("%s=%d" % kv for kv in by_pool.most_common()))
    prefixes = collections.Counter(re.sub(r"[0-9a-f]{8}-[0-9a-f-]{20,}$", "<uuid>", re.sub(r"\d+$", "<n>", str(q.get("id")))) for q in rows)
    print("ID SHAPES: " + ", ".join("%s=%d" % kv for kv in prefixes.most_common(8)))

    seen = {}
    flagged = collections.Counter()
    per_q = {}
    repeats_in_file = 0
    repeats_of_bank = 0
    for q in rows:
        p = problems_of(q)
        key = norm(q.get("questionText"))
        if key in seen:
            p.append("repeats another question in this file")
            repeats_in_file += 1
        seen.setdefault(key, q.get("id"))
        if key and key in bank_text:
            p.append("same text as a bank question")
            repeats_of_bank += 1
        per_q[q.get("id")] = p
        for item in p:
            flagged[item] += 1
    clean = sum(1 for p in per_q.values() if not p)
    print("\nMECHANICAL CHECKS: %d of %d have nothing flagged" % (clean, len(rows)))
    for item, n in flagged.most_common():
        print("   %4d  %s" % (n, item))

    nodes = bank.tree_nodes()
    by_node = collections.defaultdict(list)
    for q in rows:
        by_node[bank.assign_node(q, nodes)].append(q)
    have = collections.Counter(q.get("node") for q in in_bank)
    names = {n["id"]: n["name"] for n in nodes}
    print("\nBY TOPIC (from the label): questions in this file / already in the bank, easy-medium-hard, and how many are clean")
    for node, qs in sorted(by_node.items(), key=lambda kv: -len(kv[1])):
        d = collections.Counter(q.get("difficulty") for q in qs)
        ok = sum(1 for q in qs if not per_q[q.get("id")])
        print("   %-34s %4d / %-4d  E%-3d M%-3d H%-3d  clean %d" % (
            (names.get(node, "no topic") if node else "NO TOPIC")[:34], len(qs), have.get(node, 0), d["Easy"], d["Medium"], d["Hard"], ok))

    no_topic = collections.Counter(q.get("subTopic") for q in by_node.get(None, []))
    if no_topic:
        print("\nLABELS WITH NO TOPIC: " + ", ".join("%s=%d" % kv for kv in no_topic.most_common(20)))

    labels = collections.Counter(q.get("subTopic") for q in rows)
    print("\nLABELS (%d distinct), commonest: %s" % (len(labels), ", ".join("%s=%d" % kv for kv in labels.most_common(12))))

    print("\nSAMPLES (one per source)")
    shown = set()
    for q in rows:
        s = q.get("source")
        if s in shown:
            continue
        shown.add(s)
        opts = " | ".join("%s) %s" % (o.get("id"), o.get("text")) for o in (q.get("options") or []) if isinstance(o, dict))
        print("   [%s] %s  (%s, %s)\n      %s\n      %s   key=%s" % (
            s, q.get("id"), q.get("subTopic"), q.get("difficulty"), (q.get("questionText") or "")[:220], opts[:200], q.get("correctAnswer")))

    if wanted:
        print("\nLISTING questions whose label or source contains %r" % wanted)
        for q in rows:
            if wanted.lower() in str(q.get("subTopic")).lower() or wanted.lower() in str(q.get("source")).lower():
                print("   %s [%s] %s" % (q.get("id"), ", ".join(per_q[q.get("id")]) or "clean", (q.get("questionText") or "")[:160]))


if __name__ == "__main__":
    main()
