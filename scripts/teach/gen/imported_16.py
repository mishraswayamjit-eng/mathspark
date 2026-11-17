"""Lessons for data/bank-import/lessons/in-16.json (profit and loss stories, number patterns).

    python -X utf8 scripts/teach/gen/imported_16.py

Writes data/teach/parts/imported-16.json. Patterns that grow by the same amount are
taught by the rules in imported_16_lib (every number computed); the profit stories
and the one-off patterns are written by hand in imported_16_profit.py and
imported_16_seq.py.
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

from imported_16_lib import ANSC, ANSL, B, CHOOSE, CIRC, W, ap_list_sum, ap_sum, ap_term  # noqa: E402

P = "AIGEN_grade5_"

# ── The term in a far-off place: (id, intro, given, terms shown, n, place, each, ending) ──
TERMS = [
    (P + "09f86469-4a41-4a73-b3f3-4ecb779627dd",
     "Priya's rangoli has 5 dots in row 1, 9 dots in row 2, 13 dots in row 3, and so on. How many dots go in row 8?",
     "Rows: 5, 9, 13, …   Row 8 = ?", [5, 9, 13], 8, "row",
     "every row has 4 more dots than the row before", "So row 8 has 33 dots."),
    (P + "1ab2e80a-de78-4570-9c55-94e5c4e582d1",
     "Ravi puts 7 rupees in his piggy bank on day 1, 12 rupees on day 2 and 17 rupees on day 3, and keeps to the same pattern. How much does he put in on day 8?",
     "Days: 7, 12, 17, …   Day 8 = ?", [7, 12, 17], 8, "day",
     "each day he puts in 5 rupees more than the day before", "So on day 8 Ravi puts in 42 rupees."),
    (P + "54059d0e-e01d-4f8f-a71d-9f0edf64b65b",
     "Riya places 5 dots in the first row of her rangoli, 9 in the second and 13 in the third, adding the same number of extra dots each time. How many will she place in row 8?",
     "Rows: 5, 9, 13, …   Row 8 = ?", [5, 9, 13], 8, "row",
     "each new row gets 4 more dots than the last one", "So Riya places 33 dots in row 8."),
    (P + "676c13e0-9b3e-45bb-87f3-9e4f8c5cca9f",
     "Priya places 5 diyas in the first row, 9 in the second and 13 in the third, adding the same number of extra diyas each time. She makes 7 rows. How many diyas go in row 7?",
     "Rows: 5, 9, 13, …   Row 7 = ?", [5, 9, 13], 7, "row",
     "every row has 4 more diyas than the row before", "So row 7 has 29 diyas."),
    (P + "dce37ab5-d7d4-47cb-b9b8-46548d866784",
     "Priya uses 5 stones in row 1, 9 stones in row 2 and 13 stones in row 3, with the same number of extra stones each time. How many stones does she need for row 8?",
     "Rows: 5, 9, 13, …   Row 8 = ?", [5, 9, 13], 8, "row",
     "every row needs 4 more stones than the row before", "So Priya needs 33 stones for row 8."),
    (P + "fa67bc6b-3a6d-4eef-b478-ded5e4569af1",
     "Arjun puts 3 rupees in his piggy bank on Monday, 7 on Tuesday, 11 on Wednesday and 15 on Thursday. If the pattern carries on, how much goes in on Sunday, which is day 7?",
     "3, 7, 11, 15, …   Day 7 (Sunday) = ?", [3, 7, 11, 15], 7, "day",
     "each day he puts in 4 rupees more than the day before", "So on Sunday, day 7, Arjun puts in 27 rupees."),
]

# ── A short total: (id, intro, given, a, d, n, place, places, each, ending, shown, extras) ──
SHORT = [
    (P + "0215544c-a5ee-475a-9501-ee690589e4fb",
     "Ravi puts 7 rupees in his piggy bank on Monday, 12 on Tuesday and 17 on Wednesday, adding the same extra amount each day. How much has he saved in total by the end of Saturday, 6 days in all?",
     "7, 12, 17, …   Total for 6 days = ?", 7, 5, 6, "day", "days",
     "each day he puts in 5 rupees more than the day before", "Ravi has saved 117 rupees by the end of Saturday.", 3, {}),
    (P + "2936a290-17d6-48fa-8a00-043f0cb3c530",
     "Ananya places 3 diyas in row 1, 7 in row 2, 11 in row 3, and so on. How many diyas does she need in total for the first 6 rows?",
     "3, 7, 11, …   Total for 6 rows = ?", 3, 4, 6, "row", "rows",
     "each row has 4 more diyas than the row before", "Ananya needs 78 diyas for the first 6 rows.", 3, {}),
    (P + "b3225de1-9fdb-4b8b-b854-fbd541626efb",
     "Priya places 5 diyas in the first row, 8 in the second and 11 in the third, each row 3 more than the one before. How many diyas does she need for the first 6 rows?",
     "5, 8, 11, …   Total for 6 rows = ?", 5, 3, 6, "row", "rows",
     "each row has 3 more diyas than the row before", "Priya needs 75 diyas for the first 6 rows.", 3, {}),
    (P + "cb7d8549-92bd-4854-9123-f86ccb6ef4b3",
     "Ravi sells 6 cups of chai in over 1, 10 cups in over 2, 14 cups in over 3, and the pattern continues. How many cups does he sell in total in the first 5 overs?",
     "6, 10, 14, …   Total for 5 overs = ?", 6, 4, 5, "over", "overs",
     "each over he sells 4 more cups than the over before", "Ravi sells 70 cups in the first 5 overs.", 3, {}),
    (P + "e95d1a1c-5324-4ca5-bb30-55b43754b228",
     "Priya's rows of diyas go 5, 9, 13, each row 4 more than the last, for 15 rows. Then she takes all the diyas from the first 5 rows and puts them in one straight line. How many diyas are in that line?",
     "5, 9, 13, … (15 rows)   First 5 rows = ?", 5, 4, 5, "row", "rows",
     "each row has 4 more diyas than the row before", "So the straight line has 65 diyas.", 3,
     {"aside": B("She builds 15 rows, but only the first 5 are moved into the line. So the 15 is extra information, and we can leave it alone.",
                 CIRC("q", "First 5 rows"))}),
    (P + "210416ae-866d-47a3-a169-fbd7a72b1ef5",
     "Arjun's team scores 120 runs in match 1, and in each match after that they score 15 more runs than the match before. How many runs do they score altogether in 7 matches?",
     "Match 1: 120.   +15 each match.   Total for 7 = ?", 120, 15, 7, "match", "matches",
     "15 more runs in every match", "Arjun's team scores 1155 runs across the 7 matches.", 1, {}),
    (P + "c80525ab-9c57-4ba0-8937-5993ea75befe",
     "Ravi scores 15 runs in his first innings, 21 in his second, 27 in his third, and so on, going up by the same amount each time. How many runs does he score altogether in 7 innings?",
     "15, 21, 27, …   Total for 7 innings = ?", 15, 6, 7, "innings", "innings",
     "each innings he scores 6 more runs than the innings before", "Ravi scores 231 runs across the 7 innings.", 3, {}),
    (P + "8d0b5363-745a-41f0-a7ba-0665631dedcc",
     "Ravi scores 12 runs in match 1, and in each match after that he scores 6 more than the match before. After 7 matches the coach adds a bonus of 10 runs to his total. What is his final total?",
     "Match 1: 12.   +6 each match.   7 matches, bonus 10", 12, 6, 7, "match", "matches",
     "6 more runs in every match", "So the 7 matches give 210 runs.", 1,
     {"tail": [
         B("Now the bonus. The coach adds 10 runs to Ravi's total, and 210 plus 10 is 220. His final total is 220 runs.",
           *ANSC("fin", "210 + 10 = 220", 220)),
         B("Careful: 210 is one of the choices. It is the total before the bonus, so read the question right to its last line."),
     ],
      "summary": "So list every score, pair them up to add, and then remember anything extra the story mentions, like a bonus."}),
]

# ── A long total: (id, intro, given, a, d, n, place, places, each, ending, shown, extras) ──
LONG = [
    (P + "10a6094c-c43e-4500-8b47-7efa676353df",
     "Arjun scores 14 runs in match 1, 21 in match 2, 28 in match 3, and carries on in the same pattern. How many runs does he score altogether in 8 matches?",
     "14, 21, 28, …   Total for 8 matches = ?", 14, 7, 8, "match", "matches",
     "each match he scores 7 more runs than the match before", "Arjun scores 308 runs across the 8 matches.", 3, {}),
    (P + "17ee5d48-e964-4848-b9a9-d07e7dd6ee49",
     "Ravi's team scores 45 runs in week 1, and every week after that they score 12 more runs than the week before. How many runs do they score altogether in 8 weeks?",
     "Week 1: 45.   +12 each week.   Total for 8 weeks = ?", 45, 12, 8, "week", "weeks",
     "12 more runs every week", "The team scores 696 runs across the 8 weeks.", 1, {}),
    (P + "32d9f65a-f751-4094-acba-c394181debf4",
     "A chai stall sells 14 cups in hour 1, 21 cups in hour 2, 28 cups in hour 3, and so on in the same pattern. It stays open for 8 hours. How many cups is that in all?",
     "14, 21, 28, …   Total for 8 hours = ?", 14, 7, 8, "hour", "hours",
     "each hour he sells 7 more cups than the hour before", "He sells 308 cups of chai in the day.", 3, {}),
    (P + "33c9445d-35d6-4a05-aa52-71f500156066",
     "Ravi puts 7 rupees in his piggy bank on day 1, 12 on day 2 and 17 on day 3, adding the same extra amount each day. How much has he saved in total after 8 days?",
     "7, 12, 17, …   Total for 8 days = ?", 7, 5, 8, "day", "days",
     "each day he puts in 5 rupees more than the day before", "Ravi has saved 196 rupees after 8 days.", 3, {}),
    (P + "3e2ffe5d-60d2-471a-8463-81db406f8cfb",
     "Priya lays diyas in rows: 5 in row 1, 9 in row 2, 13 in row 3, and so on. She makes 8 rows. How many diyas does she use altogether?",
     "5, 9, 13, …   Total for 8 rows = ?", 5, 4, 8, "row", "rows",
     "each row has 4 more diyas than the row before", "Priya uses 152 diyas altogether.", 3, {}),
    (P + "668e115a-f041-4553-9337-08910c395980",
     "Priya's rows of diyas go 5, then 9, then 13, each row 4 more than the one before. With 8 rows in total, how many diyas does she use?",
     "5, 9, 13, …   Total for 8 rows = ?", 5, 4, 8, "row", "rows",
     "every row has 4 more diyas than the one before it", "So the 8 rows use 152 diyas.", 3, {}),
    (P + "84f898e4-3b49-472b-98e3-07f3d561f6cf",
     "Ananya sells 14 samosas on day 1, and each day after that she sells 6 more than the day before. She runs her stall for 8 days. How many samosas does she sell in all?",
     "Day 1: 14.   +6 each day.   Total for 8 days = ?", 14, 6, 8, "day", "days",
     "6 more samosas every day", "Ananya sells 280 samosas across the 8 days.", 1, {}),
    (P + "9aaa69ce-883c-41e6-a34d-2d9552a0242f",
     "Ravi lays diyas in rows: 5 in row 1, 8 in row 2, 11 in row 3, each row 3 more than the one before. He lays exactly 12 rows. How many diyas does he use in total?",
     "5, 8, 11, …   Total for 12 rows = ?", 5, 3, 12, "row", "rows",
     "each row has 3 more diyas than the row before", "Ravi uses 258 diyas in total.", 3, {}),
    (P + "a58b48cf-6b71-4d3b-904e-a16f27fc528c",
     "Priya's rangoli has 5 dots in row 1, 8 in row 2 and 11 in row 3, growing by the same amount each time, up to row 15. How many dots does she use across all 15 rows?",
     "5, 8, 11, …   Total for 15 rows = ?", 5, 3, 15, "row", "rows",
     "each row has 3 more dots than the row before", "Priya uses 390 dots across all 15 rows.", 3, {}),
    (P + "ae902ba4-e7e2-41d6-a812-67f448cfe685",
     "Priya's rangoli has 5 dots in row 1, 9 in row 2 and 13 in row 3, each row 4 more than the one before. It has 12 rows. How many dots does she use altogether?",
     "5, 9, 13, …   Total for 12 rows = ?", 5, 4, 12, "row", "rows",
     "each row has 4 more dots than the row before", "Priya uses 324 dots altogether.", 3, {}),
    (P + "bdbed473-8d4b-4c8c-b95d-ebd04d868784",
     "Priya lays coloured stones in rings: 5 in ring 1, 8 in ring 2, 11 in ring 3, each ring 3 more than the one before, up to ring 12. How many stones is that in total?",
     "5, 8, 11, …   Total for 12 rings = ?", 5, 3, 12, "ring", "rings",
     "each ring has 3 more stones than the ring before", "Priya uses 258 stones across all 12 rings.", 3, {}),
    (P + "cf8117ab-cb21-4886-8760-a41c3e92bc45",
     "Priya's rangoli has rings of stones: 5 in the first ring, 8 in the second, 11 in the third, each ring 3 more than the last. She completes 12 rings. How many stones does she use altogether?",
     "5, 8, 11, …   Total for 12 rings = ?", 5, 3, 12, "ring", "rings",
     "every ring has 3 more stones than the one inside it", "So the 12 rings use 258 stones.", 3, {}),
    (P + "f42fa286-32cb-4c1b-ad00-e3084e2ce698",
     "Rohan makes 6 cups of chai in hour 1, 11 in hour 2 and 16 in hour 3, going up by the same amount each hour. The fair lasts 8 hours. How many cups does he make in all?",
     "6, 11, 16, …   Total for 8 hours = ?", 6, 5, 8, "hour", "hours",
     "each hour he makes 5 more cups than the hour before", "Rohan makes 188 cups of chai during the fair.", 3, {}),
    (P + "f8c6d539-e27a-4cbe-98dc-2a3376aaaee5",
     "Meera threads 4 flowers in minute 1, 7 in minute 2, 10 in minute 3, and so on. How many flowers has she threaded in total by the end of minute 8?",
     "4, 7, 10, …   Total for 8 minutes = ?", 4, 3, 8, "minute", "minutes",
     "each minute she threads 3 more flowers than the minute before", "Meera has threaded 116 flowers by the end of minute 8.", 3, {}),
    # Long totals with one more step after the total.
    (P + "0af00a57-cee9-4091-a4f1-d76c3cf0aefb",
     "Priya lays diyas in rows: 5 in row 1, 9 in row 2, 13 in row 3, each row 4 more than the last, for 12 rows. Afterwards she has exactly 100 diyas left over. How many did she have at the start?",
     "5, 9, 13, …  12 rows, then 100 left.   Start = ?", 5, 4, 12, "row", "rows",
     "each row has 4 more diyas than the row before", "So the 12 rows use 324 diyas.", 3,
     {"tail": [
         B("Now back to the story. She used 324 diyas and still has 100 left over. So she started with 324 plus 100, which is 424 diyas.",
           *ANSC("fin", "324 + 100 = 424", 424)),
         B("Careful: 324 is one of the choices, but that is only the diyas in the rows. The question asks how many she had before she began."),
     ],
      "summary": "So find the last row, pair up to get the total used, and then add on what was left over."}),
    (P + "d4cb5b57-36d9-407b-8eed-0eee25daf5c9",
     "Priya adds diyas to her rangoli every day, following the pattern 5, 11, 17, 23, 29, and so on, for 12 days. How many does she add on day 12, and how many are there in total?",
     "5, 11, 17, 23, 29, …   Day 12 = ?   Total = ?", 5, 6, 12, "day", "days",
     "each day she adds 6 more diyas than the day before", "So the complete rangoli has 456 diyas.", 3,
     {"trap": "That answers the first part: she adds 71 diyas on day 12. Hold on to that number. Now for the total of all 12 days.",
      "tail": [
          B("So the two answers are: 71 diyas on day 12, and 456 diyas in total.",
            ANSL("fin", "Day 12: 71 diyas.   Total: 456 diyas"), CIRC("fin", "71"), CIRC("fin", "456")),
          B("Look carefully at the choices. Two of them have the right number for day 12, but only one has the right total as well. Check both parts before you choose."),
      ],
      "summary": "So find the last number with the jumps, then pair first with last for the total. And answer every part of the question."}),
    (P + "84c9d9c7-ee2f-4f36-bc7b-0f3f64d1f90e",
     "Priya puts 1 dot in the centre, then rings of dots around it: 6 in ring 1, 12 in ring 2, 18 in ring 3, each ring 6 more. After 8 rings she has used exactly half her dots. How many dots did she start with?",
     "Centre 1.   Rings: 6, 12, 18, … (8 rings) = half", 6, 6, 8, "ring", "rings",
     "each ring has 6 more dots than the ring before", "So the 8 rings use 216 dots.", 3,
     {"tail": [
         B("Don't forget the dot in the centre. 216 plus 1 is 217 dots used so far.", W("u", "216 + 1 = 217")),
         B("Those 217 dots are exactly half of all her dots. How do we get from the half to the whole?",
           ask=CHOOSE(["217 ÷ 2", "217 × 2", "217 + 2"], 1,
                      "If 217 is one half, then the other half is 217 as well. Two equal halves make the whole, so we double.")),
         B("217 times 2 is 434. Priya had 434 dots before she started.", *ANSC("fin", "217 × 2 = 434", 434)),
         B("Careful: 216 is one of the choices, but that is only the rings. And leaving out the centre dot gives 432, which is there too.",
           W("t", "216 × 2 = 432")),
     ],
      "summary": "So total the rings with the pairing shortcut, add anything extra like the centre dot, and double a half to get the whole."}),
]

LEFT_OUT = set()


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "lessons", "in-16.json"), encoding="utf-8") as f:
        batch = {q["id"]: q for q in json.load(f)}

    part = {}
    for qid, intro, given, terms, n, place, each, ending in TERMS:
        part[qid] = ap_term(qid, intro, given, terms, n, place, each, ending)
    for qid, intro, given, a, d, n, place, places, each, ending, shown, extra in SHORT:
        part[qid] = ap_list_sum(qid, intro, given, a, d, n, place, places, each, ending, shown=shown,
                                options=list(batch[qid]["options"].values()), **extra)
    for qid, intro, given, a, d, n, place, places, each, ending, shown, extra in LONG:
        part[qid] = ap_sum(qid, intro, given, a, d, n, place, places, each, ending, shown=shown,
                           options=list(batch[qid]["options"].values()), **extra)
    for name in ("imported_16_profit", "imported_16_seq"):
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        for qid, lesson in importlib.import_module(name).LESSONS.items():
            assert qid in batch and qid not in part, qid
            part[qid] = lesson

    missing = [qid for qid in batch if qid not in part and qid not in LEFT_OUT]
    out = os.path.join(ROOT, "data", "teach", "parts", "imported-16.json")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons; left out %d; no lesson yet for %d" % (len(part), len(LEFT_OUT), len(missing)))
    for qid in missing:
        print("  missing", qid)
    for qid, s in part.items():
        for i, b in enumerate(s["beats"]):
            if len(b["say"]) > 240:
                print("  say too long", qid, i, len(b["say"]))
            for c in (b.get("ask") or {}).get("choices", []):
                if len(c) > 40:
                    print("  choice too long", qid, i, c)
            for op in b.get("board", []):
                if op["op"] == "write" and len(op["text"]) > 60:
                    print("  line too long", qid, i, op["text"])


if __name__ == "__main__":
    main()
