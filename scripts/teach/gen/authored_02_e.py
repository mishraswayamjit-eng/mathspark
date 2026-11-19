"""authored-02, fifth group: integers 005 to 012."""
from authored_02_lib import ANSC, ANSLC, B, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, STRIKE, UL, W

LESSONS = {}

# A building with no floor 0.
LESSONS["G5A_INTEGERS_005"] = LESSON(
    B("In Rahul's building there is no floor 0: the floor just above floor minus 1 is floor 1. He parks on floor minus 3, goes up 8 floors to his office, then down 2 floors to the canteen. Which floor is the canteen on?",
      GIVEN("q", "No floor 0. Start −3, up 8, down 2")),
    B("It is tempting to write minus 3 plus 8, which is 5. On an ordinary number line that would be right. Why not here?",
      W("l1", "−3 + 8 = 5"),
      ask=CHOOSE(["the lift is slow", "there is no floor 0 to count", "8 is too many floors"], 1,
                 "An ordinary number line has 0 between minus 1 and 1. This building skips it, so one of the steps in our sum lands on a floor that is not there.")),
    B("So we count the floors one at a time. Here are the floors in order, with no 0.",
      LB("f", "−3, −2, −1, 1, 2, 3, 4, 5, 6")),
    B("Start on minus 3 and count 8 floors up: minus 2, minus 1, then 1, 2, 3, 4, 5, 6. The 8th floor we reach is floor 6.",
      CIRC("f", "6"), NOTE("f", "6", "office")),
    B("So the office is on floor 6, one higher than the 5 our sum gave.",
      STRIKE("l1", "5", "6")),
    B("Now the canteen is 2 floors down from 6. Which floor is that?",
      ask=CHOOSE(["floor 4", "floor 3", "floor 5"], 0,
                 "From 6, one floor down is 5, and one more down is 4. There is no missing floor between 6 and 4, so this part is ordinary counting.")),
    B("Down from 6: floor 5, then floor 4. The canteen is on floor 4.",
      *ANSC("l2", "6 − 2 = 4", 4), CIRC("f", "4")),
    B("The trap is minus 3 plus 8 minus 2, which gives 3. That counts a floor 0 that this building does not have.",
      W("l3", "−3 + 8 − 2 = 3")),
    B("So when the numbering skips a number, do not trust the sum. Count the steps one by one. The canteen is on floor 4."),
)

# k < −3: which is always the greatest?
LESSONS["G5A_INTEGERS_006"] = LESSON(
    B("k is an integer less than minus 3. Which of these is always the greatest: k plus 5, k minus 3, k plus k, or 2 minus k?",
      GIVEN("q", "k < −3. Which is always the greatest?"), LB("o", "k + 5,   k − 3,   k + k,   2 − k")),
    B("We do not know k, so let's try one value it could have. It must be less than minus 3. Let's take minus 4.",
      LB("l1", "try k = −4")),
    B("k plus 5 is minus 4 plus 5, which is 1. k minus 3 is minus 4 minus 3, which is minus 7. k plus k is minus 8.",
      W("l2", "−4 + 5 = 1"), W("l3", "−4 − 3 = −7"), W("l4", "−4 + (−4) = −8")),
    B("Now the last one: 2 minus k, which is 2 take away minus 4. What is that?",
      ask=CHOOSE(["−2", "6", "−6"], 1,
                 "Taking away a negative number is the same as adding its opposite. So 2 take away minus 4 is 2 plus 4.")),
    B("Taking away minus 4 is the same as adding 4. So 2 minus k is 2 plus 4, which is 6.",
      W("l5", "2 − (−4) = 2 + 4 = 6")),
    B("Our four results are 1, minus 7, minus 8 and 6. The greatest is 6, from 2 minus k.",
      CIRC("l5", "6"), CIRC("o", "2 − k")),
    B("But the question says always. Will it still win for other values? Try k as minus 10: k plus 5 is minus 5, and 2 minus k is 12.",
      W("l6", "−10 + 5 = −5"), W("l7", "2 − (−10) = 12")),
    B("Here is why. k plus 5 is always less than 2, because k is below minus 3. But taking away k adds more than 3 on to 2, so 2 minus k is always more than 5."),
    B("So the greatest is always 2 minus k.",
      *ANSLC("l8", "2 − k is always the greatest", "2 − k")),
    B("The trap is k plus 5, because adding looks bigger. With negative numbers, test a value: taking away a negative is what makes a number grow."),
)

# Leh: Monday −9 to 5; Tuesday's highest.
LESSONS["G5A_INTEGERS_007"] = LESSON(
    B("Monday in Leh: lowest minus 9 degrees, highest 5. Tuesday's lowest was 4 degrees lower than Monday's. Tuesday's gap between highest and lowest was 3 degrees less than Monday's gap. What was Tuesday's highest?",
      GIVEN("q", "Mon: −9°C to 5°C. Tue: lowest 4 lower, gap 3 less")),
    B("Three things to find, in order: Monday's gap, Tuesday's lowest, and Tuesday's gap. Start with Monday. How many degrees is it from minus 9 up to 5?",
      ask=CHOOSE(["4 degrees", "14 degrees", "9 degrees"], 1,
                 "Climb in two parts. From minus 9 up to zero is 9 degrees. Then from zero up to 5 is 5 more. 9 and 5 make 14.")),
    B("From minus 9 up to 0 is 9 degrees, then 5 more to reach 5. Monday's gap is 14 degrees.",
      W("l1", "9 + 5 = 14"), W("l1b", "5 − (−9) = 14")),
    B("Tuesday's gap is 3 less than that. 14 minus 3 is 11 degrees.",
      W("l2", "14 − 3 = 11")),
    B("Now Tuesday's lowest. It is 4 degrees lower than minus 9. Which way is lower?",
      ask=CHOOSE(["−5: nearer to zero", "−13: further below zero"], 1,
                 "Lower means colder. Colder than minus 9 goes further below zero, so we step down 4 from minus 9.")),
    B("Lower means further below zero. Minus 9 minus 4 is minus 13.",
      W("l3", "−9 − 4 = −13")),
    B("Tuesday starts at minus 13 and its gap is 11. Go up 11 from minus 13. That does not even reach zero: it stops at minus 2.",
      *ANSC("l4", "−13 + 11 = −2", "−2")),
    B("Check: from minus 13 up to minus 2 is 11 degrees, and 11 is 3 less than Monday's 14.",
      W("l5", "−2 − (−13) = 11")),
    B("The traps: taking Monday's gap as 9 minus 5, and taking 4 lower than minus 9 as minus 5. Lower always means further down the thermometer."),
    B("So find the gap by climbing through zero, change it as the story says, then climb from the new lowest. Tuesday's highest was minus 2 degrees."),
)

# Quiz: +5 and −2, 20 questions, 51 points.
LESSONS["G5A_INTEGERS_008"] = LESSON(
    B("In a quiz, each right answer earns 5 points, and each answer that is not right loses 2 points. Riya answered all 20 questions and scored 51. How many did she get right?",
      GIVEN("q", "Right: +5. Not right: −2. 20 questions, score 51")),
    B("Here is a clever way in. Imagine Riya got every single one right. 20 times 5 is 100 points.",
      W("l1", "20 × 5 = 100")),
    B("But she scored 51. So she is short of a perfect score by 100 minus 51, which is 49 points.",
      W("l2", "100 − 51 = 49")),
    B("Now change one right answer into one that is not right. How many points does the score drop?",
      ask=CHOOSE(["2 points", "5 points", "7 points"], 2,
                 "She does not earn the 5 points any more, and she loses 2 more on top. So the score drops by 5 and then by 2.")),
    B("Each miss costs 7 points: the 5 she does not earn, and the 2 she loses.",
      W("l3", "5 + 2 = 7")),
    B("She is 49 points short, at 7 points a miss. 49 divided by 7 is 7 misses.",
      W("l4", "49 ÷ 7 = 7")),
    B("Careful: 7 is how many were not right. The question asks how many were right. 20 minus 7 is 13.",
      *ANSC("l5", "20 − 7 = 13", 13)),
    B("Check: 13 right answers earn 65 points. 7 misses lose 14. And 65 minus 14 is 51.",
      W("l6", "13 × 5 = 65"), W("l7", "7 × 2 = 14"), W("l8", "65 − 14 = 51")),
    B("So start from a perfect score, find how far short she is, and divide by what each miss really costs. Riya got 13 right."),
)

# Integers greater than −10 that are closer to −3 than to 5.
LESSONS["G5A_INTEGERS_009"] = LESSON(
    B("How many integers greater than minus 10 are closer to minus 3 than to 5 on the number line?",
      GIVEN("q", "Integers > −10, closer to −3 than to 5")),
    B("Picture minus 3 and 5 on the number line. Somewhere between them is a point exactly as far from one as from the other. Everything to the left of that point is closer to minus 3."),
    B("How far is it from minus 3 to 5? 3 steps up to 0, and 5 more. That is 8 units.",
      W("l1", "3 + 5 = 8")),
    B("Half of 8 is 4. So the halfway point is 4 steps from each end. Minus 3 plus 4 is 1.",
      W("l2", "8 ÷ 2 = 4"), W("l3", "−3 + 4 = 1"), W("l3b", "5 − 4 = 1")),
    B("So 1 is the halfway point. Is 1 itself closer to minus 3?",
      ask=CHOOSE(["yes, count it", "no, it is equally far from both"], 1,
                 "1 is 4 steps from minus 3 and 4 steps from 5. Equally far is not closer, so 1 is not counted.")),
    B("1 is a tie, so it is out. We want the integers to the left of 1, and greater than minus 10. Here they are.",
      LB("l4", "−9, −8, −7, −6, −5, −4, −3, −2, −1, 0")),
    B("Minus 10 itself is not included, because greater than minus 10 starts at minus 9. And do not forget 0 at the other end.",
      UL("l4", "−9"), UL("l4", "0")),
    B("Count them: 9 negative integers, from minus 9 to minus 1, and then 0. 9 plus 1 is 10.",
      *ANSC("l5", "9 + 1 = 10", 10)),
    B("Check 0: it is 3 steps from minus 3 and 5 steps from 5, so it really is closer to minus 3."),
    B("So find the halfway point, leave the tie out, and count carefully at both ends. There are 10 integers."),
)

# The frog in the well.
LESSONS["G5A_INTEGERS_010"] = LESSON(
    B("A frog is at the bottom of a well, 10 metres below the ground, at minus 10. Each day it climbs 4 metres, and each night it slips down 2 metres. During which day does it first reach ground level?",
      GIVEN("q", "Start −10. Day: up 4. Night: down 2")),
    B("A quick thought: up 4 and down 2 is a gain of 2 each day, and 10 divided by 2 is 5. So is it the 5th day?",
      W("l1", "4 − 2 = 2"), W("l2", "10 ÷ 2 = 5"),
      ask=CHOOSE(["yes, the 5th day", "not sure: follow the frog"], 1,
                 "The gain of 2 is for a whole day and night. But the frog could reach the top during a day's climb, before the night's slip. So follow it step by step.")),
    B("Let's follow the frog. Day 1: it climbs from minus 10 to minus 6. That night it slips back to minus 8.",
      W("d1", "−10 + 4 = −6"), W("n1", "−6 − 2 = −8")),
    B("Day 2: it climbs from minus 8 to minus 4, then slips to minus 6.",
      W("d2", "−8 + 4 = −4"), W("n2", "−4 − 2 = −6")),
    B("Day 3: it climbs from minus 6 to minus 2, then slips to minus 4.",
      W("d3", "−6 + 4 = −2"), W("n3", "−2 − 2 = −4")),
    B("Day 4 begins at minus 4, and the frog climbs 4 metres. Where does it get to?",
      ask=CHOOSE(["−2", "0: ground level", "2"], 1,
                 "Minus 4 is 4 metres below the ground. Climbing 4 metres brings the frog exactly up to 0.")),
    B("Minus 4 plus 4 is 0. The frog is out, during the 4th day, before any slipping that night.",
      W("d4", "−4 + 4 = 0"), *ANSLC("a", "ground level on the 4th day", "4th")),
    B("So the quick thought was a trap. On its last day the frog reaches the top and does not slip back."),
    B("For climb and slip stories, follow the position after each climb and each slip. The frog first reaches the ground on the 4th day."),
)

# Greatest of −9, −4, −6, −12 (warm-up).
LESSONS["G5A_INTEGERS_011"] = LESSON(
    B("Which of these integers is the greatest: minus 9, minus 4, minus 6 or minus 12?",
      GIVEN("q", "Greatest:  −9,  −4,  −6,  −12")),
    B("Picture the number line. Numbers get greater as you move to the right. Here are our four in order, with 0 at the right-hand end.",
      LB("l1", "−12   −9   −6   −4   0")),
    B("All four are to the left of zero. Which one is nearest to zero?",
      ask=CHOOSE(["−12", "−9", "−4"], 2,
                 "Count the steps back to zero. Minus 4 needs only 4 steps, fewer than any of the others.")),
    B("Minus 4 is only 4 steps from zero, so it is the furthest to the right.",
      CIRC("l1", "−4")),
    B("So the greatest is minus 4.",
      *ANSLC("l2", "−4 is the greatest", "−4")),
    B("The trap is minus 12, because 12 is the biggest number we can see. But minus 12 is furthest to the left, so it is the smallest.",
      UL("l1", "−12")),
    B("So with negative numbers, the one nearest to zero is the greatest. Here that is minus 4."),
)

# 5 degrees below zero (warm-up).
LESSONS["G5A_INTEGERS_012"] = LESSON(
    B("A thermometer in Kargil shows 5 degrees below zero. How is this temperature written?",
      GIVEN("q", "5 degrees below zero = ?")),
    B("A thermometer is a number line standing up. Zero is the starting point. Above zero we count 1, 2, 3 upwards.",
      LB("l1", "0°C: the starting point")),
    B("Below zero we count downwards. What do we put in front of a number to show it is below zero?",
      ask=CHOOSE(["a plus sign", "a minus sign", "a zero"], 1,
                 "Numbers below zero are negative numbers, and we show that with a minus sign in front.")),
    B("A minus sign. So 5 degrees below zero is written minus 5 degrees Celsius.",
      *ANSLC("l2", "5 below zero = −5°C", "−5°C")),
    B("Check: start at minus 5 and warm up by 5 degrees. We are back at zero.",
      W("l3", "−5 + 5 = 0")),
    B("Careful: 5 without the sign would mean 5 degrees above zero, a much warmer day. The minus sign tells us which side of zero we are on."),
    B("So below zero means a minus sign in front. 5 degrees below zero is minus 5 degrees."),
)
