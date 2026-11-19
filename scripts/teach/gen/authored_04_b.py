"""Profit and loss (last 4), sequences (7) and the first speed warm-up, written one by one."""
from authored_04_lib import ANSC, ANSL, B, BOX, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, STRIKE, UL, W  # noqa: F401

LESSONS = {}

PROFIT = "Profit = selling price − cost price"

# Sells for MORE than he paid: what does he make?
LESSONS["G5A_PROFITLOSS_007"] = LESSON(
    B("A shopkeeper sells a toy for more money than he paid for it. What do we call what he makes?",
      GIVEN("q", "Sells a toy for MORE than he paid. He makes …?")),
    B("Let's try it with small numbers. Say he paid 10 rupees for the toy and sold it for 12 rupees.",
      LB("l1", "Paid ₹10, sold for ₹12")),
    B("12 minus 10 is 2. He gets back all he paid, and 2 rupees extra.",
      W("l2", "12 − 10 = 2"), NOTE("l2", "2", "extra")),
    B("What is that extra money called?",
      ask=CHOOSE(["a loss", "a discount", "a profit"], 2,
                 "A loss is when he gets back less than he paid, and a discount is money taken off for the buyer. Here the shopkeeper ends up with extra money.")),
    B("The extra money a seller earns is called a profit. So selling for more than the cost gives a profit.",
      *ANSL("l3", "Sold for more than the cost → a profit", "a profit")),
    B("And the other way round: selling for less than he paid would be a loss. More means profit, less means loss."),
)

# Bought for 900, sold for 900.
LESSONS["G5A_PROFITLOSS_008"] = LESSON(
    B("Mohan bought a cycle for 900 rupees and later sold it for 900 rupees. Did he make a profit or a loss?",
      GIVEN("q", "Bought for ₹900, sold for ₹900. Profit or loss?")),
    B("Profit or loss is always about the gap between the two prices. So compare them. Which is bigger?",
      ask=CHOOSE(["the selling price", "the cost price", "they are equal"], 2,
                 "Look at both prices. He paid 900 rupees and he got 900 rupees. Neither one is bigger.")),
    B("They are equal. So the gap is 900 minus 900, which is 0.",
      W("l1", "900 − 900 = 0")),
    B("He got back exactly what he paid: nothing gained, and nothing lost.",
      *ANSL("l2", "Neither a profit nor a loss", "Neither")),
    B("Careful: the 900 rupees is the price, not a profit. A profit is only the extra money, and here there is no extra."),
    B("So equal prices mean no profit and no loss. Mohan made neither."),
)

# Bought for 80, sold for 100: profit.
LESSONS["G5A_PROFITLOSS_009"] = LESSON(
    B("A shopkeeper bought a water bottle for 80 rupees and sold it for 100 rupees. What was his profit?",
      GIVEN("q", "Bought for ₹80, sold for ₹100. Profit?")),
    B("He sold it for more than he paid, so there is a profit. It is the gap between the two prices.",
      LB("f", PROFIT)),
    B("Which sum finds that gap?",
      ask=CHOOSE(["100 − 80", "100 + 80", "80 − 100"], 0,
                 "The profit is the extra he got over what he paid. So start with the 100 he got and take away the 80 he paid.")),
    B("100 minus 80 is 20. His profit was 20 rupees.",
      *ANSC("l1", "100 − 80 = 20", 20), NOTE("l1", "20", "rupees")),
    B("Check by counting up: from 80, add 20, and you reach 100.",
      W("l2", "80 + 20 = 100")),
    B("So profit is the selling price take away the cost price."),
)

# Paid 200: which selling price gives a profit?
LESSONS["G5A_PROFITLOSS_010"] = LESSON(
    B("A fruit seller paid 200 rupees for a box of apples. Four selling prices are offered, and we want the one that gives him a profit.",
      GIVEN("q", "Paid ₹200. Which selling price gives a profit?"),
      LB("l1", "₹180    ₹200    ₹150    ₹240")),
    B("First, the idea. For a profit, how must the selling price compare with the 200 rupees he paid?",
      ask=CHOOSE(["more than 200", "less than 200", "equal to 200"], 0,
                 "A profit means he ends up with extra money. So he has to get back more than the 200 rupees he paid.")),
    B("It must be more than 200. Now test each price. 180 is less than 200, and so is 150. Those would be losses.",
      W("l2", "180 < 200"), W("l3", "150 < 200")),
    B("200 is exactly what he paid. That gives no profit and no loss.",
      W("l4", "200 = 200")),
    B("240 is more than 200. So selling for 240 rupees gives a profit.",
      *ANSC("l5", "240 > 200", 240), CIRC("l1", "₹240")),
    B("And how big is that profit? 240 minus 200 is 40 rupees.",
      W("l6", "240 − 200 = 40")),
    B("So a profit needs a selling price above the cost price. Here, only 240 is."),
)

# 3, 4, 7, 11, 18, 29: the 9th term.
LESSONS["G5A_SEQUENCES_001"] = LESSON(
    B("Here is a sequence: 3, 4, 7, 11, 18, 29. We want its 9th term.",
      GIVEN("q", "3, 4, 7, 11, 18, 29, …  9th term?")),
    B("First idea: look at the jumps. They are 1, 3, 4, 7, 11. That is not a steady jump, so we need another idea.",
      LB("l1", "Jumps: 1, 3, 4, 7, 11")),
    B("Look at 3, 4, 7. Then look at 4, 7, 11. How is each term made from the two before it?",
      ask=CHOOSE(["add the two terms before it", "multiply the two before it", "add 4 each time"], 0,
                 "Try it. 3 plus 4 is 7. Then 4 plus 7 is 11. Each term is the two terms before it, added together.")),
    B("3 plus 4 is 7, then 7 plus 11 is 18, and 11 plus 18 is 29. The rule holds all the way along.",
      W("l2", "3 + 4 = 7"), W("l3", "7 + 11 = 18"), W("l4", "11 + 18 = 29")),
    B("Now count the places carefully. 29 is the 6th term. So the 7th term is 18 plus 29, which is 47.",
      NOTE("q", "29", "6th"), W("l5", "18 + 29 = 47"), NOTE("l5", "47", "7th")),
    B("The 8th term is 29 plus 47, which is 76.",
      W("l6", "29 + 47 = 76"), NOTE("l6", "76", "8th")),
    B("We have reached 76. Do we stop here?",
      ask=CHOOSE(["yes, 76 is the answer", "no, one more step"], 1,
                 "29 was the 6th term, so 47 is the 7th and 76 is the 8th. We want the 9th, so there is one more step to take.")),
    B("One more step. The 9th term is 47 plus 76, which is 123.",
      *ANSC("l7", "47 + 76 = 123", 123), NOTE("l7", "123", "9th")),
    B("So when the jumps make no simple pattern, see if each term is built from the ones before it. And keep count of the places as you go."),
)

# 5, 40, 8, 35, 11, 30, 14, 25: 15th term + 16th term.
LESSONS["G5A_SEQUENCES_002"] = LESSON(
    B("Look at this sequence: 5, 40, 8, 35, 11, 30, 14, 25. We want the 15th term and the 16th term, added together.",
      GIVEN("q", "5, 40, 8, 35, 11, 30, 14, 25, …  15th + 16th term?")),
    B("The terms jump up, then down, then up again. That is the clue that two patterns are woven together. So take every second term."),
    B("The odd places hold 5, 8, 11, 14, going up by 3. The even places hold 40, 35, 30, 25, going down by 5.",
      LB("l1", "Odd places: 5, 8, 11, 14 (+3)"), LB("l2", "Even places: 40, 35, 30, 25 (−5)")),
    B("The 15th term is in the odd pattern. Count the odd places up to 15 and there are 8 of them. So it is the 8th number of that pattern.",
      LB("l3", "Places 1, 3, 5, 7, 9, 11, 13, 15 → 8 numbers")),
    B("To get from the 1st number of a pattern to its 8th number, how many steps do we take?",
      ask=CHOOSE(["7 steps", "8 steps", "15 steps"], 0,
                 "Count the jumps, not the numbers. From the 1st to the 2nd is 1 step, so from the 1st to the 8th is 7 steps.")),
    B("That is the trap: 8 numbers, but only 7 steps. So the 15th term is 5 plus 7 lots of 3. 7 times 3 is 21, and 5 plus 21 is 26.",
      W("l4", "7 × 3 = 21"), W("l5", "5 + 21 = 26"), NOTE("l5", "26", "15th term")),
    B("The 16th term is the 8th number of the even pattern, again 7 steps on. 7 times 5 is 35, and 40 minus 35 is 5.",
      W("l6", "7 × 5 = 35"), W("l7", "40 − 35 = 5"), NOTE("l7", "5", "16th term", "below", 2)),
    B("Now add them. 26 plus 5 is 31.",
      *ANSC("l8", "26 + 5 = 31", 31)),
    B("Check by carrying both patterns on. After 14 come 17, 20, 23, 26. After 25 come 20, 15, 10, 5. They end on 26 and 5.",
      LB("l9", "14, 17, 20, 23, 26   and   25, 20, 15, 10, 5")),
    B("So when a sequence zigzags, split it into two patterns. And remember, the 8th number is only 7 steps after the first. The sum is 31."),
)

# 1, 2, 3, 4, 3, 2, 1, 2, ...: the 100th number.
LESSONS["G5A_SEQUENCES_003"] = LESSON(
    B("Tara counts up to 4 and back down to 1, again and again: 1, 2, 3, 4, 3, 2, 1, 2, and so on. We want the 100th number she says.",
      GIVEN("q", "1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2, 1, 2, …  100th?")),
    B("Her counting repeats, so we look for the block that repeats. A block must stop just before the pattern starts again."),
    B("Which is the repeating block?",
      ask=CHOOSE(["1, 2, 3, 4, 3, 2, 1", "1, 2, 3, 4, 3, 2", "1, 2, 3, 4"], 1,
                 "Careful with the 1. After 1, 2, 3, 4, 3, 2, the next 1 starts the pattern all over again, so it belongs to the next block.")),
    B("The block is 1, 2, 3, 4, 3, 2, and that is 6 numbers. The trap is to count 7, by taking the 1 at both ends.",
      BOX("q", "1, 2, 3, 4, 3, 2"), LB("l1", "Block: 1, 2, 3, 4, 3, 2 → 6 numbers")),
    B("How many whole blocks fit into 100 numbers? 16 times 6 is 96. So 16 blocks use up 96 numbers, and 100 minus 96 leaves 4 more.",
      W("l2", "16 × 6 = 96"), W("l3", "100 − 96 = 4")),
    B("So where in a block is the 100th number?",
      ask=CHOOSE(["the 4th number of a block", "the 6th number of a block", "the 1st number of a block"], 0,
                 "96 numbers are used up by whole blocks. Then a new block starts, and the 100th number is 4 numbers into it.")),
    B("Count 4 numbers into the block: 1, 2, 3, 4. The 4th number is 4. So the 100th number Tara says is 4.",
      *ANSL("l4", "100th number = 4", "4")),
    B("Check the idea on a small case. 10 is 6 plus 4, so the 10th number should be 4 as well. Count along Tara's list: it is.",
      W("l5", "6 + 4 = 10")),
    B("So for a repeating pattern: find the true block, divide to drop the whole blocks, and count along what is left over."),
)

# 100, 93, 86, 79, ... down by 7: how many terms are greater than 0?
LESSONS["G5A_SEQUENCES_004"] = LESSON(
    B("A sequence starts 100, 93, 86, 79, going down by 7 each time. How many of its terms are greater than 0?",
      GIVEN("q", "100, 93, 86, 79, … (down by 7). Terms above 0?")),
    B("Every step takes away 7. So first we ask: how many 7s can we take from 100 before we run out?"),
    B("14 times 7 is 98. So after 14 steps down, the term is 100 minus 98, which is 2.",
      W("l1", "14 × 7 = 98"), W("l2", "100 − 98 = 2")),
    B("2 is still greater than 0. One more step would give 2 minus 7, which is below 0. So 14 steps is as far as we can go.",
      LB("l3", "2 − 7 is below 0")),
    B("14 steps down. So how many terms are greater than 0?",
      ask=CHOOSE(["14", "15", "16"], 1,
                 "Steps are the jumps between terms. The first term, 100, is there before any step is taken. So count 1 for the start, and 1 more for each of the 14 steps.")),
    B("Here is the trap: 14 is the number of steps, not the number of terms. The starting term, 100, counts too. 14 plus 1 is 15.",
      UL("q", "100"), *ANSC("l4", "14 + 1 = 15", 15)),
    B("Check on the start of the list. 100, 93, 86, 79 is 4 terms, but only 3 steps down. Terms are always one more than steps.",
      LB("l5", "100, 93, 86, 79: 4 terms, 3 steps")),
    B("So count the steps by dividing, make sure the last term is still above 0, then add 1 for the first term. There are 15 terms."),
)

# 100 − 99 + 98 − 97 + ... + 2 − 1.
LESSONS["G5A_SEQUENCES_005"] = LESSON(
    B("Here is a long sum: 100 minus 99, plus 98 minus 97, and so on, all the way down to plus 2 minus 1.",
      GIVEN("q", "100 − 99 + 98 − 97 + … + 4 − 3 + 2 − 1 = ?")),
    B("Working from left to right would take ages. So look for small groups that are easy to work out."),
    B("Put the numbers in pairs: 100 minus 99, then 98 minus 97, and on down to 2 minus 1.",
      LB("l1", "(100 − 99) + (98 − 97) + … + (2 − 1)")),
    B("Every pair is worth 1. 100 minus 99 is 1, 98 minus 97 is 1, and 2 minus 1 is 1.",
      W("l2", "100 − 99 = 1"), W("l3", "98 − 97 = 1"), W("l4", "2 − 1 = 1")),
    B("There are 100 numbers in the sum, from 100 down to 1. How many pairs do they make?",
      ask=CHOOSE(["100 pairs", "50 pairs", "49 pairs"], 1,
                 "Each pair uses up 2 numbers. So 100 numbers make 100 divided by 2 pairs, which is 50.")),
    B("100 divided by 2 is 50. So there are 50 pairs.",
      W("l5", "100 ÷ 2 = 50")),
    B("50 pairs, each worth 1. 50 times 1 is 50.",
      *ANSC("l6", "50 × 1 = 50", 50)),
    B("Two slips to dodge. The sum does not cancel down to 0, because each pair leaves 1 behind. And it is not 100, because every pair uses 2 numbers."),
    B("Check with a small one: 4 minus 3, plus 2 minus 1. That is 1 plus 1, which is 2. 4 numbers, 2 pairs.",
      W("l7", "4 − 3 + 2 − 1 = 2")),
    B("So when a long sum has a rhythm, group it into equal pairs and count the pairs. Here that gives 50."),
)

# 1, 2, 2, 3, 3, 3, ...: the 50th term.
LESSONS["G5A_SEQUENCES_006"] = LESSON(
    B("In this sequence each number is written as many times as its own size: one 1, two 2s, three 3s, four 4s. We want the 50th term.",
      GIVEN("q", "1, 2, 2, 3, 3, 3, 4, 4, 4, 4, …  50th term?")),
    B("Let's find the place where each number ends. The 1 ends at place 1. The 2s end at place 3. The 3s end at place 6.",
      W("l1", "1 + 2 = 3"), W("l2", "1 + 2 + 3 = 6")),
    B("So we keep a running total, adding the next number each time: 1, 3, 6, 10, 15, 21, 28, 36, 45. The 9s end at place 45.",
      LB("l3", "Ends: 1, 3, 6, 10, 15, 21, 28, 36, 45"), NOTE("l3", "45", "the 9s end here")),
    B("The 9s end at place 45, and we want place 50. What is written in the places just after 45?",
      ask=CHOOSE(["more 9s", "ten 10s", "one 10, then 11s"], 1,
                 "The 9s are finished: there are exactly nine of them. Next comes 10, and it is written 10 times.")),
    B("Ten 10s come next. 45 plus 10 is 55, so the 10s fill places 46 to 55.",
      W("l4", "45 + 10 = 55"), LB("l5", "Places 46 to 55: all 10s")),
    B("Place 50 lies between 46 and 55. So the 50th term is 10.",
      *ANSL("l6", "50th term = 10", "10")),
    B("The tempting slip is to say 9, because 45 is so close to 50. But the 9s stop at place 45, and place 50 comes after that."),
    B("So add 1 plus 2 plus 3 and so on to see where each number ends, then find which stretch your place falls in. Here it is the 10s."),
)

# Start 7; odd: add 5; even: halve. The 50th term.
LESSONS["G5A_SEQUENCES_007"] = LESSON(
    B("A sequence starts with 7. If a term is odd, we add 5. If it is even, we halve it. It begins 7, 12, 6, 3, and we want the 50th term.",
      GIVEN("q", "Start 7. Odd: add 5. Even: halve. 7, 12, 6, 3, …  50th?")),
    B("Carry on from 3. It is odd, so add 5 to get 8. 8 is even, so halve it to get 4. Then 2, then 1.",
      W("l1", "3 + 5 = 8"), W("l2", "8 ÷ 2 = 4"), W("l3", "4 ÷ 2 = 2"), W("l4", "2 ÷ 2 = 1")),
    B("1 is odd, so add 5, and we get 6. We have seen 6 before! From here on, everything comes round again.",
      W("l5", "1 + 5 = 6"), LB("l6", "7, 12, 6, 3, 8, 4, 2, 1, 6, 3, 8, 4, 2, 1, …")),
    B("Which block repeats?",
      ask=CHOOSE(["7, 12, 6, 3, 8, 4, 2, 1", "6, 3, 8, 4, 2, 1", "12, 6, 3, 8, 4, 2"], 1,
                 "After the 1 we go back to 6, not to 7. So 7 and 12 never come again. The block that repeats is 6, 3, 8, 4, 2, 1.")),
    B("The block 6, 3, 8, 4, 2, 1 has 6 numbers. And here is the trap: it only starts at the 3rd term. The 7 and the 12 sit outside it.",
      BOX("l6", "6, 3, 8, 4, 2, 1"), STRIKE("l6", "7, 12", "not in the block")),
    B("So set those 2 terms aside. 50 minus 2 leaves 48 terms inside the repeating part.",
      W("l7", "50 − 2 = 48")),
    B("48 divided by 6 is exactly 8, with nothing left over. So the 50th term finishes off the 8th block.",
      W("l8", "48 ÷ 6 = 8")),
    B("It is the last number of a block. Which number is that?",
      ask=CHOOSE(["6", "1", "8"], 1,
                 "Nothing left over means we land on the end of a block, not the start of one. The block is 6, 3, 8, 4, 2, 1, and it ends with 1.")),
    B("The block ends in 1. So the 50th term is 1.",
      *ANSL("l9", "50th term = 1", "1")),
    B("Check on a near case. 2 plus 6 is 8, so the 8th term should end the first block. In our list, the 8th term is 1.",
      W("l10", "2 + 6 = 8")),
    B("So: run the rule until it comes round again, set aside the terms before the loop, then divide by the length of the block."),
)

# 12 km/hr for 3 hours: how far?
LESSONS["G5A_SPEED_001"] = LESSON(
    B("Asha cycles at a steady 12 kilometres an hour. How far does she cycle in 3 hours?",
      GIVEN("q", "12 km/hr for 3 hours. How far?")),
    B("12 kilometres an hour means she covers 12 kilometres in every single hour.",
      UL("q", "12 km/hr")),
    B("She rides for 3 hours. How do we find how far she goes?",
      ask=CHOOSE(["12 + 3", "12 × 3", "12 ÷ 3"], 1,
                 "She covers 12 kilometres in the first hour, 12 in the second and 12 in the third. That is 3 lots of 12.")),
    B("12 times 3 is 36. Asha cycles 36 kilometres.",
      *ANSC("l1", "12 × 3 = 36", 36), NOTE("l1", "36", "km")),
    B("Check by adding hour by hour: 12 plus 12 plus 12 is 36.",
      W("l2", "12 + 12 + 12 = 36")),
    B("So distance is speed times time."),
)
