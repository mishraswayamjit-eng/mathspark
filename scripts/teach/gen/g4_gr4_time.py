"""Build data/teach/parts/g4-gr4_time.json: a lesson for every Grade 4 time and calendar question.

    python -X utf8 scripts/teach/gen/g4_gr4_time.py

Every question in this topic is a one-off, so every lesson is written by hand, in the
helper files g4_gr4_time_a.py, _b.py, ... Each has a dict L: question id -> list of beats.
"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_time_lib import write_part  # noqa: E402

HELPERS = ["g4_gr4_time_a", "g4_gr4_time_b", "g4_gr4_time_c", "g4_gr4_time_d", "g4_gr4_time_e", "g4_gr4_time_f"]


def main():
    lessons = {}
    for name in HELPERS:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), name + ".py")):
            continue
        mod = importlib.import_module(name)
        for qid, beats in mod.L.items():
            if qid in lessons:
                sys.exit("two lessons for %s" % qid)
            lessons[qid] = ("authored", beats)
    write_part("gr4_time", lessons)


if __name__ == "__main__":
    main()
