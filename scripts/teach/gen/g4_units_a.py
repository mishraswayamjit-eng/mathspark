"""gr4_units lessons, part A: the real past-paper questions (EXT_G4_FP_..., PYQ_...) and the worksheet one."""
from g4_units_lib import a, b, c, g, l, n, u, w, x

LESSONS = {}

LESSONS["EXT_G4_FP_2020_029"] = [
    b("A gold ring weighs 5 grams and 15 milligrams. We want to write that as one decimal number of grams.",
      g("q", "5 g 15 mg = ? g")),
    b("The 5 grams are already grams, so they stay. Only the 15 milligrams need changing. How many milligrams make 1 gram?",
      u("q", "15 mg"),
      ask=c("1000", ["100", "10"], "Milli means a thousandth. So it takes 1000 milligrams to make 1 gram.")),
    b("1000 milligrams make 1 gram. So to turn milligrams into grams, we divide by 1000.", l("f", "1000 mg = 1 g")),
    b("15 divided by 1000. Dividing by 1000 slides each digit 3 places to the right. So we get 0.015.",
      w("c1", "15 ÷ 1000 = 0.015")),
    b("Careful here: it is 0.015, not 0.15. Thousandths need 3 places after the point, so a 0 has to stand in front of the 15.",
      u("c1", "0.015"), n("c1", "0.015", "not 0.15", "below")),
    b("Now join it to the 5 whole grams. 5 plus 0.015 is 5.015.", w("c2", "5 + 0.015 = 5.015")),
    b("So the ring weighs 5.015 grams.", a("ans", "5.015 g")),
    b("Remember: milligrams to grams means 3 decimal places. Fill any empty place with a 0."),
]


def _m_dm_cm(first):
    return [
        b(first, g("q", "2 m + 2 dm + 15 cm = ? cm")),
        b("Can we just add 2 and 2 and 15? Not yet. What must we do first?",
          ask=c("change them all to cm", ["add 2 + 2 + 15", "write 2, 2, 15 side by side"],
                "Lengths can only be added when they are in the same unit. The choices are in centimetres, so let's change everything into centimetres.")),
        b("Start with the metres. 1 metre is 100 centimetres, so 2 metres is 200 centimetres.",
          u("q", "2 m"), l("f1", "1 m = 100 cm"), w("c1", "2 × 100 = 200")),
        b("Now the decimetres. A decimetre is 10 centimetres, so 2 decimetres is 20 centimetres.",
          u("q", "2 dm"), l("f2", "1 dm = 10 cm"), w("c2", "2 × 10 = 20")),
        b("The 15 centimetres are already centimetres. Now everything matches, so we can add. 200 plus 20 is 220.",
          w("c3", "200 + 20 = 220")),
        b("And 15 more makes 235. So the total is 235 centimetres.", w("c4", "220 + 15 = 235"), a("ans", "235 cm")),
        b("Remember: same units first, then add. Never just push the numbers together."),
    ]


LESSONS["EXT_G4_FP_2021_009"] = _m_dm_cm(
    "We have to add 2 metres, 2 decimetres and 15 centimetres. Three lengths, in three different units.")
LESSONS["PYQ_2017_Q15"] = _m_dm_cm(
    "Here is a sum with a twist. 2 metres, plus 2 decimetres, plus 15 centimetres. Each length has its own unit.")


def _beans(first, given, half_line):
    return [
        b(first, g("q", given)),
        b("One weight is in grams and the other is in kilograms. What do we do first?",
          ask=c("change the kilograms to grams", ["divide straight away", "add the two weights"],
                "We can only compare weights that are in the same unit. Let's change the bag's weight into grams.")),
        b(half_line, l("f", "1 kg = 1000 g"), w("c1", "1000 ÷ 2 = 500")),
        b("Now, 2.5 is an awkward number to divide by. Here is a trick: take 2 beans together. 2.5 plus 2.5 is 5 grams.",
          w("c2", "2.5 + 2.5 = 5"), n("c2", "= 5", "2 beans", "below")),
        b("So every pair of beans weighs 5 grams. How many 5s are there in 500?",
          ask=c("100", ["10", "250"], "5 goes into 5 once. So into 500 it goes 100 times.")),
        b("500 divided by 5 is 100. That is 100 pairs of beans.", w("c3", "500 ÷ 5 = 100")),
        b("Careful: 100 is the number of pairs, not beans. Each pair is 2 beans, so we double it. 200 beans.",
          w("c4", "100 × 2 = 200"), a("ans", "200 beans")),
        b("Check: 200 beans at 2.5 grams each is 500 grams. It fits. Same units first, then count how many fit.",
          w("ck", "200 × 2.5 = 500")),
    ]


LESSONS["EXT_G4_FP_2021_017"] = _beans(
    "Each bean weighs 2.5 grams, and the whole bag of beans weighs 0.5 kilograms. How many beans are inside?",
    "Bean: 2.5 g. Bag: 0.5 kg. How many beans?",
    "1 kilogram is 1000 grams. 0.5 means a half, and half of 1000 is 500. So the bag weighs 500 grams.")
LESSONS["PYQ_2018_Q34"] = _beans(
    "Each bean weighs 2.5 grams, and all the beans in the bag weigh half a kilogram. How many beans are there?",
    "Bean: 2.5 g. Bag: half a kg. How many beans?",
    "1 kilogram is 1000 grams, and half of 1000 is 500. So the beans weigh 500 grams.")

LESSONS["EXT_G4_FP_2022_031"] = [
    b("We have 11 kilograms and 11 grams. We want to write it as one decimal number of kilograms.",
      g("q", "11 kg 11 g = ? kg")),
    b("The 11 kilograms stay as they are. It is the 11 grams we must change. A gram is what part of a kilogram?",
      u("q", "11 g"),
      ask=c("one thousandth", ["one hundredth", "one tenth"],
            "Kilo means a thousand. So 1 gram is one thousandth of a kilogram.")),
    b("1000 grams make 1 kilogram. So we divide the grams by 1000.", l("f", "1000 g = 1 kg"), w("c1", "11 ÷ 1000 = 0.011")),
    b("11 divided by 1000 is 0.011. Thousandths take 3 places after the point, so a 0 stands in front of the 11.",
      u("c1", "0.011")),
    b("Here is the trap. 0.11 kilograms would be 110 grams, far more than our 11 grams.",
      n("c1", "0.011", "0.11 kg = 110 g", "below")),
    b("Now join it to the 11 whole kilograms. 11 plus 0.011 is 11.011.", w("c2", "11 + 0.011 = 11.011")),
    b("So the weight is 11.011 kilograms.", a("ans", "11.011 kg")),
    b("Remember: grams to kilograms means 3 decimal places. Fill the empty place with a 0."),
]

LESSONS["EXT_G4_FP_2022_039"] = [
    b("4 mangoes give 250 millilitres of juice. We want enough juice to make 1 decalitre. How many mangoes is that?",
      g("q", "4 mangoes → 250 ml. ? mangoes → 1 decalitre")),
    b("First, that unusual word. What do you think deca means?",
      ask=c("ten", ["a tenth", "a hundred"],
            "Deca means ten, as in a decade, which is ten years. Deci, with an i, is the one that means a tenth.")),
    b("So 1 decalitre is 10 litres. Each litre is 1000 millilitres, so that is 10000 millilitres.",
      l("f1", "1 decalitre = 10 litres"), l("f2", "1 litre = 1000 ml"), w("c1", "10 × 1000 = 10000")),
    b("Now, how many lots of 250 fit in 10000? Start small: 4 lots of 250 make 1000, which is 1 litre.",
      w("c2", "4 × 250 = 1000")),
    b("We have 10 litres, so that is 10 times 4 lots. 40 lots of 250 millilitres.", w("c3", "10 × 4 = 40")),
    b("Careful now. 40 is the number of lots, and it is one of the choices. But how many mangoes does each lot need?",
      ask=c("4", ["1", "250"], "Go back to the start of the question. It takes 4 mangoes to make each 250 millilitres.")),
    b("Each lot needs 4 mangoes. 40 times 4 is 160. So we need 160 mangoes.",
      w("c4", "40 × 4 = 160"), a("ans", "160 mangoes")),
    b("The plan: change to the same unit, count the lots, then multiply by the mangoes in each lot."),
]

LESSONS["EXT_G4_FP_2023_024"] = [
    b("We must add 100 decigrams and 300 decagrams, and give the answer in grams. Look closely: the two words are nearly the same.",
      g("q", "100 decigrams + 300 decagrams = ? grams"), u("q", "deci"), u("q", "deca")),
    b("Deci, with an i. Is a decigram bigger or smaller than a gram?",
      ask=c("smaller: a tenth of a gram", ["bigger: 10 grams", "the same as a gram"],
            "Deci means a tenth, like a decimal. So a decigram is a small piece: one tenth of a gram.")),
    b("10 decigrams make 1 gram. So 100 decigrams is 100 divided by 10, which is 10 grams.",
      l("f1", "10 decigrams = 1 gram"), w("c1", "100 ÷ 10 = 10")),
    b("Deca, with an a, means ten. So 1 decagram is 10 grams, and 300 decagrams is 300 times 10. That is 3000 grams.",
      l("f2", "1 decagram = 10 grams"), w("c2", "300 × 10 = 3000")),
    b("Now both are in grams, so we can add. 10 plus 3000 is 3010 grams.", w("c3", "10 + 3000 = 3010")),
    b("Look at the choices: 310, 3100, 3000, or none of these. Is 3010 there?",
      l("o", "Choices: 310, 3100, 3000, none of these"),
      ask=c("no, it is not listed", ["yes, it is 3100", "yes, it is 3000"],
            "Read each choice digit by digit. 3010 has its 1 in the tens place. None of the numbers matches it.")),
    b("3010 is not one of the numbers. So the answer is: none of these. Our working is sound, so we can trust it.",
      a("ans", "3010 grams: none of these")),
    b("Remember: deci is a tenth, deca is ten. One little letter changes everything."),
]

LESSONS["EXT_G4_FP_2024_014"] = [
    b("A shopkeeper sells 1 gross of eggs for 864 rupees. We want the cost of 1 score of eggs.",
      g("q", "1 gross of eggs: ₹864. 1 score: ?")),
    b("Gross and score are old names for numbers. A gross is 12 dozen, and a dozen is 12. So a gross is 12 times 12, which is 144.",
      l("f1", "1 gross = 12 dozen"), w("c1", "12 × 12 = 144")),
    b("And how many is a score?",
      ask=c("20", ["12", "10", "100"], "A score is 20. A dozen is the one that is 12.")),
    b("So 144 eggs cost 864 rupees, and we want the price of 20 eggs. First we find the price of 1 egg.",
      l("f2", "1 score = 20"), w("t", "864 ÷ 144 = ?")),
    b("144 times 5 is 720. One more 144 makes 864. So that is 6 lots, and 1 egg costs 6 rupees.",
      w("c2", "144 × 5 = 720"), w("c3", "720 + 144 = 864"), w("c4", "864 ÷ 144 = 6")),
    b("Now 20 eggs. 20 times 6 is 120.", w("c5", "20 × 6 = 120")),
    b("So 1 score of eggs costs 120 rupees.", a("ans", "₹120")),
    b("The plan: turn the number words into numbers, find the price of 1, then multiply."),
]

LESSONS["EXT_G4_FP_2024_040"] = [
    b("We need to change 29 decametres into centimetres. That is a big unit going to a small one.",
      g("q", "29 decametres = ? centimetres")),
    b("Let's go one step at a time. Deca means ten. So 1 decametre is how many metres?",
      ask=c("10 metres", ["100 metres", "a tenth of a metre"], "Deca means ten. So 1 decametre is 10 metres.")),
    b("So 29 decametres is 29 times 10, which is 290 metres.", l("f1", "1 decametre = 10 m"), w("c1", "29 × 10 = 290")),
    b("Careful: 290 is one of the choices, but that is in metres. We are not finished.",
      n("c1", "290", "metres, not cm", "below")),
    b("Each metre is 100 centimetres. So we multiply 290 by 100: two more zeros go on the end.",
      l("f2", "1 m = 100 cm"), w("c2", "290 × 100 = 29000")),
    b("So 29 decametres is 29000 centimetres.", a("ans", "29000 cm")),
    b("Going to a smaller unit, the number gets bigger. Times 10, then times 100, is times 1000 in all.",
      w("ck", "29 × 1000 = 29000")),
]

LESSONS["EXT_G4_FP_2025_023"] = [
    b("1 score of oranges costs 130 rupees, and 1 dozen apples cost 180 rupees. We buy 12 oranges and 17 apples. What is the bill?",
      g("q", "Score of oranges ₹130. Dozen apples ₹180."), l("q2", "Buy 12 oranges and 17 apples. Cost?")),
    b("A dozen is 12. How many is a score?",
      ask=c("20", ["12", "24", "10"], "A score is 20. So 20 oranges cost 130 rupees.")),
    b("20 oranges cost 130 rupees. So 1 orange costs 130 divided by 20, which is 6.5 rupees. 6 and a half.",
      l("f1", "1 score = 20"), w("c1", "130 ÷ 20 = 6.5")),
    b("We buy 12 oranges. 12 times 6 is 72, and 12 halves are 6 more. So the oranges cost 78 rupees.",
      w("c2", "12 × 6 = 72"), w("c3", "12 × 0.5 = 6"), w("c4", "72 + 6 = 78")),
    b("Now the apples. 12 apples cost 180 rupees, so 1 apple costs 180 divided by 12. That is 15 rupees.",
      w("c5", "180 ÷ 12 = 15")),
    b("We buy 17 apples. 17 times 10 is 170, and 17 times 5 is 85. Together, 255 rupees.",
      w("c6", "17 × 15 = 170 + 85"), w("c7", "170 + 85 = 255")),
    b("Add the two costs. 78 plus 255 is 333 rupees.", w("c8", "78 + 255 = 333")),
    b("Now look at the choices: 349.50, 356.50, 330, or None. Is 333 there?",
      l("o", "Choices: ₹349.50, ₹356.50, ₹330, None"),
      ask=c("no, so the answer is None", ["yes, 330 is close enough", "yes, it is 349.50"],
            "Close is not the same as equal. 333 is not on the list, so we pick None.")),
    b("333 rupees is not listed, so the answer is None. When your working is careful, trust it.",
      a("ans", "₹333, so: None")),
    b("The plan: find the price of 1 of each fruit, multiply by how many we buy, then add."),
]

LESSONS["EXT_G4_FP_2025_034"] = [
    b("160 hectograms of rice are shared equally among 25 people. How many grams does each person get?",
      g("q", "160 hectograms ÷ 25 people = ? grams each")),
    b("Hecto is the new word here. What does hecto mean?",
      ask=c("a hundred", ["ten", "a thousand"], "Hecto means a hundred. Deca is ten, and kilo is a thousand.")),
    b("So 1 hectogram is 100 grams. And 160 hectograms is 160 times 100, which is 16000 grams.",
      l("f", "1 hectogram = 100 grams"), w("c1", "160 × 100 = 16000")),
    b("Now share 16000 grams among 25 people. Here is a neat trick: there are 4 lots of 25 in every 100.",
      w("c2", "4 × 25 = 100")),
    b("16000 is 160 hundreds. Each hundred gives 4 lots of 25, so we need 160 times 4. That is 640.",
      w("c3", "160 × 4 = 640"), w("c4", "16000 ÷ 25 = 640")),
    b("Each person gets 640 grams. The choices are 680, 720, 600, or none of these. Which do we pick?",
      l("o", "Choices: 680, 720, 600, none of these"),
      ask=c("none of these", ["600, it is closest", "680"],
            "640 is not on the list, and close does not count. So we choose none of these.")),
    b("640 grams is not listed, so the answer is: none of these.", a("ans", "640 grams: none of these")),
    b("Check: 25 times 640 is 16000. It works. Change the unit first, then share.", w("ck", "25 × 640 = 16000")),
]


def _perimeter(first):
    return [
        b(first, g("q", "Perimeter of a classroom: which unit?")),
        b("The perimeter is the distance all the way round the walls. Imagine walking round the room with your hand on the wall.",
          l("f1", "perimeter = distance all the way round"), u("f1", "distance")),
        b("So what kind of thing is a perimeter?",
          ask=c("a length", ["a weight", "an amount of liquid"],
                "A perimeter tells us how far it is around the room. How far is a length.")),
        b("Now check each unit. Litres measure liquids, like milk. Kilograms measure how heavy something is.",
          l("f2", "litre → liquid"), l("f3", "kilogram → weight"), x("f2", "litre"), x("f3", "kilogram")),
        b("Metres measure length. And a classroom is a few metres long, so the metre is just the right size.",
          l("f4", "metre → length"), u("f4", "length")),
        b("What about 'any of these'? Each unit measures one kind of thing only, so that cannot be right. The answer is the metre.",
          a("ans", "metre")),
        b("Before you measure anything, ask yourself: is it a length, a weight, or a liquid? Then choose the unit."),
    ]


LESSONS["EXT_G4_WS2_CH12_001"] = _perimeter("We want to measure the perimeter of a classroom. Which unit is suitable?")
LESSONS["Q_CH12_001"] = _perimeter("Someone wants to measure the perimeter of a classroom. Which of these units should they use?")

LESSONS["PYQ_2016_Q38"] = [
    b("Which of the choices is the same as 11.11 kilograms? Let's turn 11.11 kilograms into kilograms and grams, then compare.",
      g("q", "11.11 kg = ? kg ? g")),
    b("Split the number at the decimal point. 11 whole kilograms, and 0.11 of a kilogram.",
      w("c1", "11.11 = 11 + 0.11"), u("c1", "0.11")),
    b("The 11 kilograms are easy. But what is 0.11 kilograms in grams? Remember, 1 kilogram is 1000 grams.",
      l("f", "1 kg = 1000 g"),
      ask=c("110 g", ["11 g", "1100 g"],
            "Multiply 0.11 by 1000. The digits slide 3 places to the left, so 0.11 becomes 110.")),
    b("0.11 times 1000 is 110. So 0.11 kilograms is 110 grams.", w("c2", "0.11 × 1000 = 110")),
    b("Here is the trap. 11 kilograms 11 grams looks just like 11.11. But 11 grams is only 0.011 kilograms.",
      l("t", "11 g = 0.011 kg")),
    b("So 11.11 kilograms is 11 kilograms 110 grams.", a("ans", "11.11 kg = 11 kg 110 g", ring="11 kg 110 g")),
    b("The method: split at the decimal point, keep the whole kilograms, and change only the decimal part into grams."),
]

LESSONS["PYQ_2017_Q04"] = [
    b("500 sheets of paper make a pile 5 centimetres thick. Mr. Deepak's big stack is 1 metre 22.5 centimetres thick. How many sheets are in it?",
      g("q", "500 sheets = 5 cm thick"), l("q2", "Stack: 1 m 22.5 cm. How many sheets?")),
    b("First, let's make the stack's thickness all centimetres. 1 metre is 100 centimetres, so the stack is 100 plus 22.5. That is 122.5 centimetres.",
      l("f", "1 m = 100 cm"), w("c1", "100 + 22.5 = 122.5")),
    b("Now, 500 sheets fill 5 centimetres. So how many sheets fit in just 1 centimetre?",
      ask=c("100", ["2500", "50"], "Share the 500 sheets equally over the 5 centimetres. That is 500 divided by 5.")),
    b("500 divided by 5 is 100. So every centimetre of the stack holds 100 sheets.", w("c2", "500 ÷ 5 = 100")),
    b("The stack is 122.5 centimetres thick, so we need 122.5 times 100. Times 100 slides the digits 2 places to the left.",
      w("c3", "122.5 × 100 = 12250")),
    b("So there were 12250 sheets in all.", a("ans", "12250 sheets")),
    b("Does that make sense? 100 centimetres alone would hold 10000 sheets, so a bit more than that is just right.",
      w("ck", "100 × 100 = 10000")),
    b("The plan: find how many fit in 1 centimetre, then multiply by the number of centimetres."),
]


def _kg70(first, last):
    return [
        b(first, g("q", "7 kg 70 g = ? kg")),
        b("The 7 kilograms stay. Only the 70 grams need changing. 1000 grams make 1 kilogram, so we divide 70 by 1000.",
          u("q", "70 g"), l("f", "1000 g = 1 kg")),
        b("What is 70 divided by 1000?", w("t", "70 ÷ 1000 = ?"),
          ask=c("0.07", ["0.7", "0.007"],
                "Dividing by 1000 slides the digits 3 places to the right. The 7 lands in the hundredths place.")),
        b("70 divided by 1000 is 0.07. The 7 sits in the hundredths place.", w("c1", "70 ÷ 1000 = 0.07"), u("c1", "0.07")),
        b("Careful, this is where many people slip. 0.70 kilograms would be 700 grams, ten times too much. And 0.007 would be just 7 grams.",
          l("t1", "0.70 kg = 700 g"), l("t2", "0.007 kg = 7 g")),
        b("Now add the 7 whole kilograms. 7 plus 0.07 is 7.07.", w("c2", "7 + 0.07 = 7.07")),
        b("So 7 kilograms 70 grams is 7.07 kilograms.", a("ans", "7.07 kg")),
        b(last),
    ]


LESSONS["PYQ_2017_Q30"] = _kg70(
    "We have 7 kilograms and 70 grams, and we want one decimal number in kilograms.",
    "Remember: grams to kilograms, divide by 1000, and watch where each digit lands.")
LESSONS["PYQ_2019_Q37"] = _kg70(
    "7 kilograms 70 grams. Let's write that weight as a single decimal number of kilograms.",
    "So the rule is: divide the grams by 1000, then check the place of every digit before you choose.")

LESSONS["PYQ_2018_Q09"] = [
    b("8.05 kilograms is a decimal way of writing some kilograms and some grams. Which ones?",
      g("q", "8.05 kg = ? kg ? g")),
    b("Split it at the point. 8 whole kilograms, and 0.05 of a kilogram.", w("c1", "8.05 = 8 + 0.05"), u("c1", "0.05")),
    b("1 kilogram is 1000 grams. So to turn 0.05 kilograms into grams, we multiply by 1000.", l("f", "1 kg = 1000 g")),
    b("What is 0.05 times 1000?", w("t", "0.05 × 1000 = ?"),
      ask=c("50", ["5", "500"], "Times 1000 slides the digits 3 places to the left. So 0.05 becomes 50.")),
    b("0.05 times 1000 is 50. So 0.05 kilograms is 50 grams.", w("c2", "0.05 × 1000 = 50")),
    b("Watch the 0 after the point. 0.5 kilograms would be 500 grams, but we have 0.05, which is ten times smaller.",
      l("tr", "0.5 kg = 500 g")),
    b("So 8.05 kilograms is 8 kilograms 50 grams.", a("ans", "8.05 kg = 8 kg 50 g", ring="8 kg 50 g")),
    b("The method: split at the point, keep the whole kilograms, and change the decimal part into grams."),
]

LESSONS["PYQ_2018_Q26"] = [
    b("Twelve dozen notebooks are piled up, and each one is 5 millimetres thick. How high is the pile?",
      g("q", "12 dozen notebooks, each 5 mm thick. Height?")),
    b("First, how many notebooks is twelve dozen? A dozen is 12.",
      ask=c("144", ["24", "120"], "Twelve dozen means 12 lots of 12. That is 12 times 12.")),
    b("12 times 12 is 144. So there are 144 notebooks.", l("f1", "1 dozen = 12"), w("c1", "12 × 12 = 144")),
    b("Each is 5 millimetres thick, so we need 144 times 5. A trick: 144 times 10 is 1440, and 5 is half of 10, so halve it. 720 millimetres.",
      w("c2", "144 × 10 = 1440"), w("c3", "1440 ÷ 2 = 720"), w("c3b", "144 × 5 = 720")),
    b("Now look at the choices. 720 millimetres is not there, but one choice is in centimetres. 10 millimetres make 1 centimetre.",
      l("f2", "10 mm = 1 cm")),
    b("720 divided by 10 is 72. So the pile is 72 centimetres high.", w("c4", "720 ÷ 10 = 72"), a("ans", "72 cm")),
    b("So do not rush to 'none of these'. Sometimes the answer is hiding in a different unit."),
]
