#!/usr/bin/env python3
"""
Generate the Percent-Sense Concept Trainer.

Transforms the self-contained reference trainer data
(`scripts/sources/percent-sense-source.json`) into the app's `ConceptTrainer`
schema (see `src/types/conceptTrainer.ts`) and writes
`data/concept-trainers/percent.json`.

Design notes
------------
* Every numeric answer in the source was authored/computed offline; we only
  reshape and format it here — no math is invented, so the no-hallucinated-math
  rule holds (same guarantee as the concept-lessons generator).
* Each option's `feedback` names the misconception; we copy it verbatim.
* `validate()` self-checks structural invariants before writing.

Run:  python scripts/generate_percent_trainer.py
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "sources", "percent-sense-source.json")
OUT = os.path.join(ROOT, "data", "concept-trainers", "percent.json")

LETTERS = ["A", "B", "C", "D", "E", "F"]

# Trainer-level catalog metadata (grade span mirrors the source's Core→Stretch arc).
SLUG = "percent"
TITLE = "Percent Sense"
CONCEPT = "Percentages"
GRADE_RANGE = [5, 9]


def fmt_answer(value) -> str:
    """Format a numeric answer as a short canonical string (strip trailing .0)."""
    if isinstance(value, bool):  # guard: bool is a subclass of int
        return str(value)
    if isinstance(value, (int, float)):
        # `g` drops trailing zeros: 10.0 -> '10', 2.5 -> '2.5'
        return f"{value:g}"
    return str(value).strip()


def map_step(stage: dict) -> dict:
    """One source `stage` -> one `ConceptStep` (letters assigned by position)."""
    choices = []
    for i, opt in enumerate(stage["options"]):
        choices.append(
            {
                "letter": LETTERS[i],
                "text": str(opt["text"]).strip(),
                "isCorrect": bool(opt.get("correct", False)),
                "feedback": str(opt.get("feedback", "")).strip(),
            }
        )
    step = {
        "prompt": str(stage["prompt"]).strip(),
        "choices": choices,
        "hint": str(stage.get("hint", "")).strip(),
    }
    key = stage.get("key")
    if key:
        step["key"] = str(key).strip()
    return step


def map_visual(model) -> dict | None:
    """One source `model` -> one `ConceptVisual`, or None if unusable."""
    if not isinstance(model, dict):
        return None
    t = model.get("type")
    if t == "bar":
        return {
            "type": "bar",
            "share": model["share"],
            "whole": str(model["whole"]).strip(),
            "left": str(model["left"]).strip(),
            "right": str(model["right"]).strip(),
        }
    if t == "mapping":
        rows = [[str(a).strip(), str(b).strip()] for a, b in model["rows"]]
        return {"type": "mapping", "rows": rows}
    if t == "groups":
        visual = {
            "type": "groups",
            "caps": list(model["caps"]),
            "labels": [str(x).strip() for x in model["labels"]],
            "target": str(model["target"]).strip(),
        }
        if model.get("capLabel"):
            visual["capLabel"] = str(model["capLabel"]).strip()
        return visual
    return None


def map_item(q: dict) -> dict:
    """One source question -> one `ConceptItem`."""
    item = {
        "code": str(q["id"]).strip(),
        "title": str(q["title"]).strip(),
        "story": str(q["story"]).strip(),
        "answer": fmt_answer(q["answer"]),
        "steps": [map_step(s) for s in q["stages"]],
        "solution": [{"text": str(line).strip()} for line in q.get("worked", [])],
    }
    unit = q.get("unit")
    if unit and str(unit).strip() and str(unit).strip() != "%":
        item["unit"] = str(unit).strip()
    check = q.get("check")
    if check and str(check).strip():
        item["check"] = str(check).strip()
    explain = q.get("explain")
    if explain and str(explain).strip():
        item["explain"] = str(explain).strip()
    visual = map_visual(q.get("model"))
    if visual:
        item["visual"] = visual
    return item


def build() -> dict:
    with open(SRC, encoding="utf-8") as f:
        src = json.load(f)

    # Group questions by their module number (preserving source order).
    by_module: dict[int, list] = {}
    for q in src["questions"]:
        by_module.setdefault(q["module"], []).append(q)

    modules = []
    for m in src["modules"]:
        num = m["id"]
        module = {
            "code": f"m{num}",
            "number": num,
            "title": str(m["title"]).strip(),
            "skill": str(m.get("desc", "")).strip(),
            "items": [map_item(q) for q in by_module.get(num, [])],
        }
        if m.get("level"):
            module["level"] = str(m["level"]).strip()
        if m.get("rule"):
            module["rule"] = str(m["rule"]).strip()
        if m.get("teach"):
            module["teach"] = [str(x).strip() for x in m["teach"]]
        if m.get("contrast"):
            module["contrast"] = [str(x).strip() for x in m["contrast"]]
        if m.get("transfer"):
            module["transfer"] = str(m["transfer"]).strip()
        modules.append(module)

    return {
        "slug": SLUG,
        "title": TITLE,
        "concept": CONCEPT,
        "gradeRange": GRADE_RANGE,
        "modules": modules,
    }


def validate(trainer: dict) -> None:
    """Structural self-check; raises AssertionError on any violation."""
    assert trainer["slug"] == SLUG
    assert isinstance(trainer["gradeRange"], list) and len(trainer["gradeRange"]) == 2
    mods = trainer["modules"]
    assert len(mods) == 10, f"expected 10 modules, got {len(mods)}"

    numbers = [m["number"] for m in mods]
    assert numbers == list(range(1, 11)), f"module numbers not 1..10: {numbers}"

    for m in mods:
        assert m["code"] == f"m{m['number']}"
        assert m["title"] and m["skill"], f"module {m['code']} missing title/skill"
        items = m["items"]
        assert len(items) == 8, f"module {m['code']} has {len(items)} items (want 8)"
        for it in items:
            assert it["code"] and it["title"] and it["story"], f"{it.get('code')} missing text"
            assert it["answer"], f"{it['code']} has empty answer"
            # No KaTeX-triggering chars in the canonical answer.
            assert "\\" not in it["answer"] and "{" not in it["answer"], (
                f"{it['code']} answer has latex chars: {it['answer']!r}"
            )
            steps = it["steps"]
            assert len(steps) == 3, f"{it['code']} has {len(steps)} steps (want 3)"
            for st in steps:
                assert st["prompt"] and st["hint"], f"{it['code']} step missing prompt/hint"
                choices = st["choices"]
                assert len(choices) == 3, f"{it['code']} step has {len(choices)} choices"
                correct = [c for c in choices if c["isCorrect"]]
                assert len(correct) == 1, (
                    f"{it['code']} step '{st['prompt'][:30]}' has {len(correct)} correct"
                )
                letters = [c["letter"] for c in choices]
                assert letters == LETTERS[: len(choices)], f"{it['code']} bad letters {letters}"
                for c in choices:
                    assert c["text"], f"{it['code']} choice {c['letter']} empty text"
                    assert c["feedback"], f"{it['code']} choice {c['letter']} empty feedback"
            assert len(it["solution"]) >= 1, f"{it['code']} has no solution lines"
            visual = it.get("visual")
            if visual:
                assert visual["type"] in ("bar", "mapping", "groups")


def main() -> None:
    trainer = build()
    validate(trainer)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(trainer, f, ensure_ascii=False, indent=2)
        f.write("\n")

    n_items = sum(len(m["items"]) for m in trainer["modules"])
    n_steps = sum(len(it["steps"]) for m in trainer["modules"] for it in m["items"])
    print(f"OK  wrote {OUT}")
    print(f"    {len(trainer['modules'])} modules, {n_items} items, {n_steps} steps")


if __name__ == "__main__":
    main()
