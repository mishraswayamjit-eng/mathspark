"""Mechanical clean-up of the Grade 4 bank, and the inputs for the work that needs a reviewer.

    python -X utf8 scripts/fixes/g4_cleanup.py            # report only
    python -X utf8 scripts/fixes/g4_cleanup.py --write

  repeats   where two Grade 4 questions have the same wording and the same right answer, the
            generated or worksheet copy is removed (a real past-paper question is never removed);
  key order worksheet and hand-written questions had the right answer mostly in one position
            (A in 69% of the worksheet set). Their options are put in a fixed pseudo-random
            order, key and per-option notes moving with them. A question is left alone when
            its hints or steps name an option by letter, or an option reads "None of these",
            "All of the above" and the like, and real past-paper questions keep the printed order.
Inputs written to data/bank-import/g4/ (not part of the bank):
  dupopts-in.json   questions where two options are the same value: one needs replacing
  teach-in-NN.json  questions whose hints are filler or that have no real worked steps
"""
import collections
import hashlib
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402
import g4_classify_inputs as g4  # noqa: E402

LETTER = re.compile(r"\b[Oo]ption\s+\(?[A-D]\)?(?![A-Za-z])|\([A-D]\)|\b(?:[Aa]nswer|[Cc]hoice)(?:\s+is|\s*:)?\s+\(?[A-D]\)?(?![A-Za-z])|\b[A-D]\)\s")
FIXED_OPTION = re.compile(r"\b(none|all|both|neither|either)\b.*\b(these|above|them|of)\b|cannot be|can't be", re.I)
FILLER_HINTS = {"read the question carefully.", "think step by step.", "check your answer!"}
FILLER_STEP = re.compile(r"^\s*(the\s+)?answer\s*(is|:)?\s*\(?[A-D]\)?\.?\s*$", re.I)
REAL = ("g4_mse_final", "previous_year")
RANK = {"real": 0, "hand_crafted": 1, "g4_ipm_worksheets_2": 2}


def norm(text):
    return re.sub(r"[^a-z0-9.]+", " ", (text or "").lower()).strip()


def value(text):
    """A comparable value for an option: number if it is one (1.0 == 1.00, 8/8 == 1)."""
    t = (text or "").replace(",", "").replace("₹", "").replace("Rs.", "").strip().lower()
    m = re.match(r"^(-?\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)$", t)
    try:
        if m and float(m.group(2)) != 0:
            return round(float(m.group(1)) / float(m.group(2)), 9)
        return round(float(t), 9)
    except ValueError:
        # Not a number: compare the text itself, keeping signs and symbols (5x-10 is not 5x+10).
        return re.sub(r"\s+", "", (text or "").lower())


def is_real(q):
    return (q.get("source") or "").startswith(REAL)


def texts(q):
    out = [str(h) for h in (q.get("hints") or [])]
    out += [(s.get("text") or "") if isinstance(s, dict) else str(s) for s in (q.get("stepByStep") or [])]
    out += [str(v) for v in (q.get("misconceptions") or {}).values()]
    return out


def needs_teaching(q):
    hints = [h for h in (q.get("hints") or []) if h]
    steps = [(s.get("text") or "") if isinstance(s, dict) else str(s) for s in (q.get("stepByStep") or [])]
    filler = len(hints) < 3 or all(h.strip().lower() in FILLER_HINTS for h in hints)
    no_steps = not steps or all(FILLER_STEP.match(s) for s in steps)
    return filler or no_steps


def main():
    write = "--write" in sys.argv
    questions = bank.load_bank()
    ids4 = {q["id"] for q in bank.load_bank(4)}
    names = {n["id"]: n["name"] for n in bank.tree_nodes(4)}

    # 1. repeats
    groups = collections.defaultdict(list)
    for q in questions:
        if q["id"] in ids4:
            groups[norm(q.get("questionText"))].append(q)
    drop = set()
    kept_conflicts = 0
    for qs in groups.values():
        if len(qs) < 2:
            continue
        answers = {value(next((o["text"] for o in q["options"] if o["id"] == q["correctAnswer"]), "")) for q in qs}
        if len(answers) > 1:
            kept_conflicts += 1
            continue
        qs.sort(key=lambda q: (RANK["real"] if is_real(q) else RANK.get(q.get("source"), 3), q["id"]))
        for q in qs[1:]:
            if not is_real(q):
                drop.add(q["id"])
    questions = [q for q in questions if q["id"] not in drop]

    # 2. key order
    before = collections.Counter()
    after = collections.Counter()
    moved = 0
    for q in questions:
        if q["id"] not in ids4 or q.get("source") not in ("hand_crafted", "g4_ipm_worksheets_2"):
            continue
        before[q["correctAnswer"]] += 1
        if any(LETTER.search(t) for t in texts(q)) or any(FIXED_OPTION.search(o["text"] or "") for o in q["options"]):
            after[q["correctAnswer"]] += 1
            continue
        order = sorted(range(4), key=lambda i: hashlib.md5(("%s|%d" % (q["id"], i)).encode("utf-8")).hexdigest())
        old = q["options"]
        letters = ["A", "B", "C", "D"]
        remap = {old[src]["id"]: letters[dst] for dst, src in enumerate(order)}
        new_opts = [{"id": letters[dst], "text": old[src]["text"]} for dst, src in enumerate(order)]
        if [o["text"] for o in new_opts] != [o["text"] for o in old]:
            moved += 1
        q["options"] = new_opts
        q["correctAnswer"] = remap[q["correctAnswer"]]
        if isinstance(q.get("misconceptions"), dict) and q["misconceptions"]:
            q["misconceptions"] = {remap[k]: v for k, v in sorted(q["misconceptions"].items(), key=lambda kv: remap.get(kv[0], kv[0])) if k in remap}
        after[q["correctAnswer"]] += 1

    g4q = [q for q in questions if q["id"] in ids4]
    dup = [q for q in g4q if len({value(o["text"]) for o in q["options"]}) < 4]
    teach = [q for q in g4q if needs_teaching(q)]
    print("repeats: %d questions removed (%d groups left alone because the copies give different answers)" % (len(drop), kept_conflicts))
    print("key order: %d hand-written and worksheet questions reordered; right answer by position %s -> %s" % (
        moved, dict(sorted(before.items())), dict(sorted(after.items()))))
    print("two options the same value: %d questions (%s)" % (len(dup), dict(collections.Counter(q.get("source") for q in dup))))
    print("no real hints or steps: %d questions (%s)" % (len(teach), dict(collections.Counter("real paper" if is_real(q) else q.get("source") for q in teach))))
    if not write:
        print("nothing written (use --write)")
        return
    bank.save_bank(questions)

    def brief(q):
        return {"id": q["id"], "topic": names.get(q.get("node")), "difficulty": q.get("difficulty"), "source": q.get("source"),
                "question": q.get("questionText"), "options": {o["id"]: o["text"] for o in q["options"]},
                "answer": q.get("correctAnswer")}

    g4.dump("dupopts-in.json", [brief(q) for q in dup])
    teach.sort(key=lambda q: (q.get("node") or "", q["id"]))
    parts = 6
    size = (len(teach) + parts - 1) // parts
    for i in range(parts):
        chunk = teach[i * size:(i + 1) * size]
        g4.dump("teach-in-%02d.json" % (i + 1), [dict(brief(q), hints=q.get("hints") or [],
                steps=[(s.get("text") or "") if isinstance(s, dict) else str(s) for s in (q.get("stepByStep") or [])]) for q in chunk])
        print("teach-in-%02d.json  %d questions" % (i + 1, len(chunk)))
    print("bank written")


if __name__ == "__main__":
    main()
