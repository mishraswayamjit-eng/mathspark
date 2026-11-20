"""gr4_numbers, written per question: G4A_NUMBERS_001 to 015."""
from g4_gr4_numbers_lib import A, C, FIG, G, N, Q, U, W, X, b, chart, nline, table

L = {}

L["G4A_NUMBERS_001"] = [
    b("We must build the smallest 5-digit number from 4, 0, 7, 2 and 9. But there is one rule: the 9 has to sit in the thousands place.",
      G("Digits 4, 0, 7, 2, 9: smallest number, 9 in thousands")),
    b("In a 5-digit number, the thousands place is the second seat from the left. So the 9 goes there first.",
      W("_   9   _   _   _")),
    b("Now the first seat. We want it as small as we can. Which digit goes there?",
      Q(["2", "0", "4"],
        "0 is the smallest digit, but a number cannot start with 0. So the first seat takes the next smallest digit, which is 2.")),
    b("A number cannot start with 0, or it would not be a 5-digit number at all. So 2 leads.", W("2   9   _   _   _")),
    b("The digits left are 0, 4 and 7. To keep the number small, write them from smallest to greatest.",
      W("2   9   0   4   7")),
    b("So the number is 29047.", A("29047"), FIG(chart("29047", [1], note="9 is in the thousands place"))),
    b("Careful: 20479 is even smaller, but its 9 is in the ones place. The rule about the 9 comes first.",
      W("20479: the 9 is in the ones place")),
]

L["G4A_NUMBERS_002"] = [
    b("Two numbers to find. Each has 4 digits, and no digit may repeat. Then we subtract.",
      G("Greatest − smallest 4-digit number, all digits different")),
    b("For the greatest, start with the biggest digit, 9, and step down: 9, 8, 7, 6. That makes 9876.", W("greatest: 9876")),
    b("For the smallest, the first digit must be 1, because a number cannot start with 0. What is the best digit for the second seat?",
      Q(["0", "2", "1"],
        "0 cannot go first, but it is welcome in the second seat, and it is the smallest digit there is. The 1 is already used.")),
    b("This is the key idea. Zero cannot lead, but it can sit right behind the 1. Then come 2 and 3. So the smallest is 1023.",
      W("smallest: 1023")),
    b("Now subtract 1023 from 9876. No borrowing is needed: 6 minus 3, 7 minus 2, 8 minus 0, and 9 minus 1.",
      W("9876 − 1023 = 8853")),
    b("The difference is 8853.", A("8853")),
    b("Watch out for two traps. 1234 forgets that 0 may be used. And 1000 repeats the 0, which is not allowed.",
      W("1234: forgets the 0"), W("1000: repeats the 0")),
    b("Check by adding back: 8853 plus 1023 is 9876.", W("8853 + 1023 = 9876")),
]

L["G4A_NUMBERS_003"] = [
    b("In 7,26,935, one digit has a place value that is exactly 10,000 times its face value. Let us find that digit.",
      G("7,26,935: place value = 10,000 × face value. Which digit?"), FIG(chart("726935"))),
    b("Remember: the face value is the digit itself. The place value is the digit times what its seat is worth.",
      W("place value = face value × worth of the seat")),
    b("So we want the seat that is worth 10,000. Which place is that?",
      Q(["ten-thousands", "thousands", "lakhs"],
        "Count the seats from the right: ones, tens, hundreds, thousands, ten-thousands. The fifth seat is worth 10,000.")),
    b("Now count the seats of 7,26,935 from the right: 5 ones, 3 tens, 9 hundreds, 6 thousands, 2 ten-thousands.",
      FIG(chart("726935", [1], note="The ten-thousands place"))),
    b("So the digit is 2. Its place value is 20,000, which is 2 times 10,000.", W("2 × 10,000 = 20,000"), A("2")),
    b("Careful with the neighbours. The 6 is only in the thousands place, and the 7 is in the lakhs place. One seat off gives a different digit."),
    b("So: turn the clue into a seat, then count from the right to see who sits there."),
]

L["G4A_NUMBERS_004"] = [
    b("This number is written with Indian commas. We want to read it the international way, with millions.",
      G("3,05,40,000 in the international system = ?")),
    b("The digits do not change, only the commas. So first take the commas out. There are 8 digits.", W("30540000")),
    b("The international system groups the digits from the right. How many digits go in each group?",
      Q(["3 in every group", "3, then 2 in each group", "2 in every group"],
        "The Indian system goes 3, then 2, then 2. The international system keeps it simple: 3 digits in every group.")),
    b("So group in threes from the right. We get 30, then 540, then 3 zeros.", W("30,540,000", name="intl"), W("groups:   30    540    000")),
    b("The first group counts millions and the second counts thousands. So we have 30 million and 540 thousand.",
      U("30", on="intl"), U("540", on="intl"), W("30 million     540 thousand")),
    b("In words: thirty million, five hundred forty thousand.", A("Thirty million five hundred forty thousand")),
    b("Careful: the Indian commas make groups of 2 digits. Do not read those groups one by one. Regroup in threes first, then read."),
    b("So: drop the commas, regroup in threes from the right, then name the groups."),
]

L["G4A_NUMBERS_005"] = [
    b("Rahim gets 3,00,000 rupees, all in 100 rupee notes. We want to know how many notes that is.",
      G("₹3,00,000 in ₹100 notes. How many notes?")),
    b("Each note is worth 100. Which sum tells us the number of notes?",
      Q(["3,00,000 ÷ 100", "3,00,000 × 100", "3,00,000 − 100"],
        "We are asking how many hundreds fit into 3,00,000. Finding how many fit is a division.")),
    b("So we divide 3,00,000 by 100.", W("3,00,000 ÷ 100 = ?", name="d")),
    b("First count the zeros in 3,00,000. There are 5 of them.", U("00,000", on="d"), N("00,000", "5 zeros", on="d")),
    b("Dividing by 100 takes away 2 zeros, one for each zero in 100. So 5 zeros become 3 zeros.",
      W("5 zeros − 2 zeros = 3 zeros")),
    b("A 3 with 3 zeros is 3,000. So Rahim gets 3,000 notes.", W("3,00,000 ÷ 100 = 3,000"), A("3,000")),
    b("Check: 3,000 notes of 100 rupees make 3,00,000 rupees. It works.", W("3,000 × 100 = 3,00,000")),
    b("Careful when you count the zeros in a lakh. 1 lakh has 5 zeros, not 4. Miss one, and the answer comes out ten times too small.",
      W("1 lakh = 1,00,000")),
]

L["G4A_NUMBERS_006"] = [
    b("India became independent in the year M C M X L V I I. We want the year 75 years later, in Roman numerals.",
      G("MCMXLVII + 75 years = ? (in Roman numerals)")),
    b("Roman numerals are hard to add. So first, we change the year into our own numbers, part by part.",
      FIG(table(["M", "CM", "XL", "VII"], [["?", "?", "?", "?"]], note="The year, part by part"))),
    b("C M has a smaller letter in front of a bigger one. C is 100 and M is 1000. So what is C M?",
      W("C = 100     M = 1000"),
      Q(["900", "1100", "1000"], "A smaller letter in front is taken away. 1000 minus 100 is 900.")),
    b("So M is 1000, C M is 900, X L is 40 and V I I is 7. The year is 1947.", W("1000 + 900 + 40 + 7 = 1947")),
    b("Now add 75 years. 1947 plus 75 is 2022.", W("1947 + 75 = 2022")),
    b("Back to Roman letters. 2022 is 2000, 20 and 2.", W("2022 = 2000 + 20 + 2")),
    b("2000 is M M. 20 is X X. And 2 is I I.", W("2000 = MM     20 = XX     2 = II"), A("MMXXII")),
    b("Careful: we crossed the year 2000, so the answer has to start with M M. A numeral starting M C M is still before 2000."),
    b("So: Roman to our numbers, do the sum, then back to Roman."),
]

L["G4A_NUMBERS_007"] = [
    b("4 Roman numerals to put in order, smallest first. They look alike, so let us find the value of each one.",
      G("XL, LX, XIV, XLIV: smallest first")),
    b("X L has the smaller letter first, so we take away. 50 minus 10 is 40.", W("XL:  50 − 10 = 40", lab=True)),
    b("Now L X. The bigger letter is first this time. What is L X worth?",
      Q(["60", "40", "50"], "When the bigger letter comes first, we add. 50 and 10 make 60.")),
    b("L X is 50 plus 10, which is 60. The same letters as X L, but a different number!", W("LX:  50 + 10 = 60", lab=True)),
    b("X I V is 10, and then I V, which is 4. That makes 14.", W("XIV:  10 + 4 = 14", lab=True)),
    b("X L I V is X L, which is 40, and then I V, which is 4. That makes 44.", W("XLIV:  40 + 4 = 44", lab=True)),
    b("Now put the numbers in order: 14, 40, 44, 60.", W("14 < 40 < 44 < 60")),
    b("So in Roman numerals, smallest first: X I V, then X L, then X L I V, then L X.", A("XIV, XL, XLIV, LX")),
    b("The trap is X L I V. It begins like X L, so it is 44, and it comes before L X, not after it."),
]

L["G4A_NUMBERS_008"] = [
    b("Some number was rounded to the nearest hundred, and the result was 4,700. We want the greatest whole number it could have been.",
      G("Rounds to 4,700 (nearest hundred). Greatest number = ?"),
      FIG(nline(4600, 4800, 10, [(4700, "4,700")], note="Which numbers round to 4,700?"))),
    b("Numbers above 4,700 can round down to it, as long as they are closer to 4,700 than to 4,800.",
      W("between 4,700 and 4,800")),
    b("Halfway between them is 4,750. Which way does the halfway number round?",
      W("halfway: 4,750"),
      Q(["up, to 4,800", "down, to 4,700"],
        "The rule is: 5 or more in the tens place rounds up. 4,750 has a 5 in the tens place, so it rounds up to 4,800.")),
    b("So 4,750 is already too big, because it rounds up to 4,800. That is the trap in this question.",
      W("4,750 rounds up to 4,800")),
    b("Step back just one. 4,749 has a 4 in the tens place, and 4 is less than 5, so it rounds down to 4,700.",
      W("4,749 rounds down to 4,700"),
      FIG(nline(4600, 4800, 10, [(4700, "4,700"), (4749, "4,749")], hops=[(4749, 4700, None)], note="4,749 still rounds down"))),
    b("So the greatest whole number is 4,749.", A("4,749")),
    b("And what about 4,799? It is far too close to 4,800. Only the tens digit matters: 4 or less rounds down, 5 or more rounds up.",
      W("4,799 rounds up to 4,800")),
    b("So for the greatest number that rounds down: go to the halfway point, then step back one."),
]

L["G4A_NUMBERS_009"] = [
    b("38,462 people watched the match. Anil rounds to the nearest thousand and Bina rounds to the nearest ten. How far apart are their answers?",
      G("38,462: nearest thousand, and nearest ten. Difference?", name="g")),
    b("Anil rounds to the nearest thousand. Which digit must he look at to decide?",
      Q(["the hundreds digit, 4", "the thousands digit, 8", "the ones digit, 2"],
        "To round to a place, look at the digit just to its right. For thousands, that is the hundreds digit, which is 4.")),
    b("The hundreds digit is 4. That is less than 5, so Anil rounds down to 38,000.", U("4", on="g"), W("Anil: 38,000")),
    b("Bina rounds to the nearest ten, so she looks at the ones digit. It is 2, less than 5, so she rounds down to 38,460.",
      W("Bina: 38,460")),
    b("Now the difference: 38,460 minus 38,000 is 460.", W("38,460 − 38,000 = 460"), A("460")),
    b("Careful: use Bina's rounded number, 38,460, not the number we started with. Otherwise you get 462.",
      W("38,462 − 38,000 = 462   (not rounded!)")),
    b("So for each rounding, look one digit to the right. Less than 5, go down. 5 or more, go up."),
]

L["G4A_NUMBERS_010"] = [
    b("Two words to know here. The successor of a number is the one just after it. The predecessor is the one just before it.",
      G("Successor of greatest 4-digit + predecessor of smallest")),
    b("The greatest 4-digit number is 9,999. Its successor is 1 more. What is 9,999 plus 1?",
      W("greatest 4-digit number: 9,999"),
      Q(["10,000", "9,990", "1,00,000"],
        "Adding 1 turns every 9 into a 0 and puts a new 1 in front. So we get 10,000, which has 5 digits.")),
    b("9,999 plus 1 is 10,000. Every 9 rolls over to 0.", W("9,999 + 1 = 10,000")),
    b("The smallest 4-digit number is 1,000. Its predecessor is 1 less, which is 999.",
      W("smallest 4-digit number: 1,000"), W("1,000 − 1 = 999")),
    b("Now add the two: 10,000 plus 999 is 10,999.", W("10,000 + 999 = 10,999"), A("10,999")),
    b("Careful with the two words. Successor goes up one, predecessor goes down one. Mix them up and you add a different pair of numbers."),
    b("So: find each special number, take one step the right way, then add."),
]

L["G4A_NUMBERS_011"] = [
    b("We are told the successor of a secret number is 20,000. We want the predecessor of that same secret number.",
      G("Successor of a number = 20,000. Predecessor = ?"),
      FIG(nline(19997, 20001, 1, [(20000, "20,000")], note="20,000 is the successor"))),
    b("The successor is one more than the number. So where is the secret number?",
      Q(["one step before 20,000", "one step after 20,000", "it is 20,000 itself"],
        "20,000 comes just after the secret number. So the secret number is one step back from 20,000.")),
    b("One step back from 20,000 is 19,999. That is our secret number.", W("20,000 − 1 = 19,999")),
    b("Careful: we are not done! 19,999 is the number itself. The question asks for its predecessor, one more step back."),
    b("19,999 minus 1 is 19,998.", W("19,999 − 1 = 19,998"),
      FIG(nline(19997, 20001, 1, [(19998, "19,998"), (19999, "19,999"), (20000, "20,000")],
                hops=[(20000, 19999, "−1"), (19999, 19998, "−1")])),
      A("19,998")),
    b("So from a successor back to the predecessor is always 2 steps. 20,000 minus 2 is 19,998.", W("20,000 − 2 = 19,998")),
    b("Predecessor, number, successor: three neighbours in a row."),
]

L["G4A_NUMBERS_012"] = [
    b("We want the greatest 4-digit number whose digits are all different and add up to 10.",
      G("4 different digits that add up to 10. Greatest number?")),
    b("For a big number, the first digit should be as big as possible. So try 9 first. The other 3 digits must then add up to 1.",
      W("9 _ _ _ : the rest add up to 1", name="n9")),
    b("Three different digits that add up to 1. Can it be done?",
      Q(["No, a digit would repeat", "Yes, with 1, 0 and 0"],
        "1, 0 and 0 does add up to 1, but the 0 is used twice. The digits must all be different, so 9 cannot go first.")),
    b("So 9 is out. Try 8: the rest must add up to 2. That needs 2, 0, 0 or 1, 1, 0. A digit repeats each time, so 8 is out too.",
      X("9 _ _ _", note="repeats", on="n9"), W("8 _ _ _ : the rest add up to 2"), X("8 _ _ _", note="repeats")),
    b("Now try 7. The rest must add up to 3, and 2, 1 and 0 do it. All different!",
      W("7 _ _ _ : the rest add up to 3"), W("2 + 1 + 0 = 3")),
    b("Put those digits after the 7, from greatest to smallest. That makes 7210.", A("7210")),
    b("Check: 7 plus 2 plus 1 plus 0 is 10, and no digit repeats.", W("7 + 2 + 1 + 0 = 10")),
    b("The trap is 9100. Its digits add up to 10, but the 0 is used twice. Read every rule in the question.",
      W("9100: the 0 repeats")),
]

L["G4A_NUMBERS_013"] = [
    b("In 46,285 the digit 6 is swapped for a 9. By how much does the number grow?",
      G("46,285: the 6 becomes 9. Increase = ?"), FIG(chart("46285", [1], note="Which seat is the 6 in?"))),
    b("Count from the right: 5 ones, 8 tens, 2 hundreds. Where is the 6?",
      Q(["thousands place", "hundreds place", "ten-thousands place"],
        "5 is in the ones, 8 is in the tens, 2 is in the hundreds, and next comes the 6, in the thousands place.")),
    b("The 6 is in the thousands place, so it is worth 6,000.", W("6 × 1,000 = 6,000")),
    b("A 9 in the same seat is worth 9,000.", W("9 × 1,000 = 9,000")),
    b("Nothing else changed. So the number grows by 9,000 minus 6,000, which is 3,000.", W("9,000 − 6,000 = 3,000"), A("3,000")),
    b("Careful: 9 minus 6 is only 3. But these are 3 thousands, because of the seat the digit sits in."),
    b("Check with the whole numbers: 49,285 minus 46,285 is 3,000.", W("49,285 − 46,285 = 3,000")),
]

L["G4A_NUMBERS_014"] = [
    b("Riya writes every number from 1 to 100. We count how many times her pencil writes the digit 7.",
      G("Numbers 1 to 100: how many times is the digit 7 written?")),
    b("A 7 can be in the ones place or in the tens place. Count each place on its own. First the ones: 7, 17, 27, and so on, up to 97.",
      W("ones place: 7, 17, 27, 37, 47, 57, 67, 77, 87, 97", name="ones")),
    b("That is 10 numbers, so the 7 is written 10 times in the ones place.", W("ones place: 10 sevens")),
    b("Now the tens place. Which numbers have a 7 in the tens place?",
      Q(["70 to 79", "7 to 17", "71 to 77"],
        "A 7 in the tens place means the number is in the seventies. That is every number from 70 to 79.")),
    b("From 70 to 79 there are 10 numbers, so that is 10 more sevens.",
      W("tens place: 70, 71, 72, 73, 74, 75, 76, 77, 78, 79", name="tens"), W("tens place: 10 sevens")),
    b("Here is the trap: 77. It is in both lists! But that is right, because 77 really has two 7s, and both are written.",
      C("77", on="ones"), C("77", on="tens")),
    b("So the total is 10 plus 10, which is 20.", W("10 + 10 = 20"), A("20")),
    b("So when you count a digit, count one place at a time. A number like 77 is counted once in each place."),
]

L["G4A_NUMBERS_015"] = [
    b("A number puzzle with 5 seats. Two clues are easy: 3 goes in the ten-thousands place and 0 goes in the hundreds place.",
      G("5-digit number from clues. Greatest possible = ?"), W("3   _   0   _   _")),
    b("The ones digit is the greatest odd digit. The odd digits are 1, 3, 5, 7 and 9, so the ones digit is 9.",
      W("3   _   0   _   9")),
    b("Now the tricky clue: the thousands digit is twice the tens digit. The pairs could be 2 and 1, 4 and 2, 6 and 3, or 8 and 4.",
      W("thousands, tens:   2, 1    4, 2    6, 3    8, 4", name="pairs")),
    b("One of those pairs breaks the rule that all 5 digits are different. Which one?",
      Q(["6 and 3", "8 and 4", "4 and 2"],
        "Look at what is already in the number: 3, 0 and 9. The pair 6 and 3 would use the 3 a second time.")),
    b("So 6 and 3 is out, because 3 is already in the first seat.", X("6, 3", note="3 repeats", on="pairs")),
    b("We want the greatest number, so choose the biggest thousands digit that is left. That is 8, with 4 in the tens.",
      W("3   8   0   4   9")),
    b("The number is 38049.", A("38049"), FIG(chart("38049"))),
    b("Check every clue: 8 is twice 4, the ones digit is 9, 0 is in the hundreds, and 3, 8, 0, 4, 9 are all different."),
    b("Careful with 38409. It uses the same digits, but the 0 has slipped out of the hundreds place.",
      W("38409: 0 is not in the hundreds place")),
]
