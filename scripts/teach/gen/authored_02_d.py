"""authored-02, fourth group: fractions 006 to 009 and integers 001 to 004."""
from authored_02_lib import ANS, ANSC, ANSLC, B, CHOOSE, CIRC, GIVEN, LB, LESSON, STRIKE, W

LESSONS = {}

# Tap fills in 4 hours, drain empties in 6 hours.
LESSONS["G5A_FRACTIONS_006"] = LESSON(
    B("A tap fills an empty tank in 4 hours. A drain can empty the full tank in 6 hours. The tank is empty, and both are left open. How long will the tank take to fill?",
      GIVEN("q", "Tap fills in 4 hours. Drain empties in 6 hours")),
    B("The hours themselves cannot be added or subtracted. Instead, ask what happens in 1 hour. What fraction of the tank does the tap fill in 1 hour?",
      ask=CHOOSE(["1/4 of the tank", "4 tanks", "1/6 of the tank"], 0,
                 "The tap needs 4 equal hours for the whole tank. So in 1 hour it fills one of 4 equal parts: 1 over 4.")),
    B("In 1 hour the tap pours in 1 over 4 of the tank. In the same hour the drain lets out 1 over 6 of the tank.",
      LB("l1", "in: 1/4 each hour     out: 1/6 each hour")),
    B("Water comes in and water goes out. So what do we do with 1 over 4 and 1 over 6?",
      ask=CHOOSE(["add them", "subtract them"], 1,
                 "The drain takes water away, so it works against the tap. What stays in the tank is what came in, take away what went out.")),
    B("Subtract. In twelfths, 1 over 4 is 3 over 12, and 1 over 6 is 2 over 12. 3 over 12 minus 2 over 12 is 1 over 12.",
      W("l2", "1/4 − 1/6 = 3/12 − 2/12 = 1/12")),
    B("So each hour the tank gains just 1 over 12 of a tankful. 12 lots of 1 over 12 make the whole tank, so it needs 12 hours.",
      ANS("l3", "12 × 1/12 = 1"), CIRC("l3", "12")),
    B("12 hours is much longer than the tap's 4 hours. That makes sense, because the drain is fighting the tap."),
    B("The traps: 4 plus 6 is 10, and 6 minus 4 is 2. But 2 hours would be faster than the tap alone with no drain at all!",
      W("l4", "4 + 6 = 10"), W("l5", "6 − 4 = 2")),
    B("So for filling and draining, turn each time into a fraction for 1 hour, subtract, and see how many hours make the whole. Here it is 12 hours."),
)

# 1 to 30: multiples of 2 or 3.
LESSONS["G5A_FRACTIONS_007"] = LESSON(
    B("Look at the whole numbers from 1 to 30. What fraction of them are multiples of 2, or multiples of 3, or both?",
      GIVEN("q", "1 to 30: multiples of 2 or 3 (or both)?")),
    B("Count the multiples of 2 first. Every second number is one, so 30 divided by 2 gives 15.",
      W("l1", "30 ÷ 2 = 15")),
    B("Now the multiples of 3. Every third number is one, so 30 divided by 3 gives 10.",
      W("l2", "30 ÷ 3 = 10")),
    B("15 and 10. Can we just add them and say 25?",
      W("l3", "15 + 10 = 25"),
      ask=CHOOSE(["yes, 25 numbers", "no, some are counted twice"], 1,
                 "Think about 6. It is a multiple of 2, so it is in the first count. It is a multiple of 3 as well, so it is in the second count too.")),
    B("Numbers like 6 are in both lists, so they were counted twice. Those are the multiples of 6: 6, 12, 18, 24 and 30. There are 5 of them.",
      LB("l4", "6, 12, 18, 24, 30"), W("l5", "30 ÷ 6 = 5")),
    B("Each of those 5 was counted twice, so take 5 away once. 25 minus 5 is 20.",
      W("l6", "25 − 5 = 20")),
    B("So 20 of the 30 numbers fit. As a fraction that is 20 over 30. Divide top and bottom by 10, and we get 2 over 3.",
      *ANSC("l7", "20/30 = 2/3", "2/3")),
    B("The trap is 25 over 30, which is 5 over 6. That counts the multiples of 6 twice.",
      W("l8", "25/30 = 5/6")),
    B("So for this OR that: add the two counts, then take away the ones in both lists. The answer is 2 over 3."),
)

# 2/3 of the boys and 3/4 of the girls, 36 in all.
LESSONS["G5A_FRACTIONS_008"] = LESSON(
    B("2 over 3 of the boys and 3 over 4 of the girls of Class 5 went on a picnic. The same number of boys and girls went, and 36 children went in all. How many children are in Class 5?",
      GIVEN("q", "2/3 of boys = 3/4 of girls. 36 went in all")),
    B("The two fractions belong to two different groups, so we cannot use them on 36 directly. Start with what we can find: how many boys went?",
      ask=CHOOSE(["36", "18", "24"], 1,
                 "36 children went, and the boys and girls who went are equal in number. So split 36 into two equal halves.")),
    B("36 divided by 2 is 18. So 18 boys went, and 18 girls went.",
      W("l1", "36 ÷ 2 = 18")),
    B("Now the boys. 18 is 2 over 3 of all the boys. So 2 parts are 18, and 1 part is 9.",
      W("l2", "18 ÷ 2 = 9")),
    B("All the boys are 3 parts. 3 times 9 is 27 boys.",
      W("l3", "3 × 9 = 27"), W("l3b", "2/3 of 27 = 18")),
    B("Now the girls. 18 is 3 over 4 of all the girls. So 3 parts are 18. How big is 1 part?",
      ask=CHOOSE(["18 ÷ 4", "18 ÷ 3", "18 × 3"], 1,
                 "The 18 girls who went are 3 of the 4 parts. So share 18 among those 3 parts.")),
    B("18 divided by 3 is 6. All the girls are 4 parts, and 4 times 6 is 24 girls.",
      W("l4", "18 ÷ 3 = 6"), W("l5", "4 × 6 = 24")),
    B("The whole class is the boys and the girls together. 27 plus 24 is 51.",
      *ANSC("l6", "27 + 24 = 51", 51)),
    B("Check: 9 boys and 6 girls stayed behind, which is 15. And 36 plus 15 is 51.",
      W("l7", "9 + 6 = 15"), W("l8", "36 + 15 = 51")),
    B("The trap is to treat 36 as a fraction of the whole class. Each fraction belongs to its own group, so find each group on its own. The class has 51 children."),
)

# Equivalent to 3/5, top + bottom = 72.
LESSONS["G5A_FRACTIONS_009"] = LESSON(
    B("A fraction is equivalent to 3 over 5. Its numerator and denominator add up to 72. What is its denominator?",
      GIVEN("q", "Equivalent to 3/5. Top + bottom = 72")),
    B("Fractions equivalent to 3 over 5 are made by multiplying the top and the bottom by the same number: 6 over 10, 9 over 15, and so on.",
      W("l1", "3/5 = 6/10 = 9/15")),
    B("In every one, the top is 3 equal parts and the bottom is 5 of the same parts. How many parts is that altogether?",
      ask=CHOOSE(["8 parts", "15 parts", "2 parts"], 0,
                 "The top has 3 parts and the bottom has 5. Together, 3 plus 5 makes 8 parts.")),
    B("3 plus 5 is 8 parts, and those 8 parts add up to 72. So one part is 72 divided by 8, which is 9.",
      W("l2", "3 + 5 = 8"), W("l3", "72 ÷ 8 = 9")),
    B("The top is 3 parts: 3 times 9 is 27. The bottom is 5 parts: 5 times 9 is 45.",
      W("l4", "3 × 9 = 27"), W("l5", "5 × 9 = 45")),
    B("So the fraction is 27 over 45, and its denominator is 45.",
      *ANSC("l6", "3/5 = 27/45", "45")),
    B("Check: 27 plus 45 is 72. And careful: 27 is among the choices, but that is the numerator, the top.",
      W("l7", "27 + 45 = 72")),
    B("So think of an equivalent fraction as equal parts: add the parts, find one part, then build the top and the bottom. The denominator is 45."),
)

# 25 copies of −1 and 24 copies of −1.
LESSONS["G5A_INTEGERS_001"] = LESSON(
    B("Meena multiplies 25 copies of minus 1 together. Kabir multiplies 24 copies of minus 1 together. What is the sum of their two answers?",
      GIVEN("q", "Meena: 25 copies of −1. Kabir: 24 copies of −1")),
    B("Nobody wants to multiply 25 times! Start small and watch the sign. Two copies: minus 1 times minus 1 is plus 1.",
      W("l1", "(−1) × (−1) = 1")),
    B("Three copies: that plus 1, times one more minus 1, flips back to minus 1. Four copies flips again, to plus 1.",
      W("l2", "(−1) × (−1) × (−1) = −1"), W("l3", "(−1) × (−1) × (−1) × (−1) = 1")),
    B("See the pattern? Every pair of minus ones makes plus 1. So what do an even number of copies multiply to?",
      ask=CHOOSE(["1", "−1", "0"], 0,
                 "An even number of copies can be put into pairs with none left over. Each pair makes plus 1, and ones multiplied together stay 1.")),
    B("Kabir has 24 copies. 24 is even: it makes 12 pairs, and each pair is plus 1. So Kabir's answer is 1.",
      W("l4", "24 ÷ 2 = 12"), LB("l5", "Kabir: 1")),
    B("Meena has 25 copies. That is 12 pairs and one more minus 1 left over. So Meena's answer is minus 1.",
      W("l6", "25 = 12 × 2 + 1"), LB("l7", "Meena: −1")),
    B("Now add the two answers. Minus 1 plus 1 is 0.",
      *ANSC("l8", "(−1) + 1 = 0", 0)),
    B("The trap is to add the copies and get minus 25 and minus 24. But the copies are multiplied, and multiplying by minus 1 only flips the sign."),
    B("So with copies of minus 1: an even number gives 1, an odd number gives minus 1. Here the sum is 0."),
)

# Product positive, sum −12: the greater integer.
LESSONS["G5A_INTEGERS_002"] = LESSON(
    B("The product of two integers is positive, and their sum is minus 12. Which of these could be the greater of the two: minus 5, minus 7, 2 or minus 13?",
      GIVEN("q", "product positive, sum = −12. The greater one?"), LB("o", "−5,  −7,  2,  −13")),
    B("Start with the product. When is a product positive?",
      ask=CHOOSE(["both have the same sign", "they have different signs"], 0,
                 "Plus times plus is plus, and minus times minus is plus too. Different signs give a minus. So for a positive product, the signs match.")),
    B("Same signs, then: both positive or both negative. But two positive numbers could never add up to minus 12. So both are negative.",
      LB("l1", "both negative")),
    B("That rules out 2. And minus 13? Its partner would have to be 1 to make minus 12, and 1 is positive. So minus 13 is out as well.",
      STRIKE("o", "2"), W("l2", "−13 + 1 = −12"), STRIKE("o", "−13")),
    B("That leaves minus 5 and minus 7. And look: they are partners. Minus 5 plus minus 7 is minus 12, and their product is 35, which is positive.",
      W("l3", "(−5) + (−7) = −12"), W("l4", "(−5) × (−7) = 35")),
    B("So the pair is minus 5 and minus 7. Which one is the greater?",
      ask=CHOOSE(["−7", "−5"], 1,
                 "On the number line, the greater number is further to the right. Minus 5 is closer to zero than minus 7, so it sits to the right.")),
    B("Minus 5 is to the right of minus 7 on the number line, so minus 5 is the greater.",
      *ANSC("l5", "−5 > −7", "−5")),
    B("The trap is minus 7. 7 is bigger than 5, but with negative numbers it turns round: the one nearer to zero is greater."),
    B("So read the signs from the product and the sum, find the pair, then use the number line to pick the greater. It is minus 5."),
)

# P at −8, Q 5 away, R 12 away: greatest distance of R from 0.
LESSONS["G5A_INTEGERS_003"] = LESSON(
    B("Point P is at minus 8 on a number line. Q is 5 units away from P. R is 12 units away from Q. What is the greatest possible distance of R from 0?",
      GIVEN("q", "P at −8. Q is 5 from P. R is 12 from Q")),
    B("The key words are away from. We are not told which way. So where could Q be?",
      ask=CHOOSE(["only at −3", "only at −13", "at −13 or at −3"], 2,
                 "Away can mean to the left or to the right. 5 to the left of minus 8 is minus 13, and 5 to the right is minus 3.")),
    B("Q could be 5 to the left, at minus 13, or 5 to the right, at minus 3.",
      W("l1", "−8 − 5 = −13"), W("l2", "−8 + 5 = −3")),
    B("From each of those, R goes 12 left or 12 right. From minus 13: R is at minus 25, or at minus 1.",
      W("l3", "−13 − 12 = −25"), W("l4", "−13 + 12 = −1")),
    B("From minus 3: R is at minus 15, or at 9.",
      W("l5", "−3 − 12 = −15"), W("l6", "−3 + 12 = 9")),
    B("Four places for R: minus 25, minus 1, minus 15 and 9. Which one is furthest from 0?",
      ask=CHOOSE(["9", "−25", "−15"], 1,
                 "Distance from 0 does not care about the side. Minus 25 is 25 steps from 0, and that is more than 15 or 9.")),
    B("Minus 25 is 25 units from 0. That is the greatest distance.",
      *ANSLC("l7", "R at −25: 25 units from 0", "25")),
    B("The trap is to go right both times and land on 9. P starts on the left of 0, so going left both times carries R furthest away."),
    B("So when a question says away from, try both directions every time, then compare the distances. The greatest is 25."),
)

# Ant at −14 and beetle at 6 walk towards each other.
LESSONS["G5A_INTEGERS_004"] = LESSON(
    B("An ant is at minus 14 and a beetle is at 6 on a number line. They walk towards each other. Each second the ant moves 3 units and the beetle moves 1 unit. Where do they meet?",
      GIVEN("q", "Ant at −14 (3 a second). Beetle at 6 (1 a second)")),
    B("First, how far apart are they? From minus 14 up to 0 is 14 units, and from 0 to 6 is 6 more. 14 plus 6 is 20.",
      W("l1", "14 + 6 = 20")),
    B("Each second the ant comes 3 closer and the beetle comes 1 closer. So how much does the gap shrink each second?",
      ask=CHOOSE(["by 2 units", "by 3 units", "by 4 units"], 2,
                 "Both are walking towards each other, so both help to close the gap. 3 from the ant and 1 from the beetle make 4.")),
    B("The gap closes by 4 each second. 20 divided by 4 is 5, so they meet after 5 seconds.",
      W("l2", "3 + 1 = 4"), W("l3", "20 ÷ 4 = 5")),
    B("Careful: 5 is the time, not the place. We want the point. How far has the ant walked in 5 seconds?",
      ask=CHOOSE(["5 units", "15 units", "20 units"], 1,
                 "The ant moves 3 units every second. In 5 seconds that is 5 lots of 3.")),
    B("5 times 3 is 15. The ant starts at minus 14 and walks 15 to the right. 14 steps bring it to 0, and 1 more step takes it to 1.",
      W("l4", "5 × 3 = 15"), *ANSC("l5", "−14 + 15 = 1", "1")),
    B("Check with the beetle. It walks 5 units to the left from 6, and 6 minus 5 is 1. They are at the same point.",
      W("l6", "6 − 5 = 1")),
    B("The trap is the halfway point, minus 4. They would meet there only if they walked equally fast, and the ant is faster.",
      W("l7", "−14 + 10 = −4")),
    B("So find the gap, find how fast it closes, get the time, and then walk one of them forward. They meet at 1."),
)
