"""Build data/teach/parts/g4-gr4_units.json: "Explain it to me" lessons for gr4_units.

    python -X utf8 scripts/teach/gen/g4_units.py

Generated families get their lesson from a rule (g4_units_rules.py). Every other question
has a lesson written for it (g4_units_a.py, g4_units_b.py, ...).
"""
import importlib

from g4_units_lib import finish, questions, write_part
from g4_units_rules import rule_lessons

TOPIC = "gr4_units"
AUTHORED = ["g4_units_a", "g4_units_b", "g4_units_c", "g4_units_d", "g4_units_e", "g4_units_f"]


def main():
    qs = questions(TOPIC)
    lessons = {}
    for qid, beats in rule_lessons(qs).items():
        lessons[qid] = finish(qid, beats, "rule")
    for name in AUTHORED:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name != name:
                raise
            continue
        for qid, beats in mod.LESSONS.items():
            if qid in lessons:
                raise ValueError("%s has two lessons" % qid)
            lessons[qid] = finish(qid, beats, "authored")
    write_part(TOPIC, lessons)


if __name__ == "__main__":
    main()
