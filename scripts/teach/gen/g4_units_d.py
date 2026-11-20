"""gr4_units lessons, part D: G4A_UNITS_035 to G4A_UNITS_046 (the easy ones)."""
from g4_units_lib import a, b, c, g, l, ring, u, w, x

LESSONS = {}

LESSONS["G4A_UNITS_035"] = [
    b("We need to change 3 metres into centimetres.", g("q", "3 m = ? cm")),
    b("Which is the smaller unit: a metre or a centimetre?",
      ask=c("a centimetre", ["a metre", "they are the same"],
            "A centimetre is about the width of your fingernail. A metre is one big step. So the centimetre is much smaller.")),
    b("Small units mean we need more of them. 1 metre is 100 centimetres. A metre ruler has 100 little centimetres marked on it.",
      l("f", "1 m = 100 cm")),
    b("We have 3 metres, so that is 3 lots of 100. 3 times 100 is 300.", u("q", "3 m"), w("c1", "3 × 100 = 300")),
    b("So 3 metres is 300 centimetres.", a("ans", "300 cm")),
    b("Metres to centimetres: multiply by 100. That means two zeros go on the end."),
]

LESSONS["G4A_UNITS_036"] = [
    b("A bag of rice weighs 5 kilograms. How many grams is that?", g("q", "5 kg = ? g")),
    b("Grams are small. A paper clip weighs about 1 gram! So a bag of rice will be a lot of grams."),
    b("How many grams make 1 kilogram?",
      ask=c("1000", ["100", "10"], "Kilo means a thousand. So 1 kilogram is 1000 grams.")),
    b("1 kilogram is 1000 grams. We have 5 kilograms, so we need 5 lots of 1000.", l("f", "1 kg = 1000 g"), u("q", "5 kg")),
    b("5 times 1000 is 5000.", w("c1", "5 × 1000 = 5000")),
    b("So the bag weighs 5000 grams.", a("ans", "5000 g")),
    b("Kilograms to grams: multiply by 1000. Three zeros go on the end."),
]

LESSONS["G4A_UNITS_037"] = [
    b("A jug holds 2000 millilitres of water. How many litres is that?", g("q", "2000 ml = ? litres")),
    b("A millilitre is tiny, just a few drops. A litre is a big bottle. So we will get far fewer litres than millilitres."),
    b("How many millilitres make 1 litre?",
      ask=c("1000", ["100", "10"], "Milli means a thousandth. So it takes 1000 millilitres to fill 1 litre.")),
    b("1000 millilitres make 1 litre. So we ask: how many 1000s are in 2000?", l("f", "1000 ml = 1 litre")),
    b("1000 and another 1000 make 2000. That is 2 lots.", w("c1", "1000 + 1000 = 2000"), w("c2", "2000 ÷ 1000 = 2")),
    b("So the jug holds 2 litres.", a("ans", "2 litres")),
    b("Millilitres to litres: divide by 1000."),
]

LESSONS["G4A_UNITS_038"] = [
    b("How many eggs are there in 2 dozen?", g("q", "2 dozen = ? eggs")),
    b("Dozen is a special word for a number. Which number?",
      ask=c("12", ["10", "20"], "A dozen is 12. Eggs are often sold in boxes of 12, a dozen eggs.")),
    b("1 dozen is 12. So 2 dozen is 2 lots of 12.", l("f", "1 dozen = 12")),
    b("12 plus 12 is 24. Or, 2 times 12 is 24.", w("c1", "12 + 12 = 24"), w("c2", "2 × 12 = 24")),
    b("So there are 24 eggs in 2 dozen.", a("ans", "24 eggs")),
    b("Remember: a dozen is always 12."),
]

LESSONS["G4A_UNITS_039"] = [
    b("Amma buys half a dozen bananas. How many bananas is that?", g("q", "half a dozen = ? bananas")),
    b("First, how many is a whole dozen?",
      ask=c("12", ["10", "6"], "A dozen is 12. Think of a box of 12 eggs.")),
    b("A dozen is 12. Half means we split it into 2 equal parts and take one part.", l("f", "1 dozen = 12")),
    b("12 divided by 2 is 6, because 6 and 6 make 12.", w("c1", "12 ÷ 2 = 6"), w("c2", "6 + 6 = 12")),
    b("So Amma buys 6 bananas.", a("ans", "6 bananas")),
    b("Half a dozen is 6. You will hear that in shops all the time."),
]

LESSONS["G4A_UNITS_040"] = [
    b("Riya buys 250 grams of sugar and 500 grams of flour. What is the total weight?", g("q", "250 g + 500 g = ?")),
    b("Total means all of it together. So do we add or subtract?",
      ask=c("add", ["subtract"], "Total means putting both together. So we add the two weights.")),
    b("Both weights are in grams, so we can add them straight away.", u("q", "250 g"), u("q", "500 g")),
    b("Add the hundreds first. 200 plus 500 is 700.", w("c1", "200 + 500 = 700")),
    b("Then the 50 that was left over. 700 plus 50 is 750.", w("c2", "700 + 50 = 750")),
    b("So the total weight is 750 grams.", a("ans", "750 g")),
    b("When the units are the same, just add the numbers and keep the unit."),
]

LESSONS["G4A_UNITS_041"] = [
    b("A rope is 8 metres long. Ravi cuts off a piece 3 metres long. How long is the rope that is left?",
      g("q", "8 m − 3 m = ?")),
    b("After the cut, is the rope longer or shorter?",
      ask=c("shorter", ["longer", "the same"],
            "A piece has been cut off and taken away. So the rope that is left must be shorter.")),
    b("Shorter means we take away. We start with 8 and take away 3.", u("q", "− 3 m")),
    b("Count back 3 from 8: 7, 6, 5.", w("c1", "8 − 3 = 5")),
    b("So 5 metres of rope is left.", a("ans", "5 m")),
    b("Check: the 5 metres left and the 3 metres cut off make 8 metres again.", w("ck", "5 + 3 = 8")),
]

LESSONS["G4A_UNITS_042"] = [
    b("Which unit is best for measuring the weight of a watermelon?", g("q", "Weight of a watermelon: which unit?")),
    b("Weight tells us how heavy something is. Which of these measures how heavy?",
      ask=c("kilogram", ["litre", "centimetre"],
            "Litres are for liquids and centimetres are for lengths. Heaviness is measured in grams and kilograms.")),
    b("Let's sort the units. Litre and millilitre measure liquids, like juice.",
      l("f1", "litre, millilitre → liquid"), x("f1", "litre, millilitre")),
    b("Centimetre measures length, like how long your pencil is.", l("f2", "centimetre → length"), x("f2", "centimetre")),
    b("Kilogram measures weight. And a watermelon is heavy, a few kilograms, so it fits well.",
      l("f3", "kilogram → weight"), u("f3", "weight")),
    b("So the best unit is the kilogram.", a("ans", "kilogram")),
    b("Always ask first: am I measuring a length, a weight, or a liquid?"),
]

LESSONS["G4A_UNITS_043"] = [
    b("Which of these lengths is the longest: 1 centimetre, 1 metre, 1 millimetre or 1 kilometre?",
      g("q", "Longest: 1 cm, 1 m, 1 mm or 1 km?")),
    b("Every number is 1, so the numbers cannot help us. We have to think about the units themselves."),
    b("A millimetre is tiny, like the thickness of a coin's edge. A centimetre is about the width of your fingernail.",
      l("o", "mm → cm → m → km"), u("o", "mm"), u("o", "cm")),
    b("A metre is about one big step. What about a kilometre?",
      ask=c("a long walk, 1000 metres", ["shorter than a metre", "about one step"],
            "Kilo means a thousand. A kilometre is a thousand metres: a walk of many minutes.")),
    b("1 kilometre is 1000 metres. That is far longer than all the others.", l("f", "1 km = 1000 m"), ring("o", "km")),
    b("So the longest length is 1 kilometre.", a("ans", "1 km")),
    b("From smallest to biggest: millimetre, centimetre, metre, kilometre. Keep that order in your head."),
]

LESSONS["G4A_UNITS_044"] = [
    b("A shopkeeper has 4 bottles of juice. Each bottle holds 2 litres. How many litres does he have in all?",
      g("q", "4 bottles, 2 litres each. Total?")),
    b("4 bottles, with the same amount in each. Which sum finds the total?",
      ask=c("4 × 2", ["4 + 2", "4 − 2"],
            "There are 4 equal lots of 2 litres. Equal lots mean we multiply: 4 times 2.")),
    b("We can see it by adding the bottles one by one: 2, 4, 6, 8.", w("c1", "2 + 2 + 2 + 2 = 8")),
    b("That is the same as 4 times 2, which is 8.", w("c2", "4 × 2 = 8")),
    b("So he has 8 litres of juice in all.", a("ans", "8 litres")),
    b("Equal groups mean multiply. Just adding 4 and 2 would not count all the bottles."),
]

LESSONS["G4A_UNITS_045"] = [
    b("A pencil is 15 centimetres long and an eraser is 5 centimetres long. They are placed end to end. How long is the line they make?",
      g("q", "15 cm and 5 cm, end to end. Length?")),
    b("End to end means one starts where the other stops. So what do we do with the two lengths?",
      ask=c("add them", ["subtract them", "multiply them"],
            "The line is as long as the pencil, and then the eraser after it. So we put the two lengths together: we add.")),
    b("The line is the pencil's 15 centimetres, and then 5 more for the eraser.", w("t", "15 + 5 = ?")),
    b("5 plus 5 is 10. So 15 plus 5 is 20.", w("c1", "15 + 5 = 20")),
    b("So the line is 20 centimetres long.", a("ans", "20 cm")),
    b("End to end means add. Both lengths were in centimetres, so the answer is in centimetres too."),
]

LESSONS["G4A_UNITS_046"] = [
    b("A fruit seller has 36 bananas. How many dozen is that?", g("q", "36 bananas = ? dozen")),
    b("A dozen is 12. So we are asking: how many 12s make 36?", l("f", "1 dozen = 12")),
    b("Let's count in 12s. 12, then 24, then what?", l("m", "12, 24, ?"),
      ask=c("36", ["34", "48"], "Add 12 to 24. 24 plus 10 is 34, and 2 more makes 36.")),
    b("12, 24, 36. We counted 3 twelves to reach 36.", w("c1", "12 + 12 + 12 = 36"), w("c2", "36 ÷ 12 = 3")),
    b("So 36 bananas make 3 dozen.", a("ans", "3 dozen")),
    b("Check: 3 times 12 is 36. To find how many dozen, divide by 12.", w("ck", "3 × 12 = 36")),
]
