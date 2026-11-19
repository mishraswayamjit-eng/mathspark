"""authored-02, sixth group: integers 013 to 020 (all warm-ups, so short lessons)."""
from authored_02_lib import ANSC, ANSLC, B, CHOOSE, CIRC, GIVEN, LB, LESSON, STRIKE, UL, W

LESSONS = {}

# The opposite of −8.
LESSONS["G5A_INTEGERS_013"] = LESSON(
    B("What is the opposite of minus 8?",
      GIVEN("q", "opposite of −8 = ?")),
    B("Find minus 8 on the number line. It is 8 steps to the left of zero.",
      LB("l1", "−8 ........ 0 ........ 8"), UL("l1", "−8")),
    B("The opposite of a number is the same distance from zero, on the other side. So where is the opposite of minus 8?",
      ask=CHOOSE(["8 steps right of zero", "8 steps left of zero", "at zero"], 0,
                 "Minus 8 is on the left of zero. Its opposite must be on the other side, the right, and just as far away: 8 steps.")),
    B("8 steps to the right of zero is 8. So the opposite of minus 8 is 8.",
      *ANSLC("l2", "opposite of −8 = 8", "8")),
    B("Check: a number and its opposite always add up to zero. Minus 8 plus 8 is 0.",
      W("l3", "−8 + 8 = 0")),
    B("A trap is 16. That is the distance from minus 8 all the way to 8, not the opposite itself.",
      W("l4", "8 + 8 = 16")),
    B("So to find an opposite, keep the distance from zero and switch sides. The opposite of minus 8 is 8."),
)

# (−6) + 9.
LESSONS["G5A_INTEGERS_014"] = LESSON(
    B("Work out minus 6 plus 9.",
      W("q", "(−6) + 9 = ?", "given")),
    B("Use the number line. We start at minus 6. Adding a positive number means moving to the right, so we take 9 steps to the right.",
      LB("l1", "start at −6, move 9 steps right")),
    B("Do it in two parts. How many steps does it take to get from minus 6 up to zero?",
      ask=CHOOSE(["6 steps", "9 steps", "3 steps"], 0,
                 "Minus 6 is 6 steps to the left of zero. So it takes 6 steps to walk back to zero.")),
    B("6 steps reach zero. We have 9 steps in all, so 9 minus 6 leaves 3 steps still to go.",
      W("l2", "−6 + 6 = 0"), W("l3", "9 − 6 = 3")),
    B("Those 3 steps carry on to the right of zero, and land on 3.",
      *ANSC("l4", "(−6) + 9 = 3", 3)),
    B("Two things to watch. 6 plus 9 is 15, but our 6 was a minus 6. And the answer is plus 3, not minus 3, because 9 steps are enough to get past zero.",
      W("l5", "6 + 9 = 15")),
    B("So to add to a negative number, walk right: first to zero, then on with the steps that are left. Minus 6 plus 9 is 3."),
)

# 4 − 10.
LESSONS["G5A_INTEGERS_015"] = LESSON(
    B("Work out 4 minus 10.",
      W("q", "4 − 10 = ?", "given")),
    B("Use the number line. We start at 4. Subtracting means moving to the left, so we take 10 steps to the left.",
      LB("l1", "start at 4, move 10 steps left")),
    B("We are taking away more than we have. So where will we end up?",
      ask=CHOOSE(["above zero", "at zero", "below zero"], 2,
                 "From 4 it takes only 4 steps to reach zero. We have 10 steps, so we keep going past zero, to the left.")),
    B("4 steps take us down to zero. 10 minus 4 leaves 6 steps still to go.",
      W("l2", "4 − 4 = 0"), W("l3", "10 − 4 = 6")),
    B("Those 6 steps go below zero, and land on minus 6.",
      *ANSC("l4", "4 − 10 = −6", "−6")),
    B("Careful: the answer is not plain 6. That would be 10 minus 4. Here we went past zero, so the sign is minus."),
    B("So when you take away more than you have, walk left through zero and count what is left. 4 minus 10 is minus 6."),
)

# −2°C rises by 7°C.
LESSONS["G5A_INTEGERS_016"] = LESSON(
    B("Early in the morning the temperature in Shimla was minus 2 degrees. By noon it had risen by 7 degrees. What was the temperature at noon?",
      GIVEN("q", "Morning: −2°C. Rises by 7°C. Noon = ?")),
    B("A thermometer is a number line standing up. A rise means going up, so we start at minus 2 and climb 7 degrees.",
      W("l1", "−2 + 7 = ?")),
    B("How many of those 7 degrees are used up just getting to zero?",
      ask=CHOOSE(["2 degrees", "7 degrees", "5 degrees"], 0,
                 "Minus 2 is 2 degrees below zero. So the first 2 degrees of the rise bring it up to zero.")),
    B("2 degrees reach zero. 7 minus 2 leaves 5 degrees still to climb.",
      W("l2", "7 − 2 = 5")),
    B("So the temperature climbs 5 degrees above zero. At noon it was 5 degrees.",
      *ANSC("l3", "−2 + 7 = 5", 5)),
    B("The trap is 2 plus 7, which is 9. But the morning was 2 below zero, so part of the rise is spent reaching zero.",
      W("l4", "2 + 7 = 9")),
    B("So for a rise from below zero, climb to zero first, then count on. The noon temperature was 5 degrees."),
)

# Which statement is true?
LESSONS["G5A_INTEGERS_017"] = LESSON(
    B("Which of these statements is true? Here are the four.",
      GIVEN("a", "−5 > −2"), GIVEN("b", "−5 = 5"), GIVEN("c", "−5 < −2"), GIVEN("d", "0 < −2")),
    B("Remember how to read the signs: the wide, open end faces the bigger number, and the small pointed end points at the smaller one."),
    B("The statements use minus 5, minus 2, 0 and 5. Let's put the first three on a number line.",
      LB("l1", "−5   −4   −3   −2   −1   0")),
    B("On the number line, the number further to the left is the smaller one. Which is smaller, minus 5 or minus 2?",
      ask=CHOOSE(["−5 is smaller", "−2 is smaller"], 0,
                 "Minus 5 is further to the left than minus 2. Further left means smaller, even though 5 is bigger than 2.")),
    B("Minus 5 is further left, so minus 5 is less than minus 2. That is the true statement.",
      CIRC("l1", "−5"), *ANSC("l2", "−5 < −2", "−5 < −2")),
    B("Now the others. Minus 5 is not greater than minus 2. Minus 5 and 5 are on opposite sides of zero, so they are not equal. And 0 is to the right of minus 2, so 0 is greater.",
      STRIKE("a", "−5 > −2"), STRIKE("b", "−5 = 5"), STRIKE("d", "0 < −2")),
    B("The trap is thinking that 5 is bigger than 2, so minus 5 must be bigger than minus 2. With negative numbers it turns round."),
    B("So put the numbers on a number line: left is less. Minus 5 is less than minus 2."),
)

# 3 units to the left of 1.
LESSONS["G5A_INTEGERS_018"] = LESSON(
    B("On a number line, which integer is 3 units to the left of 1?",
      GIVEN("q", "3 units to the left of 1 = ?")),
    B("Here is a piece of the number line, with 1 near the right-hand end.",
      LB("l1", "−3   −2   −1   0   1   2"), UL("l1", "1", 2)),
    B("Start at 1 and take one step left at a time. The first step lands on 0. Where does the second step land?",
      ask=CHOOSE(["−1", "1", "−2"], 0,
                 "After 0, the next number to the left is minus 1. The steps carry on past zero into the negative numbers.")),
    B("Step 1 lands on 0, step 2 on minus 1, and step 3 on minus 2.",
      CIRC("l1", "−2")),
    B("As a subtraction, moving 3 to the left of 1 is 1 take away 3, which is minus 2.",
      *ANSC("l2", "1 − 3 = −2", "−2")),
    B("Careful to start counting from 1, not from 0. And going right instead would give 4, which is bigger, not smaller.",
      W("l3", "1 + 3 = 4")),
    B("So moving left means subtracting, and the steps can go straight through zero. 3 to the left of 1 is minus 2."),
)

# A lift on floor −2 goes up 5 floors.
LESSONS["G5A_INTEGERS_019"] = LESSON(
    B("The ground floor of a building is floor 0. A lift is on floor minus 2, two floors below the ground. It goes up 5 floors. Which floor is it on now?",
      GIVEN("q", "Lift on floor −2. Up 5 floors = ?")),
    B("Think of the floors as a number line standing up. Going up means adding, so this is minus 2 plus 5.",
      W("l1", "−2 + 5 = ?")),
    B("Count the floors as the lift passes them. The first floor it reaches is minus 1. What is the second?",
      ask=CHOOSE(["floor 0", "floor 1", "floor −2"], 0,
                 "Above minus 1 comes the ground floor, which is floor 0 in this building. It counts as a floor like any other.")),
    B("So the lift reaches minus 1, then 0, then 1, 2 and 3. That is 5 floors.",
      LB("l2", "−1, 0, 1, 2, 3"), CIRC("l2", "3")),
    B("The lift stops on floor 3.",
      *ANSC("l3", "−2 + 5 = 3", 3)),
    B("The trap is 2 plus 5, which is 7. The lift started 2 floors below the ground, so 2 of its 5 floors only bring it up to floor 0.",
      W("l4", "2 + 5 = 7")),
    B("So going up from below zero: reach zero first, then count on. Minus 2 plus 5 is 3."),
)

# The coldest temperature.
LESSONS["G5A_INTEGERS_020"] = LESSON(
    B("Which of these temperatures is the coldest: minus 1 degree, minus 10 degrees, 2 degrees or 0 degrees?",
      GIVEN("q", "Coldest:  −1°C,  −10°C,  2°C,  0°C")),
    B("Colder means lower on the thermometer. On a number line, that is further to the left."),
    B("Two of them are below zero: minus 1 and minus 10. Which is further below zero?",
      ask=CHOOSE(["−1", "−10"], 1,
                 "Minus 1 is just 1 step below zero. Minus 10 is 10 steps below, so it is much further down.")),
    B("Minus 10 is 10 steps below zero. Here are all four in order, from lowest to highest.",
      LB("l1", "−10   −1   0   2"), W("l1b", "−10 < −1 < 0 < 2")),
    B("So the coldest is minus 10 degrees.",
      CIRC("l1", "−10"), *ANSLC("l2", "coldest: −10°C", "−10°C")),
    B("The trap is minus 1, because it has a minus sign and 1 looks small. But minus 1 is only just below zero, so it is warmer than minus 10."),
    B("So the coldest temperature is the lowest number, the one furthest below zero. Here that is minus 10 degrees."),
)
