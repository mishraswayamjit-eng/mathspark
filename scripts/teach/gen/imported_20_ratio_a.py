"""Sharing-in-a-ratio lessons, first half (see imported_20_ratio.py for the builders)."""
from imported_20_lib import P, B, W, U, choose_at
from imported_20_ratio import split, diff_tail, diff_check

LESSONS = {}

TWO_RATIOS = ("So with two ratios, one after the other, do the same three moves twice: count the parts, find one part, multiply. "
              "Just be sure the second time you share the right amount.")

# ── Kavya and Lakshmi: 90 packets, 2 : 3, Kavya gives away half ──
q = P + "0843ecde-8326-451c-a173-c2df49d90fd9"
LESSONS[q] = split(
    q, "Kavya and Lakshmi share 90 packets of coloured powder in the ratio 2 to 3. Then Kavya gives half of her share to Meera. We want to know what Kavya has left.",
    ["Kavya", "Lakshmi"], (2, 3), 90, "packets", [0],
    ("Kavya has 18 packets left", "18"),
    "So Kavya has 18 packets left. The trap is to stop at 36, which is her share before she gives any away.",
    givens=["90 packets shared"], ask_share=False,
    tail=[
        B("Now the last part of the story. Kavya gives away half of her 36 packets. What is half of 36?",
          ask=choose_at(q, "half", "18", ["36", "45"], "Half means sharing equally between 2. So we divide Kavya's 36 by 2, and that makes 18.")),
        B("She gives 18 to Meera, and 36 minus 18 leaves 18 for herself. When you give away half, you keep the other half.",
          W("t1", "36 ÷ 2 = 18"), W("t2", "36 − 18 = 18")),
    ])

# ── Priya and Rohan: ₹540, 4 : 5, Rohan spends ₹80 ──
q = P + "0d64e852-7e05-460d-8d91-baac6d95cf43"
LESSONS[q] = split(
    q, "Priya and Rohan are given 540 rupees to divide in the ratio 4 to 5, and Rohan gets the larger share. He spends 80 rupees and gives the rest to his mother. How much does she get?",
    ["Priya", "Rohan"], (4, 5), 540, "rupees", [1],
    ("Rohan gives his mother ₹220", "₹220"),
    "So Rohan gives his mother 220 rupees.",
    givens=["₹540 shared"], sym="₹",
    own="Rohan gets the larger share, so he has the 5 parts",
    tail=[B("Rohan spends 80 rupees on firecrackers, so we take 80 away from his 300. That leaves 220 for his mother.", W("t1", "300 − 80 = 220"))])

# ── Rohit and Virat: 180 runs, 5 : 4, Rohit doubles ──
q = P + "0fd1ade1-501d-4851-85f2-615fbd2d6d11"
LESSONS[q] = split(
    q, "Rohit and Virat scored 180 runs together, in the ratio 5 to 4. In the next match Rohit scored twice as many as in the first. We want Rohit's runs in the second match.",
    ["Rohit", "Virat"], (5, 4), 180, "runs", [0],
    ("Rohit's second match = 200 runs", "200"),
    "So Rohit scored 200 runs in the second match. Stopping at 100 is the trap: that was only the first match.",
    givens=["180 runs together"],
    got="Rohit scored 100 runs in the first match",
    tail=[B("In the second match he scored twice as many. Twice means 2 times, and 2 times 100 is 200.", W("t1", "2 × 100 = 200"))])

# ── Ananya and Bhavna: ₹480 profit, 3 : 5, Ananya spends ₹40 ──
q = P + "1b65ce20-c120-4b2e-ad5c-4111239c6f6c"
LESSONS[q] = split(
    q, "Ananya and Bhavna share a profit of 480 rupees in the ratio 3 to 5, the same as the money they put in. Ananya then spends 40 rupees on chai. How much of her share is left?",
    ["Ananya", "Bhavna"], (3, 5), 480, "rupees", [0],
    ("Ananya has ₹140 left", "₹140"),
    "So Ananya has 140 rupees left from her share.",
    givens=["Profit ₹480 shared"], sym="₹",
    tail=[B("Then Ananya spends 40 rupees on chai. 180 minus 40 is 140.", W("t1", "180 − 40 = 140"))])

# ── Priya and Rohan: ₹180, 4 : 5, sparklers cost ₹95 ──
q = P + "276e9c48-72f4-432c-9282-3df44e5e1e9e"
LESSONS[q] = split(
    q, "Priya and Rohan split 180 rupees in the ratio 4 to 5, with Rohan getting the larger share. He wants a box of sparklers that costs 95 rupees. Does he have enough, and by how much?",
    ["Priya", "Rohan"], (4, 5), 180, "rupees", [1],
    ("Enough, with ₹5 extra", "₹5"),
    "So Rohan has enough money, with 5 rupees extra.",
    givens=["₹180 shared", "Sparklers cost ₹95"], sym="₹",
    own="Rohan gets the larger share, so he has the 5 parts",
    tail=[
        B("Now compare. The sparklers cost 95 rupees and Rohan has 100. 100 is more than 95, so he has enough.", W("t1", "100 > 95"), U("g2", "₹95")),
        B("How much extra? Take the price away from his money: 100 minus 95 is 5.", W("t2", "100 − 95 = 5")),
    ])

# ── Rohit's two innings: 96 runs, 3 : 5 ──
q = P + "31636bce-8c52-4010-8092-99938e64c6b3"
LESSONS[q] = split(
    q, "Rohit scored 96 runs over two innings, in the ratio 3 to 5. We want his runs in the second innings.",
    ["1st innings", "2nd innings"], (3, 5), 96, "runs", [1],
    ("Second innings = 60 runs", "60"),
    "And that is what the question asks for. The order of a ratio matters: the second number belongs to the second innings.",
    givens=["96 runs in two innings"], spoken=["the first innings", "the second innings"],
    own="The second innings is the second number in the ratio, so it has 5 parts",
    got="he scored 60 runs in the second innings")

# ── Priya and Rohan: ₹1,800, 2 : 3, then diyas : candles 3 : 5 ──
q = P + "3c358f29-0003-4234-a968-85ea48000016"
LESSONS[q] = split(
    q, "Priya and Rohan share 1,800 rupees in the ratio 2 to 3. Priya then spends her share on diyas and candles in the ratio 3 to 5. We want the money she spends on candles.",
    ["Priya", "Rohan"], (2, 3), 1800, "rupees", [0],
    ("Priya spends ₹450 on candles", "₹450"),
    "So Priya spends 450 rupees on candles.",
    givens=["₹1,800 shared", "Diyas : Candles = 3 : 5"], sym="₹", ask_share=False,
    tail=[
        B("Now a second sharing begins. This time the amount being shared is Priya's 720 rupees, not the 1,800. Her ratio is 3 to 5, so how many parts this time?",
          U("g2", "3 : 5"),
          ask=choose_at(q, "parts2", "8 parts", ["5 parts", "15 parts"],
                        "This is a new ratio, 3 to 5, for diyas and candles. 3 parts and 5 parts make 8 parts.")),
        B("3 plus 5 is 8. 720 divided by 8 is 90, so each of these new parts is 90 rupees.", W("t1", "3 + 5 = 8"), W("t2", "720 ÷ 8 = 90")),
        B("Candles are the second number in that ratio, so they take 5 parts. 5 times 90 is 450.", W("t3", "5 × 90 = 450")),
    ],
    check=[B("Check: diyas take 3 parts, and 3 times 90 is 270. 270 plus 450 is 720, exactly Priya's share.",
             W("c1", "3 × 90 = 270"), W("c2", "270 + 450 = 720"))],
    summary=TWO_RATIOS)

# ── Riya and Sana: ₹770, 4 : 7, notebooks at ₹14 ──
q = P + "41119a22-d531-4e64-9165-da41901e4f83"
LESSONS[q] = split(
    q, "Riya and Sana collected 770 rupees in the ratio 4 to 7. Sana spends her whole share on notebooks that cost 14 rupees each. How many notebooks can she buy?",
    ["Riya", "Sana"], (4, 7), 770, "rupees", [1],
    ("Sana can buy 35 notebooks", "35"),
    "So Sana can buy 35 notebooks.",
    givens=["₹770 collected", "1 notebook costs ₹14"], sym="₹", ask_share=False,
    tail=[
        B("Each notebook costs 14 rupees. How do we find how many notebooks 490 rupees will buy?",
          ask=choose_at(q, "div", "490 ÷ 14", ["490 × 14", "490 − 14"],
                        "We want to know how many 14s fit into 490. Counting how many times one number fits into another is division.")),
        B("14 times 30 is 420, and 14 times 5 is 70. Together that makes 490, so 14 goes into 490 exactly 35 times.",
          W("t1", "14 × 30 = 420"), W("t2", "14 × 5 = 70"), W("t3", "490 ÷ 14 = 35")),
    ])

# ── Ananya's samosas: 72, morning : evening 3 : 5, Bhavna sells twice the morning ──
q = P + "579c2967-b522-49f5-8dd1-be673798b2c3"
LESSONS[q] = split(
    q, "Ananya sold 72 samosas, morning to evening in the ratio 3 to 5. Bhavna sold twice as many as Ananya sold in the morning. We want Bhavna's samosas.",
    ["Morning", "Evening"], (3, 5), 72, "samosas", [0],
    ("Bhavna sold 54 samosas", "54"),
    "So Bhavna sold 54 samosas. Notice it is twice Ananya's morning number, not twice her whole 72.",
    givens=["Ananya sold 72 samosas"], spoken=["the morning", "the evening"],
    own="The morning is the first number, so it has 3 parts",
    got="Ananya sold 27 samosas in the morning",
    tail=[B("Bhavna sold twice as many as that. Twice means 2 times, and 2 times 27 is 54.", W("t1", "2 × 27 = 54"))])

# ── Rohit and Virat: 126 runs, 5 : 4 ──
q = P + "587c5fab-3914-4048-8410-372b0b1a9ca5"
LESSONS[q] = split(
    q, "Rohit and Virat scored 126 runs together, in the ratio 5 to 4. We want Rohit's runs.",
    ["Rohit", "Virat"], (5, 4), 126, "runs", [0],
    ("Rohit scored 70 runs", "70"),
    "That is our answer: 70 runs for Rohit.",
    givens=["126 runs together"],
    own="Rohit is named first, so he has the first number, 5 parts")

# ── Kabir, Priya and Zara: ₹450, 2 : 3 : 5, Kabir donates half ──
q = P + "5ac74bab-5f3b-4cfe-b1bf-ce7cdca23a73"
LESSONS[q] = split(
    q, "Kabir, Priya and Zara split a profit of 450 rupees in the ratio 2 to 3 to 5. Kabir gives half of his share to charity. How much does he have left?",
    ["Kabir", "Priya", "Zara"], (2, 3, 5), 450, "rupees", [0],
    ("Kabir has ₹45 left", "₹45"),
    "So Kabir has 45 rupees left. That is the size of one part, which makes sense: half of 2 parts is 1 part.",
    givens=["Profit ₹450 shared"], sym="₹",
    tail=[B("Kabir donates half of his 90 rupees. 90 divided by 2 is 45, so he gives 45 away and keeps the other 45.", W("t1", "90 ÷ 2 = 45"))])

# ── Rohan and Sahil: ₹480 prize, 5 : 3, how much more ──
q = P + "5bdede09-912a-41fe-a27b-a73ce04feb8f"
LESSONS[q] = split(
    q, "Rohan and Sahil share 480 rupees of prize money in the ratio 5 to 3, the same as their runs. How much more does Rohan get? The 96 runs are not needed: it is the money we are sharing.",
    ["Rohan", "Sahil"], (5, 3), 480, "rupees", [0, 1],
    ("Rohan gets ₹120 more than Sahil", "₹120"),
    "So Rohan receives 120 rupees more than Sahil.",
    givens=["Prize money ₹480 shared"], sym="₹",
    tail=diff_tail(q, "The question asks how much more Rohan gets than Sahil.", 300, 180),
    check=diff_check("Rohan", "Sahil", 5, 3, 60, 120))

# ── Arjun, Bharat and Chetan: 225 runs, 3 : 5 : 7, ₹10 a run ──
q = P + "654c93ce-cbc1-4228-831b-caa6ecc410d0"
LESSONS[q] = split(
    q, "Arjun, Bharat and Chetan scored 225 runs in the ratio 3 to 5 to 7. The coach gives 10 rupees for every run. How much more money does Chetan get than Arjun?",
    ["Arjun", "Bharat", "Chetan"], (3, 5, 7), 225, "runs", [0, 2],
    ("Chetan gets ₹600 more than Arjun", "₹600"),
    "So Chetan receives 600 rupees more than Arjun.",
    givens=["225 runs together", "₹10 for every run"],
    tail=[
        B("We only need Chetan and Arjun. How many more runs did Chetan score than Arjun?",
          ask=choose_at(q, "diff", "105 − 45", ["105 + 45", "225 − 105"],
                        "How many more asks for the gap between Chetan's 105 and Arjun's 45. To find a gap, take the smaller from the bigger.")),
        B("105 minus 45 is 60. Chetan scored 60 runs more.", W("t1", "105 − 45 = 60")),
        B("Each run earns 10 rupees. So 60 extra runs earn 60 times 10, which is 600 rupees.", W("t2", "60 × 10 = 600"), U("g2", "₹10")),
    ],
    check=[B("Check it another way. Arjun earns 45 times 10, which is 450 rupees, and Chetan earns 105 times 10, which is 1,050. 1,050 minus 450 is 600 again.",
             W("c1", "45 × 10 = 450"), W("c2", "105 × 10 = 1,050"), W("c3", "1,050 − 450 = 600"))],
    summary="So the plan: count the parts, find one part, multiply for each share. Then find the gap, and only at the end turn runs into rupees.")

# ── Ravi and Sunil: 96 runs, 5 : 3, samosas for 4 teammates ──
q = P + "6b85d9b5-137a-4520-a9c7-f925ed48537b"
LESSONS[q] = split(
    q, "Ravi and Sunil scored 96 runs in the ratio 5 to 3. Ravi gives one samosa for every run he scored, shared equally among his 4 teammates. How many samosas does each teammate get?",
    ["Ravi", "Sunil"], (5, 3), 96, "runs", [0],
    ("Each teammate gets 15 samosas", "15"),
    "So each teammate gets 15 samosas.",
    givens=["96 runs together", "1 samosa per run, for 4 teammates"],
    got="Ravi scored 60 runs, and that means 60 samosas",
    tail=[B("Those 60 samosas are shared equally among 4 teammates. Sharing equally is dividing, and 60 divided by 4 is 15.",
            W("t1", "60 ÷ 4 = 15"), U("g2", "4 teammates"))])
