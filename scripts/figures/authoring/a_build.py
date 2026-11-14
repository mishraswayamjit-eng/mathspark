"""Assemble data/question-figures/parts/finals-2016-2020.json from the a_y*.py files.

    python -X utf8 scripts/figures/authoring/a_build.py

Each a_y*.py file holds a dict VISUALS = { question id: QuestionVisual } written
by hand, one question at a time. This script only merges them and writes JSON.
"""
import glob
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "data", "question-figures", "parts", "finals-2016-2020.json")


def main():
    sys.path.insert(0, HERE)
    sys.dont_write_bytecode = True
    merged = {}
    for path in sorted(glob.glob(os.path.join(HERE, "a_y*.py"))):
        name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for qid, entry in mod.VISUALS.items():
            if qid in merged:
                sys.exit("%s appears twice (again in %s)" % (qid, name))
            merged[qid] = entry
    ordered = {k: merged[k] for k in sorted(merged)}
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d entries" % len(ordered))


if __name__ == "__main__":
    main()
