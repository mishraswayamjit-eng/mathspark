"""Convert the ipm-maths-practice app's Std V past-paper bank into Socratic seed format.

Source : <ipm-maths-practice>/index.html  (question data is inline JavaScript)
Output : data/ipm-pyq-grade5.json          (Socratic question objects + a report)
Merge  : --merge appends the converted questions to data/mathspark_complete_seed.json
         (idempotent: ids already present are skipped).

The converted rows follow the existing past-paper convention in the seed file
(e.g. source 'g6_final_2017', id 'EXT_G6_FP_2017_001'):

    id      EXT_G5_FP_<year>_<question number>
    topicId grade5
    source  g5_final_<year>

Nothing is generated or rewritten: question text, options, answer key, hint,
strategy and solution steps are carried over verbatim (HTML converted to plain
text; references to "option 1-4" in hints and steps become "option A-D"). Questions that depend on a figure or table are NOT converted, because
Socratic cannot render inline SVG; they are listed in the report instead.

Usage (from the repo root):
    python scripts/convert-ipm-pyq-grade5.py "<path to ipm-maths-practice/index.html>"
    python scripts/convert-ipm-pyq-grade5.py "<path>" --merge
"""

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "ipm-pyq-grade5.json"
SEED = ROOT / "data" / "mathspark_complete_seed.json"

# IPM chapter number -> Socratic subTopic. Each label contains exactly the
# Grade 5 `subTopicKey` (src/data/topicTree.ts) it should be filed under.
SUBTOPIC = {
    1: "Grade 5 — Numbers (place value and number system)",
    2: "Grade 5 — Place value",
    3: "Grade 5 — Sequence and series",
    4: "Grade 5 — Squares and square roots",
    5: "Grade 5 — Addition and subtraction",
    6: "Grade 5 — Multiplication and division",
    7: "Grade 5 — BODMAS",
    8: "Grade 5 — Equations",
    9: "Grade 5 — Algebraic expressions",
    10: "Grade 5 — HCF and LCM",
    11: "Grade 5 — Fractions",
    12: "Grade 5 — Decimals",
    13: "Grade 5 — Unitary method (ratio and proportion)",
    14: "Grade 5 — Percentage (money)",
    15: "Grade 5 — Profit and loss",
    16: "Grade 5 — Simple interest",
    17: "Grade 5 — Speed, distance and time",
    18: "Grade 5 — Angles",
    19: "Grade 5 — Perimeter (area and perimeter)",
    20: "Grade 5 — Area and perimeter",
}

SUP = str.maketrans("0123456789+-n", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ⁿ")


# ── Minimal parser for the JavaScript literals used by the app ────────────────

class Parser:
    def __init__(self, text: str):
        self.t = text
        self.i = 0

    def ws(self) -> None:
        t = self.t
        while self.i < len(t):
            if t[self.i] in " \t\r\n":
                self.i += 1
            elif t.startswith("/*", self.i):
                self.i = t.index("*/", self.i) + 2
            elif t.startswith("//", self.i):
                j = t.find("\n", self.i)
                self.i = len(t) if j < 0 else j
            else:
                break

    def value(self):
        self.ws()
        v = self.atom()
        # string concatenation: "a" + b
        while True:
            self.ws()
            if self.i < len(self.t) and self.t[self.i] == "+":
                self.i += 1
                v = str(v) + str(self.value_no_concat())
            else:
                return v

    def value_no_concat(self):
        self.ws()
        return self.atom()

    def atom(self):
        t = self.t
        c = t[self.i]
        if c == "[":
            self.i += 1
            out = []
            while True:
                self.ws()
                if t[self.i] == "]":
                    self.i += 1
                    return out
                out.append(self.value())
                self.ws()
                if t[self.i] == ",":
                    self.i += 1
        if c == "{":
            self.i += 1
            obj = {}
            while True:
                self.ws()
                if t[self.i] == "}":
                    self.i += 1
                    return obj
                m = re.compile(r"[A-Za-z_$][\w$]*").match(t, self.i)
                if m:
                    key = m.group(0)
                    self.i = m.end()
                else:
                    key = self.string(t[self.i])
                self.ws()
                assert t[self.i] == ":", f"expected ':' at {self.i}: {t[self.i:self.i+40]!r}"
                self.i += 1
                obj[key] = self.value()
                self.ws()
                if t[self.i] == ",":
                    self.i += 1
        if c in "\"'":
            return self.string(c)
        if c == "`":
            return self.template()
        m = re.compile(r"-?\d+(\.\d+)?").match(t, self.i)
        if m:
            self.i = m.end()
            s = m.group(0)
            return float(s) if "." in s else int(s)
        # identifier / call expression: not evaluated, kept as a figure marker
        return self.expr_until_delim()

    def string(self, quote: str) -> str:
        t = self.t
        assert t[self.i] == quote
        self.i += 1
        out = []
        while t[self.i] != quote:
            ch = t[self.i]
            if ch == "\\":
                nxt = t[self.i + 1]
                if nxt == "n":
                    out.append("\n")
                elif nxt == "t":
                    out.append("\t")
                elif nxt == "u":
                    out.append(chr(int(t[self.i + 2:self.i + 6], 16)))
                    self.i += 4
                else:
                    out.append(nxt)
                self.i += 2
            else:
                out.append(ch)
                self.i += 1
        self.i += 1
        return "".join(out)

    def template(self) -> str:
        t = self.t
        assert t[self.i] == "`"
        self.i += 1
        out = []
        while t[self.i] != "`":
            if t[self.i] == "\\":
                out.append(t[self.i + 1])
                self.i += 2
            elif t.startswith("${", self.i):
                self.i += 2
                start = self.i
                self.skip_balanced("}")
                out.append(eval_expr(t[start:self.i - 1]))
            else:
                out.append(t[self.i])
                self.i += 1
        self.i += 1
        return "".join(out)

    def skip_balanced(self, close: str) -> None:
        """Advance past the matching `close`, honouring nested brackets and strings."""
        t = self.t
        depth = 0
        pairs = {"(": ")", "[": "]", "{": "}"}
        closers = set(pairs.values())
        while True:
            ch = t[self.i]
            if ch in "\"'":
                self.string(ch)
                continue
            if ch == "`":
                self.template()
                continue
            if depth == 0 and ch == close:
                self.i += 1
                return
            if ch in pairs:
                depth += 1
            elif ch in closers:
                depth -= 1
            self.i += 1

    def expr_until_delim(self) -> str:
        t = self.t
        start = self.i
        depth = 0
        while True:
            ch = t[self.i]
            if ch in "\"'":
                self.string(ch)
                continue
            if ch == "`":
                self.template()
                continue
            if ch in "([{":
                depth += 1
            elif ch in ")]}":
                if depth == 0:
                    break
                depth -= 1
            elif ch == "," and depth == 0:
                break
            self.i += 1
        return eval_expr(t[start:self.i])


def eval_expr(src: str) -> str:
    """fr(a,b) becomes a fraction marker; anything else is a figure marker."""
    src = src.strip()
    if src.startswith("fr(") and src.endswith(")"):
        p = Parser(src[3:-1])
        a = p.value()
        p.ws()
        assert p.t[p.i] == ",", src
        p.i += 1
        b = p.value()
        return f"[[FR:{a}|{b}]]"
    return "[[FIG]]"


# ── Text conversion ──────────────────────────────────────────────────────────

FR_RE = re.compile(r"\[\[FR:((?:(?!\[\[FR:)[^|\]])*)\|((?:(?!\[\[FR:)[^|\]])*)\]\]")


def _frac(m: re.Match) -> str:
    a, b = m.group(1).strip(), m.group(2).strip()
    simple = re.compile(r"^[\w.%°₹]+$")
    a2 = a if simple.match(a) else f"({a})"
    b2 = b if simple.match(b) else f"({b})"
    return f"{a2}/{b2}"


def _sup(m: re.Match) -> str:
    inner = m.group(1).strip()
    if re.fullmatch(r"[0-9+\-n]+", inner):
        return inner.translate(SUP)
    if inner.isalpha():
        return inner          # ordinals: 12<sup>th</sup> -> 12th
    return f"^({inner})"


def to_plain(s: str) -> str:
    # mixed numbers: 2[[FR:1|3]] -> 2 1/3
    s = re.sub(r"(\d)\[\[FR:", r"\1 [[FR:", s)
    prev = None
    while prev != s:              # innermost-first, for nested fractions
        prev = s
        s = FR_RE.sub(_frac, s)
    s = re.sub(r"<sup>(.*?)</sup>", _sup, s, flags=re.S)
    s = re.sub(r"</?b>", "", s)
    s = re.sub(r"<br\s*/?>", " ", s)
    s = html.unescape(s)
    return re.sub(r"[ \t]+", " ", s).strip()


OPTION_REF = re.compile(r"\b(options?|statements?)\s+([1-4])(\s*[–-]\s*([1-4]))?", re.I)


def relabel_options(s: str) -> str:
    """The source numbers its options 1-4; Socratic letters them A-D.

    "Option 3: ..." -> "Option C: ...", "options 1–3" -> "options A–C".
    Applied to hints and solution steps only, never to question or option text.
    """
    def sub(m: re.Match) -> str:
        first = "ABCD"[int(m.group(2)) - 1]
        if m.group(4):
            return f"{m.group(1)} {first}–{'ABCD'[int(m.group(4)) - 1]}"
        return f"{m.group(1)} {first}"
    return OPTION_REF.sub(sub, s)


def has_figure(s: str) -> bool:
    return "[[FIG]]" in s or bool(re.search(r"<[a-zA-Z/]", re.sub(r"</?(b|sup|br)\b[^>]*>", "", s)))


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def difficulty(n: int) -> str:
    # The source has no difficulty labels. IPM papers get harder towards the
    # end, so position in the paper is used as a stand-in. This is a heuristic.
    return "Easy" if n <= 12 else "Medium" if n <= 28 else "Hard"


# ── Main ─────────────────────────────────────────────────────────────────────

def load_source(path: Path):
    text = path.read_text(encoding="utf-8")
    start = text.index("const CH=[")
    end = text.index("/* ---------- state ----------")
    region = text[start:end]

    chapters, questions = [], []
    for m in re.finditer(r"^const (CH|Q|Q\d{4})=\[", region, flags=re.M):
        p = Parser(region)
        p.i = m.end() - 1
        arr = p.value()
        if m.group(1) == "CH":
            chapters = arr
        else:
            questions.extend(arr)
    return chapters, questions


def convert(chapters, questions):
    out, skipped_fig, skipped_dup, problems = [], [], [], []
    seen = {}
    key_check_miss = []

    def year_of(y: str) -> int:
        return 2025 if y == "2024-25" else int(y)

    for q in sorted(questions, key=lambda q: (year_of(q["y"]), q["n"])):
        year, n = year_of(q["y"]), q["n"]
        qid = f"EXT_G5_FP_{year}_{n:03d}"
        fields = [q["q"], q["h"], q["f"], *q["o"], *q["s"]]

        if len(q["o"]) != 4 or not (0 <= q["a"] <= 3) or q["c"] not in SUBTOPIC:
            problems.append(qid)
            continue
        if any(has_figure(f) for f in fields):
            where = "question" if has_figure(q["q"]) else "options" if any(has_figure(o) for o in q["o"]) else "solution/hint"
            skipped_fig.append({"id": qid, "paper": q["y"], "q": n, "chapter": chapters[q["c"] - 1]["t"], "figureIn": where})
            continue

        text = to_plain(q["q"])
        opts = [to_plain(o) for o in q["o"]]
        dup_key = norm(text) + "|" + "|".join(sorted(norm(o) for o in opts))
        if dup_key in seen:
            skipped_dup.append({"id": qid, "duplicateOf": seen[dup_key]})
            continue
        seen[dup_key] = qid

        steps = [relabel_options(to_plain(s)) for s in q["s"]]
        answer = opts[q["a"]]
        # Soft consistency signal only (NOT verification): does the keyed
        # option's value appear anywhere in the worked solution?
        core = norm(re.sub(r"[₹%°]|cm²|m²|sq\.?\s*\w+|\b(cm|m|km|kg|g|years?|days?|hours?|minutes?|km/h|m/s)\b", "", answer))
        if core and core not in norm(" ".join(steps)):
            key_check_miss.append({"id": qid, "keyed": answer, "lastStep": steps[-1][:160]})

        out.append({
            "id": qid,
            "topicId": "grade5",
            "subTopic": SUBTOPIC[q["c"]],
            "difficulty": difficulty(n),
            "questionText": text,
            "questionLatex": "",
            "options": [{"id": k, "text": o} for k, o in zip("ABCD", opts)],
            "correctAnswer": "ABCD"[q["a"]],
            "hints": [relabel_options(to_plain(q["h"])), relabel_options(to_plain(q["f"])), ""],
            "stepByStep": [{"step": i + 1, "text": s, "latex": ""} for i, s in enumerate(steps)],
            "misconceptions": {"A": "", "B": "", "C": "", "D": ""},
            "source": f"g5_final_{year}",
        })

    report = {
        "sourceQuestions": len(questions),
        "converted": len(out),
        "skippedFigure": skipped_fig,
        "skippedDuplicate": skipped_dup,
        "malformed": problems,
        "answerNotFoundInSolution": key_check_miss,
        "byPaper": dict(sorted(Counter(q["source"] for q in out).items())),
        "bySubTopic": dict(Counter(q["subTopic"] for q in out).most_common()),
        "byDifficulty": dict(Counter(q["difficulty"] for q in out)),
        "chapterMapping": {c["t"]: SUBTOPIC[i + 1] for i, c in enumerate(chapters)},
    }
    return out, report


def merge(new_questions) -> None:
    raw = SEED.read_text(encoding="utf-8")
    seed = json.loads(raw)
    existing = {q["id"] for q in seed["questions"]}
    add = [q for q in new_questions if q["id"] not in existing]
    if not add:
        print("merge: nothing to add (all ids already in the seed)")
        return
    tail = "]}"
    assert raw.rstrip().endswith(tail), "unexpected seed file ending"
    # Splice into the questions array so the existing 15 MB of text is untouched.
    body = raw.rstrip()[: -len(tail)]
    chunk = ",".join(json.dumps(q, ensure_ascii=True, separators=(",", ":")) for q in add)
    SEED.write_text(body + "," + chunk + tail, encoding="utf-8", newline="")
    check = json.loads(SEED.read_text(encoding="utf-8"))
    assert len(check["questions"]) == len(seed["questions"]) + len(add)
    assert len({q["id"] for q in check["questions"]}) == len(check["questions"]), "duplicate ids after merge"
    first = len(seed["questions"])
    print(f"merge: appended {len(add)} questions at index {first}..{first + len(add) - 1} "
          f"(seed pages {first // 200}..{(first + len(add) - 1) // 200}, 200 per page)")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    chapters, questions = load_source(Path(args[0]))
    out, report = convert(chapters, questions)
    OUT.write_text(json.dumps({"report": report, "questions": out}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(f"source questions : {report['sourceQuestions']}")
    print(f"converted        : {report['converted']}")
    print(f"skipped (figure) : {len(report['skippedFigure'])}")
    print(f"skipped (dup)    : {len(report['skippedDuplicate'])}")
    print(f"malformed        : {len(report['malformed'])}")
    print(f"answer not found in solution text (soft check): {len(report['answerNotFoundInSolution'])}")
    print(f"wrote {OUT.relative_to(ROOT)}")
    if "--merge" in sys.argv:
        merge(out)


if __name__ == "__main__":
    main()
