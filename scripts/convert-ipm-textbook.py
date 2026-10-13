#!/usr/bin/env python3
"""
Offline converter: IPM "Mathematics Scholarship Std. V" textbook YAML -> JSON.

Reads the digitized textbook YAML and emits data/ipm-textbook-grade5.json: an
array of normalized MCQ records the import-textbook admin route consumes. Run
locally once (Node is unavailable in this repo), commit the JSON output.

    python scripts/convert-ipm-textbook.py <path-to-yaml>

Each record:
    {
      "ref": "ch01_q033",
      "id": "IPMTB_grade5_ch01_q033",
      "chapter": 1,
      "chapterTitle": "Numbers",
      "subTopicKey": "place value",
      "storedSubTopic": "Grade 5 — Numbers & Place Value (place value)",
      "questionText": "...",
      "option1": "...", "option2": "...", "option3": "...", "option4": "...",
      "printedAnswer": "A"            # "A".."D" or null when answerless
    }

Truth is NOT decided here. Printed answers are copied verbatim (the YAML header
says they are not independently verified); the import route LLM-verifies every
answer before any row can reach a child.
"""

import json
import re
import sys
from pathlib import Path

import yaml

# Chapter -> (subTopicKey, storedSubTopic). Keys MUST match GRADE5_TOPICS in
# src/data/topicTree.ts; storedSubTopic MUST contain the key as a substring so
# Grade-5 practice (subTopic ILIKE %key%) can surface the imported row. Chapters
# 11-17 (and 10) have zero scanned questions, so they need no mapping.
CHAPTER_MAP = {
    1:  ("place value",     "Grade 5 — Numbers & Place Value (place value)"),
    2:  ("place value",     "Grade 5 — Numbers & Place Value (place value)"),
    3:  ("sequence",        "Grade 5 — Sequences & Series (sequence)"),
    4:  ("square",          "Grade 5 — Square Numbers & Roots (square)"),
    5:  ("addition",        "Grade 5 — Addition & Subtraction (addition)"),
    6:  ("multiplication",  "Grade 5 — Multiplication & Division (multiplication)"),
    7:  ("bodmas",          "Grade 5 — BODMAS & Order of Operations (bodmas)"),
    8:  ("equation",        "Grade 5 — Equations (equation)"),
    9:  ("algebra",         "Grade 5 — Algebraic Expressions (algebra)"),
    10: ("hcf",             "Grade 5 — HCF & LCM (hcf)"),
    18: ("angle",           "Grade 5 — Angles & Lines (angle)"),
    19: ("area",            "Grade 5 — Area & Perimeter (area)"),
    20: ("area",            "Grade 5 — Area & Perimeter (area)"),
}

OPTION_LETTERS = {"a": "A", "b": "B", "c": "C", "d": "D"}

# Stems that depend on a diagram/figure/layout which did NOT survive digitization
# (the YAML carries only the question text, not the printed figure). The import
# route's LLM verification cannot validate these from text alone — it just
# rubber-stamps the model's own INVENTED figure — so a wrong "verified" answer can
# reach a child. Drop them here at convert time. Markers chosen from the live
# cleanup: they catch every figure-dependent stem found while sparing self-contained
# look-alikes ("series given below" carries its series inline; conceptual
# "linear pair" word problems need no figure). "figure out" is explicitly excluded.
FIGURE_MARKERS = (
    re.compile(r"\bfigure\b(?! out)", re.I),  # "in the figure", "figure given below"
    re.compile(r"\bshaded\b", re.I),          # "area of the shaded region"
    re.compile(r"\bdiagram\b", re.I),
    re.compile(r"problem given below", re.I),  # cryptarithm layout (add/sub problem)
    re.compile(r"\bshown (?:below|above|alongside)\b", re.I),
    re.compile(r"\badjoining\b", re.I),
)


def is_figure_dependent(text):
    """True when the stem references a figure/layout that isn't embedded in text."""
    return any(p.search(text) for p in FIGURE_MARKERS)


def normalize_answer(raw):
    """Printed option label -> 'A'..'D'; anything ambiguous/missing -> None."""
    if raw is None:
        return None
    key = str(raw).strip().lower()
    return OPTION_LETTERS.get(key)


def main():
    if len(sys.argv) < 2:
        print("usage: python scripts/convert-ipm-textbook.py <path-to-yaml>", file=sys.stderr)
        sys.exit(1)

    yaml_path = Path(sys.argv[1])
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))

    out = []
    skipped_chapters = {}
    skipped_options = 0
    skipped_figure = 0
    with_answer = 0
    answerless = 0

    for ch in data.get("chapters", []):
        chapter = ch.get("chapter_number")
        title = ch.get("title", "")
        questions = (ch.get("practice") or {}).get("questions") or []
        if not questions:
            continue

        mapping = CHAPTER_MAP.get(chapter)
        if mapping is None:
            skipped_chapters[chapter] = len(questions)
            print(f"WARNING: chapter {chapter} ({title}) is unmapped - "
                  f"skipping {len(questions)} question(s)", file=sys.stderr)
            continue

        sub_topic_key, stored_sub_topic = mapping

        for q in questions:
            number = q.get("number")
            ref = f"ch{int(chapter):02d}_q{int(number):03d}"
            text = (q.get("question") or "").strip()
            opts = q.get("options") or {}
            o1 = (opts.get("a") or "").strip()
            o2 = (opts.get("b") or "").strip()
            o3 = (opts.get("c") or "").strip()
            o4 = (opts.get("d") or "").strip()

            if not text or not (o1 and o2 and o3 and o4):
                skipped_options += 1
                print(f"WARNING: {ref} missing text or an option - skipping",
                      file=sys.stderr)
                continue

            if is_figure_dependent(text):
                skipped_figure += 1
                print(f"WARNING: {ref} is figure/layout-dependent "
                      f"(figure not in text) - skipping", file=sys.stderr)
                continue

            printed = normalize_answer(q.get("printed_answer_option"))
            if printed:
                with_answer += 1
            else:
                answerless += 1

            out.append({
                "ref": ref,
                "id": f"IPMTB_grade5_{ref}",
                "chapter": int(chapter),
                "chapterTitle": title,
                "subTopicKey": sub_topic_key,
                "storedSubTopic": stored_sub_topic,
                "questionText": text,
                "option1": o1,
                "option2": o2,
                "option3": o3,
                "option4": o4,
                "printedAnswer": printed,
            })

    out_path = Path(__file__).resolve().parent.parent / "data" / "ipm-textbook-grade5.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote {len(out)} records -> {out_path}")
    print(f"  with printed answer: {with_answer}")
    print(f"  answerless (-> fresh-solve on import): {answerless}")
    if skipped_options:
        print(f"  skipped (bad text/options): {skipped_options}")
    if skipped_figure:
        print(f"  skipped (figure/layout-dependent): {skipped_figure}")
    if skipped_chapters:
        print(f"  skipped unmapped chapters: {skipped_chapters}")


if __name__ == "__main__":
    main()
