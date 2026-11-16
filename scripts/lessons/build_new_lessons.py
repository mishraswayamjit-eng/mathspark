# -*- coding: utf-8 -*-
"""
Build the four Grade-5 concept lessons that were missing from the Learn section:

    addition-subtraction, multiplication-division,
    algebraic-expressions, speed-distance-time

The lesson text lives in the content_*.py files beside this script (one per
topic). This script only turns that text into data/lessons/<slug>.json in the
exact shape of src/types/lesson.ts (5 levels, each 5 lessons + 8 quiz items).

It does NOT decide whether the maths is right. That is the job of
check_new_lessons.py, which recomputes every answer on its own. Always run the
checker after building:

    python -X utf8 scripts/lessons/build_new_lessons.py [slug ...]
    python -X utf8 scripts/lessons/check_new_lessons.py

Edit the content_*.py files, never the generated JSON.
"""
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "data", "lessons"))
sys.path.insert(0, HERE)

MODULES = {
    "addition-subtraction": "content_addition_subtraction",
    "multiplication-division": "content_multiplication_division",
    "algebraic-expressions": "content_algebraic_expressions",
    "speed-distance-time": "content_speed_distance_time",
}

# Same five level styles as every existing lesson file.
LEVEL_STYLE = [
    ("\U0001F7E2", "#58CC02", "from-green-400 to-green-600"),
    ("\U0001F535", "#1CB0F6", "from-blue-400 to-blue-600"),
    ("\U0001F7E1", "#FFC800", "from-yellow-400 to-yellow-600"),
    ("\U0001F7E0", "#FF9600", "from-orange-400 to-orange-600"),
    ("\U0001F534", "#FF4B4B", "from-red-400 to-red-600"),
]

DIFFICULTY = ["direct", "direct", "near_transfer", "near_transfer",
              "stretch", "stretch", "challenge", "challenge"]


def build_lesson(lid, spec):
    title, intro, explanation, rule, tip = spec[0], spec[1], spec[2], spec[3], spec[4]
    out = {
        "id": lid,
        "title": title,
        "intro": intro,
        "visual": "",
        "explanation": list(explanation),
        "rule": rule,
        "tip": tip,
    }
    steps = spec[5] if len(spec) > 5 else None
    if steps:
        built = []
        for st in steps:
            d = {"text": st[0], "notation": st[1]}
            if len(st) > 2 and st[2]:
                d["tip"] = st[2]
            built.append(d)
        out["steps"] = built
    return out


def build_quiz(qid, index, spec):
    question, answer, hint = spec[0], spec[1], spec[2]
    story = spec[3] if len(spec) > 3 else None
    d = {
        "id": qid,
        "question": question,
        "answer": str(answer),
        "hint": hint,
        "difficulty": DIFFICULTY[index],
    }
    if story:
        d["story"] = story
        d["isWord"] = True
    return d


def build_topic(slug):
    mod = importlib.import_module(MODULES[slug])
    meta = mod.META
    prefix = mod.PREFIX
    if len(mod.LEVELS) != 5:
        raise SystemExit("%s: need exactly 5 levels" % slug)
    levels = []
    for n, (label, subtitle, lessons, quiz) in enumerate(mod.LEVELS, start=1):
        if len(lessons) != 5 or len(quiz) != 8:
            raise SystemExit("%s level %d: need 5 lessons and 8 quiz items" % (slug, n))
        emoji, color, grad = LEVEL_STYLE[n - 1]
        levels.append({
            "id": n,
            "label": label,
            "emoji": emoji,
            "color": color,
            "bgGradient": grad,
            "subtitle": subtitle,
            "lessons": [build_lesson("%s-l%d-les%d" % (prefix, n, i), s)
                        for i, s in enumerate(lessons, start=1)],
            "quiz": [build_quiz("%s-l%d-q%d" % (prefix, n, i + 1), i, s)
                     for i, s in enumerate(quiz)],
        })
    return {
        "id": slug,
        "topic": meta["topic"],
        "emoji": meta["emoji"],
        "color": meta["color"],
        "gradeRange": meta["gradeRange"],
        "description": meta["description"],
        "levels": levels,
    }


def main():
    slugs = sys.argv[1:] or list(MODULES.keys())
    for slug in slugs:
        if slug not in MODULES:
            raise SystemExit("unknown slug: " + slug)
        data = build_topic(slug)
        path = os.path.join(OUT_DIR, slug + ".json")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("wrote", os.path.relpath(path, os.path.join(HERE, "..", "..")))


main()
