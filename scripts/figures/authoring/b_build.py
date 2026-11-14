"""Merge b_2021.py ... b_2025.py (each defines ENTRIES) into the part file.

    python -X utf8 scripts/figures/authoring/b_build.py
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "data", "question-figures", "parts", "finals-2021-2025.json")
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

merged = {}
for year in ("2021", "2022", "2023", "2024", "2025"):
    if not os.path.exists(os.path.join(HERE, "b_%s.py" % year)):
        continue
    part = importlib.import_module("b_" + year).ENTRIES
    for qid, e in part.items():
        assert qid not in merged and ("_FP_%s_" % year) in qid, qid
        merged[qid] = e
    print(year, len(part))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(merged, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("wrote", len(merged), "entries")
