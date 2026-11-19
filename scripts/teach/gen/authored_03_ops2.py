"""Multiplication and division warm-ups for part 03: short lessons, one idea each."""
from authored_03_lib import ANSC, B, CHOOSE, GIVEN, LB, LESSON, P, W  # noqa: F401

LESSONS = {}

# 12 eggs in a tray, 6 trays.
LESSONS[P + "OPERATIONS2_001"] = LESSON(
    B("A tray holds 12 eggs. How many eggs are there in 6 full trays?",
      GIVEN("q", "1 tray holds 12 eggs. 6 full trays?")),
    B("Every tray holds the same number, 12. So we have 6 equal groups of 12."),
    B("How do we count equal groups quickly?",
      ask=CHOOSE(["12 + 6", "12 × 6", "12 − 6"], 1,
                 "Adding 12 and 6 would give one tray and 6 loose eggs. Here we have 12 eggs again and again, 6 times over, and that is multiplying.")),
    B("12 times 6 is easy if we split the 12 into 10 and 2. 10 times 6 is 60, and 2 times 6 is 12.",
      W("l1", "10 × 6 = 60"), W("l2", "2 × 6 = 12")),
    B("60 plus 12 is 72. So 12 times 6 is 72, and there are 72 eggs.",
      W("l3", "60 + 12 = 72"), *ANSC("l4", "12 × 6 = 72", 72)),
    B("So equal groups mean multiply. And a big times fact can be split into two easy ones."),
)

# Rs 9 for every km, 7 km.
LESSONS[P + "OPERATIONS2_002"] = LESSON(
    B("An auto-rickshaw charges 9 rupees for every kilometre. What is the fare for a ride of 7 kilometres?",
      GIVEN("q", "₹9 for every km. Fare for 7 km?")),
    B("Each of the 7 kilometres costs the same amount, 9 rupees."),
    B("Which sum gives the fare?",
      ask=CHOOSE(["9 + 7", "9 × 7", "9 − 7"], 1,
                 "Adding 9 and 7 mixes rupees with kilometres. The 9 rupees are paid again for every one of the 7 kilometres, so we multiply.")),
    B("Here is a neat way to do 9 times 7. 10 times 7 is 70, and that is one 7 too many. 70 minus 7 is 63.",
      W("l1", "10 × 7 = 70"), W("l2", "70 − 7 = 63")),
    B("So 9 times 7 is 63. The fare is 63 rupees.",
      *ANSC("l3", "9 × 7 = 63", 63)),
    B("So the same amount for each one means multiply. And for a times 9, work out times 10 and take one lot away."),
)

# 7 days in a week, 8 weeks.
LESSONS[P + "OPERATIONS2_003"] = LESSON(
    B("There are 7 days in a week, and Meera's summer holiday lasts exactly 8 weeks. How many days is that?",
      GIVEN("q", "7 days in a week. Holiday: 8 weeks. Days?")),
    B("There are 8 weeks, with 7 days in every one. That is 8 equal groups of 7."),
    B("Which sum counts the days?",
      ask=CHOOSE(["7 + 8", "7 × 8", "8 − 7"], 1,
                 "7 plus 8 would be one week and 8 more days. Here every one of the 8 weeks has 7 days, so we multiply.")),
    B("7 times 8 is a fact lots of people mix up, so let's build it from doubles. 7 times 2 is 14. Double that for 7 times 4, which is 28.",
      W("l1", "7 × 2 = 14"), W("l2", "7 × 4 = 28")),
    B("Double once more for 7 times 8. Double 28 is 56. The holiday lasts 56 days.",
      *ANSC("l3", "7 × 8 = 56", 56)),
    B("Here is a way to remember it. Say 5, 6, 7, 8: 56 is 7 times 8.",
      W("l4", "56 = 7 × 8")),
    B("So equal groups mean multiply. And doubling twice turns a times 2 fact into a times 8 fact."),
)

# 45 laddoos shared among 5 children.
LESSONS[P + "OPERATIONS2_004"] = LESSON(
    B("Dadi shares 45 laddoos equally among 5 children. How many laddoos does each child get?",
      GIVEN("q", "45 laddoos shared equally among 5 children")),
    B("Dadi wants every child to get the same number, with no laddoos left over."),
    B("Which sum shares 45 equally among 5?",
      ask=CHOOSE(["45 − 5", "45 ÷ 5", "45 + 5"], 1,
                 "Taking 5 away would hand out only 5 laddoos. Sharing equally into 5 groups is a division.")),
    B("To divide 45 by 5, ask yourself: 5 times what makes 45? Counting up in fives, 5 times 9 is 45.",
      W("l1", "5 × 9 = 45")),
    B("So 45 divided by 5 is 9. Each child gets 9 laddoos.",
      *ANSC("l2", "45 ÷ 5 = 9", 9)),
    B("Check: 5 children with 9 laddoos each is 9 times 5, which is 45. Every laddoo is used.",
      W("l3", "9 × 5 = 45")),
    B("So sharing equally means dividing, and a times fact you know gives you the answer."),
)

# 96 children in rows of 8.
LESSONS[P + "OPERATIONS2_005"] = LESSON(
    B("For the morning assembly, 96 children stand in rows of 8. How many rows are there?",
      GIVEN("q", "96 children in rows of 8. How many rows?")),
    B("Each row takes 8 children. So we want to know how many eights fit into 96."),
    B("Which sum tells us that?",
      ask=CHOOSE(["96 − 8", "96 ÷ 8", "96 + 8"], 1,
                 "Taking away 8 fills only one row. To find how many rows of 8 there are in 96, we divide.")),
    B("96 is past the easy part of the 8 times table, so split it into 80 and 16.",
      W("l1", "96 = 80 + 16")),
    B("80 divided by 8 is 10 rows, and 16 divided by 8 is 2 more rows.",
      W("l2", "80 ÷ 8 = 10"), W("l3", "16 ÷ 8 = 2")),
    B("10 plus 2 is 12. So 96 divided by 8 is 12, and there are 12 rows.",
      *ANSC("l4", "96 ÷ 8 = 12", 12)),
    B("Check: 12 rows of 8 is 12 times 8, which is 96. Every child has a place.",
      W("l5", "12 × 8 = 96")),
    B("So making equal rows means dividing. And a big division can be split into two easy ones."),
)

# 6 notebooks cost Rs 240.
LESSONS[P + "OPERATIONS2_006"] = LESSON(
    B("6 notebooks of the same kind cost 240 rupees altogether. What is the cost of one notebook?",
      GIVEN("q", "6 notebooks cost ₹240 altogether. One notebook?")),
    B("The notebooks are all the same, so the 240 rupees are shared equally among the 6 of them."),
    B("Which sum gives the cost of one?",
      ask=CHOOSE(["240 × 6", "240 ÷ 6", "240 − 6"], 1,
                 "240 rupees is already the price of all 6. One notebook costs an equal share of that, which is less, so we divide.")),
    B("Here is a shortcut. 240 is 24 tens, and 24 divided by 6 is 4.",
      W("l1", "24 ÷ 6 = 4")),
    B("So 24 tens divided by 6 is 4 tens, which is 40. One notebook costs 40 rupees.",
      *ANSC("l2", "240 ÷ 6 = 40", 40)),
    B("Check: 6 notebooks at 40 rupees each is 6 times 40, which is 240.",
      W("l3", "6 × 40 = 240")),
    B("So the cost of one is the total divided by how many. And a zero at the end can wait while you use a fact you know."),
)

# Which number times 9 gives 108?
LESSONS[P + "OPERATIONS2_007"] = LESSON(
    B("Which number, when multiplied by 9, gives 108?",
      GIVEN("q", "? × 9 = 108")),
    B("Some number was multiplied by 9, and the result is 108. We want the number we started with."),
    B("What undoes multiplying by 9?",
      ask=CHOOSE(["subtracting 9", "dividing by 9", "adding 9"], 1,
                 "Times and divide are partners. Whatever times does, divide undoes. So to undo times 9, we divide by 9.")),
    B("So we divide 108 by 9. Split 108 into 90 and 18.",
      W("l1", "108 = 90 + 18")),
    B("90 divided by 9 is 10, and 18 divided by 9 is 2.",
      W("l2", "90 ÷ 9 = 10"), W("l3", "18 ÷ 9 = 2")),
    B("10 plus 2 is 12. So 108 divided by 9 is 12. The number is 12.",
      *ANSC("l4", "108 ÷ 9 = 12", 12)),
    B("Check: 12 times 9. 10 nines are 90 and 2 nines are 18, and together that is 108.",
      W("l5", "12 × 9 = 108")),
    B("So a missing number in a multiplication is found by dividing."),
)

# 60 bananas: how many dozens?
LESSONS[P + "OPERATIONS2_008"] = LESSON(
    B("One dozen is 12. A fruit seller has 60 bananas. How many dozens of bananas is that?",
      GIVEN("q", "1 dozen = 12. 60 bananas = ? dozens")),
    B("A dozen is a group of 12. So we want to know how many groups of 12 there are in 60."),
    B("Which sum tells us that?",
      ask=CHOOSE(["60 − 12", "60 ÷ 12", "60 + 12"], 1,
                 "Taking away 12 removes just one dozen. To count how many dozens fit into 60, we divide.")),
    B("Let's count up in twelves and keep a tally on our fingers: 12, 24, 36, 48, 60.",
      LB("l1", "12, 24, 36, 48, 60")),
    B("That took 5 twelves. So 60 divided by 12 is 5. There are 5 dozens of bananas.",
      *ANSC("l2", "60 ÷ 12 = 5", 5)),
    B("Check: 5 dozens is 5 times 12, which is 60.",
      W("l3", "5 × 12 = 60")),
    B("So to find how many equal groups fit into a number, divide. Counting up in the group size works too."),
)
