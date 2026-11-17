"""One-off number patterns in batch 16, each written by hand."""
from imported_16_lib import ANS, ANSC, ANSL, B, BOX, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, STRIKE, UL, W, last_nth  # noqa: F401

P = "AIGEN_grade5_"
T = "IPMTB_grade5_ch03_"

LESSONS = {}

# ── Totals that need a little more than the pairing rule ──

# Rows 5, 8, 11, ... up to the row with 50 dots: total.
LESSONS[P + "1926d153-bfa7-4ad6-9531-027b4c337027"] = LESSON(
    B("Priya's rows go 5 dots, 8 dots, 11 dots, each row 3 more than the last, and she stops at the row with exactly 50 dots. How many dots are in the whole rangoli?",
      GIVEN("q", "5, 8, 11, … 50.   Total = ?")),
    B("To add the rows up we need to know how many rows there are. The story does not say, so we work it out from the jumps."),
    B("From 5 up to 50 is a climb of 45.",
      W("l1", "50 − 5 = 45")),
    B("Each jump is 3, so that is 45 divided by 3, which is 15 jumps.",
      W("l2", "45 ÷ 3 = 15"), NOTE("l2", "15", "jumps")),
    B("15 jumps. So how many rows is that?",
      ask=CHOOSE(["15 rows", "16 rows", "14 rows"], 1,
                 "Think small. 1 jump joins 2 rows, and 2 jumps join 3 rows. The rows are always one more than the jumps.")),
    B("15 jumps join 16 rows, because the first row counts too.",
      W("l3", "15 + 1 = 16"), NOTE("l3", "16", "rows")),
    B("Now the shortcut. Pair the first row with the last: 5 plus 50 is 55. The second with the second last, 8 plus 47, is 55 as well.",
      LB("list", "5, 8, 11, … 44, 47, 50"), W("l4", "5 + 50 = 55"), W("l5", "8 + 47 = 55")),
    B("16 rows make 8 pairs, and every pair is worth 55.",
      W("l6", "16 ÷ 2 = 8"), NOTE("l6", "8", "pairs")),
    B("8 times 55 is 440. Priya used 440 dots.",
      *ANSC("l7", "8 × 55 = 440", 440)),
    B("The trap is the row count. Use 15 rows instead of 16 and the total comes out too small. Always add 1 to the jumps."),
    B("Check the slow way. The first 8 rows add up to 124 and the last 8 add up to 316. And 124 plus 316 is 440.",
      W("c1", "5 + 8 + 11 + 14 + 17 + 20 + 23 + 26 = 124"), W("c2", "29 + 32 + 35 + 38 + 41 + 44 + 47 + 50 = 316"),
      W("c3", "124 + 316 = 440")),
    B("So when you know the last number but not how many there are: count the jumps, add 1, then pair first with last."),
)

# Rohit 15..45 and Virat 10..30: difference of the totals.
LESSONS[P + "42597968-a471-4599-a528-9b9cf50653bb"] = LESSON(
    B("Rohit scores 15, 21, 27, 33, 39 and 45 in his 6 innings. Virat scores 10, 14, 18, 22, 26 and 30. What is the difference between their totals?",
      GIVEN("r", "Rohit: 15, 21, 27, 33, 39, 45"), GIVEN("v", "Virat: 10, 14, 18, 22, 26, 30")),
    B("We need each player's total, and then the gap between the totals. Start with Rohit, and pair his scores from the outside in."),
    B("15 plus 45 is 60. 21 plus 39 is 60. And 27 plus 33 is 60.",
      W("r1", "15 + 45 = 60"), W("r2", "21 + 39 = 60"), W("r3", "27 + 33 = 60")),
    B("Three pairs of 60 make 180. So Rohit scores 180 runs.",
      W("r4", "3 × 60 = 180")),
    B("Now Virat. His first and last scores are 10 and 30. What will each of his pairs make?",
      ask=CHOOSE(["40", "30", "20"], 0,
                 "Add the first score to the last score: 10 plus 30. The other pairs, 14 with 26 and 18 with 22, come to the same.")),
    B("10 plus 30 is 40, and so are 14 plus 26 and 18 plus 22. Three pairs of 40 make 120 runs for Virat.",
      W("v1", "10 + 30 = 40"), W("v2", "3 × 40 = 120")),
    B("The difference is 180 minus 120, which is 60 runs.",
      *ANSC("ans", "180 − 120 = 60", 60)),
    B("Careful: finding the two totals is not the end. The question asks for the difference, so there is still a take away to do."),
    B("Here is a lovely check. Compare them innings by innings. Rohit is ahead by 5, then 7, then 9, 11, 13 and 15.",
      LB("g", "Gaps: 5, 7, 9, 11, 13, 15")),
    B("Add the gaps in pairs: 5 and 15, 7 and 13, 9 and 11. Each pair makes 20, and three 20s make 60. The same answer.",
      W("g1", "5 + 15 = 20"), W("g2", "3 × 20 = 60")),
    B("So to compare two totals: pair up each list to total it quickly, then take the smaller total from the bigger one."),
)

# Rings 5, 8, 11, ... with 100 stones: how many complete rings, how many left.
LESSONS[P + "325bc4eb-3bda-417d-9f07-fd3ffd99600e"] = LESSON(
    B("Priya's rings need 5 stones, then 8, then 11, each ring 3 more than the last. She has exactly 100 stones. How many complete rings can she make, and how many stones are left over?",
      GIVEN("q", "Rings: 5, 8, 11, …   100 stones.   Rings = ?  Left = ?")),
    B("For this one we keep a running total. After each ring we ask: have we gone past 100 yet?"),
    B("Ring 1 uses 5. Ring 2 brings the total to 13, and ring 3 brings it to 24.",
      W("l1", "5 + 8 = 13"), W("l2", "13 + 11 = 24")),
    B("Ring 4 needs 14, which makes 38. Ring 5 needs 17, which makes 55.",
      W("l3", "24 + 14 = 38"), W("l4", "38 + 17 = 55")),
    B("Ring 6 needs 20, which makes 75. Ring 7 needs 23, which makes 98.",
      W("l5", "55 + 20 = 75"), W("l6", "75 + 23 = 98"), NOTE("l6", "98", "after 7 rings")),
    B("She has used 98 stones in 7 rings. Ring 8 would need 26 stones. Can she make it?",
      LB("l7", "Ring 8 needs 23 + 3 = 26"),
      ask=CHOOSE(["Yes, she makes 8 rings", "No, she stops at 7 rings"], 1,
                 "She has 100 stones and has already used 98, so very few are left. Ring 8 needs 26, far more than that.")),
    B("100 minus 98 leaves just 2 stones. Ring 8 needs 26, so it cannot be finished.",
      W("l8", "100 − 98 = 2")),
    B("So the answer is 7 complete rings, with 2 stones left over.",
      ANSL("ans", "7 rings, 2 stones left over"), CIRC("ans", "7 rings"), CIRC("ans", "2 stones")),
    B("Careful: one choice has the right number of rings but a different leftover. The leftover has to be 100 minus 98."),
    B("Check the 98 with pairs. 5 plus 23 is 28, 8 plus 20 is 28, 11 plus 17 is 28, and 14 is left in the middle.",
      W("c1", "5 + 23 = 28"), W("c2", "8 + 20 = 28"), W("c3", "11 + 17 = 28")),
    B("3 times 28 is 84, and 84 plus 14 is 98. So 7 rings really do use 98 stones, leaving 2.",
      W("c4", "3 × 28 = 84"), W("c5", "84 + 14 = 98")),
    B("So when there is only so much to use: keep a running total, stop before you go over, and take away to find what is left."),
)

# Layers 20, 17, 14, ... down to 2: total.
LESSONS[P + "f4882e9b-324f-411b-909a-28b56a00f003"] = LESSON(
    B("Ananya's layers of samosas go 20, then 17, then 14, and carry on the same way until the top layer has only 2. How many samosas does she use altogether?",
      GIVEN("q", "Layers: 20, 17, 14, … 2.   Total = ?")),
    B("This pattern goes down. 20 minus 17 is 3, and 17 minus 14 is 3, so each layer has 3 fewer than the one below.",
      W("d1", "20 − 17 = 3"), W("d2", "17 − 14 = 3")),
    B("What do we need to do before we can add?",
      ask=CHOOSE(["Add 20 + 17 + 14 + 2", "Write out every layer down to 2", "Add just 20 + 2"], 1,
                 "The dots in the middle are hiding some layers. We have to find every one of them first, by taking away 3 each time.")),
    B("Keep taking away 3. After 14 comes 11, then 8, then 5, then 2. That is where she stops.",
      LB("list", "20, 17, 14, 11, 8, 5, 2")),
    B("Count them. There are 7 layers in all.",
      NOTE("list", "20, 17, 14, 11, 8, 5, 2", "7 layers")),
    B("Now pair them from the outside in. 20 plus 2 is 22, 17 plus 5 is 22, and 14 plus 8 is 22.",
      W("p1", "20 + 2 = 22"), W("p2", "17 + 5 = 22"), W("p3", "14 + 8 = 22")),
    B("The 11 in the middle has no partner. So we have 3 lots of 22, which is 66, and then 11 more.",
      BOX("list", "11"), W("p4", "3 × 22 = 66")),
    B("66 plus 11 is 77. Ananya uses 77 samosas.",
      *ANSC("ans", "66 + 11 = 77", 77)),
    B("The trap is losing a layer. Leave out the 11, or stop the list too early, and the total comes out too small. Writing the whole list keeps every layer safe."),
    B("Check by adding in order. 20 plus 17 plus 14 is 51, and 11 plus 8 plus 5 plus 2 is 26. Then 51 plus 26 is 77.",
      W("c1", "20 + 17 + 14 = 51"), W("c2", "11 + 8 + 5 + 2 = 26"), W("c3", "51 + 26 = 77")),
    B("So when a pattern counts down to a stopping number: write out every term, then pair them up and add."),
)

# ── Doubling patterns ──

_GROW = "Adding 3 works from 3 to 6. But then 6 plus 3 would be 9, and the next number is 12. Try times instead: each number is 2 times the one before."

# Meera's packets 3, 6, 12, 24: total for day 1 to day 6.
LESSONS[P + "14349a08-1a7d-40d8-884b-56953204695e"] = LESSON(
    B("Meera uses 3 packets of powder on day 1, then 6, then 12, then 24. If the pattern carries on, how many packets does she use altogether from day 1 to day 6?",
      GIVEN("q", "3, 6, 12, 24, …   Total for 6 days = ?")),
    B("First, how does this pattern grow?",
      ask=CHOOSE(["add 3 each time", "double each time", "add 6 each time"], 1, _GROW)),
    B("3 times 2 is 6, 6 times 2 is 12, and 12 times 2 is 24. Every day she uses double the day before.",
      W("d1", "3 × 2 = 6"), W("d2", "6 × 2 = 12"), W("d3", "12 × 2 = 24")),
    B("So day 5 is 24 times 2, which is 48. And day 6 is 48 times 2, which is 96.",
      W("l1", "24 × 2 = 48"), NOTE("l1", "48", "day 5"), W("l2", "48 × 2 = 96"), NOTE("l2", "96", "day 6")),
    B("Careful: 96 is only day 6, and it is one of the choices. The question wants all 6 days together.",
      LB("list", "3, 6, 12, 24, 48, 96")),
    B("Add them in order. 3 plus 6 plus 12 is 21. Then 21 plus 24 is 45.",
      W("a1", "3 + 6 + 12 = 21"), W("a2", "21 + 24 = 45")),
    B("45 plus 48 is 93, and 93 plus 96 is 189. She uses 189 packets.",
      W("a3", "45 + 48 = 93"), *ANSC("ans", "93 + 96 = 189", 189)),
    B("Check by adding in a different order. 24 and 6 make 30, 12 and 48 make 60, and 3 and 96 make 99. Then 30 plus 60 plus 99 is 189.",
      W("c1", "24 + 6 = 30"), W("c2", "12 + 48 = 60"), W("c3", "3 + 96 = 99"), W("c4", "30 + 60 + 99 = 189")),
    B("So first test the pattern: is it adding, or multiplying? Then find every number, and only then add them up."),
)

# Ravi's piggy bank 3, 6, 12, 24: total Monday to Saturday.
LESSONS[P + "1b8bf098-fced-43ae-b719-7634c8bb105d"] = LESSON(
    B("Ravi puts 3 rupees in his piggy bank on Monday, 6 on Tuesday, 12 on Wednesday and 24 on Thursday. If he carries on like this, how much is in there in total from Monday through Saturday?",
      GIVEN("q", "Mon 3, Tue 6, Wed 12, Thu 24, …   Total to Sat = ?")),
    B("What is the rule that takes us from one day to the next?",
      ask=CHOOSE(["add 3", "add 6", "multiply by 2"], 2, _GROW)),
    B("Each amount is double the one before: 3, then 6, then 12, then 24.",
      W("d1", "6 × 2 = 12"), W("d2", "12 × 2 = 24")),
    B("Two more days to go. Friday is 24 times 2, which is 48. Saturday is 48 times 2, which is 96.",
      W("l1", "24 × 2 = 48"), NOTE("l1", "48", "Friday"), W("l2", "48 × 2 = 96"), NOTE("l2", "96", "Saturday")),
    B("Monday through Saturday is 6 days, so there are 6 amounts to add.",
      LB("list", "3, 6, 12, 24, 48, 96")),
    B("3 plus 6 is 9. Add 12 to get 21. Add 24 to get 45.",
      W("a1", "3 + 6 = 9"), W("a2", "9 + 12 = 21"), W("a3", "21 + 24 = 45")),
    B("Add Friday's 48 to get 93. Then add Saturday's 96 to get 189. Ravi has 189 rupees.",
      W("a4", "45 + 48 = 93"), *ANSC("ans", "93 + 96 = 189", 189)),
    B("Careful: 93 and 96 are both among the choices. 93 is the total up to Friday only, and 96 is just Saturday's amount."),
    B("Here is a neat check. With doubling, the total so far is always 3 less than the next amount. 3 plus 6 is 9, and the next amount is 12.",
      UL("a1", "9"), UL("d1", "12")),
    B("After Saturday the next amount would be 96 times 2, which is 192. And 3 less than 192 is 189. It matches.",
      W("c1", "96 × 2 = 192"), W("c2", "192 − 3 = 189")),
    B("So spot the doubling, carry it on to the last day, and add every day's amount, not just the last one."),
)

# Meera's savings 3, 6, 12, 24: day 6.
LESSONS[P + "3df7ba15-d7e5-430c-bc41-23dd2a488708"] = LESSON(
    B("Meera saves 3 rupees on day 1, 6 on day 2, 12 on day 3 and 24 on day 4. If she keeps to the same pattern, how much will she save on day 6?",
      GIVEN("q", "3, 6, 12, 24, …   Day 6 = ?")),
    B("Look at how each day's savings come from the day before. What is happening?",
      ask=CHOOSE(["3 more each day", "double each day", "12 more each day"], 1, _GROW)),
    B("3 times 2 is 6, 6 times 2 is 12, and 12 times 2 is 24. Each day she saves double the day before.",
      W("d1", "3 × 2 = 6"), W("d2", "6 × 2 = 12"), W("d3", "12 × 2 = 24"), NOTE("d3", "24", "day 4")),
    B("We know day 4 is 24. How many more doublings take us to day 6?",
      ask=CHOOSE(["1", "2", "3"], 1,
                 "Day 4 to day 5 is one doubling. Day 5 to day 6 is another. Count the steps between the days, not the days themselves.")),
    B("First doubling: day 5 is 24 times 2, which is 48.",
      W("l1", "24 × 2 = 48"), NOTE("l1", "48", "day 5")),
    B("Second doubling: day 6 is 48 times 2, which is 96. Meera saves 96 rupees on day 6.",
      *ANSC("ans", "48 × 2 = 96", 96), NOTE("ans", "96", "day 6")),
    B("Two traps: stopping at 48, which is only day 5, and doubling once too often to reach 192. Both are among the choices, so label each day as you go.",
      W("t", "96 × 2 = 192"), NOTE("t", "192", "day 7")),
    B("Check by halving back down. Half of 96 is 48, and half of 48 is 24. Two halvings bring us back to day 4.",
      W("c1", "96 ÷ 2 = 48"), W("c2", "48 ÷ 2 = 24")),
    B("So find out whether the pattern adds or multiplies, then take one step at a time, naming each day."),
)

# Meera's packets doubling 3, 6, 12 for 5 days at 15 rupees a packet.
LESSONS[P + "c5bfda2b-73f7-4fbe-8216-f7cfa6212a05"] = LESSON(
    B("Meera uses 3 packets on day 1, 6 on day 2 and 12 on day 3, doubling every day. Each packet costs 15 rupees. How much does she spend over the first 5 days?",
      GIVEN("q", "3, 6, 12, … doubling.   5 days.   ₹15 a packet")),
    B("What do we need to find first?",
      ask=CHOOSE(["The packets used on day 5", "The total packets for 5 days", "15 × 5"], 1,
                 "She pays for every packet she uses, on every day. So first we need the total number of packets across all 5 days.")),
    B("Keep doubling. Day 4 is 12 times 2, which is 24. Day 5 is 24 times 2, which is 48.",
      W("l1", "12 × 2 = 24"), W("l2", "24 × 2 = 48")),
    B("Now add the 5 days. 3 plus 6 plus 12 is 21, and 24 plus 48 is 72.",
      LB("list", "3, 6, 12, 24, 48"), W("a1", "3 + 6 + 12 = 21"), W("a2", "24 + 48 = 72")),
    B("21 plus 72 is 93 packets in all.",
      W("a3", "21 + 72 = 93"), NOTE("a3", "93", "packets")),
    B("Each packet costs 15 rupees, so we need 93 times 15. Split the 15 into 10 and 5.",
      W("m0", "93 × 15")),
    B("93 times 10 is 930. And 93 times 5 is half of that, 465.",
      W("m1", "93 × 10 = 930"), W("m2", "93 × 5 = 465")),
    B("930 plus 465 is 1395. Meera spends 1395 rupees.",
      *ANSC("ans", "930 + 465 = 1395", 1395)),
    B("Careful: 93 is one of the choices, but that is packets, not rupees. And 720 is the cost of day 5 on its own.",
      W("t", "48 × 15 = 720"), NOTE("t", "720", "day 5 only")),
    B("Check the times a different way. 90 times 15 is 1350, 3 times 15 is 45, and 1350 plus 45 is 1395.",
      W("c1", "90 × 15 = 1350"), W("c2", "3 × 15 = 45"), W("c3", "1350 + 45 = 1395")),
    B("So in a two-part question: total the packets first, then multiply by the price of one."),
)

# ── Short series from the textbook ──

# 55555, 4444, 333, ?
LESSONS[T + "q002"] = LESSON(
    B("Here is a series: 55555, then 4444, then 333. We want the number that comes next.",
      GIVEN("q", "55555, 4444, 333, ?")),
    B("Don't read these as big numbers. Look at how each one is built. The first is made of 5s, and there are 5 of them.",
      UL("q", "55555"), NOTE("q", "55555", "five 5s")),
    B("The next is made of 4s, and there are 4 of them. Then come 3s, and there are 3 of them.",
      UL("q", "4444"), NOTE("q", "4444", "four 4s"), UL("q", "333"), NOTE("q", "333", "three 3s")),
    B("So what changes from one number to the next?",
      ask=CHOOSE(["Only the digit: it drops by 1", "Only the count of digits drops by 1", "Both the digit and the count drop by 1"], 2,
                 "Watch both things together. The digit goes 5, 4, 3. And the count of digits also goes 5, 4, 3.")),
    B("So next the digit must be 2, and there must be 2 of them."),
    B("Two 2s, written side by side, make 22.",
      ANS("ans", "22"), CIRC("ans", "22")),
    B("The traps come from changing only one thing. Keep three digits and you get 222. Drop to one digit and you get just 2. Both things must change together.",
      LB("t1", "222: three 2s, one too many"), LB("t2", "2: one 2, one too few")),
    B("Check the whole run: five 5s, four 4s, three 3s, two 2s. And after that would come a single 1.",
      LB("c", "55555, 4444, 333, 22, 1")),
    B("So in a pattern, look at how each number is built, not just how big it is. There can be two rules working at once."),
)

# 1, 2, 4, 8, 16: next two.
LESSONS[T + "q003"] = LESSON(
    B("The series goes 1, 2, 4, 8, 16. We want the next two numbers.",
      GIVEN("q", "1, 2, 4, 8, 16, ?, ?")),
    B("How do we get from each number to the next?",
      ask=CHOOSE(["add 2 each time", "multiply by 2 each time", "add 1, then 2, then 3"], 1,
                 "Adding 2 works from 2 to 4. But then 4 plus 2 is 6, and the next number is 8. Try doubling instead.")),
    B("1 times 2 is 2, 2 times 2 is 4, 4 times 2 is 8, and 8 times 2 is 16. Every number is double the one before.",
      W("d1", "4 × 2 = 8"), W("d2", "8 × 2 = 16"), NOTE("q", "8, 16", "× 2")),
    B("So the next number is 16 times 2, which is 32.",
      W("l1", "16 × 2 = 32")),
    B("And the one after that is 32 times 2, which is 64.",
      W("l2", "32 × 2 = 64")),
    B("So the next two numbers are 32 and 64.",
      ANSL("ans", "Next two: 32, 64"), CIRC("ans", "32, 64")),
    B("Careful: one choice begins with 16. But 16 is already in the series, so the next two must start after it."),
    B("Check by halving back. Half of 64 is 32, and half of 32 is 16, right where the series left off.",
      W("c1", "64 ÷ 2 = 32"), W("c2", "32 ÷ 2 = 16")),
    B("So test whether a series adds or multiplies. Then apply the rule once for each number you need."),
)

# 123, 234, 345, 456, ?
LESSONS[T + "q004"] = LESSON(
    B("The series goes 123, 234, 345, 456. What comes next?",
      GIVEN("q", "123, 234, 345, 456, ?")),
    B("Look at the digits of each number. 123 is 1, 2, 3 in a row. 234 is 2, 3, 4 in a row.",
      UL("q", "123"), UL("q", "234")),
    B("So how much bigger is each number than the one before?",
      ask=CHOOSE(["1 bigger", "11 bigger", "111 bigger"], 2,
                 "Each of the three digits goes up by 1: the hundreds digit, the tens digit and the ones digit. So the jump is 111.")),
    B("Test it. 234 minus 123 is 111, and 345 minus 234 is 111.",
      W("d1", "234 − 123 = 111"), W("d2", "345 − 234 = 111")),
    B("So the next number is 456 plus 111, which is 567.",
      *ANSC("ans", "456 + 111 = 567", 567)),
    B("Look at its digits: 5, 6, 7 in a row. The first digits have gone 1, 2, 3, 4, and now 5. Both ways of seeing the pattern agree.",
      LB("c", "1-2-3,  2-3-4,  3-4-5,  4-5-6,  5-6-7")),
    B("Careful with 555 and 654 in the choices. 555 repeats one digit, and 654 runs backwards. We need three digits climbing in a row, starting from 5.",
      LB("t1", "555: the same digit three times"), LB("t2", "654: digits going down")),
    B("So look for the rule inside the digits, then check it by finding the jump between neighbours."),
)

# *, 22, 33, *, 55
LESSONS[T + "q005"] = LESSON(
    B("This series has two stars hiding numbers: star, 22, 33, star, 55. We need both hidden numbers.",
      GIVEN("q", "*, 22, 33, *, 55")),
    B("Start with two neighbours we can see: 22 and 33. 33 minus 22 is 11, so the numbers go up by 11.",
      W("d1", "33 − 22 = 11"), NOTE("q", "22, 33", "+ 11")),
    B("The first star comes just before 22. How do we find it?",
      ask=CHOOSE(["22 + 11", "22 − 11", "22 ÷ 11"], 1,
                 "Going forwards we add 11. The star is one step back from 22, so we undo the adding and take 11 away.")),
    B("22 minus 11 is 11. So the first star is 11.",
      W("l1", "22 − 11 = 11")),
    B("The second star comes just after 33. 33 plus 11 is 44.",
      W("l2", "33 + 11 = 44")),
    B("Check with the last number. 44 plus 11 should be 55, and it is.",
      W("l3", "44 + 11 = 55")),
    B("So the stars are 11 and 44. The whole series is the 11 times table.",
      ANSL("ans", "11, 22, 33, 44, 55"), CIRC("ans", "11"), CIRC("ans", "44")),
    B("Don't be tempted by choices that just repeat a digit more or fewer times. A series follows a rule, and here the rule is add 11."),
    B("So find the jump from two neighbours you can see. Step back to fill a gap before them, and step forward to fill a gap after them."),
)

# 16, 32, 48, 65, 80, 96: which does not belong.
LESSONS[T + "q006"] = LESSON(
    B("Six numbers: 16, 32, 48, 65, 80, 96. One of them does not belong with the others.",
      GIVEN("q", "16, 32, 48, 65, 80, 96")),
    B("To find it, look at the jumps between neighbours. 32 minus 16 is 16, and 48 minus 32 is 16. So the pattern seems to be add 16.",
      W("d1", "32 − 16 = 16"), W("d2", "48 − 32 = 16")),
    B("Now the next jump. 65 minus 48 is 17. That is not 16, so something is off here.",
      W("d3", "65 − 48 = 17")),
    B("And 80 minus 65 is 15, also not 16. The last jump, 96 minus 80, is 16 again.",
      W("d4", "80 − 65 = 15"), W("d5", "96 − 80 = 16")),
    B("The two odd jumps are the one into 65 and the one out of 65. So which number does not belong?",
      ask=CHOOSE(["48", "65", "80"], 1,
                 "Look for the number that sits in both of the odd jumps. That is the one spoiling the pattern.")),
    B("It is 65. What should be there? 48 plus 16 is 64.",
      W("l1", "48 + 16 = 64"), STRIKE("q", "65", "64")),
    B("So 65 is the number that does not belong.",
      ANSL("ans", "65 does not belong"), CIRC("ans", "65")),
    B("Check: with 64 in its place, 64 plus 16 is 80, and every jump is 16. The series becomes the 16 times table.",
      W("c1", "64 + 16 = 80"), LB("c2", "16, 32, 48, 64, 80, 96")),
    B("So to find the odd one out, work out every jump. The number sitting between two odd jumps is the one."),
)

# 7, 12, 17, *, 27
LESSONS[T + "q007"] = LESSON(
    B("The series goes 7, 12, 17, then a star, then 27. We need the number hiding behind the star.",
      GIVEN("q", "7, 12, 17, *, 27")),
    B("Find the jump. 12 minus 7 is 5, and 17 minus 12 is 5. So each number is 5 more than the one before.",
      W("d1", "12 − 7 = 5"), W("d2", "17 − 12 = 5")),
    B("The star comes right after 17. How do we find it?",
      ask=CHOOSE(["17 + 5", "27 − 17", "17 + 12"], 0,
                 "The rule is add 5. The star is the very next number after 17, so we add 5 to 17.")),
    B("17 plus 5 is 22. So the star is 22.",
      *ANSC("ans", "17 + 5 = 22", 22)),
    B("Now check with the number after the star. 22 plus 5 should be 27, and it is.",
      W("c1", "22 + 5 = 27")),
    B("That check matters. One jump alone is not enough to be sure of a rule. We tested two jumps before the star and one after it, and all three are 5."),
    B("The full series is 7, 12, 17, 22, 27.",
      LB("c2", "7, 12, 17, 22, 27"), CIRC("c2", "22")),
    B("So find the jump from the numbers you can see, use it to fill the gap, and check that the next number still fits."),
)

# 63, 54, 45, 36: next two.
LESSONS[T + "q009"] = LESSON(
    B("The series goes 63, 54, 45, 36. We want the next two numbers.",
      GIVEN("q", "63, 54, 45, 36, ?, ?")),
    B("Are these numbers going up or down, and by how much?",
      ask=CHOOSE(["down by 9", "up by 9", "down by 11"], 0,
                 "Each number is smaller than the one before, so we are going down. Take 54 away from 63 to see by how much.")),
    B("63 minus 54 is 9, 54 minus 45 is 9, and 45 minus 36 is 9. So we take away 9 each time.",
      W("d1", "63 − 54 = 9"), W("d2", "54 − 45 = 9"), W("d3", "45 − 36 = 9")),
    B("36 minus 9 is 27.",
      W("l1", "36 − 9 = 27")),
    B("And 27 minus 9 is 18.",
      W("l2", "27 − 9 = 18")),
    B("So the next two numbers are 27 and 18.",
      ANSL("ans", "Next two: 27, 18"), CIRC("ans", "27, 18")),
    B("Did you notice? This is the 9 times table, running backwards. 9 times 7 is 63 at the start, and 9 times 2 is 18 at the end.",
      W("c1", "9 × 7 = 63"), W("c2", "9 × 2 = 18")),
    B("Careful with a choice that starts at 18. It is in the 9 times table, but it skips over 27. The next two must follow straight after 36."),
    B("So check whether the series climbs or falls, find the jump, and apply it once for each missing number."),
)

# 25, □, 75, 100, □, 150
LESSONS[T + "q011"] = LESSON(
    B("Here the series has two empty boxes: 25, a box, 75, 100, a box, 150. We need to fill both.",
      GIVEN("q", "25, □, 75, 100, □, 150")),
    B("To find the rule we need two numbers standing side by side. Which pair can we use?",
      ask=CHOOSE(["25 and 75", "75 and 100", "100 and 150"], 1,
                 "25 and 75 have a box between them, and so do 100 and 150. Only 75 and 100 are true neighbours.")),
    B("100 minus 75 is 25. So each number is 25 more than the one before.",
      W("d1", "100 − 75 = 25"), NOTE("q", "75, 100", "+ 25")),
    B("First box: 25 plus 25 is 50.",
      W("l1", "25 + 25 = 50")),
    B("Test it against the next number. 50 plus 25 is 75. Yes, it fits.",
      W("l2", "50 + 25 = 75")),
    B("Second box: 100 plus 25 is 125. And 125 plus 25 is 150, the last number, so that fits too.",
      W("l3", "100 + 25 = 125"), W("l4", "125 + 25 = 150")),
    B("So the boxes hold 50 and 125.",
      ANSL("ans", "25, 50, 75, 100, 125, 150"), CIRC("ans", "50"), CIRC("ans", "125")),
    B("The trap is treating 25 and 75 as neighbours. Their gap is 50, but that is two jumps, not one.",
      W("t", "75 − 25 = 50"), NOTE("t", "50", "two jumps", "below", last_nth("75 − 25 = 50", "50"))),
    B("So take the jump from two numbers that really are side by side. Then fill each box and check it against the number after it."),
)

# 0.0001, 0.001, 0.01: next two (0.1 and 1, which is none of the choices).
LESSONS[T + "q012"] = LESSON(
    B("Three small decimals: 0.0001, then 0.001, then 0.01. We want the next two numbers.",
      GIVEN("q", "0.0001, 0.001, 0.01, ?, ?")),
    B("Look at where the 1 sits in each number. Each time, it has moved one place to the left, closer to the decimal point.",
      UL("q", "0.0001"), UL("q", "0.001"), UL("q", "0.01")),
    B("When a digit moves one place to the left, what happens to the number?",
      ask=CHOOSE(["It gets 10 times bigger", "It gets 10 times smaller", "It gets 1 bigger"], 0,
                 "Moving a digit one place to the left makes it worth 10 times as much, just as 10 is worth 10 times as much as 1.")),
    B("So the rule is times 10. 0.0001 times 10 is 0.001, and 0.001 times 10 is 0.01.",
      W("d1", "0.0001 × 10 = 0.001"), W("d2", "0.001 × 10 = 0.01")),
    B("Next: 0.01 times 10 is 0.1.",
      W("l1", "0.01 × 10 = 0.1")),
    B("And 0.1 times 10 is 1. A whole 1, with no decimal part left.",
      W("l2", "0.1 × 10 = 1")),
    B("So the next two numbers are 0.1 and then 1. Now look for that pair among the choices.",
      LB("n", "Next two: 0.1, 1"), BOX("n", "0.1, 1")),
    B("One choice starts with 0.1 but follows it with 0.11. Another has 1 and then 10, which skips 0.1. No choice has 0.1 and then 1.",
      LB("o1", "0.1, 0.11: the second number does not fit"), LB("o2", "1, 10: skips 0.1")),
    B("So the answer is none of these. That is a real answer, and sometimes it is the right one.",
      ANSL("ans", "None of these"), CIRC("ans", "None of these")),
    B("The trap is grabbing the choice that starts with 0.1 without checking its second number. Always check both."),
    B("So work out your own answer first, and only then compare it with the choices."),
)
