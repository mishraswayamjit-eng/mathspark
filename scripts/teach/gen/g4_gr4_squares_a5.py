"""gr4_squares, written per question: G4A_SQUARES_037 to 048."""
from g4_gr4_numbers_lib import A, C, FIG, G, Q, W, X, b, dots

L = {}

L["G4A_SQUARES_037"] = [
    b("A pattern is given, and we use it to add all the odd numbers from 1 to 39. No long adding needed!",
      G("1 + 3 = 4,   1 + 3 + 5 = 9,   1 + 3 + 5 + 7 = 16", lab=True), W("1 + 3 + 5 + ... + 39 = ?")),
    b("Look at the answers: 4, 9, 16. Those are 2 times 2, 3 times 3 and 4 times 4. All squares!",
      W("4 = 2 × 2      9 = 3 × 3      16 = 4 × 4")),
    b("1 plus 3 plus 5 has 3 numbers, and its sum is 3 times 3. So what gets squared?",
      Q(["how many numbers are added", "the last number added", "the first number"],
        "With 3 odd numbers the sum is 3 times 3. With 4 odd numbers it is 4 times 4. So we square how many numbers there are.")),
    b("The sum is the count of odd numbers, times itself. So we need to know how many odd numbers there are from 1 to 39.",
      FIG(dots(4, 4, note="1 + 3 + 5 + 7 builds a 4 by 4 square"))),
    b("From 1 to 40 there are 40 numbers, and half of them are odd. Half of 40 is 20.",
      W("1 to 40:  40 numbers, half are odd"), W("40 ÷ 2 = 20")),
    b("So there are 20 odd numbers, and the sum is 20 times 20, which is 400.", W("20 × 20 = 400"), A("400")),
    b("The trap is to square the last number, 39. The pattern squares the count, not the last number."),
    b("Check with the pattern: 1, 3, 5, 7 ends in 7, and half of 7 plus 1 is 4. The sum was 4 times 4. It fits.",
      W("(7 + 1) ÷ 2 = 4")),
]

L["G4A_SQUARES_038"] = [
    b("Two numbers come one after the other, and their squares differ by 37. We want the larger number.",
      G("Two neighbours. Their squares differ by 37. Larger = ?")),
    b("Look for a pattern with small neighbours first. 4 squared is 16 and 5 squared is 25. The difference is 9.",
      W("25 − 16 = 9")),
    b("The squares of 4 and 5 differ by 9. How is 9 connected to 4 and 5?",
      Q(["9 is 4 + 5", "9 is 5 − 4", "9 is 4 × 5"],
        "4 plus 5 is 9. The difference of two neighbouring squares is the sum of the two numbers.")),
    b("4 plus 5 is 9. Try another pair, 5 and 6. 36 minus 25 is 11, and 5 plus 6 is 11. It works again!",
      W("4 + 5 = 9"), W("36 − 25 = 11"), W("5 + 6 = 11")),
    b("So our two neighbours add up to 37. Which neighbours add up to 37? 18 and 19.", W("18 + 19 = 37")),
    b("Check with the squares. 19 times 19 is 361 and 18 times 18 is 324. They differ by 37.",
      W("19 × 19 = 361"), W("18 × 18 = 324"), W("361 − 324 = 37")),
    b("So the larger number is 19.", A("19")),
    b("Careful: 18 is the smaller one. And 37 is the gap between the squares, not one of the numbers."),
]

L["G4A_SQUARES_039"] = [
    b("144 children stand in a square. Only the children on the outside edge hold a flag. How many is that?",
      G("144 children in a square. How many on the outside edge?")),
    b("First, the size of the square. 12 times 12 is 144, so each side has 12 children.",
      W("12 × 12 = 144"), FIG(dots(12, 12, note="12 rows of 12"))),
    b("There are 4 sides with 12 children on each. Is the answer 4 times 12, which is 48?",
      W("4 × 12 = 48"),
      Q(["No, the corners get counted twice", "Yes, 48"],
        "A child in a corner stands on two sides at once. So 4 times 12 counts each corner child twice.")),
    b("This is the trap. Each corner child belongs to two sides, so 48 counts 4 children twice."),
    b("Take away those 4 extra counts. 48 minus 4 is 44.", W("48 − 4 = 44"), A("44")),
    b("Check another way. The top and bottom rows have 12 each. The two sides have 10 more each, without the corners.",
      W("12 + 12 + 10 + 10 = 44")),
    b("Or think of the children inside: they make a 10 by 10 square of 100. And 144 minus 100 is 44.",
      W("10 × 10 = 100"), W("144 − 100 = 44")),
]

L["G4A_SQUARES_040"] = [
    b("A square floor of 225 tiles. The tiles on both diagonals are red. How many red tiles?",
      G("225 tiles in a square. Both diagonals are red. How many?")),
    b("First the size. 15 times 15 is 225, so the floor is 15 tiles by 15 tiles.", W("15 × 15 = 225")),
    b("A diagonal goes from corner to corner, and takes one tile from every row. So each diagonal has 15 tiles.",
      W("each diagonal: 15 tiles"),
      FIG({"kind": "grid", "rows": 5, "cols": 5, "note": "A small floor, 5 by 5",
           "shaded": [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [0, 4], [1, 3], [3, 1], [4, 0]]})),
    b("Two diagonals of 15 tiles. Is the answer 15 plus 15, which is 30?",
      W("15 + 15 = 30"),
      Q(["No, they share the middle tile", "Yes, 30"],
        "15 is odd, so there is one tile exactly in the middle. Both diagonals pass through it, and 30 counts it twice.")),
    b("Here is the trap. Because 15 is odd, the two diagonals cross on the middle tile. We counted that tile twice."),
    b("So take 1 away. 30 minus 1 is 29.", W("30 − 1 = 29"), A("29")),
    b("Look at the small floor, 5 by 5. It has 5 plus 5 minus 1 red tiles, which is 9. Count them and see!",
      W("5 + 5 − 1 = 9")),
]

L["G4A_SQUARES_041"] = [
    b("Some numbers are the sum of two perfect squares. For example, 13 is 4 plus 9. One of these 4 numbers is not.",
      G("Which is NOT a sum of two perfect squares?"), W("20     34     29     21", name="o")),
    b("The squares small enough to use are 1, 4, 9, 16 and 25.", W("squares:  1, 4, 9, 16, 25")),
    b("Test 20. Take away 4, and 16 is left. Both are squares, so 20 can be made.", W("20 = 4 + 16")),
    b("Test 34. Take away 25. What is left, and is it a square?",
      Q(["9, and it is a square", "9, but it is not a square", "11"],
        "34 minus 25 is 9, and 9 is 3 times 3. So 34 is 25 plus 9, which is two squares.")),
    b("34 is 9 plus 25. And 29 is 4 plus 25. Both can be made.",
      W("34 = 9 + 25"), W("29 = 4 + 25"), X("20", on="o"), X("34", on="o"), X("29", on="o")),
    b("Now 21. Take away each square in turn: 20, 17, 12 and 5 are left. None of those is a square.",
      W("21 − 1 = 20"), W("21 − 4 = 17"), W("21 − 9 = 12"), W("21 − 16 = 5")),
    b("So 21 cannot be made.", A("21")),
    b("The method: take away one square, and see whether a square is left. Try every square, so that nothing is missed."),
]

L["G4A_SQUARES_042"] = [
    b("Soldiers stand in a square. Then 3 full rows and 3 full columns march away, 69 soldiers in all, and a smaller square is left.",
      G("Square of soldiers. 3 rows and 3 columns leave: 69 go.")),
    b("When 3 rows and 3 columns leave, the square that remains has sides that are 3 shorter.",
      W("new side = old side − 3")),
    b("Is 69 simply 3 rows plus 3 columns of soldiers?",
      Q(["No, some soldiers are in both", "Yes, 6 lines of soldiers"],
        "A soldier in the corner is in a row that leaves and also in a column that leaves. He must not be counted twice.")),
    b("That is the trap, so we go a safer way. The soldiers who left are the big square minus the small square.",
      W("big square − small square = 69")),
    b("Test sides of 12 and 9. 144 minus 81 is 63. Not enough.", W("12 × 12 = 144"), W("9 × 9 = 81"), W("144 − 81 = 63")),
    b("Test sides of 13 and 10. 169 minus 100 is 69. That matches!",
      W("13 × 13 = 169"), W("10 × 10 = 100"), W("169 − 100 = 69")),
    b("So at first there were 13 rows of 13, which is 169 soldiers.", A("169")),
    b("Careful: 69 divided by 3 is 23, but a 23 by 23 square would lose far more than 69 soldiers.",
      W("69 ÷ 3 = 23"), W("23 × 23 − 20 × 20 = 129")),
]

L["G4A_SQUARES_043"] = [
    b("In each pair the two numbers add up to 60. Which pair has the greatest product? We can find out without doing all four.",
      G("Which product is the greatest?"), W("29 × 31     30 × 30     28 × 32     27 × 33")),
    b("Learn from small numbers first. Take pairs that add up to 10.", W("5 × 5 = 25"), W("4 × 6 = 24"), W("3 × 7 = 21")),
    b("5 times 5 is 25, 4 times 6 is 24 and 3 times 7 is 21. What happens as the two numbers move apart?",
      Q(["the product gets smaller", "the product gets bigger", "it stays the same"],
        "25, then 24, then 21. The further apart the two numbers are, the smaller the product.")),
    b("The equal pair wins. The further apart the numbers move, the smaller the product gets."),
    b("The same happens here. The equal pair is 30 times 30, which is 900.", W("30 × 30 = 900")),
    b("29 times 31 is 899, just 1 less. And 28 times 32 is 896.", W("29 × 31 = 899"), W("28 × 32 = 896"), W("27 × 33 = 891")),
    b("So the greatest product is 30 times 30.", A("30 × 30")),
    b("Careful: 33 is the biggest number here, but its partner 27 is the smallest. For the same sum, the square always wins."),
]

L["G4A_SQUARES_044"] = [
    b("Look at the pattern in the question. We use it to find 11111 times 11111 without multiplying.",
      G("11 × 11 = 121,   111 × 111 = 12321,  ...", lab=True), W("Sum of the digits of 11111 × 11111 = ?")),
    b("121. 12321. 1234321. The digits climb up, and then come back down.", W("121      12321      1234321")),
    b("11 has two 1s, and its answer climbs to 2. 111 has three 1s, and its answer climbs to 3. How high will 11111 climb?",
      Q(["to 5", "to 4", "to 9"], "Count the 1s in 11111. There are 5 of them, so the answer climbs to 5.")),
    b("11111 has five 1s. So the answer climbs to 5 and comes back down.", W("11111 × 11111 = 123454321")),
    b("Now add its digits. Going up: 1, 2, 3, 4 and 5 make 15.", W("1 + 2 + 3 + 4 + 5 = 15")),
    b("Coming down: 4, 3, 2 and 1 make 10.", W("4 + 3 + 2 + 1 = 10")),
    b("15 plus 10 is 25.", W("15 + 10 = 25"), A("25")),
    b("The trap is to stop at 15. The digits come back down too. And look: 25 is 5 times 5, another square!"),
]

L["G4A_SQUARES_045"] = [
    b("Kabir's age is a perfect square now. In 9 years it will be a perfect square again. How old is he?",
      G("Age now: a perfect square. In 9 years: a square again.")),
    b("List some perfect squares that could be ages.", W("1, 4, 9, 16, 25, 36, 49", name="sq")),
    b("Add 9 to each, and see if we land on another square. 1 becomes 10. 4 becomes 13. 9 becomes 18. No luck yet.",
      W("1 + 9 = 10"), W("4 + 9 = 13"), W("9 + 9 = 18")),
    b("Now try 16. What is 16 plus 9, and is it a square?",
      Q(["25, and it is a square", "25, but it is not a square", "24"],
        "16 plus 9 is 25. And 25 is 5 times 5, so it is a perfect square.")),
    b("16 plus 9 is 25, which is 5 times 5. It works!", W("16 + 9 = 25"), C("16", on="sq")),
    b("Could a bigger age work too? 25 plus 9 is 34. 36 plus 9 is 45. No. After 16, the squares are more than 9 apart.",
      W("25 + 9 = 34"), W("36 + 9 = 45")),
    b("So Kabir is 16 this year.", A("16")),
    b("Careful: 25 is the age he will reach, not his age now."),
]

L["G4A_SQUARES_046"] = [
    b("We multiply 12 by something to get a perfect square. But the square must be greater than 100. We want the smallest multiplier.",
      G("12 × ? = a perfect square greater than 100 (smallest ?)")),
    b("First, what turns 12 into any perfect square? 12 is 2 times 2 times 3. The 3 has no partner.", W("12 = 2 × 2 × 3")),
    b("Multiply by 3, and we get 36, a perfect square. But look at the question again.", W("12 × 3 = 36")),
    b("36 is a perfect square. Does it answer the question?",
      Q(["No, it is not greater than 100", "Yes, 3 is the smallest"],
        "The question wants a perfect square greater than 100. 36 is far below 100.")),
    b("This is the trap. 36 is too small. So we look at bigger multipliers, for a square above 100."),
    b("12 times 9 is 108. That is above 100, but 108 is between 100 and 121, so it is not a square.",
      W("12 × 9 = 108"), W("100 < 108 < 121")),
    b("12 times 12 is 144. A perfect square, and greater than 100!", W("12 × 12 = 144"), A("12")),
    b("And nothing smaller works. The only square between 100 and 144 is 121, and 12 does not divide 121."),
]

L["G4A_SQUARES_047"] = [
    b("Anu squares an odd number and subtracts 1. Some number always divides her answer. We want the greatest such number.",
      G("(odd number)² − 1: what always divides it?")),
    b("Try the first few odd numbers. 3 squared is 9, and 9 minus 1 is 8.", W("3² − 1 = 8")),
    b("5 squared is 25, minus 1 is 24. 7 squared is 49, minus 1 is 48. 9 squared is 81, minus 1 is 80.",
      W("5² − 1 = 25 − 1 = 24"), W("7² − 1 = 49 − 1 = 48"), W("9² − 1 = 81 − 1 = 80")),
    b("The very first answer is 8. Can a number bigger than 8 divide 8 exactly?",
      Q(["No, never", "Yes, sometimes"],
        "A number cannot be divided exactly by something bigger than itself. So nothing above 8 can divide every answer.")),
    b("This is the key idea. The first answer is 8, so our number cannot be more than 8. That rules out 16 and 24.",
      W("16 and 24 do not divide 8")),
    b("Does 8 divide them all? 24 is 3 times 8. 48 is 6 times 8. 80 is 10 times 8. Yes!",
      W("24 = 3 × 8"), W("48 = 6 × 8"), W("80 = 10 × 8")),
    b("So the greatest number that always divides her answer is 8.", A("8")),
    b("Careful: 4 divides them all too, but it is not the greatest. And 24 divides some of the answers, but not all."),
]

L["G4A_SQUARES_048"] = [
    b("The year 2025 is 45 times 45, a perfect square. How many years until the next perfect square year?",
      G("2025 = 45 × 45. Years until the next perfect square = ?")),
    b("Which multiplication gives the next perfect square?",
      Q(["46 × 46", "45 × 46", "50 × 50"],
        "Perfect squares come from the counting numbers, one after another. After 45 times 45 comes 46 times 46.")),
    b("The next square is 46 times 46. Build it up. 46 times 45 is one more 45 than 45 times 45. That is 2070.",
      W("2025 + 45 = 2070")),
    b("Then 46 times 46 is one more 46. 2070 plus 46 is 2116.", W("2070 + 46 = 2116"), W("46 × 46 = 2116")),
    b("So the next perfect square year is 2116. That is 91 years after 2025.", W("2116 − 2025 = 91"), A("91")),
    b("Notice: we added 45 and then 46, and 45 plus 46 is 91. Neighbouring squares always differ by the sum of the two numbers.",
      W("45 + 46 = 91")),
    b("Careful: 90 is twice 45, which is 1 short. And 46 is the next number to square, not the number of years.",
      W("2 × 45 = 90:  one short")),
]
