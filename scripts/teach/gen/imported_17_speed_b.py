"""Speed, distance and time lessons in batch 17, written one by one (second nine)."""
from imported_17_lib import (B, BOX, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, STRIKE, UL, W)

P = "AIGEN_grade5_"
L = {}

TIME = "Time = distance ÷ speed"
AVG = "Average speed = total distance ÷ total time"


def HRS(line, target, text):
    return NOTE(line, target, text, "below")


# Arjun: Bangalore to Mysore, two equal halves, average speed.
L[P + "2964efcc-7362-4bd3-bf12-d08dc12a1c73"] = LESSON(
    B("Arjun's family drive fast before chai and slowly after it. We want the average speed for the driving, with the chai break left out.",
      GIVEN("g1", "150 km in all"),
      GIVEN("g2", "first 75 km at 50 km/hr, the rest at 25 km/hr")),
    B("How far is the rest? 150 minus 75 leaves another 75 kilometres. So the trip is two equal halves.",
      W("d", "150 − 75 = 75")),
    B("Average speed is whole distance divided by whole time, so we need the time for each half. First half: 75 divided by 50 is 1 and a half hours.",
      LB("f", AVG), W("t1", "75 ÷ 50 = 1.5"), HRS("t1", "1.5", "1½ hours")),
    B("The second half is the same distance at half the speed, 25 instead of 50. What happens to the time?",
      ask=CHOOSE(["it halves", "it doubles", "it stays the same"], 1,
                 "At half the speed, every kilometre takes twice as long. So the time doubles.")),
    B("75 divided by 25 is 3 hours, double the first half.",
      W("t2", "75 ÷ 25 = 3")),
    B("Whole time: 1 and a half plus 3 is 4 and a half hours. The chai break is left out, as the question says.",
      W("t", "1.5 + 3 = 4.5")),
    B("So the average speed is 150 divided by 4 and a half. Double both numbers to clear the half: 300 divided by 9.",
      W("e", "150 ÷ 4.5 = 300 ÷ 9")),
    B("9 times 33 is 297, so 300 divided by 9 is 33 and a little bit more. As a decimal it is about 33.33 kilometres an hour.",
      W("m", "9 × 33 = 297"), W("a", "300 ÷ 9 ≈ 33.33", "answer"), CIRC("a", "33.33")),
    B("Careful: halfway between 50 and 25 is 37.5, and that is one of the choices. But they spent 3 hours going slowly and only 1 and a half going fast, so the average is pulled down.",
      W("x", "(50 + 25) ÷ 2 = 37.5"), STRIKE("x", "(50 + 25) ÷ 2 = 37.5", "not the average speed")),
    B("So with two speeds over equal distances, the slow half takes longer. Find both times, add them, and divide the whole distance by the whole time."),
)

# Neha and Arjun: Pongal, how far at 80 km/hr.
L[P + "2ba5dc32-4f7d-4ba2-b99e-762057eb2571"] = LESSON(
    B("Here we know the whole distance and the whole time, but not how long each speed lasted. That calls for a clever trick.",
      GIVEN("g1", "240 km in 4 hours"),
      GIVEN("g2", "first part at 80 km/hr, the rest at 40 km/hr"),
      GIVEN("g3", "How many km at 80 km/hr?")),
    B("The trick is to pretend. Pretend all 4 hours were driven at the slow speed, 40. Then they would cover 40 times 4, which is 160 kilometres.",
      LB("p", "Pretend: all 4 hours at 40 km/hr"), W("p1", "40 × 4 = 160")),
    B("But the real trip is 240 kilometres. So our pretend trip is 240 minus 160, which is 80 kilometres short. The missing kilometres come from the fast hours.",
      W("p2", "240 − 160 = 80")),
    B("Swap one slow hour for a fast hour. How many extra kilometres does that add?",
      ask=CHOOSE(["80", "40", "120"], 1,
                 "In 1 hour at 80 they cover 80 kilometres, and in 1 hour at 40 they cover 40. So each fast hour adds 40 extra kilometres.")),
    B("Each fast hour adds 80 minus 40, which is 40 kilometres. We are 80 short, and 80 divided by 40 is 2. So 2 of the hours were fast.",
      W("p3", "80 − 40 = 40"), W("p4", "80 ÷ 40 = 2"), NOTE("p4", "= 2", "hours at 80", "below")),
    B("Careful: the question does not ask for hours. It asks how many kilometres were driven at 80. So what do we work out?",
      UL("g3", "How many km"),
      ask=CHOOSE(["40 × 2", "80 × 2", "240 ÷ 2"], 1,
                 "2 hours were driven at 80 kilometres an hour. Distance is speed times time, so it is 80 times 2.")),
    B("80 times 2 is 160. They travelled 160 kilometres at 80 kilometres an hour.",
      W("a", "80 × 2 = 160", "answer"), CIRC("a", "= 160")),
    B("By chance, 160 was also the length of our pretend trip. Don't let that confuse you: this 160 is the real distance at the fast speed."),
    B("Check the whole trip. 160 kilometres at 80 takes 2 hours. The other 80 kilometres, at 40, take 2 hours too. 2 plus 2 is 4 hours, just as the question says.",
      W("k1", "160 ÷ 80 = 2"), W("k2", "(240 − 160) ÷ 40 = 2"), W("k3", "2 + 2 = 4")),
    B("So when you know the whole time and two speeds: pretend it was all at one speed, see how far short you are, and let the gap between the speeds tell you the hours."),
)

# Kavya: Onam boat, distances and times given.
L[P + "2d6440d7-34f6-4b72-9433-cc20a033d160"] = LESSON(
    B("Kavya's boat goes down the river and back up again. This time the question hands us distances and times directly.",
      GIVEN("g1", "18 km downstream in 2 hours"),
      GIVEN("g2", "18 km upstream in 3 hours")),
    B("Average speed is the whole distance divided by the whole time. So what is the whole distance of the round trip?",
      LB("f", AVG),
      ask=CHOOSE(["18 km", "36 km", "9 km"], 1,
                 "The boat goes 18 kilometres down the river, and then 18 kilometres back. Both legs count.")),
    B("18 plus 18 is 36 kilometres. And the whole time is 2 hours plus 3 hours, which is 5 hours.",
      W("d", "18 + 18 = 36"), W("t", "2 + 3 = 5")),
    B("So we want 36 divided by 5. 5 times 7 is 35, which leaves 1 over.",
      W("m", "5 × 7 = 35"), W("r", "36 − 35 = 1")),
    B("That last 1, shared among 5, is 0.2. So 36 divided by 5 is 7.2. The average speed is 7.2 kilometres an hour.",
      W("r2", "1 ÷ 5 = 0.2"), W("a", "36 ÷ 5 = 7.2", "answer"), CIRC("a", "7.2")),
    B("Careful: some people find the two speeds first, 18 divided by 2 is 9, and 18 divided by 3 is 6, and then take the number halfway between, 7.5.",
      W("s1", "18 ÷ 2 = 9"), W("s2", "18 ÷ 3 = 6"), W("x", "(9 + 6) ÷ 2 = 7.5")),
    B("That is close, but it is a trap. The boat spends 3 hours at the slow speed and only 2 at the fast one, so the true average is a little lower.",
      STRIKE("x", "(9 + 6) ÷ 2 = 7.5", "not the average speed")),
    B("Check: 7.2 kilometres an hour, for 5 hours, is 36 kilometres. That is the full round trip.",
      W("k", "7.2 × 5 = 36")),
    B("So for a round trip, add both distances, add both times, and divide. Never just average the two speeds."),
)

# Deepa and Riya: Madurai, river 600 m wide, metres a second.
L[P + "479772a7-763e-438e-90f0-fd2916b35bc3"] = LESSON(
    B("A boat crosses a river and comes back more slowly. Notice the units here: metres and seconds, not kilometres and hours. The method is just the same.",
      GIVEN("g1", "River: 600 m wide"),
      GIVEN("g2", "across at 3 m/s, back at 2 m/s")),
    B("Average speed is whole distance divided by whole time. Going across, the time is 600 divided by 3, which is 200 seconds.",
      LB("f", AVG), W("t1", "600 ÷ 3 = 200")),
    B("Will the trip back take more time than 200 seconds, or less?",
      ask=CHOOSE(["less", "more", "the same"], 1,
                 "The river is just as wide, but the boat is slower on the way back. Slower over the same distance means more time.")),
    B("600 divided by 2 is 300 seconds. More time, as we expected.",
      W("t2", "600 ÷ 2 = 300")),
    B("Whole distance: 600 plus 600 is 1200 metres. Whole time: 200 plus 300 is 500 seconds.",
      W("d", "600 + 600 = 1200"), W("t", "200 + 300 = 500")),
    B("So we want 1200 divided by 500. Cross two zeros off each number, and it is 12 divided by 5, which is 2.4.",
      W("e", "1200 ÷ 500 = 12 ÷ 5"), W("a", "12 ÷ 5 = 2.4", "answer"), CIRC("a", "2.4")),
    B("The average speed is 2.4 metres a second."),
    B("Careful: 2.5, halfway between 3 and 2, is the tempting answer. But the boat spends 300 seconds at the slow speed and only 200 at the fast one, so the average leans towards 2.",
      W("x", "(3 + 2) ÷ 2 = 2.5"), STRIKE("x", "(3 + 2) ÷ 2 = 2.5", "not the average speed")),
    B("Check: 2.4 metres a second, for 500 seconds, is 1200 metres. Exactly the round trip.",
      W("k", "2.4 × 500 = 1200")),
    B("So across and back: time each crossing, add the distances, add the times, and divide."),
)

# Neha: Jaipur to Udaipur, half the TIME at each speed.
L[P + "4a0451d9-932e-40a5-b895-2ac2b7d2e2cd"] = LESSON(
    B("Neha's car spends part of the trip at 80 and part at 40. Before any sums, read the question very carefully.",
      GIVEN("g1", "400 km in all"),
      GIVEN("g2", "half the TIME at 80 km/hr, half the TIME at 40 km/hr")),
    B("It says half the time, not half the distance. That one word changes the whole question.",
      UL("g2", "TIME"), UL("g2", "TIME", 2)),
    B("When the time is shared equally, picture any 2 hours of the trip: 1 hour at 80, and 1 hour at 40. How far do they go in those 2 hours?",
      LB("p", "Any 2 hours: 1 hour at 80, 1 hour at 40"),
      ask=CHOOSE(["80 km", "120 km", "40 km"], 1,
                 "In the hour at 80 they cover 80 kilometres. In the hour at 40 they cover 40 more. Add the two together.")),
    B("80 plus 40 is 120 kilometres in 2 hours. That is 60 kilometres for every hour, on average.",
      W("d", "80 + 40 = 120"), W("s", "120 ÷ 2 = 60")),
    B("The whole trip is that same pattern, repeated. So the average speed for all 400 kilometres is 60 kilometres an hour.",
      LB("a", "Average speed = 60 km/hr", "answer"), CIRC("a", "60 km/hr")),
    B("Now the trap. Suppose it had said half the distance at each speed. Each half would be 200 kilometres: 2 and a half hours at 80, but 5 hours at 40.",
      W("x1", "200 ÷ 80 = 2.5"), W("x2", "200 ÷ 40 = 5")),
    B("That would be 400 kilometres in 7 and a half hours, only about 53.3 kilometres an hour. It is one of the choices, but it answers a different question.",
      W("x3", "2.5 + 5 = 7.5"), W("x4", "400 ÷ 7.5 ≈ 53.3"), STRIKE("x4", "53.3", "half the distance")),
    B("So with two speeds, look for the key word. Equal times: the average speed is halfway between, here 60. Equal distances: it comes out lower."),
)

# Priya and Kiran: sports day, 60 km.
L[P + "4b594e5a-c931-42a0-8c21-513758c9b397"] = LESSON(
    B("Priya and Kiran leave school together for a park. Priya rides at one steady speed. Kiran starts slowly and finishes fast.",
      GIVEN("g1", "School to park: 60 km"),
      GIVEN("g2", "Priya: 15 km/hr all the way"),
      GIVEN("g3", "Kiran: half the distance at 10, half at 20 km/hr")),
    B("Priya first. Time is distance divided by speed, and 60 divided by 15 is 4. Priya takes 4 hours.",
      LB("f", TIME), W("p", "60 ÷ 15 = 4")),
    B("Kiran's speeds are 10 and 20, and halfway between them is 15, the same as Priya's speed. So will they arrive together?",
      ask=CHOOSE(["yes, together", "no, Kiran is later", "no, Kiran is earlier"], 1,
                 "Let's not guess. Kiran spends longer on his slow half than on his fast half, so we must work out his time properly.")),
    B("Each half of the distance is 30 kilometres. Kiran's slow half: 30 divided by 10 is 3 hours.",
      W("h", "60 ÷ 2 = 30"), W("k1", "30 ÷ 10 = 3")),
    B("His fast half: 30 divided by 20 is 1 and a half hours.",
      W("k2", "30 ÷ 20 = 1.5"), HRS("k2", "1.5", "1½ hours")),
    B("So Kiran's whole time is 3 plus 1 and a half, which is 4 and a half hours.",
      W("k3", "3 + 1.5 = 4.5")),
    B("Priya takes 4 hours and Kiran takes 4 and a half. Priya is first, by half an hour.",
      W("d", "4.5 − 4 = 0.5")),
    B("The question wants minutes. Half an hour is half of 60 minutes, which is 30 minutes. Priya reaches the park first, by 30 minutes.",
      W("m", "0.5 × 60 = 30"), LB("a", "Priya is first, by 30 minutes", "answer"), CIRC("a", "30 minutes")),
    B("Why didn't Kiran's two speeds balance out? Because he rode slowly for 3 whole hours, and fast for only 1 and a half. The slow part counted for more."),
    B("So never trust the number halfway between two speeds. Time each part with distance divided by speed, then compare."),
)

# Kavita: bus to Mahabaleshwar, three stretches in minutes.
L[P + "4c99bde9-c14b-4e70-aa8f-93924d069dfc"] = LESSON(
    B("Kavita's bus has three stretches, each at its own speed. We want the average speed for the whole journey.",
      GIVEN("g1", "60 km/hr for 45 min, 30 km/hr for 40 min,"),
      GIVEN("g2", "15 km/hr for 20 min")),
    B("Average speed is whole distance divided by whole time. The speeds are for an hour but the times are in minutes. So, 45 minutes is what fraction of an hour?",
      LB("f", AVG),
      ask=CHOOSE(["1/2", "3/4", "4/5"], 1,
                 "An hour is 60 minutes. 15 minutes is one quarter of that, so 45 minutes is three quarters.")),
    B("45 minutes is three quarters of an hour. Three quarters of 60 is 45, so the highway stretch is 45 kilometres.",
      W("f1", "45/60 = 3/4"), W("d1", "60 × 3/4 = 45")),
    B("40 minutes is two thirds of an hour. Two thirds of 30 is 20, so the ghat stretch is 20 kilometres.",
      W("f2", "40/60 = 2/3"), W("d2", "30 × 2/3 = 20")),
    B("20 minutes is one third of an hour. One third of 15 is 5, so the town stretch is 5 kilometres.",
      W("f3", "20/60 = 1/3"), W("d3", "15 × 1/3 = 5")),
    B("Whole distance: 45 plus 20 plus 5 is 70 kilometres.",
      W("d", "45 + 20 + 5 = 70")),
    B("Whole time: 45 plus 40 plus 20 is 105 minutes. Every 15 minutes is a quarter of an hour, and 105 divided by 15 is 7. So that is 7 quarters of an hour.",
      W("t", "45 + 40 + 20 = 105"), W("t2", "105 ÷ 15 = 7")),
    B("70 kilometres in 7 quarter hours is 10 kilometres every quarter of an hour. 4 quarters make an hour, so that is 40 kilometres an hour.",
      W("q1", "70 ÷ 7 = 10"), W("q2", "10 × 4 = 40"), W("a", "70 ÷ (7/4) = 40", "answer"), CIRC("a", "= 40")),
    B("Careful: adding the three speeds and dividing by 3 gives 35, one of the choices. But the bus spent a different time at each speed, so that does not work.",
      W("x", "(60 + 30 + 15) ÷ 3 = 35"), STRIKE("x", "(60 + 30 + 15) ÷ 3 = 35", "not the average speed")),
    B("So find the distance of every stretch, add them, add the times, and divide. The average speed here is 40 kilometres an hour."),
)

# Kavya: Pune to Mahabaleshwar, average speed including the break.
L[P + "54aca949-2fcf-42bd-9525-fa6bfec7cb40"] = LESSON(
    B("Kavya's family drive, stop for chai, and drive again. We want the average speed of the whole journey, and this question counts the break.",
      GIVEN("g1", "120 km in all"),
      GIVEN("g2", "60 km at 60 km/hr → 30-minute break →"),
      GIVEN("g3", "60 km at 30 km/hr")),
    B("Average speed is whole distance divided by whole time. The distance is given, 120 kilometres, so all the work is in the time.",
      LB("f", AVG)),
    B("Highway: 60 divided by 60 is 1 hour. Ghat road: 60 divided by 30 is 2 hours.",
      W("t1", "60 ÷ 60 = 1"), W("t2", "60 ÷ 30 = 2")),
    B("The question says to count the chai break. So what is the whole time, from start to finish?",
      ask=CHOOSE(["3 hours", "3.5 hours", "2.5 hours"], 1,
                 "Driving takes 1 hour and then 2 hours, which is 3. The 30-minute break adds half an hour, making 3 and a half hours.")),
    B("1 hour, plus half an hour, plus 2 hours, is 3 and a half hours. The car stands still during the break, but the journey is still going on.",
      BOX("g2", "30-minute break"), W("t", "1 + 0.5 + 2 = 3.5")),
    B("So the average speed is 120 divided by 3 and a half. Double both numbers to clear the half: 240 divided by 7.",
      W("e", "120 ÷ 3.5 = 240 ÷ 7")),
    B("7 times 34 is 238, which leaves just 2 over. So 240 divided by 7 is 34 and a little bit: approximately 34.3 kilometres an hour.",
      W("m", "7 × 34 = 238"), W("r", "240 − 238 = 2"), W("a", "240 ÷ 7 ≈ 34.3", "answer"), CIRC("a", "34.3")),
    B("Careful: if you forget the break, you get 120 divided by 3, which is 40. That tempting 40 is among the choices, but it is the speed while driving, not for the whole journey.",
      W("x", "120 ÷ 3 = 40"), STRIKE("x", "120 ÷ 3 = 40", "forgets the break")),
    B("So read whether a break counts. If it does, it adds to the time but not to the distance, and the average speed drops."),
)

# Deepa: Jaipur to Udaipur, total time.
L[P + "57d787f5-2ed4-4fc2-9026-dac42c105c56"] = LESSON(
    B("Deepa's trip has three parts: a drive, a chai break, and a second drive. We want the whole time, break included.",
      GIVEN("g1", "400 km in all"),
      GIVEN("g2", "80 km/hr for 2 hours → chai for 30 minutes →"),
      GIVEN("g3", "the rest at 60 km/hr")),
    B("We know the first drive takes 2 hours, and the break is 30 minutes. The missing piece is the second drive, and for that we need its distance.",
      UL("g3", "the rest")),
    B("First, how far do they go before chai? Distance is speed times time: 80 times 2 is 160 kilometres.",
      W("d1", "80 × 2 = 160")),
    B("So how far is left to drive after chai?",
      ask=CHOOSE(["160 km", "240 km", "320 km"], 1,
                 "The whole trip is 400 kilometres, and 160 are done. Take 160 away from 400.")),
    B("400 minus 160 leaves 240 kilometres.",
      W("d2", "400 − 160 = 240")),
    B("Time is distance divided by speed. 240 divided by 60 is 4, so the second drive takes 4 hours.",
      W("t2", "240 ÷ 60 = 4")),
    B("Now add every part, break included: 2 hours, half an hour, and 4 hours. That is 6 and a half hours.",
      W("t", "2 + 0.5 + 4 = 6.5")),
    B("6 and a half hours is 6 hours 30 minutes. That is how long the whole journey takes.",
      LB("a", "Total time = 6 hours 30 minutes", "answer"), CIRC("a", "6 hours 30 minutes")),
    B("Careful: there are two easy slips. Leaving out the chai break gives only 6 hours. And using the whole 400 kilometres for the second drive gives far too long."),
    B("Check the distances: 160 plus 240 is 400. The whole road is covered.",
      W("k", "160 + 240 = 400")),
    B("So when a part is described as the rest, find what is left first. Then time each part, add the break, and total it all."),
)
