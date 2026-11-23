"""Build data/teach/parts/g4-gr4_operations.json from the rule lessons and the hand-written ones.

    python -X utf8 scripts/teach/gen/g4_gr4_operations_build.py

Rules live in g4_gr4_operations_rules_*.py; individually written lessons in
g4_gr4_operations_auth_*.py (each has a LESSONS dict).
Then check with: python -X utf8 scripts/teach/validate.py --part g4-gr4_operations
"""
import glob
import importlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from g4_gr4_operations_common import PART, questions, h  # noqa: E402
from g4_gr4_operations_rules_a import add_rule, sub_rule  # noqa: E402
from g4_gr4_operations_rules_b import mul_rule  # noqa: E402
from g4_gr4_operations_rules_c import minus_times_plus, plus_times, times_then, divide_plus_times  # noqa: E402
from g4_gr4_operations_rules_d import unit_cost, think_number, total_cost, percent_sale  # noqa: E402

GENERATED = re.compile(r"^(VAR\d*_|BOOST_|PH3_)|_V\d+$")


def is_generated(qid):
    return bool(GENERATED.search(qid))


def rule_for(q):
    t = q["questionText"].strip()
    i = lambda m, *gs: [int(m.group(g)) for g in gs]
    m = re.fullmatch(r"(\d+) \+ (\d+) = \?", t)
    if m:
        return add_rule(q, *i(m, 1, 2))
    m = re.fullmatch(r"(\d+) [-−] (\d+) = \?", t)
    if m:
        return sub_rule(q, *i(m, 1, 2))
    m = re.fullmatch(r"(\d+) × (\d+) = \?", t)
    if m:
        return mul_rule(q, *i(m, 1, 2))
    m = re.fullmatch(r"(?:Work out|Simplify): (\d+) [-−] (\d+) × (\d+) \+ (\d+)", t)
    if m:
        return minus_times_plus(q, *i(m, 1, 2, 3, 4))
    m = re.fullmatch(r"Simplify: (\d+) ÷ (\d+) \+ (\d+) × (\d+)", t)
    if m:
        return divide_plus_times(q, *i(m, 1, 2, 3, 4))
    m = re.fullmatch(r"Simplify: (\d+) \+ (\d+) × (\d+)", t)
    if m:
        return plus_times(q, *i(m, 1, 2, 3))
    m = re.fullmatch(r"Simplify: (\d+) × (\d+) ([+\-−]) (\d+)", t)
    if m:
        return times_then(q, int(m.group(1)), int(m.group(2)), "+" if m.group(3) == "+" else "-", int(m.group(4)))
    m = re.fullmatch(r"If (\d+) (\w+) cost Rs\.(\d+), what is the cost of one (\w+)\?", t)
    if m:
        return unit_cost(q, int(m.group(1)), m.group(2), int(m.group(3)), m.group(4))
    m = re.fullmatch(r"Think of (?:a|the) number (\d+)\. Multiply it by (\d+) and add (\d+)\. What do you get\?", t)
    if m:
        return think_number(q, *i(m, 1, 2, 3))
    m = re.fullmatch(r"(\w+) buys (\d+) (\w+) at Rs\.(\d+) each\. What is the total cost\?", t)
    if m:
        return total_cost(q, m.group(1), int(m.group(2)), m.group(3), int(m.group(4)))
    m = re.fullmatch(r"(\w+) (?:buys|bought) a (\w+) for Rs\.(\d+) and (?:sells|sold) it at a (profit|loss) of (\d+)%\. What is the selling price\?", t)
    if m:
        return percent_sale(q, m.group(1), m.group(2), int(m.group(3)), int(m.group(5)), m.group(4))
    return None


def place_answers(qid, script):
    """The hand-written lessons list the right choice first. Move it to a stable but varied place,
    so the right answer is not always the first button."""
    for i, beat in enumerate(script["beats"]):
        ask = beat.get("ask")
        if not ask or ask.get("kind") != "choose":
            continue
        choices = list(ask["choices"])
        right = choices.pop(ask["answer"])
        pos = h(qid, "ask%d" % i) % (len(choices) + 1)
        ask["choices"] = choices[:pos] + [right] + choices[pos:]
        ask["answer"] = pos
    return script


def main():
    qs = questions()
    out = {}
    no_rule = []
    for qid, q in qs.items():
        if is_generated(qid):
            script = rule_for(q)
            if script:
                out[qid] = script
            else:
                no_rule.append(qid)
    by_rule = len(out)
    for path in sorted(glob.glob(os.path.join(HERE, "g4_gr4_operations_auth_*.py"))):
        module = importlib.import_module(os.path.splitext(os.path.basename(path))[0])
        for qid, script in module.LESSONS.items():
            if qid not in qs:
                sys.exit("%s: %s is not a question of this topic" % (os.path.basename(path), qid))
            if qid in out:
                sys.exit("%s: %s already has a lesson" % (os.path.basename(path), qid))
            out[qid] = place_answers(qid, script)
    ordered = {qid: out[qid] for qid in qs if qid in out}
    os.makedirs(os.path.dirname(PART), exist_ok=True)
    with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
        f.write("\n")
    missing = [qid for qid in qs if qid not in out]
    print("wrote %d lessons (%d by rule, %d by hand); %d questions without one" % (
        len(ordered), by_rule, len(ordered) - by_rule, len(missing)))
    for qid in no_rule:
        print("generated but no rule matched:", qid, "|", qs[qid]["questionText"])


if __name__ == "__main__":
    main()
