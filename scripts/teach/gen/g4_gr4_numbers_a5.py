"""gr4_numbers, written per question: past papers (PYQ_...)."""
from g4_gr4_numbers_lib import A, BX, FIG, G, Q, W, X, b, chart

L = {}

L["PYQ_2016_Q05"] = [
    b("Each of these numbers has two 6s. We want the number where one 6 is worth 1000 times the other 6.",
      G("One 6 worth 1000 times the other 6: in which number?"), W("576006     567060     657600")),
    b("Each seat is worth 10 times the seat on its right. So how many seats apart must the two 6s be?",
      W("1 seat left: 10 times      2 seats left: 100 times"),
      Q(["3 seats", "2 seats", "4 seats"],
        "One seat apart is 10 times. Two seats is 100 times. Three seats is 1000 times. So the 6s must be 3 seats apart.")),
    b("10 times 10 times 10 is 1000. So we look for two 6s that are 3 seats apart.", W("10 × 10 × 10 = 1000")),
    b("Take 576006. One 6 is in the thousands, worth 6000. The other is in the ones, worth 6. Yes, 3 seats apart!",
      W("576006:   6000 and 6"), FIG(chart("576006", [2, 5]))),
    b("Now the trap. Do not stop at the first one that fits! One of the choices is All of them, so we must test the others too."),
    b("In 567060 the 6s are worth 60000 and 60. That fits as well.", W("567060:   60000 and 60"), W("60 × 1000 = 60000")),
    b("In 657600 the 6s are worth 600000 and 600. That fits too.", W("657600:   600000 and 600"), W("600 × 1000 = 600000")),
    b("All three numbers work. So the answer is: All of them.", A("All of them")),
    b("Remember: when All of them is a choice, test every number before you decide."),
]

L["PYQ_2016_Q18"] = [
    b("We write the Roman numerals from 1 to 20, and count every V we write.",
      G("Roman numerals I to XX: how many times is V written?"), W("I to XX means 1 to 20")),
    b("First, 1 to 10. The numerals with a V are I V, V, V I, V I I and V I I I. Those are 4, 5, 6, 7 and 8.",
      W("IV   V   VI   VII   VIII")),
    b("What about 9? Is there a V in the numeral for 9?",
      Q(["No, 9 is I X", "Yes, 9 is V I I I I"],
        "A letter is never written 4 times in a row. 9 is 1 less than 10, so it is I X, with no V at all.")),
    b("9 is I X, so there is no V there. That gives 5 Vs from 1 to 10.", W("1 to 10:   V is written 5 times")),
    b("From 11 to 20 the same pattern repeats with an X in front: X I V, X V, X V I, X V I I and X V I I I.",
      W("XIV   XV   XVI   XVII   XVIII"), W("11 to 20:   V is written 5 times")),
    b("Careful: the sneaky ones are I V and X I V, where the V hides behind an I. And X I X and X X have no V at all."),
    b("So 5 plus 5 makes 10.", W("5 + 5 = 10"), A("10")),
    b("So: write out the pattern for 1 to 10, then see how it repeats for the next ten."),
]

L["PYQ_2016_Q40"] = [
    b("We need to write this number name in figures. Let us take it one piece at a time.",
      G("One lakh one thousand one hundred ten = ?")),
    b("One lakh is a 1 followed by 5 zeros.", W("one lakh = 1,00,000")),
    b("One thousand is 1,000. And one hundred ten is 110.", W("one thousand = 1,000"), W("one hundred ten = 110")),
    b("Now add the three pieces together.", W("1,00,000 + 1,000 + 110 = 1,01,110")),
    b("Look at the thousands. They have 2 seats, but there is only one thousand. What goes in those 2 seats?",
      Q(["0 and then 1", "1 and then 1", "1 and then 0"],
        "One thousand needs a 1 in the thousands seat. The ten-thousands seat is empty, so it gets a 0 to hold the place.")),
    b("That 0 is a place holder. Leave it out, or put a 1 there, and the number changes.",
      W("lakhs: 1     thousands: 01     ones: 110")),
    b("So the number is 1,01,110. Without the commas, that is 101110.", A("101110")),
    b("Check: it has 6 digits, just as a lakh number should."),
]

L["PYQ_2017_Q02"] = [
    b("M N is a 2-digit number with tens digit M and units digit N. N M is the same two digits swapped. We want the biggest possible difference.",
      G("'MN' − 'NM': largest possible value = ?"), W("M and N: different digits, not zero")),
    b("To make a difference big, the first number should be as big as we can make it, and the second as small as we can."),
    b("For a big M N, the tens digit M should be the biggest digit there is, 9.", W("M = 9")),
    b("Now N should be as small as the rules allow. What is the smallest N we may use?",
      Q(["1", "0", "2"],
        "0 is the smallest digit, but the question says the digits are not zero. So the smallest N allowed is 1.")),
    b("This is the trap. The digits are non zero, so N cannot be 0. The smallest it can be is 1.", W("N = 1")),
    b("So M N is 91 and N M is 19.", W("MN = 91     NM = 19")),
    b("91 minus 19 is 72.", W("91 − 19 = 72"), A("72")),
    b("A pattern to notice: the difference is always 9 times the gap between the digits. The gap here is 8, and 9 times 8 is 72.",
      W("9 × (9 − 1) = 72")),
]

L["PYQ_2017_Q31"] = [
    b("In 978652 we want the place value of the 7, the place value of the 5, and then the difference between them.",
      G("978652: place value of 7 − place value of 5 = ?"), FIG(chart("978652", [1, 4], note="Find the 7 and the 5"))),
    b("Count from the right: 2 ones, 5 tens, 6 hundreds, 8 thousands, and then the 7. Which place is the 7 in?",
      Q(["ten-thousands", "thousands", "lakhs"],
        "After the thousands comes the ten-thousands place. The 7 is the fifth digit from the right, so it sits there.")),
    b("So the 7 is worth 70000.", W("7 × 10000 = 70000")),
    b("The 5 is in the tens place, so it is worth 50.", W("5 × 10 = 50")),
    b("Difference means subtract. So we need 70000 minus 50.", W("70000 − 50 = ?")),
    b("Borrowing across all those zeros is fiddly. Try this instead: 70000 minus 100 is 69900. Then give back 50.",
      W("70000 − 100 = 69900"), W("69900 + 50 = 69950")),
    b("So the difference is 69950.", W("70000 − 50 = 69950"), A("69950")),
    b("Careful: 70050 is what you get by adding. The word difference always means take away.", W("70000 + 50 = 70050")),
]

L["PYQ_2017_Q33"] = [
    b("Three Roman numerals. Only a numeral that follows every rule is correctly written. So let us check each one against the rules.",
      G("Which Roman numeral is correctly written?"), W("MCCCCIV     CDVLII     CDLXVI", name="opts")),
    b("Rule one: a letter may be repeated at most 3 times in a row.", W("Rule 1: a letter repeats at most 3 times")),
    b("Look at M C C C C I V. Does it follow rule one?",
      Q(["No, C is written 4 times", "Yes, it is fine"], "Count the Cs. There are 4 in a row, and that breaks the rule.")),
    b("4 Cs in a row, so that one is out. 400 should be written C D.",
      X("MCCCCIV", note="4 Cs", on="opts"), W("400 = CD")),
    b("Rule two: V, L and D are never put in front of a bigger letter to take away.",
      W("Rule 2: V, L, D never go in front to take away")),
    b("In C D V L I I, the V stands in front of L. That breaks rule two, so it is out as well.",
      X("CDVLII", note="V before L", on="opts")),
    b("Now C D L X V I. C D is 400, then L is 50, X is 10, V is 5 and I is 1. Every part follows the rules. It is 466.",
      W("400 + 50 + 10 + 5 + 1 = 466"), A("CDLXVI")),
    b("So do not rush to None of these. Test each numeral against the rules, one at a time."),
]

L["PYQ_2018_Q03"] = [
    b("m stands for some even number and n stands for some odd number. We must find which of the 4 expressions is always odd.",
      G("m is even, n is odd. Which is always odd?"), W("3m + 4n     m + 3n     5m + 6n     5mn")),
    b("We do not know m and n, so let us test with easy numbers. Take m as 2 and n as 1.", W("try m = 2, n = 1")),
    b("First, 3 m plus 4 n. 3 times 2 is 6, 4 times 1 is 4, and 6 plus 4 is 10. That is even.", W("3 × 2 + 4 × 1 = 10")),
    b("Now m plus 3 n. With m as 2 and n as 1, what do we get?",
      Q(["5", "7", "6"], "3 n is 3 times 1, which is 3. Then 2 plus 3 is 5.")),
    b("2 plus 3 is 5, and 5 is odd. That looks like our answer.", W("2 + 3 × 1 = 5"), BX("5")),
    b("Check the other two. 5 m plus 6 n is 10 plus 6, which is 16. And 5 m n is 5 times 2 times 1, which is 10. Both are even.",
      W("5 × 2 + 6 × 1 = 16"), W("5 × 2 × 1 = 10")),
    b("Why does it always work? m is even. 3 n is odd times odd, which is odd. And even plus odd is always odd.",
      W("even + odd = odd")),
    b("So the answer is m plus 3 n.", A("m + 3n")),
    b("The key idea: anything times an even number is even. So look for the expression with exactly one odd part."),
]

L["PYQ_2018_Q11"] = [
    b("Four Roman numerals, and we want the largest. But be careful: not all of them are proper numerals.",
      G("Which Roman numeral has the largest value?"), W("XXXIX     XXXXIX     XXLIV     XXVIII", name="opts")),
    b("Look at X X X X I X. It has X four times in a row. Is that allowed?",
      Q(["No, at most 3 in a row", "Yes, any number of times"],
        "A Roman letter may be repeated at most 3 times in a row. Four Xs break the rule, so this is not a proper numeral.")),
    b("So X X X X I X is out. The proper way to write 49 is X L I X.", X("XXXXIX", note="4 Xs", on="opts"), W("49 = XLIX")),
    b("X X L I V puts two Xs in front of the L. Only one smaller letter may stand in front of a bigger one. So it is out too.",
      X("XXLIV", note="2 Xs before L", on="opts")),
    b("Now the two proper ones. X X X I X is three tens and a nine. That is 39.", W("XXXIX = 30 + 9 = 39")),
    b("X X V I I I is two tens, a five and three ones. That is 28.", W("XXVIII = 20 + 5 + 3 = 28")),
    b("39 is more than 28. So the largest is X X X I X.", W("39 > 28"), A("XXXIX")),
    b("The trap is to pick the longest numeral, or the one that looks biggest. Check the rules first, then compare the values."),
]

L["PYQ_2018_Q22"] = [
    b("We use 7, 4, 3 and 0, once each, to make 4-digit even numbers. How many can we make?",
      G("Digits 7, 4, 3, 0 once each: how many 4-digit even numbers?")),
    b("An even number ends in an even digit. Which of our digits can go in the last seat?",
      Q(["0 or 4", "only 4", "7 or 3"],
        "Even digits are 0, 2, 4, 6 and 8. From our four digits, 0 and 4 are even. So the last digit is 0 or 4.")),
    b("Group one: the number ends in 0. Then 7, 4 and 3 fill the first three seats in any order. That gives 6 numbers.",
      W("ends in 0:  7430, 7340, 4730, 4370, 3740, 3470"), W("6 numbers")),
    b("Group two: the number ends in 4. The digits left are 7, 3 and 0.", W("ends in 4:   _   _   _   4")),
    b("Careful, here is the trap. The first seat cannot be 0, or it is not a 4-digit number. So the first digit is 7 or 3."),
    b("That gives 7034, 7304, 3074 and 3704. Just 4 numbers.", W("7034, 7304, 3074, 3704"), W("4 numbers")),
    b("Add the two groups: 6 plus 4 is 10.", W("6 + 4 = 10"), A("10")),
    b("So: split into cases by the last digit, and leave out anything that starts with 0."),
]

L["PYQ_2019_Q06"] = [
    b("Four Roman numerals, and we want the largest. But be careful: not all of them are proper numerals.",
      G("Which Roman numeral has the largest value?"), W("XXXXIX     XXVIII     XLVI     CCD", name="opts")),
    b("C C D has big letters in it. But two Cs stand in front of the D. Is that allowed?",
      Q(["No, only one letter may go in front", "Yes, that makes 300"],
        "Only one smaller letter may stand in front of a bigger one. So C C D is not a proper numeral. 300 is written C C C.")),
    b("So C C D is out. And X X X X I X has X four times in a row, which is not allowed either. Out as well.",
      X("CCD", note="2 Cs before D", on="opts"), X("XXXXIX", note="4 Xs", on="opts")),
    b("Now the proper ones. In X L V I, X L is 10 less than 50, so it is 40. Then V I is 6. That makes 46.",
      W("XL = 50 − 10 = 40"), W("XLVI = 40 + 6 = 46")),
    b("X X V I I I is two tens, a five and three ones. That is 28.", W("XXVIII = 20 + 5 + 3 = 28")),
    b("46 is more than 28. So the largest is X L V I.", W("46 > 28"), A("XLVI")),
    b("Notice that X L V I is the shortest proper numeral here, and still the largest. Length tells you nothing."),
    b("So: rules first, values second."),
]

L["PYQ_2019_Q10"] = [
    b("Two numbers are given in words. We write them in figures, subtract, and then find the digit in the ten thousands place.",
      G("Difference of the two numbers: ten thousands digit = ?")),
    b("Ninety seven lakh, forty three thousand, seven hundred fifty three. In figures that is 97,43,753.", W("97,43,753")),
    b("Forty nine thousand, six hundred eighty two is 49,682.", W("49,682")),
    b("Now subtract. Line the numbers up by place, ones under ones, and take care with the borrowing.",
      W("97,43,753 − 49,682 = 96,94,071")),
    b("The difference is 96,94,071. Counting from the right, which seat is the ten thousands place?",
      Q(["the 5th seat", "the 4th seat", "the 6th seat"],
        "Count them: ones, tens, hundreds, thousands, ten thousands. That is the 5th seat from the right.")),
    b("Count the seats of 96,94,071 from the right: 1, 7, 0, 4, and then 9.",
      FIG(chart("9694071", [2], note="The ten thousands place"))),
    b("So the digit in the ten thousands place is 9.", A("9")),
    b("Careful: there are two 9s in the answer, and a 0 too. Always count the seats from the right, one at a time."),
]

L["PYQ_2019_Q16"] = [
    b("We use 3, 4, 5 and 7, once each. We count the numbers that are odd and also greater than 5000.",
      G("Digits 3, 4, 5, 7 once each: odd numbers above 5000?")),
    b("Two rules. To be greater than 5000, the first digit must be 5 or 7. To be odd, the last digit must be 3, 5 or 7.",
      W("first digit: 5 or 7"), W("last digit: 3, 5 or 7")),
    b("Suppose the first digit is 5. Which digits can go last?",
      Q(["3 or 7", "3, 5 or 7", "only 7"],
        "The 5 is already used in the first seat, and each digit is used only once. So the last digit can be 3 or 7.")),
    b("This is the key idea. A digit used in front cannot be used again at the end."),
    b("Start with 5 and end with 3: the middle is 4 and 7, in 2 orders. Start with 5 and end with 7: the middle is 3 and 4, in 2 orders.",
      W("5473, 5743"), W("5347, 5437")),
    b("That is 4 numbers starting with 5. Starting with 7 works the same way: the last digit is 3 or 5.",
      W("7453, 7543"), W("7345, 7435")),
    b("4 numbers start with 5 and 4 start with 7. That makes 8.", W("4 + 4 = 8"), A("8")),
    b("So: fix the first digit, then the last, then count the middle. And never use a digit twice."),
]
