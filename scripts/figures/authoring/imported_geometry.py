"""Build data/question-figures/parts/imported-geometry.json.

    python -X utf8 scripts/figures/authoring/imported_geometry.py            # build the part
    python -X utf8 scripts/figures/authoring/imported_geometry.py --verbose  # also list every note or step figure held back

Figures for the Grade 5 questions imported from the database (sources
ai_generated, ipm_textbook, official_ipm_2020) whose topic is Area & Perimeter,
Angles & Lines or Triangles. The figures themselves are in
imported_geometry_area.py, imported_geometry_angles.py and
imported_geometry_triangles.py; the shared shapes are in imported_geometry_lib.py.

Every question in scope must either get a figure or be listed with a reason
(skip): the build stops if one is unaccounted for. Then check the part:

    python -X utf8 scripts/figures/validate.py --part data/question-figures/parts/imported-geometry.json
"""
import collections
import copy
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "data", "question-figures", "parts", "imported-geometry.json")
sys.path.insert(0, HERE)
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.join(ROOT, "scripts", "figures"))

import bank  # noqa: E402
import validate as V  # noqa: E402  (read only: the same number rules the checker uses)
import imported_geometry_lib as lib  # noqa: E402

NODES = ("gr5_area", "gr5_angles", "gr5_triangles")
SOURCES = ("ai_generated", "ipm_textbook", "official_ipm_2020")
BATCHES = ("imported_geometry_area", "imported_geometry_angles", "imported_geometry_triangles")


def short_key(qid):
    if qid.startswith("AIGEN_grade5_"):
        return qid[len("AIGEN_grade5_"):][:8]
    if qid.startswith("IPMTB_grade5_"):
        return qid[len("IPMTB_grade5_"):]
    return qid


def state(fig, allowed):
    """('ok', None), ('schema', [messages]) or ('numbers', [numbers not stated yet])."""
    ctx = V.check_figure(fig, "figure")
    if ctx.errors:
        return "schema", ctx.errors
    extra = sorted(x for x in ctx.numbers if x not in allowed and x not in V.CONSTANTS)
    return ("numbers", extra) if extra else ("ok", None)


def resolve(spec, allowed, where, held, hard):
    """The first alternative whose numbers are all stated, with the first note that is too."""
    last = None
    for alt in (spec if isinstance(spec, list) else [spec]):
        fig = copy.deepcopy(alt)
        notes = fig.pop("note", None)
        if isinstance(notes, str):
            notes = [notes]
        what, detail = state(fig, allowed)
        if what == "schema":
            hard.append("%s: %s" % (where, "; ".join(detail)))
            continue
        if what == "numbers":
            last = "shows %s" % V.fmt(detail)
            continue
        for note in notes or []:
            with_note = dict(fig, note=note)
            what, detail = state(with_note, allowed)
            if what == "ok":
                return with_note
            if what == "schema":
                hard.append("%s: note %r: %s" % (where, note, "; ".join(detail)))
        if notes:
            held.append("%s: kept without a note (%r not stated yet)" % (where, notes[0]))
        return fig
    held.append("%s: no figure (%s, not stated yet)" % (where, last))
    return None


def main():
    verbose = "--verbose" in sys.argv
    for name in BATCHES:
        importlib.import_module(name)

    questions = [q for q in bank.load_bank(5) if q.get("node") in NODES and q.get("source") in SOURCES]
    by_key = {}
    for q in questions:
        key = short_key(q["id"])
        if key in by_key:
            sys.exit("short key %s is not unique" % key)
        by_key[key] = q

    unknown = sorted((set(lib.ENTRIES) | set(lib.SKIPS)) - set(by_key))
    missing = sorted(set(by_key) - set(lib.ENTRIES) - set(lib.SKIPS))
    if unknown:
        sys.exit("not a question in scope: %s" % ", ".join(unknown))

    part = {}
    held, hard, problems = [], [], []
    for key in sorted(lib.ENTRIES, key=lambda k: by_key[k]["id"]):
        spec = lib.ENTRIES[key]
        q = by_key[key]
        qid = q["id"]
        q_numbers = V.numbers_in(q.get("questionText", ""))
        o_numbers = set()
        for text in V.option_texts(q):
            o_numbers |= V.numbers_in(text)
        entry = {"origin": spec["origin"]}
        if spec["uses_options"]:
            entry["usesOptions"] = True
        if spec["figure"] is not None:
            fig = resolve(spec["figure"], q_numbers | (o_numbers if spec["uses_options"] else set()), "%s figure" % key, hard, hard)
            if fig is not None:
                entry["figure"] = fig
        own = q.get("stepByStep") or []
        bad = [i for i in spec["steps"] if not 0 <= i < len(own)]
        if bad:
            hard.append("%s: step %s does not exist (the question has %d steps)" % (key, bad, len(own)))
        figs = []
        allowed = q_numbers | o_numbers
        for i, step in enumerate(own):
            allowed = allowed | V.numbers_in(step.get("text", ""))
            figs.append(resolve(spec["steps"][i], allowed, "%s step %d" % (key, i), held, hard) if i in spec["steps"] else None)
        if any(f is not None for f in figs):
            entry["stepFigures"] = figs
        if "figure" not in entry and "stepFigures" not in entry:
            hard.append("%s: nothing left to show" % key)
            continue
        problems += V.check_entry(qid, entry, q)
        part[qid] = entry

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(sorted(part.items())), f, ensure_ascii=False, indent=1)
        f.write("\n")

    # ── Report ───────────────────────────────────────────────────────────────
    print("%d questions in scope, %d with a visual, %d left without, %d not yet decided" % (
        len(by_key), len(part), len(lib.SKIPS), len(missing)))
    kinds = collections.defaultdict(collections.Counter)
    for qid, entry in part.items():
        node = by_key[short_key(qid)]["node"]
        kinds[node][entry["figure"]["kind"] if "figure" in entry else "(step figures only)"] += 1
    for node in NODES:
        total = sum(1 for q in questions if q["node"] == node)
        print("  %-14s %3d of %3d   %s" % (node, sum(kinds[node].values()), total,
                                          ", ".join("%s %d" % kv for kv in kinds[node].most_common())))
    step_figs = sum(1 for e in part.values() for f in e.get("stepFigures", []) if f is not None)
    print("  %d step figures in all; %d notes or step figures held back until their numbers are stated" % (step_figs, len(held)))
    for category in ("contradiction", "no-picture"):
        rows = sorted((by_key[k]["id"], r) for k, (c, r) in lib.SKIPS.items() if c == category)
        print("\nLeft without a figure, %s (%d):" % (category, len(rows)))
        for qid, reason in rows:
            print("  %s  %s" % (qid, reason))
    if verbose:
        print("\nHeld back:")
        for line in held:
            print("  " + line)
    if missing:
        print("\nNOT YET DECIDED (%d):" % len(missing))
        for key in missing:
            print("  %s  %s" % (key, by_key[key]["id"]))
    if hard or problems:
        print("\n%d PROBLEMS" % (len(hard) + len(problems)))
        for line in hard + problems:
            print("  " + line)
        sys.exit(1)
    print("\nwrote %s (%d questions)" % (os.path.relpath(OUT, ROOT), len(part)))
    if missing:
        sys.exit(1)


if __name__ == "__main__":
    main()
