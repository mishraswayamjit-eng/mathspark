# -*- coding: utf-8 -*-
"""
Check the four new concept lessons before they can ship.

    python -X utf8 scripts/lessons/check_new_lessons.py [slug ...]

It reads ONLY the JSON under data/lessons/ (what the app serves) and never the
content_*.py files they were built from, so a slip in the text cannot hide.

What is checked, for every lesson file:

  1. Shape: valid JSON, 5 levels (ids 1-5), 5 lessons + 8 quiz items each,
     unique ids, the fields src/types/lesson.ts needs, the same header as the
     entry in src/data/lessonTopics.ts.
  2. Quiz answers: every quiz id has an expected computation in
     expected_<topic>.py. It is evaluated with exact fractions and must equal
     the keyed answer. Every number in that computation must appear in the
     question (or be declared as a constant such as 60 minutes in an hour), so
     the computation really is about the question on screen.
  3. Every equality written anywhere in the lesson ("345 + 278 = 623",
     "3x + 2x = 5x", "x = 4 ... 3x + 5 = 17", notation boxes included) is
     recomputed: plain arithmetic exactly, algebra as an identity at several
     values or with the values the lesson assigns. An equality the checker
     cannot prove is a failure unless the exact sentence is listed in ALLOW (or
     the fact in FACTS) with its own proof.
  4. Rendering and tone: no backslash or brace outside notation boxes (the app
     would treat the whole sentence as LaTeX), only LaTeX the checker
     understands inside them, answers a child can type (digits only), and none
     of the words the app must never say to a child.

Exit code 0 only when nothing failed.
"""
import importlib
import json
import os
import random
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
LESSON_DIR = os.path.join(ROOT, "data", "lessons")
sys.path.insert(0, HERE)

TOPICS = {
    # slug: (id prefix, expected-module, letters used as variables)
    "addition-subtraction": ("as", "expected_addition_subtraction", ""),
    "multiplication-division": ("md", "expected_multiplication_division", ""),
    "algebraic-expressions": ("ae", "expected_algebraic_expressions", "xymnpq"),
    "speed-distance-time": ("sd", "expected_speed_distance_time", ""),
}

LEVEL_STYLE = [
    ("\U0001F7E2", "#58CC02", "from-green-400 to-green-600"),
    ("\U0001F535", "#1CB0F6", "from-blue-400 to-blue-600"),
    ("\U0001F7E1", "#FFC800", "from-yellow-400 to-yellow-600"),
    ("\U0001F7E0", "#FF9600", "from-orange-400 to-orange-600"),
    ("\U0001F534", "#FF4B4B", "from-red-400 to-red-600"),
]
DIFFICULTY = ["direct", "direct", "near_transfer", "near_transfer",
              "stretch", "stretch", "challenge", "challenge"]

FORBIDDEN = re.compile(r"\b(wrong|incorrect|fail|failed|failure|error|mistake|stupid|silly)\b", re.I)

# Unit facts a sentence may state. Each has a proof that is evaluated too.
FACTS = {
    "1 km = 1000 m": "1 * 1000 == 1000",
    "1 hour = 60 minutes": "60 == 60",
    "1 minute = 60 seconds": "60 == 60",
    "1 hour = 3600 seconds": "60 * 60 == 3600",
    "1 day = 24 hours": "24 == 24",
    "1 week = 7 days": "7 == 7",
    "1 m/s = 3.6 km/h": "1 * 3600 / 1000 == 3.6",
    "18 km/h = 5 m/s": "18 * 1000 / 3600 == 5",
    "36 km/h = 10 m/s": "36 * 1000 / 3600 == 10",
    "72 km/h = 20 m/s": "72 * 1000 / 3600 == 20",
    "54 km/h = 15 m/s": "54 * 1000 / 3600 == 15",
    "90 km/h = 25 m/s": "90 * 1000 / 3600 == 25",
    "108 km/h = 30 m/s": "108 * 1000 / 3600 == 30",
}

# ── exact evaluation ─────────────────────────────────────────────────────────

NUM_RE = re.compile(r"\d+(?:\.\d+)?")


def _ds(n):
    return Fraction(sum(int(c) for c in str(int(n))))


def _gcd(a, b):
    a, b = int(a), int(b)
    while b:
        a, b = b, a % b
    return Fraction(a)


def _lcm(a, b):
    return Fraction(int(a) * int(b)) / _gcd(a, b)


def _rnd(n, base):
    """Round to the nearest multiple of base; a half rounds up, as taught."""
    n, base = Fraction(n), Fraction(base)
    return Fraction((n / base + Fraction(1, 2)).__floor__()) * base


SAFE = {"__builtins__": {}, "F": Fraction, "ds": _ds, "gcd": _gcd, "lcm": _lcm, "rnd": _rnd,
        "min": min, "max": max, "abs": abs, "True": True, "False": False}


def exact(expr, env=None):
    """Evaluate a Python arithmetic expression with every number as a Fraction."""
    py = NUM_RE.sub(lambda m: "F('%s')" % m.group(0), expr)
    scope = dict(SAFE)
    if env:
        scope.update(env)
    return eval(py, scope)  # noqa: S307 - expressions come from this repo only


def show(v):
    """Fraction -> the string a child would type (whole number or decimal)."""
    if isinstance(v, bool):
        return str(v)
    v = Fraction(v)
    if v.denominator == 1:
        return str(v.numerator)
    d = v.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    if d != 1:
        return "%d/%d" % (v.numerator, v.denominator)
    digits = 0
    x = v
    while x.denominator != 1:
        x *= 10
        digits += 1
    sign = "-" if x < 0 else ""
    s = str(abs(x.numerator)).rjust(digits + 1, "0")
    return sign + s[:-digits] + "." + s[-digits:]


# ── reading equalities out of text ───────────────────────────────────────────

OP, EQ, LP, RP, POW, OPND, OTHER = "op", "eq", "lp", "rp", "pow", "opnd", "other"
TRAIL = ".,;:!?'\"\u201d\u2019"
LEAD = "'\"\u201c\u2018"


def strip_commas(s):
    return re.sub(r"(?<=\d),(?=\d{2,3}(?!\d))", "", s)


def normalise(s):
    s = s.replace("\u2212", "-").replace("\u00d7", "*").replace("\u00f7", "/")
    s = s.replace("\u20b9", "").replace("\u00b2", "^2").replace("\u00b3", "^3")
    s = strip_commas(s)
    s = re.sub(r"([\dA-Za-z)])\(", r"\1 * (", s)
    s = re.sub(r"\)(?=[\dA-Za-z(])", ") * ", s)
    # a slash between two letters is a unit (km/h), not a division
    s = re.sub(r"(?<![A-Za-z])/|/(?![A-Za-z])", " / ", s)
    s = re.sub(r"([+\-*=()])", r" \1 ", s)
    return s


def classify(tok, letters):
    if tok in ("+", "-", "*", "/"):
        return OP
    if tok == "=":
        return EQ
    if tok == "(":
        return LP
    if tok == ")":
        return RP
    if re.match(r"^\^\d+$", tok):
        return POW
    if re.match(r"^\d+(\.\d+)?$", tok):
        return OPND
    if letters:
        v = "[" + letters + "]"
        if re.match(r"^\d+(\.\d+)?" + v + r"{1,3}(\^\d+)?$", tok):
            return OPND
        if re.match(r"^" + v + r"{1,3}(\^\d+)?$", tok):
            return OPND
    if re.match(r"^\d+(\.\d+)?\^\d+$", tok):
        return OPND
    return OTHER


def tokenise(s, letters):
    out = []
    for raw in normalise(s).split():
        t = raw.lstrip(LEAD)
        brk = False
        while len(t) > 1 and t[-1] in TRAIL:
            t = t[:-1]
            brk = True
        if t in TRAIL:
            if out:
                out[-1] = (out[-1][0], out[-1][1], True)
            continue
        out.append((t, classify(t, letters), brk))
    return out


def opnd_to_py(tok):
    m = re.match(r"^(\d+(?:\.\d+)?)?([a-z]*)(?:\^(\d+))?$", tok)
    parts = []
    if m.group(1):
        parts.append(m.group(1))
    parts.extend(list(m.group(2)))
    s = "*".join(parts)
    if m.group(3):
        s += "**" + m.group(3)
    # 12xy is one term: 12xy / 4y must mean (12xy) / (4y)
    return "(" + s + ")" if len(parts) > 1 else s


def part_to_py(tokens):
    bits = []
    for t, c in tokens:
        if c == OPND:
            bits.append(opnd_to_py(t))
        elif c == POW:
            bits.append("**" + t[1:])
        else:
            bits.append(t)
    return " ".join(bits)


def part_vars(tokens):
    vs = set()
    for t, c in tokens:
        if c == OPND:
            vs.update(re.sub(r"\^\d+$", "", t).strip("0123456789."))
    return vs


class Scanner(object):
    """Collects every equality in a group of strings that share variable values
    (one lesson, or one quiz item)."""

    def __init__(self, letters, where):
        self.letters = letters
        self.where = where
        self.env = {}
        self.ok = 0
        self.identities = 0
        self.substituted = 0
        self.assigned = 0
        self.labels = []
        self.facts = 0
        self.fails = []
        self.deferred = []
        self.allowed_texts = set()

    def scan(self, text, field, allow, key=None):
        key = text if key is None else key
        toks = tokenise(text, self.letters)
        consumed = set()
        local_fails = []
        run = []

        def flush():
            if run:
                self._process(list(run), text, consumed, local_fails)
                del run[:]

        for i, (t, c, brk) in enumerate(toks):
            if c == OTHER:
                flush()
                continue
            if c in (OPND, LP) and run and run[-1][2] in (OPND, RP, POW):
                flush()
            run.append((i, t, c))
            if brk:
                flush()
        flush()

        # every '=' that no verified chain used
        loose = 0
        for i, (t, c, _b) in enumerate(toks):
            if c != EQ or i in consumed:
                continue
            left = toks[i - 1][0] if i > 0 else ""
            left2 = toks[i - 2][0] if i > 1 else ""
            right = toks[i + 1][0] if i + 1 < len(toks) else ""
            near_digit = bool(re.search(r"\d", left + right))
            if not near_digit:
                continue  # a formula in words: Speed = Distance / Time
            left_cls = toks[i - 1][1] if i > 0 else OTHER
            if left_cls == OTHER and not re.search(r"\d", left) and not re.search(r"\d", left2):
                self.labels.append("%s %s: %s" % (self.where, field, text))
                continue
            loose += 1
        if loose:
            flat = re.sub(r"\s+", " ", strip_commas(text))
            n_facts = sum(flat.count(f) for f in FACTS)
            if n_facts >= loose:
                self.facts += loose
            else:
                local_fails.append("equality the checker could not prove")

        if key in allow:
            self.allowed_texts.add(text)
            for proof in allow[key]:
                if exact(proof) is not True:
                    self.fails.append("%s %s: ALLOW proof is not true: %s" % (self.where, field, proof))
            self.ok += len(allow[key])
        else:
            for f in local_fails:
                self.fails.append("%s %s: %s :: %s" % (self.where, field, f, text))

    def _process(self, run, text, consumed, fails):
        def balance(r):
            while r and sum(1 for x in r if x[2] == LP) > sum(1 for x in r if x[2] == RP) and r[0][2] == LP:
                r.pop(0)
            while r and sum(1 for x in r if x[2] == RP) > sum(1 for x in r if x[2] == LP) and r[-1][2] == RP:
                r.pop()

        balance(run)
        taint_first = taint_last = False
        lead_eqs = []  # "pens sold = 1180 + 765 = 1945": the first '=' only names the sum
        while run and run[0][2] in (OP, EQ, POW, RP):
            if run[0][2] != EQ:
                taint_first = True
            else:
                lead_eqs.append(run[0][0])
            run.pop(0)
        while run and run[-1][2] in (OP, EQ, LP):
            if run[-1][2] != EQ:
                taint_last = True
            run.pop()
        balance(run)
        if not any(x[2] == EQ for x in run):
            return
        parts, eqs, cur = [], [], []
        for i, t, c in run:
            if c == EQ:
                parts.append(cur)
                eqs.append(i)
                cur = []
            else:
                cur.append((t, c))
        parts.append(cur)
        if taint_first:
            parts, eqs = parts[1:], eqs[1:]
        if taint_last:
            parts, eqs = parts[:-1], eqs[:-1]
        if len(parts) < 2 or any(len(p) == 0 for p in parts):
            return
        snippet = " = ".join(" ".join(t for t, _c in p) for p in parts)
        pys = [part_to_py(p) for p in parts]
        vs = set()
        for p in parts:
            vs |= part_vars(p)
        consumed.update(eqs)
        if not taint_first:
            consumed.update(lead_eqs)
        try:
            if not vs:
                vals = [exact(p) for p in pys]
                if all(v == vals[0] for v in vals):
                    self.ok += len(vals) - 1
                else:
                    fails.append("arithmetic does not hold: %s  (values %s)" % (snippet, ", ".join(show(v) for v in vals)))
                return
            # x = 4 : the lesson gives a variable a value
            if len(parts) == 2:
                for a, b in ((0, 1), (1, 0)):
                    if len(parts[a]) == 1 and re.match(r"^[a-z]$", parts[a][0][0]) and not part_vars(parts[b]):
                        self.env[parts[a][0][0]] = exact(pys[b])
                        self.assigned += 1
                        return
            if self._identity(pys, vs):
                self.identities += len(pys) - 1
                return
            # y = x - 2 : a new letter defined from letters that already have values
            if len(parts) == 2:
                for a, b in ((0, 1), (1, 0)):
                    name = parts[a][0][0] if len(parts[a]) == 1 else ""
                    if (re.match(r"^[a-z]$", name) and name not in self.env
                            and all(v in self.env for v in part_vars(parts[b]))):
                        self.env[name] = exact(pys[b], self.env)
                        self.assigned += 1
                        return
            self.deferred.append((pys, vs, snippet, text, fails is not None))
            if all(v in self.env for v in vs):
                vals = [exact(p, self.env) for p in pys]
                if all(v == vals[0] for v in vals):
                    self.substituted += len(vals) - 1
                    self.deferred.pop()
                    return
        except Exception as e:  # noqa: BLE001
            fails.append("could not evaluate: %s (%s)" % (snippet, e))

    def _identity(self, pys, vs):
        rnd = random.Random(7)
        for _ in range(4):
            env = dict((v, Fraction(rnd.choice([2, 3, 5, 7, 11, 13]))) for v in vs)
            vals = [exact(p, env) for p in pys]
            if not all(v == vals[0] for v in vals):
                return False
        return True

    def finish(self, allow):
        """Retry algebra lines whose values were only given later in the lesson."""
        for pys, vs, snippet, text, _x in self.deferred:
            if text in self.allowed_texts:
                continue
            if all(v in self.env for v in vs):
                vals = [exact(p, self.env) for p in pys]
                if all(v == vals[0] for v in vals):
                    self.substituted += len(vals) - 1
                    continue
                self.fails.append("%s: does not hold with the lesson's values: %s :: %s" % (self.where, snippet, text))
            else:
                self.fails.append("%s: letters with no value and not an identity: %s :: %s" % (self.where, snippet, text))


def latex_to_plain(n):
    n = n.replace("{,}", "")
    for _ in range(3):
        n = re.sub(r"\\t?frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1) / (\2))", n)
    n = re.sub(r"\\text\{([^{}]*)\}", r" \1 ", n)
    n = re.sub(r"\^\{(\d+)\}", r"^\1", n)
    for a, b in (("\\times", " \u00d7 "), ("\\div", " \u00f7 "), ("\\left", ""), ("\\right", ""),
                 ("\\square", " \u25a1 "), ("\\Rightarrow", " so "), ("\\rightarrow", " to "),
                 ("\\quad", " "), ("\\,", " "), ("\\;", " ")):
        n = n.replace(a, b)
    return n


# ── per-file checks ──────────────────────────────────────────────────────────

def topic_meta_from_ts(slug):
    path = os.path.join(ROOT, "src", "data", "lessonTopics.ts")
    with open(path, encoding="utf-8") as f:
        ts = f.read()
    m = re.search(
        r"id: '" + re.escape(slug) + r"',\s*topic: '([^']*)',\s*emoji: '([^']*)',\s*color: '([^']*)',"
        r"\s*gradeRange: \[(\d+), (\d+)\],\s*description: '([^']*)'", ts)
    if not m:
        return None
    return {"topic": m.group(1), "emoji": m.group(2), "color": m.group(3),
            "gradeRange": [int(m.group(4)), int(m.group(5))], "description": m.group(6)}


def visual_keys():
    path = os.path.join(ROOT, "src", "data", "lessonVisuals.ts")
    with open(path, encoding="utf-8") as f:
        return set(re.findall(r"^\s{2}'?([\w-]+)'?: \{", f.read(), re.M))


def check_prose(text, where, fails):
    if not isinstance(text, str) or not text.strip():
        fails.append("%s: empty text" % where)
        return
    if re.search(r"[\\{}*$]", text):
        fails.append("%s: backslash, brace, star or dollar in plain text: %s" % (where, text))
    if FORBIDDEN.search(text):
        fails.append("%s: a word the app must not say: %s" % (where, text))
    if text != text.strip() or "  " in text:
        fails.append("%s: stray spaces: %r" % (where, text))


def check_topic(slug):
    prefix, modname, letters = TOPICS[slug]
    fails, warns, labels = [], [], []
    stats = {"quiz": 0, "eq": 0, "identity": 0, "subst": 0, "assign": 0, "facts": 0, "notation": 0}
    path = os.path.join(LESSON_DIR, slug + ".json")
    if not os.path.exists(path):
        return ["%s: file missing: %s" % (slug, path)], warns, labels, stats
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    mod = importlib.import_module(modname)
    expect = mod.EXPECT
    allow = getattr(mod, "ALLOW", {})
    used_allow = set()

    # header
    if data.get("id") != slug:
        fails.append("%s: id is %r" % (slug, data.get("id")))
    meta = topic_meta_from_ts(slug)
    if meta is None:
        fails.append("%s: not registered in src/data/lessonTopics.ts" % slug)
    else:
        for k in meta:
            if data.get(k) != meta[k]:
                fails.append("%s: header %s differs from lessonTopics.ts: %r vs %r" % (slug, k, data.get(k), meta[k]))
    check_prose(data.get("description", ""), slug + " description", fails)

    levels = data.get("levels", [])
    if [l.get("id") for l in levels] != [1, 2, 3, 4, 5]:
        fails.append("%s: level ids must be 1..5" % slug)
    vkeys = visual_keys()
    seen_ids = set()
    seen_questions = set()

    for n, lv in enumerate(levels, start=1):
        emoji, color, grad = LEVEL_STYLE[n - 1]
        if (lv.get("emoji"), lv.get("color"), lv.get("bgGradient")) != (emoji, color, grad):
            fails.append("%s L%d: level style differs from the other lessons" % (slug, n))
        check_prose(lv.get("label", ""), "%s L%d label" % (slug, n), fails)
        check_prose(lv.get("subtitle", ""), "%s L%d subtitle" % (slug, n), fails)
        lessons = lv.get("lessons", [])
        quiz = lv.get("quiz", [])
        if len(lessons) != 5 or len(quiz) != 8:
            fails.append("%s L%d: needs 5 lessons and 8 quiz items" % (slug, n))

        for i, les in enumerate(lessons, start=1):
            lid = les.get("id")
            if lid != "%s-l%d-les%d" % (prefix, n, i) or lid in seen_ids:
                fails.append("%s: bad or repeated lesson id %r" % (slug, lid))
            seen_ids.add(lid)
            if les.get("visual", "") not in ("",) and les.get("visual") not in vkeys:
                fails.append("%s: visual %r is not in lessonVisuals.ts" % (lid, les.get("visual")))
            sc = Scanner(letters, lid)
            # (field, text to scan, text as written, is plain prose) in reading order
            strings = [("title", les.get("title", ""), None, True),
                       ("intro", les.get("intro", ""), None, True)]
            expl = les.get("explanation", [])
            if not isinstance(expl, list) or len(expl) < 2:
                fails.append("%s: explanation should be a list of at least 2 lines" % lid)
                expl = []
            for k, e in enumerate(expl):
                strings.append(("explanation[%d]" % k, e, None, True))
            for k, st in enumerate(les.get("steps", []) or []):
                strings.append(("step[%d].text" % k, st.get("text", ""), None, True))
                note = st.get("notation", "")
                if not isinstance(note, str) or not note.strip():
                    fails.append("%s step[%d]: empty notation" % (lid, k))
                else:
                    plain = latex_to_plain(note)
                    if re.search(r"[\\{}]", plain):
                        fails.append("%s step[%d]: LaTeX the checker does not know: %s" % (lid, k, note))
                    else:
                        stats["notation"] += 1
                        strings.append(("step[%d].notation" % k, plain, note, False))
                if "tip" in st:
                    strings.append(("step[%d].tip" % k, st["tip"], None, True))
            strings.append(("rule", les.get("rule", ""), None, True))
            strings.append(("tip", les.get("tip", ""), None, True))
            for field, text, written, is_prose in strings:
                if is_prose:
                    check_prose(text, "%s %s" % (lid, field), fails)
                key = written if written is not None else text
                if key in allow:
                    used_allow.add(key)
                sc.scan(text, field, allow, key)
            sc.finish(allow)
            fails.extend(sc.fails)
            labels.extend(sc.labels)
            stats["eq"] += sc.ok
            stats["identity"] += sc.identities
            stats["subst"] += sc.substituted
            stats["assign"] += sc.assigned
            stats["facts"] += sc.facts

        for i, q in enumerate(quiz, start=1):
            qid = q.get("id")
            if qid != "%s-l%d-q%d" % (prefix, n, i) or qid in seen_ids:
                fails.append("%s: bad or repeated quiz id %r" % (slug, qid))
            seen_ids.add(qid)
            if q.get("difficulty") != DIFFICULTY[i - 1]:
                fails.append("%s: difficulty should be %s" % (qid, DIFFICULTY[i - 1]))
            question, answer, hint = q.get("question", ""), q.get("answer", ""), q.get("hint", "")
            story = q.get("story", "")
            if question in seen_questions:
                fails.append("%s: the same question appears twice" % qid)
            seen_questions.add(question)
            check_prose(question, qid + " question", fails)
            check_prose(hint, qid + " hint", fails)
            if "story" in q:
                check_prose(story, qid + " story", fails)
                if q.get("isWord") is not True:
                    fails.append("%s: story without isWord" % qid)
            if not isinstance(answer, str) or not re.match(r"^\d+(\.\d+)?$", answer):
                fails.append("%s: answer %r is not a plain number a child can type" % (qid, answer))
                continue
            if "." in answer and (answer.endswith("0") or answer.startswith(".")):
                fails.append("%s: decimal answer %r is not in its shortest form" % (qid, answer))

            exp = expect.get(qid)
            if exp is None:
                fails.append("%s: no expected computation in %s" % (qid, modname))
            else:
                expr, consts = (exp, "") if isinstance(exp, str) else exp
                try:
                    got = show(exact(expr))
                except Exception as e:  # noqa: BLE001
                    got = "could not evaluate (%s)" % e
                if got != answer:
                    fails.append("%s: keyed answer %s but %s = %s" % (qid, answer, expr, got))
                else:
                    stats["quiz"] += 1
                shown = set(NUM_RE.findall(strip_commas(story + " " + question).replace(":", " ")))
                shown |= set(str(int(float(x))) for x in list(shown) if float(x) == int(float(x)))
                extra = set(consts.split())
                for lit in NUM_RE.findall(expr):
                    if lit not in shown and lit not in extra:
                        fails.append("%s: the computation uses %s, which is not in the question: %s" % (qid, lit, expr))
                for c in extra:
                    if c not in NUM_RE.findall(expr):
                        fails.append("%s: constant %s is declared but not used" % (qid, c))
            if re.search(r"(?<![\d.])" + re.escape(answer) + r"(?![\d.])", strip_commas(hint)):
                warns.append("%s: the hint contains the answer %s: %s" % (qid, answer, hint))

            sc = Scanner(letters, qid)
            for field, text in (("story", story), ("question", question), ("hint", hint)):
                if text:
                    if text in allow:
                        used_allow.add(text)
                    sc.scan(text, field, allow)
            sc.finish(allow)
            fails.extend(sc.fails)
            labels.extend(sc.labels)
            stats["eq"] += sc.ok
            stats["identity"] += sc.identities
            stats["subst"] += sc.substituted
            stats["assign"] += sc.assigned
            stats["facts"] += sc.facts

    for qid in expect:
        if qid not in seen_ids:
            fails.append("%s: expected computation for an id that is not in the lesson" % qid)
    for text in allow:
        if text not in used_allow:
            fails.append("%s: ALLOW entry matches no sentence: %s" % (slug, text))
    return fails, warns, labels, stats


def main():
    slugs = sys.argv[1:] or list(TOPICS.keys())
    bad = 0
    for f, proof in sorted(FACTS.items()):
        if exact(proof) is not True:
            print("FAIL  unit fact is not true: %s (%s)" % (f, proof))
            bad += 1
    for slug in slugs:
        fails, warns, labels, st = check_topic(slug)
        print("== %s ==" % slug)
        print("   quiz answers recomputed: %d/40" % st["quiz"])
        print("   equalities recomputed: %d arithmetic, %d algebra identities, %d by substitution"
              % (st["eq"], st["identity"], st["subst"]))
        print("   values given to letters: %d; unit facts: %d; notation boxes read: %d"
              % (st["assign"], st["facts"], st["notation"]))
        for l in labels:
            print("   note  'name = number' not recomputed (read by hand): " + l)
        for w in warns:
            print("   WARN  " + w)
        for f in fails:
            print("   FAIL  " + f)
        bad += len(fails)
    print("")
    print("RESULT: %s" % ("ALL CHECKS PASSED" if bad == 0 else "%d FAILURE(S)" % bad))
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
