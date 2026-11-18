"""Group the Grade 4 variants by the FORM of their question, for classifying by form.

    python -X utf8 scripts/fixes/g4_variant_forms.py

The variants filed under a parent exam question mostly do not test that parent's skill:
they come from a few dozen generator forms. A form is the wording with every number, and
every word that is not in the common vocabulary of the set (names, items), blanked out.
Writes data/bank-import/g4/forms-in.json: one entry per form with its count and examples.
Reads the bank; changes nothing.
"""
import collections
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402
import g4_classify_inputs as g4  # noqa: E402


def words(text):
    return re.findall(r"[A-Za-z]+", text or "")


def form_of(text, common):
    text = re.sub(r"\d+(?:[.,]\d+)*", "N", text or "")
    return re.sub(r"[A-Za-z]+", lambda m: m.group(0).lower() if m.group(0).lower() in common else "_", text).strip()


def main():
    rows = [q for q in bank.load_bank(4) if g4.family(q)[0] == "variant"]
    freq = collections.Counter(w.lower() for q in rows for w in set(words(q.get("questionText"))))
    common = {w for w, n in freq.items() if n >= 25}
    forms = collections.defaultdict(list)
    for q in rows:
        forms[form_of(q.get("questionText"), common)].append(q)
    out = []
    for form, qs in sorted(forms.items(), key=lambda kv: -len(kv[1])):
        out.append({
            "form": form, "count": len(qs),
            "difficulties": dict(collections.Counter(q.get("difficulty") for q in qs)),
            "examples": [{
                "id": q["id"], "question": q.get("questionText"),
                "options": {o["id"]: o["text"] for o in q["options"]}, "answer": q.get("correctAnswer"),
            } for q in qs[:3]],
        })
    g4.dump("forms-in.json", out)
    sizes = [f["count"] for f in out]
    print("%d variants in %d forms; %d forms have 10 or more and cover %d; %d forms have one question" % (
        len(rows), len(out), sum(1 for s in sizes if s >= 10), sum(s for s in sizes if s >= 10), sum(1 for s in sizes if s == 1)))
    for f in out[:12]:
        print("  %4d  %s" % (f["count"], f["form"][:110]))


if __name__ == "__main__":
    main()
