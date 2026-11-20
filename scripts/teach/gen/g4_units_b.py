"""gr4_units lessons, part B: G4A_UNITS_001 to G4A_UNITS_018."""
from g4_units_lib import a, b, c, fig, g, l, n, qfig, u, w

LESSONS = {}
T = "gr4_units"

LESSONS["G4A_UNITS_001"] = [
    b("A cycle track is 4 kilometres 75 metres long. We want that as one number of kilometres.",
      g("q", "4 km 75 m = ? km")),
    b("The 4 kilometres stay put. The 75 metres must become a part of a kilometre. How many metres make 1 kilometre?",
      u("q", "75 m"),
      ask=c("1000", ["100", "10"], "Kilo means a thousand. So it takes 1000 metres to make 1 kilometre.")),
    b("1000 metres make 1 kilometre, so we divide 75 by 1000. The digits slide 3 places to the right.",
      l("f", "1000 m = 1 km"), w("c1", "75 ÷ 1000 = 0.075")),
    b("Careful here. 0.75 kilometres would be 750 metres. Our 75 metres is much less, so a 0 must come after the point: 0.075.",
      l("tr", "0.75 km = 750 m"), u("c1", "0.075")),
    b("Now join it to the 4 whole kilometres. 4 plus 0.075 is 4.075.", w("c2", "4 + 0.075 = 4.075")),
    b("See it in the place chart. The 4 is in the ones, and the 7 and the 5 sit in the hundredths and thousandths.",
      fig("pc", qfig(T, "G4A_UNITS_001", 2))),
    b("So the track is 4.075 kilometres long.", a("ans", "4.075 km")),
    b("Remember: metres to kilometres means 3 decimal places. Fill the empty place with a 0."),
]

LESSONS["G4A_UNITS_002"] = [
    b("Meera's bottle holds 1.2 litres. She drinks 350 millilitres. How many millilitres are left?",
      g("q", "1.2 litres − 350 ml = ? ml")),
    b("Can we take 350 away from 1.2 just like that?",
      ask=c("no, change litres to ml first", ["yes, subtract straight away", "no, add them instead"],
            "The two amounts are in different units. We must make them both millilitres before we subtract.")),
    b("1 litre is 1000 millilitres. So 1.2 litres is 1.2 times 1000, which is 1200 millilitres.",
      l("f", "1 litre = 1000 ml"), w("c1", "1.2 × 1000 = 1200")),
    b("Careful: it is 1200, not 1020. The 0.2 of a litre is 200 millilitres.",
      l("tr", "0.2 litre = 200 ml"), n("c1", "1200", "not 1020", "below")),
    b("She drank the water, so we take it away. 1200 minus 350.", w("t", "1200 − 350 = ?")),
    b("Take away 300 first, which leaves 900. Then take away 50 more. That leaves 850.",
      w("c2", "1200 − 300 = 900"), w("c3", "900 − 50 = 850")),
    b("So 850 millilitres of water are left.", a("ans", "850 ml")),
    b("Check: 850 plus 350 is 1200. It works. Same units first, then subtract.", w("ck", "850 + 350 = 1200")),
]

LESSONS["G4A_UNITS_003"] = [
    b("A new pencil is 14 centimetres 6 millimetres long. After sharpening, it is 12 centimetres 9 millimetres. How many millimetres shorter is it?",
      g("q", "14 cm 6 mm − 12 cm 9 mm = ? mm")),
    b("The answer is wanted in millimetres. What is a good first step?",
      ask=c("write both lengths in mm", ["take 6 mm from 9 mm", "take 12 from 14 and stop"],
            "Mixed units are slippery. Let's write each length in millimetres only, then subtract once.")),
    b("1 centimetre is 10 millimetres. So 14 centimetres is 140 millimetres, and 6 more makes 146.",
      l("f", "1 cm = 10 mm"), w("c1", "140 + 6 = 146")),
    b("The same for the short pencil. 12 centimetres is 120 millimetres, and 9 more makes 129.",
      w("c2", "120 + 9 = 129")),
    b("Now find the gap between 129 and 146. Count up: 1 more gets us to 130, and 16 more gets us to 146.",
      w("c3", "129 + 1 = 130"), w("c4", "130 + 16 = 146")),
    b("1 and 16 make 17. So the pencil is 17 millimetres shorter.", w("c5", "146 − 129 = 17"), a("ans", "17 mm")),
    b("Here is the trap to dodge. Taking 6 from 9 mixes up the two pencils: the 9 millimetres belong to the shorter one."),
    b("So change everything into the small unit first. Then it is one clean subtraction."),
]

LESSONS["G4A_UNITS_004"] = [
    b("Amma buys 1 kilogram 750 grams of potatoes and 2 kilograms 400 grams of onions. What is the total, in kilograms?",
      g("q", "1 kg 750 g + 2 kg 400 g = ? kg")),
    b("Add the grams first. 750 plus 400 is 1150 grams.", u("q", "750 g"), u("q", "400 g"), w("c1", "750 + 400 = 1150")),
    b("1150 grams is more than 1000 grams. So what is hiding inside it?", l("f", "1000 g = 1 kg"),
      ask=c("a whole kilogram", ["nothing, leave it as it is", "ten kilograms"],
            "1000 grams make 1 kilogram. 1150 is more than 1000, so 1 whole kilogram is inside, with some grams left over.")),
    b("1150 grams is 1 kilogram and 150 grams. That extra kilogram joins the others.",
      w("c2", "1150 = 1000 + 150"), l("c2b", "1150 g = 1 kg 150 g")),
    b("Now the kilograms. 1 plus 2, plus the 1 we carried, makes 4. So the total is 4 kilograms 150 grams.",
      w("c3", "1 + 2 + 1 = 4"), l("c4", "Total = 4 kg 150 g")),
    b("Last step: write it as a decimal. 150 grams is 150 divided by 1000, which is 0.15 kilograms.",
      w("c5", "150 ÷ 1000 = 0.15")),
    b("So the vegetables weigh 4.15 kilograms. Watch the place: 0.015 would be only 15 grams.",
      n("c5", "0.15", "0.015 = only 15 g", "below"), a("ans", "4.15 kg")),
    b("Remember: when the grams pass 1000, carry a kilogram across."),
]

LESSONS["G4A_UNITS_005"] = [
    b("A fruit seller has 7 dozen bananas. He sells 3 score. How many bananas are left?",
      g("q", "7 dozen − 3 score = ? bananas")),
    b("Dozen and score are names for numbers. A dozen is 12. So 7 dozen is 7 times 12, which is 84 bananas.",
      l("f1", "1 dozen = 12"), w("c1", "7 × 12 = 84")),
    b("Now the score. How many is 1 score?",
      ask=c("20", ["12", "10"], "A score is 20. It is bigger than a dozen.")),
    b("A score is 20. So 3 score is 3 times 20, which is 60 bananas.", l("f2", "1 score = 20"), w("c2", "3 × 20 = 60")),
    b("He sold 60, so we take them away. 84 minus 60 is 24.", w("c3", "84 − 60 = 24")),
    b("So 24 bananas are left.", a("ans", "24 bananas")),
    b("Turn the number words into numbers first. After that it is a sum you already know how to do."),
]

LESSONS["G4A_UNITS_006"] = [
    b("A box holds 1 gross of pencils. A teacher gives 2 pencils to each of 54 children. How many pencils remain?",
      g("q", "1 gross − (2 each for 54 children) = ?")),
    b("How many is a gross?",
      ask=c("144", ["120", "100", "12"], "A gross is 12 dozen. And 12 times 12 is 144.")),
    b("A gross is 12 dozen, and 12 times 12 is 144. So the box starts with 144 pencils.",
      l("f", "1 gross = 12 dozen"), w("c1", "12 × 12 = 144")),
    b("Each of the 54 children gets 2 pencils. 54 times 2 is 108.", w("c2", "54 × 2 = 108")),
    b("Careful: it is 2 pencils each, not 1. If we forgot that, we would take away only 54.", u("q", "2 each")),
    b("Now subtract. 144 minus 108. Take away 100 to get 44, then 8 more to get 36.",
      w("c3", "144 − 100 = 44"), w("c4", "44 − 8 = 36")),
    b("So 36 pencils remain in the box.", a("ans", "36 pencils")),
    b("Check: 108 given out, plus 36 left, makes 144. It fits.", w("ck", "108 + 36 = 144")),
]

LESSONS["G4A_UNITS_007"] = [
    b("A milkman pours 750 millilitres of milk into each of 6 packets. How many litres does he use?",
      g("q", "6 packets × 750 ml = ? litres")),
    b("First the total in millilitres. 6 times 700 is 4200, and 6 times 50 is 300. Together, 4500 millilitres.",
      w("c1", "6 × 700 = 4200"), w("c2", "6 × 50 = 300"), w("c3", "4200 + 300 = 4500")),
    b("The question asks for litres. How do we change millilitres into litres?",
      ask=c("divide by 1000", ["multiply by 1000", "divide by 100"],
            "1000 millilitres make 1 litre. Litres are bigger, so there are fewer of them. We divide by 1000.")),
    b("1000 millilitres make 1 litre. 4500 divided by 1000 is 4.5.", l("f", "1000 ml = 1 litre"), w("c4", "4500 ÷ 1000 = 4.5")),
    b("So the milkman uses 4.5 litres of milk. That is 4 and a half litres.", a("ans", "4.5 litres")),
    b("Does it make sense? Each packet is less than 1 litre, so 6 packets must be less than 6 litres. 4.5 fits nicely."),
    b("The plan: multiply first, then change the unit at the end."),
]

LESSONS["G4A_UNITS_008"] = [
    b("Ravi's school is 850 metres from home. He walks there and back on each of 5 school days. How many kilometres is that in the week?",
      g("q", "850 m to school, there and back, 5 days"), l("q2", "How many km in the week?")),
    b("Read it slowly: there and back. How many times does Ravi walk the 850 metres in one day?",
      u("q", "there and back"),
      ask=c("2 times", ["1 time", "5 times"],
            "He walks to school, and then he walks home again. That is the 850 metres twice each day.")),
    b("So in one day he walks 850 times 2, which is 1700 metres.", w("c1", "850 × 2 = 1700")),
    b("There are 5 school days, so we need 1700 times 5. 1000 times 5 is 5000, and 700 times 5 is 3500. Together, 8500 metres.",
      w("c2", "1000 × 5 = 5000"), w("c3", "700 × 5 = 3500"), w("c4", "5000 + 3500 = 8500")),
    b("Now change metres into kilometres. 1000 metres make 1 kilometre, so we divide by 1000.",
      l("f", "1000 m = 1 km"), w("c5", "8500 ÷ 1000 = 8.5")),
    b("So Ravi walks 8.5 kilometres in the week.", a("ans", "8.5 km")),
    b("The trap was the walk home. Forget it and you get only half the distance. Always ask: one way, or both ways?"),
]

LESSONS["G4A_UNITS_009"] = [
    b("A carpenter cuts a plank 3 metres long into 8 equal pieces. How long is each piece, in centimetres?",
      g("q", "3 m ÷ 8 pieces = ? cm each")),
    b("The answer is wanted in centimetres. What shall we do first?",
      ask=c("change 3 m into cm", ["multiply 3 by 8", "divide 8 by 3"],
            "Cutting into equal pieces is sharing, so we will divide. But first, let's turn the 3 metres into centimetres.")),
    b("1 metre is 100 centimetres, so 3 metres is 300 centimetres.", l("f", "1 m = 100 cm"), w("c1", "3 × 100 = 300")),
    b("Now share 300 among 8 pieces. Halving 3 times is the same as dividing by 8. Half of 300 is 150.",
      w("c2", "300 ÷ 2 = 150")),
    b("Half of 150 is 75. And half of 75 is 37.5.", w("c3", "150 ÷ 2 = 75"), w("c4", "75 ÷ 2 = 37.5")),
    b("So each piece is 37.5 centimetres long.", w("c5", "300 ÷ 8 = 37.5"), a("ans", "37.5 cm")),
    b("Check: 8 pieces of 37.5 centimetres make 300 centimetres. And each piece is much shorter than the plank, as it should be.",
      w("ck", "8 × 37.5 = 300")),
]

LESSONS["G4A_UNITS_010"] = [
    b("A stack of 40 equal coins is 6 centimetres tall. How thick is one coin, in millimetres?",
      g("q", "40 coins = 6 cm tall. 1 coin = ? mm")),
    b("The answer is in millimetres, so change the height first. 1 centimetre is 10 millimetres, so 6 centimetres is 60 millimetres.",
      l("f", "1 cm = 10 mm"), w("c1", "6 × 10 = 60")),
    b("The 40 coins share that height equally. So which sum gives one coin?",
      ask=c("60 ÷ 40", ["60 × 40", "40 ÷ 60"],
            "The whole stack is 60 millimetres, shared among 40 coins. Sharing means dividing the height by the number of coins.")),
    b("60 divided by 40. Take a zero off both, and it is 6 divided by 4. 4 goes into 6 once, with 2 left over, and 2 out of 4 is a half.",
      w("c2", "60 ÷ 40 = 6 ÷ 4"), w("c3", "6 ÷ 4 = 1.5")),
    b("So one coin is 1.5 millimetres thick.", a("ans", "1.5 mm")),
    b("Check: 40 coins at 1.5 millimetres each make 60 millimetres, which is our 6 centimetres.", w("ck", "40 × 1.5 = 60")),
    b("Change the unit first, then share. And ask if the answer is sensible: a coin really is about that thin."),
]

LESSONS["G4A_UNITS_011"] = [
    b("Which of these 4 lengths is the greatest? They are written in different ways, so we cannot tell just by looking.",
      g("q", "Greatest: 1.08 km, 1 km 800 m, 1008 m, 10800 cm?")),
    b("What is the fair way to compare them?",
      ask=c("put them all in metres", ["pick the biggest number", "pick the biggest unit"],
            "A big number with a tiny unit can still be a short length. Let's write every length in metres, then compare.")),
    b("First, 1.08 kilometres. 1 kilometre is 1000 metres, so 1.08 times 1000 is 1080 metres.",
      l("f", "1 km = 1000 m"), w("c1", "1.08 × 1000 = 1080")),
    b("Next, 1 kilometre 800 metres. That is 1000 plus 800, which is 1800 metres.", w("c2", "1000 + 800 = 1800")),
    b("1008 metres is already in metres. Now the last one: 10800 centimetres. 100 centimetres make 1 metre, so divide by 100. Only 108 metres!",
      l("f2", "100 cm = 1 m"), w("c3", "10800 ÷ 100 = 108")),
    b("So in metres we have 1080, 1800, 1008 and 108. Which is the biggest?",
      l("cmp", "1080 m, 1800 m, 1008 m, 108 m"),
      ask=c("1800", ["1080", "1008"],
            "Look at the hundreds. 1800 has 8 hundreds after its thousand, more than any of the others.")),
    b("1800 metres is the greatest. That is 1 kilometre 800 metres.", u("cmp", "1800 m"), a("ans", "1 km 800 m")),
    b("Did you see the trap? 10800 looked huge, but centimetres are tiny. Always compare in the same unit."),
]

LESSONS["G4A_UNITS_012"] = [
    b("One tablet has 250 milligrams of medicine. How many grams are there in a strip of 10 tablets?",
      g("q", "10 tablets × 250 mg = ? g")),
    b("First the total in milligrams. 10 times 250 is 2500 milligrams.", w("c1", "10 × 250 = 2500")),
    b("Now we need grams. How many milligrams make 1 gram?",
      ask=c("1000", ["100", "10"], "Milli means a thousandth. So 1000 milligrams make 1 gram.")),
    b("1000 milligrams make 1 gram, so we divide by 1000. 2500 divided by 1000 is 2.5.",
      l("f", "1000 mg = 1 g"), w("c2", "2500 ÷ 1000 = 2.5")),
    b("So the strip contains 2.5 grams of medicine.", a("ans", "2.5 g")),
    b("Careful with the choices. 2500 is the number of milligrams, not grams. And 0.25 grams is just 1 tablet.",
      l("tr", "250 mg = 0.25 g")),
    b("Multiply first, then change the unit. And always check which unit the question wants."),
]

LESSONS["G4A_UNITS_013"] = [
    b("A tailor has 5 metres of cloth. He uses 2 metres 35 centimetres for a kurta. How much cloth is left?",
      g("q", "5 m − 2 m 35 cm = ?")),
    b("Let's write both lengths in centimetres. 1 metre is 100 centimetres, so 5 metres is 500 centimetres.",
      l("f", "1 m = 100 cm"), w("c1", "5 × 100 = 500")),
    b("And 2 metres 35 centimetres is 200 plus 35, which is 235 centimetres.", w("c2", "200 + 35 = 235")),
    b("Now subtract. 500 minus 200 is 300, and 300 minus 35 is 265.", w("c3", "500 − 200 = 300"), w("c4", "300 − 35 = 265")),
    b("265 centimetres. How do we write that in metres and centimetres?",
      ask=c("2 m 65 cm", ["26 m 5 cm", "3 m 65 cm"],
            "Every 100 centimetres is 1 metre. 265 has 2 hundreds, with 65 left over.")),
    b("265 is 200 and 65. So 2 metres 65 centimetres of cloth is left.", a("ans", "2 m 65 cm")),
    b("The trap is 3 metres 65. To take away the 35 centimetres, one of the metres had to be broken into 100 centimetres."),
    b("Check: 235 used, plus 265 left, makes 500. It works.", w("ck", "235 + 265 = 500")),
]

LESSONS["G4A_UNITS_014"] = [
    b("A running track is 4 hectometres long. Sunil runs 5 rounds. How many kilometres does he run?",
      g("q", "Track: 4 hectometres. 5 rounds = ? km")),
    b("What does hecto mean?",
      ask=c("a hundred", ["ten", "a thousand"], "Hecto means a hundred. So a hectometre is a hundred metres.")),
    b("1 hectometre is 100 metres. So one round is 4 times 100, which is 400 metres.",
      l("f1", "1 hectometre = 100 m"), w("c1", "4 × 100 = 400")),
    b("Sunil runs 5 rounds. 400 times 5 is 2000 metres.", w("c2", "400 × 5 = 2000")),
    b("Now change to kilometres. 1000 metres make 1 kilometre, and 2000 divided by 1000 is 2.",
      l("f2", "1000 m = 1 km"), w("c3", "2000 ÷ 1000 = 2")),
    b("So Sunil runs 2 kilometres.", a("ans", "2 km")),
    b("Remember: hecto is a hundred, and kilo is a thousand. Change to metres first, and the rest is easy."),
]

LESSONS["G4A_UNITS_015"] = [
    b("Rina needs 150 laddoos. The shop sells them only in boxes of one dozen. What is the least number of boxes she must buy?",
      g("q", "150 laddoos. Boxes of 1 dozen. Fewest boxes?")),
    b("A dozen is 12. So we ask: how many 12s do we need to reach 150? Start with 10 boxes: 12 times 10 is 120.",
      l("f", "1 dozen = 12"), w("c1", "12 × 10 = 120")),
    b("2 more boxes give 24 more laddoos. 120 plus 24 is 144. So 12 boxes hold 144 laddoos.",
      w("c2", "120 + 24 = 144"), w("c3", "12 × 12 = 144")),
    b("Rina needs 150, and 12 boxes give 144. Is that enough?", w("c4", "150 − 144 = 6"),
      ask=c("no, she is 6 short", ["yes, 144 is close enough", "no, she is 12 short"],
            "150 minus 144 is 6. She would be 6 laddoos short, and her guests would notice!")),
    b("She cannot buy part of a box. So she needs one whole box more. 12 plus 1 is 13 boxes.", w("c5", "12 + 1 = 13")),
    b("13 boxes hold 156 laddoos, which is enough. So Rina must buy 13 boxes.", w("c6", "13 × 12 = 156"), a("ans", "13 boxes")),
    b("When things come in packs, a remainder means one more pack. Round up, so that there is enough."),
]

LESSONS["G4A_UNITS_016"] = [
    b("Arjun walks 2 kilometres 75 metres, then 850 metres, then 1.5 kilometres. How many kilometres in all?",
      g("q", "2 km 75 m + 850 m + 1.5 km = ? km")),
    b("The 3 distances are written in 3 different ways. What is the safest plan?",
      ask=c("change all to metres, then add", ["add 2.75 + 850 + 1.5", "add 2 + 75 + 850 + 1.5"],
            "Different units cannot be added as they are. Let's put all of them in metres, add, and change back at the end.")),
    b("1 kilometre is 1000 metres. So 2 kilometres 75 metres is 2000 plus 75, which is 2075 metres.",
      l("f", "1 km = 1000 m"), w("c1", "2000 + 75 = 2075")),
    b("Careful: 2075, not 2750. The 75 metres are just 75.", n("c1", "2075", "not 2750", "below")),
    b("850 metres is already in metres. And 1.5 kilometres is 1.5 times 1000, which is 1500 metres.",
      w("c2", "1.5 × 1000 = 1500")),
    b("Now add. 2075 plus 1500 is 3575. Then 850 more makes 4425 metres.",
      w("c3", "2075 + 1500 = 3575"), w("c4", "3575 + 850 = 4425")),
    b("Back to kilometres: divide by 1000. 4425 divided by 1000 is 4.425.", w("c5", "4425 ÷ 1000 = 4.425")),
    b("So Arjun walks 4.425 kilometres in all.", a("ans", "4.425 km")),
    b("The plan: everything into the small unit, add, then change back."),
]

LESSONS["G4A_UNITS_017"] = [
    b("An empty basket weighs 600 grams. With 12 equal mangoes in it, it weighs 4 kilograms 200 grams. What does one mango weigh?",
      g("q", "Basket 600 g. Basket + 12 mangoes = 4 kg 200 g."), l("q2", "1 mango = ? g")),
    b("First make it all grams. 4 kilograms is 4000 grams, and 200 more makes 4200 grams.",
      l("f", "1 kg = 1000 g"), w("c1", "4000 + 200 = 4200")),
    b("Is 4200 grams the weight of the mangoes?",
      ask=c("no, the basket is in there too", ["yes, share it among 12", "no, add the basket again"],
            "The scale weighed the basket and the mangoes together. We must take the basket's 600 grams away first.")),
    b("Take the basket away. 4200 minus 600 is 3600 grams. That is the 12 mangoes alone.",
      w("c2", "4200 − 600 = 3600"), n("c2", "3600", "12 mangoes", "below")),
    b("Now share 3600 among 12 mangoes. 36 divided by 12 is 3, so 3600 divided by 12 is 300.",
      w("c3", "36 ÷ 12 = 3"), w("c4", "3600 ÷ 12 = 300")),
    b("So one mango weighs 300 grams.", a("ans", "300 g")),
    b("Check: 12 mangoes weigh 3600 grams, and the basket's 600 makes 4200. It fits.", w("ck", "3600 + 600 = 4200")),
    b("When something is weighed in a container, take the container away first."),
]

LESSONS["G4A_UNITS_018"] = [
    b("A leaking tap drips 5 millilitres of water every minute. How many litres does it waste in one full day?",
      g("q", "5 ml every minute. 1 day = ? litres")),
    b("Let's climb in steps: a minute, then an hour, then a day. An hour has 60 minutes, and a day has 24 hours.",
      l("f1", "1 hour = 60 minutes"), l("f2", "1 day = 24 hours")),
    b("So how much water drips away in one hour?",
      ask=c("5 × 60 ml", ["5 × 24 ml", "5 + 60 ml"],
            "The tap loses 5 millilitres in every one of the 60 minutes. So we multiply 5 by 60.")),
    b("5 times 60 is 300. The tap wastes 300 millilitres every hour.", w("c1", "5 × 60 = 300")),
    b("Now a whole day: 300 times 24. 3 times 24 is 72, so 300 times 24 is 7200 millilitres.",
      w("c2", "3 × 24 = 72"), w("c3", "300 × 24 = 7200")),
    b("Change to litres. 1000 millilitres make 1 litre, so 7200 divided by 1000 is 7.2.",
      l("f3", "1000 ml = 1 litre"), w("c4", "7200 ÷ 1000 = 7.2")),
    b("So the tap wastes 7.2 litres in a day. That is more than 7 big bottles of water, from tiny drips!",
      a("ans", "7.2 litres")),
    b("The trap is to stop at 300, which is only one hour. Go up step by step and you will not miss one."),
]
