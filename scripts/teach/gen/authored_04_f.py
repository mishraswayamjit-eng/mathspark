"""Ratio, proportion and variation 001 to 008, written one by one."""
from authored_04_lib import ANSC, ANSL, B, BOX, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, STRIKE, UL, W  # noqa: F401

LESSONS = {}

# 5 : 3; Asha gives 12 and they are equal: Asha at first.
LESSONS["G5A_VARIATION_001"] = LESSON(
    B("Asha and Bina have stickers in the ratio 5 to 3. Asha gives 12 stickers to Bina, and now they have the same number. How many did Asha have at first?",
      GIVEN("q", "Asha : Bina = 5 : 3. Asha gives 12 → equal. Asha at first?")),
    B("Asha has 5 parts and Bina has 3 parts. So Asha is ahead by 5 minus 3, which is 2 parts.",
      W("l1", "5 − 3 = 2"), NOTE("l1", "2", "parts ahead")),
    B("Asha gives 12 stickers to Bina, and they become equal. So how big was the gap between them?",
      ask=CHOOSE(["12 stickers", "24 stickers", "6 stickers"], 1,
                 "Giving 12 does two things at once. Asha goes down by 12, and Bina goes up by 12. So the gap closes from both sides.")),
    B("That is the trap. The gap closes from both sides: Asha drops 12 and Bina climbs 12. So the gap was 12 plus 12, which is 24.",
      W("l2", "12 + 12 = 24")),
    B("The gap is 2 parts, and it is 24 stickers. So 1 part is 24 divided by 2, which is 12 stickers.",
      W("l3", "24 ÷ 2 = 12")),
    B("Asha had 5 parts. 5 times 12 is 60. Asha had 60 stickers at first.",
      *ANSC("l4", "5 × 12 = 60", 60)),
    B("Check: Bina had 3 times 12, which is 36. After the gift, Asha has 60 minus 12 and Bina has 36 plus 12. Both come to 48.",
      W("l5", "3 × 12 = 36"), W("l6", "60 − 12 = 48"), W("l7", "36 + 12 = 48")),
    B("So when one gives to the other and they end up equal, the gap was twice the gift. Then the ratio turns the gap into parts."),
)

# 5 : 1; Meena gives 15; becomes 2 : 1: Meena now.
LESSONS["G5A_VARIATION_002"] = LESSON(
    B("Meena and Tara share money in the ratio 5 to 1. Meena gives 15 rupees to Tara, and the ratio becomes 2 to 1. How much does Meena have now?",
      GIVEN("q", "Meena : Tara = 5 : 1. Meena gives ₹15 → 2 : 1. Meena now?")),
    B("When Meena gives money to Tara, the total they have together does not change. That is the key to this one."),
    B("At first there are 5 plus 1, that is 6 parts in all. Afterwards, the ratio 2 to 1 has only 3 parts. Same total, but parts of a different size.",
      W("l1", "5 + 1 = 6"), W("l2", "2 + 1 = 3")),
    B("How can we write 2 to 1 so that it has 6 parts as well?",
      ask=CHOOSE(["4 : 2", "3 : 3", "2 : 4"], 0,
                 "Double both numbers of 2 to 1. That gives 4 to 2, which is the same ratio, and 4 plus 2 makes 6 parts.")),
    B("Double both numbers: 2 to 1 is the same as 4 to 2. Now both ratios have 6 parts, so the parts are the same size.",
      LB("l3", "2 : 1 = 4 : 2"), W("l4", "4 + 2 = 6")),
    B("Meena goes from 5 parts down to 4 parts. She lost 1 part, and that is the 15 rupees she gave. So 1 part is 15 rupees.",
      LB("l5", "Meena: 5 parts → 4 parts"), W("l6", "5 − 4 = 1"), NOTE("l6", "1", "part = ₹15", "below", 1)),
    B("Meena now has 4 parts. 4 times 15 is 60. She has 60 rupees now.",
      *ANSC("l7", "4 × 15 = 60", 60)),
    B("The trap is to compare 5 to 1 with 2 to 1 straight away, as if the parts matched. They only match once both ratios have the same total."),
    B("Check: at first Meena had 5 times 15, which is 75, and Tara had 15. After the gift they have 60 and 30, and 60 is twice 30.",
      W("l8", "5 × 15 = 75"), W("l9", "75 − 15 = 60"), W("l10", "15 + 15 = 30"), W("l11", "60 = 2 × 30")),
    B("So when money only moves between two people, the total stays fixed. Write both ratios with the same total, then compare."),
)

# Boys : girls 3 : 4; 6 boys join; 6 : 7: children now.
LESSONS["G5A_VARIATION_003"] = LESSON(
    B("In a chess club, boys to girls is 3 to 4. Then 6 more boys join, and the ratio becomes 6 to 7. How many children are in the club now?",
      GIVEN("q", "Boys : girls = 3 : 4. 6 more boys → 6 : 7. Children now?")),
    B("Only boys join. The number of girls does not change. So we make the girls the same number of parts in both ratios."),
    B("Girls are 4 parts in one ratio and 7 parts in the other. What number can both become?",
      ask=CHOOSE(["11", "28", "14"], 1,
                 "We need a number that both 4 and 7 go into. 4 times 7 is 28, and both of them go into 28.")),
    B("4 times 7 is 28. So multiply the first ratio by 7: 3 to 4 becomes 21 to 28.",
      W("l1", "4 × 7 = 28"), W("l2", "3 × 7 = 21"), LB("l3", "3 : 4 = 21 : 28")),
    B("And multiply the second ratio by 4: 6 to 7 becomes 24 to 28.",
      W("l4", "6 × 4 = 24"), LB("l5", "6 : 7 = 24 : 28")),
    B("Now the parts match. Boys go from 21 parts to 24 parts. That is 3 more parts, and they are the 6 new boys. So 1 part is 2 children.",
      W("l6", "24 − 21 = 3"), W("l7", "6 ÷ 3 = 2")),
    B("The club now has 24 parts of boys and 28 parts of girls. 24 plus 28 is 52 parts.",
      W("l8", "24 + 28 = 52")),
    B("52 parts, with 2 children in each. 52 times 2 is 104. There are 104 children in the club now.",
      *ANSC("l9", "52 × 2 = 104", 104)),
    B("The trap is to say the boys went from 3 parts to 6 parts. Those parts are not the same size until the girls have been matched."),
    B("Check: now there are 48 boys and 56 girls. Before, there were 42 boys, and 42 plus 6 is 48.",
      W("l10", "24 × 2 = 48"), W("l11", "28 × 2 = 56"), W("l12", "21 × 2 = 42"), W("l13", "42 + 6 = 48")),
    B("So find what does not change, give it the same number of parts in both ratios, and then compare the rest. The club has 104 children."),
)

# Walkers : ALL = 3 : 8; 40 do not walk.
LESSONS["G5A_VARIATION_004"] = LESSON(
    B("In Class 5B, the ratio of children who walk to school, to all the children in the class, is 3 to 8. There are 40 children who do not walk. How many walk?",
      GIVEN("q", "Walkers : ALL children = 3 : 8. 40 do not walk. Walkers?")),
    B("Read the ratio carefully. The 8 is not another group. It is the whole class. Out of every 8 children, 3 walk.",
      UL("q", "ALL")),
    B("So how many parts do not walk?",
      ask=CHOOSE(["8 parts", "5 parts", "3 parts"], 1,
                 "The whole class is 8 parts, and 3 of those parts walk. The rest do not, and 8 minus 3 leaves 5.")),
    B("8 minus 3 is 5. So 5 parts do not walk, and those 5 parts are the 40 children.",
      W("l1", "8 − 3 = 5")),
    B("1 part is 40 divided by 5, which is 8 children.",
      W("l2", "40 ÷ 5 = 8")),
    B("The walkers are 3 parts. 3 times 8 is 24. So 24 children walk to school.",
      *ANSC("l3", "3 × 8 = 24", 24)),
    B("The trap is to read 3 to 8 as walkers to non walkers. Then the 40 children would be taken as 8 parts, and everything after that goes astray."),
    B("Check: the whole class is 8 parts, and 8 times 8 is 64 children. Take away the 24 walkers, and 40 are left.",
      W("l4", "8 × 8 = 64"), W("l5", "64 − 24 = 40")),
    B("So always ask what each number in a ratio stands for: a group, or the whole. Here 24 children walk."),
)

# Anu : Bela = 3 : 4, Bela : Chitra = 6 : 5, total 372: Chitra.
LESSONS["G5A_VARIATION_005"] = LESSON(
    B("Anu, Bela and Chitra share 372 rupees. Anu to Bela is 3 to 4, and Bela to Chitra is 6 to 5. How much does Chitra get?",
      GIVEN("q", "Anu : Bela = 3 : 4, Bela : Chitra = 6 : 5. Share ₹372.")),
    B("Bela is in both ratios, but she is 4 in one and 6 in the other. Before we can join them, Bela must be the same number in both.",
      UL("q", "4"), UL("q", "6")),
    B("Which number can Bela be in both ratios?",
      ask=CHOOSE(["10", "12", "2"], 1,
                 "We need a number that 4 and 6 both go into. 4 times 3 is 12, and 6 times 2 is 12. So Bela can be 12.")),
    B("Multiply the first ratio by 3: 3 to 4 becomes 9 to 12.",
      W("l1", "3 × 3 = 9"), W("l2", "4 × 3 = 12"), LB("l3", "3 : 4 = 9 : 12")),
    B("Multiply the second ratio by 2: 6 to 5 becomes 12 to 10.",
      W("l4", "6 × 2 = 12"), W("l5", "5 × 2 = 10"), LB("l6", "6 : 5 = 12 : 10")),
    B("Now join them. Anu to Bela to Chitra is 9 to 12 to 10. In all, that is 9 plus 12 plus 10, which is 31 parts.",
      LB("l7", "Anu : Bela : Chitra = 9 : 12 : 10"), W("l8", "9 + 12 + 10 = 31")),
    B("31 parts make 372 rupees. 372 divided by 31 is 12, so 1 part is 12 rupees.",
      W("l9", "372 ÷ 31 = 12")),
    B("Chitra has 10 parts. 10 times 12 is 120. Chitra gets 120 rupees.",
      *ANSC("l10", "10 × 12 = 120", 120)),
    B("The trap is to write 3 to 4 to 5 straight away. That forgets that Bela is 4 in one ratio and 6 in the other."),
    B("Check: Anu gets 108 and Bela gets 144. Add Chitra's 120, and the total is 372.",
      W("l11", "9 × 12 = 108"), W("l12", "12 × 12 = 144"), W("l13", "108 + 144 + 120 = 372")),
    B("So to join two ratios, first make the shared person the same number in both. Then count the parts and share."),
)

# Half of Kavi's = a third of Lata's; together 150: Kavi.
LESSONS["G5A_VARIATION_006"] = LESSON(
    B("Half of Kavi's savings is equal to a third of Lata's savings. Together they have saved 150 rupees. How much has Kavi saved?",
      GIVEN("q", "½ of Kavi's = ⅓ of Lata's. Together ₹150. Kavi?")),
    B("Call that equal amount 1 block. Half of Kavi's savings is 1 block, so the whole of Kavi's savings is 2 blocks.",
      LB("l1", "Kavi: 2 blocks")),
    B("A third of Lata's savings is 1 block. So how many blocks does Lata have?",
      ask=CHOOSE(["2 blocks", "3 blocks", "1 block"], 1,
                 "A third means one of 3 equal pieces. If one piece is 1 block, then the whole of Lata's savings is 3 blocks.")),
    B("Lata has 3 blocks. Notice that Lata has more than Kavi: it takes only a third of hers to match half of his.",
      LB("l2", "Lata: 3 blocks")),
    B("Together that is 2 plus 3, which is 5 blocks, worth 150 rupees. 150 divided by 5 is 30, so 1 block is 30 rupees.",
      W("l3", "2 + 3 = 5"), W("l4", "150 ÷ 5 = 30")),
    B("Kavi has 2 blocks. 2 times 30 is 60. Kavi has saved 60 rupees.",
      *ANSC("l5", "2 × 30 = 60", 60)),
    B("The slip to dodge is giving Kavi the 3 blocks and Lata the 2. It flips over: the one whose half is used has the smaller amount."),
    B("Check: Lata has 3 times 30, which is 90. Half of 60 is 30, and a third of 90 is 30, so they match. And 60 plus 90 is 150.",
      W("l6", "3 × 30 = 90"), W("l7", "½ × 60 = 30"), W("l8", "⅓ × 90 = 30"), W("l9", "60 + 90 = 150")),
    B("So when a fraction of one amount equals a fraction of another, call the equal bit 1 block and count blocks. Kavi has 60 rupees."),
)

# 12 workers, 20 days; after 5 days 3 leave: total days.
LESSONS["G5A_VARIATION_007"] = LESSON(
    B("12 workers can build a wall in 20 days. They all work for 5 days, and then 3 workers leave. How many days does the wall take from start to finish?",
      GIVEN("q", "12 workers: 20 days. After 5 days, 3 leave. Total days?")),
    B("Measure the wall in worker days: the work 1 worker does in 1 day. 12 workers for 20 days is 12 times 20, which is 240 worker days.",
      W("l1", "12 × 20 = 240"), NOTE("l1", "240", "worker-days")),
    B("In the first 5 days, all 12 are working. 12 times 5 is 60 worker days done. 240 minus 60 leaves 180 still to do.",
      W("l2", "12 × 5 = 60"), W("l3", "240 − 60 = 180")),
    B("Then 3 workers leave. 12 minus 3 is 9 workers left.",
      W("l4", "12 − 3 = 9")),
    B("How do we find the days the 9 workers need for the rest?",
      ask=CHOOSE(["180 ÷ 9", "180 ÷ 12", "240 ÷ 9"], 0,
                 "Only 9 workers are left, and only 180 worker days of work are left. Each day the 9 of them do 9 worker days, so divide 180 by 9.")),
    B("180 divided by 9 is 20. They need 20 more days.",
      W("l5", "180 ÷ 9 = 20")),
    B("Careful: 20 is only the days after the others left. The question asks for start to finish, so the first 5 days go in too.",
      UL("q", "Total days")),
    B("5 plus 20 is 25. The wall takes 25 days from start to finish.",
      *ANSC("l6", "5 + 20 = 25", 25)),
    B("Check the work: 60 worker days at first, then 9 workers for 20 days is 180 more. 60 plus 180 is 240, the whole wall.",
      W("l7", "9 × 20 = 180"), W("l8", "60 + 180 = 240")),
    B("So measure a job in worker days, take off what is done, and share the rest among the workers who are left."),
)

# Rice for 40 students for 30 days; after 10 days 10 more join.
LESSONS["G5A_VARIATION_008"] = LESSON(
    B("A hostel has rice to feed 40 students for 30 days. After 10 days, 10 more students join. For how many more days will the rice last?",
      GIVEN("q", "Rice: 40 students, 30 days. After 10 days, 10 more join.")),
    B("First, how much rice is left after 10 days? The 40 students have eaten for 10 of the 30 days. So there is rice for 20 more days, for those 40.",
      W("l1", "30 − 10 = 20")),
    B("Count the rice in student days: the rice 1 student eats in 1 day. 40 students for 20 days is 40 times 20, which is 800 student days.",
      W("l2", "40 × 20 = 800"), NOTE("l2", "800", "student-days left")),
    B("Now 10 more students join. 40 plus 10 is 50 students.",
      W("l3", "40 + 10 = 50")),
    B("50 students share 800 student days of rice. Which sum tells us how long it lasts?",
      ask=CHOOSE(["800 ÷ 50", "800 ÷ 40", "800 ÷ 10"], 0,
                 "Every day, the 50 students eat 50 student days of rice. So we see how many 50s there are in 800.")),
    B("800 divided by 50 is 16. The rice will last 16 more days.",
      *ANSC("l4", "800 ÷ 50 = 16", 16)),
    B("The trap is to start from all 30 days of rice. But 10 days of it were already eaten, and by only 40 students. Always start from what is left."),
    B("It makes sense too. With nobody new, the rice would last 20 more days. More mouths means fewer days, and 16 is fewer than 20."),
    B("Check: 50 students for 16 days is 50 times 16, which is 800 student days, exactly the rice that was left.",
      W("l5", "50 × 16 = 800")),
    B("So count the food that is left in student days, then divide by the new number of students."),
)
