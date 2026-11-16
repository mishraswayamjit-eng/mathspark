"""How the real past papers are built, per grade. Reads data files only; changes nothing.

    python -X utf8 scripts/audit/past_papers.py
"""
import collections
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402  (scripts/bank/bank.py: the question bank, data/bank/)

PAST = re.compile(r"^(g\d_final_|g\d_mse_final_|g\d_mega_final_|mega_final_|previous_year_)(\d{4})$")


def norm(text):
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())[:80]


def main():
    seed = bank.load_bank()

    papers = collections.defaultdict(list)
    for q in seed:
        if PAST.match(str(q.get("source"))):
            papers[(q.get("topicId") if str(q.get("topicId")).startswith("grade") else "grade4(ch)", q["source"])].append(q)

    print("PAPERS PER GRADE (years held, questions per paper)")
    by_grade = collections.defaultdict(list)
    for (grade, src), rows in papers.items():
        by_grade[grade].append((src[-4:], src, len(rows)))
    for grade in sorted(by_grade):
        items = sorted(by_grade[grade])
        print("  %-11s %s" % (grade, "  ".join("%s:%d" % (y, n) for y, _, n in items)))

    print("\nGRADE 5: questions per chapter in each real paper (the paper has 40 questions)")
    chapters = collections.Counter()
    worst = 0
    for (grade, src), rows in sorted(papers.items()):
        if grade != "grade5":
            continue
        c = collections.Counter(r.get("subTopic", "").replace("Grade 5 — ", "") for r in rows)
        worst = max(worst, max(c.values()))
        chapters.update(c)
    for name, n in chapters.most_common():
        print("  %-48s %3d over 10 papers (%.1f a paper)" % (name, n, n / 10.0))
    print("  most questions any one chapter has in any one paper: %d" % worst)

    print("\nGRADE 4: are previous_year_YYYY (chapter pool) and g4_mse_final_YYYY (grade4 pool) the same papers?")
    for year in ("2016", "2017", "2018", "2019"):
        a = set(norm(q["questionText"]) for q in papers.get(("grade4(ch)", "previous_year_" + year), []))
        b = set(norm(q["questionText"]) for q in papers.get(("grade4", "g4_mse_final_" + year), []))
        print("  %s: %d and %d questions, %d share the same opening text" % (year, len(a), len(b), len(a & b)))

    print("\nID AND FIELD SHAPE PER SOURCE FAMILY (first row)")
    seen = set()
    for (grade, src), rows in sorted(papers.items()):
        fam = (grade, re.sub(r"\d{4}$", "", src))
        if fam in seen:
            continue
        seen.add(fam)
        r = sorted(rows, key=lambda q: q["id"])[0]
        print("  %-11s %-18s id=%s  questionNumber=%s year=%s hints=%d steps=%d" % (
            grade, fam[1], r["id"], r.get("questionNumber"), r.get("year"), len(r.get("hints") or []), len(r.get("stepByStep") or [])))


if __name__ == "__main__":
    main()
