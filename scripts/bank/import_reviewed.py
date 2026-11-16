"""Bring independently checked database-only questions into the bank.

    python -X utf8 -I scripts/bank/import_reviewed.py            # report only
    python -X utf8 -I scripts/bank/import_reviewed.py --write    # add the passing questions to the bank

Inputs, all under data/bank-import/ (written by import_triage.py and the checkers):
  candidates.json          the questions, as exported
  keys.json                their answer keys
  answers/part-NN.json     each question worked from scratch by a checker who did not see the key

A question enters the bank only when ALL of these hold:
  - the checker reached a definite answer, was sure, and raised no issue;
  - that answer is the keyed answer;
  - it is not a near-copy of a question already kept (same topic, same numbers in the
    text, same right answer) or of one in the bank.
Everything else is left out. For topics that would otherwise have no questions at all,
the ones left out are listed in data/bank-import/repair.json to be put right by hand.

On the way in: decorative emoji are removed from the text, and the four options are put
in a fixed order chosen from the question's id so the right answer is not always A or B
(the key and the per-option notes move with them). A question whose text or options refer
to an option by letter or position ("none of these", "both A and B") keeps its order.
"""
import collections
import glob
import hashlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)
import bank  # noqa: E402

IMPORT = os.path.join(bank.ROOT, "data", "bank-import")
EMOJI = re.compile(u"[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍]")
ORDER_SENSITIVE = re.compile(r"\b(none of|all of|both\b.*\band\b|either|neither|option\s*[A-D1-4]\b|\([A-Da-d]\)|above|below)\b", re.I)
LETTERS = ("A", "B", "C", "D")


def tidy(text):
    if not isinstance(text, str):
        return text
    out = EMOJI.sub("", text)
    out = re.sub(r"[ \t]{2,}", " ", out)
    out = re.sub(r"\s+([.,?!;])", r"\1", out)
    return out.strip()


def numbers_in(text):
    return tuple(sorted(re.findall(r"\d+(?:\.\d+)?", (text or "").replace(",", ""))))


def norm(text):
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())


def refers_to_letters(q):
    parts = [q.get("questionText") or ""] + [str(o.get("text")) for o in q["options"]]
    parts += [str(h) for h in (q.get("hints") or [])]
    for step in q.get("stepByStep") or []:
        parts.append(json.dumps(step, ensure_ascii=False))
    parts += [str(v) for v in (q.get("misconceptions") or {}).values()]
    return any(ORDER_SENSITIVE.search(p) for p in parts)


def reorder(q):
    """Options in an order fixed by the question id; key and per-option notes follow."""
    if refers_to_letters(q):
        return q, False
    digest = hashlib.sha256(q["id"].encode("utf-8")).digest()
    order = list(range(4))
    # Fisher-Yates driven by the digest: the same id always gives the same order.
    for i in range(3, 0, -1):
        j = digest[i] % (i + 1)
        order[i], order[j] = order[j], order[i]
    old = q["options"]
    old_key = q["correctAnswer"]
    old_mis = q.get("misconceptions") or {}
    new_opts, new_mis, new_key = [], {}, None
    for pos, src in enumerate(order):
        letter = LETTERS[pos]
        new_opts.append({"id": letter, "text": old[src]["text"]})
        src_letter = old[src]["id"]
        if src_letter in old_mis:
            new_mis[letter] = old_mis[src_letter]
        if src_letter == old_key:
            new_key = letter
    out = dict(q)
    out["options"] = new_opts
    out["correctAnswer"] = new_key
    if isinstance(q.get("misconceptions"), dict):
        out["misconceptions"] = {k: new_mis[k] for k in LETTERS if k in new_mis}
    return out, True


def clean(q):
    out = dict(q)
    out["questionText"] = tidy(q.get("questionText"))
    out["hints"] = [tidy(h) for h in (q.get("hints") or [])]
    steps = []
    for step in q.get("stepByStep") or []:
        if isinstance(step, dict):
            steps.append({k: tidy(v) for k, v in step.items()})
        else:
            steps.append(tidy(step))
    out["stepByStep"] = steps
    if isinstance(q.get("misconceptions"), dict):
        out["misconceptions"] = {k: tidy(v) for k, v in q["misconceptions"].items()}
    out["options"] = [{"id": o["id"], "text": tidy(o["text"])} for o in q["options"]]
    return out


def main():
    with io.open(os.path.join(IMPORT, "candidates.json"), encoding="utf-8") as f:
        candidates = json.load(f)
    with io.open(os.path.join(IMPORT, "keys.json"), encoding="utf-8") as f:
        keys = json.load(f)
    worked = {}
    for path in sorted(glob.glob(os.path.join(IMPORT, "answers", "part-*.json"))):
        with io.open(path, encoding="utf-8") as f:
            for row in json.load(f):
                worked[row.get("id")] = row
    print("%d candidates, %d worked by a checker" % (len(candidates), len(worked)))

    nodes = bank.tree_nodes()
    names = {n["id"]: n["name"] for n in nodes}
    in_bank = bank.load_bank()
    have = collections.Counter(q.get("node") for q in in_bank)
    kept_signatures = set()
    for q in in_bank:
        if q.get("topicId") == "grade5":
            right = [o["text"] for o in q["options"] if o["id"] == q["correctAnswer"]]
            kept_signatures.add((q.get("node"), numbers_in(q.get("questionText")), norm(right[0] if right else "")))

    verdicts = collections.defaultdict(collections.Counter)
    by_node = collections.defaultdict(collections.Counter)
    passing, left_out = [], []
    for q in sorted(candidates, key=lambda r: r["id"]):
        node = bank.assign_node(q, nodes)
        w = worked.get(q["id"])
        if w is None:
            why = "not worked"
        elif w.get("answer") not in LETTERS:
            why = "checker found no single answer"
        elif w.get("issue"):
            why = "checker raised an issue"
        elif not w.get("sure"):
            why = "checker was not sure"
        elif w["answer"] != keys.get(q["id"]):
            why = "checker's answer differs from the key"
        elif node is None:
            why = "no topic"
        else:
            right = [o["text"] for o in q["options"] if o["id"] == q["correctAnswer"]]
            sig = (node, numbers_in(q.get("questionText")), norm(right[0] if right else ""))
            if sig in kept_signatures and len(sig[1]) >= 2:
                why = "near-copy of a question already kept"
            else:
                kept_signatures.add(sig)
                why = None
        verdicts[why or "PASS"][q.get("source")] += 1
        by_node[node]["pass" if why is None else "out"] += 1
        if why is None:
            passing.append((q, node))
        else:
            left_out.append({"id": q["id"], "node": node, "source": q.get("source"), "why": why,
                             "checker": (w or {}).get("answer"), "key": keys.get(q["id"]),
                             "issue": (w or {}).get("issue"), "working": (w or {}).get("working"),
                             "question": q.get("questionText")})

    print("\nVERDICTS")
    for why, by in sorted(verdicts.items(), key=lambda kv: -sum(kv[1].values())):
        print("   %4d  %-40s %s" % (sum(by.values()), why, ", ".join("%s=%d" % kv for kv in by.most_common())))

    print("\nBY TOPIC: passing / left out, and what the bank holds now")
    for node, c in sorted(by_node.items(), key=lambda kv: -kv[1]["pass"]):
        print("   %-34s %4d pass  %3d out   bank now %4d -> %4d" % (
            (names.get(node) or "NO TOPIC")[:34], c["pass"], c["out"], have.get(node, 0), have.get(node, 0) + c["pass"]))

    disagreements = [r for r in left_out if r["why"] == "checker's answer differs from the key"]
    print("\nKEY DISAGREEMENTS: %d (the checker's working says the stored answer is not right)" % len(disagreements))
    for r in disagreements[:12]:
        print("   %s key=%s checker=%s  %s  | %s" % (r["id"][-28:], r["key"], r["checker"], (r["working"] or "")[:90], (r["question"] or "")[:70]))

    only_source = [r for r in left_out if have.get(r["node"], 0) == 0 and r["node"]]
    out_rows = []
    moved = 0
    for q, node in passing:
        row, changed = reorder(clean(q))
        moved += 1 if changed else 0
        row["node"] = node
        out_rows.append(row)
    spread = collections.Counter(r["correctAnswer"] for r in out_rows)
    before = collections.Counter(q["correctAnswer"] for q, _ in passing)
    print("\nRIGHT ANSWER POSITION among the passing questions: before %s; after reordering %d of them: %s" % (
        dict(sorted(before.items())), moved, dict(sorted(spread.items()))))
    print("left out but the only questions their topic has (repair list): %d" % len(only_source))

    if "--write" not in sys.argv:
        print("\nnothing written (use --write)")
        return
    with io.open(os.path.join(IMPORT, "repair.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(only_source, f, ensure_ascii=False, indent=1)
        f.write("\n")
    with io.open(os.path.join(IMPORT, "left-out.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(left_out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    ids = set(q["id"] for q in in_bank)
    added = [r for r in out_rows if r["id"] not in ids]
    bank.save_bank(in_bank + added)
    print("\nadded %d questions to the bank; wrote repair.json (%d) and left-out.json (%d)" % (len(added), len(only_source), len(left_out)))


if __name__ == "__main__":
    main()
