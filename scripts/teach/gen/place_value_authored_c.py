"""Place-value lessons written by hand, part C: final papers 2020 to 2025 (EXT_G5_FP_...)."""
from place_value_lib import a, al, b, ch, fig, gl, nt, pchart, ring, tbl, ul, w, wl, x
from place_value_authored_b import walk_lesson

LESSONS = {}

# (x + 21) is odd: the 3rd even number after it  -> (x + 26)
LESSONS["EXT_G5_FP_2020_005"] = [
    b("There is a letter in this one, but it is really a counting puzzle.", gl("q", "(x + 21) is odd. The 3rd even number after it?")),
    b("We do not know x, but we do know x plus 21 is odd. Let's walk forward from it, one number at a time."),
    b("What kind of number comes right after an odd number?",
      ask=ch(["an even number", "another odd number"],
             "Odd and even numbers take turns, like left foot, right foot. After an odd number comes an even one.")),
    b("So the 1st even number is just 1 more: x plus 22.", wl("e1", "1st even:  x + 21 + 1  =  x + 22")),
    b("Even numbers are 2 apart. So the 2nd one is x plus 24.", wl("e2", "2nd even:  x + 22 + 2  =  x + 24")),
    b("And the 3rd is x plus 26. Careful: the first step was only 1, because we started on an odd number. After that the steps are 2.",
      wl("e3", "3rd even:  x + 24 + 2  =  x + 26")),
    b("Try it with a real number. If x is 2, then x plus 21 is 23. The even numbers after 23 are 24, 26, 28. And 2 plus 26 is 28.",
      w("c1", "2 + 21 = 23"), wl("c2", "after 23:  24, 26, 28"), w("c3", "2 + 26 = 28")),
    b("So the answer is x plus 26. One step to reach the first even number, then jumps of 2.",
      al("ans", "(x + 26)"), ring("ans", "x + 26")),
]

# Difference between the place values of 9 and 7 is 83000  -> 197000
LESSONS["EXT_G5_FP_2020_016"] = [
    b("Four numbers, each with a 9 and a 7. In one of them, the place values of the 9 and the 7 differ by 83000.",
      gl("q", "place value of 9 − place value of 7 = 83000"), gl("opts", "1907000   109700   197000   91700")),
    b("Think first. Which two place values have a difference of 83000?",
      ask=ch(["90000 and 7000", "9000 and 700", "900000 and 7000"],
             "Try them. 90000 minus 7000 is 83000. The other pairs give differences that are too small or too big.")),
    b("90000 minus 7000 is 83000. So the 9 must be worth 90000 and the 7 must be worth 7000.", w("t", "90000 − 7000 = 83000")),
    b("That means 9 in the ten-thousands place, with 7 right beside it in the thousands place. Let's look for that pattern."),
    b("1907000: here the 9 is in the lakhs place, worth 900000. Far too much.", x("opts", "1907000")),
    b("109700: the 9 is only worth 9000. And in 91700 the 9 is right, but the 7 is only worth 700. Both out.",
      x("opts", "109700"), x("opts", "91700")),
    b("197000: 9 in the ten-thousands, 7 in the thousands. Exactly what we wanted.",
      ring("opts", "197000"), fig("chart", pchart("197000", hi=[1, 2]))),
    b("So the number is 197000. Working out what we needed first made the search quick.", a("ans", "197000"), ring("ans", "197000")),
]

# Two consecutive primes add up to 42  -> difference 4
LESSONS["EXT_G5_FP_2020_023"] = [
    b("Two prime numbers, next to each other in the list of primes, add up to 42. We want the difference between them.",
      gl("q", "two primes next to each other add up to 42")),
    b("If two numbers are close together and add up to 42, each must be close to half of 42. Half of 42 is 21.", w("h", "42 ÷ 2 = 21")),
    b("So one prime is a little below 21 and the other a little above. Which is the nearest prime below 21?",
      ask=ch(["19", "20", "17"], "20 is even, so it is not prime. 19 cannot be divided by anything, so it is the nearest prime below 21.")),
    b("Here are the numbers around 21. Cross out 20 and 22, which are even, and 21, which is 3 times 7. The primes left are 19 and 23.",
      wl("p", "19, 20, 21, 22, 23"), x("p", "20", "even"), x("p", "21", "3 × 7"), x("p", "22", "even"),
      ring("p", "19"), ring("p", "23")),
    b("19 plus 23 is 42. It fits! And there is no prime between them, so they really are next to each other.", w("s", "19 + 23 = 42")),
    b("Now the difference. 23 minus 19 is 4.", w("d", "23 − 19 = 4")),
    b("So the two primes differ by 4.", al("ans", "Difference = 4"), ring("ans", "4")),
    b("When two numbers have a known total, start from half of it and look on both sides."),
]

# Three consecutive natural numbers add up to 66  -> 23
LESSONS["EXT_G5_FP_2020_036"] = [
    b("Three numbers in a row add up to 66. We need to find them, then see which one is among the choices.",
      gl("q", "three numbers in a row add up to 66")),
    b("Three numbers in a row are balanced around the middle one. One is 1 less, one is 1 more. So together they equal 3 lots of the middle number."),
    b("So how do we find the middle number?",
      ask=ch(["66 ÷ 3", "66 − 3", "66 × 3"], "Three equal lots make 66. To find one lot, we share 66 into 3 equal parts.")),
    b("66 divided by 3 is 22. That is the middle number.", w("m", "66 ÷ 3 = 22")),
    b("One less is 21, and one more is 23. So the numbers are 21, 22 and 23.", wl("l", "21, 22, 23"), ring("l", "22")),
    b("Check by adding: 21 plus 22 plus 23 is 66.", w("c", "21 + 22 + 23 = 66")),
    b("Of our three numbers, the one offered in the choices is 23.", a("ans", "23"), ring("ans", "23")),
    b("For numbers in a row, divide the total by how many there are. That gives the middle one."),
]

# 555 digits in the page numbers: how many pages?  -> 221
LESSONS["EXT_G5_FP_2020_037"] = [
    b("Jack's book uses 555 digits for its page numbers. We work backwards to find how many pages there are.",
      gl("q", "page numbers use 555 digits. How many pages?")),
    b("Let's spend the 555 digits group by group. Pages 1 to 9 use 1 digit each. That is 9 digits.", w("g1", "9 × 1 = 9")),
    b("Next, the pages with 2 digits, from 10 up to 99. How many pages is that?",
      ask=ch(["90", "89", "99"], "From 1 to 99 there are 99 pages. Take away the first 9, and 90 pages are left.")),
    b("90 pages times 2 digits is 180. With the first 9, we have used 189 digits by page 99.",
      w("g2", "90 × 2 = 180"), w("g3", "9 + 180 = 189")),
    b("555 minus 189 leaves 366 digits for the pages with 3 digits.", w("r", "555 − 189 = 366")),
    b("Careful: 366 is a number of digits, not pages. Each of these pages takes 3 digits, and 366 divided by 3 is 122 pages.",
      w("p", "366 ÷ 3 = 122")),
    b("99 pages before, plus 122 more, makes 221.",
      w("t", "99 + 122 = 221"),
      fig("table", tbl(["pages", "how many", "digits"], [["1 to 9", "9", "9"], ["10 to 99", "90", "180"], ["100 to 221", "122", "366"]]))),
    b("So Jack's book has 221 pages. Use up the 1 digit and 2 digit pages first, then share what is left among the 3 digit pages.",
      al("ans", "221 pages"), ring("ans", "221")),
]

# Which number is divisible by 11?  -> 901351
LESSONS["EXT_G5_FP_2021_004"] = [
    b("Which of these four numbers can be divided exactly by 11? Dividing each one would take ages, so we use a test.",
      gl("q", "Which number is divisible by 11?"), gl("opts", "3116365   901351   11111   8790321")),
    b("Here is the test for 11. Add every other digit, starting with the first. Then add the digits you skipped. Take one total from the other."),
    b("If that difference is 0, or 11, or another multiple of 11, the number can be divided by 11.",
      wl("r", "difference 0 or 11: divisible by 11")),
    b("Try 3116365. Every other digit: 3, 1, 3, 5, which make 12. The skipped ones: 1, 6, 6, which make 13. The difference is only 1. Out.",
      w("a1", "3 + 1 + 3 + 5 = 12"), w("a2", "1 + 6 + 6 = 13"), x("opts", "3116365", "13 − 12 = 1")),
    b("Now 901351. Every other digit: 9, 1 and 5. What do they add up to?",
      ask=ch(["15", "14", "16"], "9 plus 1 is 10, and 5 more makes 15.")),
    b("15 for those. The skipped digits, 0, 3 and 1, make 4. And 15 minus 4 is 11. That passes the test!",
      w("b1", "9 + 1 + 5 = 15"), w("b2", "0 + 3 + 1 = 4"), w("b3", "15 − 4 = 11"), ring("opts", "901351")),
    b("A quick look at the others. 11111 gives 3 and 2, a difference of 1. 8790321 gives 21 and 9, a difference of 12. Both out.",
      x("opts", "11111", "3 − 2 = 1"), x("opts", "8790321", "21 − 9 = 12")),
    b("So the number is 901351. For 11: add alternate digits, subtract the two totals, and look for 0 or a multiple of 11.",
      a("ans", "901351"), ring("ans", "901351")),
]

# Two 6s: one worth 1000 times the other  -> 68762
LESSONS["EXT_G5_FP_2021_007"] = [
    b("Each of these numbers has two 6s. In only one of them is one 6 worth 1000 times the other.",
      gl("q", "one 6 = 1000 × the other 6"), gl("opts", "66728   68726   86762   68762")),
    b("Moving a digit one column to the left makes it worth 10 times more. To be worth 1000 times more, how many columns must it move?",
      w("s", "10 × 10 × 10 = 1000"),
      ask=ch(["3 columns", "2 columns", "4 columns"],
             "One column is times 10. Every extra column is times 10 again. It takes three of them to make 1000, so we need 3 columns.")),
    b("So we look for two 6s with a gap of 3 columns. In 66728 the 6s are neighbours. A gap of 1.", x("opts", "66728", "gap 1")),
    b("In 68726 one 6 is in the ten-thousands and the other in the units. A gap of 4. Too wide.", x("opts", "68726", "gap 4")),
    b("In 86762 they are in the thousands and the tens. A gap of 2. Not enough.", x("opts", "86762", "gap 2")),
    b("In 68762 they are in the ten-thousands and the tens. A gap of 3. That is the one!",
      ring("opts", "68762"), fig("chart", pchart("68762", hi=[0, 3]))),
    b("Check with the real values: 60000 and 60. 60000 divided by 60 is 1000.", w("v", "60000 ÷ 60 = 1000")),
    b("So the number is 68762. With the same digit, count the columns between them: each column is one more times 10.",
      a("ans", "68762"), ring("ans", "68762")),
]

# A number made only of 4s, divisible by 18: fewest 4s  -> 9
LESSONS["EXT_G5_FP_2021_026"] = [
    b("A number made only of 4s, like 444, that can be divided exactly by 18. What is the fewest 4s it can have?",
      gl("q", "444…4 is divisible by 18. Fewest 4s?")),
    b("18 is 2 times 9. So our number must be divisible by 2, and also by 9.", w("f", "18 = 2 × 9")),
    b("Divisible by 2 is easy. The number ends in 4, which is even. So that part is always fine."),
    b("Now the 9. What is the test for dividing by 9?",
      ask=ch(["the digit sum is a multiple of 9", "the last digit is 9", "the number ends in 0"],
             "For 9, we add up all the digits. If that total is in the 9 times table, the number can be divided by 9.")),
    b("Every digit is a 4, so the digit sum climbs in fours. We need the first total that is also in the 9 times table.",
      wl("m", "4, 8, 12, 16, 20, 24, 28, 32, 36")),
    b("36 is the first one. It is 4 times 9, so it takes 9 fours to get there.", ring("m", "36"), w("c", "4 × 9 = 36")),
    b("So the smallest such number has 9 fours.", al("ans", "9 fours:  444444444"), ring("ans", "9")),
    b("Split 18 into 2 and 9, and test each one. The 2 was free, and the 9 test did all the work."),
]

LESSONS["EXT_G5_FP_2022_008"] = walk_lesson("EXT_G5_FP_2022_008", "Z", 41, "even", 19, False, "(Z + 4)", 1)

# How many odd three-digit square numbers?  -> None of these (there are 11)
LESSONS["EXT_G5_FP_2022_009"] = [
    b("A square number is a number times itself. We are counting the squares that have 3 digits and are odd.",
      gl("q", "odd 3-digit square numbers: how many?")),
    b("First, which squares have 3 digits? 10 times 10 is 100, the smallest 3 digit number. So we start at 10.", w("lo", "10 × 10 = 100")),
    b("31 times 31 is 961, still 3 digits. But 32 times 32 is 1024, which is too long. So we stop at 31.",
      w("hi", "31 × 31 = 961"), w("ov", "32 × 32 = 1024"), x("ov", "1024", "4 digits")),
    b("Now, which numbers give an odd square?",
      ask=ch(["odd numbers", "even numbers", "all numbers"],
             "Odd times odd is odd, and even times even is even. So only an odd number has an odd square.")),
    b("So we need the odd numbers from 10 to 31. Here they are, starting at 11 and ending at 31.",
      wl("l", "11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31")),
    b("Count along the list and you will find 11 numbers. Each one gives an odd square, so there are 11 odd squares with 3 digits.",
      w("n", "(31 − 11) ÷ 2 + 1 = 11")),
    b("Now look at the choices: 10, 12 and 13. Our 11 is not there!", wl("o", "choices: 10, 12, 13, None of these")),
    b("So the answer is 'None of these'. Trust your working: when your number is not on the list, that is the right choice.",
      al("ans", "11 squares, so: None of these"), ring("ans", "None of these")),
]

# Sixty-seven lakhs, ninety-four thousand, five hundred and twenty-one: place value of the middle digit  -> 4000
LESSONS["EXT_G5_FP_2022_025"] = [
    b("The number is given in words: sixty-seven lakhs, ninety-four thousand, five hundred and twenty-one. First we turn it into digits.",
      gl("q", "67 lakh, 94 thousand, 5 hundred and 21")),
    b("In the Indian system we write it with commas like this: 67 for the lakhs, 94 for the thousands, then the last three digits.",
      w("n", "67,94,521")),
    b("How many digits does the number have?",
      ask=ch(["7", "6", "8"], "Count them one by one: 6, 7, 9, 4, 5, 2, 1. That is 7 digits.")),
    b("7 digits, so the middle one is the 4th, with 3 digits on each side of it. That is the 4.", ul("n", "4"), nt("n", "4", "middle")),
    b("Now, which column is the 4 in? Units, tens, hundreds, thousands. It is in the thousands place.",
      fig("chart", pchart("6794521", hi=[3]))),
    b("4 thousands: 4 times 1000 is 4000.", w("pv", "4 × 1000 = 4000")),
    b("Careful: the 9 beside it is in the ten-thousands place. They are neighbours, so it is easy to mix them up.",
      al("ans", "Place value of 4 = 4000"), ring("ans", "4000")),
    b("So the place value is 4000. Write the number in digits first, find the middle, then name its column."),
]

# Sum of the numbers divisible by 3 among 861, 435, 218, 764 and 1263  -> 2559
LESSONS["EXT_G5_FP_2022_032"] = [
    b("Five numbers. We keep only the ones that 3 divides exactly, and then add those up.", gl("q", "861   435   218   764   1263")),
    b("What is the quick test for dividing by 3?",
      ask=ch(["add the digits", "look at the last digit", "halve the number"],
             "For 3, the last digit does not help. Add up the digits: if the total is in the 3 times table, so is the number.")),
    b("861: 8 plus 6 plus 1 is 15. 435: 4 plus 3 plus 5 is 12. Both totals are in the 3 times table, so we keep both.",
      w("t1", "8 + 6 + 1 = 15"), w("t2", "4 + 3 + 5 = 12"), ring("q", "861"), ring("q", "435")),
    b("218 gives 11, and 764 gives 17. Neither is a multiple of 3, so cross them out.",
      w("t3", "2 + 1 + 8 = 11"), w("t4", "7 + 6 + 4 = 17"), x("q", "218"), x("q", "764")),
    b("1263 gives 12. Keep it.", w("t5", "1 + 2 + 6 + 3 = 12"), ring("q", "1263")),
    b("Now add the three we kept. 861 plus 435 is 1296. Then 1296 plus 1263 is 2559.",
      w("s1", "861 + 435 = 1296"), w("s2", "1296 + 1263 = 2559")),
    b("So the sum is 2559.", a("ans", "2559"), ring("ans", "2559")),
    b("Test with the digit sum, keep the ones that pass, then add. Sorting first keeps the adding small."),
]

LESSONS["EXT_G5_FP_2023_011"] = walk_lesson("EXT_G5_FP_2023_011", "M", 46, "odd", 19, False, "M + 9", 1, prime_note=True)

# Product of all the one-digit factors of 48  -> 1152
LESSONS["EXT_G5_FP_2023_012"] = [
    b("We want every one digit factor of 48, all multiplied together. A factor of 48 is a number that divides 48 exactly.",
      gl("q", "one-digit factors of 48, all multiplied")),
    b("Let's test each one digit number, 1 to 9.", wl("l", "1  2  3  4  5  6  7  8  9")),
    b("Which of these does not divide 48?",
      ask=ch(["5", "6", "8"], "48 does not end in 0 or 5, so 5 does not divide it. But 6 times 8 is 48, so 6 and 8 both do.")),
    b("5, 7 and 9 do not divide 48, so cross them out. The factors left are 1, 2, 3, 4, 6 and 8.",
      x("l", "5"), x("l", "7"), x("l", "9")),
    b("Now multiply them, in friendly groups. 1 times 2 times 3 times 4 is 24. And 6 times 8 is 48.",
      w("g1", "1 × 2 × 3 × 4 = 24"), w("g2", "6 × 8 = 48")),
    b("So we need 24 times 48. 24 times 50 is 1200. That is 2 lots of 24 too many, so take away 48. We get 1152.",
      w("m1", "24 × 50 = 1200"), w("m2", "1200 − 48 = 1152"), w("m3", "24 × 48 = 1152")),
    b("So the product is 1152.", a("ans", "1152"), ring("ans", "1152")),
    b("List, test, cross out, then multiply in easy groups. And notice the 1: it is a factor, but it changes nothing."),
]

# Place value of 6 in (greatest 2-digit prime) × (greatest 3-digit number)  -> 6000
LESSONS["EXT_G5_FP_2023_027"] = [
    b("Three steps: find two special numbers, multiply them, then find what the 6 in the answer is worth.",
      gl("q", "(greatest 2-digit prime) × (greatest 3-digit number)")),
    b("The greatest 3 digit number is easy. It is 999.", wl("g3", "greatest 3-digit number: 999")),
    b("Now the greatest 2 digit prime. Which is it?",
      ask=ch(["97", "99", "91"],
             "99 can be divided by 9, and 91 can be divided by 7. 97 cannot be divided by anything, so it is the greatest 2 digit prime.")),
    b("So we need 97 times 999.", wl("g2", "greatest 2-digit prime: 97")),
    b("999 is just 1 less than 1000. So take 97 thousands, and then take away one 97. That leaves 96903.",
      w("m1", "97 × 1000 = 97000"), w("m2", "97000 − 97 = 96903")),
    b("Now find the 6 in 96903. Units, tens, hundreds, thousands. It is in the thousands place.",
      fig("chart", pchart("96903", hi=[1])), ul("m2", "6"), nt("m2", "6", "thousands")),
    b("6 thousands: 6 times 1000 is 6000.", w("pv", "6 × 1000 = 6000")),
    b("So the place value of the 6 is 6000. Multiplying by 999 is easy when you think of it as 1000 take away 1.",
      al("ans", "Place value of 6 = 6000"), ring("ans", "6000")),
]

# Smallest 5-digit even number from 7, 4, 3, 6, 9: the digit in the hundreds place  -> 7
LESSONS["EXT_G5_FP_2023_034"] = [
    b("We build the smallest 5 digit even number from 7, 4, 3, 6 and 9. Then we read off its hundreds digit.",
      gl("q", "digits 7, 4, 3, 6, 9: smallest 5-digit even number")),
    b("Even means it ends in an even digit. Ours are 4 and 6, so one of them goes last.", wl("c", "last digit: 4 or 6")),
    b("The smallest digit, 3, goes first. We would like 4 to come next. So which even digit should go last?",
      ask=ch(["6", "4"],
             "If 4 went last, we could not use it near the front, where it keeps the number small. So we save the 4 and put 6 at the end.")),
    b("3, then 4, then 7 and 9 in rising order, and 6 at the end. That makes 34796.", w("n", "34796")),
    b("Compare it with putting 4 at the end. The best we could do then is 36794, and ours is smaller.", w("k", "34796 < 36794")),
    b("Now the hundreds place. Units, tens, hundreds: the third digit from the right is 7.",
      fig("chart", pchart("34796", hi=[2])), ul("n", "7"), nt("n", "7", "hundreds")),
    b("So the digit in the hundreds place is 7.", al("ans", "Hundreds digit = 7"), ring("ans", "7")),
    b("Choose the last digit so that the small digits stay free for the front. Then count the places from the right."),
]

# 7th odd number after 54, plus the 12th even number before 65  -> 109
LESSONS["EXT_G5_FP_2024_007"] = [
    b("Two little hunts, then one addition. First the 7th odd number after 54, then the 12th even number before 65.",
      gl("q", "(7th odd number after 54) + (12th even number before 65)")),
    b("The odd numbers after 54 are short enough to list: 55, 57, 59, 61, 63, 65, 67. The 7th one is 67.",
      wl("o", "55, 57, 59, 61, 63, 65, 67"), ring("o", "67")),
    b("Now the even numbers before 65. Counting backwards, they start at 64 and go down in jumps of 2.", wl("e", "64, 62, 60, …")),
    b("64 is the 1st. How many jumps back do we need to reach the 12th?",
      ask=ch(["11 jumps", "12 jumps", "13 jumps"],
             "The 1st is already there with no jump at all. Each jump after that gives one more, so the 12th needs 11 jumps.")),
    b("11 jumps of 2 is 22. And 64 minus 22 is 42.", w("j", "11 × 2 = 22"), w("d", "64 − 22 = 42")),
    b("Now add the two answers. 67 plus 42 is 109.", w("s", "67 + 42 = 109")),
    b("So the sum is 109.", a("ans", "109"), ring("ans", "109")),
    b("When you count along a list, the jumps are always one fewer than the position."),
]

# Place value of 4 in the square of the greatest 2-digit prime  -> 400
LESSONS["EXT_G5_FP_2024_011"] = [
    b("Three steps: find the greatest 2 digit prime, square it, and then find what the 4 in the answer is worth.",
      gl("q", "square of the greatest 2-digit prime")),
    b("Which is the greatest 2 digit prime?",
      ask=ch(["97", "99", "93"], "99 can be divided by 9, and 93 by 3. 97 cannot be divided by anything, so it is the greatest 2 digit prime.")),
    b("So we must square 97. That means 97 times 97.", wl("p", "greatest 2-digit prime: 97")),
    b("97 is 3 less than 100. So take 97 hundreds, 9700, and take away 3 lots of 97, which is 291. That leaves 9409.",
      w("m1", "97 × 100 = 9700"), w("m2", "3 × 97 = 291"), w("m3", "9700 − 291 = 9409")),
    b("So the square is 9409. Now find the 4.", w("sq", "97 × 97 = 9409"), fig("chart", pchart("9409", hi=[1]))),
    b("Units, tens, hundreds. The 4 is in the hundreds place, so it is worth 4 times 100, which is 400.",
      w("pv", "4 × 100 = 400")),
    b("So the place value of the 4 is 400.", al("ans", "Place value of 4 = 400"), ring("ans", "400")),
    b("Find the number, do the sum, then read the place. Take one step at a time and a long question becomes easy."),
]

# Two-digit primes whose digit sum is more than 10  -> 8
LESSONS["EXT_G5_FP_2024_025"] = [
    b("We go through the 2 digit primes and keep the ones whose digits add up to more than 10.",
      gl("q", "2-digit primes with digit sum more than 10")),
    b("More than 10 means 11 or bigger. Keep that in mind.", wl("r", "digit sum must be 11 or more")),
    b("Small primes have small digit sums, so the first ones that pass are these. 29 gives 11, 47 gives 11, 59 gives 14 and 67 gives 13.",
      wl("k1", "29→11   47→11   59→14   67→13")),
    b("Carrying on: 79 gives 16, 83 gives 11, 89 gives 17 and 97 gives 16.", wl("k2", "79→16   83→11   89→17   97→16")),
    b("What about 19, 37 and 73? Each has a digit sum of exactly 10. Do they count?",
      wl("t", "19→10   37→10   73→10"),
      ask=ch(["No, 10 is not more than 10", "Yes, 10 is enough"],
             "The question says more than 10. A sum of exactly 10 is not more than 10, so these three stay out.")),
    b("So cross them out. This is the trap in the question.", x("t", "19→10   37→10   73→10", "not more than 10")),
    b("Count the ones we kept: 4 in the first row and 4 in the second. That makes 8.", w("n", "4 + 4 = 8")),
    b("So there are 8 such primes. Read the words 'more than' carefully: they shut the door on exactly 10.",
      al("ans", "8 primes"), ring("ans", "8")),
]

# Sum of all the one-digit factors of 72  -> 33
LESSONS["EXT_G5_FP_2024_039"] = [
    b("We want every one digit factor of 72, added together. A factor of 72 is a number that divides 72 exactly.",
      gl("q", "one-digit factors of 72, all added")),
    b("Test each one digit number, 1 to 9.", wl("l", "1  2  3  4  5  6  7  8  9")),
    b("Does 9 divide 72?",
      ask=ch(["Yes, 9 × 8 = 72", "No, it does not"], "9 times 8 is 72. So 9 is a factor, and so is its partner 8.")),
    b("72 does not end in 0 or 5, so 5 is out. And 72 is not in the 7 times table, so 7 is out. Everything else divides 72.",
      x("l", "5"), x("l", "7")),
    b("Now add the ones left: 1, 2, 3, 4, 6, 8 and 9. Make it easy. 1 and 9 are 10, 2 and 8 are 10. That is 20.",
      w("s1", "(1 + 9) + (2 + 8) = 20")),
    b("Then 3, 4 and 6 make 13. And 20 plus 13 is 33.", w("s2", "3 + 4 + 6 = 13"), w("s3", "20 + 13 = 33")),
    b("So the sum is 33.", a("ans", "33"), ring("ans", "33")),
    b("List, test, cross out, then add in friendly pairs that make 10."),
]

# (sum of one-digit odd numbers) × (greatest 2-digit prime): place value of the hundreds digit  -> 400
LESSONS["EXT_G5_FP_2025_001"] = [
    b("A recipe with three steps: add, multiply, then look at the hundreds place of the answer.",
      gl("q", "(sum of 1-digit odd numbers) × (greatest 2-digit prime)")),
    b("The one digit odd numbers are 1, 3, 5, 7 and 9. Together they make 25.", w("s", "1 + 3 + 5 + 7 + 9 = 25")),
    b("And which is the greatest 2 digit prime?",
      ask=ch(["97", "99", "95"], "99 can be divided by 9, and 95 by 5. 97 cannot be divided by anything, so it is the one.")),
    b("So we need 25 times 97. 97 is 3 less than 100. 25 hundreds is 2500. Take away 25 threes, which is 75, and we get 2425.",
      w("m1", "25 × 100 = 2500"), w("m2", "25 × 3 = 75"), w("m3", "2500 − 75 = 2425")),
    b("Now the hundreds place of 2425. Units, tens, hundreds: the digit there is 4.",
      w("n", "25 × 97 = 2425"), fig("chart", pchart("2425", hi=[1])), ul("n", "4"), nt("n", "4", "hundreds")),
    b("4 hundreds: 4 times 100 is 400.", w("pv", "4 × 100 = 400")),
    b("So the place value of the hundreds digit is 400.", al("ans", "Place value = 400"), ring("ans", "400")),
    b("Careful with the last step: the question wants the place value, 400, and not just the digit 4."),
]

# 12th even number after 99, plus the 18th even number before 99  -> 186
LESSONS["EXT_G5_FP_2025_015"] = [
    b("Two hunts and then an addition: the 12th even number after 99, and the 18th even number before 99.",
      gl("q", "(12th even after 99) + (18th even before 99)")),
    b("Start with the even numbers after 99. The first one is 100, and they go up in jumps of 2.", wl("u", "100, 102, 104, …")),
    b("100 is the 1st. How many jumps of 2 take us to the 12th?",
      ask=ch(["11", "12", "13"], "The 1st needs no jump at all. So the 12th needs one fewer than 12, which is 11 jumps.")),
    b("11 jumps of 2 is 22. And 100 plus 22 is 122.", w("j1", "11 × 2 = 22"), w("a1", "100 + 22 = 122")),
    b("Now go backwards from 99. The first even number before it is 98. For the 18th we need 17 jumps back.",
      wl("d", "98, 96, 94, …"), w("j0", "18 − 1 = 17")),
    b("17 jumps of 2 is 34. And 98 minus 34 is 64.", w("j2", "17 × 2 = 34"), w("a2", "98 − 34 = 64")),
    b("Add the two: 122 plus 64 is 186.", w("s", "122 + 64 = 186")),
    b("So the sum is 186. The 1st one costs no jumps, so always use one fewer jump than the position.",
      a("ans", "186"), ring("ans", "186")),
]
