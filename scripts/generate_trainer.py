#!/usr/bin/env python3
"""
Parametric Concept-Trainer generator.

Reshapes a self-contained trainer *source* JSON into the app's `ConceptTrainer`
schema (`src/types/conceptTrainer.ts`) and writes
`data/concept-trainers/<slug>.json`.

Unlike the bespoke `generate_percent_trainer.py`, this script is topic-agnostic:
the trainer-level metadata (`slug`, `title`, `concept`, `gradeRange`) is read
FROM the source's top level, so one generator serves every trainer.

Math-correctness gate
---------------------
Structure is always validated. In addition, any item that carries a `verify`
spec `{op, args, expect?}` is MATH-checked: the op is recomputed with
`fractions.Fraction` and the result must equal the item's authored `answer`
(and `expect`, if given). This upholds the no-hallucinated-math rule — authored
arithmetic is never trusted, it is recomputed. Items without a `verify` spec
(e.g. purely conceptual "name the whole" items) pass structure-only.

Usage:
    python scripts/generate_trainer.py scripts/sources/fractions-g5-source.json
"""

import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

LETTERS = ["A", "B", "C", "D", "E", "F"]
VISUAL_TYPES = ("bar", "mapping", "groups", "parts")


# ── fraction helpers (the math gate) ─────────────────────────────────────────

def parse_frac(s) -> Fraction:
    """Parse '3/8', '21/5', '4 1/5' (mixed), or '7' into a Fraction."""
    if isinstance(s, (int,)):
        return Fraction(s)
    if isinstance(s, float):
        return Fraction(s).limit_denominator(10**6)
    text = str(s).strip()
    if " " in text:  # mixed number: "4 1/5"
        whole, frac = text.split(None, 1)
        f = Fraction(frac)
        sign = -1 if whole.strip().startswith("-") else 1
        return Fraction(int(whole)) + sign * f
    return Fraction(text)


def fmt_frac(f: Fraction) -> str:
    """Canonical short string: integers as 'n', else lowest-terms 'n/d'."""
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


def fmt_mixed(f: Fraction) -> str:
    """Format as a mixed number '4 1/5' (or 'n' / 'n/d' when not mixed)."""
    if f.denominator == 1:
        return str(f.numerator)
    if abs(f.numerator) < f.denominator:
        return fmt_frac(f)
    sign = "-" if f < 0 else ""
    a = abs(f)
    whole = a.numerator // a.denominator
    rem = a - whole
    return f"{sign}{whole} {rem.numerator}/{rem.denominator}"


def compute(op: str, args: list):
    """Recompute a fraction operation. Returns a formatted canonical string."""
    if op == "simplify":
        return fmt_frac(parse_frac(args[0]))
    if op == "add":
        return fmt_frac(sum((parse_frac(a) for a in args), Fraction(0)))
    if op == "sub":
        acc = parse_frac(args[0])
        for a in args[1:]:
            acc -= parse_frac(a)
        return fmt_frac(acc)
    if op == "mul":
        acc = Fraction(1)
        for a in args:
            acc *= parse_frac(a)
        return fmt_frac(acc)
    if op == "of":  # fraction OF a quantity: of(frac, qty)
        return fmt_frac(parse_frac(args[0]) * parse_frac(args[1]))
    if op == "larger":  # the greatest of the given fractions
        return fmt_frac(max(parse_frac(a) for a in args))
    if op == "smaller":
        return fmt_frac(min(parse_frac(a) for a in args))
    if op == "compare":  # symbol between two: '<' '>' '='
        a, b = parse_frac(args[0]), parse_frac(args[1])
        return "<" if a < b else (">" if a > b else "=")
    if op == "to_improper":
        return fmt_frac(parse_frac(args[0]))
    if op == "to_mixed":
        return fmt_mixed(parse_frac(args[0]))
    if op == "equiv":  # equivalent fraction: equiv('3/4', mult) -> unreduced 'n*k/d*k'
        f = parse_frac(args[0])
        k = int(args[1])
        return f"{f.numerator * k}/{f.denominator * k}"
    raise ValueError(f"unknown verify op: {op!r}")


# ── source -> schema reshaping ───────────────────────────────────────────────

def map_step(stage: dict) -> dict:
    choices = []
    for i, opt in enumerate(stage["options"]):
        choices.append({
            "letter": LETTERS[i],
            "text": str(opt["text"]).strip(),
            "isCorrect": bool(opt.get("correct", False)),
            "feedback": str(opt.get("feedback", "")).strip(),
        })
    step = {
        "prompt": str(stage["prompt"]).strip(),
        "choices": choices,
        "hint": str(stage.get("hint", "")).strip(),
    }
    if stage.get("key"):
        step["key"] = str(stage["key"]).strip()
    return step


def map_visual(model):
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
        return {"type": "mapping", "rows": [[str(a).strip(), str(b).strip()] for a, b in model["rows"]]}
    if t == "groups":
        v = {
            "type": "groups",
            "caps": list(model["caps"]),
            "labels": [str(x).strip() for x in model["labels"]],
            "target": str(model["target"]).strip(),
        }
        if model.get("capLabel"):
            v["capLabel"] = str(model["capLabel"]).strip()
        return v
    if t == "parts":
        v = {"type": "parts", "total": int(model["total"]), "shaded": int(model["shaded"])}
        if model.get("shape"):
            v["shape"] = str(model["shape"]).strip()
        if model.get("label"):
            v["label"] = str(model["label"]).strip()
        return v
    return None


def fmt_answer(value) -> str:
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, (int, float)):
        return f"{value:g}"
    return str(value).strip()


def map_item(q: dict) -> dict:
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
    if q.get("check") and str(q["check"]).strip():
        item["check"] = str(q["check"]).strip()
    if q.get("explain") and str(q["explain"]).strip():
        item["explain"] = str(q["explain"]).strip()
    visual = map_visual(q.get("model"))
    if visual:
        item["visual"] = visual
    return item


def build(src: dict) -> dict:
    by_module: dict = {}
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
        for opt in ("level", "rule", "transfer"):
            if m.get(opt):
                module[opt] = str(m[opt]).strip()
        for lst in ("teach", "contrast"):
            if m.get(lst):
                module[lst] = [str(x).strip() for x in m[lst]]
        modules.append(module)

    gr = src["gradeRange"]
    return {
        "slug": str(src["slug"]).strip(),
        "title": str(src["title"]).strip(),
        "concept": str(src["concept"]).strip(),
        "gradeRange": [int(gr[0]), int(gr[1])],
        "modules": modules,
    }


# ── verification ─────────────────────────────────────────────────────────────

def validate(trainer: dict) -> None:
    assert trainer["slug"], "missing slug"
    gr = trainer["gradeRange"]
    assert isinstance(gr, list) and len(gr) == 2 and gr[0] <= gr[1], f"bad gradeRange {gr}"
    mods = trainer["modules"]
    assert len(mods) >= 1, "no modules"
    nums = [m["number"] for m in mods]
    assert nums == list(range(1, len(mods) + 1)), f"module numbers not 1..N: {nums}"

    for m in mods:
        assert m["code"] == f"m{m['number']}"
        assert m["title"] and m["skill"], f"module {m['code']} missing title/skill"
        assert len(m["items"]) >= 1, f"module {m['code']} has no items"
        for it in m["items"]:
            assert it["code"] and it["title"] and it["story"], f"{it.get('code')} missing text"
            assert it["answer"], f"{it['code']} empty answer"
            assert "\\" not in it["answer"] and "{" not in it["answer"], (
                f"{it['code']} answer has latex chars: {it['answer']!r}"
            )
            steps = it["steps"]
            assert len(steps) == 3, f"{it['code']} has {len(steps)} steps (want 3)"
            for st in steps:
                assert st["prompt"] and st["hint"], f"{it['code']} step missing prompt/hint"
                ch = st["choices"]
                assert 2 <= len(ch) <= 4, f"{it['code']} step has {len(ch)} choices"
                assert sum(1 for c in ch if c["isCorrect"]) == 1, (
                    f"{it['code']} step '{st['prompt'][:30]}' must have exactly 1 correct"
                )
                assert [c["letter"] for c in ch] == LETTERS[: len(ch)], f"{it['code']} bad letters"
                for c in ch:
                    assert c["text"], f"{it['code']} choice {c['letter']} empty text"
                    assert c["feedback"], f"{it['code']} choice {c['letter']} empty feedback"
            assert len(it["solution"]) >= 1, f"{it['code']} has no solution lines"
            v = it.get("visual")
            if v:
                assert v["type"] in VISUAL_TYPES, f"{it['code']} bad visual {v['type']}"
                if v["type"] == "parts":
                    assert v["total"] >= 1 and 0 <= v["shaded"] <= v["total"], f"{it['code']} bad parts"


def math_gate(src: dict) -> tuple[int, int]:
    """Recompute every item's `verify` spec; returns (checked, total)."""
    checked = 0
    total = len(src["questions"])
    for q in src["questions"]:
        spec = q.get("verify")
        if not spec:
            continue
        got = compute(spec["op"], spec["args"])
        want = fmt_answer(q["answer"])
        assert got == want, (
            f"{q['id']}: verify {spec['op']}{spec['args']} = {got!r} but answer is {want!r}"
        )
        if "expect" in spec:
            assert got == str(spec["expect"]).strip(), (
                f"{q['id']}: verify result {got!r} != expect {spec['expect']!r}"
            )
        checked += 1
    return checked, total


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: python scripts/generate_trainer.py <source.json>", file=sys.stderr)
        sys.exit(2)
    src_path = sys.argv[1]
    with open(src_path, encoding="utf-8") as f:
        src = json.load(f)

    for key in ("slug", "title", "concept", "gradeRange", "modules", "questions"):
        if key not in src:
            print(f"ERROR: source missing top-level '{key}'", file=sys.stderr)
            sys.exit(1)

    checked, total = math_gate(src)
    trainer = build(src)
    validate(trainer)

    out = os.path.join(ROOT, "data", "concept-trainers", f"{trainer['slug']}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(trainer, f, ensure_ascii=False, indent=2)
        f.write("\n")

    n_items = sum(len(m["items"]) for m in trainer["modules"])
    n_steps = sum(len(it["steps"]) for m in trainer["modules"] for it in m["items"])
    print(f"OK  wrote {out}")
    print(f"    {len(trainer['modules'])} modules, {n_items} items, {n_steps} steps")
    print(f"    math-gate: {checked}/{total} items recomputed & verified")


if __name__ == "__main__":
    main()
