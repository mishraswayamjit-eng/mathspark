"""Number-series lessons in batch 17 written one by one (fractions, decimals, digit patterns, squares, cubes)."""
from imported_17_lib import (B, CHOOSE, CIRC, GIVEN, GROUP, LB, LESSON, NOTE, Series, UL, W)

T = "IPMTB_grade5_ch03_"
L = {}

# ── Fractions ────────────────────────────────────────────────────────────────

L[T + "q014"] = LESSON(
    B("This series mixes fractions with one whole number, the 2. That 2 looks out of place, so let's see what it is hiding.",
      GIVEN("s", "1/2, 2/2, 3/2, 2, 5/2, __, __")),
    B("Look at the bottom numbers. They are all 2, so these fractions are halves. How many halves make the whole number 2?",
      ask=CHOOSE(["2/2", "4/2", "1/2"], 1,
                 "2 halves make just 1 whole. For 2 wholes we need twice as many, so that is 4 halves.")),
    B("So 2 is the same as 4 over 2. Write the series again, all in halves, and the top numbers read 1, 2, 3, 4, 5.",
      W("e", "2 = 4/2"), LB("h", "1/2, 2/2, 3/2, 4/2, 5/2"), UL("h", "4/2")),
    B("The top goes up by 1 each time, and the bottom stays at 2. So the next two are 6 over 2, and 7 over 2.",
      LB("n", "next: 6/2, 7/2")),
    B("Careful, we are not finished yet. Can 6 over 2 be written more simply?",
      ask=CHOOSE(["no, leave it as 6/2", "yes, it is 3", "yes, it is 6"], 1,
                 "6 over 2 means 6 divided by 2, and that is 3. When the top divides exactly by the bottom, the fraction is a whole number.")),
    B("6 divided by 2 is 3. But 7 does not divide exactly by 2, so 7 over 2 stays just as it is.",
      W("d", "6/2 = 3"), UL("n", "6/2")),
    B("So the next two numbers are 3, and 7 over 2. That matches the way the series wrote 4 over 2 as a plain 2.",
      LB("a", "Next two: 3, 7/2", "answer"), CIRC("a", "3, 7/2")),
    B("Check the step. Every number should be a half more than the one before. 5 over 2, plus a half, is 3. And 3, plus a half, is 7 over 2.",
      W("k1", "5/2 + 1/2 = 3"), W("k2", "3 + 1/2 = 7/2")),
    B("So when a series mixes fractions and whole numbers, write them all with the same bottom number first. Then the pattern shows itself."),
)

L[T + "q016"] = LESSON(
    B("Here is a series of fractions, and we want the next two. A fraction has two parts, a top and a bottom, so we look at each part on its own.",
      GIVEN("s", "1/2, 1/3, 1/4, 1/5, 1/6, __, __")),
    B("Read only the top numbers, all the way along. What do you notice?",
      ask=CHOOSE(["they go up by 1", "they are always 1", "they go down by 1"], 1,
                 "Read just the tops once more: 1, 1, 1, 1, 1. The top number never changes.")),
    B("The top stays at 1. Now read the bottom numbers: 2, 3, 4, 5, 6. They go up by 1 each time.",
      LB("t", "tops: 1, 1, 1, 1, 1"), LB("b", "bottoms: 2, 3, 4, 5, 6")),
    B("So the next two bottom numbers are 6 plus 1, which is 7, and 7 plus 1, which is 8.",
      W("b1", "6 + 1 = 7"), W("b2", "7 + 1 = 8")),
    B("So what are the next two numbers of the series?",
      ask=CHOOSE(["7, 8", "2/7, 2/8", "1/7, 1/8"], 2,
                 "7 and 8 are only the bottom numbers. Every number in this series is a fraction, with a 1 on top.")),
    B("Keep the 1 on top, and put the 7 and the 8 underneath. The next two are 1 over 7, and 1 over 8.",
      LB("a", "Next two: 1/7, 1/8", "answer"), CIRC("a", "1/7, 1/8")),
    B("Does that make sense? As the bottom number grows, the fraction shrinks. One roti shared among 8 gives smaller pieces than one roti shared among 7."),
    B("So for a series of fractions, read the tops and the bottoms as two separate patterns. Then put them back together."),
)

L[T + "q037"] = LESSON(
    B("One fraction is missing from this series. The others will tell us what it must be.",
      GIVEN("s", "1/7, 1/6, 1/5, __, 1/3")),
    B("Read only the bottom numbers: 7, 6, 5, then the gap, then 3. What is happening to them?",
      ask=CHOOSE(["they go down by 1", "they go up by 1", "they go down by 2"], 0,
                 "7, then 6, then 5. Each bottom number is 1 less than the one before it.")),
    B("The bottoms count down by 1. 5 minus 1 is 4. And 4 minus 1 is 3, the bottom that comes after the gap, so 4 fits.",
      LB("b", "bottoms: 7, 6, 5, __, 3"), W("b1", "5 − 1 = 4"), W("b2", "4 − 1 = 3")),
    B("And the top numbers? Every one of them is 1. So the missing fraction has a 1 on top as well.",
      LB("t", "tops: 1, 1, 1, __, 1")),
    B("So what goes in the gap?",
      ask=CHOOSE(["4", "4/1", "1/4"], 2,
                 "4 is only the bottom number. The fraction needs its 1 on top, with the 4 underneath.")),
    B("The missing number is 1 over 4, one quarter. Careful: 4 over 1 would mean 4 wholes, far too big to sit between a fifth and a third.",
      LB("a", "1/7, 1/6, 1/5, 1/4, 1/3", "answer"), CIRC("a", "1/4")),
    B("So in a series of fractions, find the pattern in the tops and the pattern in the bottoms. Then build the missing fraction from both."),
)

L[T + "q045"] = LESSON(
    B("Three fractions, and we want the fourth. The top and the bottom each have a pattern of their own, so we take them one at a time.",
      GIVEN("s", "2/1, 4/2, 6/3, ?")),
    B("The tops first: 2, 4, 6. What comes next?",
      ask=CHOOSE(["7", "8", "9"], 1, "2, 4, 6 goes up by 2 each time. So after 6 comes 6 plus 2, which is 8.")),
    B("The tops go up by 2, so the next top is 8.",
      LB("t", "tops: 2, 4, 6, 8"), W("t1", "6 + 2 = 8")),
    B("Now the bottoms: 1, 2, 3. They go up by 1, so the next bottom is 4.",
      LB("b", "bottoms: 1, 2, 3, 4"), W("b1", "3 + 1 = 4")),
    B("Careful here: the top and the bottom follow different rules. The top goes up by 2, but the bottom only goes up by 1. Don't use one step for both."),
    B("Put the two parts together: 8 on top, 4 underneath. The next number is 8 over 4.",
      LB("a", "Next: 8/4", "answer"), CIRC("a", "8/4")),
    B("Here is a lovely check. 2 divided by 1 is 2, 4 divided by 2 is 2, 6 divided by 3 is 2, and 8 divided by 4 is 2. Every fraction here is worth 2.",
      W("k", "2/1 = 4/2 = 6/3 = 8/4 = 2")),
    B("So split a fraction series into tops and bottoms, find each rule, and join them up again."),
)

L[T + "q038"] = LESSON(
    B("Three numbers and a gap. Two are fractions and one is a whole number, so let's make them all look alike first.",
      GIVEN("s", "1/4, 2/4, 1, __")),
    B("The fractions here are quarters. How many quarters make 1 whole?",
      ask=CHOOSE(["3/4", "4/4", "1/4"], 1,
                 "A whole cut into quarters has 4 pieces. So 1 whole is 4 quarters.")),
    B("So 1 is the same as 4 over 4. Now the top numbers read 1, 2, 4.",
      W("e", "1 = 4/4"), LB("h", "1/4, 2/4, 4/4, __")),
    B("It is tempting to say this series adds a quarter each time. But then 3 over 4 would come after 2 over 4, and it does not. The series jumps straight to 4 over 4."),
    B("So how do the tops get from 1 to 2, and from 2 to 4?",
      ask=CHOOSE(["they add 1", "they double", "they add 2"], 1,
                 "1 doubled is 2, and 2 doubled is 4. Adding 1 would give 3 after 2, and that is not what we see.")),
    B("Each top is double the one before. So the next top is 4 times 2, which is 8.",
      W("m1", "1 × 2 = 2"), W("m2", "2 × 2 = 4"), W("m3", "4 × 2 = 8")),
    B("That makes 8 over 4. And 8 over 4 means 8 divided by 4, which is 2. So the missing number is 2.",
      W("a", "8/4 = 2", "answer"), CIRC("a", "= 2")),
    B("Check with the numbers themselves: a quarter, a half, 1, 2. Each one is double the one before.",
      W("k1", "1/4 × 2 = 2/4"), W("k2", "2/4 × 2 = 1"), W("k3", "1 × 2 = 2")),
    B("So write everything with the same bottom number, then test the tops. If adding does not fit, try doubling."),
)

# ── Decimals ─────────────────────────────────────────────────────────────────

_d17 = Series("s", ["0.1", "0.01", "0.001", "*", "0.00001"])
_a17 = Series("a", ["0.1", "0.01", "0.001", "0.0001", "0.00001"])
L[T + "q017"] = LESSON(
    B("These are all tiny decimals, and each one has a single 1 in it. A star is hiding one of them.", _d17.given()),
    B("Count the zeros between the point and the 1. 0.1 has none. 0.01 has 1. 0.001 has 2.",
      _d17.note(0, "no zeros", "below"), _d17.note(1, "1 zero", "below"), _d17.note(2, "2 zeros", "below")),
    B("The number after the star, 0.00001, has 4 zeros. So how many zeros does the star need?",
      ask=CHOOSE(["2", "3", "4"], 1,
                 "The zeros go none, 1, 2, then the star, then 4. The star sits between 2 and 4, so it needs 3 zeros."),
      ),
    B("3 zeros after the point, and then the 1. That makes 0.0001.",
      _d17.note(4, "4 zeros", "below"), LB("f", "* = 0.0001")),
    B("Why does one more zero appear each time? Because each number is the one before it, divided by 10. Dividing by 10 pushes the 1 one place to the right.",
      W("m1", "0.1 ÷ 10 = 0.01"), W("m2", "0.01 ÷ 10 = 0.001")),
    B("Check both sides of the star. 0.001 divided by 10 is 0.0001. And 0.0001 divided by 10 is 0.00001. It fits on both sides.",
      W("k1", "0.001 ÷ 10 = 0.0001"), W("k2", "0.0001 ÷ 10 = 0.00001")),
    B("So the star is 0.0001. Careful when you pick it out: its neighbours 0.001 and 0.00001 look almost the same, so count the zeros slowly.",
      _a17.label("answer"), _a17.mark(3)),
    B("So with tiny decimals, count the zeros after the point. If one more appears each time, each number is the one before divided by 10."),
)

_d40 = Series("s", ["0.000001", "0.00001", "0.0001", "?", "?", "?"])
L[T + "q040"] = LESSON(
    B("Three very small decimals, and we want the next three. Each has a single 1, so the story is in the zeros.", _d40.given()),
    B("Count the zeros between the point and the 1. The first number has 5, the second has 4, and the third has 3.",
      _d40.note(0, "5 zeros", "below"), _d40.note(1, "4 zeros", "below"), _d40.note(2, "3 zeros", "below")),
    B("A zero disappears each time. So are the numbers getting bigger or smaller?",
      ask=CHOOSE(["smaller", "bigger", "staying the same"], 1,
                 "Fewer zeros after the point means the 1 sits in a bigger place. So 0.0001 is bigger than 0.00001. The series is growing.")),
    B("In fact each number is 10 times the one before. Multiplying by 10 moves the 1 one place to the left, and one zero drops away.",
      W("m1", "0.000001 × 10 = 0.00001"), W("m2", "0.00001 × 10 = 0.0001")),
    B("So keep going. 0.0001 times 10 is 0.001, with 2 zeros. Then 0.001 times 10 is 0.01, with just 1 zero.",
      W("n1", "0.0001 × 10 = 0.001"), W("n2", "0.001 × 10 = 0.01")),
    B("One more to find. What is 0.01 times 10?",
      ask=CHOOSE(["1", "0.1", "0.001"], 1,
                 "Only one zero drops away at each step. 0.01 has 1 zero after the point, so the next number has none: 0.1.")),
    B("0.01 times 10 is 0.1. Careful: it is tempting to leap to 1, but we only move one place at a time.",
      W("n3", "0.01 × 10 = 0.1")),
    B("So the next three numbers are 0.001, 0.01 and 0.1.",
      LB("a", "Next three: 0.001, 0.01, 0.1", "answer"), CIRC("a", "0.001, 0.01, 0.1")),
    B("So count the zeros after the point. Here one zero drops away each time, because every number is 10 times the one before."),
)

# ── Patterns in the digits ───────────────────────────────────────────────────

_a22 = Series("a", ["8888", "666", "44", "2"])
L[T + "q022"] = LESSON(
    B("These are strange numbers: 8888, then 666, then 44. Subtracting will not help much here. Look instead at how each number is built.",
      GIVEN("s", "8888, 666, 44, __")),
    B("Each number is one digit, written again and again. So there are two things to watch: which digit it is, and how many times it is written.",
      LB("p1", "8888: digit 8, written 4 times"), LB("p2", "666: digit 6, written 3 times"), LB("p3", "44: digit 4, written 2 times")),
    B("Take the digits first: 8, then 6, then 4. Which digit comes next?",
      ask=CHOOSE(["3", "2", "0"], 1, "8, 6, 4 goes down by 2 each time. So the next digit is 4 minus 2, which is 2.")),
    B("The digit drops by 2 each time, so the next digit is 2.",
      LB("dg", "digits: 8, 6, 4, 2"), W("d1", "4 − 2 = 2")),
    B("Now the count: written 4 times, then 3 times, then 2 times. How many times is the next digit written?",
      ask=CHOOSE(["2 times", "1 time", "3 times"], 1,
                 "4, 3, 2: the count drops by 1 each time. So the next digit is written just once.")),
    B("The count drops by 1 each time, so the next count is 1.",
      LB("ct", "times written: 4, 3, 2, 1"), W("c1", "2 − 1 = 1")),
    B("So we write the digit 2, once. Careful: writing it twice would have the right digit, but the count has to drop to 1. The next number is simply 2.",
      _a22.label("answer"), _a22.mark(3)),
    B("So when numbers look odd, ask what they are made of. Here two small patterns, the digit and the count, ran side by side."),
)

L[T + "q030"] = LESSON(
    B("Every number here is made only of 1s. So the pattern cannot be in the digit. It must be in how many 1s there are.",
      GIVEN("s", "1111111, 11111, 111, __")),
    B("Count them slowly, with a finger on each one. The first number has 7 ones, the second has 5, and the third has 3.",
      LB("p1", "1111111 has 7 ones"), LB("p2", "11111 has 5 ones"), LB("p3", "111 has 3 ones")),
    B("7, then 5, then 3. How many 1s will the next number have?",
      ask=CHOOSE(["2", "1", "0"], 1, "7, 5, 3 goes down by 2 each time. 3 minus 2 is 1, so the next number has a single 1.")),
    B("7 minus 2 is 5, 5 minus 2 is 3, and 3 minus 2 is 1. Two of the 1s are rubbed out at every step.",
      W("d1", "7 − 2 = 5"), W("d2", "5 − 2 = 3"), W("d3", "3 − 2 = 1")),
    B("Careful: 11 is tempting, because it looks like the next one down. But 11 has 2 ones, and that is a drop of only 1.",
      LB("t", "11 has 2 ones: a drop of only 1")),
    B("A number made of a single 1 is just 1. So the next number in the series is 1.",
      LB("a", "Next number: 1", "answer"), CIRC("a", "1")),
    B("So when every number uses the same digit, count how many times it is written. The pattern is hiding in the count."),
)

_s26 = Series("s", ["123", "132", "231", "213", "312", "__"])
_a26 = Series("a", ["123", "132", "231", "213", "312", "321"])
L[T + "q026"] = LESSON(
    B("Every number here uses the same three digits, 1, 2 and 3, just shuffled. So adding and subtracting are not the idea. Let's watch the shuffling.",
      _s26.given()),
    B("Look at them in pairs. 123 and 132 both start with 1. Then 231 and 213 both start with 2.",
      GROUP("s", ["123", "132"], "start with 1"), GROUP("s", ["231", "213"], "start with 2")),
    B("Inside a pair, what changes? Compare 123 with 132.",
      ask=CHOOSE(["the first digit changes", "the last two digits swap", "all three digits move"], 1,
                 "Both numbers keep the 1 in front. Behind it, the 2 and the 3 have swapped places.")),
    B("Yes: the first digit stays, and the last two swap. 231 turns into 213 in just the same way. The 2 stays, and the 3 and the 1 swap."),
    B("The last pair starts with 3, and its first number is 312. So keep the 3 in front, and swap the 1 and the 2.",
      _s26.mark(4, "underline"), LB("w", "312: keep the 3, swap 1 and 2")),
    B("That gives 321. So the next number in the series is 321.",
      _a26.label("answer"), _a26.mark(5)),
    B("Check another way. Three different digits can be arranged in only 6 ways, and 321 is the one arrangement the series had not used yet.",
      LB("k1", "start with 1: 123, 132"), LB("k2", "start with 2: 213, 231"), LB("k3", "start with 3: 312, 321")),
    B("So when the same digits keep coming back, look at how they are arranged. Find what stays put and what swaps."),
)

# ── Squares and cubes ────────────────────────────────────────────────────────

L[T + "q024"] = LESSON(
    B("49, 36, 25, 16. These are not just any numbers. Each one is a bit special, and that is the key to what comes next.",
      GIVEN("s", "49, 36, 25, 16, __")),
    B("49 is 7 times 7. So what kind of numbers are 49, 36, 25 and 16?",
      ask=CHOOSE(["multiples of 7", "square numbers", "even numbers"], 1,
                 "Each one is a number multiplied by itself. 7 times 7 is 49, and 6 times 6 is 36. Numbers like that are called square numbers.")),
    B("49 is 7 times 7. 36 is 6 times 6. 25 is 5 times 5. And 16 is 4 times 4.",
      W("q1", "49 = 7 × 7"), W("q2", "36 = 6 × 6"), W("q3", "25 = 5 × 5"), W("q4", "16 = 4 × 4")),
    B("Now look only at the numbers being squared: 7, 6, 5, 4. They count down by 1.",
      LB("r", "squaring: 7, 6, 5, 4, ?")),
    B("So which number gets squared next?",
      ask=CHOOSE(["2", "3", "4"], 1, "7, 6, 5, 4: one less each time. So after 4 comes 3.")),
    B("It is 3. But careful: 3 is only the number being squared, not the answer. We want 3 times 3, which is 9.",
      W("a", "3 × 3 = 9", "answer"), CIRC("a", "= 9")),
    B("Check with the jumps. 49 minus 36 is 13, 36 minus 25 is 11, 25 minus 16 is 9, and 16 minus 9 is 7. The jumps shrink by 2 each time, with no break.",
      W("k1", "49 − 36 = 13"), W("k2", "36 − 25 = 11"), W("k3", "25 − 16 = 9"), W("k4", "16 − 9 = 7")),
    B("So when a series looks familiar, ask if the numbers are squares. Find what is being squared, follow that pattern, then square again."),
)

L[T + "q029"] = LESSON(
    B("Two stars to find in this series. The numbers we can see, 125, 64 and 8, belong to a special family.",
      GIVEN("s", "125, 64, *, 8, *")),
    B("125 is 5 times 5 times 5. A number multiplied by itself, three times over like this, is called a cube.",
      W("c5", "125 = 5 × 5 × 5")),
    B("64 is a cube too. Which number, used three times, makes 64?",
      ask=CHOOSE(["8", "4", "6"], 1,
                 "8 times 8 is already 64, and that uses the 8 only twice. It takes a smaller number, used three times: 4 times 4, times 4 again.")),
    B("64 is 4 times 4 times 4. And little 8 is 2 times 2 times 2.",
      W("c4", "64 = 4 × 4 × 4"), W("c2", "8 = 2 × 2 × 2")),
    B("So the numbers being cubed go 5, 4, a star, 2, a star. They count down by 1, so the stars are cubing 3 and 1.",
      LB("r", "cubing: 5, 4, 3, 2, 1"), UL("r", "3"), UL("r", "1")),
    B("First star. Careful to use the 3 three times: 3 times 3 is 9, and 9 times 3 is 27.",
      W("c3", "3 × 3 × 3 = 27")),
    B("Second star: 1 times 1 times 1 is still 1.",
      W("c1", "1 × 1 × 1 = 1")),
    B("So the stars are 27 and 1.",
      LB("a", "125, 64, 27, 8, 1", "answer"), CIRC("a", "27"), CIRC("a", "1", 2)),
    B("So if a series is not squares, try cubes: 1, 8, 27, 64, 125. Find the numbers being cubed, and follow their pattern."),
)

L[T + "q039"] = LESSON(
    B("One number is missing from this series, and 121 is waiting at the end. Let's see what these numbers have in common.",
      GIVEN("s", "9, 25, 49, __, 121")),
    B("They are all square numbers. 9 is 3 times 3. Which number, times itself, makes 25?",
      ask=CHOOSE(["4", "5", "6"], 1, "Try it: 5 times 5 is 25.")),
    B("9 is 3 times 3, 25 is 5 times 5, 49 is 7 times 7, and at the far end 121 is 11 times 11.",
      W("q1", "9 = 3 × 3"), W("q2", "25 = 5 × 5"), W("q3", "49 = 7 × 7"), W("q4", "121 = 11 × 11")),
    B("Look at what is being squared: 3, 5, 7, a gap, then 11. Those are odd numbers.",
      LB("r", "squaring: 3, 5, 7, __, 11")),
    B("So which number is squared in the gap?",
      ask=CHOOSE(["8", "9", "10"], 1,
                 "3, 5, 7 goes up by 2 each time. 7 plus 2 is 9, and 9 plus 2 is 11, which matches the end.")),
    B("7 plus 2 is 9. And 9 plus 2 is 11, right on the number at the end, so 9 fits.",
      W("r1", "7 + 2 = 9"), W("r2", "9 + 2 = 11")),
    B("Careful: the gap wants the square, not the 9 itself. 9 times 9 is 81. So the missing number is 81.",
      W("a", "9 × 9 = 81", "answer"), CIRC("a", "81")),
    B("Notice that 64 and 100 are square numbers too. But they are 8 times 8 and 10 times 10, and this series squares only odd numbers.",
      W("t1", "8 × 8 = 64"), W("t2", "10 × 10 = 100")),
    B("So with a series of squares, write down what is being squared. Fill the gap in that small series first, then square it."),
)

L[T + "q034"] = LESSON(
    B("This question has two jobs in it. First find the next number in the series. Then square that number.",
      GIVEN("s", "72, 63, 54, 45, __"), GIVEN("g", "Find the square of the next number")),
    B("Job one. How do we get from 72 to 63?",
      ask=CHOOSE(["take away 11", "take away 9", "add 9"], 1,
                 "63 is smaller than 72, by 9. So the step is take away 9.")),
    B("72 minus 63 is 9, 63 minus 54 is 9, and 54 minus 45 is 9. The series goes down by 9 every time. It is the 9 times table, backwards.",
      W("d1", "72 − 63 = 9"), W("d2", "63 − 54 = 9"), W("d3", "54 − 45 = 9")),
    B("So the next number is 45 minus 9, which is 36.", W("n", "45 − 9 = 36")),
    B("Is 36 our final answer?",
      ask=CHOOSE(["yes, 36 is the answer", "no, we still have to square it"], 1,
                 "Read the question once more. It asks for the square of the next number, so there is one more job to do.")),
    B("Job two. Squaring means multiplying a number by itself, so 36 times 36. Split it up: 36 times 30 is 1080, and 36 times 6 is 216.",
      UL("g", "square"), W("p1", "36 × 30 = 1080"), W("p2", "36 × 6 = 216")),
    B("1080 plus 216 is 1296. So the square of the next number is 1296.",
      W("p3", "1080 + 216 = 1296"), W("a", "36 × 36 = 1296", "answer"), CIRC("a", "1296")),
    B("A quick check on the size. 36 is a little under 40, and 40 times 40 is 1600. So an answer a little under 1600 makes sense.",
      W("k", "40 × 40 = 1600")),
    B("So read the question right to the end. Find the next number with the step, then do the extra job it asks for."),
)
