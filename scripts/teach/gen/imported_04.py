"""Lessons for data/bank-import/lessons/in-04.json (order of operations, one counting question).

    python -X utf8 scripts/teach/gen/imported_04.py

Writes data/teach/parts/imported-04.json. Lines that are one order-of-operations
expression are taught by the rule in imported_04_lib.bodmas, which computes every
number; the rest are written by hand in imported_04_hand.py.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

from imported_04_lib import bodmas  # noqa: E402
from imported_04_hand import LESSONS as HAND  # noqa: E402

P = "AIGEN_grade5_"
T = "IPMTB_grade5_ch07_"

# (id, the line, how the teacher opens, what the answer means)
LINES = [
    (P + "375b8984-54d9-4135-b0f0-ba86330bca04", "120 − (8 + 4) × 6 + 18 ÷ 3",
     "Aarav's teacher has written the samosa stall's profit as one long line. It has brackets, a times and a divide in it, so the order we work in matters.",
     "So the expression is worth 54."),
    (P + "375bd5f2-103e-42ed-b8a2-e5b2dd7dbdb7", "200 + 15 × 6 − 25 + 8 × 4",
     "Rohan starts with 200 rupees, earns 15 rupees from each of 6 players, spends 25, then earns 8 rupees from each of 4 more. Here is his line.",
     "Rohan finishes the day with 297 rupees."),
    (P + "470db5aa-8284-4ed5-9ddc-6aa1bd35aa3d", "(48 ÷ 6 + 3) × 4 − 18 ÷ 2",
     "Here is the scorer's formula for Kabir's team. Notice that the brackets hold two jobs, a divide and a plus.",
     "Kabir's team earns 35 bonus points."),
    (P + "47203ffd-4bce-4ce2-bd93-5e72c9b6b0b1", "60 − 4 × 7 + 3 × 5",
     "Priya has 60 packets. She gives away 4 bags of 7, then her brother brings 3 boxes of 5. The line says exactly that.",
     "Priya has 47 colour packets now."),
    (P + "587aa540-6468-4889-94e7-9eaeb4d22a26", "12 + 8 × (15 − 9) ÷ 4 − 3",
     "Arjun's coach has a formula for his performance points. There is a bracket tucked in the middle of it.",
     "Arjun gets 21 performance points."),
    (P + "633ee290-ad2f-4f7f-8ed7-bdf8c7e17ef7", "200 − 5 × 9 − 4 × 25 + 50 − 15",
     "Meera has a budget of 200 rupees. Out go 5 ribbons at 9 rupees and 4 boxes of sweets at 25 rupees, in comes 50 from Grandmother, and out goes 15 for paper.",
     "Meera has 90 rupees left."),
    (P + "655c1341-b66e-4f1a-bc46-09fb8103432b", "5 + 3 × (12 − 4) ÷ 2 − 1",
     "Here is the scorer's formula for the bonus points. One bracket, with a times, a divide, a plus and a minus around it.",
     "The expression is worth 16."),
    (P + "6b60e562-f08a-408b-a88c-fb58d25a0975", "5 × 12 − 3 × 8 − 6 + 2 × 9",
     "Riya's mother makes 5 batches of 12 samosas, sells 3 boxes of 8, gives away 6, then makes 2 more batches of 9. The line tells the whole day.",
     "She has 48 samosas at the end of the day."),
    (P + "70ac2e6a-0c92-4780-8370-b36c4cac37ce", "6 × 8 − 2 × 8 + 15",
     "Priya buys 6 boxes of diyas at 8 rupees each, returns 2 of those boxes, and buys candles for 15 rupees. The line says the same thing in numbers.",
     "Priya spends 47 rupees in all."),
    (P + "78d6ed4c-5aef-48ee-a8ce-e74d636c22a0", "60 − 48 ÷ (2 + 6) × 5 + 15",
     "This is the profit formula from the samosa stall. It has a bracket, with a divide just before it and a times just after it.",
     "The profit is 45 rupees."),
    (P + "7945cdef-e505-4b96-8158-35ce53d4b3a9", "50 − 6 × 3 + 4 × 5",
     "Meera starts with 50 diyas, gives 6 each to 3 neighbours, and then gets 4 times 5 more from her grandmother. Here is her line.",
     "Meera has 52 diyas now."),
    (P + "82f232bb-eec4-49fb-bffb-8a2a8ceeb543", "5 + 3 × (12 − 4) ÷ 2",
     "Meena's line for the laddoos has a bracket, a times, a divide and a plus. Let's take them in the proper order.",
     "Meena packs 17 laddoos."),
    (P + "87f340c6-ac43-47ab-aeb2-c54122f05d17", "5 × 12 + 8 − 20",
     "Riya pays for 5 packets at 12 rupees each and a chai for 8 rupees, then gets 20 rupees back from her brother. The line shows how much less money she has.",
     "Riya has 48 rupees less than when she left home."),
    (P + "9ce0b59d-2bb8-491b-bf77-57c93d366339", "48 + 5 × 12 + 15 − 3 × 2",
     "Rohan's team made 48 runs, then 5 batsmen made 12 each, the rest made 15, and 3 runs were taken off 2 times as a penalty. Here is the line.",
     "The team's total is 117 runs."),
    (P + "9f317157-0b60-4b26-8973-e320d7fc03f0", "150 − (6 + 2) × (15 − 3 × 4) + 5 × 2",
     "Priya's line for the samosas she sold has two pairs of brackets, and one of them has a times hiding inside it.",
     "Priya sold 136 samosas."),
    (P + "a9f006e7-6234-410d-b916-14c42f82a6b8", "48 ÷ (4 + 2) × 3 − 5 + 12",
     "Here is the coach's line for Ravi's runs. It opens with a divide, and a bracket comes straight after.",
     "The expression is worth 31."),
    (P + "bd9fc1f3-e26c-4f09-b3ce-f4b04a76568b", "50 + 6 × 8 − 10",
     "Kabir starts with 50 rupees, earns 6 rupees for each of 8 glasses, and pays 10 rupees for lemons. Here is his line.",
     "Kabir has 88 rupees now."),
    (P + "c3bd4edc-3a3b-42c6-9f20-4d592c3261a9", "30 + 12 ÷ 4 × 2 − 5",
     "Arjun's line has no brackets at all. But it does have a divide and a times sitting side by side in the middle.",
     "The correct result is 31."),
    (P + "c5ecf669-5f04-4d10-81f0-77af3c6678a5", "100 − 3 × 12 + 2 × 8",
     "The question itself says this line does not quite match Riya's shopping. So we leave the story alone and simply find what the line is worth.",
     "The line is worth 80."),
    (P + "c63da34f-565d-466d-8558-af09ebb10bba", "5 × 8 + 12 − 3",
     "Riya buys 5 packets at 8 rupees each and a bottle of chutney for 12 rupees, then gets 3 rupees off. Here is her bill as one line.",
     "Riya pays 49 rupees."),
    (P + "c9bc6cdd-74cf-4a20-96c2-2c64466c4fe8", "200 − 3 × 25 + 50 − 2 × 30",
     "Riya has 200 rupees. She buys 3 packets at 25 rupees each, gets 50 more from her mother, then buys 2 boxes at 30 rupees each. Here is the line.",
     "Riya has 115 rupees left."),
    (P + "c9c12930-1b79-4192-a7a9-b764929f4bc8", "(500 − 4 × 35 + 150) ÷ 5",
     "Arjun has 500 rupees, spends 4 lots of 35, and gets 150 from his uncle. The brackets hold all of that, because the whole amount is then shared among 5 people.",
     "Each person gets 102 rupees."),
    (P + "ccd223d3-1454-4ace-88be-a2da0a701940", "120 ÷ (4 + 2) × 3 − 8 + 5 × (10 − 7)",
     "Arjun's dad has set a puzzle for the Diwali lights. It has two pairs of brackets, one near the start and one at the very end.",
     "They need 67 lights."),
    (P + "cde4569b-9af5-4d4b-978b-ddc1a035f908", "5 × (12 − 4) + 36 ÷ (3 + 6) − 2 × 3",
     "Ravi's line for the cricket balls has two pairs of brackets, with a times in front of one and a divide in front of the other.",
     "Ravi needs 38 cricket balls."),
    (P + "d13a7b01-01a5-4a46-aba3-e1cb9c81a581", "50 + 8 × 12 − 3 × 15 + 10",
     "The cash box starts with 50 rupees. In come 8 cups of chai at 12 rupees, out go 3 packets of biscuits at 15 rupees, and in comes a tip of 10. Here is the line.",
     "The cash box holds 111 rupees."),
    (P + "d50ffcdb-8b78-47cf-abe1-d3370f97aa4c", "15 + 12 ÷ 3 × 2 − 5",
     "Here is the coach's line for Aarav's score. No brackets, but there is a divide and a times side by side.",
     "Aarav's total score is 18."),
    (P + "d69fa5f3-a643-4a83-b887-5043f633652b", "(3 × 12 − 6) ÷ 6 + 4 × 5",
     "The brackets work out the diyas for each rangoli: 3 boxes of 12, less 6, shared among 6. After the brackets come 4 packets of 5 sparklers.",
     "The expression is worth 25."),
    (P + "d9bb5286-5a2e-48de-a2cb-3853188571d0", "120 ÷ (4 + 2) × 3 + 50 − 8 × 5",
     "Here is the chai stall's earnings line, in rupees. It starts with a divide and a bracket, and ends with a times.",
     "She earned 70 rupees."),
    (P + "da4b169b-95b0-44a8-8340-c6a2fd3a8efb", "200 − 3 × (15 + 5) + 48 ÷ 6 × 2",
     "Arjun's profit line, in rupees, has a bracket near the front, and a divide and a times side by side at the end.",
     "Arjun's profit is 156 rupees."),
    (P + "da97fe1f-3c2b-4356-852f-a003539f0eeb", "120 − 4 × (3 + 7) + 60 ÷ 5",
     "Ananya's cost line, in rupees, has one bracket, a times, a divide, a minus and a plus.",
     "Ananya needs to spend 92 rupees."),
    (P + "dd8a4ba1-cb76-4fe7-b226-feb11a02a4d4", "50 + 4 × 8 − 6",
     "Priya's mother starts with 50 millilitres of water, adds 4 cups of milk of 8 millilitres each, and loses 6 millilitres. The line says just that.",
     "She has 76 millilitres now."),
    (P + "e3a14a5a-d6db-4677-8315-20fee3f39bef", "15 + 4 × 6 + 2",
     "Arjun made 15 runs in the first over, then 6 runs in each of the next 4 overs, and got 2 bonus runs. Here is his line.",
     "Arjun's total is 41 runs."),
    (P + "eba70c91-7be5-4aaf-8677-d4c0e34ffc00", "50 + 4 × 6 − 3 × 2",
     "The team starts with 50 runs, hits 4 sixes worth 6 runs each, and loses 2 runs for each of 3 wickets. Here is the line.",
     "The team's final score is 68."),
    (P + "ed1dfb29-7d00-47c9-82a6-4eb82d03cf77", "60 − 3 × 8 − 15",
     "Kabir starts with 60 rupees. He buys 3 boxes of diyas at 8 rupees each and a packet of sparklers for 15 rupees. Here is the line.",
     "Kabir has 21 rupees left."),
    (P + "f2e7d837-306a-4d34-b9fe-eac659a7ea0c", "5 × 12 + 8 − 3",
     "Ravi buys 5 packets at 12 rupees each and a bottle of chutney for 8 rupees, then gets 3 rupees off. Here is his bill as one line.",
     "Ravi pays 65 rupees."),
    (P + "f71c32d3-dbdc-4b1d-8bad-0746b5478f62", "120 ÷ (4 + 2) × 3 − 5 × (8 − 6) + 15",
     "Aarav's line for the chai stall has two pairs of brackets, and a divide, two times signs, a minus and a plus.",
     "The expression is worth 65."),
    (P + "fa924757-fe85-405f-9147-036f9e33c886", "120 − 48 ÷ (2 + 6) × 3 + 15",
     "Here is the earnings line from Ravi's family chai stall. Watch the middle: a divide, then a bracket, then a times.",
     "The expression is worth 117."),
    (P + "fda86098-5028-4f4a-8061-a86ca2071505", "30 − 2 × 5 + 3 × 4",
     "Meera has 30 packets. She gives away 2 groups of 5, then buys 3 times 4 more. The line says the same in numbers.",
     "Meera has 32 packets now."),
    (T + "q006", "7 × 2 − 7 ÷ 7 + 3 × 1",
     "No brackets in this one. But look how many times and divide signs are mixed in with the plus and the minus.",
     "The answer is 16."),
    (T + "q016", "16 × 5 + 5 − 2 × 10 ÷ 5 + 5 × 2 − 1",
     "A long line with no brackets. Don't let the length worry you: we just take the jobs in the right order.",
     "The answer is 90."),
    (T + "q025", "35 ÷ 7 + 25 ÷ 5 + 15 ÷ 5",
     "Three divides, joined by plus signs. Each divide is a little job of its own.",
     "The answer is 13."),
]

# Left out on purpose (see the report): the story and the line disagree.
LEFT_OUT = {
    P + "6603373f-f901-4feb-bb1d-1e81a8d2f084",
    P + "e9fcd7d2-1969-496a-bcf8-2f72ec4f3166",
}


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "lessons", "in-04.json"), encoding="utf-8") as f:
        batch = {q["id"]: q for q in json.load(f)}

    part = {}
    for qid, expr, intro, ending in LINES:
        q = batch[qid]
        keyed = q["options"][q["answer"]]
        answer = int(re.sub(r"[^\d]", "", keyed))
        part[qid] = bodmas(qid, expr, intro, ending, answer)
    for qid, lesson in HAND.items():
        assert qid in batch and qid not in part, qid
        part[qid] = lesson

    missing = [qid for qid in batch if qid not in part and qid not in LEFT_OUT]
    long = [(qid, i) for qid, s in part.items() for i, b in enumerate(s["beats"]) if len(b["say"]) > 240]
    out = os.path.join(ROOT, "data", "teach", "parts", "imported-04.json")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons; left out %d; no lesson yet for %d" % (len(part), len(LEFT_OUT), len(missing)))
    for qid in missing:
        print("  missing", qid)
    for qid, i in long:
        print("  too long", qid, i)


if __name__ == "__main__":
    main()
