"""gr4_units lessons, part E: the hand-written questions (Q_CH11_..., Q_CH12_...)."""
from g4_units_lib import a, b, c, g, l, n, u, w, x

LESSONS = {}

LESSONS["Q_CH11_018"] = [
    b("A ribbon is 6.9 metres long. How many pieces of 3 centimetres can be cut from it?",
      g("q", "6.9 m ribbon. Pieces of 3 cm. How many?")),
    b("Can we just divide 6.9 by 3?",
      ask=c("no, make the units the same first", ["yes, the answer is 2.3", "no, multiply them instead"],
            "The ribbon is in metres but the pieces are in centimetres. We must change the ribbon into centimetres first.")),
    b("1 metre is 100 centimetres. So 6.9 metres is 6.9 times 100, which is 690 centimetres.",
      l("f", "1 m = 100 cm"), w("c1", "6.9 × 100 = 690")),
    b("Careful: 690, not 69. Times 100 moves the digits 2 places.", n("c1", "690", "not 69", "below")),
    b("Now, how many 3s are in 690? 69 divided by 3 is 23, so 690 divided by 3 is 230.",
      w("c2", "69 ÷ 3 = 23"), w("c3", "690 ÷ 3 = 230")),
    b("So 230 pieces can be cut.", a("ans", "230 pieces")),
    b("Check: 230 pieces of 3 centimetres make 690 centimetres. Same units first, then divide.", w("ck", "230 × 3 = 690")),
]

LESSONS["Q_CH11_019"] = [
    b("One bottle holds 125 millilitres of oil. How many bottles do we need for 2.5 litres?",
      g("q", "Bottle: 125 ml. Oil: 2.5 litres. How many bottles?")),
    b("First, the same unit. 1 litre is 1000 millilitres, so 2.5 litres is 2500 millilitres.",
      l("f", "1 litre = 1000 ml"), w("c1", "2.5 × 1000 = 2500")),
    b("Think about 1 litre first. 2 bottles hold 250 millilitres. So how many bottles fill 1000?",
      w("c2", "125 × 2 = 250"),
      ask=c("8", ["4", "10"], "4 lots of 250 make 1000. Each 250 is 2 bottles, so that is 8 bottles.")),
    b("8 bottles fill 1 litre.", w("c3", "125 × 8 = 1000")),
    b("We have 2 and a half litres. 2 litres need 16 bottles, and the half litre needs 4 more.",
      w("c4", "8 × 2 = 16"), w("c5", "8 ÷ 2 = 4")),
    b("16 plus 4 is 20. So 20 bottles are needed.", w("c6", "16 + 4 = 20"), a("ans", "20 bottles")),
    b("Check: 20 bottles of 125 millilitres make 2500 millilitres. It fits.", w("ck", "20 × 125 = 2500")),
]

LESSONS["Q_CH12_003"] = [
    b("How do we change decametres into decimetres? The two words look alike, so let's go slowly.",
      g("q", "decametre → decimetre: what do we do?"), u("q", "deca"), u("q", "deci")),
    b("Deca means ten. So 1 decametre is 10 metres. Deci means a tenth. So 1 metre is 10 decimetres.",
      l("f1", "1 decametre = 10 metres"), l("f2", "1 metre = 10 decimetres")),
    b("Which one is the smaller unit?",
      ask=c("the decimetre", ["the decametre", "they are equal"],
            "A decimetre is only a tenth of a metre, about the length of a crayon. A decametre is 10 whole metres.")),
    b("We are going from a big unit to a small one. So there will be more of them, and that means we multiply."),
    b("Two steps down: decametre to metre is times 10, and metre to decimetre is times 10 again. 10 times 10 is 100.",
      w("c1", "10 × 10 = 100")),
    b("So to change decametres into decimetres, we multiply by 100.", a("ans", "multiply by 100")),
    b("Going to a smaller unit: multiply. Going to a bigger unit: divide. And count the steps between them."),
]

LESSONS["Q_CH12_004"] = [
    b("We want a pair of units where one is 1 hundredth of the other.", g("q", "Which pair: one unit = 1/100 of the other?")),
    b("Let's test each pair. A kilogram and a tonne: 1000 kilograms make a tonne. That is a thousandth, not a hundredth.",
      l("p1", "1000 kg = 1 tonne"), x("p1", "1000 kg = 1 tonne")),
    b("A metre and a kilometre: 1000 metres make a kilometre. A thousandth again.",
      l("p2", "1000 m = 1 km"), x("p2", "1000 m = 1 km")),
    b("A gram and a decagram: deca means ten, so 10 grams make a decagram. That is a tenth.",
      l("p3", "10 g = 1 decagram"), x("p3", "10 g = 1 decagram")),
    b("That leaves centilitre and litre. What does centi mean?",
      ask=c("a hundredth", ["a tenth", "a thousandth"],
            "Think of a century, which is 100 years, or a centimetre: 100 of them make a metre. Centi means a hundredth.")),
    b("100 centilitres make 1 litre. So a centilitre is 1 hundredth of a litre. That is our pair.",
      l("p4", "100 centilitres = 1 litre"), a("ans", "centilitre & litre")),
    b("The start of the word tells you: deci is a tenth, centi is a hundredth, milli is a thousandth."),
]

LESSONS["Q_CH12_005"] = [
    b("125 millilitres is what part of a litre? The answer will be a fraction.", g("q", "125 ml = ? litre")),
    b("1000 millilitres make 1 litre. So 125 millilitres is 125 out of 1000.",
      l("f", "1000 ml = 1 litre"), l("c1", "125 ml = 125/1000 litre")),
    b("That fraction is clumsy, so let's make it simpler. 125 doubled is 250. 250 doubled is 500. And 500 doubled is 1000.",
      w("c2", "125 × 2 = 250"), w("c3", "250 × 2 = 500"), w("c4", "500 × 2 = 1000")),
    b("We doubled 3 times. So how many 125s make 1000?",
      ask=c("8", ["3", "6"], "Doubling 3 times is 2 times 2 times 2. That makes 8.")),
    b("8 times 125 is 1000. So we can divide the top and the bottom of the fraction by 125.",
      w("c5", "8 × 125 = 1000"), w("c6", "125/1000 = 1/8")),
    b("125 millilitres is 1 eighth of a litre.", a("ans", "125 ml = 1/8 litre", ring="1/8")),
    b("So 8 small glasses of 125 millilitres fill 1 litre. Write the part over the whole, then simplify."),
]

LESSONS["Q_CH12_006"] = [
    b("37.02 kilograms. Let's write it as kilograms and grams.", g("q", "37.02 kg = ? kg ? g")),
    b("Split it at the point. 37 whole kilograms, and 0.02 of a kilogram.", w("c1", "37.02 = 37 + 0.02"), u("c1", "0.02")),
    b("1 kilogram is 1000 grams. So what is 0.02 kilograms in grams?", l("f", "1 kg = 1000 g"),
      ask=c("20 g", ["2 g", "200 g"],
            "Multiply 0.02 by 1000. The digits slide 3 places to the left, so 0.02 becomes 20.")),
    b("0.02 times 1000 is 20. So 0.02 kilograms is 20 grams.", w("c2", "0.02 × 1000 = 20")),
    b("Careful: it is not 2 grams. 2 grams would be 0.002 kilograms, with one more 0.", l("tr", "2 g = 0.002 kg")),
    b("So 37.02 kilograms is 37 kilograms 20 grams.", a("ans", "37 kg 20 g")),
    b("Split at the point, keep the whole kilograms, and multiply the decimal part by 1000."),
]

LESSONS["Q_CH12_007"] = [
    b("How many articles make 0.3 score? An article just means one thing, one item.", g("q", "0.3 score = ? articles")),
    b("First, how many is 1 whole score?",
      ask=c("20", ["12", "10", "100"], "A score is 20. A dozen is 12.")),
    b("1 score is 20. So 0.3 score is 0.3 times 20.", l("f", "1 score = 20"), w("t", "0.3 × 20 = ?")),
    b("0.3 means 3 tenths. One tenth of 20 is 2.", w("c1", "20 ÷ 10 = 2")),
    b("So 3 tenths of 20 is 3 times 2, which is 6.", w("c2", "3 × 2 = 6"), w("c3", "0.3 × 20 = 6")),
    b("So 0.3 score is 6 articles.", a("ans", "6 articles")),
    b("0.3 score is less than 1 score, so the answer must be less than 20. Always check the size of your answer."),
]

LESSONS["Q_CH12_008"] = [
    b("How many gross make a dozen? That sounds upside down, so let's think carefully.", g("q", "? gross = 1 dozen")),
    b("A gross is 12 dozen. That is 12 times 12, which is 144 things.", l("f", "1 gross = 12 dozen"), w("c1", "12 × 12 = 144")),
    b("Which is bigger: a gross or a dozen?",
      ask=c("a gross", ["a dozen", "they are equal"],
            "A gross holds 12 dozens inside it. So a gross is much bigger than a dozen.")),
    b("A dozen is smaller than a gross. So a dozen is only a part of a gross. The answer must be a fraction, less than 1."),
    b("12 dozens make 1 gross. So 1 dozen is 1 of 12 equal parts of a gross. That is 1 twelfth.",
      l("c2", "1 dozen = 1/12 gross")),
    b("So 1 twelfth of a gross makes a dozen.", a("ans", "1/12 gross")),
    b("Careful with the choices. 12 is how many dozens make a gross, and 144 is how many things. The question asked it the other way round."),
]

LESSONS["Q_CH12_009"] = [
    b("We must add 4 kilometres, 40 metres and 400 centimetres, and give the answer in metres.",
      g("q", "4 km + 40 m + 400 cm = ? m")),
    b("Three different units. What do we do before adding?",
      ask=c("change each one into metres", ["add 4 + 40 + 400", "write 4, 40, 400 side by side"],
            "We can only add lengths in the same unit. The answer is wanted in metres, so let's change each part into metres.")),
    b("1 kilometre is 1000 metres. So 4 kilometres is 4000 metres.",
      u("q", "4 km"), l("f1", "1 km = 1000 m"), w("c1", "4 × 1000 = 4000")),
    b("The 40 metres are already in metres. They stay as 40.", u("q", "40 m")),
    b("Now the centimetres. 100 centimetres make 1 metre, so 400 centimetres is 400 divided by 100. Only 4 metres.",
      u("q", "400 cm"), l("f2", "100 cm = 1 m"), w("c2", "400 ÷ 100 = 4")),
    b("Careful there: going to a bigger unit, the number gets smaller. 400 centimetres is not 400 metres."),
    b("Now add. 4000 plus 40 plus 4 is 4044.", w("c3", "4000 + 40 + 4 = 4044")),
    b("So the total is 4044 metres.", a("ans", "4044 m")),
]

LESSONS["Q_CH12_012"] = [
    b("We need to change 5 hectometres into decimetres.", g("q", "5 hm = ? dm")),
    b("Let's go through metres. Hecto means a hundred, so 1 hectometre is 100 metres. 5 hectometres is 500 metres.",
      l("f1", "1 hm = 100 m"), w("c1", "5 × 100 = 500")),
    b("Now metres to decimetres. Deci means a tenth. So how many decimetres are in 1 metre?",
      ask=c("10", ["100", "a tenth"],
            "A decimetre is a tenth of a metre. So it takes 10 of them to make 1 whole metre.")),
    b("1 metre is 10 decimetres. So 500 metres is 500 times 10, which is 5000 decimetres.",
      l("f2", "1 m = 10 dm"), w("c2", "500 × 10 = 5000")),
    b("So 5 hectometres is 5000 decimetres.", a("ans", "5000 dm")),
    b("Careful: 500 is in the choices, but that is the metres. We needed one more step down."),
    b("Times 100, then times 10. Altogether that is times 1000.", w("ck", "5 × 1000 = 5000")),
]

LESSONS["Q_CH12_013"] = [
    b("We want to write 800 grams in kilograms.", g("q", "800 g = ? kg")),
    b("Is 800 grams more than 1 kilogram, or less?",
      ask=c("less than 1 kilogram", ["more than 1 kilogram", "exactly 1 kilogram"],
            "1 kilogram is a thousand grams. 800 is not quite that many, so it is less than 1 kilogram.")),
    b("1000 grams make 1 kilogram. 800 is less than 1000, so our answer will start with 0 point something.",
      l("f", "1000 g = 1 kg")),
    b("To change grams into kilograms we divide by 1000. Each digit slides 3 places to the right.",
      w("t", "800 ÷ 1000 = ?")),
    b("The 8 lands in the tenths place. 800 divided by 1000 is 0.8.", w("c1", "800 ÷ 1000 = 0.8"), u("c1", "0.8")),
    b("So 800 grams is 0.8 kilograms.", a("ans", "0.8 kg")),
    b("Check: 0.8 is 8 tenths, and a tenth of a kilogram is 100 grams. 8 of those make 800 grams.", w("ck", "8 × 100 = 800")),
]

LESSONS["Q_CH12_014"] = [
    b("We want to write 80 metres in kilometres.", g("q", "80 m = ? km")),
    b("1000 metres make 1 kilometre. 80 metres is much less than that, so the answer is a small decimal.",
      l("f", "1000 m = 1 km")),
    b("To go from metres to kilometres, what do we do?",
      ask=c("divide by 1000", ["multiply by 1000", "divide by 100"],
            "Kilometres are bigger, so we need fewer of them. And 1000 metres make 1 kilometre, so we divide by 1000.")),
    b("80 divided by 1000. The digits slide 3 places to the right. The 8 lands in the hundredths place.",
      w("c1", "80 ÷ 1000 = 0.08"), u("c1", "0.08")),
    b("So 80 metres is 0.08 kilometres.", a("ans", "0.08 km")),
    b("Careful with the place. 0.8 kilometres would be 800 metres, ten times too far.", l("tr", "0.8 km = 800 m")),
    b("Divide by 1000, then check where each digit landed."),
]

LESSONS["Q_CH12_015"] = [
    b("We want to write 5 milligrams in grams.", g("q", "5 mg = ? g")),
    b("How many milligrams make 1 gram?",
      ask=c("1000", ["100", "10"], "Milli means a thousandth. So 1000 milligrams make 1 gram.")),
    b("1000 milligrams make 1 gram. So 1 milligram is 1 thousandth of a gram, and we divide by 1000.",
      l("f", "1000 mg = 1 g")),
    b("5 divided by 1000. The 5 slides 3 places to the right: past the tenths, past the hundredths, into the thousandths.",
      w("c1", "5 ÷ 1000 = 0.005")),
    b("We fill the empty places with zeros. 0.005.", u("c1", "0.005")),
    b("So 5 milligrams is 0.005 grams.", a("ans", "0.005 g")),
    b("Thousandths always need 3 places after the point. 0.5 grams would be 500 milligrams, far too much.",
      l("tr", "0.5 g = 500 mg")),
]

LESSONS["Q_CH12_016"] = [
    b("3 metres 7 decimetres. We want it all in centimetres.", g("q", "3 m 7 dm = ? cm")),
    b("Start with the metres. 1 metre is 100 centimetres, so 3 metres is 300 centimetres.",
      u("q", "3 m"), l("f1", "1 m = 100 cm"), w("c1", "3 × 100 = 300")),
    b("Now the decimetres. How many centimetres are in 1 decimetre?",
      ask=c("10", ["100", "1"], "A decimetre is a tenth of a metre. A tenth of 100 centimetres is 10 centimetres.")),
    b("1 decimetre is 10 centimetres, so 7 decimetres is 70 centimetres.",
      u("q", "7 dm"), l("f2", "1 dm = 10 cm"), w("c2", "7 × 10 = 70")),
    b("Careful: 70, not 7. With 7 centimetres we would get 307, and that is in the choices to catch us.",
      n("c2", "70", "not 7 → 307", "below")),
    b("Add the two parts. 300 plus 70 is 370.", w("c3", "300 + 70 = 370")),
    b("So 3 metres 7 decimetres is 370 centimetres.", a("ans", "370 cm")),
]

LESSONS["Q_CH12_017"] = [
    b("3 metres 7 centimetres. This time we want decimetres.", g("q", "3 m 7 cm = ? dm")),
    b("A decimetre sits between the metre and the centimetre. 1 metre is 10 decimetres, and 1 decimetre is 10 centimetres.",
      l("f1", "1 m = 10 dm"), l("f2", "1 dm = 10 cm")),
    b("The metres first. 3 metres is 3 times 10, which is 30 decimetres.", u("q", "3 m"), w("c1", "3 × 10 = 30")),
    b("Now 7 centimetres. Is that more than 1 decimetre, or less?",
      ask=c("less than 1 decimetre", ["more than 1 decimetre", "exactly 1 decimetre"],
            "It takes 10 centimetres to make 1 decimetre. We only have 7, so it is less than 1.")),
    b("7 centimetres is 7 tenths of a decimetre. 7 divided by 10 is 0.7.", u("q", "7 cm"), w("c2", "7 ÷ 10 = 0.7")),
    b("Add the parts. 30 plus 0.7 is 30.7.", w("c3", "30 + 0.7 = 30.7")),
    b("So 3 metres 7 centimetres is 30.7 decimetres.", a("ans", "30.7 dm")),
    b("Bigger unit to smaller: multiply. Smaller unit to bigger: divide. We used both here."),
]

LESSONS["Q_CH12_018"] = [
    b("2.5 kilograms. Let's write it as whole kilograms and grams.", g("q", "2.5 kg = ? kg ? g")),
    b("Split at the point. 2 whole kilograms, and 0.5 of a kilogram.", w("c1", "2.5 = 2 + 0.5"), u("c1", "0.5")),
    b("0.5 is the same as a half. 1 kilogram is 1000 grams. So what is half a kilogram?", l("f", "1 kg = 1000 g"),
      ask=c("500 g", ["5 g", "50 g"], "Half of 1000 is 500. So half a kilogram is 500 grams.")),
    b("0.5 times 1000 is 500. So 0.5 kilograms is 500 grams.", w("c2", "0.5 × 1000 = 500")),
    b("So 2.5 kilograms is 2 kilograms 500 grams.", a("ans", "2 kg 500 g")),
    b("Careful: the 5 after the point does not mean 5 grams. It means 5 tenths of a kilogram."),
    b("Split at the point, then multiply the decimal part by 1000."),
]

LESSONS["Q_CH12_019"] = [
    b("2.05 litres. Let's write it as whole litres and millilitres.", g("q", "2.05 litres = ? litres ? ml")),
    b("Split at the point. 2 whole litres, and 0.05 of a litre.", w("c1", "2.05 = 2 + 0.05"), u("c1", "0.05")),
    b("1 litre is 1000 millilitres. So we multiply 0.05 by 1000.", l("f", "1 litre = 1000 ml"), w("t", "0.05 × 1000 = ?")),
    b("Times 1000 slides the digits 3 places to the left. What does 0.05 become?",
      ask=c("50", ["5", "500"], "Slide the 5 once, twice, three times. It ends up in the tens place, with a 0 after it. That makes 50.")),
    b("0.05 times 1000 is 50. So 0.05 litres is 50 millilitres.", w("c2", "0.05 × 1000 = 50")),
    b("So 2.05 litres is 2 litres 50 millilitres.", a("ans", "2 litres 50 ml")),
    b("Watch that 0 after the point. 0.5 litres would be 500 millilitres, but 0.05 is ten times less.",
      l("tr", "0.5 litre = 500 ml")),
]

LESSONS["Q_CH12_020"] = [
    b("2.05 metres. Let's write it as whole metres and centimetres.", g("q", "2.05 m = ? m ? cm")),
    b("Split at the point. 2 whole metres, and 0.05 of a metre.", w("c1", "2.05 = 2 + 0.05"), u("c1", "0.05")),
    b("Now be careful. How many centimetres make 1 metre?",
      ask=c("100", ["1000", "10"],
            "Centi means a hundredth. So 100 centimetres make 1 metre. The 1000 is for millimetres.")),
    b("1 metre is 100 centimetres. So we multiply 0.05 by 100, and the digits slide 2 places to the left.",
      l("f", "1 m = 100 cm"), w("c2", "0.05 × 100 = 5")),
    b("So 0.05 metres is 5 centimetres.", u("c2", "= 5")),
    b("And 2.05 metres is 2 metres 5 centimetres.", a("ans", "2 m 5 cm")),
    b("With metres and centimetres it is times 100, not times 1000. Know your unit before you multiply."),
]

LESSONS["Q_CH12_021"] = [
    b("We want to write 30 kilograms in tonnes. A tonne is a very heavy weight, about as heavy as a small car.",
      g("q", "30 kg = ? tonne")),
    b("How many kilograms make 1 tonne?",
      ask=c("1000", ["100", "10"], "A tonne is a thousand kilograms.")),
    b("1000 kilograms make 1 tonne. 30 kilograms is tiny next to that, so the answer is a small decimal.",
      l("f", "1000 kg = 1 tonne")),
    b("We divide by 1000. The digits slide 3 places to the right, so the 3 lands in the hundredths place.",
      w("c1", "30 ÷ 1000 = 0.03"), u("c1", "0.03")),
    b("So 30 kilograms is 0.03 tonnes.", a("ans", "0.03 tonne")),
    b("Check the place. 0.3 tonnes would be 300 kilograms, and 0.003 tonnes would be only 3 kilograms.",
      l("t1", "0.3 tonne = 300 kg"), l("t2", "0.003 tonne = 3 kg")),
    b("Divide by 1000, then check where the digits landed."),
]

LESSONS["Q_CH12_024"] = [
    b("A shopkeeper has 5.4 kilograms of rice. He sells 2 kilograms 750 grams. How much rice is left?",
      g("q", "5.4 kg − 2 kg 750 g = ?")),
    b("One weight is a decimal, and the other is in kilograms and grams. What is the easiest plan?",
      ask=c("change both into grams", ["take 2 from 5 and 400 from 750", "add them"],
            "Mixed forms are hard to subtract. If both weights are in grams, it is one simple subtraction.")),
    b("1 kilogram is 1000 grams. So 5.4 kilograms is 5.4 times 1000, which is 5400 grams.",
      l("f", "1 kg = 1000 g"), w("c1", "5.4 × 1000 = 5400")),
    b("And 2 kilograms 750 grams is 2000 plus 750, which is 2750 grams.", w("c2", "2000 + 750 = 2750")),
    b("Now subtract. 5400 minus 2000 is 3400. Then take away the 750: 3400 minus 700 is 2700, and 50 less is 2650.",
      w("c3", "5400 − 2000 = 3400"), w("c4", "3400 − 700 = 2700"), w("c5", "2700 − 50 = 2650")),
    b("2650 grams is 2 kilograms and 650 grams. That is how much rice is left.", a("ans", "2 kg 650 g")),
    b("Check: 2650 plus 2750 is 5400. It works.", w("ck", "2650 + 2750 = 5400")),
    b("The trap is to take 400 from 750 because it looks easier. The 750 is being sold, so it is the one we take away."),
]
