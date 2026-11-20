"""Individually written lessons, Grade 4 operations: past papers 2017-19 and hand-written questions CH09 001-010."""
from g4_gr4_operations_common import (B, W, GIVEN, ANS, ANSR, M, N, S, RING, FIG, choose, lesson, step_figure, figures)

LESSONS = {}

LESSONS["PYQ_2017_Q39"] = lesson(
    B("Four times sums joined by plus and minus. We could work out each one. But first, look closely. Which number keeps coming back?",
      GIVEN("q", "11 × 7 + 13 × 7 − 7 × 6 + 2 × 7"),
      ask=choose(["7", "11", "6"], 0, "Every part has a 7 in it: 11 times 7, 13 times 7, 7 times 6 and 2 times 7.")),
    B("Every part has a 7. So each part is just a number of sevens: 11 sevens, 13 sevens, 6 sevens and 2 sevens.",
      M("q", "7", "underline", 1), M("q", "7", "underline", 2), M("q", "7", "underline", 3), M("q", "7", "underline", 4)),
    B("So we can simply count sevens. But careful: one lot is taken away. Which one?",
      ask=choose(["the 6 sevens", "the 2 sevens", "none of them"], 0,
                 "Look at the sign in front of 7 times 6. It is a minus. So those 6 sevens are taken away.")),
    B("11 plus 13 is 24. Take away 6 to get 18. Add 2 to get 20. So there are 20 sevens altogether.",
      W("c1", "11 + 13 = 24"), W("c2", "24 − 6 = 18"), W("c3", "18 + 2 = 20")),
    B("20 sevens. 2 times 7 is 14, so 20 times 7 is 140.", W("m", "2 × 7 = 14"), *ANSR("ans", "20 × 7 = 140", "140")),
    B("Let us check the long way. The four products are 77, 91, 42 and 14. The 42 is the one that is taken away.",
      W("p", "77 + 91 − 42 + 14")),
    B("77 plus 91 is 168. Take away 42 to get 126. Add 14 to get 140. The same answer.",
      W("p1", "77 + 91 = 168"), W("p2", "168 − 42 = 126"), W("p3", "126 + 14 = 140")),
    B("So when the same number sits in every part, count how many of it you have. And watch for the minus: that part is taken away."),
)

LESSONS["PYQ_2018_Q05"] = lesson(
    B("Three statements, and we check each one by the rules. Maybe one is true. Maybe none is. Let us find out.",
      GIVEN("q", "Which one is correct by the BODMAS rule?", label=True)),
    B("First: 2 times 7 minus 5 equals 4. Which part goes first?",
      W("a", "2 × 7 − 5 = 4 ?"),
      ask=choose(["2 × 7", "7 − 5"], 0, "Times goes before minus. So 2 times 7 comes first.")),
    B("2 times 7 is 14, and 14 take away 5 is 9, not 4. So the first one is not true.",
      W("a1", "2 × 7 − 5 = 14 − 5 = 9"), S("a", "2 × 7 − 5 = 4")),
    B("Second: 5 plus 5 times 25 equals 250. Times first again. 5 times 25 is 125.",
      W("b", "5 + 5 × 25 = 250 ?"), W("b1", "5 × 25 = 125")),
    B("Then 5 plus 125 is 130, not 250. Not true. The 250 comes from adding 5 and 5 first, and that breaks the rule.",
      W("b2", "5 + 125 = 130"), S("b", "5 + 5 × 25 = 250")),
    B("Third: bracket 18 plus 7, divided by 7, equals 19. Bracket first: 18 plus 7 is 25.",
      W("c", "(18 + 7) ÷ 7 = 19 ?"), W("c1", "18 + 7 = 25")),
    B("25 divided by 7 is 3, with 4 left over. That is nowhere near 19. Not true.",
      W("c2", "7 × 3 + 4 = 25"), S("c", "(18 + 7) ÷ 7 = 19")),
    B("All three are crossed off. So the answer is none of these.", ANS("ans", "None of these", label=True), RING("ans", "None of these")),
    B("Each statement hid a trap: it did the jobs in a different order from the rule. Brackets first, then times and divide, then plus and minus."),
)

LESSONS["PYQ_2018_Q07"] = lesson(
    B("Two mystery numbers with three digits each. One ends in 8, the other ends in 7. Which choice could be their product?",
      GIVEN("q", "(★ ★ 8) × (★ ★ 7) = ?", label=True)),
    B("We cannot multiply mystery numbers. But we can be detectives and rule choices out. Here they are.",
      W("opts", "11558    10556    9995006    36846", label=True)),
    B("Clue one: the last digit. The last digit of a product comes only from the last digits of the two numbers. What is 8 times 7?",
      ask=choose(["56", "54", "15"], 0, "8 times 7 is 56. So the product must end in 6.")),
    B("8 times 7 is 56, so the product must end in 6. But 11558 ends in 8. Cross it off.",
      W("c1", "8 × 7 = 56"), S("opts", "11558", "ends in 8")),
    B("The other three all end in 6. So now we need clue two: the size."),
    B("The smallest the two numbers can be is 108 and 107. 108 times 100 is 10800, and 108 times 7 is 756.",
      W("sm", "Smallest: 108 and 107", label=True), W("c2", "108 × 100 = 10800"), W("c3", "108 × 7 = 756")),
    B("Together that is 11556. So the product is at least 11556. But 10556 is smaller than that. Cross it off.",
      W("c4", "108 × 107 = 10800 + 756 = 11556"), S("opts", "10556", "too small")),
    B("Both numbers are less than 1000, and 1000 times 1000 is 1000000. So the product is less than that. 9995006 is far bigger. Cross it off.",
      W("c5", "1000 × 1000 = 1000000"), S("opts", "9995006", "too big")),
    B("Only 36846 is left. It ends in 6 and it is the right size.", ANS("ans", "36846"), RING("ans", "36846")),
    B("The sneaky one was 10556. It ends in 6, but it is just too small. So check the last digit and the size, both."),
)

LESSONS["PYQ_2018_Q17"] = lesson(
    B("A bracket, a divide, a plus and a times. Brackets go first, so we begin inside.",
      GIVEN("q", "(19 + 3 × 2) ÷ 5 + 4 × 3")),
    B("Inside the bracket: 19 plus 3 times 2. Which goes first?",
      M("q", "(19 + 3 × 2)", "box"),
      ask=choose(["3 × 2", "19 + 3"], 0, "Even inside a bracket, times goes before plus. So 3 times 2 comes first.")),
    B("3 times 2 is 6, and 19 plus 6 is 25. The bracket is worth 25.",
      W("a1", "3 × 2 = 6"), W("a2", "19 + 6 = 25"), W("l2", "25 ÷ 5 + 4 × 3")),
    B("Now we have 25 divided by 5, plus 4 times 3. Here is the trap. What happens to the plus?",
      ask=choose(["it waits until the end", "it goes next"], 0,
                 "Divide and times go before plus. So the plus waits until both of them are done.")),
    B("The plus waits. 25 divided by 5 is 5. And 4 times 3 is 12.",
      M("l2", "25 ÷ 5", "box"), M("l2", "4 × 3", "box"), W("b1", "25 ÷ 5 = 5"), W("b2", "4 × 3 = 12")),
    B("Now the plus gets its turn. 5 plus 12 is 17.", *ANSR("ans", "5 + 12 = 17", "17")),
    B("If we had added the 5 and the 4 first, and then multiplied by 3, we would have got a different number. The 4 belongs to the times."),
    B("So: bracket first, with times before plus inside it. Then divide and times. The plus comes last."),
)

LESSONS["PYQ_2018_Q23"] = lesson(
    B("A cinema hall with rows named by letters. To count the people, we first need to know how many rows there are.",
      GIVEN("q", "Rows A to Q, 17 seats each. Rows A to H: 3 empty each.", label=True)),
    B("The rows go from A to Q. Count along the alphabet on your fingers. How many letters is that?",
      ask=choose(["17", "16", "26"], 0, "Q is the 17th letter of the alphabet. So rows A to Q make 17 rows.")),
    B("Q is the 17th letter, so there are 17 rows. And each row has 17 seats.", W("r", "A to Q = 17 rows", label=True)),
    B("17 rows of 17 seats. 17 times 10 is 170, and 17 times 7 is 119. Together, 289 seats.",
      W("s1", "17 × 10 = 170"), W("s2", "17 × 7 = 119"), W("s", "17 × 17 = 170 + 119 = 289")),
    B("Now the empty seats. Rows A to H each have 3 empty, and H is the 8th letter. How many seats are empty?",
      W("h", "A to H = 8 rows", label=True),
      ask=choose(["8 × 3", "17 × 3", "just 3"], 0,
                 "Only rows A to H have empty seats. That is 8 rows, with 3 empty seats in each. So 8 times 3.")),
    B("8 times 3 is 24. So 24 seats are empty.", W("e", "8 × 3 = 24")),
    B("Take the empty seats away from all the seats. 289 take away 24 is 265.", *ANSR("ans", "289 − 24 = 265", "265")),
    B("So 265 people are seated. The trap was in the letters: A to Q is 17 rows, and A to H is 8 rows. Count them carefully."),
)

LESSONS["PYQ_2019_Q02"] = lesson(
    B("This sum should come to 13. One bracket will make it true. Where does it go?",
      GIVEN("q", "48 ÷ 8 − 2 + 5 = 13", label=True)),
    B("First, with no bracket. 48 divided by 8 is 6. Then 6 take away 2 is 4, and 4 plus 5 is 9. Too small.",
      W("n1", "48 ÷ 8 = 6"), W("n2", "6 − 2 + 5 = 9")),
    B("We need a bigger answer. Here is an idea. If we divide 48 by a smaller number, what happens to the answer?",
      ask=choose(["it gets bigger", "it gets smaller"], 0,
                 "Share 48 among fewer people and each one gets more. Dividing by a smaller number gives a bigger answer.")),
    B("So let us make the number after the divide sign smaller. Put the bracket round 8 minus 2.",
      W("t", "48 ÷ (8 − 2) + 5"), M("t", "(8 − 2)", "box")),
    B("Bracket first. 8 take away 2 is 6.", W("t1", "48 ÷ 6 + 5")),
    B("Then the divide. 48 divided by 6 is 8.", W("t2", "8 + 5")),
    B("Then the plus. 8 plus 5 is 13. That is our number!", W("t3", "8 + 5 = 13")),
    B("So the bracket goes round 8 minus 2.", ANS("ans", "48 ÷ (8 − 2) + 5 = 13"), RING("ans", "(8 − 2)")),
    B("A bracket round 48 divided by 8 changes nothing, because the divide goes first anyway. A bracket is only useful when it changes the order."),
)

LESSONS["PYQ_2019_Q20"] = lesson(
    B("Five eights and four different signs! It looks like a riddle, but the BODMAS rule sorts it out.",
      GIVEN("q", "8 + 8 × 8 − 8 ÷ 8")),
    B("Which two jobs go first?",
      ask=choose(["8 × 8 and 8 ÷ 8", "8 + 8", "8 − 8"], 0,
                 "Times and divide go before plus and minus. So 8 times 8, and 8 divided by 8, go first.")),
    B("Box the times and the divide.", M("q", "8 × 8", "box"), M("q", "8 ÷ 8", "box")),
    B("8 times 8 is 64. And 8 divided by 8 is 1.", W("a", "8 × 8 = 64"), W("b", "8 ÷ 8 = 1")),
    B("Write the sum again, with 64 and 1 where the boxes were. The 8 at the front is still there.",
      W("l2", "8 + 64 − 1"), M("l2", "8", "circle")),
    B("Left to right now. 8 plus 64 is 72.", W("l3", "8 + 64 = 72")),
    B("And 72 take away 1 is 71.", *ANSR("ans", "72 − 1 = 71", "71")),
    B("Two traps here. Going straight along from the left gives a different answer. And do not forget that first 8: it still has to be added."),
    B("So: times and divide first, then plus and minus from left to right."),
)

LESSONS["PYQ_2019_Q32"] = lesson(
    B("Two mystery numbers with three digits each. One ends in 7, the other ends in 6. Which choice could be their product?",
      GIVEN("q", "(★ ★ 7) × (★ ★ 6) = ?", label=True)),
    B("We cannot multiply them, but we can rule choices out, like detectives. Here are the four.",
      W("opts", "1342    312312    9933012    51276", label=True)),
    B("Clue one: the last digit. 7 times 6 is 42. So what must the product end in?",
      W("c1", "7 × 6 = 42"),
      ask=choose(["2", "6", "4"], 0, "7 times 6 is 42, and 42 ends in 2. So the product must end in 2.")),
    B("It must end in 2. But 51276 ends in 6, so cross it off.", S("opts", "51276", "ends in 6")),
    B("Clue two: the size. Each number has three digits, so each is at least 100. And 100 times 100 is 10000, which has five digits.",
      W("c2", "100 × 100 = 10000")),
    B("So the product has at least five digits. 1342 has only four. Too small, so cross it off.", S("opts", "1342", "too small")),
    B("Each number is also less than 1000. And 1000 times 1000 is 1000000, which has seven digits. So the product has fewer than seven digits.",
      W("c3", "1000 × 1000 = 1000000")),
    B("9933012 has seven digits. Too big, so cross it off.", S("opts", "9933012", "too big")),
    B("Only 312312 is left. It ends in 2, and it has six digits, which is just right.", ANS("ans", "312312"), RING("ans", "312312")),
    B("The key idea: check the last digit, then count the digits. No long multiplying needed."),
)

LESSONS["PYQ_2019_Q38"] = lesson(
    B("Three and a quarter dozen. That means 3 whole dozens, and then a quarter of a dozen more. We do each part.",
      GIVEN("q", "3 and a quarter dozen = ? articles", label=True)),
    B("One dozen is 12. So 3 dozen is 3 times 12, which is 36.", W("a", "3 × 12 = 36")),
    B("Now a quarter of a dozen. A quarter means one of 4 equal parts. So what is a quarter of 12?",
      ask=choose(["3", "4", "6"], 0, "Split 12 into 4 equal parts. 12 divided by 4 is 3. So a quarter of a dozen is 3.")),
    B("12 divided by 4 is 3. So a quarter of a dozen is 3 articles.", W("b", "12 ÷ 4 = 3")),
    B("Now put the two parts together. 36 plus 3 is 39.", *ANSR("ans", "36 + 3 = 39", "39")),
    B("Careful with the trap. A quarter does not mean add 4. It means divide by 4."),
    B("So: the whole dozens first, then the part of a dozen, then add them."),
)

LESSONS["Q_CH09_001"] = lesson(
    B("Here is our sum: a minus, a times and a plus. The order we do them in changes the answer, so let us get it right.",
      GIVEN("q", "50 − 3 × 8 + 2")),
    B("Which part goes first?",
      ask=choose(["3 × 8", "50 − 3", "8 + 2"], 0,
                 "Times goes before plus and minus, even when it sits in the middle. So 3 times 8 goes first.")),
    B("Times goes first. Box 3 times 8.", M("q", "3 × 8", "box"), N("q", "3 × 8", "first", "below")),
    B("3 times 8 is 24. Write 24 where the box was, and copy the rest.", W("l2", "50 − 24 + 2")),
    B("Now left to right. 50 take away 24. Take away 20 to get 30, then 4 more to get 26.",
      W("a", "50 − 20 = 30"), W("l3", "50 − 24 = 26")),
    B("Are we finished?",
      ask=choose(["Not yet: add the 2", "Yes, it is 26"], 0,
                 "Look back at the sum. There is still a plus 2 at the end, waiting for its turn.")),
    B("26 plus 2 is 28.", *ANSR("ans", "26 + 2 = 28", "28")),
    B("The big trap is doing 50 take away 3 first, because it is on the left. Times always jumps ahead of plus and minus."),
    B("So: times first, then plus and minus from left to right, all the way to the end."),
)

LESSONS["Q_CH09_002"] = lesson(
    B("Here is a sum with a bracket. A bracket is like a little box that says: open me first.",
      GIVEN("q", "(15 + 5) × 3")),
    B("So what do we work out first?",
      ask=choose(["15 + 5", "5 × 3", "15 × 3"], 0, "The bracket goes first. Inside the bracket is 15 plus 5.")),
    B("Bracket first. 15 plus 5 is 20.", M("q", "(15 + 5)", "box"), W("a", "15 + 5 = 20")),
    B("Now the bracket has turned into 20. The sum is 20 times 3.", W("l2", "20 × 3")),
    B("2 times 3 is 6, so 20 times 3 is 60.", *ANSR("ans", "20 × 3 = 60", "60")),
    B("Careful: without the bracket, we would do 5 times 3 first and get a different answer. The bracket tells us to add first."),
    B("So: brackets first, then the rest."),
)

LESSONS["Q_CH09_003"] = lesson(
    B("Here is our sum. It has a divide and a plus in it.", GIVEN("q", "36 ÷ 6 + 14")),
    B("Which job goes first?",
      ask=choose(["36 ÷ 6", "6 + 14"], 0, "Divide goes before plus. So 36 divided by 6 comes first.")),
    B("Divide goes before plus. So box 36 divided by 6.", M("q", "36 ÷ 6", "box")),
    B("36 divided by 6 is 6, because 6 times 6 is 36.", W("a", "6 × 6 = 36"), W("b", "36 ÷ 6 = 6")),
    B("Put that answer where the box was. Now the sum is 6 plus 14.", W("l2", "6 + 14")),
    B("6 plus 14 is 20.", *ANSR("ans", "6 + 14 = 20", "20")),
    B("Notice something funny. The answer to the divide was also a 6. But the first job was still the divide, not the plus."),
    B("So: divide before you add."),
)

LESSONS["Q_CH09_004"] = lesson(
    B("A bracket, a divide and a times. We take them in order.", GIVEN("q", "48 ÷ (4 + 4) × 2")),
    B("Bracket first. 4 plus 4 is 8.", M("q", "(4 + 4)", "box"), W("l2", "48 ÷ 8 × 2")),
    B("Now a divide and a times are left. Which goes first?",
      ask=choose(["48 ÷ 8", "8 × 2"], 0,
                 "Divide and times are equal partners, so we go left to right. The divide is on the left, so it goes first.")),
    B("Divide and times are equal partners, so we go left to right, like reading. 48 divided by 8 is 6.",
      M("l2", "48 ÷ 8", "underline"), W("l3", "6 × 2")),
    B("Then 6 times 2 is 12.", *ANSR("ans", "6 × 2 = 12", "12")),
    B("Two things to watch. Use the whole bracket, 8, not just one of the 4s. And do not stop at 6: the times 2 is still waiting."),
    B("So: brackets first. Then divide and times from left to right."),
)

LESSONS["Q_CH09_005"] = lesson(
    B("Three kinds of bracket, tucked inside each other like nesting dolls. We start with the smallest doll, in the middle.",
      GIVEN("q", "[25 − {10 − (3 + 2)}]")),
    B("Which bracket is in the very middle?",
      ask=choose(["(3 + 2)", "{10 − ...}", "[25 − ...]"], 0, "The round bracket is the innermost one. So we start with 3 plus 2.")),
    B("Round bracket first. 3 plus 2 is 5.", M("q", "(3 + 2)", "box"), W("l2", "[25 − {10 − 5}]")),
    B("Next, the curly bracket. 10 take away 5 is 5.", M("l2", "{10 − 5}", "box"), W("l3", "[25 − 5]")),
    B("Careful here. Only that 5 is taken away from 25. We do not take away the 10, and then the 5 as well."),
    B("Last, the square bracket. 25 take away 5 is 20.", *ANSR("ans", "25 − 5 = 20", "20")),
    B("So with brackets inside brackets, work from the inside out: round, then curly, then square."),
)

LESSONS["Q_CH09_006"] = lesson(
    B("Here is a sum with fractions: one half, plus one third times 6. The order rules work just the same.",
      GIVEN("q", "1/2 + 1/3 × 6")),
    B("Which part goes first?",
      ask=choose(["1/3 × 6", "1/2 + 1/3"], 0, "Times goes before plus, with fractions too. So one third times 6 comes first.")),
    B("Times goes first. One third times 6 means one third of 6. So share 6 into 3 equal groups.",
      M("q", "1/3 × 6", "box"), step_figure("Q_CH09_006", "set", 0)),
    B("6 divided by 3 is 2. So one third of 6 is 2.", W("a", "6 ÷ 3 = 2"), W("b", "1/3 × 6 = 2")),
    B("Now the sum is one half plus 2. That makes 2 and a half.", W("l2", "1/2 + 2")),
    B("The choices are written as decimals. One half is the same as 0.5. So 2 and a half is 2.5.",
      W("h", "1/2 = 0.5"), *ANSR("ans", "1/2 + 2 = 2.5", "2.5")),
    B("The trap is adding the half and the third first. The 6 multiplies only the one third, so that job is done first."),
    B("So the answer is 2.5. Times before plus, even with fractions."),
)

LESSONS["Q_CH09_007"] = lesson(
    B("A minus, a divide and a times. The minus is first in line, but it is not the first job to be done.",
      GIVEN("q", "100 − 50 ÷ 5 × 2")),
    B("Which sign has to wait until the end?",
      ask=choose(["the −", "the ÷", "the ×"], 0, "Divide and times go before minus. So the minus waits until the end.")),
    B("Divide and times go before minus. So box the middle part: 50 divided by 5 times 2.", M("q", "50 ÷ 5 × 2", "box")),
    B("Inside the box there is a divide and a times. Which goes first?",
      ask=choose(["50 ÷ 5", "5 × 2"], 0,
                 "Divide and times are equal partners, so we go left to right. 50 divided by 5 comes first.")),
    B("Left to right. 50 divided by 5 is 10. Then 10 times 2 is 20.", W("a", "50 ÷ 5 = 10"), W("b", "10 × 2 = 20")),
    B("So the box is worth 20. Now the minus gets its turn.", W("l2", "100 − 20")),
    B("100 take away 20 is 80.", *ANSR("ans", "100 − 20 = 80", "80")),
    B("The trap is starting with 100 take away 50, just because it is on the left. And 20 is not the final answer: it still has to be taken from 100."),
    B("So: divide and times first, from left to right. Then the minus."),
)

LESSONS["Q_CH09_008"] = lesson(
    B("The word estimate means we do not need the exact answer. We want a quick, sensible answer, using friendly round numbers.",
      GIVEN("q", "498 × 21 ≈ ?")),
    B("498 is very close to a friendly round number. Which one?",
      ask=choose(["500", "400", "498"], 0, "498 is only 2 away from 500. So we round it to 500.")),
    B("498 is just 2 less than 500. So we use 500.", M("q", "498", "underline"), N("q", "498", "500", "below")),
    B("And 21 is just 1 more than 20. So we use 20.", M("q", "21", "underline"), N("q", "21", "20", "below")),
    B("Now multiply the round numbers. 5 times 2 is 10. Then put the three zeros back: two from 500 and one from 20.",
      W("a", "5 × 2 = 10"), W("b", "500 × 20 = 10,000")),
    B("So our estimate is 10,000.", *ANSR("ans", "498 × 21 ≈ 10,000", "10,000")),
    B("Careful with the trap. Round both numbers, not just one. If only the 498 is rounded, the estimate comes out too high."),
    B("So to estimate, round each number to a friendly one, then multiply."),
)

LESSONS["Q_CH09_009"] = lesson(
    B("Here is a times sum that has been split into two easier pieces. One number is missing, and we must find it.",
      GIVEN("q", "35 × 12 = 35 × 10 + 35 × ?")),
    B("35 times 12 means 12 lots of 35. Someone has split those 12 lots into 10 lots, and some more lots.",
      M("q", "35 × 10", "underline"), FIG("fig", figures()["Q_CH09_009"]["figure"])),
    B("10 lots are already there. How many more lots do we need to make 12 lots?",
      ask=choose(["2", "12", "22"], 0, "12 is 10 and 2 more. The 10 lots are already there, so 2 more lots are needed.")),
    B("12 is 10 and 2. So 12 lots is 10 lots and 2 lots.", W("a", "12 = 10 + 2")),
    B("So the missing number is 2.", ANS("ans", "35 × 12 = 35 × 10 + 35 × 2"), RING("ans", "2", 2)),
    B("We can check. 35 times 10 is 350, and 35 times 2 is 70. 350 plus 70 is 420, which is 35 times 12.",
      W("c1", "35 × 10 = 350"), W("c2", "35 × 2 = 70"), W("c3", "350 + 70 = 420")),
    B("So a big times sum can be split into two small ones. The two pieces must add up to the number you started with. Here, 10 and 2 make 12."),
)

LESSONS["Q_CH09_010"] = lesson(
    B("This one looks big, but there is nothing to work out. It is asking about a rule of multiplying.",
      GIVEN("q", "256 × 18 = 18 × ?")),
    B("Try a small one first. 3 times 4 is 12. And 4 times 3 is 12 as well. The order does not matter.",
      W("a", "3 × 4 = 4 × 3 = 12")),
    B("Picture 3 rows of 4 squares. Turn the page sideways and it is 4 rows of 3 squares. Same squares, same number.",
      FIG("fig", {"kind": "grid", "rows": 3, "cols": 4, "note": "3 rows of 4, or 4 rows of 3"})),
    B("Now look at our sum. The left side is 256 times 18. The right side starts with 18. So which number is missing?",
      ask=choose(["256", "18", "4608"], 0, "The two numbers have simply swapped places. 18 is already there, so the missing one is 256.")),
    B("The two numbers have just swapped places. So the missing number is 256.",
      ANS("ans", "256 × 18 = 18 × 256"), RING("ans", "256", 2)),
    B("Did you notice? We never had to multiply 256 by 18 at all."),
    B("So remember: you can multiply two numbers in either order, and the answer is the same."),
)
