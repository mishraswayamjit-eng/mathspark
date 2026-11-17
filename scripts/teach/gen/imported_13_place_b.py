"""Batch 13: place value questions that divide, multiply, move or swap digits."""
from imported_13_lib import ANS, B, FIG, GIVEN, M, N, P, RING, S, W, ask, chart, gi, lesson
from imported_13_place import PLACES, place_ask, pv_line, where

LESSONS = {}


def times_ask(big, small, third):
    return ask("divide: %s ÷ %s" % (big, small), ["subtract: %s − %s" % (big, small), third],
               "How many times asks how many lots of %s fit into %s. Counting how many fit is dividing, not subtracting." % (small, big))


# ── Place value of 7 compared with the face value of 8 ───────────────────────

def ratio8(qid, number, context, eight_note):
    i7, k7, n7 = where(number, 7)
    i8, k8, n8 = where(number, 8)
    return lesson(
        B("%s How many times the face value of the 8 is the place value of the 7?" % context,
          GIVEN("q", gi(number)), M("q", "7", "circle", n7), M("q", "8", "circle", n8), FIG("f", chart(number, i7, i8))),
        place_ask(number, 7, k7, "Two different values are mixed here, so go slowly. First the 7: which place is it in?"),
        B("So the 7 means 7 ten-thousands. 7 times 10,000 is 70,000.",
          N("q", "7", "ten-thousands", nth=n7), W("pv", pv_line(7, k7)), N("pv", "= 70,000", "place value of 7")),
        B(eight_note, W("fv", "Face value of 8 = 8", True)),
        B("Now, how many times 8 is 70,000? Which operation tells us?",
          ask=times_ask("70,000", "8", "multiply: 70,000 × 8")),
        B("Dividing by 8 is the same as halving 3 times. Half of 70,000 is 35,000.",
          W("h1", "70,000 ÷ 2 = 35,000")),
        B("Half of 35,000 is 17,500, and half of 17,500 is 8,750.",
          W("h2", "35,000 ÷ 2 = 17,500"), W("h3", "17,500 ÷ 2 = 8,750")),
        B("So 70,000 divided by 8 is 8,750. The place value of the 7 is 8,750 times the face value of the 8.",
          ANS("a", "70,000 ÷ 8 = 8,750"), RING("a", "8,750")),
        B("Check by multiplying back: 8,750 times 8 is 70,000.",
          W("c", "8,750 × 8 = 70,000")),
        B("So: read which value is wanted for each digit, place or face. And how many times always means divide."),
    )


LESSONS[P + "206b268a-69f9-4bb8-811b-f193929fff14"] = ratio8(
    P + "206b268a", 74086, "An old army had 74,086 soldiers.",
    "Now the 8. Careful: it sits in the tens place, but the question asks only for its face value. Face value is just the digit, 8.")
LESSONS[P + "98fdf2e6-d5a7-477d-8fea-58c99d7758e3"] = ratio8(
    P + "98fdf2e6", 74208, "Riya ordered 74,208 packets of coloured powder.",
    "Now the 8. The question asks for its face value, and face value is just the digit itself, wherever it sits. So that is 8.")


# ── 57,482: place value of the 7 against its own face value ──────────────────

LESSONS[P + "24226af4-0819-4663-bf24-a2fc1232fcec"] = lesson(
    B("Riya's seat number is 57,482. One digit has a face value of 7 and a place value of 7,000. How many times its face value is its place value?",
      GIVEN("q", "57,482"), M("q", "7", "circle"), FIG("f", chart(57482, 1))),
    place_ask(57482, 7, 3, "A face value of 7 means the digit is 7. Let's check its place value for ourselves. Which place is the 7 in?"),
    B("So the 7 means 7 thousands. 7 times 1,000 is 7,000, just as the question says.",
      N("q", "7", "thousands"), W("pv", "7 × 1,000 = 7,000"), N("pv", "= 7,000", "place value")),
    B("Now, how many times 7 is 7,000? Which operation tells us?",
      ask=times_ask("7,000", "7", "multiply: 7,000 × 7")),
    B("7,000 divided by 7. 7 divided by 7 is 1, and the 3 zeros stay, so we get 1,000.",
      ANS("a", "7,000 ÷ 7 = 1,000"), RING("a", "1,000")),
    B("Look at that answer. It is exactly the worth of the thousands place. A place value is always the face value times the worth of its place.",
      M("pv", "1,000", "box")),
    B("Check by multiplying back: 1,000 times 7 is 7,000.",
      W("c", "1,000 × 7 = 7,000")),
    B("So how many times means divide. And a digit in the thousands place is always worth 1,000 times its face value."),
)


# ── 56,482: place value of 5 against place value of 4 ────────────────────────

LESSONS[P + "84e4d085-09e6-4cfb-a036-c9dd3fc658ff"] = lesson(
    B("The firecrackers cost 56,482 rupees. How many times the place value of the 4 is the place value of the 5?",
      GIVEN("q", "56,482"), M("q", "5", "circle"), M("q", "4", "circle"), FIG("f", chart(56482, 0, 2))),
    place_ask(56482, 5, 4, "We need two place values. Start with the 5: which place is it in?"),
    B("So the 5 means 5 ten-thousands. 5 times 10,000 is 50,000.",
      N("q", "5", "ten-thousands"), W("pa", "5 × 10,000 = 50,000"), N("pa", "= 50,000", "place value of 5")),
    B("Now the 4. It sits in the hundreds place, so it means 4 times 100, which is 400.",
      N("q", "4", "hundreds"), W("pb", "4 × 100 = 400"), N("pb", "= 400", "place value of 4")),
    B("How many times 400 is 50,000? Which operation tells us?",
      ask=times_ask("50,000", "400", "divide the digits: 5 ÷ 4")),
    B("Both numbers end in zeros, so make the sum smaller. Cross 2 zeros off each, and we have 500 divided by 4.",
      W("d", "50,000 ÷ 400 = 500 ÷ 4"), S("d", "00", "÷ 100", nth=1), S("d", "00", "÷ 100", nth=2)),
    B("To divide by 4, halve and halve again. Half of 500 is 250, and half of 250 is 125.",
      W("h1", "500 ÷ 2 = 250"), W("h2", "250 ÷ 2 = 125")),
    B("So the place value of the 5 is 125 times the place value of the 4.",
      ANS("a", "50,000 ÷ 400 = 125"), RING("a", "125")),
    B("Check by multiplying back. 125 times 4 is 500, so 125 times 400 is 50,000.",
      W("c", "125 × 400 = 50,000")),
    B("So: turn each digit into its place value, then divide. And crossing off the same number of zeros from both makes a big division small."),
)


# ── 63,242: the same digit in two places ─────────────────────────────────────

LESSONS[P + "9de4023b-4f41-4da1-98f2-8d5387afc092"] = lesson(
    B("Team Lotus has the code 63,242. The digit 2 is there twice, in the hundreds place and in the units place. How many times as big is the place value of the first 2?",
      GIVEN("q", "63,242"), M("q", "2", "circle", 1), M("q", "2", "circle", 2), FIG("f", chart(63242, 2, 4))),
    B("Same digit, different seats. The 2 in the hundreds place means 2 hundreds: 2 times 100 is 200.",
      N("q", "2", "hundreds", nth=1), W("pa", "2 × 100 = 200")),
    B("The 2 at the end is in the units place. 2 times 1 is just 2.",
      N("q", "2", "units", nth=2), W("pb", "2 × 1 = 2")),
    B("How many times 2 is 200? Which operation tells us?",
      ask=times_ask("200", "2", "neither: both are just 2")),
    B("200 divided by 2 is 100. The 2 in the hundreds place is worth 100 times the 2 in the units place.",
      ANS("a", "200 ÷ 2 = 100"), RING("a", "100")),
    B("Here is why. Each step to the left makes a digit 10 times bigger. From units to hundreds is 2 steps, and 10 times 10 is 100.",
      W("w", "10 × 10 = 100")),
    B("Check by multiplying back: 100 times 2 is 200.",
      W("c", "100 × 2 = 200")),
    B("So the same digit can be worth very different amounts. Its seat decides, and how many times means divide."),
)


# ── 90,517: place value of 5 times face value of 9 ───────────────────────────

LESSONS[P + "0c3a73ba-62ba-4fd4-8249-9a65100e4bb7"] = lesson(
    B("Vikram's jersey number is 90,517. He multiplies the place value of the 5 by the face value of the 9. What does he get?",
      GIVEN("q", "90,517"), M("q", "5", "circle"), M("q", "9", "circle"), FIG("f", chart(90517, 0, 2))),
    place_ask(90517, 5, 2, "Two different values are mixed here, so go slowly. First, the place value of the 5. Which place is the 5 in?"),
    B("So the 5 means 5 hundreds. 5 times 100 is 500.",
      N("q", "5", "hundreds"), W("pv", "5 × 100 = 500"), N("pv", "= 500", "place value of 5")),
    B("Now the 9. Read carefully: the question asks for its face value. What is the face value of the 9?",
      ask=ask("9", ["90,000", "9,000"],
              "Face value is just the digit as you see it, wherever it sits. So the face value of the 9 is 9. The 90,000 is its place value, and we are not asked for that.")),
    B("So we multiply 500 by 9. Start with 5 times 9, which is 45.",
      W("fv", "Face value of 9 = 9", True), W("m", "5 × 9 = 45")),
    B("500 is 5 hundreds, so the answer is 45 hundreds. That is 4,500.",
      ANS("a", "500 × 9 = 4,500"), RING("a", "4,500")),
    B("Check by dividing back: 4,500 divided by 9 is 500.",
      W("c", "4,500 ÷ 9 = 500")),
    B("So read each word of the question. Place value is the digit times its place. Face value is just the digit."),
)


# ── 74,283: divide two place values, then multiply by a face value ───────────

LESSONS[P + "2d8f2714-399f-4b72-a474-5a82fa4b1a25"] = lesson(
    B("Meera's code is 74,283. She divides the place value of the 7 by the place value of the 8, and multiplies the result by the face value of the 4. What does she get?",
      GIVEN("q", "74,283"), M("q", "7", "circle"), M("q", "8", "circle"), FIG("f", chart(74283, 0, 3))),
    place_ask(74283, 7, 4, "Three values to find, one at a time. First the 7: which place is it in?"),
    B("So the 7 means 7 ten-thousands. 7 times 10,000 is 70,000.",
      N("q", "7", "ten-thousands"), W("pa", "7 × 10,000 = 70,000")),
    B("Now the 8. It sits in the tens place, so it means 8 times 10, which is 80.",
      N("q", "8", "tens"), W("pb", "8 × 10 = 80")),
    B("Divide the first by the second. Both end in a zero, so cross 1 zero off each: 7,000 divided by 8.",
      W("d", "70,000 ÷ 80 = 7,000 ÷ 8")),
    B("Dividing by 8 is halving 3 times. Half of 7,000 is 3,500, half of that is 1,750, and half of that is 875.",
      W("h1", "7,000 ÷ 2 = 3,500"), W("h2", "3,500 ÷ 2 = 1,750"), W("h3", "1,750 ÷ 2 = 875")),
    B("Last, we multiply 875 by the face value of the 4. What is the face value of the 4?",
      ask=ask("4", ["4,000", "40"],
              "Face value is just the digit itself, so it is 4. The 4,000 is its place value, and the question does not ask for that.")),
    B("875 times 4. Times 4 is doubling twice: 875 doubled is 1,750, and 1,750 doubled is 3,500.",
      ANS("a", "875 × 4 = 3,500"), RING("a", "3,500")),
    B("Check the division by multiplying back: 875 times 80 is 70,000.",
      W("c", "875 × 80 = 70,000")),
    B("So in a long question, find each value on its own first, place or face as asked. Then do the sums in the order the question gives."),
)


# ── 86,472: divide two place values, then add a face value ───────────────────

LESSONS[P + "6e0d7632-233a-4473-b676-adaf27dff724"] = lesson(
    B("Arjun has 86,472 rupees. He divides the place value of the 8 by the place value of the 2, and then adds the face value of the 6. What number does he get?",
      GIVEN("q", "86,472"), M("q", "8", "circle"), M("q", "2", "circle"), FIG("f", chart(86472, 0, 4))),
    place_ask(86472, 8, 4, "Three values to find, one at a time. First the 8: which place is it in?"),
    B("So the 8 means 8 ten-thousands. 8 times 10,000 is 80,000.",
      N("q", "8", "ten-thousands"), W("pa", "8 × 10,000 = 80,000")),
    B("The 2 is the last digit, in the units place. 2 times 1 is 2, so here the place value is the same as the digit.",
      N("q", "2", "units"), W("pb", "2 × 1 = 2")),
    B("Divide the first by the second. 80,000 divided by 2 is half of 80,000, which is 40,000.",
      W("d", "80,000 ÷ 2 = 40,000")),
    B("Now we add the face value of the 6. What is the face value of the 6?",
      ask=ask("6", ["6,000", "60"],
              "Face value is just the digit itself, so it is 6. The 6,000 is its place value, and the question does not ask for that.")),
    B("40,000 plus 6 is 40,006. The 6 goes in the units place, and zeros hold the places in between.",
      ANS("a", "40,000 + 6 = 40,006"), RING("a", "40,006")),
    B("Check by going backwards: 40,006 minus 6 is 40,000, and 40,000 times 2 is 80,000.",
      W("c1", "40,006 − 6 = 40,000"), W("c2", "40,000 × 2 = 80,000")),
    B("So find each value on its own first, place or face as asked. Then do the sums in the order the question gives."),
)


# ── 74,208: the 2 moves to the ten-thousands place ───────────────────────────

LESSONS[P + "474382c8-4700-4027-8e63-da3d237e70e0"] = lesson(
    B("Ravi's code is 74,208. He imagines moving the 2 into the ten-thousands place. What is the difference between its new place value and its original place value?",
      GIVEN("q", "74,208"), M("q", "2", "circle"), FIG("f", chart(74208, 2))),
    place_ask(74208, 2, 2, "First, where is the 2 right now? Which place is it in?"),
    B("So at the moment the 2 means 2 hundreds. 2 times 100 is 200.",
      N("q", "2", "hundreds"), W("old", "2 × 100 = 200"), N("old", "= 200", "original")),
    B("Now picture the 2 in the ten-thousands place, where the 7 is. There it would mean 2 times 10,000, which is 20,000.",
      M("q", "7", "box"), W("new", "2 × 10,000 = 20,000"), N("new", "= 20,000", "new")),
    B("Which sum gives the difference between the new place value and the original one?",
      ask=ask("20,000 − 200", ["20,000 − 2", "20,000 + 200"],
              "Difference means subtract. And we subtract the original place value, which is 200, not the bare digit 2.")),
    B("20,000 minus 200 is 19,800. Take care with the zeros: we are taking away 2 hundreds.",
      ANS("a", "20,000 − 200 = 19,800"), RING("a", "19,800")),
    B("Check by adding back: 19,800 plus 200 is 20,000.",
      W("c", "19,800 + 200 = 20,000")),
    B("The digit stayed a 2 the whole time. Only its seat changed, and the seat decides what a digit is worth."),
)


# ── 72,508: swap the thousands and tens digits ───────────────────────────────

LESSONS[P + "a56730ce-48d8-4d2f-acef-d09c2c668917"] = lesson(
    B("Riya writes 72,508. She swaps the digit in the thousands place with the digit in the tens place. What is the difference between the original number and the new one?",
      GIVEN("q", "72,508"), FIG("f", chart(72508, 1, 3))),
    B("Which two digits change seats?",
      ask=ask("the 2 and the 0", ["the 7 and the 0", "the 2 and the 5"],
              "Count from the right, one digit at a time: 8 is in the ones, 0 in the tens, 5 in the hundreds, and 2 in the thousands. So the 2 and the 0 change seats.")),
    B("Swap them. The 0 goes to the thousands place and the 2 goes to the tens place. Every other digit stays, so the new number is 70,528.",
      M("q", "2", "circle"), M("q", "0", "circle"), W("n", "70,528"), N("n", "70,528", "new number")),
    B("We could subtract the long way. But look closer: only the 2 really moved, because the 0 is worth nothing in any seat.",
      W("s", "72,508 − 70,528 = ?")),
    B("In the thousands place the 2 was worth 2,000. In the tens place it is worth only 20.",
      W("v1", "2 × 1,000 = 2,000"), W("v2", "2 × 10 = 20")),
    B("So the number lost 2,000 and got 20 back. 2,000 minus 20 is 1,980.",
      W("d", "2,000 − 20 = 1,980")),
    B("Careful: the difference is not 2,000. The 2 did not vanish. It still counts for 20 in its new seat.",
      ANS("a", "72,508 − 70,528 = 1,980"), RING("a", "1,980")),
    B("Check by adding back: 70,528 plus 1,980 is 72,508, the number Riya started with.",
      W("c", "70,528 + 1,980 = 72,508")),
    B("So when digits swap seats, ask what each one was worth before and after. The change in worth is the change in the number."),
)


# ── A 7 in the ten-thousands place and a 3 in the hundreds place ─────────────

LESSONS[P + "48dd3746-66b6-4dfc-becd-5cee5cffa096"] = lesson(
    B("Riya's number has 5 digits. It has a 7 in the ten-thousands place and a 3 in the hundreds place, and every other digit is 0. What is the number?",
      GIVEN("q", "7 in ten-thousands, 3 in hundreds, rest 0", True)),
    B("The clue says the number is the sum of the two place values. So first, the 7 in the ten-thousands place: 7 times 10,000 is 70,000.",
      W("pa", "7 × 10,000 = 70,000")),
    B("Now the 3 in the hundreds place. What is it worth?",
      ask=ask("300", ["30", "3,000"],
              "The hundreds place is the third seat from the right. A 3 sitting there means 3 hundreds, and that is 300.")),
    B("3 times 100 is 300.", W("pb", "3 × 100 = 300")),
    B("Add the two place values. 70,000 plus 300 is 70,300.",
      ANS("a", "70,000 + 300 = 70,300"), RING("a", "70,300")),
    B("See it in the chart: 7, 0, 3, 0, 0. The zeros hold the empty seats, so the 3 stays in the hundreds place.",
      FIG("f", chart(70300, 0, 2))),
    B("Careful with the other choices. They all use the same digits, but they put the 3 in the tens, the thousands or the ones place."),
    B("So a number is the sum of the place values of its digits. And zeros matter: they keep every digit in its proper seat."),
)
