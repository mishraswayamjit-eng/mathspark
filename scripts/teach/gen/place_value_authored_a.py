"""Place-value lessons written by hand, part A: the worksheet one-offs (EXT_G5_WS_...).

Each lesson is a list of beats. In every ask the FIRST choice is the right one;
place_value_lib.finish() moves it to a varied position when the part is built.
"""
from place_value_lib import a, al, b, ch, fig, g, gl, nt, pchart, ring, tbl, ul, w, wl, x

LESSONS = {}

PLACES4 = ["thousands", "hundreds", "tens", "units"]

# How many tens form six hundred hundreds?  -> 6000
LESSONS["EXT_G5_WS_01_001"] = [
    b("Six hundred hundreds. That sounds like a tongue twister, so let's turn it into numbers.",
      gl("q", "six hundred hundreds = how many tens?")),
    b("Six hundred is 600, and one hundred is 100. So six hundred hundreds means 600 lots of 100. What is 600 times 100?",
      wl("m", "600 hundreds = 600 × 100"),
      ask=ch(["60,000", "6000", "600"],
             "Times 100 puts 2 more zeros on the end. 600 with 2 more zeros is 60,000.")),
    b("600 times 100 is 60,000. Two more zeros on the end.", w("t", "600 × 100 = 60,000")),
    b("Careful: 60,000 is the whole amount, not the number of tens. How do we find how many tens are inside it?",
      ask=ch(["divide by 10", "multiply by 10", "divide by 100"],
             "Each ten is a group of 10. To see how many groups of 10 fit into a number, we divide it by 10.")),
    b("Dividing by 10 takes one zero off the end. 60,000 becomes 6000.", w("d", "60,000 ÷ 10 = 6000")),
    b("Check by going back: 6000 tens is 6000 times 10, which is 60,000. That is our six hundred hundreds.",
      w("c", "6000 × 10 = 60,000")),
    b("So 6000 tens form six hundred hundreds. Turn the words into a number first, then ask how many tens fit in.",
      al("ans", "6000 tens"), ring("ans", "6000")),
]

# Which digit has the same place value and face value wherever it is?  -> 0
LESSONS["EXT_G5_WS_01_002"] = [
    b("We want a digit whose place value and face value are the same, wherever it sits. Face value is the digit as it looks. Place value is what it is worth in its column.",
      gl("q", "place value = face value, in every place?")),
    b("Let's test 9. Put it in the tens place. Now it is worth 9 times 10, which is 90, but its face is still 9. Not the same.",
      fig("chart", pchart("90", hi=[0])), w("n", "9 × 10 = 90")),
    b("Now try 1 in the tens place. Is its place value the same as its face value?",
      ask=ch(["No, it is worth 10", "Yes, it is worth 1"],
             "1 in the tens column means one ten. That is worth 10, not 1.")),
    b("1 in the tens place is worth 10, but its face value is 1. So 1 does not work either.", w("o", "1 × 10 = 10")),
    b("Now zero. Put 0 in the tens place, the hundreds place, the thousands place. 0 times 10 is 0. 0 times 100 is 0. 0 times 1000 is 0.",
      w("z1", "0 × 10 = 0"), w("z2", "0 × 100 = 0"), w("z3", "0 × 1000 = 0")),
    b("Zero times anything is zero. So the place value of 0 is always 0, and its face value is 0 as well. They match in every column.",
      ring("z1", "0", 3), ring("z2", "0", 4), ring("z3", "0", 5)),
    b("So the digit is 0.", al("ans", "The digit 0"), ring("ans", "0")),
    b("In the units place every digit matches its face value. But only zero keeps them equal everywhere."),
]

# If the place value of a digit is odd, which place is it in?  -> Units place
LESSONS["EXT_G5_WS_01_003"] = [
    b("A digit has an odd place value. Which column could it be sitting in? Let's try a digit, say 7, in different columns and see.",
      gl("q", "The place value is odd. Which place?")),
    b("In the tens place, 7 is worth 7 times 10, which is 70. Is 70 odd or even?",
      w("t", "7 × 10 = 70"),
      ask=ch(["even", "odd"], "70 ends in 0, and any number ending in 0 can be halved exactly. So it is even.")),
    b("Even. In fact anything times 10 ends in 0, so a place value in the tens column is always even."),
    b("Hundreds and thousands tell the same story. 700 and 7000 both end in zeros, so they are even too.",
      w("h", "7 × 100 = 700"), w("th", "7 × 1000 = 7000")),
    b("But in the units place, 7 is worth just 7. No zero on the end, and 7 is odd.",
      w("u", "7 × 1 = 7"), ring("u", "7", 2)),
    b("Careful: the digit itself must be odd too. A 4 in the units place is worth 4, which is even. But the units place is the only one where odd is possible at all.",
      w("f", "4 × 1 = 4")),
    b("So a digit with an odd place value must be in the units place.", al("ans", "Units place"), ring("ans", "Units place")),
    b("Tens, hundreds and beyond always end in zero, so they are always even. Odd place values live only in the units place."),
]

# In 69512, difference between the digits with the greatest and least place values  -> 4
LESSONS["EXT_G5_WS_01_004"] = [
    b("Here is 69512. We need two special digits: the one with the greatest place value, and the one with the least.", g("n", "69512")),
    b("Place value depends on the column. The column furthest left is worth the most, and the column furthest right is worth the least.",
      fig("chart", pchart("69512", hi=[0, 4]))),
    b("So which digit has the greatest place value?",
      ask=ch(["6", "9", "2"],
             "9 is the biggest digit to look at, but it sits in the thousands. The 6 is in the ten-thousands, so the 6 is worth more.")),
    b("The 6 is worth 60000. The 9 is only worth 9000. Don't let the big 9 fool you.",
      w("a", "6 × 10000 = 60000"), w("c", "9 × 1000 = 9000"), ul("n", "6"), nt("n", "6", "greatest", "above")),
    b("And the least place value is in the units column. That is the 2, worth just 2.", ul("n", "2"), nt("n", "2", "least", "below")),
    b("The question asks for the difference between the digits themselves. 6 minus 2 is 4.", w("d", "6 − 2 = 4")),
    b("So the difference is 4.", al("ans", "Difference = 4"), ring("ans", "4")),
    b("Greatest place value means furthest left. Least means furthest right. The size of the digit does not decide it."),
]

# In 76025, how many times is the place value of 6 to that of 2?  -> 300
LESSONS["EXT_G5_WS_01_005"] = [
    b("Here is 76025. We are comparing the place value of the 6 with the place value of the 2.",
      g("n", "76025"), ul("n", "6"), nt("n", "6", "thousands", "above"), ul("n", "2"), nt("n", "2", "tens", "below")),
    b("Here they are in the chart. The 6 sits in the thousands column. What is it worth?",
      fig("chart", pchart("76025", hi=[1, 3])),
      ask=ch(["6000", "600", "6"],
             "Count the columns from the right: units, tens, hundreds, thousands. So the 6 means 6 thousands.")),
    b("6 times 1000 is 6000. And the 2 is in the tens column, so it is worth 2 times 10, which is 20.",
      w("va", "6 × 1000 = 6000"), w("vb", "2 × 10 = 20")),
    b("Now, how many times 20 is 6000? Which sum tells us?",
      ask=ch(["6000 ÷ 20", "6 ÷ 2", "6000 − 20"],
             "Dividing the digits, 6 by 2, forgets their columns. We must divide the place values: 6000 by 20.")),
    b("6000 divided by 20. Cross one zero off each to make it easy: 600 divided by 2 is 300.",
      w("d", "6000 ÷ 20 = 300"), w("e", "600 ÷ 2 = 300")),
    b("Check it: 300 times 20 gives back 6000. It works.", w("c", "300 × 20 = 6000")),
    b("So the place value of the 6 is 300 times the place value of the 2.", al("ans", "300 times"), ring("ans", "300")),
    b("Two place values first, then one division. Dividing the digits alone would have given 3, and missed by a long way."),
]

# Two 8s: in which number is one 8 worth 1000 times the other?  -> 81586
LESSONS["EXT_G5_WS_01_006"] = [
    b("Four numbers, each with two 8s. In just one of them, one 8 is worth a thousand times the other 8.",
      gl("q", "one 8 = 1000 × the other 8"), gl("opts", "68815   65818   81586   85168")),
    b("Here is the key. Each step to the left makes a digit worth 10 times more, and 10 times 10 times 10 is 1000. So how far apart must the two 8s be?",
      w("s", "10 × 10 × 10 = 1000"),
      ask=ch(["3 columns apart", "2 columns apart", "4 columns apart"],
             "Each column is one more times 10. We need times 10 three times over to reach 1000, so the 8s are 3 columns apart.")),
    b("So we just hunt for two 8s that are 3 columns apart. In 68815 the 8s are side by side, only 1 apart. Out.",
      x("opts", "68815", "1 apart")),
    b("65818 has one 8 in the hundreds and one in the units. That is 2 apart. Out.", x("opts", "65818", "2 apart")),
    b("81586 has one 8 in the ten-thousands and one in the tens. Count the steps between them: 3. This looks right!",
      ring("opts", "81586"), fig("chart", pchart("81586", hi=[0, 3]))),
    b("Check with the real values. The first 8 is worth 80000 and the other is worth 80. 80000 divided by 80 is 1000.",
      w("v", "80000 ÷ 80 = 1000")),
    b("And in 85168 the 8s are 4 apart, which would be ten thousand times. So that one is out too.", x("opts", "85168", "4 apart")),
    b("So the number is 81586. The digit is the same both times, so only the gap between the columns matters.",
      a("ans", "81586"), ring("ans", "81586")),
]

# Two 3s: one worth 100 times the other  -> 863135
LESSONS["EXT_G5_WS_01_007"] = [
    b("Four numbers, and each has more than one 3. We want the one where one 3 is worth a hundred times another 3.",
      gl("q", "one 3 = 100 × the other 3"), gl("opts", "134639   752339   863135   307638")),
    b("Each column to the left is worth 10 times more, and 10 times 10 is 100. So how far apart must the 3s be?",
      w("s", "10 × 10 = 100"),
      ask=ch(["2 columns apart", "1 column apart", "3 columns apart"],
             "One step left is times 10. Two steps is times 10 and times 10 again, which is times 100. So 2 columns apart.")),
    b("134639: its 3s are in the ten-thousands and the tens. That is 3 apart. Too far.", x("opts", "134639", "3 apart")),
    b("752339: the two 3s are next door to each other. Only 1 apart.", x("opts", "752339", "1 apart")),
    b("863135: one 3 in the thousands, one in the tens. 2 apart. Promising!",
      ring("opts", "863135"), fig("chart", pchart("863135", hi=[2, 4]))),
    b("Check with the values. The first 3 is worth 3000, the other is worth 30. 3000 divided by 30 is 100.",
      w("v", "3000 ÷ 30 = 100")),
    b("And 307638 has one 3 in the lakhs place and one in the tens, 4 apart. Out.", x("opts", "307638", "4 apart")),
    b("So the number is 863135. To be 100 times bigger, the same digit must sit exactly 2 columns to the left.",
      a("ans", "863135"), ring("ans", "863135")),
]

# Successor of the greatest 4-digit number from 1, 5, 0, 8  -> 8511
LESSONS["EXT_G5_WS_01_011"] = [
    b("Two jobs here. First build the greatest number from the digits 1, 5, 0 and 8. Then find its successor.",
      gl("q", "digits 1, 5, 0, 8: greatest number, then its successor")),
    b("For the greatest number, the biggest digit should go where it is worth the most: the thousands place. Which digit goes first?",
      ask=ch(["8", "5", "1"], "The thousands place is worth the most, so it deserves the biggest digit we have. That is 8.")),
    b("Then the next biggest in the hundreds, and so on down: 8, 5, 1, 0. That gives 8510.",
      w("n", "8510"), fig("chart", pchart("8510"))),
    b("Now, successor. That is simply the number that comes next when we count. So we add 1.", w("s", "8510 + 1 = 8511")),
    b("Careful: the successor does not have to use our four digits. 8511 has two 1s, and that is fine. It is just the next number."),
    b("So the answer is 8511.", a("ans", "8511"), ring("ans", "8511")),
    b("Greatest number: biggest digits first. Successor: add 1. Two small steps."),
]

# Middle digit of the greatest odd number from 5, 8, 0, 7, 4  -> 4
LESSONS["EXT_G5_WS_01_012"] = [
    b("We build the greatest odd number from 5, 8, 0, 7 and 4, and then look at its middle digit.",
      gl("q", "digits 5, 8, 0, 7, 4: greatest odd number")),
    b("Whether a number is odd is decided by one digit only. Which one?",
      ask=ch(["the last digit", "the first digit", "the middle digit"],
             "A number is odd when its units digit is odd. The other digits make no difference.")),
    b("So the last digit must be odd. Our odd digits are 5 and 7.", wl("c", "last digit: 5 or 7")),
    b("We want the number as big as possible. So which odd digit should we spend on the units place?",
      ask=ch(["5, the smaller one", "7, the bigger one"],
             "The units place is worth the least. So we give it the smaller odd digit, 5, and keep the 7 for a place that is worth more.")),
    b("With 5 at the end, arrange the rest from biggest to smallest: 8, 7, 4, 0. That makes 87405.",
      w("n", "87405"), fig("chart", pchart("87405", hi=[2]))),
    b("Compare it with putting 7 last, which gives 85407. That is smaller, so 87405 wins.", w("k", "87405 > 85407")),
    b("Now the middle. There are 5 digits, so the middle one is the third: 4.",
      ul("n", "4"), nt("n", "4", "middle"), al("ans", "Middle digit = 4"), ring("ans", "4")),
    b("Decide the last digit first, using the smaller odd digit. Then line the others up, biggest first."),
]

# Place value of 7 in the smallest even number from 2, 7, 3, 9, 6  -> 700
LESSONS["EXT_G5_WS_01_013"] = [
    b("First we build the smallest even number from 2, 7, 3, 9 and 6. Then we find what its 7 is worth.",
      gl("q", "digits 2, 7, 3, 9, 6: smallest even number")),
    b("Even means the last digit is even. Our even digits are 2 and 6, so one of them must go last.", wl("c", "last digit: 2 or 6")),
    b("For the smallest number, the 2 is precious. Where is it most useful?",
      ask=ch(["at the front", "at the end"],
             "The front place is worth the most, so the smallest digit should go there to keep the number small. That means the 6 goes last.")),
    b("So 6 goes at the end, and the others go from smallest to biggest: 2, 3, 7, 9. That makes 23796.", w("n", "23796")),
    b("Check the other choice. Ending in 2, the smallest we could make is 36792, and that is bigger.", w("k", "23796 < 36792")),
    b("Now find the 7. Count from the right: units, tens, hundreds. The 7 is in the hundreds place.",
      fig("chart", pchart("23796", hi=[2])), ul("n", "7"), nt("n", "7", "hundreds")),
    b("7 hundreds: 7 times 100 is 700.", w("pv", "7 × 100 = 700")),
    b("Careful: 'hundreds' is only the name of the place. The place value is the number, 700.",
      al("ans", "Place value of 7 = 700"), ring("ans", "700")),
    b("Build the number first, then read the place. Two questions hiding in one."),
]

# Two-digit even numbers with an odd tens digit  -> 25
LESSONS["EXT_G5_WS_01_014"] = [
    b("We are counting 2 digit numbers that are even, and have an odd digit in the tens place. Let's count the choices for each place.",
      gl("q", "2-digit even numbers with an odd tens digit")),
    b("The tens digit must be odd: 1, 3, 5, 7 or 9. That is 5 choices.", wl("t", "tens: 1, 3, 5, 7, 9")),
    b("The number must be even, so the units digit is even. How many choices are there for it?",
      ask=ch(["5", "4", "10"],
             "The even digits are 0, 2, 4, 6 and 8. Do not forget 0: it is even too. That makes 5.")),
    b("0, 2, 4, 6, 8. Five choices, and zero is one of them.", wl("u", "units: 0, 2, 4, 6, 8")),
    b("Each tens digit can pair with every one of those. Take tens digit 1: we get 10, 12, 14, 16, 18. That is 5 numbers.",
      wl("eg", "10, 12, 14, 16, 18")),
    b("The same happens for 3, 5, 7 and 9. So 5 tens digits, with 5 numbers each: 5 times 5 is 25.",
      fig("table", tbl(["tens", "units"], [["1, 3, 5, 7, 9", "0, 2, 4, 6, 8"], ["5 choices", "5 choices"]])),
      w("m", "5 × 5 = 25")),
    b("So there are 25 such numbers.", al("ans", "25 numbers"), ring("ans", "25")),
    b("Count the choices for each place, then multiply. No need to write out all 25."),
]

# 4-digit numbers from 7, 0, 3, 9 each once  -> 18
LESSONS["EXT_G5_WS_01_015"] = [
    b("Four digits, 7, 0, 3 and 9, each used once. How many different 4 digit numbers can we make? Let's fill the places one at a time, from the left.",
      gl("q", "digits 7, 0, 3, 9: how many 4-digit numbers?"),
      fig("table", tbl(PLACES4, [["?", "?", "?", "?"]]))),
    b("Start with the thousands place. How many of our digits are allowed there?",
      ask=ch(["3", "4", "1"],
             "0 cannot go first, because then the number would really have only 3 digits. So only 7, 3 or 9 can lead. 3 choices.")),
    b("Zero cannot lead, so the thousands place has 3 choices.", wl("p1", "thousands: 7, 3 or 9, so 3 choices")),
    b("One digit is used up, so 3 are left for the hundreds, and zero is welcome now. Then 2 are left for the tens, and 1 for the units.",
      wl("p2", "then 3 choices, then 2, then 1")),
    b("Multiply the choices. 3 times 3 is 9, times 2 is 18, times 1 is still 18.", w("m", "3 × 3 × 2 × 1 = 18")),
    b("Let's check one group. Starting with 7 we get 7039, 7093, 7309, 7390, 7903 and 7930: 6 numbers. The same for 3 and for 9.",
      wl("l", "7039, 7093, 7309, 7390, 7903, 7930"), w("c", "6 × 3 = 18")),
    b("So 18 different numbers can be formed.", al("ans", "18 numbers"), ring("ans", "18")),
    b("Go place by place from the left, count the choices, and multiply. Just remember that zero can never lead."),
]

# 4-digit numbers below 5000 from 2, 5, 0, 8  -> 6
LESSONS["EXT_G5_WS_01_016"] = [
    b("Digits 2, 5, 0 and 8, each used once. We want the 4 digit numbers that are less than 5000.",
      gl("q", "digits 2, 5, 0, 8: 4-digit numbers below 5000")),
    b("The thousands digit decides whether a number is below 5000. Which of our digits can go there?",
      ask=ch(["only 2", "2 or 0", "2 or 5"],
             "0 cannot lead a 4 digit number. And with 5 in front the number is at least 5000, which is not less than 5000. Only 2 works.")),
    b("So every one of our numbers starts with 2.",
      wl("p1", "thousands: only 2"), fig("table", tbl(PLACES4, [["2", "?", "?", "?"]]))),
    b("The digits 5, 0 and 8 fill the other three places. 3 choices for the hundreds, then 2 for the tens, then 1 for the units.",
      w("m", "3 × 2 × 1 = 6")),
    b("Let's list them to be sure: 2058, 2085, 2508, 2580, 2805, 2850.", wl("l", "2058, 2085, 2508, 2580, 2805, 2850")),
    b("Six numbers, and even the biggest, 2850, is well below 5000.", ring("l", "2850")),
    b("So 6 numbers can be formed.", al("ans", "6 numbers"), ring("ans", "6")),
    b("Deal with the place that has a rule first. Here that was the thousands place. Then count the rest and multiply."),
]

# Swap 5 and 6 in 469571  -> less by 9900
LESSONS["EXT_G5_WS_B2_011"] = [
    b("Here is 469571. We are going to swap its 5 and its 6, and see how the number changes.", g("n", "469571")),
    b("First, where are they? The 6 is in the ten-thousands place. The 5 is in the hundreds place.",
      fig("chart", pchart("469571", hi=[1, 3])),
      ul("n", "6"), nt("n", "6", "ten-thousands", "above"), ul("n", "5"), nt("n", "5", "hundreds", "below")),
    b("Swap them. Now the 5 is in the ten-thousands place and the 6 is in the hundreds place: 459671.", w("m", "459671")),
    b("Before we subtract anything: is the new number bigger or smaller?",
      ask=ch(["smaller", "bigger", "the same"],
             "Look at the ten-thousands place, the bigger of the two columns. It went down from 6 to 5. So the whole number went down.")),
    b("The ten-thousands place lost 1, so the number dropped by 10000. The hundreds place gained 1, so it rose by 100. Overall it fell by 9900.",
      w("d", "10000 − 100 = 9900")),
    b("Check by subtracting the whole numbers. 469571 minus 459671 is 9900.", w("c", "469571 − 459671 = 9900")),
    b("So the new number is less by 9900.", al("ans", "less by 9900"), ring("ans", "9900")),
    b("When two digits swap, only their two columns change. The bigger column tells you whether the number went up or down."),
]

# Notes numbered 40801 to 40901, each worth Rs. 5  -> Rs. 505
LESSONS["EXT_G5_WS_B3_010"] = [
    b("A bundle of 5 rupee notes, numbered from 40801 to 40901. Two steps: count the notes, then multiply by 5.",
      gl("q", "notes numbered 40801 to 40901, each Rs. 5")),
    b("So how many notes are there, from 40801 to 40901?",
      ask=ch(["101", "100", "99"],
             "Try it with small numbers. Notes 1 to 3 are 3 notes, but 3 minus 1 is only 2. We must add 1, to count the first note as well.")),
    b("40901 minus 40801 is 100. Then add 1 for the first note, 40801 itself. That makes 101 notes.",
      w("c1", "40901 − 40801 = 100"), w("c2", "100 + 1 = 101")),
    b("This is the trap in the question. Subtracting counts the steps between the notes, and there is always one more note than steps."),
    b("Now the money. 100 notes of 5 rupees make 500 rupees, and 1 more note makes 505.",
      w("m1", "100 × 5 = 500"), w("m2", "101 × 5 = 505")),
    b("So the bundle holds 505 rupees.", al("ans", "Rs. 505"), ring("ans", "505")),
    b("Counting from one number to another: subtract, then add 1, because both ends are in the bundle."),
]

# Digit 7 in the primes from 1 to 100  -> 9
LESSONS["EXT_G5_WS_B4_018"] = [
    b("Imagine writing out every prime number from 1 to 100. How many times would we write the digit 7? It can appear in the units place or in the tens place.",
      gl("q", "primes from 1 to 100: how many 7s are written?")),
    b("First, 7 in the units place. Here are all the numbers that end in 7. But not all of them are prime.",
      wl("u", "7, 17, 27, 37, 47, 57, 67, 77, 87, 97")),
    b("Which of these three is not a prime?",
      ask=ch(["27", "37", "67"], "27 is in the 3 times table, so it can be divided. 37 and 67 cannot be divided by anything.")),
    b("27, 57, 77 and 87 can all be divided, so they go. Six primes are left, and each has one 7.",
      x("u", "27", "3 × 9"), x("u", "57", "3 × 19"), x("u", "77", "7 × 11"), x("u", "87", "3 × 29")),
    b("Now 7 in the tens place: the seventies. The primes there are 71, 73 and 79. Three more 7s.", wl("t", "71, 73, 79")),
    b("6 and 3 make 9.", w("s", "6 + 3 = 9")),
    b("So the digit 7 is written 9 times.", al("ans", "9 times"), ring("ans", "9")),
    b("Sort the search by place: 7 in the units, then 7 in the tens. And 77, with its two 7s, never counted, because it is not prime."),
]

# Digit 3 in the two-digit primes  -> 8
LESSONS["EXT_G5_WS_B4_019"] = [
    b("Imagine writing out every 2 digit prime. How many times do we write the digit 3? Let's look at the units place first, then the tens place.",
      gl("q", "2-digit primes: how many 3s are written?")),
    b("Here are all the 2 digit numbers ending in 3.", wl("u", "13, 23, 33, 43, 53, 63, 73, 83, 93")),
    b("Three of these are in the 3 times table, so they are not prime. Which three?",
      ask=ch(["33, 63 and 93", "13, 43 and 73", "23, 53 and 83"],
             "Add the digits of each. 3 plus 3, 6 plus 3 and 9 plus 3 are all multiples of 3. So 33, 63 and 93 can be divided by 3.")),
    b("Cross them out. Six primes are left: 13, 23, 43, 53, 73 and 83. That is six 3s.",
      x("u", "33"), x("u", "63"), x("u", "93")),
    b("Next, 3 in the tens place: the thirties. The primes there are 31 and 37. Two more 3s.", wl("t", "31, 37")),
    b("6 and 2 make 8. And 33, the only number with two 3s, is not prime, so nothing was counted twice.", w("s", "6 + 2 = 8")),
    b("So the digit 3 is written 8 times.", al("ans", "8 times"), ring("ans", "8")),
    b("Split the search by place, units then tens, and throw out anything that is not prime."),
]

# Even numbers from all the one-digit primes, each once  -> 6
LESSONS["EXT_G5_WS_B4_020"] = [
    b("We use all the one digit primes, each exactly once, and count the even numbers we can make.",
      gl("q", "all 1-digit primes, each once: how many even numbers?")),
    b("First we need the one digit primes. Which list is right?",
      ask=ch(["2, 3, 5, 7", "1, 3, 5, 7", "3, 5, 7, 9"],
             "1 is not a prime, and 9 is 3 times 3. But 2 is a prime, the only even one. So the list is 2, 3, 5, 7.")),
    b("Four digits, and all of them are used. So every number we make has 4 digits.", wl("d", "digits: 2, 3, 5, 7")),
    b("An even number must end in an even digit. Only 2 is even, so 2 is locked into the units place.",
      fig("table", tbl(PLACES4, [["?", "?", "?", "2"]]))),
    b("That leaves 3, 5 and 7 for the other three places. 3 choices, then 2, then 1.", w("m", "3 × 2 × 1 = 6")),
    b("Here they all are: 3572, 3752, 5372, 5732, 7352, 7532. Every one ends in 2.", wl("l", "3572, 3752, 5372, 5732, 7352, 7532")),
    b("So 6 even numbers can be formed.", al("ans", "6 numbers"), ring("ans", "6")),
    b("Fix the place that has a rule first. Then count the choices for the rest and multiply."),
]
