"""Where the right answer sits (A-D), by grade and source. Reads the bank; changes nothing.

    python -X utf8 scripts/bank/key_spread.py
"""
import collections
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402


def main():
    by_grade = collections.defaultdict(collections.Counter)
    by_source = collections.defaultdict(collections.Counter)
    for q in bank.load_bank():
        g = bank.grade_of(q.get("topicId"))
        by_grade[g][q.get("correctAnswer")] += 1
        by_source[q.get("source")][q.get("correctAnswer")] += 1
    print("BY GRADE (share of questions whose right answer is A / B / C / D)")
    for g in sorted(by_grade):
        c = by_grade[g]
        n = float(sum(c.values()))
        print("   grade %s  %5d   A %2.0f%%  B %2.0f%%  C %2.0f%%  D %2.0f%%" % (g, n, 100 * c["A"] / n, 100 * c["B"] / n, 100 * c["C"] / n, 100 * c["D"] / n))
    print("\nSOURCES WHERE ONE LETTER HOLDS OVER 40% (200+ questions)")
    for s, c in sorted(by_source.items(), key=lambda kv: -sum(kv[1].values())):
        n = float(sum(c.values()))
        top = max(c.values()) / n
        if n >= 200 and top > 0.40:
            print("   %-28s %5d   A %2.0f%%  B %2.0f%%  C %2.0f%%  D %2.0f%%" % (s, n, 100 * c["A"] / n, 100 * c["B"] / n, 100 * c["C"] / n, 100 * c["D"] / n))


if __name__ == "__main__":
    main()
