"""gr4_counting lessons, part B: G4A_COUNTING_001 to G4A_COUNTING_016."""
from g4_counting_lib import a, b, c, g, l, n, qf, u, w

LESSONS = {}

LESSONS["G4A_COUNTING_001"] = [
    b("How many whole numbers are there from 15 to 42, counting both 15 and 42?",
      g("q", "15, 16, 17, ... , 42. How many numbers?")),
    b("Let's try a tiny case first. From 1 to 3 we have 1, 2, 3. That is 3 numbers. But 3 minus 1 is only 2.",
      w("c0", "3 − 1 = 2")),
    b("So if we only subtract, what do we miss?",
      ask=c("one of the end numbers", ["nothing", "two numbers"],
            "Subtracting counts the jumps between the numbers. There is always one more number than jumps.")),
    b("Subtracting counts the jumps. So first, 42 minus 15 is 27 jumps.", w("c1", "42 − 15 = 27")),
    b("Then add 1, so that the starting number 15 is counted too. 27 plus 1 is 28.", w("c2", "27 + 1 = 28")),
    b("So there are 28 whole numbers from 15 to 42.", a("ans", "28 numbers")),
    b("Counting both ends: subtract, then add 1."),
]

LESSONS["G4A_COUNTING_002"] = [
    b("Meera is in a queue. She is 7th from the front and 5th from the back. How many children are in the queue?",
      g("q", "7th from the front, 5th from the back. How many?"), qf("G4A_COUNTING_002")),
    b("If Meera is 7th from the front, how many children are in front of her?",
      ask=c("6", ["7", "8"], "Meera herself is number 7. So the children in front of her are numbers 1 to 6.")),
    b("6 children are in front. In the same way, she is 5th from the back, so 4 children are behind her.",
      w("c1", "7 − 1 = 6"), w("c2", "5 − 1 = 4")),
    b("Now add everyone up: 6 in front, Meera herself, and 4 behind.", w("c3", "6 + 1 + 4 = 11")),
    b("So there are 11 children in the queue.", a("ans", "11 children")),
    b("The trap is 7 plus 5, which is 12. That counts Meera twice, once from each end. Take 1 away and we get 11 again.",
      w("tr", "7 + 5 = 12"), w("tr2", "12 − 1 = 11")),
    b("So the quick rule is: add the two positions, then take away 1."),
]

LESSONS["G4A_COUNTING_003"] = [
    b("A straight fence is 40 metres long. A post stands every 5 metres, with one at each end. How many posts are there?",
      g("q", "Fence 40 m. A post every 5 m, and at each end.")),
    b("First count the gaps between the posts. Each gap is 5 metres, so 40 divided by 5 is 8 gaps.", w("c1", "40 ÷ 5 = 8")),
    b("8 gaps. So how many posts?", qf("G4A_COUNTING_003", 0),
      ask=c("9", ["8", "7"],
            "Count the marks on the line, starting from 0. Each gap ends with a post, and there is one more post at the very start.")),
    b("The posts stand at 0, 5, 10, and so on up to 40. Count them and you get 9. It is always one more than the gaps.",
      w("c2", "8 + 1 = 9")),
    b("So there are 9 posts.", a("ans", "9 posts")),
    b("Look at your hand: 5 fingers, 4 gaps. In a straight line, the posts are the gaps plus 1."),
]

LESSONS["G4A_COUNTING_004"] = [
    b("How many 2-digit numbers end in the digit 5?", g("q", "2-digit numbers ending in 5: how many?")),
    b("A 2-digit number has a tens digit and a ones digit. The ones digit is fixed: it must be 5.", l("bx", "[ ? ] [ 5 ]")),
    b("So only the tens digit can change. Can the tens digit be 0?",
      ask=c("no", ["yes"], "With 0 in the tens place we would just have the number 5. That has only one digit.")),
    b("The tens digit can be 1, 2, 3, and so on up to 9. That is 9 choices."),
    b("Let's list them to be sure: 15, 25, 35, 45, 55, 65, 75, 85, 95.", l("m", "15, 25, 35, 45, 55, 65, 75, 85, 95")),
    b("Count them: 9 numbers.", a("ans", "9 numbers")),
    b("The trap is saying 10. The number 5 on its own does not count, because it has just one digit."),
]

LESSONS["G4A_COUNTING_005"] = [
    b("Riya has 3 different tops and 2 different skirts. An outfit is one top with one skirt. How many outfits can she make?",
      g("q", "3 tops, 2 skirts. How many outfits?")),
    b("Take the first top. She can wear it with skirt 1 or with skirt 2. That is 2 outfits from just one top.",
      l("t1", "Top 1: 2 outfits")),
    b("The second top can also go with either skirt. And the third top too. So how do we find the total?",
      ask=c("3 × 2", ["3 + 2", "3 × 3"], "Each of the 3 tops makes 2 outfits. 3 lots of 2 means we multiply.")),
    b("3 tops, with 2 outfits each. That is 3 times 2, which is 6.",
      l("t2", "Top 2: 2 outfits"), l("t3", "Top 3: 2 outfits"), w("c1", "3 × 2 = 6")),
    b("So Riya can make 6 different outfits.", a("ans", "6 outfits")),
    b("The trap is adding: 3 plus 2 is 5. But every top pairs with every skirt, so we multiply."),
]

LESSONS["G4A_COUNTING_006"] = [
    b("How many even numbers are there from 1 to 30?", g("q", "Even numbers from 1 to 30: how many?")),
    b("Even numbers are the ones in the 2 times table: 2, 4, 6, 8 and so on.",
      l("m", "1, 2, 3, 4, 5, 6, ... , 29, 30"), u("m", "2", 1), u("m", "4"), u("m", "6")),
    b("Look at the pattern: odd, even, odd, even. What part of all the numbers are even?",
      ask=c("half of them", ["all of them", "a quarter of them"],
            "The numbers take turns: odd, even, odd, even. So every second number is even. That is half.")),
    b("There are 30 numbers from 1 to 30, and half of them are even. 30 divided by 2 is 15.", w("c1", "30 ÷ 2 = 15")),
    b("So there are 15 even numbers.", a("ans", "15 even numbers")),
    b("Check the ends: the last number, 30, is even, so it is counted. And 0 is not in our list."),
    b("From 1 up to an even number, exactly half the numbers are even."),
]

LESSONS["G4A_COUNTING_007"] = [
    b("A carpenter cuts a long plank into 6 pieces, one cut at a time. How many cuts does he make?",
      g("q", "1 plank → 6 pieces. How many cuts?")),
    b("Before any cut, the plank is 1 piece. After 1 cut, there are 2 pieces.", l("t1", "1 cut → 2 pieces")),
    b("After 2 cuts, how many pieces?",
      ask=c("3", ["4", "2"], "Each cut turns one piece into two. So each cut adds just 1 more piece.")),
    b("2 cuts make 3 pieces. 3 cuts make 4 pieces. The pieces are always one more than the cuts.",
      l("t2", "2 cuts → 3 pieces"), l("t3", "3 cuts → 4 pieces")),
    b("So for 6 pieces we need one fewer cut. 6 minus 1 is 5.", w("c1", "6 − 1 = 5")),
    b("The carpenter makes 5 cuts.", a("ans", "5 cuts")),
    b("Try it with a strip of paper. Cuts are always one fewer than pieces."),
]

LESSONS["G4A_COUNTING_008"] = [
    b("How many 2-digit numbers can we make using only the digits 3 and 8? A digit may be used twice.",
      g("q", "Digits 3 and 8, repeats allowed. 2-digit numbers?")),
    b("A 2-digit number has two places: tens and ones. The tens digit can be 3 or 8. That is 2 choices.",
      l("bx", "[3 or 8] [ ? ]")),
    b("The digit may be used again. So how many choices are there for the ones digit?",
      ask=c("2", ["1", "3"], "Repeats are allowed. So the ones digit can also be 3 or 8, whatever the tens digit was.")),
    b("2 choices for the tens, and for each of them 2 choices for the ones. 2 times 2 is 4.", w("c1", "2 × 2 = 4")),
    b("Let's list them: 33, 38, 83 and 88.", l("m", "33, 38, 83, 88")),
    b("So 4 numbers can be made.", a("ans", "4 numbers")),
    b("The trap is to count only 38 and 83. Read carefully: a digit may be used twice, so 33 and 88 count too."),
]

LESSONS["G4A_COUNTING_009"] = [
    b("The pages of a book are numbered 1 to 25. How many digits are printed in all?",
      g("q", "Pages 1 to 25. How many digits printed?")),
    b("Do all the page numbers have the same number of digits?",
      ask=c("no: some have 1, some have 2", ["yes, 1 digit each", "yes, 2 digits each"],
            "Page 7 has one digit, but page 25 has two. So we need two groups.")),
    b("First group: pages 1 to 9. That is 9 pages with 1 digit each, so 9 digits.", l("g1", "Pages 1 to 9: 9 digits")),
    b("Second group: pages 10 to 25. How many pages? 25 minus 10 is 15, plus 1 because we count both ends. 16 pages.",
      w("c0", "25 − 10 = 15"), w("c1", "15 + 1 = 16")),
    b("Careful there: it is 16 pages, not 15. Count on your fingers from 10 to 25 if you are unsure.",
      n("c1", "16", "count both ends", "below")),
    b("Each of those 16 pages has 2 digits. 16 times 2 is 32 digits.", w("c2", "16 × 2 = 32")),
    b("Add the two groups. 9 plus 32 is 41.", w("c3", "9 + 32 = 41")),
    b("So 41 digits are printed.", a("ans", "41 digits")),
    b("Split the pages by how many digits they have, count each group, then add."),
]

LESSONS["G4A_COUNTING_010"] = [
    b("How many 2-digit numbers have digits that add up to 7?", g("q", "2-digit numbers, digits add up to 7. How many?")),
    b("Let's be organised and go through the tens digit. If the tens digit is 1, the ones digit must be 6. That is 16.",
      l("m1", "16")),
    b("Tens digit 2 needs a 5: that is 25. Then come 34, 43, 52 and 61.", l("m2", "25, 34, 43, 52, 61")),
    b("Is that all of them? What if the tens digit is 7?",
      ask=c("70 works: 7 + 0 = 7", ["no, 7 is too big", "then the ones digit is 7"],
            "7 plus 0 is 7. So 70 belongs on our list too. Zero is a digit as well!")),
    b("Yes: 70. But the tens digit cannot be 0, because that would just be the 1-digit number 7.", l("m3", "70")),
    b("Count the list: 16, 25, 34, 43, 52, 61, 70. That is 7 numbers.", a("ans", "7 numbers")),
    b("Go through the tens digit in order, and you will not miss any or count any twice."),
]

LESSONS["G4A_COUNTING_011"] = [
    b("Kiran writes all the numbers from 1 to 40. How many times does she write the digit 3?",
      g("q", "Write 1 to 40. How often is the digit 3 written?")),
    b("A 3 can sit in the ones place or in the tens place. Let's count each place on its own."),
    b("Ones place first: 3, 13, 23 and 33. That is 4 times.", l("o", "Ones place: 3, 13, 23, 33")),
    b("Now the tens place. Which numbers have a 3 in the tens place?",
      ask=c("30 to 39", ["only 30", "3, 13, 23, 33"],
            "The tens digit is 3 for every number in the thirties, from 30 up to 39.")),
    b("30, 31, 32, all the way to 39. That is 10 numbers, so 10 more 3s.", l("t", "Tens place: 30, 31, 32, ... , 39")),
    b("What about 33? It has two 3s. And we counted it in both lists, once for each 3. So that is just right.",
      u("o", "33")),
    b("Add the two counts. 4 plus 10 is 14.", w("c1", "4 + 10 = 14")),
    b("So she writes the digit 3 a total of 14 times.", a("ans", "14 times")),
    b("Count place by place. Then a number like 33 looks after itself."),
]

LESSONS["G4A_COUNTING_012"] = [
    b("30 children stand in a line. Arjun is 12th from the front. What is his position from the back?",
      g("q", "30 in a line. 12th from the front. From the back?"), qf("G4A_COUNTING_012")),
    b("First, how many children are behind Arjun? Take away the first 12 children, which includes Arjun. 30 minus 12 is 18.",
      w("c1", "30 − 12 = 18")),
    b("18 children are behind him. Counting from the back, what is Arjun's position?",
      ask=c("19th", ["18th", "20th"],
            "Count from the back: the 18 children behind him come first. Arjun is the very next one.")),
    b("Those 18 come first, and then Arjun. 18 plus 1 is 19.", w("c2", "18 + 1 = 19")),
    b("So Arjun is 19th from the back.", a("ans", "19th from the back")),
    b("Check: add his two positions and take away 1, since he was counted twice. 12 plus 19 minus 1 is 30. It fits.",
      w("ck", "12 + 19 − 1 = 30")),
    b("Position from the other end: the total, minus the position, plus 1."),
]

LESSONS["G4A_COUNTING_013"] = [
    b("A square garden has sides of 12 metres. Posts go all around it, one at every corner and one every 3 metres. How many posts?",
      g("q", "Square, side 12 m. A post every 3 m all around."), qf("G4A_COUNTING_013")),
    b("The posts go all the way round, so find the distance around. 4 sides of 12 metres make 48 metres.",
      w("c1", "4 × 12 = 48")),
    b("Each gap between posts is 3 metres. 48 divided by 3 is 16 gaps.", w("c2", "48 ÷ 3 = 16")),
    b("On a straight fence we would add 1 to the gaps. But this fence goes round in a loop. So how many posts?",
      ask=c("16, the same as the gaps", ["17, one more than the gaps", "15, one fewer"],
            "Walk round the garden. After the last gap you arrive back at the first post. No extra post is needed.")),
    b("In a loop, the last gap ends at the first post again. So the posts and the gaps are equal: 16."),
    b("So 16 posts are needed.", a("ans", "16 posts")),
    b("Another trap: each side has 5 posts, and 4 times 5 is 20. But that counts every corner post twice. 20 minus 4 is 16 again.",
      w("ck1", "4 × 5 = 20"), w("ck2", "20 − 4 = 16")),
    b("Straight line: gaps plus 1. Closed loop: the same as the gaps."),
]

LESSONS["G4A_COUNTING_014"] = [
    b("Anu, Binu and Charu stand in a row for a photo. In how many different orders can they stand?",
      g("q", "Anu, Binu, Charu in a row. How many orders?")),
    b("Think of 3 empty places. Any of the 3 children can take the first place. That is 3 choices.",
      l("b1", "[3 choices] [ ? ] [ ? ]")),
    b("One child has taken the first place. How many children are left to choose from for the second place?",
      ask=c("2", ["3", "1"], "One child is already standing in the first place. So only 2 are left for the second.")),
    b("2 choices for the second place. Then just 1 child is left for the last place.",
      l("b2", "[3 choices] [2 choices] [1 choice]")),
    b("Multiply the choices. 3 times 2 times 1 is 6.", w("c1", "3 × 2 × 1 = 6")),
    b("Let's check with letters: A B C, A C B, B A C, B C A, C A B, C B A. That is 6.", l("m", "ABC ACB BAC BCA CAB CBA")),
    b("So they can stand in 6 different orders.", a("ans", "6 orders")),
    b("To arrange things in a row: count the choices for each place, getting smaller each time, and multiply."),
]

LESSONS["G4A_COUNTING_015"] = [
    b("A window has 4 small square panes, in 2 rows of 2. Counting squares of every size, how many squares can you see?",
      g("q", "2 rows of 2 panes. Squares of every size?"), qf("G4A_COUNTING_015")),
    b("Start with the small ones. There are 4 small square panes.", l("s1", "small squares: 4")),
    b("Are there any bigger squares hiding?",
      ask=c("yes, the whole window", ["no, only the 4 panes", "yes, 2 panes side by side"],
            "Step back and look at the whole window. It is as wide as it is tall, so it is a square too.")),
    b("The whole window is 1 big square, made of all 4 panes.", l("s2", "big square: 1")),
    b("What about 2 panes side by side? That shape is longer than it is tall. It is a rectangle, not a square, so we do not count it."),
    b("Add them. 4 small and 1 big make 5.", w("c1", "4 + 1 = 5")),
    b("So there are 5 squares in the window.", a("ans", "5 squares")),
    b("When counting shapes, go size by size: small ones first, then bigger ones."),
]

LESSONS["G4A_COUNTING_016"] = [
    b("16 players enter a knockout tournament. In every match the loser goes out. How many matches are played to find the champion?",
      g("q", "16 players, knockout. How many matches?")),
    b("Go round by round. In round 1, the 16 players make 8 matches. 8 winners go on.", w("c1", "16 ÷ 2 = 8")),
    b("The 8 winners play 4 matches. Then 4 players play 2 matches. Then the last 2 play 1 match: the final.",
      l("r", "Rounds: 8, 4, 2, 1 matches")),
    b("Add the rounds. 8 plus 4 plus 2 plus 1 is 15.", w("c2", "8 + 4 + 2 + 1 = 15")),
    b("Here is a clever shortcut. Each match sends exactly 1 player out. How many players must go out to leave 1 champion?",
      ask=c("15", ["16", "8"], "There are 16 players and only 1 champion. Everyone else must lose once. 16 take away 1.")),
    b("15 players must lose, and each match makes exactly 1 loser. So there are 15 matches. Both ways agree!",
      w("c3", "16 − 1 = 15")),
    b("So 15 matches are played.", a("ans", "15 matches")),
    b("In a knockout, the matches are always one fewer than the players."),
]
