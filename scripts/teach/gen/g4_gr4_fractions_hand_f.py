"""Grade 4 fractions, written one by one: Q_CH07_009 to 025 (the hand-written chapter questions)."""
from g4_gr4_fractions_lib import B, CH, FIG, MARK, NOTE, W, bars, bm, lesson, nline

LESSONS = {}


def A(qid, beats, check=None):
    LESSONS[qid] = lesson(beats, "authored", check)


def circles(*items):
    spec = bars(*items)
    spec["shape"] = "circle"
    return spec


def counters(total, groups, shaded=0, item=None):
    spec = {"kind": "set", "total": total, "groups": groups}
    if shaded:
        spec["shadedGroups"] = shaded
    if item:
        spec["item"] = item
    return spec


A("Q_CH07_009", [
    B("3 over 5, times 10. Let's see what that really means.",
      W("l1", "3/5 × 10 = ?", "given")),
    B("3 over 5 times 10 is the same as 3 over 5 of 10. So we are taking a part of 10. Here are 10 counters.",
      FIG("fig", counters(10, 5))),
    B("The bottom number is 5. What does it tell us to do with the 10?",
      ask=CH(["share 10 into 5 equal groups", "multiply 10 by 5", "add 5 to 10"], 0,
             "The bottom number says how many equal groups to make. So we share the 10 into 5 equal groups.")),
    B("10 divided by 5 is 2. Each group holds 2.",
      W("l2", "10 ÷ 5 = 2")),
    B("The top number is 3. So how many do we take?",
      ask=CH(["3 groups of 2, which is 6", "1 group of 2", "all 10"], 0,
             "The top number says how many groups to take. 3 groups, with 2 in each, makes 6.")),
    B("3 times 2 is 6. So 3 over 5 times 10 is 6.",
      W("l3", "3 × 2 = 6"), FIG("fig", counters(10, 5, 3)),
      W("l4", "3/5 × 10 = 6", "answer"), MARK("l4", "6", "circle")),
    B("Does it make sense? 3 over 5 is less than 1 whole, so the answer must be less than 10. And 6 is. Good."),
    B("So for a fraction times a whole number: divide by the bottom, then multiply by the top."),
])

A("Q_CH07_010", [
    B("We need two thirds of 45.",
      W("l1", "2/3 of 45 = ?", "given")),
    B("The bottom number is 3, so we share 45 into 3 equal groups. Here are 45 counters.",
      FIG("fig", counters(45, 3))),
    B("What is 45 divided by 3?",
      ask=CH(["15", "12", "135"], 0,
             "Check by multiplying: 3 times 15 is 45. So each group holds 15.")),
    B("45 divided by 3 is 15. So one third of 45 is 15.",
      W("l2", "45 ÷ 3 = 15")),
    B("Is 15 our answer?",
      ask=CH(["No, we need 2 thirds", "Yes, 15 is the answer"], 0,
             "15 is only one third. The top number is 2, so we need 2 of those groups.")),
    B("The top number is 2, so we take 2 groups. 2 times 15 is 30.",
      W("l3", "2 × 15 = 30"), FIG("fig", counters(45, 3, 2))),
    B("So two thirds of 45 is 30.",
      W("l4", "2/3 of 45 = 30", "answer"), MARK("l4", "30", "circle")),
    B("Check: 3 groups of 15 make 45, and we took 2 of them. Divide by the bottom, multiply by the top."),
])

A("Q_CH07_011", [
    B("Which fraction is equivalent to three quarters? The choices are 6 over 8, 6 over 12, 9 over 16 and 4 over 3.",
      W("l1", "Which is equivalent to 3/4?", "given", True), W("l2", "6/8,  6/12,  9/16,  4/3", label=True)),
    B("Equivalent means equal in value. We make an equal fraction by multiplying the top and the bottom by the same number."),
    B("Let's try doubling. 3 times 2 is 6. The top was doubled, so what must the bottom, 4, become?",
      W("l3", "3 × 2 = 6"),
      ask=CH(["8", "12", "6"], 0,
             "Whatever we do to the top, we do to the bottom. Double 4 is 8.")),
    B("4 times 2 is 8. So three quarters equals 6 over 8.",
      W("l4", "4 × 2 = 8"), W("l5", "3/4 = 6/8"), NOTE("l5", "3/4", "× 2 top and bottom"),
      FIG("fig", bars((4, 3, "3/4"), (8, 6, "6/8")))),
    B("Look at the bars. The same amount is shaded. Each quarter was just cut in two."),
    B("What about 6 over 12? The top was doubled, but the bottom was multiplied by 3. Not the same number, so it is not equal. In fact, it is one half.",
      W("l6", "6/12 = 1/2")),
    B("And 9 over 16: the top was multiplied by 3, the bottom by 4. Not equal either. And 4 over 3 is just three quarters upside down.",
      W("l7", "3/4 ≠ 9/16")),
    B("So the answer is 6 over 8.",
      W("l8", "3/4 = 6/8", "answer"), MARK("l8", "6/8", "circle")),
    B("For equal fractions: multiply the top and the bottom by the very same number."),
])

A("Q_CH07_012", [
    B("We must simplify 18 over 24. That means: the same amount, written with smaller numbers.",
      W("l1", "18/24 = ?", "given")),
    B("To simplify, we divide the top and the bottom by the same number. The best choice is the biggest number that goes into both."),
    B("Which is the biggest number that goes into both 18 and 24?",
      ask=CH(["6", "2", "9"], 0,
             "2 goes into both, but 6 is bigger and also goes into both. 9 goes into 18, but not into 24.")),
    B("6 it is. 18 divided by 6 is 3, and 24 divided by 6 is 4.",
      NOTE("l1", "18/24", "÷ 6 top and bottom"), W("l2", "18 ÷ 6 = 3"), W("l3", "24 ÷ 6 = 4")),
    B("So 18 over 24 is three quarters.",
      W("l4", "18/24 = 3/4", "answer"), MARK("l4", "3/4", "circle"),
      FIG("fig", bars((24, 18, "18/24"), (4, 3, "3/4")))),
    B("Can three quarters be made simpler still?",
      ask=CH(["No, only 1 goes into 3 and 4", "Yes, divide by 2"], 0,
             "2 goes into 4 but not into 3. Nothing bigger than 1 goes into both, so we are done.")),
    B("If you divide by 2 first, you get 9 over 12. That is fine, but not finished. Divide by 3 as well, and you reach three quarters too.",
      W("l5", "18/24 = 9/12"), W("l6", "9/12 = 3/4")),
    B("So: keep dividing the top and bottom by the same number, until only 1 goes into both."),
])

A("Q_CH07_013", [
    B("Riya ate 2 over 5 of a pizza, and 1 over 5 was left over. What fraction did the others eat?",
      W("l1", "Riya ate 2/5.  1/5 is left.  Others ate ?", "given", True)),
    B("The pizza is cut into fifths. So the whole pizza is 5 over 5.",
      W("l2", "Whole pizza = 5/5", label=True), FIG("fig", circles((5, 2, "Riya ate 2/5")))),
    B("The pizza went three ways: Riya's part, the others' part, and the leftover. We know two of them."),
    B("Riya's 2 fifths and the 1 fifth left over. How much is that together?",
      ask=CH(["3/5", "3/10", "1/5"], 0,
             "The pieces are the same size, so just count. 2 fifths and 1 fifth make 3 fifths. The bottom stays 5.")),
    B("2 fifths plus 1 fifth is 3 fifths.",
      W("l3", "2/5 + 1/5 = 3/5")),
    B("The whole pizza is 5 fifths. 3 fifths are Riya's or left over. So how much did the others eat?",
      ask=CH(["2/5", "3/5", "4/5"], 0,
             "5 fifths take away 3 fifths. 5 take away 3 is 2, so it is 2 fifths.")),
    B("5 take away 3 is 2. The others ate 2 over 5 of the pizza.",
      W("l4", "5/5 − 3/5 = 2/5", "answer"), MARK("l4", "2/5", "circle")),
    B("Check: 2 fifths for Riya, 2 fifths for the others, and 1 fifth left. That makes 5 fifths, the whole pizza.",
      W("l5", "2/5 + 2/5 + 1/5 = 5/5")),
])

A("Q_CH07_014", [
    B("Four fractions to put in ascending order. Ascending means going up, like climbing stairs: smallest first.",
      W("l1", "2/3, 3/4, 5/6, 1/2.   Ascending order", "given", True)),
    B("The bottoms are 3, 4, 6 and 2. Which number do all of them go into?",
      ask=CH(["12", "6", "8"], 0,
             "6 is close, but 4 does not go into 6. All four bottoms go into 12.")),
    B("So we change them all into twelfths. Two thirds is 8 over 12. Three quarters is 9 over 12.",
      W("l2", "2/3 = 8/12"), NOTE("l2", "2/3", "× 4 top and bottom"),
      W("l3", "3/4 = 9/12"), NOTE("l3", "3/4", "× 3 top and bottom")),
    B("5 over 6 is 10 over 12. And one half is 6 over 12.",
      W("l4", "5/6 = 10/12"), NOTE("l4", "5/6", "× 2 top and bottom"),
      W("l5", "1/2 = 6/12"), NOTE("l5", "1/2", "× 6 top and bottom"),
      FIG("fig", bars((12, 8, "2/3"), (12, 9, "3/4"), (12, 10, "5/6"), (12, 6, "1/2")))),
    B("The tops are 8, 9, 10 and 6. Which is the smallest?",
      ask=CH(["6", "8", "10"], 0,
             "In counting order they go 6, 8, 9, 10. So 6 comes first.")),
    B("In order, the tops go 6, 8, 9, 10.",
      W("l6", "6/12 < 8/12 < 9/12 < 10/12")),
    B("Now give them back their own names. One half, two thirds, three quarters, then 5 over 6.",
      W("l7", "1/2 < 2/3 < 3/4 < 5/6", "answer"), MARK("l7", "1/2 < 2/3 < 3/4 < 5/6", "circle")),
    B("So to put fractions in order: one bottom for all, order the tops, then swap the names back."),
])

A("Q_CH07_015", [
    B("Two thirds, times 3 over 5.",
      W("l1", "2/3 × 3/5 = ?", "given")),
    B("Times with fractions is the friendly one: no common bottom is needed. We multiply top by top, and bottom by bottom."),
    B("Tops first. What is 2 times 3?",
      ask=CH(["6", "5", "1"], 0,
             "2 times 3 means 2 lots of 3, which is 6. Here we multiply, we do not add.")),
    B("2 times 3 is 6. Now the bottoms: 3 times 5 is 15. So we get 6 over 15.",
      W("l2", "2 × 3 = 6"), W("l3", "3 × 5 = 15"), W("l4", "2/3 × 3/5 = 6/15")),
    B("6 over 15 can be made simpler. Which number goes into both 6 and 15?",
      ask=CH(["3", "2", "5"], 0,
             "2 goes into 6 but not into 15. 5 goes into 15 but not into 6. Only 3 goes into both.")),
    B("6 divided by 3 is 2, and 15 divided by 3 is 5. So 6 over 15 is 2 over 5.",
      W("l5", "6/15 = 2/5"), NOTE("l5", "6/15", "÷ 3 top and bottom")),
    B("So two thirds times 3 over 5 is 2 over 5.",
      W("l6", "2/3 × 3/5 = 2/5", "answer"), MARK("l6", "2/5", "circle")),
    B("It means two thirds of 3 fifths. Picture 3 fifths, and take 2 of those 3 pieces. That is 2 fifths. It fits!",
      FIG("fig", bars((5, 3, "3/5"), (5, 2, "2/3 of 3/5")))),
    B("So for times: top times top, bottom times bottom, then simplify."),
])

A("Q_CH07_016", [
    B("Two mixed numbers to add. 2 and one third, plus 1 and two thirds.",
      W("l1", "2 1/3 + 1 2/3 = ?", "given", True)),
    B("We add the wholes, and we add the fractions. Wholes first: 2 and 1 make 3.",
      W("l2", "2 + 1 = 3")),
    B("Now the fractions: one third plus two thirds. What is that?",
      ask=CH(["3/3", "3/6", "2/3"], 0,
             "Both are thirds, so count the pieces: 1 and 2 make 3. The bottom stays 3.")),
    B("1 third and 2 thirds make 3 thirds.",
      W("l3", "1/3 + 2/3 = 3/3"), FIG("fig", bars((3, 1, "1/3"), (3, 2, "2/3"), (3, 3, "3/3")))),
    B("3 thirds. What is that worth?",
      ask=CH(["1 whole", "3 wholes", "one third"], 0,
             "3 pieces out of 3 fills the whole bar. So 3 thirds is 1 whole.")),
    B("3 thirds is 1 whole. So the fractions gave us 1 extra whole.",
      W("l4", "3/3 = 1")),
    B("3 wholes and 1 more whole make 4. The answer is exactly 4.",
      W("l5", "3 + 1 = 4"), W("l6", "2 1/3 + 1 2/3 = 4", "answer", True), MARK("l6", "4", "circle")),
    B("So with mixed numbers: add the wholes, add the fractions, and if the fractions make a whole, carry it over."),
])

A("Q_CH07_017", [
    B("We need the reciprocal of 5 over 7.",
      W("l1", "The reciprocal of 5/7 = ?", "given", True)),
    B("Reciprocal is a big word for a small idea. It means: flip the fraction. The top goes to the bottom, and the bottom goes to the top."),
    B("In 5 over 7, the top is 5 and the bottom is 7. After the flip, which number is on top?",
      ask=CH(["7", "5", "1"], 0,
             "The flip swaps the two numbers. The 7 was on the bottom, so now it goes on top.")),
    B("7 goes on top and 5 goes below. So the reciprocal is 7 over 5.",
      W("l2", "5/7  →  7/5", label=True), W("l3", "Reciprocal of 5/7 = 7/5", "answer", True), MARK("l3", "7/5", "circle")),
    B("Here is how to check a reciprocal. Multiply the fraction by it. 5 times 7 on top is 35, and 7 times 5 below is 35.",
      W("l4", "5/7 × 7/5 = 35/35")),
    B("What is 35 over 35?",
      ask=CH(["1", "35", "0"], 0,
             "When the top and the bottom are the same, the fraction is 1 whole.")),
    B("35 over 35 is 1. A fraction times its reciprocal is always 1. So 7 over 5 is right.",
      W("l5", "35/35 = 1")),
    B("Watch out: a minus sign does not make a reciprocal. Just flip the fraction: 5 over 7 becomes 7 over 5."),
])

A("Q_CH07_018", [
    B("Which fraction lies between 0 and one half? The choices are three quarters, one quarter, 5 over 6 and 7 over 8.",
      W("l1", "Which fraction is between 0 and 1/2?", "given", True), W("l2", "3/4,  1/4,  5/6,  7/8", label=True)),
    B("Between 0 and one half means less than half. Here is a quick test. Double the top. If it is still smaller than the bottom, the fraction is less than half."),
    B("Three quarters: double 3 is 6, bigger than 4. So it is more than half.",
      W("l3", "3/4 > 1/2"), NOTE("l3", "3/4", "3 × 2 = 6")),
    B("5 over 6: double 5 is 10, bigger than 6. 7 over 8: double 7 is 14, bigger than 8. Both are more than half.",
      W("l4", "5/6 > 1/2"), NOTE("l4", "5/6", "5 × 2 = 10"),
      W("l5", "7/8 > 1/2"), NOTE("l5", "7/8", "7 × 2 = 14")),
    B("Now one quarter. Double 1 is 2. Is 2 smaller than the bottom, 4?",
      ask=CH(["Yes, so 1/4 is less than half", "No, so 1/4 is more than half"], 0,
             "2 is smaller than 4. So one quarter is less than one half.")),
    B("2 is less than 4, so one quarter is less than half. And it is more than 0, because we do have 1 piece.",
      W("l6", "0 < 1/4 < 1/2", "answer"), MARK("l6", "1/4", "circle"),
      FIG("fig", nline(0, 4, 1, [(1, "1/4"), (2, "1/2")], "counting in quarters", "ends"))),
    B("On the number line, one quarter sits between 0 and one half. The other three are all past the half mark."),
    B("So to test against one half: double the top, and compare it with the bottom."),
])

A("Q_CH07_019", [
    B("Which of these is a unit fraction? The choices are 2 over 5, 1 over 7, 3 over 1 and 5 over 5.",
      W("l1", "Which is a unit fraction?", "given", True), W("l2", "2/5,  1/7,  3/1,  5/5", label=True)),
    B("Unit means one. A unit fraction is just one piece of a whole. So its top number is 1."),
    B("Which of these has 1 as its top number?",
      ask=CH(["1/7", "3/1", "5/5"], 0,
             "The top number is the one above the line. In 3 over 1, the 1 is below the line. Only 1 over 7 has 1 on top.")),
    B("1 over 7 has 1 on top. It is one piece, when a whole is cut into 7 equal pieces.",
      MARK("l2", "1/7", "box"), FIG("fig", bars((7, 1, "1/7")))),
    B("Careful with 3 over 1. Its 1 is on the bottom, so it means 3 wholes. That is not a unit fraction."),
    B("And 5 over 5 equals 1 whole, but its top number is 5. It is 5 pieces, not one piece.",
      W("l3", "5/5 = 1")),
    B("So the unit fraction is 1 over 7.",
      W("l4", "Unit fraction: 1/7", "answer", True), MARK("l4", "1/7", "circle")),
    B("Remember: a unit fraction always has 1 on top. One half, one third and one quarter are all unit fractions."),
])

A("Q_CH07_020", [
    B("A tank is three quarters full. Then one third of the tank is used. Using water means we take away.",
      W("l1", "3/4 − 1/3 = ?", "given")),
    B("Here are the two fractions. Quarters and thirds. Can we subtract straight away?",
      FIG("fig", bars((4, 3, "3/4 full"), (3, 1, "1/3 used"))),
      ask=CH(["No, match the pieces first", "Yes, subtract tops and bottoms"], 0,
             "Quarters and thirds are different sizes. We can only take away pieces that are the same size.")),
    B("4 and 3 both go into 12. So we use twelfths.",
      W("l2", "4 × 3 = 12")),
    B("Three quarters: multiply the top and bottom by 3, and we get 9 over 12. One third: multiply by 4, and we get 4 over 12.",
      W("l3", "3/4 = 9/12"), NOTE("l3", "3/4", "× 3 top and bottom"),
      W("l4", "1/3 = 4/12"), NOTE("l4", "1/3", "× 4 top and bottom"),
      FIG("fig", bars((12, 9, "3/4 = 9/12"), (12, 4, "1/3 = 4/12")))),
    B("9 twelfths take away 4 twelfths. What is left?",
      ask=CH(["5/12", "7/12", "1/4"], 0,
             "9 pieces take away 4 pieces leaves 5 pieces. And the pieces are twelfths.")),
    B("9 take away 4 is 5. So 5 over 12 of the tank is left.",
      W("l5", "9/12 − 4/12 = 5/12"), W("l6", "3/4 − 1/3 = 5/12", "answer"), MARK("l6", "5/12", "circle")),
    B("Check by adding back: 5 twelfths plus 4 twelfths is 9 twelfths, our three quarters.",
      W("l7", "5/12 + 4/12 = 9/12")),
    B("So for a take away with different bottoms: same size pieces first, then subtract the tops."),
])

A("Q_CH07_021", [
    B("Which is greater, 5 over 8 or 3 over 5?",
      W("l1", "Which is greater: 5/8 or 3/5?", "given", True)),
    B("Here they are as bars. They look very close! We cannot tell by eye, so we need pieces of the same size.",
      FIG("fig", bars((8, 5, "5/8"), (5, 3, "3/5")))),
    B("Which number do both 8 and 5 go into?",
      ask=CH(["40", "13", "20"], 0,
             "8 times 5 is 40, and 5 times 8 is 40. So both go into 40. And 13 is only 8 plus 5.")),
    B("8 times 5 is 40. So for 5 over 8, we multiply the top by 5 too. 5 times 5 is 25.",
      W("l2", "5/8 = 25/40"), NOTE("l2", "5/8", "× 5 top and bottom")),
    B("5 times 8 is 40. So for 3 over 5, we multiply the top by 8 too. 3 times 8 is 24.",
      W("l3", "3/5 = 24/40"), NOTE("l3", "3/5", "× 8 top and bottom")),
    B("25 over 40, or 24 over 40. Which is greater?",
      ask=CH(["25/40", "24/40", "they are equal"], 0,
             "The pieces are the same size now, so count them. 25 pieces is more than 24 pieces.")),
    B("25 is more than 24, by just one tiny piece. So 5 over 8 is the greater fraction.",
      W("l4", "25/40 > 24/40"), W("l5", "5/8 > 3/5", "answer"), MARK("l5", "5/8", "circle")),
    B("Any two fractions can be compared. Give them the same bottom, then compare the tops."),
])

A("Q_CH07_022", [
    B("We want to write the number 4 as a fraction with 3 on the bottom.",
      W("l1", "4 = ?/3", "given")),
    B("So we want 4 wholes written as thirds. Here are 4 whole bars, each cut into 3 thirds.",
      FIG("fig", bars((3, 3, "1 whole"), (3, 3, "1 whole"), (3, 3, "1 whole"), (3, 3, "1 whole")))),
    B("How many thirds are in 1 whole?",
      ask=CH(["3", "1", "4"], 0,
             "Look at one bar. It is cut into 3 equal pieces, so 1 whole is 3 thirds.")),
    B("1 whole is 3 thirds.",
      W("l2", "1 = 3/3")),
    B("So how many thirds are in 4 wholes?",
      ask=CH(["4 × 3 = 12", "4 + 3 = 7", "just 4"], 0,
             "Each of the 4 wholes has 3 thirds. So we need 4 lots of 3, which is 12.")),
    B("4 times 3 is 12. So 4 is the same as 12 over 3.",
      W("l3", "4 × 3 = 12"), W("l4", "4 = 12/3", "answer"), MARK("l4", "12/3", "circle")),
    B("Check by dividing: 12 divided by 3 is 4. Yes!",
      W("l5", "12 ÷ 3 = 4")),
    B("Careful: 4 over 3 is only 1 whole and 1 third. To write a whole number as a fraction, multiply it by the bottom number."),
])

A("Q_CH07_023", [
    B("8 hours is what fraction of a day?",
      W("l1", "8 hours = what fraction of a day?", "given", True)),
    B("First we need the whole. How many hours are in a day?",
      ask=CH(["24", "12", "60"], 0,
             "A full day, with its day time and its night time, has 24 hours. 12 is only half a day.")),
    B("A day has 24 hours. So 8 hours is 8 out of 24, which we write as 8 over 24.",
      W("l2", "8/24")),
    B("Now we simplify. How many times does 8 go into 24?",
      ask=CH(["3", "4", "2"], 0,
             "Use the 8 times table. 8 times 3 is 24.")),
    B("8 times 3 is 24. So we divide the top and bottom by 8. That gives 1 over 3, which is one third.",
      W("l3", "8 × 3 = 24"), W("l4", "8/24 = 1/3", "answer"), NOTE("l4", "8/24", "÷ 8 top and bottom"),
      MARK("l4", "1/3", "circle"), FIG("fig", bars((24, 8, "8 hours of 24"), (3, 1, "1/3")))),
    B("Does that feel right? 3 lots of 8 hours make a whole day. Like 8 hours of sleep, 8 of school and play, and 8 more."),
    B("So for a fraction of a day: put the hours over 24, then simplify."),
])

A("Q_CH07_024", [
    B("A rope is 20 metres long, and three quarters of it is used. How many metres are used?",
      W("l1", "3/4 of 20 m = ?", "given", True)),
    B("The bottom number is 4, so we cut the 20 metre rope into 4 equal parts.",
      FIG("fig", bm(["?"] * 4, 0, "20 m"))),
    B("How long is each part?",
      ask=CH(["5 m", "4 m", "16 m"], 0,
             "20 metres is shared into 4 equal parts. 20 divided by 4 is 5.")),
    B("20 divided by 4 is 5. So one quarter of the rope is 5 metres.",
      W("l2", "20 ÷ 4 = 5"), FIG("fig", bm(["5 m"] * 4, 0, "20 m"))),
    B("Three quarters are used. How many metres is that?",
      ask=CH(["15 m", "5 m", "12 m"], 0,
             "Three quarters means 3 of the parts. Each part is 5 metres, so we need 3 times 5.")),
    B("3 times 5 is 15. So 15 metres of the rope are used.",
      W("l3", "3 × 5 = 15"), FIG("fig", bm(["5 m"] * 4, 3, "20 m")),
      W("l4", "3/4 of 20 = 15", "answer"), MARK("l4", "15", "circle")),
    B("Check: 15 metres are used, and 1 part, 5 metres, is not. 15 and 5 make 20.",
      W("l5", "15 + 5 = 20")),
    B("Divide by the bottom, multiply by the top. And remember, 5 metres is the part not used."),
])

A("Q_CH07_025", [
    B("A riddle with two clues. Clue 1: my top is 3 less than my bottom. Clue 2: I am equal to 4 over 7. Who am I?",
      W("l1", "top = bottom − 3,   equal to 4/7", "given", True), W("l2", "4/7,  8/11,  12/21,  8/14", label=True)),
    B("Clue 1 first. For each choice, take the top away from the bottom.",
      W("l3", "7 − 4 = 3"), W("l4", "11 − 8 = 3"), W("l5", "21 − 12 = 9"), W("l6", "14 − 8 = 6")),
    B("Which fractions pass clue 1, with a gap of 3?",
      ask=CH(["4/7 and 8/11", "12/21 and 8/14", "all four"], 0,
             "Look at the gaps we wrote: 3, 3, 9 and 6. Only the first two are 3. Those are 4 over 7 and 8 over 11.")),
    B("Only 4 over 7 and 8 over 11 pass. Now clue 2. Double the top and bottom of 4 over 7, and we get 8 over 14, not 8 over 11.",
      W("l7", "4/7 = 8/14"), W("l8", "8/14 ≠ 8/11")),
    B("So which fraction passes both clues?",
      ask=CH(["4/7", "8/11", "8/14"], 0,
             "8 over 11 is not equal to 4 over 7. And 8 over 14 has a gap of 6. Only 4 over 7 fits both clues.")),
    B("4 over 7 is equal to itself, of course! And 7 take away 4 is 3. So the fraction is 4 over 7.",
      W("l9", "The fraction is 4/7", "answer", True), MARK("l9", "4/7", "circle")),
    B("Funny, isn't it? The answer was sitting inside the question. With clues, test every choice against every clue."),
])
