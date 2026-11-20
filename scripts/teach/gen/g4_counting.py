"""Build data/teach/parts/g4-gr4_counting.json: "Explain it to me" lessons for gr4_counting.

    python -X utf8 scripts/teach/gen/g4_counting.py

The topic has no generated families, so every lesson is written for its question
(g4_counting_a.py, g4_counting_b.py, ...).
"""
import importlib

from g4_counting_lib import TOPIC, finish, write_part

AUTHORED = ["g4_counting_a", "g4_counting_b", "g4_counting_c", "g4_counting_d"]


def main():
    lessons = {}
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
