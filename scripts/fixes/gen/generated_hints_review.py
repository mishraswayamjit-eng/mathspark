"""Print a sample of the generated hints for reading, grouped by wording.

    python -X utf8 scripts/fixes/gen/generated_hints_review.py                 # every family, 5 per wording
    python -X utf8 scripts/fixes/gen/generated_hints_review.py angles          # one family
    python -X utf8 scripts/fixes/gen/generated_hints_review.py angles 8        # 8 per wording
    python -X utf8 scripts/fixes/gen/generated_hints_review.py tiers           # every example that shares a number
    python -X utf8 scripts/fixes/gen/generated_hints_review.py h2 bodmas       # hint 2 only, every question

The sample is spread evenly through each wording (first, last and in between), never random.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generated_hints import build  # noqa: E402  (this also puts scripts/fixes on the path)
from check import correct_text, option_texts  # noqa: E402


def spread(items, n):
    if len(items) <= n:
        return items
    return [items[round(i * (len(items) - 1) / (n - 1))] for i in range(n)]


def show(r):
    q = r["q"]
    print("  %s  [example tier %d]" % (q["id"], r["tier"]))
    print("    Q: %s   choices: %s   key: %s" % (q["questionText"], " | ".join(option_texts(q)), correct_text(q)))
    for i, h in enumerate(r["fix"]["hints"]):
        print("    %d (%3d): %s" % (i + 1, len(h), h))


def main():
    args = sys.argv[1:]
    rows = [r for r in build() if r["fix"]]
    if args and args[0] == "tiers":
        for r in rows:
            if r["tier"] != 1:
                show(r)
        return
    if args and args[0] == "h2":
        for r in rows:
            if len(args) < 2 or r["family"] == args[1]:
                print("%-34s %s" % (r["q"]["id"].replace("VAR_G5_vary_", ""), r["fix"]["hints"][1]))
        return
    family = args[0] if args and not args[0].isdigit() else None
    count = int(args[-1]) if args and args[-1].isdigit() else 5
    groups = collections.OrderedDict()
    for r in rows:
        if family is None or r["family"] == family:
            groups.setdefault((r["family"], r["rule"], r["variant"]), []).append(r)
    for (fam, rule, variant), items in groups.items():
        print("\n== %s / %s%s (%d questions)" % (fam, rule, " / " + variant if variant else "", len(items)))
        for r in spread(items, count):
            show(r)


if __name__ == "__main__":
    main()
