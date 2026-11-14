"""Assemble data/question-figures/parts/extracted.json from the c_b*.py batches.
    python -X utf8 scripts/figures/authoring/c_build.py
Each batch module defines E = { "<question id>": QuestionVisual }.
"""
import glob, importlib.util, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "data", "question-figures", "parts", "extracted.json")

sys.path.insert(0, HERE)
merged = {}
for path in sorted(glob.glob(os.path.join(HERE, "c_b*.py"))):
    name = os.path.splitext(os.path.basename(path))[0]
    if name == "c_build":
        continue
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for qid, e in mod.E.items():
        if qid in merged:
            sys.exit("%s defined twice (%s)" % (qid, name))
        merged[qid] = e

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(dict(sorted(merged.items())), f, ensure_ascii=False, indent=1)
    f.write("\n")
print("wrote %d entries" % len(merged))
