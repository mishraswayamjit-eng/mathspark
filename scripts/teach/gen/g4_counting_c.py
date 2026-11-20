"""gr4_counting lessons, part C: G4A_COUNTING_017 to G4A_COUNTING_032."""
from g4_counting_lib import a, b, c, g, l, n, qf, u, w, x

LESSONS = {}

LESSONS["G4A_COUNTING_017"] = [
    b("How many 2-digit numbers are multiples of 7?", g("q", "2-digit multiples of 7: how many?")),
    b("Multiples of 7 are the 7 times table: 7, 14, 21 and so on. But 7 itself has only 1 digit. So the first one we want is 14.",
      l("m", "7, 14, 21, ..."), x("m", "7"), w("c1", "7 × 2 = 14")),
    b("Now the biggest one. 7 times 14 is 98. What about 7 times 15?", w("c2", "7 × 14 = 98"), w("c3", "7 × 15 = 105"),
      ask=c("105: too big, it has 3 digits", ["105: still a 2-digit number", "99"],
            "98 plus 7 is 105. That has 3 digits, so it is out. 98 is the last one.")),
    b("So our multiples go from 7 times 2 up to 7 times 14.", l("r", "7 × 2, 7 × 3, ... , 7 × 14")),
    b("Now count the multipliers from 2 to 14. From 1 to 14 there are 14 of them. Leave out the 1, and there are 13.",
      w("c4", "14 − 1 = 13")),
    b("So there are 13 two-digit multiples of 7.", a("ans", "13 numbers")),
    b("The trap is 14, which forgets that 7 itself is only a 1-digit number. Find the first and the last, then count."),
]

LESSONS["G4A_COUNTING_018"] = [
    b("Sunita climbs from the 1st floor to the 4th floor: 48 steps. Every floor has the same number of steps. How many steps from the 1st floor to the 7th?",
      g("q", "1st → 4th floor: 48 steps. 1st → 7th floor: ?")),
    b("From the 1st floor to the 4th floor, how many flights of stairs does she climb?",
      ask=c("3", ["4", "5"],
            "Count the climbs: 1st to 2nd, 2nd to 3rd, 3rd to 4th. She starts on the 1st floor, so she does not climb up to it.")),
    b("1st to 2nd, 2nd to 3rd, 3rd to 4th. That is 3 flights, not 4.", w("c1", "4 − 1 = 3")),
    b("So 48 steps are shared among 3 flights. 48 divided by 3 is 16 steps in each flight.", w("c2", "48 ÷ 3 = 16")),
    b("Now the 7th floor. In the same way, 1st to 7th is 6 flights.", w("c3", "7 − 1 = 6")),
    b("6 flights of 16 steps. 6 times 16 is 96.", w("c4", "6 × 16 = 96")),
    b("So she would climb 96 steps.", a("ans", "96 steps")),
    b("Floors are like fence posts, and flights of stairs are the gaps. Always count the gaps."),
]

LESSONS["G4A_COUNTING_019"] = [
    b("An ice-cream shop has 4 flavours: mango, chocolate, vanilla and strawberry. Rohan picks 2 different flavours. How many different pairs can he choose?",
      g("q", "4 flavours: M, C, V, S. Pairs of 2 different ones?")),
    b("Let's list the pairs in order, so that we miss none. Mango can go with chocolate, vanilla or strawberry. 3 pairs.",
      l("p1", "MC  MV  MS")),
    b("Next, chocolate. Chocolate with mango is already on the list. So how many new pairs does chocolate make?",
      ask=c("2", ["3", "1"],
            "Chocolate with mango is the same cup as mango with chocolate. The new ones are chocolate with vanilla, and chocolate with strawberry.")),
    b("Chocolate gives 2 new pairs. Then vanilla with strawberry is the last new pair.", l("p2", "CV  CS"), l("p3", "VS")),
    b("Add them. 3 plus 2 plus 1 is 6.", w("c1", "3 + 2 + 1 = 6")),
    b("So Rohan can choose 6 different pairs.", a("ans", "6 pairs")),
    b("The trap is 4 times 3, which is 12. That counts every pair twice. In a cup, the order does not matter, so halve it.",
      w("ck1", "4 × 3 = 12"), w("ck2", "12 ÷ 2 = 6")),
]

LESSONS["G4A_COUNTING_020"] = [
    b("Using each of the digits 2, 0 and 5 exactly once, how many 3-digit numbers can be made?",
      g("q", "Digits 2, 0, 5, each once. 3-digit numbers?")),
    b("One of these digits cannot go in the hundreds place. Which one?",
      ask=c("0", ["2", "5"],
            "If 0 goes first, the number is not really a 3-digit number. A 0 at the front counts for nothing.")),
    b("So the hundreds digit is 2 or 5. Start with 2: the other two digits can go as 0 then 5, or 5 then 0. That gives 205 and 250.",
      l("m1", "205, 250")),
    b("Start with 5 and we get 502 and 520.", l("m2", "502, 520")),
    b("Count them: 2 numbers and 2 numbers. 2 plus 2 is 4.", w("c1", "2 + 2 = 4")),
    b("So 4 three-digit numbers can be made.", a("ans", "4 numbers")),
    b("The trap is 3 times 2 times 1, which is 6. That would also count numbers that start with 0. Watch out for 0 at the front."),
]

LESSONS["G4A_COUNTING_021"] = [
    b("A big triangle has 2 lines drawn from its top corner down to its base, making 3 small triangles side by side. How many triangles are there, of every size?",
      g("q", "3 small triangles side by side. Every size?"), qf("G4A_COUNTING_021")),
    b("Let's count size by size. First the small ones: left, middle and right. That is 3.", l("s1", "1 part: 3")),
    b("Can 2 small triangles next to each other make a bigger triangle?",
      ask=c("yes: left+middle, middle+right", ["no", "yes, but only one way"],
            "Join the left and the middle: the shape still has 3 corners, so it is a triangle. The middle and the right do the same.")),
    b("Left with middle is one. Middle with right is another. That is 2 triangles made of 2 parts.", l("s2", "2 parts: 2")),
    b("Left with right? They do not touch, so that is not a shape. And all 3 parts together make the 1 big triangle.",
      l("s3", "3 parts: 1")),
    b("Add them. 3 plus 2 plus 1 is 6.", w("c1", "3 + 2 + 1 = 6")),
    b("So there are 6 triangles in the figure.", a("ans", "6 triangles")),
    b("Count shapes by size: 1 part, 2 parts, 3 parts. Then nothing hides from you."),
]

LESSONS["G4A_COUNTING_022"] = [
    b("In a queue, Ravi is 8th from the front and Sana is 15th from the front. How many people stand between them?",
      g("q", "Ravi: 8th. Sana: 15th. How many between?"), qf("G4A_COUNTING_022")),
    b("Between means after Ravi and before Sana. So we want the people in places 9, 10, 11, 12, 13 and 14.",
      l("m", "9, 10, 11, 12, 13, 14")),
    b("Count those places. How many are there?",
      ask=c("6", ["7", "8"], "Point at each one: 9, 10, 11, 12, 13, 14. Do not count Ravi's 8 or Sana's 15.")),
    b("There are 6. Now a quick way. 15 minus 8 is 7. But that 7 counts Sana's own place too.", w("c1", "15 − 8 = 7")),
    b("So take 1 away for Sana. 7 minus 1 is 6.", w("c2", "7 − 1 = 6")),
    b("So 6 people stand between them.", a("ans", "6 people")),
    b("For 'between', subtract the positions, then take away 1."),
]

LESSONS["G4A_COUNTING_023"] = [
    b("How many numbers from 100 to 200, counting both, end in the digit 0?", g("q", "100 to 200. How many end in 0?")),
    b("Numbers ending in 0 are the tens: 100, 110, 120 and so on, up to 200.", l("m", "100, 110, 120, ... , 190, 200")),
    b("From 100 to 200 is a distance of 100. Each jump is 10, so there are 10 jumps.",
      w("c1", "200 − 100 = 100"), w("c2", "100 ÷ 10 = 10")),
    b("10 jumps. So how many numbers?",
      ask=c("11", ["10", "9"], "Think of fence posts. 10 gaps need 11 posts, because both ends count.")),
    b("The numbers are the posts, and the jumps are the gaps. 10 plus 1 is 11.", w("c3", "10 + 1 = 11")),
    b("So 11 numbers end in 0.", a("ans", "11 numbers")),
    b("Whenever both ends are counted, it is the jumps plus 1."),
]

LESSONS["G4A_COUNTING_024"] = [
    b("A book's pages are numbered from 1. In all, 129 digits were printed. How many pages does the book have?",
      g("q", "Pages from 1. 129 digits printed. How many pages?")),
    b("Pages 1 to 9 have 1 digit each. So the first 9 pages use up 9 digits.", l("g1", "Pages 1 to 9: 9 digits")),
    b("How many digits are left? 129 minus 9 is 120.", w("c1", "129 − 9 = 120")),
    b("From page 10 onwards, how many digits does each page use?",
      ask=c("2", ["1", "3"], "Page 10 and the pages after it are each written with 2 digits.")),
    b("Each page uses 2 digits. So 120 digits make 120 divided by 2, which is 60 pages.", w("c2", "120 ÷ 2 = 60")),
    b("Careful: 60 is only the 2-digit pages. Add back the first 9 pages. 9 plus 60 is 69.", w("c3", "9 + 60 = 69")),
    b("So the book has 69 pages.", a("ans", "69 pages")),
    b("Check: 9 digits, then 60 pages of 2 digits is 120 more. 9 plus 120 is 129. It fits.", w("ck", "9 + 120 = 129")),
]

LESSONS["G4A_COUNTING_025"] = [
    b("How many 2-digit numbers have a tens digit bigger than the ones digit? 72 is one, but 27 is not.",
      g("q", "2-digit numbers with tens digit > ones digit?")),
    b("Go through the tens digits in order. Tens digit 1: the ones digit must be smaller than 1, so only 0. That is the number 10. Just 1 number.",
      l("t1", "Tens 1: 10 → 1 number")),
    b("Tens digit 2: the ones digit can be 0 or 1. How many numbers is that?", l("t2", "Tens 2: 20, 21 → ?"),
      ask=c("2", ["1", "3"], "The ones digit can be 0 or 1, giving the numbers 20 and 21.")),
    b("2 numbers. Do you see the pattern? Tens digit 3 gives 3 numbers, tens digit 4 gives 4, all the way up to tens digit 9, which gives 9.",
      l("t3", "Tens 3: 3 numbers ... Tens 9: 9 numbers")),
    b("So we add 1 plus 2 plus 3, all the way up to 9.", w("c1", "1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 = 45")),
    b("A neat way to add: pair 1 with 9, 2 with 8, 3 with 7, 4 with 6. That is 4 tens, which is 40, and the 5 in the middle makes 45.",
      w("c2", "40 + 5 = 45")),
    b("So there are 45 such numbers.", a("ans", "45 numbers")),
    b("Do not forget the numbers that end in 0, like 10 and 20. Zero is smaller than every tens digit, so they count."),
]

LESSONS["G4A_COUNTING_026"] = [
    b("How many 3-digit numbers have digits that add up to 4?", g("q", "3-digit numbers, digits add up to 4. How many?")),
    b("Let's go through the hundreds digit. It cannot be 0. If it is 1, the other two digits must add up to 3."),
    b("That gives 103, 112, 121 and 130. 4 numbers.", l("h1", "103, 112, 121, 130")),
    b("Hundreds digit 2: the other two digits must add up to 2. How many numbers?",
      ask=c("3", ["2", "4"], "The last two digits can be 0 and 2, or 1 and 1, or 2 and 0. That is 3 ways.")),
    b("They are 202, 211 and 220. 3 numbers.", l("h2", "202, 211, 220")),
    b("Hundreds digit 3 gives 301 and 310. And hundreds digit 4 gives just 400.", l("h3", "301, 310"), l("h4", "400")),
    b("Add the groups. 4 plus 3 plus 2 plus 1 is 10.", w("c1", "4 + 3 + 2 + 1 = 10")),
    b("So there are 10 such numbers.", a("ans", "10 numbers")),
    b("The easy ones to miss are 400 and the others with zeros in them. Going in order catches them all."),
]

LESSONS["G4A_COUNTING_027"] = [
    b("A square board has 9 small squares, in 3 rows of 3. Counting squares of every size, how many are there?",
      g("q", "3 rows of 3 small squares. Squares of every size?"), qf("G4A_COUNTING_027")),
    b("Size by size. The smallest squares first: there are 9 of them.", l("s1", "1 by 1: 9")),
    b("Next, squares that are 2 wide and 2 tall. How many of those fit on the board?",
      ask=c("4", ["2", "1"],
            "A 2 by 2 square can sit in the top left, top right, bottom left or bottom right. They overlap, and that is fine.")),
    b("There are 4: one snug in each corner of the board. They overlap each other, and that is allowed.",
      l("s2", "2 by 2: 4"), qf("G4A_COUNTING_027", 1, "f2")),
    b("And the biggest: the whole board is 1 square, 3 wide and 3 tall.", l("s3", "3 by 3: 1")),
    b("Add all the sizes. 9 plus 4 plus 1 is 14.", w("c1", "9 + 4 + 1 = 14")),
    b("So there are 14 squares on the board.", a("ans", "14 squares")),
    b("The 2 by 2 squares are the ones people miss. Count every size, one at a time."),
]

LESSONS["G4A_COUNTING_028"] = [
    b("4 small squares are joined in a row to make a strip. Counting rectangles of every size, small squares too, how many are there?",
      g("q", "A strip of 4 squares. Rectangles of every size?"), qf("G4A_COUNTING_028")),
    b("A square is a special rectangle, so each small square counts. That is 4.", l("s1", "1 square long: 4")),
    b("Now rectangles made of 2 squares side by side. How many are there?",
      ask=c("3", ["2", "4"], "Number the squares 1, 2, 3, 4. The pairs are 1 and 2, then 2 and 3, then 3 and 4.")),
    b("1 with 2, 2 with 3, 3 with 4. That is 3.", l("s2", "2 squares long: 3")),
    b("Rectangles made of 3 squares: 1 to 3, and 2 to 4. That is 2. And the whole strip is 1 more.",
      l("s3", "3 squares long: 2"), l("s4", "4 squares long: 1")),
    b("Add them. 4 plus 3 plus 2 plus 1 is 10.", w("c1", "4 + 3 + 2 + 1 = 10")),
    b("So there are 10 rectangles in the strip.", a("ans", "10 rectangles")),
    b("Notice the pattern: 4, 3, 2, 1. Each longer size has one fewer place to sit."),
]

LESSONS["G4A_COUNTING_029"] = [
    b("At a party, every child gave one card to every other child. In all, 30 cards were given. How many children were there?",
      g("q", "Each child gives a card to every other. 30 cards.")),
    b("Try a small party first. With 3 children, each one gives 2 cards. 3 times 2 is 6 cards.", w("c0", "3 × 2 = 6")),
    b("So the rule is: the number of children, times one fewer than that. We need two neighbouring numbers that multiply to 30.",
      l("r", "children × (children − 1) = 30")),
    b("Which pair of neighbours multiplies to 30?",
      ask=c("6 × 5", ["5 × 4", "10 × 3"], "Neighbours are numbers next to each other, like 5 and 6. Multiply each neighbouring pair, and look for the one that makes 30.")),
    b("6 times 5 is 30. So there were 6 children, and each one gave 5 cards.", w("c1", "6 × 5 = 30")),
    b("So 6 children were at the party.", a("ans", "6 children")),
    b("Careful: 5 is the number of cards each child gave, not the number of children. The children are one more."),
    b("And we do not halve here, as we do for handshakes. A card from Anu to Binu is different from a card from Binu to Anu."),
]

LESSONS["G4A_COUNTING_030"] = [
    b("Using the digits 0, 1, 2 and 3, with no digit repeated, how many 3-digit even numbers can be made?",
      g("q", "Digits 0, 1, 2, 3, no repeats. 3-digit even numbers?")),
    b("An even number ends in an even digit. Here that means it ends in 0 or in 2. Let's take the two cases one at a time.",
      l("bx", "_ _ [0 or 2]")),
    b("Case 1: it ends in 0. The hundreds digit can be 1, 2 or 3: 3 choices. Then 2 digits are left for the tens place. 3 times 2 is 6.",
      w("c1", "3 × 2 = 6"), n("c1", "6", "ends in 0", "below")),
    b("Case 2: it ends in 2. The digits left are 0, 1 and 3. How many of them can go in the hundreds place?",
      ask=c("2", ["3", "1"], "0 cannot go first, or the number would not have 3 digits. So only 1 or 3 can go there.")),
    b("Only 1 or 3: that is 2 choices. Then 2 digits are left for the tens place, and one of them is the 0. 2 times 2 is 4.",
      w("c2", "2 × 2 = 4"), n("c2", "4", "ends in 2", "below")),
    b("Add the two cases. 6 plus 4 is 10.", w("c3", "6 + 4 = 10")),
    b("So 10 such numbers can be made.", a("ans", "10 numbers")),
    b("When 0 is one of the digits, split into cases. Zero is not allowed at the front, so it changes the count."),
]

LESSONS["G4A_COUNTING_031"] = [
    b("A temple bell takes 6 seconds to ring 4 times, from the first ring to the last. How long does it take to ring 10 times?",
      g("q", "4 rings take 6 seconds. 10 rings take ?")),
    b("The time passes in the gaps between the rings. How many gaps are there between 4 rings?",
      ask=c("3", ["4", "5"], "Tap the table 4 times: ding, ding, ding, ding. There are only 3 waits in between.")),
    b("4 rings have 3 gaps. So 6 seconds are shared among 3 gaps. 6 divided by 3 is 2 seconds for each gap.",
      w("c1", "4 − 1 = 3"), w("c2", "6 ÷ 3 = 2")),
    b("Now 10 rings. In the same way, 10 rings have 9 gaps.", w("c3", "10 − 1 = 9")),
    b("9 gaps of 2 seconds each. 9 times 2 is 18.", w("c4", "9 × 2 = 18")),
    b("So it takes 18 seconds to ring 10 times.", a("ans", "18 seconds")),
    b("The trap is to share the 6 seconds among the 4 rings. The clock only runs in the gaps between them."),
]

LESSONS["G4A_COUNTING_032"] = [
    b("Tara is 9th from the left and Uma is 6th from the right. They swap places, and now Tara is 15th from the left. How many children are in the row?",
      g("q", "Tara: 9th from left. Uma: 6th from right."), l("q2", "After the swap, Tara: 15th from left. How many?")),
    b("After the swap, where is Tara standing?",
      ask=c("in Uma's old spot", ["in her own old spot", "at the end of the row"],
            "They swapped. So Tara has moved into the place where Uma used to stand.")),
    b("Tara is in Uma's old spot. We know two things about that one spot: it is 15th from the left, and it is 6th from the right.",
      l("s", "One spot: 15th from left, 6th from right"), u("q", "6th from right")),
    b("So there are 14 children to its left, and 5 children to its right.", w("c1", "15 − 1 = 14"), w("c2", "6 − 1 = 5")),
    b("Add them all: 14 on the left, the spot itself, and 5 on the right. 14 plus 1 plus 5 is 20.",
      w("c3", "14 + 1 + 5 = 20")),
    b("So there are 20 children in the row.", a("ans", "20 children")),
    b("The 9 was only there to distract us. We never needed it! The shortcut: 15 plus 6, minus 1 for the spot counted twice.",
      w("ck", "15 + 6 − 1 = 20")),
]
