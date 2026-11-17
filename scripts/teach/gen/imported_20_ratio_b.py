"""Sharing-in-a-ratio lessons, second half (see imported_20_ratio.py for the builders)."""
from imported_20_lib import P, B, LESSON, G, W, Lb, A, U, C, N, X, F, bar, bars, seg, choose_at
from imported_20_ratio import split, diff_tail, diff_check, chain
from imported_20_ratio_a import TWO_RATIOS

LESSONS = {}

# ── Priya 12 and Rohan 8: ₹180 by age, Priya spends ₹45, then ₹50 more by age ──
q = P + "20edeb68-701c-4afd-b23b-86f0128cc816"
LESSONS[q] = split(
    q, "Priya and Rohan split 180 rupees in the ratio of their ages. Then Priya spends 45 rupees, and after that cousin Ankit gives them 50 rupees more, shared the same way. How much does Priya have now?",
    ["Priya", "Rohan"], (3, 2), 180, "rupees", [0],
    ("Priya has ₹93 now", "₹93"),
    "So Priya has 93 rupees now. We followed her money in order: a share, a spend, then another share.",
    givens=["₹180 shared by age, Priya spends ₹45", "Then ₹50 more, shared the same way"], sym="₹",
    pre={"x": 12, "y": 8, "g": 4, "others": ["2", "8"],
         "lead": "Priya is 12 years old and Rohan is 8. So the ratio of their ages, Priya to Rohan, is 12 to 8."},
    tail=[
        B("Next, Priya spends 45 rupees on sparklers. 108 minus 45 is 63.", W("t1", "108 − 45 = 63"), U("g1", "₹45")),
        B("Ankit's 50 rupees are shared the same way, into 5 parts. 50 divided by 5 is 10, and Priya's 3 parts make 3 times 10, which is 30.",
          W("t2", "50 ÷ 5 = 10"), W("t3", "3 × 10 = 30"), U("g2", "₹50")),
        B("Add that to what she had left: 63 plus 30 is 93.", W("t4", "63 + 30 = 93")),
    ])

# ── Sneha ₹35 and Tanvi ₹49: 84 balloons ──
q = P + "83fd5679-b0c2-48f4-9070-0b98c176dae8"
LESSONS[q] = split(
    q, "Sneha and Tanvi bought 84 water balloons together, and they share them in the ratio of the money each one paid. We want Tanvi's balloons.",
    ["Sneha", "Tanvi"], (5, 7), 84, "balloons", [1],
    ("Tanvi gets 49 balloons", "49"),
    "That is our answer. It is only a coincidence that Tanvi also paid 49 rupees: the money gave us the ratio, not the share.",
    givens=["84 balloons, shared by money paid"],
    pre={"x": 35, "y": 49, "g": 7, "others": ["5", "9"],
         "lead": "Sneha paid 35 rupees and Tanvi paid 49 rupees. So the ratio, Sneha to Tanvi, is 35 to 49."})

# ── Riya and Karan: ₹540, 4 : 5, then sparklers : rockets 2 : 3 ──
q = P + "8d09d599-8105-47ef-aa82-cc87d7cf3e53"
LESSONS[q] = split(
    q, "Riya and Karan split 540 rupees in the ratio 4 to 5, and Karan gets the larger share. He spends it on sparklers and rockets in the ratio 2 to 3. How much goes on rockets?",
    ["Riya", "Karan"], (4, 5), 540, "rupees", [1],
    ("Karan spends ₹180 on rockets", "₹180"),
    "So Karan spends 180 rupees on rockets.",
    givens=["₹540 shared", "Sparklers : Rockets = 2 : 3"], sym="₹", ask_share=False,
    own="Karan gets the larger share, so he has the 5 parts",
    tail=[
        B("Now a second sharing begins. This time the amount being shared is Karan's 300 rupees, not the 540. His ratio is 2 to 3, so how many parts this time?",
          U("g2", "2 : 3"),
          ask=choose_at(q, "parts2", "5 parts", ["9 parts", "6 parts"],
                        "This is a new ratio, 2 to 3, for sparklers and rockets. 2 parts and 3 parts make 5 parts.")),
        B("2 plus 3 is 5. 300 divided by 5 is 60, so each of these new parts is 60 rupees.", W("t1", "2 + 3 = 5"), W("t2", "300 ÷ 5 = 60")),
        B("Rockets are the second number in that ratio, so they take 3 parts. 3 times 60 is 180.", W("t3", "3 × 60 = 180")),
    ],
    check=[B("Check: sparklers take 2 parts, and 2 times 60 is 120. 120 plus 180 is 300, exactly Karan's share.",
             W("c1", "2 × 60 = 120"), W("c2", "120 + 180 = 300"))],
    summary=TWO_RATIOS)

# ── Kabir and Sahil: ₹480, 3 : 5 ──
q = P + "8ed85b3c-923c-4f0f-99c8-c38dd5222e83"
LESSONS[q] = split(
    q, "Kabir and Sahil scored runs in the ratio 3 to 5, and their coach shares 480 rupees between them in that same ratio. How much does Sahil get? It is the money we are sharing, so the 96 runs are not needed.",
    ["Kabir", "Sahil"], (3, 5), 480, "rupees", [1],
    ("Sahil receives ₹300", "₹300"),
    "That is our answer: 300 rupees for Sahil.",
    givens=["₹480 shared like their runs"], sym="₹")

# ── Ravi and Sanjay: 84 runs, 3 for every 4 ──
q = P + "8fc2cb61-e37c-4507-9e1d-715a30546cee"
LESSONS[q] = split(
    q, "Ravi and Sanjay scored 84 runs together. For every 3 runs Ravi scored, Sanjay scored 4. That is a ratio in disguise: Ravi to Sanjay is 3 to 4. We want Sanjay's runs.",
    ["Ravi", "Sanjay"], (3, 4), 84, "runs", [1],
    ("Sanjay scored 48 runs", "48"),
    "That is our answer: 48 runs for Sanjay.",
    givens=["84 runs together"])

# ── Priya and Kavya: 640 g of sand, 3 : 5, how much more ──
q = P + "90cb26fc-5785-45fc-ad62-546626d6d990"
LESSONS[q] = split(
    q, "Priya and Kavya used 640 grams of coloured sand in the ratio 3 to 5. How many grams more did Kavya use? The 18 diyas are only decoration here: they have nothing to do with the sand.",
    ["Priya", "Kavya"], (3, 5), 640, "grams", [0, 1],
    ("Kavya used 160 grams more", "160"),
    "So Kavya used 160 grams more sand than Priya.",
    givens=["640 grams of sand used"],
    tail=diff_tail(q, "The question asks how much more sand Kavya used than Priya.", 400, 240),
    check=diff_check("Kavya", "Priya", 5, 3, 80, 160))

# ── Team Sixer and Team Boundary: 84 balls, 3 : 4, 5 balls move ──
q = P + "a3734b08-6e99-4148-8d42-f99c7bd5bdb6"
LESSONS[q] = split(
    q, "Coach Sharma shares 84 balls between Team Sixer and Team Boundary in the ratio 3 to 4. Later, 5 balls move from Team Boundary to Team Sixer. We want the new ratio.",
    ["Sixer", "Boundary"], (3, 4), 84, "balls", [0, 1],
    ("New ratio, Sixer : Boundary = 41 : 43", "41 : 43"),
    "So the new ratio is 41 to 43. No number bigger than 1 divides both 41 and 43, so it cannot be made any simpler.",
    givens=["84 balls shared", "Then 5 balls go from Boundary to Sixer"], spoken=["Team Sixer", "Team Boundary"],
    tail=[
        B("Now 5 balls move from Team Boundary to Team Sixer. What happens to the two numbers?", U("g2", "5 balls"),
          ask=choose_at(q, "move", "Sixer + 5, Boundary − 5", ["Sixer + 5 only", "Sixer − 5, Boundary + 5"],
                        "The 5 balls leave Team Boundary, so Boundary loses 5. They arrive at Team Sixer, so Sixer gains 5. Both numbers change.")),
        B("36 plus 5 is 41 for Team Sixer. 48 minus 5 is 43 for Team Boundary.", W("t1", "36 + 5 = 41"), W("t2", "48 − 5 = 43")),
    ],
    check=[B("Check: no ball was lost, they only changed teams. 41 plus 43 is still 84.", W("c1", "41 + 43 = 84"))],
    summary="So the plan: share in the ratio first to get real numbers, make the change the story describes to those numbers, then write the new ratio.")

# ── Arjun and Kabir: 108 runs, 4 : 5, how many more ──
q = P + "ac9d619e-11af-4125-8dc6-083becdacf97"
LESSONS[q] = split(
    q, "Arjun and Kabir scored 108 runs together, in the ratio 4 to 5. By how many runs did Kabir outscore Arjun?",
    ["Arjun", "Kabir"], (4, 5), 108, "runs", [0, 1],
    ("Kabir scored 12 runs more", "12"),
    "So Kabir outscored Arjun by 12 runs.",
    givens=["108 runs together"],
    tail=diff_tail(q, "The question asks by how many runs Kabir outscored Arjun.", 60, 48),
    check=diff_check("Kabir", "Arjun", 5, 4, 12, 12))

# ── Priya ₹60 and Rohan ₹30: 90 sparklers, how many more ──
q = P + "aebb8ef4-58c9-464e-ab24-88e328e5115f"
LESSONS[q] = split(
    q, "Priya and Rohan buy a box of 90 sparklers and share them in the ratio of the money each one paid. How many more sparklers does Priya get than Rohan?",
    ["Priya", "Rohan"], (2, 1), 90, "sparklers", [0, 1],
    ("Priya gets 30 sparklers more", "30"),
    "So Priya gets 30 more sparklers than Rohan.",
    givens=["90 sparklers, shared by money paid"],
    pre={"x": 60, "y": 30, "g": 30, "others": ["10", "60"],
         "lead": "Priya paid 60 rupees and Rohan paid 30 rupees. So the ratio, Priya to Rohan, is 60 to 30."},
    tail=diff_tail(q, "The question asks how many more sparklers Priya gets than Rohan.", 60, 30, ask=False),
    check=diff_check("Priya", "Rohan", 2, 1, 30, 30))

# ── Ananya 3 hours and Bhavesh 5 hours: ₹640, how much more ──
q = P + "b733c45f-a070-4501-b33d-beceede72eda"
LESSONS[q] = split(
    q, "Ananya worked 3 hours and Bhavesh worked 5 hours, so they split the profit of 640 rupees in the ratio 3 to 5. How much more does Bhavesh get than Ananya?",
    ["Ananya", "Bhavesh"], (3, 5), 640, "rupees", [0, 1],
    ("Bhavesh gets ₹160 more", "₹160"),
    "So Bhavesh gets 160 rupees more than Ananya.",
    givens=["Profit ₹640, shared by hours worked"], sym="₹",
    tail=diff_tail(q, "The question asks how much more Bhavesh gets than Ananya.", 400, 240),
    check=diff_check("Bhavesh", "Ananya", 5, 3, 80, 160))

# ── Priya 9 and Rohan 6: ₹270 by age ──
q = P + "bcb8feb8-d435-4818-af5c-5c10c6ce3c2c"
LESSONS[q] = split(
    q, "Priya and Rohan are given 270 rupees, to divide in the ratio of their ages. We want Priya's share.",
    ["Priya", "Rohan"], (3, 2), 270, "rupees", [0],
    ("Priya receives ₹162", "₹162"),
    "That is our answer: 162 rupees for Priya.",
    givens=["₹270 shared by age"], sym="₹",
    pre={"x": 9, "y": 6, "g": 3, "others": ["2", "6"],
         "lead": "Priya is 9 years old and Rohan is 6. So the ratio of their ages, Priya to Rohan, is 9 to 6."})

# ── Priya and Rohan: 90 sparklers, 4 : 5, Rohan gives 6 away ──
q = P + "bf2f986e-1f70-4943-ad12-ca04c7b91bd5"
LESSONS[q] = split(
    q, "Priya and Rohan share 90 sparklers in the ratio 4 to 5, with Rohan getting the bigger share. Then Rohan gives 6 sparklers to his neighbour. How many does he have now?",
    ["Priya", "Rohan"], (4, 5), 90, "sparklers", [1],
    ("Rohan has 44 sparklers now", "44"),
    "So Rohan has 44 sparklers now.",
    givens=["90 sparklers shared"],
    own="Rohan gets the bigger share, so he has the 5 parts",
    tail=[B("Then Rohan gives 6 sparklers to his neighbour. 50 minus 6 is 44.", W("t1", "50 − 6 = 44"))])

# ── Riya ₹250 and Karan ₹200: 18 accessories ──
q = P + "c0efac63-758c-4006-99a2-c341f01b58c2"
LESSONS[q] = split(
    q, "Riya and Karan bought a cricket kit together, and they share its 18 extra accessories in the ratio of the money each one paid. We want Riya's accessories.",
    ["Riya", "Karan"], (5, 4), 18, "accessories", [0],
    ("Riya gets 10 accessories", "10"),
    "That is our answer. The rupees only told us the ratio: what we shared was the 18 accessories.",
    givens=["18 accessories, shared by money paid"],
    pre={"x": 250, "y": 200, "g": 50, "others": ["25", "100"],
         "lead": "Riya paid 250 rupees and Karan paid 200 rupees. So the ratio, Riya to Karan, is 250 to 200."})

# ── Priya and Sneha: 270 packets, 4 : 5, Sneha returns one third ──
q = P + "c95ebc37-14a9-4005-879a-6c281a37a100"
LESSONS[q] = split(
    q, "Priya and Sneha share 270 packets of coloured sand in the ratio 4 to 5. Afterwards Sneha gives one third of her packets back to the art teacher. How many does she have now?",
    ["Priya", "Sneha"], (4, 5), 270, "packets", [1],
    ("Sneha has 100 packets now", "100"),
    "So Sneha has 100 packets now.",
    givens=["270 packets shared"], ask_share=False,
    tail=[
        B("Sneha gives back one third of her 150 packets. To find one third, we divide by 3, and 150 divided by 3 is 50.", W("t1", "150 ÷ 3 = 50")),
        B("So 50 packets go back to the teacher. How many does Sneha have now?",
          ask=choose_at(q, "left", "150 − 50", ["just the 50", "150 + 50"],
                        "The 50 packets are the ones she gave back, not the ones she kept. Take them away from her 150 to see what is left.")),
        B("150 minus 50 is 100.", W("t2", "150 − 50 = 100")),
    ])

# ── Ananya and Bhavna: ₹360, 5 : 4, gift boxes at ₹30 ──
q = P + "cad3044f-c8d2-4812-8c96-87d5a50b5020"
LESSONS[q] = split(
    q, "Ananya and Bhavna share a profit of 360 rupees in the ratio 5 to 4. Ananya buys gift boxes that cost 30 rupees each with her share. How many boxes can she buy?",
    ["Ananya", "Bhavna"], (5, 4), 360, "rupees", [0],
    ("Ananya can buy 6 gift boxes", "6"),
    "So Ananya can buy 6 gift boxes, with 20 rupees left over.",
    givens=["Profit ₹360 shared", "1 gift box costs ₹30"], sym="₹", ask_share=False,
    tail=[
        B("Each gift box costs 30 rupees, so count in 30s. 6 boxes cost 6 times 30, which is 180. 7 boxes would cost 210.",
          W("t1", "6 × 30 = 180"), W("t2", "7 × 30 = 210")),
        B("Ananya has 200 rupees. So how many boxes can she buy?",
          ask=choose_at(q, "boxes", "6 boxes", ["7 boxes", "6 and a bit boxes"],
                        "7 boxes cost 210 rupees, and she only has 200, so 7 is too many. And a shop will not sell part of a box. 6 is the most she can buy.")),
        B("6 boxes use up 180 rupees. 200 minus 180 leaves 20 rupees, which is not enough for another box.", W("t3", "200 − 180 = 20")),
    ],
    summary="So the plan: count the parts, find one part, multiply for the share. And when you are buying whole things, leftover money that cannot buy one more is simply left over.")

# ── Riya 9 and Karan 6: ₹360 by age, diyas at ₹12 ──
q = P + "cf785395-4e40-48f4-90cf-9275c420f09b"
LESSONS[q] = split(
    q, "Riya and Karan share 360 rupees in the ratio of their ages. Riya spends her share on diyas that cost 12 rupees each. How many diyas can she buy?",
    ["Riya", "Karan"], (3, 2), 360, "rupees", [0],
    ("Riya can buy 18 diyas", "18"),
    "So Riya can buy 18 diyas.",
    givens=["₹360 shared by age", "1 diya costs ₹12"], sym="₹",
    pre={"x": 9, "y": 6, "g": 3, "others": ["2", "6"],
         "lead": "Riya is 9 years old and Karan is 6. So the ratio of their ages, Riya to Karan, is 9 to 6."},
    tail=[B("Each diya costs 12 rupees, so we need the number of 12s in 216. 12 times 10 is 120, and 12 times 8 is 96. Together that makes 216, so 12 goes in 18 times.",
            W("t1", "12 × 10 = 120"), W("t2", "12 × 8 = 96"), W("t3", "216 ÷ 12 = 18"))])

# ── Ananya and Bhavya: ₹480, 3 : 5, how much more ──
q = P + "e2016dbd-a828-4fcf-98ef-200367f21204"
LESSONS[q] = split(
    q, "Ananya and Bhavya share a profit of 480 rupees in the ratio 3 to 5, the same as the money they put in. How much more does Bhavya get than Ananya?",
    ["Ananya", "Bhavya"], (3, 5), 480, "rupees", [0, 1],
    ("Bhavya gets ₹120 more", "₹120"),
    "So Bhavya receives 120 rupees more than Ananya.",
    givens=["Profit ₹480 shared"], sym="₹",
    tail=diff_tail(q, "The question asks how much more Bhavya gets than Ananya.", 300, 180),
    check=diff_check("Bhavya", "Ananya", 5, 3, 60, 120))

# ── Riya's gulal: 25 packets, pink : yellow 3 : 2, ₹15 and ₹20 ──
q = P + "fb12d557-0838-4285-b7a6-f6b167b31fff"
LESSONS[q] = split(
    q, "Riya buys 25 packets of gulal, pink to yellow in the ratio 3 to 2. A pink packet costs 15 rupees and a yellow packet costs 20 rupees. How much does she spend altogether?",
    ["Pink", "Yellow"], (3, 2), 25, "packets", [0, 1],
    ("Riya spends ₹425 altogether", "₹425"),
    "So Riya spends 425 rupees altogether.",
    givens=["25 packets in all", "Pink ₹15 each, Yellow ₹20 each"], spoken=["pink", "yellow"],
    both_say="Pink has 3 parts: 3 times 5 is 15 packets. Yellow has 2 parts: 2 times 5 is 10 packets.",
    tail=[
        B("Now the money. There are 15 pink packets at 15 rupees each. Which sum gives their cost?", U("g2", "₹15"),
          ask=choose_at(q, "cost", "15 × 15", ["15 + 15", "25 × 15"],
                        "Each of the 15 pink packets costs 15 rupees. 15 lots of 15 is 15 times 15.")),
        B("15 times 15 is 225 rupees for pink. And 10 yellow packets at 20 rupees each cost 10 times 20, which is 200 rupees.",
          W("t1", "15 × 15 = 225"), W("t2", "10 × 20 = 200"), U("g2", "₹20")),
        B("Add the two costs: 225 plus 200 is 425.", W("t3", "225 + 200 = 425")),
    ],
    summary="So the plan: use the ratio to find how many of each kind, multiply each kind by its own price, then add the two costs.")

# ── Two ratios joined by one person ──
q = P + "29c81b6d-a4f6-47b3-930f-76d2073ba15e"
LESSONS[q], v = chain(
    q, "Riya and Sameer collect packets in the ratio 3 to 5. Sameer and Tina collect in the ratio 2 to 3. Tina collected 45 packets, and we want Riya's.",
    ("Riya", "Sameer", "Tina"), (3, 5), (2, 3), 2, 45, "packets", "",
    "Riya collected 18 packets", "So Riya collected 18 packets.")
assert v == 18

q = P + "458f85a6-4041-45af-8113-9c3d024fb8d5"
LESSONS[q], v = chain(
    q, "Kabir and Riya collected money in the ratio 3 to 5. Riya and Sanya collected in the ratio 4 to 7. Kabir collected 1,800 rupees, and we want Sanya's amount.",
    ("Kabir", "Riya", "Sanya"), (3, 5), (4, 7), 0, 1800, "rupees", "₹",
    "Sanya collected ₹5,250", "So Sanya collected 5,250 rupees.")
assert v == 5250

q = P + "7b8396f6-95ba-4875-9c94-37a432c8cf78"
LESSONS[q], v = chain(
    q, "Kabir and Lakshmi collected money in the ratio 3 to 5. Lakshmi and Neha collected in the ratio 4 to 7. Kabir collected 360 rupees, and we want Neha's amount.",
    ("Kabir", "Lakshmi", "Neha"), (3, 5), (4, 7), 0, 360, "rupees", "₹",
    "Neha collected ₹1,050", "So Neha collected 1,050 rupees.")
assert v == 1050

# ── Rohit and Virat: 5 : 3, then + 18 and + 42 makes them equal ──
q = P + "1259a4d7-be6e-4797-9ba3-7ee28eabc280"
LESSONS[q] = LESSON([
    B("Rohit's and Virat's runs were in the ratio 5 to 3. Then Rohit scored 18 more and Virat scored 42 more, and their totals became equal. We want Rohit's total over both matches.",
      G("g1", "First match, Rohit : Virat = 5 : 3"), G("g2", "Then Rohit + 18, Virat + 42: totals equal")),
    B("We don't know the runs yet, only the parts. In the first match Rohit has 5 equal parts and Virat has 3. Each bar then gets its extra runs.",
      F(bars(bar("Rohit", [seg(tone="a") for _ in range(5)] + [seg("18", 1.5, "c")]),
             bar("Virat", [seg(tone="b") for _ in range(3)] + [seg("42", 3.5, "c")]),
             note="After both matches the two bars are equal")),
      U("g1", "5"), U("g1", "3")),
    B("After the second match the totals are equal. So 5 parts plus 18 is the same as 3 parts plus 42.",
      Lb("e1", "5 parts + 18 = 3 parts + 42")),
    B("Both sides have at least 3 parts. If we take 3 parts off each side, what is left?",
      ask=choose_at(q, "bal", "2 parts + 18 = 42", ["2 parts = 42 + 18", "8 parts + 18 = 42"],
                    "Taking the same thing from both sides keeps them equal. 5 parts take away 3 parts leaves 2 parts on the left, and the 42 stays alone on the right.")),
    B("So 2 parts plus 18 equals 42.",
      X("e1", "3 parts", "− 3 parts"), N("e1", "5 parts", "− 3 parts", "above"), Lb("e2", "2 parts + 18 = 42")),
    B("Now take the 18 away from both sides. 42 minus 18 is 24, so 2 parts are worth 24 runs.",
      X("e2", "+ 18", "− 18"), W("w1", "42 − 18 = 24")),
    B("If 2 parts are 24 runs, one part is 24 divided by 2, which is 12.", W("w2", "24 ÷ 2 = 12")),
    B("Rohit had 5 parts in the first match. Which sum gives his runs in that match?",
      ask=choose_at(q, "first", "5 × 12", ["3 × 12", "5 + 12"],
                    "Each part is 12 runs, and Rohit has 5 of them. 5 lots of 12 is 5 times 12.")),
    B("5 times 12 is 60. But careful: the question wants his runs across both matches, so we add the 18. 60 plus 18 is 78.",
      W("w3", "5 × 12 = 60"), W("w4", "60 + 18 = 78")),
    B("So Rohit scored 78 runs across both matches.", A("ans", "Rohit's total = 78 runs"), C("ans", "78")),
    B("Check with Virat. 3 times 12 is 36, and 36 plus 42 is 78 as well. The totals are equal, just as the story says.",
      W("c1", "3 × 12 = 36"), W("c2", "36 + 42 = 78")),
    B("So when a ratio hides the real numbers, work in parts: write what the story says using parts, find one part, then go back for what the question asks."),
])

# ── Red and yellow paint: 3 : 5, yellow is 24 litres ──
q = P + "c8f3a7cb-530e-4e77-9630-f3e546143d59"
LESSONS[q] = LESSON([
    B("Red and yellow paint are mixed in the ratio 3 to 5, and 24 litres of yellow paint were used. We want the litres of red.",
      G("r", "Red : Yellow = 3 : 5"), G("g1", "Yellow = 24 litres")),
    B("The ratio means equal parts: 3 parts of red for every 5 parts of yellow.",
      F(bars(bar("Red", [seg(tone="a") for _ in range(3)], "?"), bar("Yellow", [seg(tone="b") for _ in range(5)], "24 litres"))),
      U("r", "3"), U("r", "5")),
    B("Here is the trap in this question. What is the 24 litres?", U("g1", "24 litres"),
      ask=choose_at(q, "what", "the yellow paint only", ["all the paint together", "the red paint only"],
                    "Read it once more: they used 24 litres of yellow paint. So 24 is not the total. It is the yellow on its own.")),
    B("So this time we do not add 3 and 5. The 24 litres fill yellow's 5 parts, and nothing else.", N("r", "5", "24 litres", "below")),
    B("One part is 24 divided by 5. A neat way to divide by 5 is to double, then divide by 10. Double 24 is 48, and 48 divided by 10 is 4.8.",
      W("w1", "24 × 2 = 48"), W("w2", "48 ÷ 10 = 4.8"), W("w3", "24 ÷ 5 = 4.8")),
    B("So each part is 4.8 litres. Red has 3 parts. Which sum gives the red paint?",
      ask=choose_at(q, "red", "3 × 4.8", ["5 × 4.8", "24 ÷ 3"],
                    "Each part is 4.8 litres, and red has 3 parts. So we want 3 lots of 4.8.")),
    B("3 times 4 is 12, and 3 times 0.8 is 2.4. Add them: 12 plus 2.4 is 14.4.",
      W("w4", "3 × 4 = 12"), W("w5", "3 × 0.8 = 2.4"), W("w6", "3 × 4.8 = 14.4")),
    B("So they used 14.4 litres of red paint.", A("ans", "Red paint = 14.4 litres"), C("ans", "14.4")),
    B("Check: red has fewer parts than yellow, and 14.4 is less than 24, so that fits. And 5 parts of 4.8 give back the 24 litres of yellow.",
      W("c1", "5 × 4.8 = 24"), W("c2", "14.4 < 24")),
    B("So before you share in a ratio, ask what the number in the story belongs to. If it is one share, divide by that share's parts, not by all the parts."),
])
