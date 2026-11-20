"""gr4_numbers, written per question: G4A_NUMBERS_016 to 029."""
from g4_gr4_numbers_lib import A, BX, FIG, G, Q, W, X, b, chart, nline

L = {}

L["G4A_NUMBERS_016"] = [
    b("We want the smallest 5-digit number that is odd and has no digit repeated. Build it one seat at a time, from the left.",
      G("Smallest 5-digit odd number, all digits different = ?")),
    b("The first seat cannot be 0, so it takes 1. The second seat can take 0, the smallest digit of all.",
      W("1   0   _   _   _")),
    b("Next come the smallest digits not used yet: 2, and then 3.", W("1   0   2   3   _")),
    b("Now the last seat. The number must be odd, and no digit may repeat. Which digit goes there?",
      Q(["5", "4", "1"],
        "4 would make the number even. 1 and 3 are odd, but they are already used. So the smallest odd digit left is 5.")),
    b("Odd numbers end in 1, 3, 5, 7 or 9. But 1 and 3 are taken, so we use 5.", W("1   0   2   3   5")),
    b("The number is 10235.", A("10235")),
    b("Careful: 10234 is the smallest with different digits, but it is even. And 12345 forgets that 0 can sit in the second seat.",
      W("10234: even"), W("12345: forgets the 0")),
]

L["G4A_NUMBERS_017"] = [
    b("Which of these 4 numbers needs the most letters when it is written in Roman numerals? Let us write each one and count.",
      G("99, 98, 88, 78: which needs the most Roman symbols?")),
    b("First, a question. Is the biggest number always the longest in Roman numerals?",
      Q(["No, some big numbers are short", "Yes, bigger means longer"],
        "Think of 10. It is just X. But 8 is V I I I, which is much longer. Bigger does not mean longer.")),
    b("99 is 90 and 9. That is X C and I X. Only 4 letters, thanks to the take away trick.",
      W("99 = 90 + 9:   XC, IX   →  4 letters")),
    b("98 is 90 and 8. That is X C and V I I I, which makes 6 letters.", W("98 = 90 + 8:   XC, VIII   →  6 letters")),
    b("78 is 70 and 8. That is L X X and V I I I, which makes 7 letters.", W("78 = 70 + 8:   LXX, VIII   →  7 letters")),
    b("88 is 80 and 8. That is L X X X and V I I I, which makes 8 letters. The longest of all!",
      W("88 = 80 + 8:   LXXX, VIII   →  8 letters"), BX("8 letters")),
    b("So the answer is 88.", A("88")),
    b("The lesson: 8s make a numeral long, because an 8 needs 4 letters. 9s and 4s keep it short."),
]

L["G4A_NUMBERS_018"] = [
    b("Meena does not know the take away rule. She just adds up all four letters of X L I V. How much bigger is her total than the true value?",
      G("XLIV: Meena adds X, L, I and V. How much too big?")),
    b("First, Meena's way. X is 10, L is 50, I is 1 and V is 5. She adds them all and gets 66.", W("10 + 50 + 1 + 5 = 66")),
    b("Now the true value. In X L, the smaller letter X is in front of L. What does that mean?",
      Q(["take 10 away from 50", "add 10 to 50", "write 10 and then 50"],
        "A smaller letter in front of a bigger one is taken away. So X L is 50 minus 10.")),
    b("X L is 50 minus 10, which is 40. And I V is 5 minus 1, which is 4.",
      W("XL:  50 − 10 = 40", lab=True), W("IV:  5 − 1 = 4", lab=True)),
    b("So the true value is 40 plus 4, which is 44.", W("40 + 4 = 44")),
    b("Now compare. Meena's 66 minus the true 44 is 22.", W("66 − 44 = 22"), A("22")),
    b("Careful: 66 and 44 are both among the choices, but neither is what the question asks. It asks how much greater."),
    b("A neat check: each letter in front was added when it should be taken away, so it counts double. Twice 10 plus twice 1 is 22.",
      W("2 × 10 + 2 × 1 = 22")),
]

L["G4A_NUMBERS_019"] = [
    b("Lots of numbers round to 600 when we round to the nearest hundred. We want to count all of them.",
      G("How many whole numbers round to 600 (nearest hundred)?"),
      FIG(nline(500, 700, 10, [(600, "600")], note="Which numbers round to 600?"))),
    b("Numbers below 600 can round up to it. What is the smallest number that rounds up to 600?",
      Q(["550", "551", "500"],
        "A 5 in the tens place is enough to round up, and 550 has a 5 there. Anything smaller rounds down to 500 instead.")),
    b("The smallest is 550, because a 5 in the tens place rounds up.", W("smallest: 550")),
    b("Numbers above 600 round down while the tens digit is 4 or less. So the greatest is 649. The next one, 650, rounds up to 700.",
      W("greatest: 649"), W("650 rounds up to 700"),
      FIG(nline(500, 700, 10, [(550, "550"), (600, "600"), (649, "649")], note="From 550 to 649"))),
    b("Now count from 550 to 649. Subtract first: 649 minus 550 is 99.", W("649 − 550 = 99")),
    b("Careful, this is the trap! Subtracting counts the steps, not the numbers. We add 1 so that both ends are counted.",
      W("99 + 1 = 100")),
    b("So 100 whole numbers round to 600.", A("100")),
    b("That makes sense: 50 numbers from 550 to 599, and 50 more from 600 to 649.",
      W("550 to 599: 50 numbers     600 to 649: 50 numbers")),
]

L["G4A_NUMBERS_020"] = [
    b("A number rounds to 350 to the nearest ten, and to 300 to the nearest hundred. We want the greatest number that does both.",
      G("Rounds to 350 (nearest ten) and 300 (nearest hundred)"), W("Greatest such number = ?")),
    b("Take the first clue. The numbers that round to 350, to the nearest ten, run from 345 up to 354.",
      W("nearest ten gives 350:   345 to 354", name="c1")),
    b("Now the second clue. To the nearest hundred, where does 350 itself go?",
      Q(["up to 400", "down to 300"], "350 has a 5 in the tens place, and 5 or more rounds up. So 350 goes up to 400.")),
    b("So 350, and anything above it, rounds to 400 and not 300. Only the numbers below 350 are left.",
      W("350 and above round to 400"), X("354", note="rounds to 400", on="c1")),
    b("The numbers that fit both clues are 345, 346, 347, 348 and 349.", W("fits both:  345, 346, 347, 348, 349")),
    b("The greatest of these is 349.", A("349")),
    b("Check: 349 to the nearest ten is 350. And 349 to the nearest hundred is 300. Both clues fit."),
    b("The trap is 354. It is the greatest number that rounds to 350, but it does not fit the second clue."),
]

L["G4A_NUMBERS_022"] = [
    b("Sana and Ravi both start with 4,446. Sana rounds 3 times, one step at a time. Ravi rounds just once. Will they end at the same number?",
      G("4,446: Sana rounds in 3 steps, Ravi rounds once")),
    b("Sana first rounds to the nearest ten. The ones digit is 6, which is 5 or more, so she goes up to 4,450.",
      W("Sana:   4,446 → 4,450")),
    b("Next she rounds 4,450 to the nearest hundred. The tens digit is 5. Which way does she go?",
      Q(["up, to 4,500", "down, to 4,400"], "5 or more rounds up. The tens digit is exactly 5, so 4,450 goes up to 4,500.")),
    b("Up to 4,500. Then she rounds that to the nearest thousand. The hundreds digit is now 5, so up again, to 5,000.",
      W("4,450 → 4,500 → 5,000")),
    b("Now Ravi. He rounds 4,446 straight to the nearest thousand. The hundreds digit is 4, less than 5, so he goes down to 4,000.",
      W("Ravi:   4,446 → 4,000")),
    b("The difference is 5,000 minus 4,000, which is 1,000.", W("5,000 − 4,000 = 1,000"), A("1,000")),
    b("Here is the surprise. Each little rounding pushed Sana's number up a bit, until it tipped over. Rounding in steps can change the answer."),
    b("So always round straight from the number you started with. Ravi's way is the proper one."),
]

L["G4A_NUMBERS_023"] = [
    b("A printer numbers the pages from 1 to 120. Some page numbers have 1 digit, some have 2 and some have 3. So we count in three groups.",
      G("Pages 1 to 120: how many digits are printed?")),
    b("Pages 1 to 9 have 1 digit each. That is 9 pages, so 9 digits.", W("pages 1 to 9:   9 × 1 = 9", lab=True)),
    b("Pages 10 to 99 have 2 digits each. How many pages is that?",
      Q(["90", "89", "99"], "There are 99 pages up to page 99. Take away the first 9 pages, and 90 pages are left.")),
    b("90 pages with 2 digits each is 180 digits.", W("pages 10 to 99:   90 × 2 = 180", lab=True)),
    b("Now pages 100 to 120. Careful, this is the trap. 120 minus 100 is 20, but there are 21 pages, because page 100 counts too.",
      W("120 − 100 = 20"), W("20 + 1 = 21")),
    b("21 pages with 3 digits each is 63 digits.", W("pages 100 to 120:   21 × 3 = 63", lab=True)),
    b("Add the three groups: 9 plus 180 plus 63 is 252.", W("9 + 180 + 63 = 252"), A("252")),
    b("So: split the pages into groups by how many digits they have, and count both ends of every group."),
]

L["G4A_NUMBERS_024"] = [
    b("Take a 2-digit number, swap its digits, and add the two. The total must be 121. How many numbers can do that?",
      G("Number + its reverse = 121. How many 2-digit numbers?")),
    b("Try one to see what happens. 29 plus 92 is 121. It works! And look at its digits: 2 plus 9 is 11.",
      W("29 + 92 = 121"), W("2 + 9 = 11")),
    b("Here is why. In the ones column we add the two digits. In the tens column we add the same two digits again. So the total is 11 times the digit sum.",
      W("11 × (2 + 9) = 121")),
    b("So what must the two digits add up to, for a total of 121?",
      Q(["11", "121", "12"], "The total is 11 times the digit sum. 11 times 11 is 121, so the digits must add up to 11.")),
    b("The digits must add up to 11. List the pairs: 2 and 9, 3 and 8, 4 and 7, 5 and 6.",
      W("2 and 9     3 and 8     4 and 7     5 and 6")),
    b("Careful, this is the trap. Each pair makes two numbers, like 29 and 92. So 4 pairs give 8 numbers.",
      W("29, 92, 38, 83, 47, 74, 56, 65"), W("4 × 2 = 8")),
    b("So 8 different numbers work.", A("8")),
    b("And why not start with 1? Its partner would have to be 10, and 10 is not a digit."),
]

L["G4A_NUMBERS_025"] = [
    b("A number like 2552 reads the same forwards and backwards. We want the greatest 4-digit one whose digits add up to 14.",
      G("Reads the same both ways, digits add up to 14. Greatest?")),
    b("Such a number has a matching outer pair and a matching inner pair.", W("outer   inner   inner   outer")),
    b("The 4 digits add up to 14. Each digit is there twice, so one outer digit and one inner digit add up to half of 14, which is 7.",
      W("14 ÷ 2 = 7"), W("outer + inner = 7")),
    b("For the greatest number, which digit should be as big as possible?",
      Q(["the outer digit", "the inner digit"],
        "The outer digit sits in the thousands place, the most powerful seat. So make the outer digit as big as you can.")),
    b("The outer digit can be as big as 7. That leaves 0 for the inner digit, and 0 is allowed in the middle.",
      W("outer = 7     inner = 0")),
    b("So the number is 7007.", A("7007")),
    b("Check: 7 plus 0 plus 0 plus 7 is 14, and 7007 reads the same both ways.", W("7 + 0 + 0 + 7 = 14")),
    b("Two traps here. 6116 fits the clues, but it is smaller. And 7700 adds up to 14, but backwards it is not the same.",
      W("6116 < 7007"), W("7700: not the same backwards")),
]

L["G4A_NUMBERS_026"] = [
    b("In 8,35,264 we count the digits whose place value is more than 100 times their face value.",
      G("8,35,264: digits with place value > 100 × face value?"), FIG(chart("835264"))),
    b("Place value is face value times the worth of the seat. So this is really about seats: which seats are worth more than 100?",
      W("seats:  1, 10, 100, 1,000, 10,000, 1,00,000")),
    b("The 2 is in the hundreds place, so it is worth 200. That is exactly 100 times 2. Does it count?",
      W("2 × 100 = 200"),
      Q(["No, exactly 100 is not more than 100", "Yes, it counts"],
        "The question says more than 100 times. The 2 is worth exactly 100 times its face value, and exactly is not more.")),
    b("This is the trap. Exactly 100 times is not more than 100 times. So the 2 is out, and so are the 6 in the tens and the 4 in the ones."),
    b("The seats worth more than 100 are the thousands, ten-thousands and lakhs. The digits sitting there are 5, 3 and 8.",
      FIG(chart("835264", [0, 1, 2], note="Seats worth more than 100"))),
    b("That is 3 digits.", A("3")),
    b("Check one of them: the 5 is worth 5,000, which is 1,000 times 5. Yes, that is more than 100 times.",
      W("5 × 1,000 = 5,000")),
    b("So: turn the clue into seats, and read little words like more than very carefully."),
]

L["G4A_NUMBERS_027"] = [
    b("Among the Roman numerals from 1 to 39, some are written with exactly 2 letters. We count them in an orderly way.",
      G("Roman numerals 1 to 39: how many use exactly 2 letters?")),
    b("Only 3 letters are used up to 39: I, V and X. Let us sort the 2-letter numerals by their first letter.",
      W("letters:   I = 1     V = 5     X = 10")),
    b("Starting with I: I I is 2, I V is 4 and I X is 9. That is 3 numerals.", W("II = 2     IV = 4     IX = 9")),
    b("Starting with V, there is V I, which is 6. Is V V a proper numeral as well?",
      Q(["No, V is never repeated", "Yes, V V is 10"],
        "Two fives make 10, and 10 already has its own letter, X. So V is never written twice.")),
    b("So V gives just one numeral, V I. And V X is not allowed either, because V is never used to take away.", W("VI = 6")),
    b("Starting with X: X I is 11, X V is 15 and X X is 20. That is 3 more.", W("XI = 11     XV = 15     XX = 20")),
    b("Careful: X L has 2 letters too. But X L is 40, and that is outside 1 to 39.", W("XL = 40: too big")),
    b("Add them up: 3 plus 1 plus 3 is 7.", W("3 + 1 + 3 = 7"), A("7")),
    b("So when you count, sort into groups, and check the edges of the range."),
]

L["G4A_NUMBERS_028"] = [
    b("We add something to 49,950, and we want its ten-thousands digit to change. What is the smallest number that does it?",
      G("49,950 + ? changes the ten-thousands digit"), FIG(chart("49950", [0], note="The ten-thousands digit is 4"))),
    b("The ten-thousands digit is 4 now. Counting up, which is the first number with a different ten-thousands digit?",
      Q(["50,000", "59,950", "49,960"],
        "As we count up from 49,950, the 4 in front stays until all the other seats are full. It first changes at 50,000.")),
    b("The 4 changes to a 5 the moment we reach 50,000.", W("target: 50,000"),
      FIG(nline(49900, 50050, 10, [(49950, "49,950"), (50000, "50,000")], hops=[(49950, 50000, "+ ?")]))),
    b("So how far is 49,950 from 50,000? Subtract.", W("50,000 − 49,950 = 50")),
    b("Just 50! The number was already very close.", A("50")),
    b("Check: 49,950 plus 50 is 50,000. And adding anything less, like 49, stays below 50,000.",
      W("49,950 + 50 = 50,000"), W("49,950 + 49 = 49,999")),
    b("The trap is to think a big seat needs a big number, like 10,000. But the question asks for the smallest.",
      W("10,000 works, but it is not the smallest")),
]

L["G4A_NUMBERS_029"] = [
    b("Rahul writes a 6-digit number using only the digits 3, 0 and 8. Each must appear at least once. We want the greatest number.",
      G("6 digits, only 3, 0 and 8, each used at least once"), W("Greatest number = ?")),
    b("At least once. Does that mean a digit can be used more than once?",
      Q(["Yes, as many times as we like", "No, exactly once each"],
        "At least once means once or more. And we need 6 digits from only 3 kinds, so some digit has to repeat.")),
    b("So digits may repeat. For the greatest number, we want the biggest digit, 8, in as many seats on the left as possible."),
    b("But 3 and 0 must each appear once. So they take 2 seats, and 8 fills the other 4.", W("8   8   8   8   _   _")),
    b("Now the last two seats. The tens seat is worth more than the ones seat, so the bigger digit, 3, goes in the tens.",
      W("8   8   8   8   3   0")),
    b("The greatest number is 888830.", A("888830")),
    b("Careful with 888803. It is very close, but the 3 and the 0 are the other way round, and that makes it smaller.",
      W("888803 < 888830")),
    b("So: fill the big seats with the big digit, and give the small digits the smallest seats."),
]
