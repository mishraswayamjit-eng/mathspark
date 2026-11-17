"""Speed, distance and time lessons in batch 17, written one by one (first nine)."""
from imported_17_lib import (B, BOX, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, STRIKE, UL, W)

P = "AIGEN_grade5_"
L = {}

TIME = "Time = distance ÷ speed"
DIST = "Distance = speed × time"
AVG = "Average speed = total distance ÷ total time"


def HRS(line, target, text):
    return NOTE(line, target, text, "below")


# Neha: Hyderabad to Vijayawada, arrival time.
L[P + "005fc3f8-e2b5-4c4a-85d9-7ce326980c6f"] = LESSON(
    B("Neha's trip has four parts: a drive, a chai break, a second drive, and one last stretch. We find how long each part takes, then count on from 7 o'clock.",
      GIVEN("g1", "270 km in all, leaving at 7:00 AM"),
      GIVEN("g2", "90 km at 60 km/hr → 30-minute break →"),
      GIVEN("g3", "120 km at 80 km/hr → the rest at 60 km/hr")),
    B("For a drive, time is distance divided by speed. First drive: 90 divided by 60 is 1 and a half, so 1 and a half hours.",
      LB("f", TIME), W("t1", "90 ÷ 60 = 1.5"), HRS("t1", "1.5", "1½ hours")),
    B("Second drive: 120 divided by 80 is 1 and a half as well. Another 1 and a half hours.",
      W("t2", "120 ÷ 80 = 1.5"), HRS("t2", "1.5", "1½ hours")),
    B("Now the last stretch. The question does not say how long it is. How can we find out?",
      ask=CHOOSE(["90 + 120", "270 − 90 − 120", "270 − 120"], 1,
                 "The whole trip is 270 kilometres. Take away the 90 and the 120 already driven, and what is left is the last stretch.")),
    B("270 minus 90 minus 120 leaves 60 kilometres. At 60 kilometres an hour, that takes exactly 1 hour.",
      W("d3", "270 − 90 − 120 = 60"), W("t3", "60 ÷ 60 = 1")),
    B("Careful: the chai break is not driving, but the clock keeps ticking. 30 minutes is half an hour, and it counts.",
      BOX("g2", "30-minute break"), HRS("g2", "30-minute break", "0.5 hour")),
    B("Add up all four parts: 1 and a half, plus a half, plus 1 and a half, plus 1. That makes 4 and a half hours.",
      W("sum", "1.5 + 0.5 + 1.5 + 1 = 4.5")),
    B("Now count on from 7 o'clock. 4 hours later is 11 o'clock, and half an hour more makes it 11 30 in the morning.",
      LB("a", "7:00 AM + 4 h 30 min = 11:30 AM", "answer"), CIRC("a", "11:30 AM")),
    B("Check the distances: 90 plus 120 plus 60 is 270, the whole trip. Nothing has been left out.",
      W("k", "90 + 120 + 60 = 270")),
    B("So for a trip in parts: find the time for each part, remember any break, add them all up, and count on from the starting time."),
)

# Priya: Shatabdi, Chennai to Bangalore, arrival time.
L[P + "008aeb36-e7d1-453c-8ac2-dd1777aad834"] = LESSON(
    B("Priya's train trip has three parts: a run, a stop at Vellore, and another run. We time each part, then count on from 6 o'clock.",
      GIVEN("g1", "Leaves at 6:00 AM"),
      GIVEN("g2", "120 km at 80 km/hr → stops 30 min →"),
      GIVEN("g3", "240 km at 120 km/hr")),
    B("While the train is moving, time is distance divided by speed. For the first run, which sum gives the time?",
      LB("f", TIME),
      ask=CHOOSE(["80 ÷ 120", "120 ÷ 80", "120 × 80"], 1,
                 "Time is distance divided by speed. The distance is 120 kilometres and the speed is 80, so it is 120 divided by 80.")),
    B("120 divided by 80 is 1 and a half. The first 80 kilometres take 1 hour, and what is left takes half an hour more.",
      W("t1", "120 ÷ 80 = 1.5"), HRS("t1", "1.5", "1½ hours")),
    B("Second run: 240 divided by 120 is 2. So that run takes 2 hours.",
      W("t2", "240 ÷ 120 = 2")),
    B("Careful: don't forget the stop at Vellore. The train is standing still, but the clock is not. 30 minutes is half an hour.",
      BOX("g2", "stops 30 min"), HRS("g2", "stops 30 min", "0.5 hour")),
    B("Add the three parts: 1 and a half, plus a half, plus 2. That makes 4 hours.",
      W("sum", "1.5 + 0.5 + 2 = 4")),
    B("The train left at 6 o'clock, and 4 hours later is 10 o'clock. It arrives in Bangalore at 10 in the morning.",
      LB("a", "6:00 AM + 4 hours = 10:00 AM", "answer"), CIRC("a", "10:00 AM")),
    B("Walk the clock through to check. The first run ends at half past 7. The stop ends at 8 o'clock. Then 2 more hours bring us to 10 o'clock.",
      LB("k", "6:00 → 7:30 → 8:00 → 10:00")),
    B("So time each moving part with distance divided by speed, add in any stop, and count on from the starting time."),
)

# Ravi: auto-rickshaw, two halves, answer in minutes.
L[P + "0275ee67-deaa-41e1-b4b9-ad89d80895a8"] = LESSON(
    B("Ravi's auto changes speed halfway to the station. So we time the two halves separately, and the answer has to be in minutes.",
      GIVEN("g1", "18 km to the station"),
      GIVEN("g2", "first half at 36 km/hr, second half at 24 km/hr")),
    B("How long is each half of the trip?",
      ask=CHOOSE(["18 km", "9 km", "36 km"], 1,
                 "The whole trip is 18 kilometres, and half of 18 is 9. So each half is 9 kilometres long.")),
    B("Each half is 9 kilometres. First half: at 36 kilometres an hour, 9 kilometres is a quarter of an hour's driving.",
      W("h", "18 ÷ 2 = 9"), W("t1", "9 ÷ 36 = 1/4")),
    B("We want minutes. An hour has 60 minutes, and a quarter of 60 is 15. So the first half takes 15 minutes.",
      LB("u", "1 hour = 60 minutes"), W("m1", "1/4 × 60 = 15")),
    B("Before we work it out: which half takes longer?",
      ask=CHOOSE(["the first half", "the second half", "they take the same time"], 1,
                 "Both halves are 9 kilometres, but the second one is driven more slowly. Slower over the same distance means more time.")),
    B("Second half, at 24 kilometres an hour. 24 kilometres take 60 minutes, so 1 kilometre takes 60 divided by 24, which is 2.5 minutes.",
      W("p", "60 ÷ 24 = 2.5")),
    B("9 kilometres take 9 times 2.5, which is 22.5 minutes. Longer than the first half, just as we expected.",
      W("m2", "9 × 2.5 = 22.5")),
    B("Add the two halves: 15 plus 22.5 is 37.5. The whole trip takes 37.5 minutes.",
      W("a", "15 + 22.5 = 37.5", "answer"), CIRC("a", "37.5")),
    B("Careful: it is tempting to average the two speeds and use that for the whole trip. It does not work, because the slow half lasts longer than the fast half."),
    B("So when the speed changes, time each part on its own with distance divided by speed. Then add the times."),
)

# Priya: Chennai to Pondicherry, half distance against half time.
L[P + "033e5e03-1780-45bd-b614-2ff77ce829e4"] = LESSON(
    B("This is a puzzle about average speed. Going, the two speeds share the distance equally. Coming back, they share the time equally. That small change matters.",
      GIVEN("g1", "TO: half the distance at 40, half at 60 km/hr"),
      GIVEN("g2", "BACK: half the time at 40, half at 60 km/hr")),
    B("No distance is given, so we may choose one that is easy to work with. Let's say the road is 240 kilometres long. Then each half is 120 kilometres.",
      LB("s", "Suppose the road is 240 km"), W("h", "240 ÷ 2 = 120")),
    B("Going there: 120 kilometres at 40 takes 3 hours. And 120 kilometres at 60 takes 2 hours.",
      W("t1", "120 ÷ 40 = 3"), W("t2", "120 ÷ 60 = 2")),
    B("Average speed is the whole distance divided by the whole time. So which sum gives the average speed going there?",
      LB("f", AVG),
      ask=CHOOSE(["(40 + 60) ÷ 2", "240 ÷ 5", "240 ÷ 2"], 1,
                 "The whole distance is 240 kilometres. The whole time is 3 hours plus 2 hours, which is 5 hours. So it is 240 divided by 5.")),
    B("240 divided by 5 is 48. Going to Pondicherry, the average speed is 48 kilometres an hour.",
      W("t3", "3 + 2 = 5"), W("to", "240 ÷ 5 = 48")),
    B("Now coming back, with half the time at each speed. Picture any 2 hours of that drive: 1 hour at 40, and 1 hour at 60. Together that is 100 kilometres.",
      W("b1", "40 × 1 + 60 × 1 = 100")),
    B("100 kilometres in 2 hours is 50 kilometres an hour. So coming back, the average speed is 50.",
      W("b2", "100 ÷ 2 = 50")),
    B("50 minus 48 is 2. Coming back is faster, by 2 kilometres an hour.",
      W("d", "50 − 48 = 2"), LB("a", "BACK is faster, by 2 km/hr", "answer"), CIRC("a", "2 km/hr")),
    B("Why the difference? Going there, the slow half took 3 hours and the fast half only 2. They spent more time going slowly, and that drags the average down."),
    B("So average speed is always whole distance divided by whole time. Equal distances are not equal times: the slower part always lasts longer."),
)

# Deepa and Arjun: the forgotten sweets.
L[P + "10d2ce3d-f46f-486a-8d20-0dfa4359d91a"] = LESSON(
    B("Two cyclists set off together. Deepa makes one steady trip. Arjun is faster, but he has to go there, come back for the sweets, and go there again.",
      GIVEN("g1", "Home to Grandmother's house: 30 km"),
      GIVEN("g2", "Deepa: 10 km/hr.  Arjun: 15 km/hr")),
    B("Deepa first. Time is distance divided by speed, and 30 divided by 10 is 3. Deepa takes 3 hours.",
      LB("f", TIME), W("d", "30 ÷ 10 = 3")),
    B("Now Arjun. How far does he cycle altogether before he arrives for the second time?",
      ask=CHOOSE(["30 km", "60 km", "90 km"], 2,
                 "Count his trips: to Grandmother's house, back home, and to Grandmother's house again. That is 3 trips of 30 kilometres.")),
    B("3 trips of 30 kilometres make 90 kilometres.", W("a1", "30 × 3 = 90")),
    B("At 15 kilometres an hour, 90 divided by 15 is 6. Arjun's whole ride takes 6 hours.",
      W("a2", "90 ÷ 15 = 6")),
    B("They started at the same time. Deepa arrives after 3 hours and Arjun after 6. 6 minus 3 is 3, so Arjun arrives 3 hours after Deepa.",
      W("a", "6 − 3 = 3", "answer"), CIRC("a", "= 3"), NOTE("a", "= 3", "hours later", "below")),
    B("Careful: the easy slip is to count only 2 trips for Arjun, there and back. But he still has to carry the sweets to Grandmother's house, and that is the third trip."),
    B("Check with a timeline. Each trip takes Arjun 2 hours, so he is at Grandmother's at 2 hours, home at 4, and back at Grandmother's at 6. Deepa walked in at 3.",
      W("k", "30 ÷ 15 = 2"), LB("k2", "Arjun: 2 h → 4 h → 6 h.   Deepa: 3 h")),
    B("So in a question like this, find each person's whole distance first, then their time. The gap between the times is the answer."),
)

# Neha: picnic, average speed including the chai break.
L[P + "18327336-63b9-4b85-97e2-d9052a77bd67"] = LESSON(
    B("We want the average speed for Neha's whole journey, and the question says the chai break counts too. Keep that in mind.",
      GIVEN("g1", "40 km/hr for 2 hours → chai for 30 minutes →"),
      GIVEN("g2", "60 km/hr for 1 hour")),
    B("Average speed is the whole distance divided by the whole time. So we need two totals. Distance first.",
      LB("f", AVG)),
    B("Distance is speed times time. 40 times 2 is 80 kilometres. Then 60 times 1 is 60 kilometres. Together, 80 plus 60 is 140 kilometres.",
      W("d1", "40 × 2 = 80"), W("d2", "60 × 1 = 60"), W("d3", "80 + 60 = 140")),
    B("Now the whole time. Remember, the chai break counts. So how long is the journey from start to finish?",
      ask=CHOOSE(["3 hours", "3.5 hours", "2.5 hours"], 1,
                 "They drive for 2 hours and then 1 hour, which is 3 hours. The 30-minute break is half an hour more, so 3 and a half hours.")),
    B("2 hours, plus half an hour, plus 1 hour, is 3 and a half hours. No distance is covered during the break, but the time still passes.",
      BOX("g1", "chai for 30 minutes"), W("t", "2 + 0.5 + 1 = 3.5")),
    B("So we want 140 divided by 3 and a half. Double both numbers to get rid of the half: 280 divided by 7, and that is 40.",
      W("e", "140 ÷ 3.5 = 280 ÷ 7"), W("a", "280 ÷ 7 = 40", "answer"), CIRC("a", "= 40")),
    B("So the average speed for the whole journey is 40 kilometres an hour."),
    B("Careful: two slips are waiting here. One is to leave out the break. The other is to take the number halfway between 40 and 60, which is 50.",
      W("x", "(40 + 60) ÷ 2 = 50"), STRIKE("x", "(40 + 60) ÷ 2 = 50", "not the average speed")),
    B("Check: 40 kilometres an hour, kept up for 3 and a half hours, gives 140 kilometres. That is exactly the distance they covered.",
      W("k", "40 × 3.5 = 140")),
    B("So for average speed: add up all the distance, add up all the time, breaks included if the question says so, and divide."),
)

# Deepa: Dal Lake, out and back.
L[P + "1f368230-2fc1-4206-bff3-18234b041e34"] = LESSON(
    B("The boat goes out to an island and comes back. We know how long the trip out takes, but not the trip back. That is the piece to find.",
      GIVEN("g1", "Out: 6 km/hr for 20 minutes"),
      GIVEN("g2", "Back, same route: 4 km/hr")),
    B("To time the trip back we need the distance to the island. Start here: 20 minutes is what fraction of an hour?",
      LB("u", "1 hour = 60 minutes"),
      ask=CHOOSE(["1/2", "1/3", "1/4"], 1,
                 "An hour has 60 minutes, and 20 goes into 60 exactly 3 times. So 20 minutes is one third of an hour.")),
    B("20 minutes is a third of an hour. In a full hour the boat would go 6 kilometres, so in a third of an hour it goes a third of 6, which is 2 kilometres.",
      W("fr", "20/60 = 1/3"), W("d", "6 × 1/3 = 2")),
    B("The way back is the same route, so it is 2 kilometres too. At 4 kilometres an hour, 2 divided by 4 is a half: half an hour.",
      W("t", "2 ÷ 4 = 1/2")),
    B("Half an hour is half of 60 minutes, which is 30 minutes.",
      W("m", "1/2 × 60 = 30")),
    B("Careful: the trip back is not 20 minutes again. The distance is the same, but the boat is slower, so it takes longer."),
    B("20 minutes out, plus 30 minutes back, makes 50 minutes for the whole ride.",
      W("a", "20 + 30 = 50", "answer"), CIRC("a", "= 50"), NOTE("a", "= 50", "minutes", "below")),
    B("Does 30 minutes back make sense? At 4 kilometres an hour, half an hour gives 2 kilometres, exactly the distance to the island.",
      W("k", "4 × 1/2 = 2")),
    B("So for a there-and-back trip: use the leg you know fully to find the distance, then use that distance to time the other leg."),
)

# Ravi: Kerala, 3 km downstream and upstream, average speed.
L[P + "1fe16fb0-b0a5-4b97-b6d6-494f11811187"] = LESSON(
    B("Ravi's boat races downstream and crawls back upstream. We want its average speed for the whole trip.",
      GIVEN("g1", "3 km downstream at 15 km/hr"),
      GIVEN("g2", "3 km upstream at 5 km/hr")),
    B("Here is a tempting shortcut: the number halfway between 15 and 5 is 10. Will that be the average speed?",
      W("x", "(15 + 5) ÷ 2 = 10"),
      ask=CHOOSE(["yes, halfway is the average", "no, the slow part lasts longer"], 1,
                 "The boat spends much longer crawling upstream than racing downstream. So the slow speed counts for more, and halfway will not do.")),
    B("Average speed is the whole distance divided by the whole time. The distance is easy: 3 kilometres down and 3 back make 6 kilometres.",
      STRIKE("x", "(15 + 5) ÷ 2 = 10", "not the average speed"), LB("f", AVG), W("d", "3 + 3 = 6")),
    B("Time downstream: 3 divided by 15 is one fifth of an hour. One fifth of 60 minutes is 12 minutes.",
      W("t1", "3 ÷ 15 = 1/5"), W("m1", "1/5 × 60 = 12")),
    B("Time upstream: 3 divided by 5 is three fifths of an hour, and that is 36 minutes. Three times as long as the trip down!",
      W("t2", "3 ÷ 5 = 3/5"), W("m2", "3/5 × 60 = 36")),
    B("Together, 12 plus 36 is 48 minutes. In fifths, one fifth plus three fifths is four fifths of an hour.",
      W("m3", "12 + 36 = 48"), W("t3", "1/5 + 3/5 = 4/5")),
    B("So the boat covers 6 kilometres in 4 fifths of an hour. In each fifth of an hour, that is 6 divided by 4, which is 1.5 kilometres.",
      W("p", "6 ÷ 4 = 1.5")),
    B("A whole hour is 5 fifths, and 5 times 1.5 is 7.5. So the average speed is 7.5 kilometres an hour.",
      W("q", "1.5 × 5 = 7.5"), W("a", "6 ÷ (4/5) = 7.5", "answer"), CIRC("a", "7.5")),
    B("It makes sense that 7.5 is nearer to 5 than to 15. The boat spent 36 minutes going slowly and only 12 minutes going fast."),
    B("So never average the two speeds. Find the whole distance and the whole time, and divide."),
)

# Ravi: Ganges, upstream then downstream, prayer time left out.
L[P + "27632c7e-9b71-456a-a6b0-d35305b5b385"] = LESSON(
    B("Ravi and his grandfather go up the river to a temple and come back down. We want the average speed on the water, with the prayer time left out.",
      GIVEN("g1", "Upstream: 6 km/hr for 2 hours"),
      GIVEN("g2", "1 hour of prayers (not counted)"),
      GIVEN("g3", "Downstream, same route: 12 km/hr")),
    B("Average speed is whole distance divided by whole time. First, how far is the temple? Distance is speed times time: 6 times 2 is 12 kilometres.",
      LB("f", AVG), W("d1", "6 × 2 = 12")),
    B("Coming back is the same 12 kilometres, at 12 kilometres an hour. How long does that take?",
      ask=CHOOSE(["half an hour", "1 hour", "2 hours"], 1,
                 "Time is distance divided by speed. 12 divided by 12 is 1, so the way back takes 1 hour.")),
    B("12 divided by 12 is 1 hour. Twice the speed, so half the time of the trip up.",
      W("t2", "12 ÷ 12 = 1")),
    B("Whole distance: 12 kilometres there and 12 back make 24 kilometres.",
      W("d", "12 + 12 = 24")),
    B("Whole time. Careful: the question tells us to leave out the hour of prayers. So we count only the time on the water, 2 hours plus 1 hour, which is 3 hours.",
      STRIKE("g2", "1 hour of prayers", "leave out"), W("t", "2 + 1 = 3")),
    B("24 divided by 3 is 8. The average speed is 8 kilometres an hour.",
      W("a", "24 ÷ 3 = 8", "answer"), CIRC("a", "= 8")),
    B("Notice it is not 9, the number halfway between 6 and 12. They spent 2 hours at the slow speed and only 1 hour at the fast speed, so the average sits nearer to 6."),
    B("Check: 8 kilometres an hour, for 3 hours, is 24 kilometres. That is the whole trip.",
      W("k", "8 × 3 = 24")),
    B("So for average speed, total the distance, total the time the question wants counted, and divide."),
)
