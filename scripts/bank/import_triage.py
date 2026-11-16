"""Sort a file of database-only questions into: cannot be kept, and worth working through.

    python -X utf8 -I scripts/bank/import_triage.py <export file> [--write]

Mechanical reasons a question cannot be kept (it is left out of the bank):
  - not four different, non-empty options, or an answer key that is not A-D
  - no question text, or text that is only a fragment (under 25 characters)
  - the same text as a question already in the bank, or as an earlier one in the file
  - a past-paper copy of a paper the bank already holds
Everything else is a candidate. Candidates still need their answers worked independently
before they may enter the bank; with --write they are written, WITHOUT their answer keys,
to data/bank-import/review/part-NN.json for that, and the keys to data/bank-import/keys.json.
Nothing in the bank changes.
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

OUT = os.path.join(bank.ROOT, "data", "bank-import")
PART_SIZE = 110


def norm(text):
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())


def words(text):
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


def reason_to_drop(q, seen, bank_text, bank_2020):
    opts = q.get("options")
    if not isinstance(opts, list) or len(opts) != 4:
        return "not four options"
    texts = [str(o.get("text", "")).strip() if isinstance(o, dict) else "" for o in opts]
    if any(not t for t in texts):
        return "an empty option"
    if len(set(norm(t) for t in texts)) < 4:
        return "two options the same"
    if q.get("correctAnswer") not in ("A", "B", "C", "D"):
        return "answer key is not A-D"
    text = (q.get("questionText") or "").strip()
    if len(text) < 25:
        return "question text is a fragment"
    key = norm(text)
    if key in bank_text:
        return "same text as a bank question"
    if key in seen:
        return "repeats an earlier question in the file"
    if str(q.get("source")) == "official_ipm_2020":
        w = words(text)
        for other in bank_2020:
            if len(w & other) >= 0.7 * max(1, min(len(w), len(other))):
                return "copy of a 2020 paper question the bank holds"
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        raise SystemExit(__doc__)
    with io.open(args[0], encoding="utf-8") as f:
        data = json.load(f)
    rows = data["questions"] if isinstance(data, dict) else data

    in_bank = bank.load_bank()
    bank_text = set(norm(q.get("questionText")) for q in in_bank)
    bank_2020 = [words(q.get("questionText")) for q in in_bank if q.get("source") == "g5_final_2020"]
    nodes = bank.tree_nodes()
    names = {n["id"]: n["name"] for n in nodes}

    seen = set()
    dropped = collections.defaultdict(collections.Counter)
    candidates = []
    for q in sorted(rows, key=lambda r: str(r.get("id"))):
        why = reason_to_drop(q, seen, bank_text, bank_2020)
        seen.add(norm(q.get("questionText")))
        if why:
            dropped[why][q.get("source")] += 1
        else:
            candidates.append(q)

    print("%d questions in the file" % len(rows))
    print("\nCANNOT BE KEPT: %d" % sum(sum(c.values()) for c in dropped.values()))
    for why, by in sorted(dropped.items(), key=lambda kv: -sum(kv[1].values())):
        print("   %4d  %-46s %s" % (sum(by.values()), why, ", ".join("%s=%d" % kv for kv in by.most_common())))

    print("\nCANDIDATES: %d  (%s)" % (len(candidates), ", ".join("%s=%d" % kv for kv in collections.Counter(q.get("source") for q in candidates).most_common())))
    per = collections.Counter(bank.assign_node(q, nodes) for q in candidates)
    have = collections.Counter(q.get("node") for q in in_bank)
    for node, n in per.most_common():
        print("   %-34s %4d candidates, %4d in the bank now" % ((names.get(node) or "NO TOPIC")[:34], n, have.get(node, 0)))

    if "--write" not in sys.argv:
        print("\nnothing written (use --write)")
        return
    review = os.path.join(OUT, "review")
    if not os.path.isdir(review):
        os.makedirs(review)
    keys = {}
    parts = [candidates[i:i + PART_SIZE] for i in range(0, len(candidates), PART_SIZE)]
    for n, part in enumerate(parts, 1):
        blind = []
        for q in part:
            keys[q["id"]] = q["correctAnswer"]
            blind.append({"id": q["id"], "topic": names.get(bank.assign_node(q, nodes)), "difficulty": q.get("difficulty"),
                          "question": q.get("questionText"), "options": {o["id"]: o["text"] for o in q["options"]}})
        with io.open(os.path.join(review, "part-%02d.json" % n), "w", encoding="utf-8", newline="\n") as f:
            json.dump(blind, f, ensure_ascii=False, indent=1)
            f.write("\n")
    with io.open(os.path.join(OUT, "keys.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(keys, f, ensure_ascii=False, indent=0, sort_keys=True)
        f.write("\n")
    with io.open(os.path.join(OUT, "candidates.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(candidates, f, ensure_ascii=False)
        f.write("\n")
    print("\nwrote %d review parts of up to %d questions (no answer keys in them), keys.json and candidates.json under data/bank-import/" % (len(parts), PART_SIZE))


if __name__ == "__main__":
    main()
