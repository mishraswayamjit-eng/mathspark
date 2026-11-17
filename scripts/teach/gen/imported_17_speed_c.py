"""Speed, distance and time lessons in batch 17, written one by one (last nine)."""
from imported_17_lib import (B, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, STRIKE, UL, W)

P = "AIGEN_grade5_"
L = {}

TIME = "Time = distance ÷ speed"
DIST = "Distance = speed × time"
AVG = "Average speed = total distance ÷ total time"


def HRS(line, target, text):
    return NOTE(line, target, text, "below")


# Aarav: bicycle to the Diwali party, total distance.
L[P + "597a64d3-34f5-4bb7-8a42-f7d971e33595"] = LESSON(
    B("Aarav rides in two stretches, one quick and one slow. We want the whole distance to his friend's house.",
      GIVEN("g1", "10 km/hr for 30 minutes"),
      GIVEN("g2", "6 km/hr for 20 minutes")),
    B("Distance is speed times time. But each speed is for a whole hour, and Aarav rides for less than that. So, 30 minutes is what fraction of an hour?",
      LB("f", DIST), LB("u", "1 hour = 60 minutes"),
      ask=CHOOSE(["1/3", "1/2", "3/10"], 1,
                 "An hour is 60 minutes, and 30 is half of 60. So 30 minutes is half an hour.")),
    B("In a whole hour Aarav would ride 10 kilometres. In half an hour he rides half of 10, which is 5 kilometres.",
      W("d1", "10 × 1/2 = 5")),
    B("Now the crowded market. 20 minutes goes into 60 three times, so 20 minutes is one third of an hour.",
      W("fr", "20/60 = 1/3")),
    B("In a whole hour at this speed he would ride 6 kilometres. A third of 6 is 2 kilometres.",
      W("d2", "6 × 1/3 = 2")),
    B("5 plus 2 is 7. Aarav rides 7 kilometres altogether.",
      W("a", "5 + 2 = 7", "answer"), CIRC("a", "= 7"), NOTE("a", "= 7", "km", "below")),
    B("Careful: the big slip here is to multiply the speed by the minutes, like 10 times 30. The speed is for each hour, so the time must be in hours too."),
    B("So when the time is in minutes, turn it into a fraction of an hour first. Then distance is speed times time, one stretch at a time."),
)

# Vikram: jog to the ground, walk back.
L[P + "6c21fe21-0dd5-461b-9280-a9cb4a1aaf1c"] = LESSON(
    B("Vikram jogs to the cricket ground and walks home again. Same road both ways, but two different speeds.",
      GIVEN("g1", "Ground: 4 km from home"),
      GIVEN("g2", "jogs there at 8 km/hr, walks back at 4 km/hr")),
    B("We time each way separately. For the jog, which sum gives the time?",
      LB("f", TIME),
      ask=CHOOSE(["8 ÷ 4", "4 ÷ 8", "8 × 4"], 1,
                 "Time is distance divided by speed. The distance is 4 kilometres and the speed is 8, so it is 4 divided by 8.")),
    B("4 divided by 8 is one half. That makes sense: in a whole hour he would jog 8 kilometres, so 4 kilometres takes half an hour.",
      W("t1", "4 ÷ 8 = 1/2"), HRS("t1", "1/2", "½ hour")),
    B("Now the walk home. The same 4 kilometres, at 4 kilometres an hour. 4 divided by 4 is 1, so the walk takes 1 hour.",
      W("t2", "4 ÷ 4 = 1"), HRS("t2", "= 1", "hour")),
    B("Careful: the way back is not another half hour. It is the same road, but at half the speed, so it takes twice as long."),
    B("Half an hour plus 1 hour is 1 and a half hours. And half an hour is 30 minutes, so that is 1 hour 30 minutes.",
      W("s", "0.5 + 1 = 1.5"), LB("a", "Total time = 1 hour 30 minutes", "answer"), CIRC("a", "1 hour 30 minutes")),
    B("Check each way. Jogging at 8 for half an hour covers 4 kilometres. Walking at 4 for 1 hour covers 4 kilometres. Both match the distance to the ground.",
      W("k1", "8 × 1/2 = 4"), W("k2", "4 × 1 = 4")),
    B("So for a there-and-back trip at two speeds: time each way with distance divided by speed, then add the two times."),
)

# Deepa and Arjun: Sankranti, catching up.
L[P + "6ce388ca-8012-4430-aaed-00b85ef1bbd3"] = LESSON(
    B("Deepa sets off first, and Arjun chases her on a faster cycle. We want to know when he catches up, and how far they still have to go.",
      GIVEN("g1", "Grandmother's house: 24 km away"),
      GIVEN("g2", "Deepa: starts 8:00 AM, 8 km/hr"),
      GIVEN("g3", "Arjun: starts 8:30 AM, 12 km/hr")),
    B("Deepa has a head start of 30 minutes, which is half an hour. How far does she get before Arjun even sets off?",
      ask=CHOOSE(["8 km", "4 km", "12 km"], 1,
                 "In a whole hour Deepa cycles 8 kilometres. In half an hour she covers half of that.")),
    B("Half of 8 is 4. So at half past 8, when Arjun starts, Deepa is 4 kilometres ahead.",
      W("h", "8 × 1/2 = 4"), NOTE("h", "= 4", "km head start", "below")),
    B("Now both are moving. Each hour Arjun covers 12 kilometres and Deepa covers 8. So each hour Arjun gains 12 minus 8, which is 4 kilometres.",
      W("c", "12 − 8 = 4"), NOTE("c", "= 4", "km gained each hour", "below")),
    B("The gap is 4 kilometres, and it shrinks by 4 kilometres every hour. How long until Arjun catches up?",
      ask=CHOOSE(["half an hour", "1 hour", "2 hours"], 1,
                 "The gap is 4 kilometres wide and closes by 4 kilometres each hour. 4 divided by 4 is 1, so it takes 1 hour.")),
    B("4 divided by 4 is 1 hour. Arjun started at half past 8, so he catches Deepa at half past 9.",
      W("t", "4 ÷ 4 = 1"), LB("t2", "8:30 AM + 1 hour = 9:30 AM")),
    B("Where are they then? Arjun has cycled 1 hour at 12, so 12 kilometres. Deepa has cycled 1 and a half hours at 8, which is also 12 kilometres. They really are side by side.",
      W("p1", "12 × 1 = 12"), W("p2", "8 × 1.5 = 12")),
    B("Careful: the question asks how far they are from Grandmother's house, not from home. 24 minus 12 leaves 12 kilometres still to go.",
      W("r", "24 − 12 = 12")),
    B("So Arjun catches up at 9 30 in the morning, and they are 12 kilometres away from Grandmother's house.",
      LB("a", "9:30 AM, and 12 km from Grandmother's", "answer"), CIRC("a", "9:30 AM"), CIRC("a", "12 km")),
    B("So for a catching-up question: find the head start, find how fast the gap closes, and divide. Then read exactly what the question asks for."),
)

# Kabir: Jaipur to a dhaba, two halves, total time.
L[P + "71d92ff4-e747-4f87-84f7-ea9b483d01fc"] = LESSON(
    B("Kabir's dad drives the first half of the way quickly, then traffic slows the second half. We want the time for the whole trip.",
      GIVEN("g1", "Dhaba: 120 km away"),
      GIVEN("g2", "first half at 60 km/hr, second half at 40 km/hr")),
    B("Half of 120 is 60, so each half is 60 kilometres. The first half is 60 kilometres at 60 kilometres an hour, and that takes exactly 1 hour.",
      W("h", "120 ÷ 2 = 60"), LB("f", TIME), W("t1", "60 ÷ 60 = 1")),
    B("Now the second half: 60 kilometres at 40 kilometres an hour. Which sum gives the time?",
      ask=CHOOSE(["40 ÷ 60", "60 ÷ 40", "120 ÷ 40"], 1,
                 "Time is distance divided by speed. This half is 60 kilometres long and the speed is 40, so it is 60 divided by 40.")),
    B("60 divided by 40 is 1 and a half. The first 40 kilometres take 1 hour, and what is left takes half an hour more.",
      W("t2", "60 ÷ 40 = 1.5"), HRS("t2", "1.5", "1½ hours")),
    B("1 hour plus 1 and a half hours is 2 and a half hours. That is 2 hours 30 minutes.",
      W("s", "1 + 1.5 = 2.5"), LB("a", "Total time = 2 hours 30 minutes", "answer"), CIRC("a", "2 hours 30 minutes")),
    B("Careful: it is tempting to average the speeds to 50, and divide 120 by 50. That gives a little under 2 and a half hours, and it is a trap. The slow half lasts longer.",
      W("x", "(60 + 40) ÷ 2 = 50"), STRIKE("x", "(60 + 40) ÷ 2 = 50", "a trap")),
    B("Check the distance. 1 hour at 60 is 60 kilometres. 1 and a half hours at 40 is 60 kilometres as well. Together, 120 kilometres.",
      W("k", "60 × 1 + 40 × 1.5 = 120")),
    B("So when a trip is split into halves by distance, time each half on its own and add. Never average the two speeds."),
)

# Ravi: Onam boat, 40 minutes downstream, average speed.
L[P + "760c2d33-3b78-477f-901a-99386bad9471"] = LESSON(
    B("Ravi's boat goes down the river to a temple and back up again. We want the average speed on the water, with the time at the temple left out.",
      GIVEN("g1", "Downstream: 18 km/hr for 40 minutes"),
      GIVEN("g2", "30 minutes at the temple (not counted)"),
      GIVEN("g3", "Upstream, same route: 12 km/hr")),
    B("First we need the distance to the temple. The speed is for an hour, so: 40 minutes is what fraction of an hour?",
      LB("u", "1 hour = 60 minutes"),
      ask=CHOOSE(["3/4", "2/3", "4/10"], 1,
                 "40 out of 60 is the same as 4 out of 6, and that is 2 out of 3. So 40 minutes is two thirds of an hour.")),
    B("40 minutes is two thirds of an hour. Two thirds of 18 is 12, so the temple is 12 kilometres away.",
      W("fr", "40/60 = 2/3"), W("d1", "18 × 2/3 = 12")),
    B("Coming back is the same 12 kilometres, at 12 kilometres an hour. 12 divided by 12 is 1, so the trip back takes 1 hour.",
      W("t2", "12 ÷ 12 = 1")),
    B("Whole distance: 12 kilometres there and 12 back make 24 kilometres.",
      W("d", "12 + 12 = 24")),
    B("Whole time, leaving out the temple as the question says: two thirds of an hour, plus 1 hour. In thirds, that is 5 thirds of an hour.",
      STRIKE("g2", "30 minutes at the temple", "leave out"), W("t", "2/3 + 1 = 5/3")),
    B("So the boat covers 24 kilometres in 5 thirds of an hour. In each third of an hour, that is 24 divided by 5, which is 4.8 kilometres.",
      LB("f", AVG), W("p", "24 ÷ 5 = 4.8")),
    B("A whole hour is 3 thirds, and 3 times 4.8 is 14.4. The average speed is 14.4 kilometres an hour.",
      W("q", "4.8 × 3 = 14.4"), W("a", "24 ÷ (5/3) = 14.4", "answer"), CIRC("a", "14.4")),
    B("Careful: 15, halfway between 18 and 12, is one of the choices. But the boat spent a whole hour at the slow speed and only 40 minutes at the fast one, so the answer is below 15.",
      W("x", "(18 + 12) ÷ 2 = 15"), STRIKE("x", "(18 + 12) ÷ 2 = 15", "not the average speed")),
    B("So find the distance from the leg you know, time the other leg, then divide whole distance by whole time on the move."),
)

# Suresh and Priya: same total time, Priya's steady speed.
L[P + "7c4fc3bc-d48a-4421-952e-19b607aebd1b"] = LESSON(
    B("Suresh jogs to the park and walks back. Priya cycles there and back at one steady speed, and takes exactly as long as he does. We want her speed.",
      GIVEN("g1", "Park: 6 km away"),
      GIVEN("g2", "Suresh: there at 6 km/hr, back at 4 km/hr"),
      GIVEN("g3", "Priya: same total time, one steady speed")),
    B("Priya's time is the same as Suresh's, so we find his first. Jogging there: 6 divided by 6 is 1 hour.",
      LB("f", TIME), W("t1", "6 ÷ 6 = 1")),
    B("Walking back: 6 divided by 4 is 1 and a half hours. Altogether, 1 plus 1 and a half makes 2 and a half hours.",
      W("t2", "6 ÷ 4 = 1.5"), W("t", "1 + 1.5 = 2.5")),
    B("So Priya is out for 2 and a half hours too. How far does she cycle in that time?",
      ask=CHOOSE(["6 km", "12 km", "10 km"], 1,
                 "Priya goes to the park and back, just like Suresh. That is 6 kilometres, and then 6 more.")),
    B("6 plus 6 is 12 kilometres.", W("d", "6 + 6 = 12")),
    B("Speed is distance divided by time: 12 divided by 2 and a half. Double both numbers to clear the half, and it becomes 24 divided by 5.",
      W("e", "12 ÷ 2.5 = 24 ÷ 5")),
    B("5 times 4 is 20, which leaves 4 over. And 4 shared among 5 is 0.8. So 24 divided by 5 is 4.8.",
      W("m", "5 × 4 = 20"), W("r", "4 ÷ 5 = 0.8"), W("a", "24 ÷ 5 = 4.8", "answer"), CIRC("a", "4.8")),
    B("Priya cycles at 4.8 kilometres an hour. Careful: 5, halfway between 6 and 4, is the tempting answer. But Suresh walks for longer than he jogs, so the true speed is a little under 5."),
    B("Check: 4.8 kilometres an hour, for 2 and a half hours, is 12 kilometres. There and back, exactly.",
      W("k", "4.8 × 2.5 = 12")),
    B("So one steady speed that matches a whole trip is the whole distance divided by the whole time."),
)

# Priya on the houseboat, Arjun on the road.
L[P + "7dad391b-e598-40db-bb55-7906d0be05d0"] = LESSON(
    B("A long story, so let's pick out what matters. The boat's trip back and Arjun's ride begin at the same moment. Whichever takes less time arrives first.",
      GIVEN("g1", "Boat: 12 km/hr for 1 h 30 min to the temple,"),
      GIVEN("g2", "then back the same way at 8 km/hr"),
      GIVEN("g3", "Arjun: 20 km by road at 10 km/hr")),
    B("Arjun is the easy one. Time is distance divided by speed, and 20 divided by 10 is 2. He takes 2 hours.",
      LB("f", TIME), W("ar", "20 ÷ 10 = 2")),
    B("For the boat's trip back we know the speed, 8. What else do we need?",
      ask=CHOOSE(["how long they stayed at the temple", "how far the temple is by river", "how fast Arjun cycles"], 1,
                 "Time is distance divided by speed. We have the speed, so the missing piece is the river distance to the temple.")),
    B("The trip out tells us. 12 kilometres an hour for 1 and a half hours: 12 for the hour and 6 more for the half hour. That is 18 kilometres.",
      W("d", "12 × 1.5 = 18")),
    B("Careful: the river route is 18 kilometres, but the road is 20. They are different lengths. The boat uses 18, and only Arjun uses 20.",
      UL("d", "18"), UL("g3", "20 km")),
    B("Boat back: 18 divided by 8. 8 goes into 18 twice, with 2 left over, and 2 out of 8 is a quarter. So 2 and a quarter hours.",
      W("bt", "18 ÷ 8 = 2.25"), HRS("bt", "2.25", "2¼ hours")),
    B("Arjun takes 2 hours and the boat takes 2 and a quarter. Arjun arrives first, by a quarter of an hour.",
      W("df", "2.25 − 2 = 0.25")),
    B("A quarter of an hour is a quarter of 60 minutes, which is 15 minutes. Arjun arrives first, by 15 minutes.",
      W("m", "0.25 × 60 = 15"), LB("a", "Arjun is first, by 15 minutes", "answer"), CIRC("a", "15 minutes")),
    B("Notice what we never needed: how long they spent at the temple. Both trips start together afterwards, so that time makes no difference."),
    B("So in a long story problem, find the two things being compared, give each its own distance and speed, and compare the times."),
)

# Ankit: train from Delhi to Agra, average speed.
L[P + "8d081413-2efb-49c7-b56e-22c5f7f76efb"] = LESSON(
    B("Ankit's train runs fast for an hour and then slower for half an hour. We want its average speed for the whole journey.",
      GIVEN("g1", "90 km/hr for 1 hour"),
      GIVEN("g2", "60 km/hr for 30 minutes")),
    B("Average speed is whole distance divided by whole time. First stretch: 90 kilometres an hour, for 1 hour, is 90 kilometres.",
      LB("f", AVG), W("d1", "90 × 1 = 90")),
    B("Second stretch: 60 kilometres an hour, but only for 30 minutes. How far does the train go?",
      ask=CHOOSE(["60 km", "30 km", "1800 km"], 1,
                 "60 kilometres an hour means 60 kilometres in a full hour. 30 minutes is half an hour, so the train covers half of that.")),
    B("Half of 60 is 30 kilometres. Careful: we multiply by a half, because the time has to be in hours, not minutes.",
      W("d2", "60 × 1/2 = 30")),
    B("Whole distance: 90 plus 30 is 120 kilometres. Whole time: 1 hour plus half an hour is 1 and a half hours.",
      W("d", "90 + 30 = 120"), W("t", "1 + 0.5 = 1.5")),
    B("So we want 120 divided by 1 and a half. Double both numbers to clear the half: 240 divided by 3, which is 80.",
      W("e", "120 ÷ 1.5 = 240 ÷ 3"), W("a", "240 ÷ 3 = 80", "answer"), CIRC("a", "= 80")),
    B("The average speed is 80 kilometres an hour."),
    B("Careful: halfway between 90 and 60 is 75, and that is one of the choices. But the train ran at 90 for twice as long as it ran at 60, so the average sits nearer to 90.",
      W("x", "(90 + 60) ÷ 2 = 75"), STRIKE("x", "(90 + 60) ÷ 2 = 75", "not the average speed")),
    B("Check: 80 kilometres an hour, for 1 and a half hours, is 80 plus half of 80, which is 120 kilometres. That is the distance we found.",
      W("k", "80 × 1.5 = 120")),
    B("So find the distance of each stretch, with the time in hours. Add the distances, add the times, and divide."),
)

# Kavya: Pune to a hill station, average speed.
L[P + "8e29fe73-a781-43bf-be05-6d8fc378eefd"] = LESSON(
    B("Kavya's family drive fast on the highway, then slowly up the mountain. We want the average speed for the whole journey.",
      GIVEN("g1", "60 km/hr for 2 hours"),
      GIVEN("g2", "30 km/hr for 1 hour")),
    B("The number halfway between 60 and 30 is 45. Before we work anything out: will the average speed be 45, more than 45, or less?",
      W("x", "(60 + 30) ÷ 2 = 45"),
      ask=CHOOSE(["exactly 45", "more than 45", "less than 45"], 1,
                 "They drive at 60 for 2 hours, but at 30 for only 1 hour. More of the trip is fast, so the average is pulled up above 45.")),
    B("Let's prove it. Average speed is the whole distance divided by the whole time.",
      STRIKE("x", "(60 + 30) ÷ 2 = 45", "not the average speed"), LB("f", AVG)),
    B("Distance is speed times time. Highway: 60 times 2 is 120 kilometres. Mountain road: 30 times 1 is 30 kilometres.",
      W("d1", "60 × 2 = 120"), W("d2", "30 × 1 = 30")),
    B("Whole distance: 120 plus 30 is 150 kilometres. Whole time: 2 hours plus 1 hour is 3 hours.",
      W("d", "120 + 30 = 150"), W("t", "2 + 1 = 3")),
    B("150 divided by 3 is 50. The average speed is 50 kilometres an hour, and yes, it is more than 45.",
      W("a", "150 ÷ 3 = 50", "answer"), CIRC("a", "= 50")),
    B("Here is another way to see it. List the speed for each hour of the trip: 60, 60, then 30. Add them and share by 3, and you get 50 again.",
      W("k", "(60 + 60 + 30) ÷ 3 = 50")),
    B("So average speed is whole distance divided by whole time. A speed kept up for longer counts for more."),
)
