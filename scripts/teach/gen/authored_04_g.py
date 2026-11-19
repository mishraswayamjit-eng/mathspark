"""Ratio, proportion and variation 009 to 015, written one by one."""
from authored_04_lib import ANSC, ANSL, B, BOX, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, STRIKE, UL, W  # noqa: F401

LESSONS = {}

# Taxi: 5 km costs 110, 8 km costs 155; 12 km?
LESSONS["G5A_VARIATION_009"] = LESSON(
    B("A taxi charges a fixed amount for every trip, plus the same amount for each kilometre. 5 kilometres cost 110 rupees and 8 kilometres cost 155 rupees. What do 12 kilometres cost?",
      GIVEN("q", "Fixed amount + per km. 5 km: ₹110. 8 km: ₹155. 12 km?")),
    B("Every fare has the fixed amount hidden inside it. So we cannot just divide 110 by 5. That is the trap. Instead, compare the two trips."),
    B("The second trip is 8 minus 5, that is 3 kilometres longer. And it costs 155 minus 110, that is 45 rupees more.",
      W("l1", "8 − 5 = 3"), W("l2", "155 − 110 = 45")),
    B("The fixed amount is the same in both trips. So what are those extra 45 rupees paying for?",
      ask=CHOOSE(["the fixed amount", "the 3 extra kilometres", "all 8 kilometres"], 1,
                 "Both trips include the same fixed amount, so it drops out when we compare them. The only difference is the 3 extra kilometres.")),
    B("Just the 3 extra kilometres. So 1 kilometre costs 45 divided by 3, which is 15 rupees.",
      W("l3", "45 ÷ 3 = 15"), NOTE("l3", "15", "rupees per km")),
    B("Now the fixed amount. In the 5 kilometre trip, the kilometres cost 5 times 15, which is 75. And 110 minus 75 leaves 35 rupees fixed.",
      W("l4", "5 × 15 = 75"), W("l5", "110 − 75 = 35"), NOTE("l5", "35", "fixed")),
    B("For 12 kilometres, the kilometres cost 12 times 15, which is 180 rupees.",
      W("l6", "12 × 15 = 180")),
    B("Add the fixed 35. 180 plus 35 is 215. The 12 kilometre trip costs 215 rupees.",
      *ANSC("l7", "180 + 35 = 215", 215)),
    B("Check with the 8 kilometre trip: 8 times 15 is 120, and 120 plus 35 is 155. That matches the fare we were told.",
      W("l8", "8 × 15 = 120"), W("l9", "120 + 35 = 155")),
    B("So when a price has a fixed part, compare two cases to find the cost of one more, then work back to the fixed part."),
)

# 30 litres, milk : water = 7 : 3; add water to make 3 : 2.
LESSONS["G5A_VARIATION_010"] = LESSON(
    B("A 30 litre mixture has milk and water in the ratio 7 to 3. How many litres of water must be added to make the ratio of milk to water 3 to 2?",
      GIVEN("q", "30 litres, milk : water = 7 : 3. Add water → 3 : 2.")),
    B("First turn the ratio into litres. 7 plus 3 is 10 parts, and they make 30 litres. So 1 part is 3 litres.",
      W("l1", "7 + 3 = 10"), W("l2", "30 ÷ 10 = 3")),
    B("Milk is 7 parts: 7 times 3 is 21 litres. Water is 3 parts: 3 times 3 is 9 litres.",
      W("l3", "7 × 3 = 21"), NOTE("l3", "21", "litres of milk"), W("l4", "3 × 3 = 9"), NOTE("l4", "9", "litres of water")),
    B("We add only water. So what stays the same?",
      ask=CHOOSE(["the milk, 21 litres", "the total, 30 litres", "the water, 9 litres"], 0,
                 "Pouring in water makes the water grow, and the total grows with it. Nothing touches the milk, so it stays at 21 litres.")),
    B("The milk stays at 21 litres. That is the key. The trap is to keep the total at 30, but the total grows as the water goes in."),
    B("In the new ratio, 3 to 2, the milk is the 3 parts. So 3 parts are 21 litres, and 1 part is 21 divided by 3, which is 7 litres.",
      W("l5", "21 ÷ 3 = 7")),
    B("The water must be 2 parts. 2 times 7 is 14 litres of water in all.",
      W("l6", "2 × 7 = 14")),
    B("But 9 litres of water are already there. 14 minus 9 is 5. So 5 litres of water must be added.",
      *ANSC("l7", "14 − 9 = 5", 5)),
    B("Check: 21 litres of milk to 14 litres of water. Divide both by 7 and you get 3 to 2.",
      W("l8", "21 ÷ 7 = 3"), W("l9", "14 ÷ 7 = 2")),
    B("So find what does not change, here the milk, and build the new ratio around it. Then take away what was already there."),
)

# Jar P: 20 litres 3 : 1. Jar Q: 30 litres 2 : 3. Mixed.
LESSONS["G5A_VARIATION_011"] = LESSON(
    B("Jar P holds 20 litres of milk and water in the ratio 3 to 1. Jar Q holds 30 litres in the ratio 2 to 3. Both are emptied into a drum. What is the ratio of milk to water there?",
      GIVEN("q", "P: 20 litres, 3 : 1. Q: 30 litres, 2 : 3. Milk : water?")),
    B("The jars hold different amounts, so we cannot just add the ratio numbers. That is the trap. We have to work in litres."),
    B("Jar P: 3 plus 1 is 4 parts, making 20 litres, so 1 part is 5 litres. Milk is 3 times 5, which is 15 litres, and water is 5 litres.",
      W("l1", "3 + 1 = 4"), W("l2", "20 ÷ 4 = 5"), W("l3", "3 × 5 = 15")),
    B("Jar Q holds 30 litres in the ratio 2 to 3. How many litres is 1 part?",
      ask=CHOOSE(["30 ÷ 2 = 15", "30 ÷ 3 = 10", "30 ÷ 5 = 6"], 2,
                 "Count all the parts first. 2 parts of milk and 3 parts of water make 5 parts, and those 5 parts are the 30 litres.")),
    B("2 plus 3 is 5 parts, so 1 part is 30 divided by 5, which is 6 litres. Milk is 2 times 6, which is 12. Water is 3 times 6, which is 18.",
      W("l4", "2 + 3 = 5"), W("l5", "30 ÷ 5 = 6"), W("l6", "2 × 6 = 12"), W("l7", "3 × 6 = 18")),
    B("Now pour both into the drum. Milk: 15 plus 12 is 27 litres. Water: 5 plus 18 is 23 litres.",
      W("l8", "15 + 12 = 27"), W("l9", "5 + 18 = 23")),
    B("So milk to water is 27 to 23. No number divides both, so that is the ratio.",
      *ANSL("a", "Milk : water = 27 : 23", "27 : 23")),
    B("Mind the order: milk first, then water. 23 to 27 would be water to milk."),
    B("Check the total: 27 plus 23 is 50 litres, and the jars held 20 plus 30, which is 50 as well.",
      W("l10", "27 + 23 = 50"), W("l11", "20 + 30 = 50")),
    B("So to mix two mixtures, change each ratio into litres, add the milk, add the water, and only then write the ratio: 27 to 23."),
)

# Coins 1, 2, 5 rupees in the ratio 5 : 3 : 2, worth 210: how many 5-rupee coins?
LESSONS["G5A_VARIATION_012"] = LESSON(
    B("A money box has 1 rupee, 2 rupee and 5 rupee coins, in the ratio 5 to 3 to 2. All the coins together are worth 210 rupees. How many 5 rupee coins are there?",
      GIVEN("q", "₹1, ₹2, ₹5 coins in ratio 5 : 3 : 2. Value ₹210. ₹5 coins?")),
    B("Careful: the ratio counts coins, but 210 is a value in rupees. So we cannot share the 210 in the ratio 5 to 3 to 2. That is the trap."),
    B("Instead, make one small group of coins: 5 coins of 1 rupee, 3 coins of 2 rupees, and 2 coins of 5 rupees.",
      LB("l1", "Group: 5 × ₹1,  3 × ₹2,  2 × ₹5")),
    B("How much is one group worth?",
      ask=CHOOSE(["10 rupees", "21 rupees", "8 rupees"], 1,
                 "Add up the values, not the number of coins. 5 coins of 1 rupee are worth 5, 3 coins of 2 rupees are worth 6, and 2 coins of 5 rupees are worth 10.")),
    B("5 times 1 is 5, 3 times 2 is 6, and 2 times 5 is 10. Then 5 plus 6 plus 10 is 21. One group is worth 21 rupees.",
      W("l2", "5 × 1 = 5"), W("l3", "3 × 2 = 6"), W("l4", "2 × 5 = 10"), W("l5", "5 + 6 + 10 = 21")),
    B("The whole box is worth 210 rupees. 210 divided by 21 is 10, so there are 10 groups.",
      W("l6", "210 ÷ 21 = 10"), NOTE("l6", "10", "groups")),
    B("Each group has 2 coins of 5 rupees. 10 groups have 10 times 2, which is 20 of them.",
      *ANSC("l7", "10 × 2 = 20", 20)),
    B("Notice that 10 is the number of groups, not the answer. And the question asks how many coins, not how much they are worth."),
    B("Check: 50 coins of 1 rupee, 30 coins of 2 rupees and 20 coins of 5 rupees. That is 50 plus 60 plus 100, which is 210 rupees.",
      W("l8", "50 × 1 = 50"), W("l9", "30 × 2 = 60"), W("l10", "20 × 5 = 100"), W("l11", "50 + 60 + 100 = 210")),
    B("So when a ratio counts things of different values, find the value of one group, then count the groups. There are 20 coins of 5 rupees."),
)

# Mother : Riya = 7 : 2; in 5 years 8 : 3.
LESSONS["G5A_VARIATION_013"] = LESSON(
    B("The ages of a mother and her daughter Riya are in the ratio 7 to 2. In 5 years' time, they will be in the ratio 8 to 3. How old is the mother now?",
      GIVEN("q", "Mother : Riya = 7 : 2. In 5 years: 8 : 3. Mother now?")),
    B("Both of them grow older by the same 5 years. So the gap between their ages never changes. That is the key."),
    B("Now, the gap is 7 minus 2, which is 5 parts. In 5 years, the gap is 8 minus 3, which is 5 parts again.",
      W("l1", "7 − 2 = 5"), W("l2", "8 − 3 = 5")),
    B("The same gap is 5 parts both times. So the parts are the same size in both ratios, and we can compare them directly."),
    B("The mother goes from 7 parts to 8 parts in 5 years. So how many years is 1 part?",
      ask=CHOOSE(["5 years", "1 year", "8 years"], 0,
                 "She gains 1 part, going from 7 parts to 8. In that time she gets 5 years older. So that 1 part is 5 years.")),
    B("She gains 1 part while she gets 5 years older. So 1 part is 5 years.",
      W("l3", "8 − 7 = 1"), NOTE("l3", "1", "part = 5 years")),
    B("The mother is 7 parts now. 7 times 5 is 35. She is 35 years old.",
      *ANSC("l4", "7 × 5 = 35", 35)),
    B("The trap is to give her age in 5 years' time, which is 8 parts. The question asks for her age now."),
    B("Check: Riya is 2 times 5, which is 10. In 5 years they will be 40 and 15. Divide both by 5 and you get 8 to 3.",
      W("l5", "2 × 5 = 10"), W("l6", "35 + 5 = 40"), W("l7", "10 + 5 = 15"), W("l8", "40 ÷ 5 = 8"), W("l9", "15 ÷ 5 = 3")),
    B("So with ages, the gap never changes. If the gap is the same number of parts both times, the parts match, and the mother is 35."),
)

# 3 men or 6 boys: 20 days. 2 men and 4 boys?
LESSONS["G5A_VARIATION_014"] = LESSON(
    B("3 men, or 6 boys, can paint a school hall in 20 days. How many days will 2 men and 4 boys take, working together?",
      GIVEN("q", "3 men OR 6 boys: 20 days. 2 men + 4 boys: days?")),
    B("First, change everyone into one kind of worker. 3 men do the same work as 6 boys. So 1 man works like 6 divided by 3, which is 2 boys.",
      W("l1", "6 ÷ 3 = 2"), NOTE("l1", "2", "boys = 1 man")),
    B("So the team of 2 men and 4 boys is worth how many boys?",
      ask=CHOOSE(["6 boys", "8 boys", "10 boys"], 1,
                 "Each man counts as 2 boys. So the 2 men are worth 4 boys, and there are 4 real boys as well.")),
    B("2 men are worth 2 times 2, which is 4 boys. Add the 4 real boys, and the team is like 8 boys. The trap is to count 6 workers, all the same.",
      W("l2", "2 × 2 = 4"), W("l3", "4 + 4 = 8")),
    B("How big is the job? 6 boys take 20 days, so it is 6 times 20, which is 120 boy days of work.",
      W("l4", "6 × 20 = 120"), NOTE("l4", "120", "boy-days")),
    B("8 boys share 120 boy days. 120 divided by 8 is 15. The team takes 15 days.",
      *ANSC("l5", "120 ÷ 8 = 15", 15)),
    B("Does that make sense? The team is worth 8 boys, which is more than 6 boys. So it should take less than 20 days, and 15 is less."),
    B("Check: 8 boys for 15 days is 8 times 15, which is 120 boy days, the whole job.",
      W("l6", "8 × 15 = 120")),
    B("So turn a mixed team into one kind of worker, measure the job in worker days, and divide."),
)

# 3 : 2; each spends 40; 2 : 1: Kiran at first.
LESSONS["G5A_VARIATION_015"] = LESSON(
    B("Kiran and Leela had money in the ratio 3 to 2. Each of them spent 40 rupees on a book, and now the ratio is 2 to 1. How much did Kiran have at first?",
      GIVEN("q", "Kiran : Leela = 3 : 2. Each spends ₹40 → 2 : 1. Kiran?")),
    B("Both spend the same 40 rupees. So the gap between their money does not change. That is the key."),
    B("Before, the gap is 3 minus 2, which is 1 part. After, the gap is 2 minus 1, which is 1 part again.",
      W("l1", "3 − 2 = 1"), W("l2", "2 − 1 = 1")),
    B("The same gap is 1 part both times. So the parts are the same size before and after."),
    B("Kiran goes from 3 parts to 2 parts by spending 40 rupees. So how much is 1 part?",
      ask=CHOOSE(["20 rupees", "40 rupees", "80 rupees"], 1,
                 "He drops by 1 part, from 3 parts to 2. What he lost is the 40 rupees he spent. So that 1 part is 40 rupees.")),
    B("He lost 1 part, and he spent 40 rupees. So 1 part is 40 rupees.",
      LB("l3", "Kiran: 3 parts → 2 parts, so 1 part = ₹40")),
    B("At first Kiran had 3 parts. 3 times 40 is 120. He had 120 rupees.",
      *ANSC("l4", "3 × 40 = 120", 120)),
    B("Careful: the question asks for his money at first, not after the book. After the book he has only 2 parts."),
    B("Check: Leela had 2 times 40, which is 80. After spending, Kiran has 80 and Leela has 40, and 80 is twice 40.",
      W("l5", "2 × 40 = 80"), W("l6", "120 − 40 = 80"), W("l7", "80 − 40 = 40"), W("l8", "80 = 2 × 40")),
    B("So when both spend the same amount, the gap stays fixed. Match the gap in both ratios, and the parts tell you the rest."),
)
