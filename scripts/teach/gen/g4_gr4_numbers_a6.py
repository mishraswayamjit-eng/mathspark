"""gr4_numbers, written per question: hand-written chapter questions (Q_CH01_...)."""
from g4_gr4_numbers_lib import A, FIG, G, Q, U, W, X, b, chart, nline

L = {}

L["Q_CH01_001"] = [
    b("Here is 3,62,489. We want to know how much its 6 is really worth.",
      G("Place value of 6 in 3,62,489 = ?"), FIG(chart("362489", [1], note="How much is the 6 worth?"))),
    b("Count the seats from the right: 9 is in the ones, 8 in the tens, 4 in the hundreds and 2 in the thousands.",
      W("ones 9,   tens 8,   hundreds 4,   thousands 2")),
    b("The 6 comes next. Which seat is it in?",
      Q(["ten-thousands", "thousands", "lakhs"],
        "After the thousands seat comes the ten-thousands seat. The 2 is in the thousands, so the 6 is in the ten-thousands.")),
    b("The ten-thousands seat is worth 10,000. So we multiply 6 by 10,000.", W("6 × 10,000 = 60,000")),
    b("6 times 10,000 is 60,000. That is the place value of the 6.", A("60,000")),
    b("Careful: 6 on its own is just the face value. The place value counts the seat as well."),
    b("A quick check: 4 digits come after the 6, so its value is a 6 followed by 4 zeros."),
]

L["Q_CH01_002"] = [
    b("The successor of a number is the very next number. So we add 1 to 99,999.",
      G("Successor of 99,999 = ?"), W("99,999 + 1 = ?")),
    b("What happens to a 9 when we add 1 to it?",
      Q(["it becomes 0, and 1 is carried", "it becomes 10 in the same seat", "it stays 9"],
        "9 plus 1 is 10. A seat can hold only one digit, so we write 0 and carry the 1 to the next seat.")),
    b("The 9 in the ones becomes 0 and carries 1. That carry turns the next 9 into 0 as well, and so on, like falling dominoes."),
    b("All five 9s become 0, and the last carry makes a brand new 1 in front.", W("99,999 + 1 = 1,00,000")),
    b("So the successor is 1,00,000. That is one lakh.", A("1,00,000")),
    b("Notice that it has 6 digits now. The largest 5-digit number, plus 1, is the smallest 6-digit number."),
    b("Careful: 99,998 is the number before. Successor means after, so we add.", W("99,998 is the predecessor")),
]

L["Q_CH01_003"] = [
    b("4 numbers that look very alike. To find the largest, we compare them seat by seat, starting from the left.",
      G("Largest of 45,032   45,302   45,320   45,203", name="g")),
    b("All four start with 4 and then 5. So the first two seats are a tie, and we move on to the hundreds."),
    b("The hundreds digits are 0, 3, 3 and 2. Which numbers are still in the race?",
      Q(["45,302 and 45,320", "45,032 and 45,203", "only 45,320"],
        "The biggest hundreds digit is 3. Two numbers have it: 45,302 and 45,320.")),
    b("3 is the biggest hundreds digit, so 45,032 and 45,203 drop out.", X("45,032", on="g"), X("45,203", on="g")),
    b("Now compare the tens of the two that are left. 45,302 has 0 tens. 45,320 has 2 tens.", W("45,320 > 45,302")),
    b("So the largest is 45,320.", A("45,320")),
    b("So the plan: start at the left, and move one seat to the right only when there is a tie."),
]

L["Q_CH01_006"] = [
    b("We round 4,567 to the nearest hundred. First: which two hundreds does it sit between?",
      G("4,567 to the nearest hundred = ?", name="g"),
      FIG(nline(4500, 4600, 10, [(4500, "4,500"), (4567, "4,567"), (4600, "4,600")], note="Which hundred is nearer?"))),
    b("It is between 4,500 and 4,600.", W("4,500 < 4,567 < 4,600")),
    b("To choose between them, which digit of 4,567 do we look at?",
      Q(["the tens digit, 6", "the ones digit, 7", "the hundreds digit, 5"],
        "To round to the hundreds, look at the digit just to the right of the hundreds. That is the tens digit, 6.")),
    b("The tens digit is 6. The rule: 5 or more, round up. Less than 5, round down.", U("6", on="g")),
    b("6 is more than 5, so we round up to 4,600.", A("4,600")),
    b("It makes sense: 4,567 is past the halfway mark, 4,550, so it is nearer to 4,600.", W("halfway: 4,550")),
    b("Careful: 4,570 is rounding to the nearest ten. For the nearest hundred, the last two digits both become 0.",
      W("4,570: nearest ten")),
]

L["Q_CH01_007"] = [
    b("How many digits does 5,43,21,678 have? The commas make it easy to count in groups.",
      G("5,43,21,678: how many digits?")),
    b("The commas split the number into 4 groups: 5, then 43, then 21, then 678.", W("5   |   43   |   21   |   678")),
    b("How many digits are in the last group, 678?",
      Q(["3", "2", "1"], "6, 7 and 8. That is 3 digits. In the Indian system the last group always has 3 digits.")),
    b("So the groups have 1, 2, 2 and 3 digits. Add them up.", W("1 + 2 + 2 + 3 = 8")),
    b("The number has 8 digits.", A("8")),
    b("Careful: commas are not digits. Count only the digits between them."),
    b("Check: write it without commas, 54321678, and count. 8 digits.", W("54321678")),
]

L["Q_CH01_008"] = [
    b("Expanded form means we break 30,507 into the value of each digit, and write the values as a sum.",
      G("30,507 in expanded form = ?"), FIG(chart("30507"))),
    b("The 3 is in the ten-thousands place, so it is worth 30,000.", W("3 → 30,000")),
    b("Next is a 0 in the thousands place. What does it add to the number?",
      Q(["nothing", "1,000", "10"],
        "0 thousands is nothing at all. The zero only holds the seat, so that the 3 stays in the ten-thousands place.")),
    b("A zero adds nothing, so we skip it. The 5 is in the hundreds place, so it is worth 500.", W("5 → 500")),
    b("Another 0 in the tens, so we skip again. The 7 is in the ones, so it is worth 7.", W("7 → 7")),
    b("Put the three values together as a sum.", W("30,000 + 500 + 7 = 30,507"), A("30,000 + 500 + 7")),
    b("Careful: 30,000 plus 507 also makes 30,507, but 507 is not fully broken up. Expanded form splits every digit.",
      W("30,000 + 507: not fully expanded")),
]

L["Q_CH01_009"] = [
    b("Ascending means going up, smallest first. All 4 numbers use the same digits, so we compare them seat by seat.",
      G("Ascending order: 5,432   5,342   5,423   5,234")),
    b("All four have 5 thousands, so that is a tie. Look at the hundreds digits: 4, 3, 4 and 2."),
    b("Which number has the smallest hundreds digit?",
      Q(["5,234", "5,342", "5,423"], "The hundreds digits are 4, 3, 4 and 2. The smallest is 2, and that belongs to 5,234.")),
    b("5,234 is the smallest, with 2 hundreds. Next is 5,342, with 3 hundreds.", W("5,234 < 5,342")),
    b("Two numbers have 4 hundreds: 5,432 and 5,423. Break the tie with the tens. 2 tens is less than 3 tens, so 5,423 comes first.",
      W("5,423 < 5,432")),
    b("So from smallest to largest, here is the order.", A("5,234; 5,342; 5,423; 5,432")),
    b("Careful: descending is the other way round, largest first. Always check which order is asked for."),
]

L["Q_CH01_010"] = [
    b("We have the digits 7, 0, 3 and 5, and we use each one once. We want the largest number we can build.",
      G("Digits 7, 0, 3, 5: largest 4-digit number = ?")),
    b("Which seat matters most for making a number large?",
      Q(["the thousands seat", "the ones seat", "the tens seat"],
        "The seat on the far left is worth the most. One thousand beats all the hundreds, tens and ones we could put here.")),
    b("So the biggest digit, 7, goes in the thousands seat.", W("7   _   _   _")),
    b("Then the next biggest, 5, in the hundreds. Then 3 in the tens. And 0 is left for the ones.", W("7   5   3   0")),
    b("The largest number is 7,530.", A("7,530")),
    b("Careful: 7,503 looks close. But 3 tens and 0 ones is more than 0 tens and 3 ones.", W("7,530 > 7,503")),
    b("So for the largest number, write the digits from biggest to smallest."),
]

L["Q_CH01_011"] = [
    b("The predecessor is the number just before. So we take 1 away from 10,000.",
      G("Predecessor of 10,000 = ?"), FIG(nline(9998, 10001, 1, [(10000, "10,000")], note="One step back"))),
    b("Will the answer have 5 digits, like 10,000?",
      Q(["No, it will have 4 digits", "Yes, 5 digits"],
        "10,000 is the smallest 5-digit number. Anything before it must have fewer digits, so the answer has 4 digits.")),
    b("10,000 is the smallest number with 5 digits. One step back, and we land on the largest number with 4 digits."),
    b("The largest 4-digit number has a 9 in every seat.", W("10,000 − 1 = 9,999")),
    b("So the predecessor is 9,999.", A("9,999")),
    b("Check by adding back: 9,999 plus 1 is 10,000.", W("9,999 + 1 = 10,000")),
    b("Careful: 10,001 is the successor, the number after. Predecessor means before.", W("10,001 is the successor")),
]

L["Q_CH01_012"] = [
    b("In 4,562, the digit 5 has two values: a place value and a face value. We want the difference between them.",
      G("4,562: place value of 5 − face value of 5 = ?"), FIG(chart("4562", [1]))),
    b("Which of these is the face value of the 5?",
      Q(["5", "500", "50"], "Face value is the easy one. It is just the digit itself, wherever it sits. So the face value is 5.")),
    b("The face value is simply 5.", W("face value = 5")),
    b("For the place value, find the seat. From the right: 2 ones, 6 tens, 5 hundreds. So it is 5 times 100, which is 500.",
      W("5 × 100 = 500"), W("place value = 500")),
    b("Now the difference: 500 minus 5 is 495.", W("500 − 5 = 495"), A("495")),
    b("Careful: 500 and 5 are both among the choices. But the question wants the difference between them."),
    b("So remember: place value uses the seat, and face value ignores it."),
]

L["Q_CH01_013"] = [
    b("One of these four is not a proper Roman numeral. Each one puts a smaller letter in front of a bigger one, so let us check that rule.",
      G("Which is NOT a valid Roman numeral?"), W("XL     VX     XIV     IX", name="opts")),
    b("A smaller letter in front means take away. But only I, X and C are allowed to do that.",
      W("May go in front to take away: I, X, C")),
    b("Which letters are never used to take away?",
      W("V = 5     L = 50     D = 500"),
      Q(["V, L and D", "I, X and C", "only M"],
        "The letters V for 5, L for 50 and D for 500 are never put in front to take away.")),
    b("X L has X in front of L, and X is allowed. That is 50 minus 10, which is 40. Fine.", W("XL = 40")),
    b("X I V has I in front of V. Allowed, and it is 14. I X is 9. Both are fine.", W("XIV = 14     IX = 9")),
    b("In V X, the V stands in front of X. But V is never used to take away. So V X is not valid.",
      X("VX", note="V cannot take away", on="opts"), A("VX")),
    b("And there is no need for it. 10 minus 5 is 5, and 5 already has its own letter, V."),
]

L["Q_CH01_014"] = [
    b("To estimate this sum, we round each number to the nearest thousand first, and then add the round numbers.",
      G("4,891 + 3,207: estimate to the nearest thousand")),
    b("To round 4,891 to the nearest thousand, which digit do we check?",
      Q(["the hundreds digit, 8", "the thousands digit, 4", "the ones digit, 1"],
        "Look one seat to the right of the thousands. That is the hundreds digit, which is 8.")),
    b("The hundreds digit is 8. That is 5 or more, so 4,891 rounds up to 5,000.", W("4,891 → 5,000")),
    b("For 3,207 the hundreds digit is 2. That is less than 5, so it rounds down to 3,000.", W("3,207 → 3,000")),
    b("Now add the round numbers. 5,000 plus 3,000 is 8,000.", W("5,000 + 3,000 = 8,000"), A("8,000")),
    b("Is that sensible? The exact sum is 8,098, which is close to 8,000. A good estimate.", W("4,891 + 3,207 = 8,098")),
    b("Careful: one number went up and the other went down. Check each number on its own."),
]

L["Q_CH01_015"] = [
    b("We read 23,45,678 in the Indian system. The commas show us the groups, which are called periods.",
      G("23,45,678 in words (Indian system)")),
    b("From the right, the first comma cuts off 3 digits: 678. Then come groups of 2 digits: 45, and then 23.",
      W("23   |   45   |   678")),
    b("678 is the ones period and 45 is the thousands period. What is the period of the 23?",
      Q(["lakhs", "crores", "millions"],
        "In the Indian system the periods go: ones, thousands, lakhs, crores. The third group from the right is lakhs.")),
    b("So 23 is in the lakhs period.", W("23 lakh     45 thousand     678")),
    b("Read each group with its name: twenty-three lakh, forty-five thousand, six hundred seventy-eight.",
      A("Twenty-three lakh forty-five thousand"), A("six hundred seventy-eight")),
    b("Careful: million belongs to the international system. And a crore needs 8 digits, but this number has only 7."),
    b("So: split at the commas, name each period, and read from the left."),
]

L["Q_CH01_016"] = [
    b("We count the even numbers between 11 and 21. Between means that 11 and 21 themselves are not included.",
      G("Even numbers between 11 and 21: how many?"),
      FIG(nline(11, 21, 1, [(11, "11"), (21, "21")], note="The numbers between 11 and 21"))),
    b("Which is the first even number after 11?",
      Q(["12", "11", "13"], "11 is odd. The very next number, 12, ends in 2, so it is even.")),
    b("Start at 12 and jump in twos: 12, 14, 16, 18, 20.", W("12, 14, 16, 18, 20")),
    b("The next jump would land on 22, which is past 21. So we stop at 20.", W("22 is past 21")),
    b("Count them. There are 5 even numbers.", A("5")),
    b("Careful: do not forget 20. It is less than 21, so it counts."),
    b("So: find the first one, jump in twos, and stop before you pass the end."),
]

L["Q_CH01_017"] = [
    b("We use 9, 0, 3, 1 and 7, once each, to build the smallest 5-digit number.",
      G("Digits 9, 0, 3, 1, 7: smallest 5-digit number = ?")),
    b("The smallest digit is 0. Can 0 go in the first seat?",
      Q(["No, then it is not a 5-digit number", "Yes, smallest digit first"],
        "A number that starts with 0 loses a digit, so it would only be a 4-digit number. The first seat needs the next smallest digit.")),
    b("So the first seat takes the next smallest digit, 1.", W("1   _   _   _   _")),
    b("Now 0 can take the second seat. It is welcome anywhere except the front.", W("1   0   _   _   _")),
    b("The rest go from smallest to biggest: 3, 7, 9.", W("1   0   3   7   9")),
    b("The smallest number is 10,379.", A("10,379")),
    b("Careful: 13,079 puts the 3 before the 0, and that makes it bigger. Get the 0 in as early as you can.",
      W("10,379 < 13,079")),
]

L["Q_CH01_019"] = [
    b("6 empty seats. We want the smallest number that fills all of them.",
      G("Smallest 6-digit number = ?"), W("_   _   _   _   _   _")),
    b("We want small digits. What is the smallest digit we can put in the first seat?",
      Q(["1", "0", "9"], "0 is smaller, but a number cannot begin with 0. So the first seat gets a 1.")),
    b("The first seat takes 1, because a number cannot begin with 0.", W("1   _   _   _   _   _")),
    b("Every other seat takes the smallest digit there is, 0.", W("1   0   0   0   0   0")),
    b("With Indian commas, that is 1,00,000. One lakh!", A("1,00,000")),
    b("A nice check: it is 1 more than 99,999, the largest 5-digit number.", W("99,999 + 1 = 1,00,000")),
    b("Careful when you count the zeros: a 1, and then exactly 5 zeros."),
]

L["Q_CH01_021"] = [
    b("Two big numbers, and we want a number that lies between them.", G("Between 3,45,678 and 3,45,680 = ?")),
    b("Compare them from the left. Both start with the same three digits: 3, 4, 5. Only the endings differ: 678 and 680.",
      W("endings:   678   and   680")),
    b("Which whole number comes between 678 and 680?",
      Q(["679", "677", "681"], "Count up from 678. The next number is 679, and then comes 680. So 679 is in between.")),
    b("678, then 679, then 680. Only 679 fits in the gap.",
      FIG(nline(677, 681, 1, [(678, "678"), (679, "679"), (680, "680")], note="Look at the endings"))),
    b("Now put the front digits back. The number is 3,45,679.", A("3,45,679")),
    b("Check: it is 1 more than 3,45,678 and 1 less than 3,45,680.",
      W("3,45,678 + 1 = 3,45,679"), W("3,45,680 − 1 = 3,45,679")),
    b("Careful: 3,45,677 and 3,45,681 are close neighbours, but they sit outside the gap.",
      W("3,45,677 and 3,45,681 are outside")),
]

L["Q_CH01_022"] = [
    b("In 4,372 we need two things: the place value of the 4 and the face value of the 7. Then we multiply them.",
      G("4,372: (place value of 4) × (face value of 7) = ?"), FIG(chart("4372", [0, 2]))),
    b("The 4 is the first digit of 4,372. What is its place value?",
      Q(["4,000", "400", "4"], "4,372 has 4 digits, so the first seat is the thousands. 4 thousands is 4,000.")),
    b("The 4 is in the thousands place, so its place value is 4,000.", W("place value of 4 = 4,000")),
    b("Face value is just the digit itself. So the face value of 7 is 7, even though it sits in the tens.",
      W("face value of 7 = 7")),
    b("Product means multiply. 4 times 7 is 28, so 4,000 times 7 is 28,000.",
      W("4 × 7 = 28"), W("4,000 × 7 = 28,000"), A("28,000")),
    b("Careful: do not use 70 for the 7. The question asks for its face value, not its place value.",
      W("place value of 7 = 70: not needed")),
    b("So: read which value is asked for each digit, and then do the sum."),
]

L["Q_CH01_023"] = [
    b("How many zeros does 5 crore have? Let us build up to a crore, step by step.", G("How many zeros are in 5 crore?")),
    b("One thousand has 3 zeros. One lakh has 5 zeros.", W("1 thousand = 1,000"), W("1 lakh = 1,00,000")),
    b("A crore is 100 lakh. Multiplying by 100 adds 2 more zeros. So how many zeros are in 1 crore?",
      W("1 crore = 100 lakh"),
      Q(["7", "6", "8"], "A lakh has 5 zeros, and times 100 adds 2 more. 5 plus 2 is 7.")),
    b("1 crore is a 1 followed by 7 zeros.", W("1 crore = 1,00,00,000")),
    b("For 5 crore, the 1 simply becomes a 5. The zeros stay the same.", W("5 crore = 5,00,00,000")),
    b("So 5 crore has 7 zeros.", A("7")),
    b("Careful: the 5 in front changes nothing about the zeros. 5 crore, 7 crore, 9 crore: they all have 7 zeros."),
]

L["Q_CH01_024"] = [
    b("We are told the digit in each seat. Let us put them into a place value chart, biggest seat first.",
      G("4 ten-thousands, 0 thousands, 3 hundreds, 0 tens, 8 ones")),
    b("4 in the ten-thousands, 0 in the thousands, 3 in the hundreds, 0 in the tens and 8 in the ones.",
      W("TTh   Th   H   T   O"), W("4     0    3   0   8")),
    b("Two seats hold a 0. Can we leave those zeros out when we write the number?",
      Q(["No, they hold the seats", "Yes, zero means nothing"],
        "A zero adds nothing, but it keeps every other digit in its proper seat. Leave it out, and the 4 slides down to a smaller seat.")),
    b("Zeros are place holders. Without them the 4 would not stay in the ten-thousands place."),
    b("Read the seats from left to right. The number is 40,308.", A("40,308"), FIG(chart("40308"))),
    b("Check by adding the values: 40,000 plus 300 plus 8.", W("40,000 + 300 + 8 = 40,308")),
    b("Careful: 4,308 drops a zero and has only 4 digits. And 40,380 puts the 8 in the tens seat.",
      W("4,308: a zero is missing"), W("40,380: the 8 is in the tens")),
]

L["Q_CH01_025"] = [
    b("Which sign goes in the blank: greater than, less than, or equals? We compare the two numbers seat by seat, from the left.",
      G("65,432  ___  65,342", name="g")),
    b("Both have 5 digits. Both have 6 ten-thousands, and both have 5 thousands. Still a tie."),
    b("Now the hundreds. The first number has 4 hundreds and the second has 3. Which number is bigger?",
      Q(["the first, 65,432", "the second, 65,342", "they are equal"],
        "4 hundreds is more than 3 hundreds. Once one seat is bigger, the seats to its right cannot change the result.")),
    b("4 hundreds beats 3 hundreds. We can stop here: the first number is greater.", U("4", on="g"), U(("3", 2), on="g")),
    b("The sign for greater than opens towards the bigger number.", A("65,432 > 65,342")),
    b("Careful: the two numbers use the same digits. But it is the order of the digits that matters, not just which digits they are."),
    b("So: go from the left, and the first seat that differs decides."),
]

L["Q_CH01_027"] = [
    b("Just before means 1 less. So we take 1 away from 50,00,000.", G("The number just before 50,00,000 = ?")),
    b("50,00,000 ends in 6 zeros. When we take 1 away, what do those zeros become?",
      Q(["all 9s", "they stay 0s", "all 1s"],
        "Think of a smaller sum: 10 minus 1 is 9. The zero has to borrow, and it turns into a 9.")),
    b("It is like 100 minus 1, which is 99. Every zero borrows from its neighbour and turns into a 9.", W("100 − 1 = 99")),
    b("The 5 in front lends 1 and becomes 4. And all 6 zeros become 9s.", W("50,00,000 − 1 = 49,99,999")),
    b("So the number just before is 49,99,999.", A("49,99,999")),
    b("Check: 49,99,999 plus 1 is 50,00,000.", W("49,99,999 + 1 = 50,00,000")),
    b("Careful: count the 9s. There must be 6 of them, so the answer still has 7 digits."),
]

L["Q_CH01_028"] = [
    b("We use 5, 3, 8 and 1, once each. We want the largest number, but it must be even.",
      G("Digits 5, 3, 8, 1: largest 4-digit EVEN number = ?")),
    b("An even number must end in an even digit. Which of our digits are even?",
      Q(["only 8", "8 and 1", "5 and 3"], "5, 3 and 1 are odd. The only even digit we have is 8.")),
    b("Only 8 is even. So 8 has to go in the ones seat, like it or not.", W("_   _   _   8")),
    b("This is the trap. We would love to put 8 in front, but then the number would end in an odd digit."),
    b("The other digits fill the front, biggest first: 5, 3, 1.", W("5   3   1   8")),
    b("The largest even number is 5,318.", A("5,318")),
    b("Careful: 8,531 is the largest number from these digits, but it ends in 1, so it is odd.", W("8,531 is odd")),
]

L["Q_CH01_029"] = [
    b("Adding Roman numerals is hard. So we change them into our own numbers, add, and change back.", G("XIV + XXVIII = ?")),
    b("X I V is a ten and a four. That is 14.", W("XIV = 10 + 4 = 14")),
    b("X X V I I I is two tens, a five and three ones. That is 28.", W("XXVIII = 20 + 5 + 3 = 28")),
    b("Add them. 14 plus 28 is 42.", W("14 + 28 = 42")),
    b("42 is 40 and 2. How do the Romans write 40?",
      W("42 = 40 + 2"), W("L = 50"),
      Q(["XL", "XXXX", "LX"], "A letter is never written 4 times in a row. 40 is 10 less than 50, so X goes in front of L.")),
    b("40 is X L, and 2 is I I. So the total is X L I I.", A("XLII")),
    b("Careful: X X X X I I adds up to 42 as well, but 4 Xs in a row are not allowed."),
    b("So: change to our numbers, add, and change back."),
]
