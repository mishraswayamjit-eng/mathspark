"""The question bank: the one module that reads and writes data/bank/.

    import bank
    questions = bank.load_bank()          # every question, each with its "node"
    bank.save_bank(questions)             # rewrite data/bank/** from the list

Layout (see scripts/bank/README.md):
    data/bank/_meta.json                  the bank's metadata
    data/bank/grade5/gr5_fractions.json   one file per topic-tree node (src/data/topicTree.ts)
    data/bank/grade5/_unsorted.json       questions of that grade that belong to no node
    src/data/bank/seedIds.json            every id in the bank, sorted

Each file is a JSON array with one question per line, sorted by id. A question is
    {"id", "node", "topicId", "subTopic", "difficulty", "questionText", "questionLatex",
     "options", "correctAnswer", "hints", "stepByStep", "misconceptions", "source", ...}
`node` is the topic-tree node id (null in _unsorted.json); `topicId` is the database pool.

No other script opens bank files directly. Plain Python 3 standard library only.
"""
import collections
import glob
import io
import json
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
BANK = os.path.join(ROOT, "data", "bank")
META = os.path.join(BANK, "_meta.json")
SEED_IDS = os.path.join(ROOT, "src", "data", "bank", "seedIds.json")
TREE = os.path.join(ROOT, "src", "data", "topicTree.ts")

UNSORTED = "_unsorted"
GRADES = (2, 3, 4, 5, 6, 7, 8, 9)
DIFFICULTIES = ("Easy", "Medium", "Hard")
OPTION_IDS = ("A", "B", "C", "D")
# Every question has these, in this order, after "id" and "node". A row may carry more.
FIELDS = ("topicId", "subTopic", "difficulty", "questionText", "questionLatex", "options",
          "correctAnswer", "hints", "stepByStep", "misconceptions", "source")
STRING_FIELDS = ("id", "topicId", "subTopic", "difficulty", "questionText", "questionLatex", "correctAnswer", "source")

_NODE_RE = re.compile(
    r"\{\s*id:\s*'([^']+)',\s*name:\s*'([^']+)'.*?grade:\s*(\d+),\s*examWeight:\s*([\d.]+),"
    r"\s*dbTopicId:\s*'([^']+)'(?:,\s*subTopicKey:\s*'([^']+)')?")
_GRADE_POOL = re.compile(r"^grade(\d+)$")
_CHAPTER_POOL = re.compile(r"^(ch\d\d(-\d\d)?|dh)$")
_WORD_CHAR = re.compile(r"[a-z0-9]")
_tree_cache = None


# ── The topic tree ───────────────────────────────────────────────────────────

def tree_nodes(grade=None):
    """The nodes of src/data/topicTree.ts, in file order (optionally one grade's).

    Each is {"id", "name", "grade", "w" (examWeight), "db" (dbTopicId), "key" (subTopicKey or None)}.
    """
    global _tree_cache
    if _tree_cache is None:
        with io.open(TREE, encoding="utf-8") as f:
            text = f.read()
        _tree_cache = [
            {"id": m.group(1), "name": m.group(2), "grade": int(m.group(3)), "w": float(m.group(4)),
             "db": m.group(5), "key": m.group(6)}
            for m in _NODE_RE.finditer(text)]
    return [dict(n) for n in _tree_cache if grade is None or n["grade"] == grade]


def node_by_id(nodes=None):
    return dict((n["id"], n) for n in (tree_nodes() if nodes is None else nodes))


def matches(sub_topic, key):
    """Same rule as matchesSubTopicKey (src/lib/sharedUtils.ts): the key must start a word
    in the label. Case-insensitive. An empty key matches everything."""
    if not key:
        return True
    hay, needle = (sub_topic or "").lower(), key.lower()
    start = 0
    while True:
        i = hay.find(needle, start)
        if i == -1:
            return False
        if i == 0 or not _WORD_CHAR.match(hay[i - 1]):
            return True
        start = i + 1


def grade_of(topic_id):
    """The grade a database pool belongs to: gradeN -> N; the Grade 4 chapter pools -> 4."""
    m = _GRADE_POOL.match(topic_id or "")
    if m:
        return int(m.group(1))
    if _CHAPTER_POOL.match(topic_id or ""):
        return 4
    return None


def _last_word_start(label, key):
    """Where the key last starts a word in the label, or -1."""
    hay, needle = (label or "").lower(), key.lower()
    best, start = -1, 0
    while True:
        i = hay.find(needle, start)
        if i == -1:
            return best
        if i == 0 or not _WORD_CHAR.match(hay[i - 1]):
            best = i
        start = i + 1


_GRADE_PREFIX = re.compile(r"^\s*Grade\s+\d+\s*[—–-]\s*", re.I)
_HEAD_END = re.compile(r"\s+[—–-]\s+|[:(]|\s+(?:with|of|on|in|for|using)\s+", re.I)
# Keys that name an operation or a general word rather than a subject: "Fraction addition"
# is fractions work, and the Addition topic is about whole numbers.
WEAK_KEYS = ("addition", "multiplication", "number")


def _head_phrase(label):
    """What the label is about: the part before a dash, a colon, a bracket or a preposition,
    without the 'Grade N —' opening. 'Grade 5 — BODMAS with fractions' -> 'BODMAS'."""
    rest = _GRADE_PREFIX.sub("", label or "")
    return _HEAD_END.split(rest, 1)[0]


def candidate_nodes(question, nodes=None):
    """Every node whose key reaches this question's label (shared pools), or the one
    node that owns a chapter pool. Nodes without a key on a shared pool reach nothing."""
    nodes = tree_nodes() if nodes is None else nodes
    pool = question.get("topicId")
    mine = [n for n in nodes if n["db"] == pool]
    if _GRADE_POOL.match(pool or ""):
        return [n for n in mine if n["key"] and matches(question.get("subTopic"), n["key"])]
    return [n for n in mine if not n["key"]]


def assign_node(question, nodes=None):
    """The topic-tree node id this question belongs to, or None.

    Chapter pools (ch06, dh, ...): the node whose dbTopicId is the pool.
    Shared pools (grade5, ...): the node whose subTopicKey starts a word in the label.
    When several keys do, the key that names what the label is about wins, in three steps:
      1. keys found in the head phrase (before a dash, colon, bracket or "with/of/on/in/
         for/using") beat keys found only after it: "BODMAS with fractions" is BODMAS,
         "Fractions of money" is fractions, "Triangle — ratio" is triangles;
      2. a subject key beats an operation key (WEAK_KEYS): "Fraction addition" is fractions;
      3. of what is left, the key furthest to the right wins, because English puts the
         head noun last: "Fraction equations" is equations, "Place value algebra" is algebra.
    A tie goes to the first node in the tree.
    """
    hits = candidate_nodes(question, nodes)
    if not hits:
        return None
    if len(hits) == 1:
        return hits[0]["id"]
    label = question.get("subTopic")
    head = _head_phrase(label)
    in_head = [n for n in hits if matches(head, n["key"])]
    if in_head:
        hits, label = in_head, head
    strong = [n for n in hits if n["key"].lower() not in WEAK_KEYS]
    if strong:
        hits = strong
    best = max(_last_word_start(label, n["key"]) for n in hits)
    return [n for n in hits if _last_word_start(label, n["key"]) == best][0]["id"]


# ── Reading ──────────────────────────────────────────────────────────────────

def grade_dir(grade):
    return os.path.join(BANK, "grade%d" % grade)


def file_for(question):
    """The bank file a question belongs in."""
    grade = grade_of(question.get("topicId"))
    if grade is None:
        raise ValueError("%s: topicId %r belongs to no grade" % (question.get("id"), question.get("topicId")))
    return os.path.join(grade_dir(grade), "%s.json" % (question.get("node") or UNSORTED))


def bank_files(grade=None):
    """Every bank file, in a fixed order: grade, then file name."""
    out = []
    for g in GRADES if grade is None else (grade,):
        out.extend(sorted(glob.glob(os.path.join(grade_dir(g), "*.json"))))
    return out


def read_file(path):
    with io.open(path, encoding="utf-8", newline="") as f:
        return f.read()


def load_bank(grade=None):
    """Every question in the bank (or one grade's), each a dict with its `node`.
    Order: grade, file name, id."""
    if not os.path.isdir(BANK):
        raise SystemExit("The bank is missing: %s. Run: python -X utf8 scripts/bank/split.py" % os.path.relpath(BANK, ROOT))
    out = []
    for path in bank_files(grade):
        out.extend(json.loads(read_file(path)))
    return out


def by_id(questions):
    return dict((q["id"], q) for q in questions)


def load_by_id(grade=None, topic_id=None):
    """id -> question, for a grade and/or a database pool."""
    if grade is None and topic_id is not None:
        grade = grade_of(topic_id)
    return dict((q["id"], q) for q in load_bank(grade) if topic_id is None or q.get("topicId") == topic_id)


def load_pool(topic_id):
    """The questions of one database pool ('grade5', 'ch06', ...), as a list."""
    return [q for q in load_bank(grade_of(topic_id)) if q.get("topicId") == topic_id]


def load_meta():
    with io.open(META, encoding="utf-8") as f:
        return json.load(f)


def load_seed_ids():
    with io.open(SEED_IDS, encoding="utf-8") as f:
        return json.load(f)


# ── Checking rows ────────────────────────────────────────────────────────────

def row_problems(questions, nodes=None):
    """What is wrong with these questions, as a list of lines (empty = nothing).
    Checks the rows themselves; scripts/bank/check.py also checks the files."""
    known = node_by_id(nodes)
    problems = []
    seen = collections.Counter(q.get("id") if isinstance(q, dict) else None for q in questions)
    for qid, n in seen.items():
        if n > 1:
            problems.append("%s: id used %d times" % (qid, n))
    for q in questions:
        if not isinstance(q, dict):
            problems.append("a row is not an object: %r" % (q,))
            continue
        qid = q.get("id")
        if not isinstance(qid, str) or not qid:
            problems.append("a row has no id: %s" % json.dumps(q, ensure_ascii=False)[:80])
            continue
        if "node" not in q:
            problems.append("%s: no node field (use null for unsorted)" % qid)
        for k in FIELDS:
            if k not in q:
                problems.append("%s: %s is missing" % (qid, k))
        for k in STRING_FIELDS:
            if k in q and not isinstance(q[k], str):
                problems.append("%s: %s is not text" % (qid, k))
        for k in ("topicId", "questionText", "source"):
            if isinstance(q.get(k), str) and not q[k].strip():
                problems.append("%s: %s is empty" % (qid, k))
        if "difficulty" in q and q["difficulty"] not in DIFFICULTIES:
            problems.append("%s: difficulty %r is not Easy, Medium or Hard" % (qid, q["difficulty"]))
        options = q.get("options")
        if "options" in q:
            if not isinstance(options, list) or len(options) != 4:
                problems.append("%s: options is not a list of four" % qid)
            elif not all(isinstance(o, dict) and isinstance(o.get("id"), str) and isinstance(o.get("text"), str) for o in options):
                problems.append("%s: every option needs a text id and a text" % qid)
            elif tuple(o["id"] for o in options) != OPTION_IDS:
                problems.append("%s: option ids are %s, not A B C D" % (qid, " ".join(o["id"] for o in options)))
        if "correctAnswer" in q and q["correctAnswer"] not in OPTION_IDS:
            problems.append("%s: correctAnswer %r is not A, B, C or D" % (qid, q["correctAnswer"]))
        if "hints" in q and not (isinstance(q["hints"], list) and all(isinstance(h, str) for h in q["hints"])):
            problems.append("%s: hints is not a list of text" % qid)
        if "stepByStep" in q and not (isinstance(q["stepByStep"], list) and all(isinstance(s, dict) for s in q["stepByStep"])):
            problems.append("%s: stepByStep is not a list of steps" % qid)
        if "misconceptions" in q and not isinstance(q["misconceptions"], dict):
            problems.append("%s: misconceptions is not an object" % qid)
        grade = grade_of(q.get("topicId")) if isinstance(q.get("topicId"), str) else None
        if isinstance(q.get("topicId"), str) and grade is None:
            problems.append("%s: topicId %r belongs to no grade" % (qid, q["topicId"]))
        node = q.get("node")
        if node is not None:
            n = known.get(node) if isinstance(node, str) else None
            if n is None:
                problems.append("%s: node %r is not in src/data/topicTree.ts" % (qid, node))
            elif n["grade"] != grade:
                problems.append("%s: node %s is Grade %d but topicId %s is Grade %s" % (qid, node, n["grade"], q.get("topicId"), grade))
            elif n["db"] != q.get("topicId"):
                problems.append("%s: node %s holds pool %s, not %s" % (qid, node, n["db"], q.get("topicId")))
    return problems


# ── Writing ──────────────────────────────────────────────────────────────────

def ordered(question):
    """The row with its keys in bank order: id, node, then the rest as they were."""
    out = {"id": question["id"], "node": question.get("node")}
    for k, v in question.items():
        if k not in ("id", "node"):
            out[k] = v
    return out


def dump_row(question):
    return json.dumps(ordered(question), ensure_ascii=False, separators=(",", ":"))


def file_text(questions):
    """A bank file's exact text: one question per line, sorted by id."""
    rows = sorted(questions, key=lambda q: q["id"])
    if not rows:
        return "[\n]\n"
    return "[\n" + ",\n".join(dump_row(q) for q in rows) + "\n]\n"


def _write_if_changed(path, text):
    if os.path.exists(path) and read_file(path) == text:
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    return True


def _is_bank_file(path):
    """True for a file this module wrote: a JSON array of rows that each carry `node`."""
    try:
        rows = json.loads(read_file(path))
    except (ValueError, OSError):
        return False
    return isinstance(rows, list) and all(isinstance(r, dict) and "id" in r and "node" in r for r in rows)


def seed_ids_text(questions):
    return json.dumps(sorted(q["id"] for q in questions), ensure_ascii=True, separators=(",", ":")) + "\n"


def meta_text(meta):
    return json.dumps(meta, ensure_ascii=False, indent=2) + "\n"


def planned_files(questions):
    """path -> text for every bank file: one per tree node and one _unsorted per grade,
    whether or not it holds a question, so the layout does not depend on the data."""
    groups = collections.defaultdict(list)
    for g in GRADES:
        groups[os.path.join(grade_dir(g), UNSORTED + ".json")]
        for n in tree_nodes(g):
            groups[os.path.join(grade_dir(g), n["id"] + ".json")]
    for q in questions:
        groups[file_for(q)].append(q)
    return dict((path, file_text(rows)) for path, rows in groups.items())


def save_bank(questions, meta=None):
    """Rewrite data/bank/** (and the id list) from the list of questions.

    Refuses to write if a row is not valid (row_problems). Files whose text would not
    change are left untouched. A bank file left over from a node that is no longer in
    the tree is removed, but only if it is a bank file. Returns the paths written or removed.
    """
    problems = row_problems(questions)
    if problems:
        raise SystemExit("%d PROBLEMS in the bank, nothing written\n  %s" % (len(problems), "\n  ".join(problems[:80])))
    plan = planned_files(questions)
    changed = [path for path in sorted(plan) if _write_if_changed(path, plan[path])]
    for path in bank_files():
        if path not in plan and _is_bank_file(path):
            os.remove(path)
            changed.append(path)
    if meta is None:
        meta = load_meta() if os.path.exists(META) else {}
    meta = dict(meta)
    meta["totalQuestions"] = len(questions)
    if _write_if_changed(META, meta_text(meta)):
        changed.append(META)
    if _write_if_changed(SEED_IDS, seed_ids_text(questions)):
        changed.append(SEED_IDS)
    return changed
