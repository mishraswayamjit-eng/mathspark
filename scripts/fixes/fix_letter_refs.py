"""Make the worked steps of imported questions name the right option letter.

    python -X utf8 scripts/fixes/fix_letter_refs.py            # report only
    python -X utf8 scripts/fixes/fix_letter_refs.py --write

When the imported questions came into the bank their options were put in a new order so
the right answer is not always A or B. A question whose hints or steps name an option by
letter ("The answer is B", "option C forgets...") must not be reordered, or the letter in
the working no longer points at the same option. This:
  1. finds imported questions whose hints, steps or per-option notes name an option letter;
  2. puts those questions' options back in their original order (from
     data/bank-import/candidates.json), key and notes with them;
  3. where the working names the ANSWER by a letter that is not the key (a slip that was
     already in the question), corrects that letter.
Only options, correctAnswer, misconceptions and those letters change.
"""
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402
import import_reviewed  # noqa: E402

ANY_REF = re.compile(r"\b[Oo]ption\s+\(?[A-D]\)?(?![A-Za-z])|\([A-D]\)|\b(?:[Aa]nswer|[Cc]hoice)(?:\s+is|\s*:)?\s+\(?[A-D]\)?(?![A-Za-z])")
ANSWER_REF = re.compile(r"(\b(?:[Tt]he\s+)?(?:[Cc]orrect\s+)?(?:[Aa]nswer|[Oo]ption|[Cc]hoice)(?:\s+is|\s*:)\s+\(?)([A-D])(\)?(?![A-Za-z]))")


def texts_of(q):
    out = [str(h) for h in (q.get("hints") or [])]
    for step in q.get("stepByStep") or []:
        out.append(json.dumps(step, ensure_ascii=False) if not isinstance(step, str) else step)
    out += [str(v) for v in (q.get("misconceptions") or {}).values()]
    return out


def fix_answer_letter(value, key, counter):
    if not isinstance(value, str):
        return value

    def swap(m):
        if m.group(2) != key:
            counter[0] += 1
        return m.group(1) + key + m.group(3)

    return ANSWER_REF.sub(swap, value)


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "candidates.json"), encoding="utf-8") as f:
        original = {q["id"]: q for q in json.load(f)}
    questions = bank.load_bank()
    restored = 0
    letters_fixed = [0]
    touched = 0
    samples = []
    for q in questions:
        orig = original.get(q["id"])
        if orig is None or not any(ANY_REF.search(t) for t in texts_of(q)):
            continue
        touched += 1
        cleaned = import_reviewed.clean(orig)
        if [o["text"] for o in q["options"]] != [o["text"] for o in cleaned["options"]]:
            restored += 1
        q["options"] = cleaned["options"]
        q["correctAnswer"] = cleaned["correctAnswer"]
        if isinstance(cleaned.get("misconceptions"), dict):
            q["misconceptions"] = cleaned["misconceptions"]
        key = q["correctAnswer"]
        before = letters_fixed[0]
        q["hints"] = [fix_answer_letter(h, key, letters_fixed) for h in (q.get("hints") or [])]
        steps = []
        for step in q.get("stepByStep") or []:
            if isinstance(step, dict):
                steps.append({k: fix_answer_letter(v, key, letters_fixed) for k, v in step.items()})
            else:
                steps.append(fix_answer_letter(step, key, letters_fixed))
        q["stepByStep"] = steps
        if letters_fixed[0] > before and len(samples) < 6:
            samples.append("%s key=%s  %s" % (q["id"][-30:], key, json.dumps(steps[-1], ensure_ascii=False)[:150]))

    print("%d imported questions name an option letter in their working" % touched)
    print("  %d had been reordered and are back in their original order" % restored)
    print("  %d answer letters in the working did not match the key and were corrected" % letters_fixed[0])
    for s in samples:
        print("     " + s)
    if "--write" not in sys.argv:
        print("nothing written (use --write)")
        return
    bank.save_bank(questions)
    print("bank written")


if __name__ == "__main__":
    main()
