"""Adding and subtracting stories (gr5_operations1, gr5_decimals): what came in on one bar,
where it went on the other; the two bars are the same length, so the "?" piece is what is missing."""
from imported_other_lib import model, S, H, U, commas


def M(v, tag=""):
    """A rupee amount the question states."""
    f = float(v)
    text = "₹" + (commas(v) if f == int(f) else "%.2f" % f)
    return S(text + (" " + tag if tag else ""), v)


def W(v, word):
    """A count with its word: 987 boys."""
    return S("%s %s" % (commas(v), word), v)


def one(sid, whole, parts, **kw):
    """One bar: the whole on the brace, the pieces under it."""
    kw.setdefault("note", "How much is left?")
    kw.setdefault("unote", "Left: %s")
    model(sid, [("", parts, whole)], **kw)


def two(sid, top, bottom, **kw):
    model(sid, [top, bottom], **kw)


IN, OUT = "Money in", "Spent and left"
LEFT = dict(note="Both bars are the same money. How much is left?", unote="Left: %s")

# ── Whole numbers (gr5_operations1) ──
two("bbbd3f407726", (IN, [M(500), M(75)]), (OUT, [M(178), M(145), U()]), **LEFT)
one("91c26e6bef86", ("₹7,500", 7500), [M(2475), M(1368), M(2157), M(500), U()])
two("3a33caa1beb8", ("Telescope", [M(4500)]), ("Saved", [M(2450), M(375), M(1280), U()]),
    note="How much more does she need?", unote="Still needed: %s")
one("ac28c1d6ec77", ("₹1,000", 1000), [M(245), M(178), M(367), U()], note="How much change?", unote="Change: %s")
two("14c7202175e6", ("Team A", [S("287", 287), S("194", 194), S("38 more", 38)]), ("Team B", [S("315", 315), U()]), unit="runs",
    note="Team B wins by 38 runs, so its bar is 38 longer than Team A's runs", unote="Second innings: %s")
two("731249823ca6", ("Team A", [S("247", 247), S("183", 183), S("15 more", 15)]), ("Team B", [S("198", 198), U()]), unit="runs",
    note="Team B must finish 15 runs ahead of Team A", unote="Second innings: %s")
two("e718b43ae720", (IN, [M(500), M(20)]), (OUT, [M(137), M(218), M(89), U()]), **LEFT)
two("229497da7d6f", (IN, [M(4750), M(1150)]), (OUT, [M(1285), M(968), M(500), U()]), **LEFT)
one("61cca19c2bb4", ("₹5,000", 5000), [M(2475), M(1368), M(957), U()])
two("fd5a16ac4722", ("Cricket bat", [M(1250)]), ("Money so far", [M(485), M(378), M(200), U()]),
    note="How much more do they need?", unote="Still needed: %s")
two("ac44c2c02651", ("Gift", [U()]), (OUT, [M(2365), M(1480), M(955), M(3200, "left")]),
    note="The gift is everything she spent plus what is left", unote="The gift: %s")
two("acb5ccc157f5", (IN, [M(500), M(75)]), (OUT, [M(127), M(89), U()]), **LEFT)
two("48c374e6a2cc", ("Box", [U()]), ("Given and left", [S("168", 168), S("245", 245), S("137", 137), S("150 left", 150)]), unit="ladoos",
    note="The box held everything given away plus what is left", unote="In the box: %s")
one("7686251827ab", ("₹7,500", 7500), [M(2475), M(1368), M(2157), U()])
two("d03bd1579564", ("Team A", [S("248", 248), S("176", 176)]), ("Team B", [S("195", 195), S("213", 213)]), unit="runs",
    note="Which bar is longer, and by how many runs?", unote="The gap is %s")
two("020e23216286", (IN, [M(500), M(20)]), (OUT, [M(127), M(89), M(156), U()]), **LEFT)
two("3a98bbb464b8", ("India", [S("247", 247), S("189", 189)]), ("Australia", [S("312", 312), U()]), unit="runs",
    note="A tie: both bars the same length", unote="Second innings: %s")
two("03ccd1851975", ("Team A", [S("247", 247), S("189", 189)]), ("Team B", [S("312", 312), U()]), unit="runs",
    note="A tie: both bars the same length", unote="Second innings: %s")
two("9943d2b3a790", ("Team A", [S("247", 247), S("189", 189), S("1 more", 1)]), ("Team B", [S("315", 315), U()]), unit="runs",
    note="Team B must finish exactly 1 run ahead of Team A", unote="Second innings: %s")
two("47aef5cadb8f", (IN, [M(4750), M(1200)]), (OUT, [M(1285), M(965), U()]), **LEFT)
two("f10a7d43181a", ("Team A", [S("247", 247), S("189", 189), S("1 more", 1)]), ("Team B", [S("312", 312), U()]), unit="runs",
    note="To win, Team B needs at least 1 run more than Team A", unote="Second innings: %s")
two("97cc4d6f11b9", (IN, [M(500), M(75)]), (OUT, [M(128), M(97), U()]), **LEFT)
two("c2ec1c9d5425", ("Team A", [S("247", 247), S("189", 189)]), ("Team B", [S("198", 198), S("215", 215)]), unit="runs",
    note="Which bar is longer, and by how many runs?", unote="The gap is %s")
one("0fd67cfc9e65", ("₹1,200", 1200), [M(345), M(278), M(467), U()])
one("08d45be7cd1b", ("₹7,500", 7500), [M(2475), M(1368), M(2157), M(250), U()])
two("8c57f5fe7ae9", ("Gift", [U()]), ("Where it went", [M(750, "lent"), M(1275), M(850), M(1460), M(2165, "left")]),
    note="The gift is everything that went out plus what is left", unote="The gift: %s")
two("88027f2a6efe", ("Had", [M(1500, "saved"), U()]), (OUT, [M(1245), M(876), M(1534), M(2345, "left")]),
    note="The ? piece is grandmother's gift", unote="Grandmother's gift: %s")
two("e7fc2785e5cd", ("Had", [M(500, "found"), U()]), (OUT, [M(1245), M(867), M(1538), M(2350, "left")]),
    note="The ? piece is grandmother's gift", unote="Grandmother's gift: %s")
two("ee48fa3a72cc", ("Had", [M(500), M(750), U()]), (OUT, [M(1245), M(876), M(1389), M(2490, "left")]),
    note="The ? piece is grandmother's gift", unote="Grandmother's gift: %s")
one("f6b3c7441d56", ("₹5,000", 5000), [M(2475), M(1368), M(957), U("?", 2)],
    note="The 2 equal pieces are the 2 charity boxes", unote="Each box: %s")
two("b166c1fe39cf", ("Money in", [M(3500), M(2475), M(1860), M(2190)]), ("Out and left", [M(1345), U()]),
    note="How much is in the cash box at the end?", unote="In the box: %s")
two("f61af1d2a0d5", (IN, [M(5000), M(750)]), (OUT, [M(1475), M(1260), M(785), U(), M(1980, "left")]),
    note="The ? piece is the donation", unote="Donation: %s")

# Textbook questions.
one("IPMTB_grade5_ch05_q009", ("99,999", 99999), [S("70,369", 70369), U()], unit="", note="What must be added?", unote="Add %s")
one("IPMTB_grade5_ch05_q028", ("99,999", 99999), [S("65,269", 65269), U()], unit="", note="What must be added?", unote="Add %s")
one("IPMTB_grade5_ch05_q022", ("1600 students", 1600), [W(987, "boys"), U("? girls")], unit="", ans=lambda u: 987 - u,
    note="How many more boys than girls?", unote="Girls: %s")
one("IPMTB_grade5_ch05_q042", ("1500 students", 1500), [W(643, "boys"), U("? girls")], unit="", note="How many girls?", unote="Girls: %s")
two("IPMTB_grade5_ch05_q017", ("Students", [S("1007", 1007), W(49, "joined")]), ("Where they went", [W(17, "left"), W(1000, "passed"), U()]),
    unit="", note="The ? piece is the students who did not pass", unote="Did not pass: %s")
two("IPMTB_grade5_ch05_q047", ("Students", [S("1900", 1900), W(143, "joined")]), ("Where they went", [W(170, "left"), W(1300, "passed"), U()]),
    unit="", note="The ? piece is the students who did not pass", unote="Did not pass: %s")

# ── Decimals (gr5_decimals) ──
one("dfbb34789255", ("₹156.50", 156.5), [M(45.75), M(38.60), M(29.85), U("?", 2)],
    note="The 2 equal pieces are Kiran's and Priya's shares", unote="Each pays %s")
two("aab52d11f241", ("Ravi's gift", [U()]), (OUT, [M(247.50), M(183.75), M(118.25), M(200.50, "left")]), ans=lambda u: u - 150,
    note="Find Ravi's gift first. Priya got ₹150 less.", unote="Ravi's gift: %s")
two("b2b4a264e9e4", ("Ravi's gift", [U()]), (OUT, [M(247.50), M(183.75), M(94.25), M(124.50, "left")]), ans=lambda u: u - 350,
    note="Find Ravi's gift first. Priya got ₹350 less.", unote="Ravi's gift: %s")
two("60f66802660a", (IN, [M(100), M(2)]), (OUT, [M(32.45), M(18.70), M(25.50), U()]), **LEFT)
two("815f46f61421", ("Rohan", [S("14.38 s", 14.38)]), ("Kiran", [U(), S("1.65 s faster", 1.65)]), unit="s",
    note="Kiran's time is shorter than Rohan's by 1.65 seconds", unote="Kiran's time: %s")
one("3cf3c3a4746f", ("₹500", 500), [H("3 × ₹45.75", 137.25), H("4 × ₹32.50", 130), M(12.25), U()])
two("ff76ccf7fb0a", (IN, [M(50), M(5)]), (OUT, [M(18.75), M(14.50), U()]), **LEFT)
two("eec181959281", (IN, [M(100), M(5.25)]), (OUT, [M(23.45), M(31.80), U()]), **LEFT)
two("90b402055bcd", ("Bat", [M(875.50)]), ("Money", [M(312.75), M(248.60), U("?", 2)]),
    note="The 2 equal pieces are grandmother's gift, split in two", unote="Each gets %s")
one("3867840e7e5c", ("₹500", 500), [H("3.5 kg × ₹48.60", 170.10), H("1.75 kg × ₹96.40", 168.70), U()], note="How much change?", unote="Change: %s")
two("e1c920bc28f8", ("Bought", [S("1.25 kg", 1.25), S("0.8 kg", 0.8), S("1.45 kg", 1.45)]), ("Used and left", [S("2.75 kg", 2.75), U()]),
    unit="kg", note="How much powder is left over?", unote="Left over: %s")
one("908df02673a3", ("₹100", 100), [H("3 × ₹12.65", 37.95), M(45.50), U()], note="How much change?", unote="Change: %s")
one("a5a60c96bc7a", ("₹5,000", 5000), [H("2.5 kg × ₹864", 2160), H("1.75 kg × ₹1,120", 1960), U()], note="How much change?", unote="Change: %s")
one("b213f17c4419", ("₹200", 200), [H("3 × ₹45.75", 137.25), M(28.50), U()], note="How much change?", unote="Change: %s")
one("20ab0e973ca0", ("₹100", 100), [M(45.60), M(12.85), M(3.75), U()], note="How much change?", unote="Change: %s")
one("18f0181de900", ("65 runs", 65), [S("12.5", 12.5), S("8.75", 8.75), S("15.25", 15.25), S("9.50", 9.5), S("14.00", 14), U()], unit="",
    note="How many more runs to reach 65?", unote="Runs still needed: %s")
one("24a658ebc331", ("5 litres", 5), [H("12 × 0.35 litres", 4.2), U()], unit="litres")
one("395dd1f82cc2", ("₹200", 200), [H("3.5 kg × ₹48.60", 170.10), U()], note="How much change?", unote="Change: %s")
one("18ec0e94b6b2", ("15.6 kg", 15.6), [H("4 × 2.35 kg", 9.4), U()], unit="kg", note="What is left for the 5th day?", unote="5th day: %s")
one("00b714d76500", ("₹500", 500), [H("2.5 kg × ₹84.60", 211.50), U()], note="How much change?", unote="Change: %s")
one("72d773fd8af6", ("₹500", 500), [H("3.5 kg × ₹64.50", 225.75), U()], note="How much change?", unote="Change: %s")
one("e9dc6f4eae76", ("₹500", 500), [H("3 × ₹48.75", 146.25), H("2 × ₹62.50", 125), U("?", 4)],
    note="The 4 equal pieces are the gifts for 4 friends", unote="Each friend: %s")
one("7d47aadd3402", ("₹500", 500), [H("2.5 kg × ₹120.50", 301.25), H("1.75 kg × ₹80.40", 140.70), U()], note="How much change?", unote="Change: %s")
two("IPMTB_grade5_ch05_q016", ("In all", [U()]), ("", [S("Rs. 16.75", 16.75), S("Rs. 25.25", 25.25), S("Rs. 9.05", 9.05)]), unit="Rs.",
    note="Poonam, Urmila and Anjali put their money together", unote="In all: %s")
two("IPMTB_grade5_ch05_q039", ("In all", [U()]), ("", [S("Rs. 16.25", 16.25), S("Rs. 60.05", 60.05), S("Rs. 33.75", 33.75)]), unit="Rs.",
    note="Asha, Reeta and Geeta put their money together", unote="In all: %s",
    check=False)   # the key is "None of these": the total is not among the choices, so it is never shown
