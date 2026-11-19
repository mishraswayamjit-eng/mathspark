"""Place value (2) and profit and loss (first 6), written one by one."""
from authored_04_lib import ANSC, ANSL, B, BOX, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, UL, W  # noqa: F401

LESSONS = {}

PROFIT = "Profit = selling price − cost price"
LOSS = "Loss = cost price − selling price"

# Digits 2, 5, 7 once each: sum of all six 3-digit numbers.
LESSONS["G5A_PLACEVALUE_017"] = LESSON(
    B("Using the digits 2, 5 and 7 once each, we can make six different 3 digit numbers. We want the sum of all six.",
      GIVEN("q", "Digits 2, 5, 7 once each: sum of all six numbers?")),
    B("Here they are. With 2 in front: 257 and 275. With 5 in front: 527 and 572. With 7 in front: 725 and 752.",
      LB("l1", "257, 275, 527, 572, 725, 752")),
    B("We could add all six, but there is a quicker way. Look only at the hundreds place. How many times does each digit sit there?",
      ask=CHOOSE(["once", "twice", "3 times"], 1,
                 "Look at the list. 2 is in front of two numbers, 257 and 275. The same goes for 5 and for 7. So each digit is in the hundreds place twice.")),
    B("Each digit leads twice. And it is the same in the tens place and in the ones place: every digit turns up there exactly twice.",
      UL("l1", "257"), UL("l1", "275")),
    B("So one place adds up to twice the sum of the digits. 2 plus 5 plus 7 is 14, and twice 14 is 28.",
      W("l2", "2 + 5 + 7 = 14"), W("l3", "2 × 14 = 28")),
    B("That gives us 28 hundreds, 28 tens and 28 ones. 28 hundreds is 2800, and 28 tens is 280.",
      W("l4", "28 × 100 = 2800"), W("l5", "28 × 10 = 280")),
    B("Add them up. 2800 plus 280 plus 28 is 3108. That is the sum of all six numbers.",
      *ANSC("l6", "2800 + 280 + 28 = 3108", 3108)),
    B("The slip to watch for is counting each digit once, or 3 times, in a place. Six numbers shared among 3 digits gives each digit a place exactly twice."),
    B("Check the long way. The first pair makes 532, the second pair 1099, and the third pair 1477. Together they make 3108 again.",
      W("l7", "257 + 275 = 532"), W("l8", "527 + 572 = 1099"), W("l9", "725 + 752 = 1477"),
      W("l10", "532 + 1099 + 1477 = 3108")),
    B("So when digits are shuffled through every place, count how often each digit lands in a place, then add place by place."),
)

# How many 4-digit palindromes are even?
LESSONS["G5A_PLACEVALUE_018"] = LESSON(
    B("A palindrome reads the same forwards and backwards, like 3553. We want to know how many 4 digit palindromes are even numbers.",
      GIVEN("q", "4-digit palindromes, like 3553: how many are even?")),
    B("Look at 3553. The last digit copies the first, and the third copies the second. So once we choose the first two digits, the whole number is decided.",
      LB("l1", "A B B A"), NOTE("l1", "A", "last = first", "below", 2)),
    B("A number is even when its last digit is even. But here the last digit is also the first digit. So which digits can it be?",
      ask=CHOOSE(["0, 2, 4, 6 or 8", "2, 4, 6 or 8", "any digit from 1 to 9"], 1,
                 "The last digit must be even, and it is also the first digit. A 4 digit number cannot start with 0, so 0 is out. That leaves 2, 4, 6 and 8.")),
    B("That is the trap. 0 is an even digit, but a number cannot start with 0. So the first digit has only 4 choices: 2, 4, 6 or 8.",
      LB("l2", "A: 2, 4, 6 or 8 → 4 choices")),
    B("The second digit has no rule to obey. It can be any digit from 0 to 9, and that is 10 choices.",
      LB("l3", "B: 0 to 9 → 10 choices")),
    B("Each of the 4 choices for the first digit can go with each of the 10 choices for the second. So we multiply: 4 times 10 is 40.",
      *ANSC("l4", "4 × 10 = 40", 40)),
    B("Check with 2 in front: 2002, 2112, 2222, and so on up to 2992. That is 10 palindromes, and there are 10 more each for 4, 6 and 8.",
      LB("l5", "2002, 2112, 2222, … 2992")),
    B("So in a palindrome, count only the digits you are free to choose, and remember the first digit is never 0. There are 40 even ones."),
)

# Bought for 40, sold for 55: profit.
LESSONS["G5A_PROFITLOSS_001"] = LESSON(
    B("A shopkeeper bought a toy car for 40 rupees and sold it for 55 rupees. We want his profit.",
      GIVEN("q", "Bought for ₹40, sold for ₹55. Profit?")),
    B("Profit is the extra money he gets back, on top of what he paid.",
      LB("f", PROFIT)),
    B("So how do we find it here?",
      ask=CHOOSE(["55 + 40", "55 − 40", "40 − 55"], 1,
                 "Profit is how much more he got than he paid. So we take the 40 he paid away from the 55 he got.")),
    B("55 minus 40 is 15. His profit is 15 rupees.",
      *ANSC("l1", "55 − 40 = 15", 15), NOTE("l1", "15", "rupees")),
    B("Check: the 40 he paid, plus the 15 profit, makes 55, the selling price.",
      W("l2", "40 + 15 = 55")),
    B("So for a profit, take the cost price away from the selling price."),
)

# Bought for 250, sold for 220: loss.
LESSONS["G5A_PROFITLOSS_002"] = LESSON(
    B("Meena bought a bag for 250 rupees and sold it for 220 rupees. We want her loss.",
      GIVEN("q", "Bought for ₹250, sold for ₹220. Loss?")),
    B("She got back less than she paid, so she lost some money. The loss is the gap between the two prices.",
      LB("f", LOSS)),
    B("Which sum gives that gap?",
      ask=CHOOSE(["250 + 220", "250 − 220", "220 − 200"], 1,
                 "The loss is how much less she got than she paid. So we take the 220 she got away from the 250 she paid.")),
    B("250 minus 220 is 30. Her loss is 30 rupees.",
      *ANSC("l1", "250 − 220 = 30", 30), NOTE("l1", "30", "rupees")),
    B("Check: the 220 she got, plus the 30 she lost, makes 250, the price she paid.",
      W("l2", "220 + 30 = 250")),
    B("So for a loss, take the selling price away from the cost price."),
)

# Cost 300, wants a profit of 50: selling price.
LESSONS["G5A_PROFITLOSS_003"] = LESSON(
    B("A fruit seller buys a basket of mangoes for 300 rupees. He wants a profit of 50 rupees. What should his selling price be?",
      GIVEN("q", "Cost ₹300, wants a profit of ₹50. Selling price?")),
    B("Think first. To make a profit, should he sell the basket for more than 300 rupees, or for less?",
      ask=CHOOSE(["more than 300", "less than 300", "exactly 300"], 0,
                 "A profit means he ends up with extra money. So he must get back more than the 300 rupees he paid.")),
    B("More. He needs his 300 rupees back, and 50 rupees on top.",
      LB("f", "Selling price = cost price + profit")),
    B("300 plus 50 is 350. He should sell the basket for 350 rupees.",
      *ANSC("l1", "300 + 50 = 350", 350), NOTE("l1", "350", "rupees")),
    B("Check: selling for 350 after paying 300 leaves 350 minus 300, which is 50. That is the profit he wanted.",
      W("l2", "350 − 300 = 50")),
    B("So to make a profit, add the profit to the cost price."),
)

# Cost 500, sold at a loss of 80: selling price.
LESSONS["G5A_PROFITLOSS_004"] = LESSON(
    B("Ravi bought a cricket bat for 500 rupees, and sold it to a friend at a loss of 80 rupees. For how much did he sell it?",
      GIVEN("q", "Cost ₹500, sold at a loss of ₹80. Selling price?")),
    B("A loss. So did Ravi get more than the 500 rupees he paid, or less?",
      ask=CHOOSE(["more than 500", "less than 500"], 1,
                 "A loss means he got back less money than he paid. So the selling price is below 500 rupees.")),
    B("Less. He got 80 rupees less than he paid, so we take the loss away from the cost price.",
      LB("f", "Selling price = cost price − loss"), UL("q", "loss")),
    B("500 minus 80 is 420. He sold the bat for 420 rupees.",
      *ANSC("l1", "500 − 80 = 420", 420), NOTE("l1", "420", "rupees")),
    B("Check: 420 plus the 80 he lost makes 500, the price he paid.",
      W("l2", "420 + 80 = 500")),
    B("So with a loss, the selling price is the cost price take away the loss."),
)

# Sold for 90 with a profit of 20: cost price.
LESSONS["G5A_PROFITLOSS_005"] = LESSON(
    B("A shopkeeper sold a pen for 90 rupees and made a profit of 20 rupees. How much had he paid for the pen?",
      GIVEN("q", "Sold for ₹90, profit ₹20. Cost price?")),
    B("This one runs backwards: we know the selling price and want the cost price. He made a profit, so the 90 rupees is his cost and a bit more.",
      LB("f", "Cost price + profit = selling price")),
    B("So how do we get back to what he paid?",
      ask=CHOOSE(["90 + 20", "90 − 20", "it is 20"], 1,
                 "He made a profit, so he paid less than the 90 rupees he got. Take the 20 rupees of profit off the 90.")),
    B("90 minus 20 is 70. He had paid 70 rupees for the pen.",
      *ANSC("l1", "90 − 20 = 70", 70), NOTE("l1", "70", "rupees")),
    B("The tempting slip is to add, because profit sounds like more. But the profit is already inside the 90. The cost is the smaller number."),
    B("Check: 70 rupees, plus a profit of 20, makes 90, the selling price.",
      W("l2", "70 + 20 = 90")),
    B("So with a profit, the cost price is the selling price take away the profit."),
)

# Sold for 150 at a loss of 30: cost price.
LESSONS["G5A_PROFITLOSS_006"] = LESSON(
    B("Sita sold a storybook for 150 rupees and made a loss of 30 rupees. How much had she paid for it?",
      GIVEN("q", "Sold for ₹150, loss ₹30. Cost price?")),
    B("She made a loss. So was the price she paid more than 150 rupees, or less?",
      ask=CHOOSE(["more than 150", "less than 150", "exactly 150"], 0,
                 "A loss means she got back less than she paid. She got 150 rupees, so she must have paid more than that.")),
    B("More. She got back 30 rupees less than she paid. So to find what she paid, we put those 30 rupees back.",
      LB("f", "Cost price = selling price + loss")),
    B("150 plus 30 is 180. She had paid 180 rupees for the storybook.",
      *ANSC("l1", "150 + 30 = 180", 180), NOTE("l1", "180", "rupees")),
    B("The tempting slip is to take away, because loss sounds like less. But the loss has already been taken off. The cost is the bigger number."),
    B("Check: she paid 180 and got 150. 180 minus 150 is 30, the loss in the story.",
      W("l2", "180 − 150 = 30")),
    B("So with a loss, the cost price is the selling price plus the loss."),
)
