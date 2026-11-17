"""Square-number lessons for batch 18, written one by one (third group)."""
from imported_18_lib import ANS, ANSC, B, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, P, UL, W  # noqa: F401

LESSONS = {}

# A square and the next square add to 85.
LESSONS[P + "a5b0faf0-a638-453d-8069-b01a7747fb12"] = LESSON(
    B("Rohan has two trays. One holds a perfect square number of samosas, and the other holds the very next perfect square number. Together they hold 85. How many are on the larger tray?",
      GIVEN("q", "a square + the next square = 85")),
    B("Let's write out the square numbers, so we can see the neighbours side by side.",
      LB("sq", "1, 4, 9, 16, 25, 36, 49, 64, 81")),
    B("The two trays hold nearly the same amount, and 85 together. Roughly how big is each one?",
      ask=CHOOSE(["about 10 each", "around 40 each, about half of 85", "about 85 each"], 1,
                 "Two numbers that are close together and add up to 85 must each be near half of 85, which is a little over 40.")),
    B("So we want neighbours in the list that sit either side of 40 or so. That points at 36 and 49.",
      CIRC("sq", "36"), CIRC("sq", "49")),
    B("Test them. 36 plus 49 is 85. That's our pair.",
      W("l1", "36 + 49 = 85")),
    B("36 is 6 times 6 and 49 is 7 times 7, so they really are squares next door to each other. The larger tray holds 49 samosas.",
      W("l2", "6 × 6 = 36"), *ANSC("l3", "7 × 7 = 49", 49)),
    B("Careful: 36 is among the choices too. It is the smaller tray, and the question asks for the larger one."),
    B("Check the pairs on either side. 25 plus 36 is 61, too small. 49 plus 64 is 113, too big. Only 36 and 49 work.",
      W("l4", "25 + 36 = 61"), W("l5", "49 + 64 = 113")),
    B("So when two neighbouring squares add up to a total, look near half of the total, then test the pair."),
)

# Ravi's square of dots + 25 = 169.
LESSONS[P + "aa962e84-9236-4aec-9f62-77fac659d704"] = LESSON(
    B("Ravi's dots are in a perfect square. Meena says that with 25 more dots he would have 169 in all. How many dots are along each side of his square?",
      GIVEN("q", "Ravi's square of dots + 25 = 169. Side?")),
    B("169 is what he would have. How do we find what he has now?",
      ask=CHOOSE(["169 + 25", "169 − 25", "the square root of 169"], 1,
                 "The 169 already includes the 25 extra dots. To get back to what Ravi really has, take the 25 away.")),
    B("169 minus 25 is 144. Ravi has 144 dots now.",
      W("l1", "169 − 25 = 144")),
    B("His 144 dots make a square, so we need a number that times itself is 144. 10 times 10 is 100, which is a bit too small.",
      W("l2", "10 × 10 = 100")),
    B("144 ends in 4. Which number just above 10 could it be?",
      ask=CHOOSE(["11", "12", "13"], 1,
                 "Look at the last digits. 1 times 1 ends in 1, and 3 times 3 ends in 9. Only 2 times 2 ends in 4, so try 12.")),
    B("12 times 10 is 120, and 12 times 2 is 24. 120 plus 24 is 144. So each side has 12 dots.",
      W("l3", "12 × 10 = 120"), W("l4", "12 × 2 = 24"), W("l5", "120 + 24 = 144"), *ANSC("l6", "√144 = 12", 12)),
    B("The trap is 13. That is the square root of 169, the number with the extra dots in it. Ravi's own square is the 144.",
      W("l7", "13 × 13 = 169")),
    B("Check: 12 times 12 is 144, and 144 plus 25 is 169, just as Meena said.",
      W("l8", "144 + 25 = 169")),
    B("So first undo the extra to find what he really has. Then take the square root."),
)

# 15² − 9².
LESSONS[P + "afcda5cb-5f01-4e9b-ad14-6f127bff29df"] = LESSON(
    B("Meera's square rangoli has 15 tiles on each side. Arjun's smaller square has 9 tiles on each side. How many more tiles does Meera use than Arjun?",
      GIVEN("q", "Meera: 15 on each side. Arjun: 9 on each side. Gap?")),
    B("What do we need to compare?",
      ask=CHOOSE(["the sides: 15 − 9", "the totals: 15 × 15 and 9 × 9", "the borders: 4 × 15 and 4 × 9"], 1,
                 "The question asks about tiles used, and the tiles fill each whole square. So we need each total first: side times side.")),
    B("Meera's total: 15 times 10 is 150, 15 times 5 is 75, and 150 plus 75 is 225.",
      W("l1", "15 × 10 = 150"), W("l2", "15 × 5 = 75"), W("l3", "15 × 15 = 225")),
    B("Arjun's total: 9 times 9 is 81.",
      W("l4", "9 × 9 = 81")),
    B("Now the difference. 225 minus 81 is 144. Meera uses 144 more tiles.",
      *ANSC("l5", "225 − 81 = 144", 144)),
    B("The big trap is to start with 15 minus 9, which is 6, and square that to get 36. Squaring the difference is not the same as the difference of the squares.",
      W("l6", "15 − 9 = 6"), W("l7", "6 × 6 = 36")),
    B("Check by adding back: 81 plus 144 is 225, Meera's total.",
      W("l8", "81 + 144 = 225")),
    B("So square first, subtract second. Never subtract the sides and then square."),
)

# 16² + 49.
LESSONS[P + "b5495610-aeff-4c64-b3a6-d3658e9e4932"] = LESSON(
    B("Arjun tiles a square courtyard with exactly 16 tiles in each row. His father said the total is more than the square of 15 but less than the square of 17. Then Arjun tiles a small path with 49 tiles. How many tiles in all?",
      GIVEN("q", "Square courtyard, 16 in each row. Path: 49 tiles. Total?")),
    B("The courtyard is a square with 16 tiles in each row. How many tiles does it need?",
      ask=CHOOSE(["16 × 4", "16 × 16", "16 + 16"], 1,
                 "A square has as many rows as it has tiles in a row. So there are 16 rows of 16, and that means multiplying 16 by itself.")),
    B("16 times 10 is 160, and 16 times 6 is 96. 160 plus 96 is 256 tiles for the courtyard.",
      W("l1", "16 × 10 = 160"), W("l2", "16 × 6 = 96"), W("l3", "16 × 16 = 256")),
    B("Now test the father's clue. The square of 15 is 225, and the square of 17 is 289. Is 256 between them? Yes, it is.",
      W("l4", "15² = 225"), W("l5", "17² = 289"), W("l6", "225 < 256 < 289")),
    B("Then the path adds 49 tiles. 256 plus 49 is 305 tiles in all.",
      *ANSC("l7", "256 + 49 = 305", 305)),
    B("The trap is using the father's numbers as the answer. 225 is only the square of 15, the lower fence. The courtyard itself is 256."),
    B("Check by taking the path away again: 305 minus 49 is 256, the courtyard.",
      W("l8", "305 − 49 = 256")),
    B("So pick out what the question asks for: square the row for the courtyard, then add the path. The father's clue was only there as a check."),
)

# 3 boxes of 5² and 2 boxes of 8².
LESSONS[P + "c1429cf6-78e1-40bb-9fa8-b77c5ca16e08"] = LESSON(
    B("Meena's small box holds 5 squared samosas and her large box holds 8 squared. She sells 3 small boxes and 2 large boxes. How many samosas is that?",
      W("q", "3 × 5² + 2 × 8²", "given")),
    B("What does 5 squared mean?",
      ask=CHOOSE(["5 × 2", "5 × 5", "5 + 5"], 1,
                 "Squared means the number multiplied by itself, like a square with 5 rows of 5. So 5 squared is 5 times 5.")),
    B("5 squared is 5 times 5, which is 25. A small box holds 25 samosas.",
      UL("q", "5²"), W("l1", "5² = 25")),
    B("8 squared is 8 times 8, which is 64. A large box holds 64 samosas.",
      UL("q", "8²"), W("l2", "8² = 64")),
    B("3 small boxes: 3 times 25 is 75 samosas.",
      W("l3", "3 × 25 = 75")),
    B("2 large boxes: 2 times 64 is 128 samosas.",
      W("l4", "2 × 64 = 128")),
    B("Altogether, 75 plus 128 is 203 samosas.",
      *ANSC("l5", "75 + 128 = 203", 203)),
    B("The classic slip is reading 5 squared as 5 times 2. That would make a small box hold only 10, and the total would come out far too small."),
    B("Check by taking away: 203 minus 128 is 75, the samosas in the small boxes.",
      W("l6", "203 − 128 = 75")),
    B("So do the squares first, then the times, then add."),
)

# Square garden, each side + 5 m, new area 576 sq m.
LESSONS[P + "c6ab10b2-4525-4d4d-a7bd-2b183f0da88f"] = LESSON(
    B("Raju's grandfather has a square garden. He adds 5 metres to each side, and the new square garden has an area of 576 square metres. How long was a side of the first garden?",
      GIVEN("q", "Square garden, each side + 5 m → area 576 sq m")),
    B("Which do we find first?",
      ask=CHOOSE(["576 − 5", "the side of the new garden", "576 ÷ 4"], 1,
                 "The 5 metres were added to a side, not to the area. So we need the new side first, and then we can step back 5.")),
    B("The new garden is a square, so its side times itself is 576. 20 times 20 is 400 and 30 times 30 is 900, so the side is between 20 and 30.",
      W("l1", "20 × 20 = 400"), W("l2", "30 × 30 = 900")),
    B("576 ends in 6, so the side ends in 4 or 6. Try 24: 24 times 20 is 480, 24 times 4 is 96, and 480 plus 96 is 576. The new side is 24 metres.",
      W("l3", "24 × 20 = 480"), W("l4", "24 × 4 = 96"), W("l5", "24 × 24 = 576")),
    B("The new side is the old side plus 5. So step back: 24 minus 5 is 19. The first garden had a side of 19 metres.",
      *ANSC("l6", "24 − 5 = 19", 19)),
    B("The trap is stopping at 24. That is the side after the garden grew. And adding another 5 would be going the opposite way."),
    B("Check: 19 plus 5 is 24, and 24 times 24 is 576. It fits.",
      W("l7", "19 + 5 = 24")),
    B("So work backwards: a square root gives the new side, then undo the change to get the old side."),
)

# The border ring of a square courtyard has 76 tiles.
LESSONS[P + "d1258e2b-ee26-4aa6-96dd-b95e249144d9"] = LESSON(
    B("Aman tiles a square courtyard. The outermost ring of tiles, the border, has 76 tiles. How many tiles cover the whole courtyard?",
      GIVEN("q", "Square courtyard. Border ring: 76 tiles. Total?")),
    B("We need the number of tiles along one side. But count the border one side at a time, and something odd happens at the corners."),
    B("If we count all 4 sides in full, how many times is each corner tile counted?",
      ask=CHOOSE(["once", "2 times", "4 times"], 1,
                 "A corner tile sits at the end of two sides: the one going across and the one going down. So it gets counted with both of them.")),
    B("Each corner is counted 2 times, and there are 4 corners. So 4 full sides come to 4 more than the border: 76 plus 4 is 80.",
      W("l1", "76 + 4 = 80"), NOTE("l1", "+ 4", "corners, counted twice")),
    B("4 full sides make 80, so one side is 80 divided by 4, which is 20 tiles.",
      W("l2", "80 ÷ 4 = 20")),
    B("The whole courtyard is 20 rows of 20. 20 times 20 is 400 tiles.",
      *ANSC("l3", "20 × 20 = 400", 400)),
    B("The trap is 76 divided by 4, which is 19, and then 19 times 19, which is 361. That forgets that the corners are shared.",
      W("l4", "76 ÷ 4 = 19"), W("l5", "19 × 19 = 361")),
    B("Check: 4 sides of 20 is 80. Take off the 4 corners that were counted double, and we get 76, just what Aman counted.",
      W("l6", "4 × 20 − 4 = 76")),
    B("So for the border of a square: add 4 for the shared corners, divide by 4 to get the side, then square the side for the total."),
)

# square + 45 = a bigger square with 23 on each side.
LESSONS[P + "d6446615-ea54-4e31-8414-3703da1e62f2"] = LESSON(
    B("Priya has diyas in a square. With 45 more, she can make a bigger square that has 23 diyas on each side. How many diyas are in her first square?",
      GIVEN("q", "square + 45 = a bigger square with 23 on each side")),
    B("Where do we start?",
      ask=CHOOSE(["23 + 45", "the bigger square: 23 × 23", "45 − 23"], 1,
                 "We know everything about the bigger square: 23 on each side. So we can count its diyas, and then step back to the first square.")),
    B("23 times 20 is 460, and 23 times 3 is 69. 460 plus 69 is 529. The bigger square has 529 diyas.",
      W("l1", "23 × 20 = 460"), W("l2", "23 × 3 = 69"), W("l3", "23 × 23 = 529")),
    B("The bigger square is the first square plus 45. So how do we get back to the first square?",
      ask=CHOOSE(["529 + 45", "529 − 45", "529 ÷ 45"], 1,
                 "The 45 were added to make the bigger square. To go back to the first square, take them off again.")),
    B("529 minus 45 is 484. Her first square has 484 diyas.",
      *ANSC("l4", "529 − 45 = 484", 484)),
    B("The story says the first arrangement is a square too, so 484 should be a square number. 22 times 20 is 440, 22 times 2 is 44, and 440 plus 44 is 484. It is 22 times 22.",
      W("l5", "22 × 20 = 440"), W("l6", "22 × 2 = 44"), W("l7", "22 × 22 = 484")),
    B("Careful: 529 is among the choices. That is the bigger square, after the 45 were added."),
    B("So when you know the bigger square, build it first, then take away what was added. And check that what is left is a square too."),
)

# A square with 7 more rows and 7 more columns would have 225 tiles.
LESSONS[P + "dbdd5f42-8b96-4dfa-9670-86a9ad7f0b0e"] = LESSON(
    B("Riya has a square rangoli of tiles. With 7 more rows and 7 more columns, the bigger square would need 225 tiles in total. How many tiles are in the rangoli she has now?",
      GIVEN("q", "her square with 7 more rows and columns = 225 tiles")),
    B("The bigger rangoli is a square of 225 tiles, so its side times itself is 225. 15 times 10 is 150, 15 times 5 is 75, and 150 plus 75 is 225. Its side is 15.",
      W("l1", "15 × 10 = 150"), W("l2", "15 × 5 = 75"), W("l3", "15 × 15 = 225")),
    B("The bigger square has 7 more rows and 7 more columns than hers. So what is the side of her square?",
      ask=CHOOSE(["15 − 14 = 1", "15 − 7 = 8", "225 − 7 = 218"], 1,
                 "7 more rows make it 7 taller, and 7 more columns make it 7 wider. Each side grew by 7 just once, so step each side back by 7.")),
    B("15 minus 7 is 8. Her rangoli is 8 by 8.",
      W("l4", "15 − 7 = 8")),
    B("So how many tiles does she have now?",
      ask=CHOOSE(["8", "8 × 8 = 64", "8 × 4 = 32"], 1,
                 "8 is only one side. The tiles fill the whole square, 8 rows of 8, so we multiply 8 by 8.")),
    B("8 times 8 is 64. Her rangoli has 64 tiles.",
      *ANSC("l5", "8 × 8 = 64", 64)),
    B("The trap is 7 times 7, which is 49. The 7 changes the side of the square. It is not a little square of tiles to take away.",
      W("l6", "7 × 7 = 49")),
    B("Check: 8 plus 7 is 15, and 15 times 15 is 225. It fits.",
      W("l7", "8 + 7 = 15")),
    B("So work backwards from the bigger square: square root for its side, step the side back, then square again."),
)
