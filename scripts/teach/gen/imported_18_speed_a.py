"""Time, distance and speed lessons for batch 18, written one by one (first half)."""
from imported_18_lib import ANS, ANSC, B, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, P, UL, W  # noqa: F401

LESSONS = {}

AVG = "Average speed = total distance ÷ total time"

# Once round a 400 m by 200 m park at 3 km/hr: how many minutes?
LESSONS[P + "9abd6007-86c6-467f-b518-630d3c6e25fb"] = LESSON(
    B("Ravi and his grandfather walk once round a park that is 400 metres long and 200 metres wide, at 3 kilometres an hour. We want the time in minutes.",
      GIVEN("q", "Park 400 m by 200 m, speed 3 km/hr, time in minutes?")),
    B("One full round means walking along the boundary. So what do we find first?",
      ask=CHOOSE(["400 × 200, the area", "2 × (400 + 200), the perimeter", "400 + 200"], 1,
                 "Walking round the park means going along all 4 sides. Two sides are 400 metres and two are 200 metres, so we need the perimeter.")),
    B("One long side and one short side make 400 plus 200, which is 600. There are two of each, so 2 times 600 is 1200. One round is 1200 metres.",
      W("l1", "400 + 200 = 600"), W("l2", "2 × 600 = 1200"), NOTE("l2", "1200", "metres")),
    B("Now the trap. The distance is in metres, but the speed is in kilometres an hour. Before we divide, the units have to match.",
      UL("q", "3 km/hr")),
    B("3 kilometres is 3000 metres, and an hour is 60 minutes. So they walk 3000 metres in 60 minutes.",
      LB("l3", "3 km in 1 hr = 3000 m in 60 min")),
    B("How many metres do they walk in just 1 minute?",
      ask=CHOOSE(["3000 ÷ 60", "3000 × 60", "60 ÷ 3"], 0,
                 "The 3000 metres are spread equally over 60 minutes. So we share 3000 by 60 to find the metres in one minute.")),
    B("3000 divided by 60 is 50. They walk 50 metres every minute.",
      W("l4", "3000 ÷ 60 = 50")),
    B("So how many minutes for 1200 metres? 1200 divided by 50 is 24. One round takes 24 minutes.",
      *ANSC("l5", "1200 ÷ 50 = 24", 24)),
    B("Check: 24 minutes at 50 metres a minute is 24 times 50, which is 1200 metres. That is exactly one round.",
      W("l6", "24 × 50 = 1200")),
    B("So the plan is: find the distance, make the units match, and then time is distance divided by speed."),
)

# Train 7:30 AM to 12:30 PM: 60 km/hr for 2 hr, 30 min stop, then 90 km/hr. Total distance?
LESSONS[P + "9f8bd7db-3343-405c-b559-a286aa6f9dcb"] = LESSON(
    B("A train leaves at 7:30 in the morning and arrives at 12:30. It runs at 60 kilometres an hour for 2 hours, stops for 30 minutes, then runs at 90 kilometres an hour. How far is the whole trip?",
      GIVEN("q", "7:30 to 12:30: 60 km/hr for 2 hr, stop 30 min, 90 km/hr")),
    B("The first part is ready to go. 60 kilometres an hour for 2 hours is 60 times 2, which is 120 kilometres.",
      W("l1", "60 × 2 = 120")),
    B("For the second part we know the speed, 90, but not the time. So first: how long is the whole trip, from 7:30 to 12:30?",
      ask=CHOOSE(["4 hours", "5 hours", "5 hours 30 minutes"], 1,
                 "The minutes are the same at both ends, so just count the hours from 7 up to 12. That is 5 hours.")),
    B("The whole trip is 5 hours. Take away the 2 hours of the first part, and the half hour at the station. 5 minus 2 minus a half leaves 2.5 hours, that is 2 and a half hours.",
      W("l2", "5 − 2 − 0.5 = 2.5")),
    B("Careful here: the 30 minutes at the station use up time, but the train covers no distance while it stands still.",
      UL("q", "stop 30 min")),
    B("Now the second part: 90 kilometres an hour for 2.5 hours. How do we find its distance?",
      ask=CHOOSE(["90 × 2.5", "90 ÷ 2.5", "90 × 5"], 0,
                 "Distance is speed times time. The speed is 90, and the time for this part is 2.5 hours, not the whole 5.")),
    B("2 hours at 90 is 180 kilometres. The extra half hour adds half of 90, which is 45. So the second part is 225 kilometres.",
      W("l3", "90 × 2 = 180"), W("l4", "90 × 0.5 = 45"), W("l5", "180 + 45 = 225")),
    B("Add the two parts. 120 plus 225 is 345. The whole trip is 345 kilometres.",
      *ANSC("l6", "120 + 225 = 345", 345)),
    B("Check the time: 2 hours, plus half an hour, plus 2.5 hours makes 5 hours, from 7:30 to 12:30. It fits.",
      W("l7", "2 + 0.5 + 2.5 = 5")),
    B("So when a trip comes in parts: find the time for each part, use speed times time for each distance, then add the distances."),
)

# Neha (5 m/s) and Kavitha (3 m/s) run towards each other on 600 m; Neha runs back at 4 m/s.
LESSONS[P + "9fab80d7-4e4f-464f-bccd-3901d2bbe536"] = LESSON(
    B("Neha and Kavitha run towards each other from the two ends of a 600 metre track. Neha runs 5 metres a second and Kavitha 3. When they meet, Neha turns and runs back to her start at 4 metres a second.",
      GIVEN("q", "600 m track: Neha 5 m/s, Kavitha 3 m/s; Neha back at 4 m/s")),
    B("There are two stretches of time to find: the time until they meet, and the time Neha takes to run back. Then we add them."),
    B("Each second, Neha covers 5 metres and Kavitha covers 3. By how much does the gap between them shrink each second?",
      ask=CHOOSE(["5 + 3 = 8 metres", "5 − 3 = 2 metres", "5 × 3 = 15 metres"], 0,
                 "They run towards each other, so both of them eat into the gap. Neha takes 5 metres off it and Kavitha takes 3, so it shrinks by 8 metres each second.")),
    B("The gap starts at 600 metres and shrinks by 8 metres a second. 600 divided by 8 is 75, so they meet after 75 seconds.",
      W("l1", "5 + 3 = 8"), W("l2", "600 ÷ 8 = 75")),
    B("How far has Neha run by then? 5 metres a second for 75 seconds is 5 times 75, which is 375 metres.",
      W("l3", "5 × 75 = 375")),
    B("Now she turns and runs back to her start. How far does she have to run?",
      ask=CHOOSE(["600 metres", "375 metres", "225 metres"], 1,
                 "She goes back the way she came. She is 375 metres from her starting point, so that is how far she runs back.")),
    B("375 metres at 4 metres a second means 375 divided by 4. Half of 375 is 187.5, and half of that is 93.75. The run back takes 93.75 seconds.",
      W("l4", "375 ÷ 2 = 187.5"), W("l5", "187.5 ÷ 2 = 93.75")),
    B("Add the two times. 75 plus 93.75 is 168.75 seconds.",
      *ANSC("l6", "75 + 93.75 = 168.75", "168.75")),
    B("The trap is stopping at 75 seconds. That is only when the girls meet. The question asks for the time until Neha is back where she started."),
    B("Check the run back: 93.75 seconds at 4 metres a second is 375 metres, exactly as far as she ran out.",
      W("l7", "93.75 × 4 = 375")),
    B("So when two runners come towards each other, add their speeds to see how fast the gap closes. Then take the story one stretch at a time."),
)

# Train 120 km at 60, 80 km at 40, 100 km at 50; bus does the 300 km in the same time.
LESSONS[P + "a6765258-aa69-4276-8490-060e8e11c0d8"] = LESSON(
    B("Priya's train covers 120 kilometres at 60 kilometres an hour, then 80 at 40, then 100 at 50. Deepa's bus does the whole 300 kilometres at one steady speed and arrives at exactly the same time.",
      GIVEN("q", "Train: 120 km at 60, 80 km at 40, 100 km at 50. Bus: 300 km")),
    B("For the bus's speed we need its distance, 300, and its time. Where will the time come from?",
      ask=CHOOSE(["add 60, 40 and 50", "add the train's three times", "300 ÷ 3"], 1,
                 "Both arrive at the same moment, so the bus takes exactly as long as the train. So we find the train's time for each part and add them up.")),
    B("Time is distance divided by speed. First part: 120 divided by 60 is 2 hours.",
      W("l1", "120 ÷ 60 = 2")),
    B("Second part: 80 divided by 40 is 2 hours. Third part: 100 divided by 50 is 2 hours as well.",
      W("l2", "80 ÷ 40 = 2"), W("l3", "100 ÷ 50 = 2")),
    B("So the train takes 2 plus 2 plus 2, which is 6 hours. The bus takes 6 hours too.",
      W("l4", "2 + 2 + 2 = 6")),
    B("The bus covers 300 kilometres in 6 hours. 300 divided by 6 is 50, so the bus travels at 50 kilometres an hour.",
      *ANSC("l5", "300 ÷ 6 = 50", 50)),
    B("A word of warning. Never find a steady speed by just mixing the speeds 60, 40 and 50 together. Always use the whole distance divided by the whole time."),
    B("Check: 50 kilometres an hour for 6 hours is 50 times 6, which is 300 kilometres. It fits.",
      W("l6", "50 × 6 = 300")),
    B("So: arriving together means taking the same time. Find the total time, and then speed is distance divided by time."),
)

# 24 km at 12 km/hr, back at 8 km/hr: average speed.
LESSONS[P + "a7714f4e-8b4a-40fd-945e-db3b1a1ec170"] = LESSON(
    B("Priya cycles 24 kilometres to the library at 12 kilometres an hour, and comes back the same way at 8 kilometres an hour. We want her average speed for the whole trip.",
      GIVEN("q", "24 km there at 12 km/hr, 24 km back at 8 km/hr")),
    B("What do we work out to get an average speed?",
      ask=CHOOSE(["(12 + 8) ÷ 2", "total distance ÷ total time", "12 − 8"], 1,
                 "It is tempting to take the number halfway between 12 and 8. But she spends longer riding at the slow speed, so we need the whole distance divided by the whole time.")),
    B("Average speed is the whole distance divided by the whole time. The whole distance is there and back: 24 plus 24 is 48 kilometres.",
      LB("f", AVG), W("l1", "24 + 24 = 48")),
    B("Going: 24 kilometres at 12 an hour takes 24 divided by 12, which is 2 hours.",
      W("l2", "24 ÷ 12 = 2")),
    B("Coming back: 24 divided by 8 is 3 hours. Slower, so it takes longer.",
      W("l3", "24 ÷ 8 = 3")),
    B("The whole time is 2 plus 3, which is 5 hours.",
      W("l4", "2 + 3 = 5")),
    B("Now 48 kilometres in 5 hours. 48 divided by 5 is 9.6, so her average speed is 9.6 kilometres an hour.",
      *ANSC("l5", "48 ÷ 5 = 9.6", "9.6")),
    B("See the trap? Halfway between 12 and 8 is 10, but the true answer is a little less. She rides at 8 for 3 hours and at 12 for only 2, so the slow speed pulls the average down."),
    B("Check: 9.6 times 5 is 48, the whole distance.",
      W("l6", "9.6 × 5 = 48")),
    B("So for an average speed, never average the speeds. Add up the distances, add up the times, and divide."),
)

# Train leaves 6:15 AM: 120 km at 60, 30 min stop, 240 km at 80. Arrival time?
LESSONS[P + "b1cb3843-2972-4747-99e6-6cf02d5cd394"] = LESSON(
    B("Deepak's train leaves at 6:15 in the morning. It covers 120 kilometres at 60 kilometres an hour, stops for 30 minutes, then covers 240 kilometres at 80 kilometres an hour. When does it arrive?",
      GIVEN("q", "Leaves 6:15 AM: 120 km at 60, stop 30 min, 240 km at 80")),
    B("The arrival time is the leaving time plus all the time that passes. There are three pieces of time: the first run, the stop, and the second run."),
    B("First run: 120 kilometres at 60 an hour. Time is distance divided by speed, and 120 divided by 60 is 2 hours.",
      W("l1", "120 ÷ 60 = 2")),
    B("Second run: 240 kilometres at 80 an hour. 240 divided by 80 is 3 hours.",
      W("l2", "240 ÷ 80 = 3")),
    B("So how much time passes altogether, from leaving to arriving?",
      ask=CHOOSE(["5 hours", "5 hours 30 minutes", "6 hours"], 1,
                 "2 hours and 3 hours of running make 5 hours. But the clock keeps ticking during the 30 minute stop, so that goes in as well.")),
    B("2 hours, plus 3 hours, plus the 30 minute stop: that is 5 hours 30 minutes in all. Leaving out the stop is the classic slip here.",
      LB("l3", "2 hr + 3 hr + 30 min = 5 hr 30 min"), UL("l3", "30 min")),
    B("Now add that to 6:15. First the 5 hours: 6:15 becomes 11:15.",
      LB("l4", "6:15 AM + 5 hr = 11:15 AM")),
    B("Then the 30 minutes: 15 plus 30 is 45. So the train arrives at 11:45 in the morning.",
      LB("l5", "11:15 AM + 30 min = 11:45 AM", "answer"), CIRC("l5", "11:45 AM")),
    B("Check by going backwards. From 11:45, take off 30 minutes to reach 11:15, then take off 5 hours to reach 6:15. That is when the train left."),
    B("So for an arrival time: find each running time with distance divided by speed, add any stops, then add the total to the starting time."),
)

# 6 km at 12 km/hr, then 4 km at 8 km/hr: average speed.
LESSONS[P + "b8e871d8-1266-48e3-a10a-c218966ff709"] = LESSON(
    B("Farhan rides 6 kilometres at 12 kilometres an hour, then 4 kilometres at 8 kilometres an hour. We want his average speed for the whole delivery trip.",
      GIVEN("q", "6 km at 12 km/hr, then 4 km at 8 km/hr")),
    B("What two things do we need for an average speed?",
      ask=CHOOSE(["the two speeds added: 12 + 8", "total distance and total time", "only the two distances"], 1,
                 "Average speed is how far you went altogether, divided by how long it took altogether. So we need the whole distance and the whole time.")),
    B("The whole distance is 6 plus 4, which is 10 kilometres.",
      LB("f", AVG), W("l1", "6 + 4 = 10")),
    B("Time for the first ride: 6 kilometres at 12 an hour. 6 is half of 12, so it takes half an hour.",
      W("l2", "6 ÷ 12 = 1/2")),
    B("Second ride: 4 kilometres at 8 an hour. 4 is half of 8, so that is half an hour too.",
      W("l3", "4 ÷ 8 = 1/2")),
    B("Two half hours make 1 whole hour.",
      W("l4", "1/2 + 1/2 = 1")),
    B("10 kilometres in 1 hour. So his average speed is 10 kilometres an hour.",
      *ANSC("l5", "10 ÷ 1 = 10", 10)),
    B("Here the answer happens to sit halfway between 12 and 8. That only works because he rode for the same time at each speed. It is not a rule you can trust."),
    B("Check: half an hour at 12 is 6 kilometres, and half an hour at 8 is 4 kilometres. That matches the story.",
      W("l6", "12 × 1/2 = 6"), W("l7", "8 × 1/2 = 4")),
    B("So for an average speed: add up the distances, add up the times, and divide the first by the second."),
)

# Downstream 18 km/hr for 40 min; back at 12 km/hr: minutes for the return.
LESSONS[P + "bfca9ba2-08fe-452f-8f60-22e5cfdf8a40"] = LESSON(
    B("Ravi's boat goes downstream at 18 kilometres an hour for 40 minutes to reach a temple. It comes back the same way at 12 kilometres an hour. How many minutes does the trip back take?",
      GIVEN("q", "There: 18 km/hr for 40 min. Back: 12 km/hr, time?")),
    B("We want the time for the trip back, and we know its speed. What else do we need?",
      ask=CHOOSE(["the speed of the current", "the distance to the temple", "the 40 minutes again"], 1,
                 "Time is distance divided by speed. We have the speed coming back, so the missing piece is how far away the temple is.")),
    B("The trip there tells us the distance. An hour is 60 minutes, so 40 minutes is 40 out of 60, which is 2 thirds of an hour.",
      W("l1", "40/60 = 2/3")),
    B("18 kilometres an hour for 2 thirds of an hour. A third of 18 is 6, so 2 thirds is 12. The temple is 12 kilometres away.",
      W("l2", "18 × 2/3 = 12"), NOTE("l2", "12", "km to the temple")),
    B("Coming back, it is the same 12 kilometres, now at 12 kilometres an hour. 12 divided by 12 is 1, so the trip back takes 1 hour.",
      W("l3", "12 ÷ 12 = 1")),
    B("Careful: the question asks for minutes, not hours. 1 hour is 60 minutes.",
      *ANSC("l4", "1 × 60 = 60", 60)),
    B("Notice the trip back is longer than the 40 minutes going. Same distance, slower boat, more time. So 40 minutes could never be the answer."),
    B("Check: 12 kilometres an hour for 1 whole hour is 12 kilometres, exactly the distance to the temple.",
      W("l5", "12 × 1 = 12")),
    B("So for a there and back trip: use the first leg to find the distance, then divide that distance by the speed coming back."),
)
