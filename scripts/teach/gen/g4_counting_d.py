"""gr4_counting lessons, part D: G4A_COUNTING_033 to G4A_COUNTING_047."""
from g4_counting_lib import a, b, c, g, l, n, ring, u, w, x

LESSONS = {}

LESSONS["G4A_COUNTING_033"] = [
    b("Aman writes all the numbers from 1 to 100. How many times does he write the digit 1?",
      g("q", "Write 1 to 100. How often is the digit 1 written?")),
    b("Count place by place. Ones place first: 1, 11, 21, 31, and so on up to 91. That is 10 times.",
      l("o", "Ones: 1, 11, 21, 31, 41, 51, 61, 71, 81, 91")),
    b("Now the tens place. Which numbers have a 1 in the tens place?",
      ask=c("10 to 19", ["only 10", "11 only"],
            "Every number in the teens has a 1 in the tens place, and so does 10 itself.")),
    b("10, 11, 12, up to 19. That is 10 numbers, so 10 more 1s.", l("t", "Tens: 10, 11, 12, ... , 19")),
    b("The number 11 has two 1s, and it is in both lists, once for each. So that is right.", u("o", "11"), u("t", "11")),
    b("One more to find: the hundreds place. The number 100 starts with a 1.", l("h", "Hundreds: 100")),
    b("Add them. 10 plus 10 plus 1 is 21.", w("c1", "10 + 10 + 1 = 21")),
    b("So Aman writes the digit 1 a total of 21 times.", a("ans", "21 times")),
    b("Place by place: ones, tens, hundreds. And do not forget the last number, 100."),
]

LESSONS["G4A_COUNTING_034"] = [
    b("How many numbers from 1 to 60 can be divided exactly by 2, or by 3, or by both?",
      g("q", "1 to 60: divisible by 2 or by 3 (or both)?")),
    b("First the multiples of 2. Every second number is one, so 60 divided by 2 is 30 of them.", w("c1", "60 ÷ 2 = 30")),
    b("Next the multiples of 3. Every third number is one, so 60 divided by 3 is 20 of them.", w("c2", "60 ÷ 3 = 20")),
    b("30 plus 20 is 50. But think of the number 6. Which list is it in?", w("c3", "30 + 20 = 50"),
      ask=c("both lists", ["only the 2s", "only the 3s"],
            "6 is 2 times 3. So it is a multiple of 2 and also a multiple of 3. We counted it twice!")),
    b("Numbers like 6, 12 and 18 are in both lists. They are the multiples of 6, and there are 60 divided by 6 of them. That is 10.",
      l("m", "6, 12, 18, ..."), w("c4", "60 ÷ 6 = 10")),
    b("We counted those 10 twice, so take them away once. 50 minus 10 is 40.", w("c5", "50 − 10 = 40")),
    b("So there are 40 such numbers.", a("ans", "40 numbers")),
    b("For 'this or that': count each list, add, then take away what is in both."),
]

LESSONS["G4A_COUNTING_035"] = [
    b("A flag has 3 stripes in a row. Each is red, green or blue. Stripes that touch must be different colours. How many flags can be made?",
      g("q", "3 stripes. Red, green or blue. Neighbours differ.")),
    b("Paint one stripe at a time. The first stripe can be any of the 3 colours.", l("b1", "[3] [ ? ] [ ? ]")),
    b("The second stripe touches the first. So how many colours can it be?",
      ask=c("2", ["3", "1"], "It cannot match the first stripe. That leaves the other 2 colours.")),
    b("2 choices for the second. Now the third stripe. It touches only the second one, not the first.",
      l("b2", "[3] [2] [ ? ]")),
    b("So how many colours can the third stripe be?",
      ask=c("2", ["1", "3"],
            "It only has to differ from the second stripe. It is allowed to match the first, because they do not touch.")),
    b("The third stripe has 2 choices as well. It may even be the same as the first. Multiply: 3 times 2 times 2 is 12.",
      l("b3", "[3] [2] [2]"), w("c1", "3 × 2 × 2 = 12")),
    b("So 12 different flags can be made.", a("ans", "12 flags")),
    b("The trap is 3 times 2 times 1, which is 6. That makes all 3 stripes different, but the rule was only about stripes that touch."),
]

LESSONS["G4A_COUNTING_036"] = [
    b("How many numbers are in this list? 4, 8, 12, 16, 20, 24.", g("q", "4, 8, 12, 16, 20, 24")),
    b("The question asks how many numbers there are. It does not ask how big they are. So we just count them, one by one."),
    b("Point at each number as you count. 4 is the 1st. 8 is the 2nd. 12 is the 3rd.",
      n("q", "4", "1st", "below", 1), n("q", "8", "2nd", "below"), n("q", "12", "3rd", "below")),
    b("16 is the 4th, and 20 is the 5th. What about 24?", n("q", "16", "4th", "below"), n("q", "20", "5th", "below"),
      ask=c("the 6th", ["the 5th", "the 24th"],
            "After the 5th comes the 6th. 24 is the last number, and it is the 6th one we point at.")),
    b("24 is the 6th, and it is the last one.", n("q", "24", "6th", "below")),
    b("So there are 6 numbers in the list.", a("ans", "6 numbers")),
    b("Careful: 24 is the last number, not how many there are. Count the numbers, not their size."),
]

LESSONS["G4A_COUNTING_037"] = [
    b("Ria writes down the whole numbers from 6 to 10: 6, 7, 8, 9, 10. How many numbers does she write?",
      g("q", "6, 7, 8, 9, 10")),
    b("Let's count them one at a time, pointing as we go. 6 is the 1st, 7 is the 2nd, 8 is the 3rd.",
      n("q", "6", "1st", "below"), n("q", "7", "2nd", "below"), n("q", "8", "3rd", "below")),
    b("9 is the 4th. So what is 10?", n("q", "9", "4th", "below"),
      ask=c("the 5th", ["the 4th", "the 10th"],
            "After the 4th comes the 5th. 10 is the last number she writes, and it is the 5th one.")),
    b("10 is the 5th, and the last.", n("q", "10", "5th", "below")),
    b("So Ria writes 5 numbers.", a("ans", "5 numbers")),
    b("Careful: 10 minus 6 is 4, but there are 5 numbers. When both ends are counted, there is always one extra.",
      w("ck", "10 − 6 + 1 = 5")),
]

LESSONS["G4A_COUNTING_038"] = [
    b("How many whole numbers lie between 10 and 15? We must not count 10 or 15.",
      g("q", "Between 10 and 15 (not 10, not 15). How many?")),
    b("Between means after 10 and before 15. Let's write them down: 11, 12, 13, 14.",
      l("m", "10 | 11, 12, 13, 14 | 15"), x("m", "10"), x("m", "15")),
    b("How many numbers did we write?",
      ask=c("4", ["5", "6"], "Count them one by one: 11, 12, 13, 14. The ends, 10 and 15, are left out.")),
    b("11, 12, 13, 14. That is 4 numbers.", u("m", "11, 12, 13, 14")),
    b("So there are 4 whole numbers between 10 and 15.", a("ans", "4 numbers")),
    b("A quick check: 15 minus 10 is 5, and we take away 1 because neither end counts. That gives 4.",
      w("ck", "15 − 10 − 1 = 4")),
]

LESSONS["G4A_COUNTING_039"] = [
    b("Anu and Bala stand in a line, one behind the other. In how many different orders can they stand?",
      g("q", "Anu and Bala in a line. How many orders?")),
    b("Let's try it. Anu can stand in front, with Bala behind.", l("o1", "Anu, Bala")),
    b("Is there another way?",
      ask=c("yes, they can swap", ["no, that is the only way"],
            "The two children can change places. Then Bala is in front and Anu is behind.")),
    b("They swap. Now Bala is in front, with Anu behind.", l("o2", "Bala, Anu")),
    b("Are there any more? With 2 children, one is in front and the other is behind. So that is all."),
    b("So they can stand in 2 different orders.", a("ans", "2 orders")),
    b("To count orders, write each one down. Then you can see that you have them all."),
]

LESSONS["G4A_COUNTING_040"] = [
    b("Using the digits 4 and 7 once each, how many different 2-digit numbers can you make?",
      g("q", "Digits 4 and 7, once each. 2-digit numbers?")),
    b("Put 4 in the tens place and 7 in the ones place. That makes 47.", l("m1", "47")),
    b("Now swap the two digits around. Which number do we get?",
      ask=c("74", ["77", "44"], "Put 7 in the tens place and 4 in the ones place. That reads 74.")),
    b("7 first, then 4. That makes 74.", l("m2", "74")),
    b("Could we make 44 or 77? Not here: each digit can be used only once."),
    b("So we can make 2 different numbers.", a("ans", "2 numbers")),
    b("With 2 digits used once each, there are 2 numbers: one, and its swap."),
]

LESSONS["G4A_COUNTING_041"] = [
    b("5 children stand in a queue. From the front they are Asha, Bina, Chetan, Dev and Esha. Who is 3rd?",
      g("q", "Asha, Bina, Chetan, Dev, Esha")),
    b("The question says: starting from the front. So we begin counting at Asha.", u("q", "Asha")),
    b("Asha is 1st. Bina is 2nd.", n("q", "Asha", "1st", "below"), n("q", "Bina", "2nd", "below")),
    b("Who comes next, in 3rd place?",
      ask=c("Chetan", ["Dev", "Bina"], "After Bina, who is 2nd, the next child in the line is Chetan.")),
    b("Chetan is 3rd. After him, Dev is 4th and Esha is 5th.",
      n("q", "Chetan", "3rd", "below"), n("q", "Dev", "4th", "below"), n("q", "Esha", "5th", "below")),
    b("So Chetan is 3rd in the queue.", a("ans", "Chetan")),
    b("For positions, always check which end to start from. Then count along: 1st, 2nd, 3rd."),
]

LESSONS["G4A_COUNTING_042"] = [
    b("Ravi is 4th in a queue. How many children are standing in front of him?",
      g("q", "Ravi is 4th. How many in front of him?")),
    b("Let's draw the queue. 1st, 2nd, 3rd, and then Ravi in 4th place.", l("m", "1st, 2nd, 3rd, Ravi")),
    b("Which places are in front of Ravi?",
      ask=c("1st, 2nd and 3rd", ["1st, 2nd, 3rd and 4th", "2nd and 3rd"],
            "Ravi is the 4th child himself. He cannot be in front of himself! So it is only the 1st, 2nd and 3rd.")),
    b("The 1st, 2nd and 3rd children are in front. Ravi is the 4th, so we do not count him.", u("m", "1st, 2nd, 3rd")),
    b("That is 3 children. 4 minus 1 is 3.", w("c1", "4 − 1 = 3")),
    b("So 3 children are standing in front of Ravi.", a("ans", "3 children")),
    b("The number of people in front is always one less than your position."),
]

LESSONS["G4A_COUNTING_043"] = [
    b("There are 6 children in a queue. Meena is at the very front. How many children are behind her?",
      g("q", "6 in a queue. Meena is first. How many behind?")),
    b("Meena is at the front. So every other child in the queue is behind her.", l("m", "Meena, then all the others")),
    b("There are 6 children altogether. Is Meena one of the 6?",
      ask=c("yes", ["no"], "The 6 children in the queue include Meena. So she must not be counted among those behind her.")),
    b("So take Meena away from the 6. 6 minus 1 is 5.", w("c1", "6 − 1 = 5")),
    b("So 5 children are behind Meena.", a("ans", "5 children")),
    b("Check: Meena and the 5 behind her make 6. It fits.", w("ck", "1 + 5 = 6")),
]

LESSONS["G4A_COUNTING_044"] = [
    b("How many even numbers are in this list? 3, 4, 7, 8, 10, 13.", g("q", "3, 4, 7, 8, 10, 13")),
    b("Even numbers can be shared into 2 equal groups. They end in 0, 2, 4, 6 or 8."),
    b("Check each one. 3 is odd, so cross it out. 4 is even: keep it. 7 is odd.",
      x("q", "3", None, 1), ring("q", "4"), x("q", "7")),
    b("8 is even. Now, what about 10?", ring("q", "8"),
      ask=c("even, it ends in 0", ["odd", "neither"],
            "10 can be shared into 2 groups of 5. A number ending in 0 is always even.")),
    b("10 ends in 0, so it is even. And 13 ends in 3, so it is odd.", ring("q", "10"), x("q", "13")),
    b("The even numbers are 4, 8 and 10. That is 3 numbers.", a("ans", "3 even numbers")),
    b("To spot an even number, look only at its last digit."),
]

LESSONS["G4A_COUNTING_045"] = [
    b("Here are all the orders for Anu, Binu and Charu: A B C, A C B, B A C, B C A, C A B, C B A. In how many is Anu first?",
      g("q", "ABC, ACB, BAC, BCA, CAB, CBA")),
    b("A stands for Anu. So we want the orders that begin with the letter A."),
    b("Look at the first letter of each order. Which ones start with A?",
      ask=c("ABC and ACB", ["ABC only", "ABC, ACB and BAC"],
            "Look only at the first letter. B A C has an A in it, but it starts with B.")),
    b("A B C starts with A. So does A C B.", ring("q", "ABC"), ring("q", "ACB")),
    b("The other 4 start with B or C, so Anu is not first in those.",
      x("q", "BAC"), x("q", "BCA"), x("q", "CAB"), x("q", "CBA")),
    b("So Anu is first in 2 of the orders.", a("ans", "2 orders")),
    b("When a list is given, read exactly what to look for, then check each item."),
]

LESSONS["G4A_COUNTING_046"] = [
    b("Count the days from Monday to Thursday, counting both Monday and Thursday. How many days is that?",
      g("q", "Monday to Thursday, counting both. How many days?")),
    b("Let's write the days in order: Monday, Tuesday, Wednesday, Thursday.", l("m", "Monday, Tuesday, Wednesday, Thursday")),
    b("The question says to count both Monday and Thursday. So where do we start counting?",
      ask=c("at Monday", ["at Tuesday", "at Wednesday"], "Both ends count. So Monday itself is day number 1.")),
    b("Monday is 1, Tuesday is 2, Wednesday is 3, Thursday is 4.",
      n("m", "Monday", "1", "below"), n("m", "Tuesday", "2", "below"), n("m", "Wednesday", "3", "below"),
      n("m", "Thursday", "4", "below")),
    b("So that is 4 days.", a("ans", "4 days")),
    b("When both ends are counted, write the list and count every item, the first and the last too."),
]

LESSONS["G4A_COUNTING_047"] = [
    b("7 chairs stand in a row, numbered 1 to 7. Which chair is exactly in the middle?", g("q", "1  2  3  4  5  6  7")),
    b("The middle chair has the same number of chairs on each side of it."),
    b("Here is a way to find it. Cross off one chair from each end at the same time. First 1 and 7.",
      x("q", "1"), x("q", "7")),
    b("Then 2 and 6. Then 3 and 5.", x("q", "2"), x("q", "6"), x("q", "3"), x("q", "5")),
    b("Which chair is left?",
      ask=c("Chair 4", ["Chair 3", "Chair 5"],
            "We crossed off 1, 2 and 3 from one end, and 7, 6 and 5 from the other. Only one chair is left standing.")),
    b("Chair 4 is left. It has 3 chairs on its left and 3 chairs on its right.", ring("q", "4")),
    b("So the middle chair is Chair 4.", a("ans", "Chair 4")),
    b("To find the middle, cross off from both ends together until one is left."),
]
