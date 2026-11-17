"""Time, distance and speed lessons for batch 18 (second half): two builders for
questions that share a structure, and the rest written one by one."""
from imported_18_lib import ANS, ANSC, B, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, P, UL, W, last_nth  # noqa: F401

LESSONS = {}

AVG = "Average speed = total distance ÷ total time"


def num(x):
    """A number as it is written on the board: 3, 4.5, 7.5."""
    return ("%g" % x)


# ── A drive with a break: total distance, first stretch by time, the rest by speed ──

def avg_break(intro, given, D, v1, t1, v2, break_name, t2_say, t2_ops, final_say, final_ops, people):
    d1 = v1 * t1
    rest = D - d1
    t2 = rest / v2
    T = t1 + t2
    A = D / T
    assert A == int(A) and d1 == int(d1)
    A = int(A)
    final_line = "%d ÷ %s = %d" % (D, num(T), A)
    return LESSON(
        B(intro, GIVEN("q", given)),
        B("Average speed is the whole distance divided by the whole driving time. We know the distance, %d kilometres. So the real job is to find the time." % D,
          LB("f", AVG)),
        B("First stretch: %d kilometres an hour for %d hours is %d times %d, which is %d kilometres." % (v1, t1, v1, t1, d1),
          W("l1", "%d × %d = %d" % (v1, t1, d1))),
        B("How far is left for the second stretch?",
          ask=CHOOSE(["%d + %d" % (D, d1), "%d − %d" % (D, d1), "%d − %d" % (D, v1)], 1,
                     "The whole trip is %d kilometres, and %s have done %d of them already. Take those away to see what is left." % (D, people, d1))),
        B("%d minus %d is %d. So %d kilometres are still to go." % (D, d1, rest, rest),
          W("l2", "%d − %d = %d" % (D, d1, rest))),
        B(t2_say, *t2_ops),
        B("Now, which times go into the whole driving time?",
          ask=CHOOSE(["%d + %s + 0.5" % (t1, num(t2)), "%d + %s" % (t1, num(t2)), "only %s" % num(t2)], 1,
                     "The question tells us to leave the %s out. So we count only the hours spent driving: %d hours and then %s hours." % (break_name, t1, num(t2)))),
        B("%d plus %s is %s hours of driving. The %s is not in there, just as the question asked." % (t1, num(t2), num(T), break_name),
          W("l4", "%d + %s = %s" % (t1, num(t2), num(T)))),
        B(final_say, *(final_ops + [ANS("l5", final_line), CIRC("l5", str(A), last_nth(final_line, str(A)))])),
        B("Check: %d kilometres an hour for %s hours is %d times %s, which is %d kilometres. That is the whole trip." % (A, num(T), A, num(T), D),
          W("l6", "%d × %s = %d" % (A, num(T), D))),
        B("So: average speed is the whole distance over the whole time. Never just average the two speeds, and read carefully whether a break counts."),
    )


# Pune to Goa, 450 km: 75 km/hr for 3 hr, chai break, the rest at 50 km/hr.
LESSONS[P + "a954701c-ebae-486b-be8d-2cf78ac8a526"] = avg_break(
    "Neha's family drive 450 kilometres from Pune to Goa. They do 75 kilometres an hour for the first 3 hours, stop 30 minutes for chai, then drive the rest at 50 kilometres an hour. We want the average speed, leaving the break out.",
    "450 km: 75 km/hr for 3 hr, break 30 min, rest at 50 km/hr",
    450, 75, 3, 50, "chai break",
    "225 kilometres at 50 an hour takes 225 divided by 50. Double both numbers to make it friendlier: 450 divided by 100, which is 4.5. So 4 and a half hours.",
    [W("l3", "225 ÷ 50 = 4.5"), NOTE("l3", "225 ÷ 50", "450 ÷ 100")],
    "450 kilometres in 7.5 hours. Double both again: 900 divided by 15, and that is 60. The average speed is 60 kilometres an hour.",
    [W("l4b", "900 ÷ 15 = 60")],
    "they",
)

# Jaipur to Udaipur, 420 km: 60 km/hr for 3 hr, lunch, the rest at 80 km/hr.
LESSONS[P + "e6a88dda-9aac-4665-aedd-a8eb5d429699"] = avg_break(
    "Kavya and her mother drive 420 kilometres from Jaipur to Udaipur. They do 60 kilometres an hour for the first 3 hours, stop 30 minutes for lunch, then drive the rest at 80 kilometres an hour. We want the average speed, leaving lunch out.",
    "420 km: 60 km/hr for 3 hr, lunch 30 min, rest at 80 km/hr",
    420, 60, 3, 80, "lunch break",
    "240 kilometres at 80 an hour takes 240 divided by 80, which is 3 hours.",
    [W("l3", "240 ÷ 80 = 3")],
    "420 kilometres in 6 hours. 420 divided by 6 is 70, so the average speed is 70 kilometres an hour.",
    [],
    "they",
)


# ── Several stretches, each a speed in km/hr for some minutes: total distance ──

FRACS = {
    40: (2, 3, "2 thirds", "2 thirds of an hour"),
    30: (1, 2, "half", "half an hour"),
    20: (1, 3, "a third", "a third of an hour"),
    10: (1, 6, "a sixth", "a sixth of an hour"),
}
ORD = ["First", "Second", "Third"]


def minute_parts(intro, given, parts, ending):
    """parts: [(speed, minutes)]."""
    dists = []
    for v, m in parts:
        n, d, _, _ = FRACS[m]
        assert (v * n) % d == 0
        dists.append(v * n // d)
    total = sum(dists)
    beats = [
        B(intro, GIVEN("q", given)),
        B("The speeds are in kilometres an hour, but the times are in minutes. What should we do with the minutes first?",
          ask=CHOOSE(["multiply them by the speeds", "turn them into parts of an hour", "add them all up"], 1,
                     "A speed in kilometres an hour tells us what happens in one whole hour. So each time has to be written as a part of an hour before we multiply.")),
    ]
    # The minutes as parts of an hour.
    seen = []
    for _, m in parts:
        if m not in seen:
            seen.append(m)
    bits = []
    ops = []
    for i, m in enumerate(seen):
        n, d, _, long = FRACS[m]
        ops.append(W("f%d" % i, "%d/60 = %d/%d" % (m, n, d)))
        if i == 0:
            bits.append("%d minutes is %d out of 60, which is %s" % (m, m, long))
        else:
            bits.append("%d minutes is %s" % (m, long))
    if len(bits) == 1:
        say = "An hour is 60 minutes. So %s. Both stretches last that long." % bits[0]
    elif len(bits) == 2:
        say = "An hour is 60 minutes. So %s. And %s." % (bits[0], bits[1])
    else:
        say = "An hour is 60 minutes. So %s. Then %s, and %s." % (bits[0], bits[1], bits[2])
    beats.append(B(say, *ops))

    for i, (v, m) in enumerate(parts):
        n, d, short, long = FRACS[m]
        dist = dists[i]
        line = W("l%d" % (i + 1), "%d × %d/%d = %d" % (v, n, d, dist))
        last = i == len(parts) - 1
        if last:
            beats.append(B("%s stretch: %d kilometres an hour for %s. How far is that?" % ("Last" if len(parts) > 2 else ORD[i], v, long),
                           ask=CHOOSE(["%d km" % (v * d), "%d km" % v, "%d km" % dist], 2,
                                      "%s is less than a whole hour, so the distance must be less than %d kilometres. Share %d into %d equal parts." % (
                                          long.capitalize(), v, v, d))))
            beats.append(B("%s of %d is %d. So that stretch is %d kilometres." % (short.capitalize(), v, dist, dist), line))
        elif n == 1:
            beats.append(B("%s stretch: %d kilometres an hour for %s. %s of %d is %d, so that is %d kilometres." % (
                ORD[i], v, long, short.capitalize(), v, dist, dist), line))
        else:
            third = v // d
            beats.append(B("%s stretch: %d kilometres an hour for %s. A third of %d is %d, so %s is %d kilometres." % (
                ORD[i], v, long, v, third, short, dist), line, NOTE("l%d" % (i + 1), "%d/%d" % (n, d), "%d ÷ %d = %d" % (v, d, third))))

    sum_line = " + ".join(str(x) for x in dists) + " = %d" % total
    beats.append(B("Now add the stretches. %s is %d. %s" % (" plus ".join(str(x) for x in dists), total, ending),
                   ANS("t", sum_line), CIRC("t", str(total), last_nth(sum_line, str(total)))))
    v, m = parts[-1]
    n, d, short, long = FRACS[m]
    beats.append(B("Check the last stretch another way. %d minutes fits into an hour %d times, and %d times %d is %d, the speed we were given." % (
        m, d, d, dists[-1], v), W("c", "%d × %d = %d" % (d, dists[-1], v))))
    beats.append(B("The trap in this kind of question is multiplying a speed by the minutes as they stand. Kilometres an hour needs hours."))
    beats.append(B("So when the time is in minutes and the speed is for an hour: turn the minutes into a part of an hour, multiply, then add the stretches."))
    return LESSON(*beats)


LESSONS[P + "b30339a8-4dda-4ae6-bd0f-f5558340ce4e"] = minute_parts(
    "Aarav's train runs at 90 kilometres an hour for 40 minutes, then 60 kilometres an hour for 30 minutes, then 120 kilometres an hour for 20 minutes. How far does it go altogether?",
    "90 km/hr 40 min, then 60 km/hr 30 min, 120 km/hr 20 min",
    [(90, 40), (60, 30), (120, 20)],
    "The train covers 130 kilometres.")

LESSONS[P + "e5f256fe-aa46-48e5-bdb7-1a6b0085e7db"] = minute_parts(
    "Rohan's auto goes at 15 kilometres an hour for 20 minutes through the lanes, then at 30 kilometres an hour for 30 minutes on the main road. How far is the station from his house?",
    "15 km/hr for 20 min, then 30 km/hr for 30 min",
    [(15, 20), (30, 30)],
    "The station is 20 kilometres from Rohan's house.")

LESSONS[P + "f2d37300-cb9d-44ee-9f66-16bb5fe2098b"] = minute_parts(
    "Ananya's father drives at 30 kilometres an hour for the first 10 minutes, then at 60 kilometres an hour for the next 10 minutes. How far is the school from her home?",
    "30 km/hr for 10 min, then 60 km/hr for 10 min",
    [(30, 10), (60, 10)],
    "The school is 15 kilometres from Ananya's home.")


# ── Written one by one ──

# 360 km in 5 hr, part at 90 km/hr and the rest at 60 km/hr: km at the slower speed.
LESSONS[P + "cabecb79-a128-4dda-b5ee-2d5c24c3f7f8"] = LESSON(
    B("Rohan's train covers 360 kilometres in 5 hours. It runs at 90 kilometres an hour at first, then slows to 60 kilometres an hour for the rest. How many kilometres does it do at the slower speed?",
      GIVEN("q", "360 km in 5 hr: part at 90 km/hr, the rest at 60 km/hr")),
    B("We don't know how long the train spent at each speed. So let's try a pretend trip: what if it had kept to 90 for the whole 5 hours?"),
    B("5 hours at 90 would be 5 times 90, which is 450 kilometres.",
      W("l1", "5 × 90 = 450")),
    B("But the real trip is only 360. The pretend trip is too long by 450 minus 360, which is 90 kilometres.",
      W("l2", "450 − 360 = 90")),
    B("Every hour the train goes at 60 when we pretended 90, how many kilometres does it lose?",
      ask=CHOOSE(["60", "30", "150"], 1,
                 "In one hour at 90 it would cover 90 kilometres. At 60 it covers only 60. The gap between those two is what each slow hour loses.")),
    B("90 minus 60 is 30. Every slow hour loses 30 kilometres.",
      W("l3", "90 − 60 = 30")),
    B("We have 90 kilometres to lose, 30 at a time. 90 divided by 30 is 3, so the train spent 3 hours at the slower speed.",
      W("l4", "90 ÷ 30 = 3"), NOTE("l4", "3", "slow hours")),
    B("3 hours at 60 kilometres an hour is 3 times 60, which is 180 kilometres at the slower speed.",
      *ANSC("l5", "3 × 60 = 180", 180)),
    B("Careful: the 3 is hours, and the question asks for kilometres. That is why we needed one more step."),
    B("Check: the other 2 hours were at 90, which is 180 kilometres as well. 180 plus 180 is 360, the whole trip.",
      W("l6", "2 × 90 = 180"), W("l7", "180 + 180 = 360")),
    B("So when you know the total but not the split: pretend it was all one speed, see how far off you are, and put it right one hour at a time."),
)

# Round a 600 m track in opposite directions at 5 m/s and 3 m/s: the third meeting.
LESSONS[P + "cd0b4e43-222d-47fc-9a45-b4631c319a09"] = LESSON(
    B("Priya and Kiran start from the same point on a 600 metre round track and run in opposite directions. Priya runs 5 metres a second and Kiran 3. When do they meet for the third time?",
      GIVEN("q", "600 m round track, opposite ways: 5 m/s and 3 m/s")),
    B("They set off in opposite directions, so they come round to meet on the far side. Between them, they must cover one whole lap of 600 metres before they meet."),
    B("Each second, how many metres do the two of them cover between them?",
      ask=CHOOSE(["5 − 3 = 2", "5 + 3 = 8", "5 × 3 = 15"], 1,
                 "Priya covers 5 metres of the lap, and Kiran covers 3 metres of it from the other side. Together that uses up 8 metres of the lap every second.")),
    B("Together they cover 8 metres a second. 600 divided by 8 is 75, so they first meet after 75 seconds.",
      W("l1", "5 + 3 = 8"), W("l2", "600 ÷ 8 = 75")),
    B("They pass each other and keep running. When do they meet again?",
      ask=CHOOSE(["after another 75 seconds", "after another 600 seconds", "never again"], 0,
                 "From the moment they pass, it is the same story again: side by side, heading opposite ways, with one whole lap to cover between them. That takes 75 seconds again.")),
    B("So they meet every 75 seconds. The first meeting is at 75 seconds, and the second is at 150.",
      W("l3", "75 + 75 = 150")),
    B("The third meeting is 75 seconds later still. 3 times 75 is 225 seconds.",
      *ANSC("l4", "3 × 75 = 225", 225)),
    B("The trap is stopping at 75. That is the first meeting, and the question asks for the third."),
    B("Check: in 225 seconds Priya runs 1125 metres and Kiran runs 675. Together that is 1800 metres, which is exactly 3 laps of 600.",
      W("l5", "5 × 225 = 1125"), W("l6", "3 × 225 = 675"), W("l7", "1125 + 675 = 1800"), W("l8", "3 × 600 = 1800")),
    B("So on a round track, running opposite ways: add the speeds, find the time for one lap between you, and count one meeting for each lap."),
)

# 150 km: 60 km at 40, chai 30 min, 60 km at 60, 30 km at 15. Average speed with the stop.
LESSONS[P + "e0aab10d-53f6-4e15-b3c9-090d5246eaa3"] = LESSON(
    B("Rohan and his dad drive 150 kilometres. They do 60 kilometres at 40 kilometres an hour, stop 30 minutes for chai, do 60 kilometres at 60, and the last 30 kilometres at 15. We want the average speed, with the stop counted.",
      GIVEN("q", "150 km: 60 at 40, stop 30 min, 60 at 60, 30 at 15")),
    B("Average speed is the whole distance divided by the whole time. The distance is 150 kilometres. So we need every piece of time.",
      LB("f", AVG)),
    B("First stretch: 60 kilometres at 40 an hour. 60 divided by 40 is 1.5, so one and a half hours.",
      W("l1", "60 ÷ 40 = 1.5")),
    B("Second stretch: 60 kilometres at 60 an hour takes 1 hour. Last stretch: 30 kilometres at 15 an hour takes 2 hours.",
      W("l2", "60 ÷ 60 = 1"), W("l3", "30 ÷ 15 = 2")),
    B("The question says to include the chai stop. So which sum gives the whole time?",
      ask=CHOOSE(["1.5 + 1 + 2", "1.5 + 0.5 + 1 + 2", "1.5 + 30 + 1 + 2"], 1,
                 "This time the stop counts. And the stop is 30 minutes, which is half an hour, so it goes in as 0.5, in hours like all the others.")),
    B("1.5 plus 0.5 is 2. Add 1 to get 3, and add 2 to get 5. The whole journey takes 5 hours.",
      W("l4", "1.5 + 0.5 + 1 + 2 = 5"), UL("l4", "0.5"), NOTE("l4", "0.5", "chai stop")),
    B("150 kilometres in 5 hours. 150 divided by 5 is 30, so the average speed is 30 kilometres an hour.",
      *ANSC("l5", "150 ÷ 5 = 30", 30)),
    B("Two traps here. One is forgetting the stop. The other is adding the 30 minutes as if it were 30 hours. Keep every time in hours."),
    B("Check: 30 kilometres an hour for 5 hours is 30 times 5, which is 150 kilometres. It fits.",
      W("l6", "30 × 5 = 150")),
    B("So for an average speed: add up every piece of time the question tells you to count, then divide the whole distance by it."),
)

# Walk at 4 km/hr, auto back at 20 km/hr, 3 hours in all: how far is the market?
LESSONS[P + "eae4d773-e97d-467f-91eb-84abe609cb03"] = LESSON(
    B("Meera walks to the market at 4 kilometres an hour and comes home by auto at 20 kilometres an hour. The round trip takes 3 hours. How far away is the market?",
      GIVEN("q", "Walk there at 4 km/hr, auto back at 20 km/hr, 3 hr in all")),
    B("We don't know the distance. So let's think about just 1 kilometre of the road, and ask how long that 1 kilometre takes each way."),
    B("Walking: 4 kilometres take an hour, which is 60 minutes. So 1 kilometre takes 60 divided by 4, which is 15 minutes.",
      W("l1", "60 ÷ 4 = 15")),
    B("By auto, 20 kilometres take 60 minutes. How long does 1 kilometre take?",
      ask=CHOOSE(["20 minutes", "3 minutes", "80 minutes"], 1,
                 "Share the 60 minutes equally over the 20 kilometres. 60 divided by 20 gives the minutes for each one.")),
    B("60 divided by 20 is 3 minutes. So every kilometre of road costs her 15 minutes going and 3 minutes coming back: 18 minutes in all.",
      W("l2", "60 ÷ 20 = 3"), W("l3", "15 + 3 = 18")),
    B("The whole trip took 3 hours. In minutes, that is 3 times 60, which is 180 minutes.",
      W("l4", "3 × 60 = 180")),
    B("How many lots of 18 minutes fit into 180? 180 divided by 18 is 10. So the market is 10 kilometres away.",
      *ANSC("l5", "180 ÷ 18 = 10", 10)),
    B("Check: walking 10 kilometres at 4 an hour takes 2.5 hours. The auto does 10 kilometres at 20 an hour in half an hour. 2.5 plus 0.5 is 3 hours.",
      W("l6", "10 ÷ 4 = 2.5"), W("l7", "10 ÷ 20 = 0.5"), W("l8", "2.5 + 0.5 = 3")),
    B("Notice the trap: she does not spend half the time each way. The walk takes most of the 3 hours, because walking is so much slower."),
    B("So when the distance is unknown: find the time for 1 kilometre there and back, then see how many of those fit into the total time."),
)

# Houseboat 12 km/hr for 1 hr 30 min; Arjun cycles the same distance in 1 hr 12 min.
LESSONS[P + "ec5a09e1-2ca2-4258-8914-651929f1dfb6"] = LESSON(
    B("A houseboat goes downstream at 12 kilometres an hour for 1 hour 30 minutes to reach a temple. Arjun cycles the same one-way distance in 1 hour 12 minutes. What is Arjun's speed?",
      GIVEN("q", "Boat: 12 km/hr for 1 hr 30 min. Arjun: 1 hr 12 min")),
    B("Arjun's speed needs his distance and his time. We have his time. Where does the distance come from?",
      ask=CHOOSE(["the boat's trip back at 6", "the boat's trip downstream", "it cannot be found"], 1,
                 "Arjun covers the same one-way distance as the boat. For the trip downstream we know both the speed and the time, so that trip gives us the distance.")),
    B("The boat does 12 kilometres an hour for one and a half hours. The hour gives 12 kilometres, and the half hour gives 6 more. 12 plus 6 is 18 kilometres.",
      W("l1", "12 + 6 = 18"), NOTE("l1", "18", "km one way")),
    B("The trip back upstream at 6 kilometres an hour is only there to distract us. Arjun's ride has nothing to do with it."),
    B("Arjun takes 1 hour 12 minutes. In minutes, that is 60 plus 12, which is 72 minutes for the 18 kilometres.",
      W("l2", "60 + 12 = 72")),
    B("72 minutes for 18 kilometres. How many minutes for each kilometre?",
      ask=CHOOSE(["54", "4", "90"], 1,
                 "Share the 72 minutes equally over the 18 kilometres. 72 divided by 18 tells us the minutes for one kilometre.")),
    B("72 divided by 18 is 4. He needs 4 minutes for every kilometre.",
      W("l3", "72 ÷ 18 = 4")),
    B("An hour has 60 minutes, and 60 divided by 4 is 15. So in one hour he rides 15 kilometres. His speed is 15 kilometres an hour.",
      *ANSC("l4", "60 ÷ 4 = 15", 15)),
    B("Check: at that speed, the first hour covers 15 kilometres. The last 12 minutes, at 4 minutes each, cover 3 more. 15 plus 3 is 18.",
      W("l5", "12 ÷ 4 = 3"), W("l6", "15 + 3 = 18")),
    B("So pick out only what you need: one trip to find the distance, then that distance and the rider's own time to find the speed."),
)

# Grandfather at 3 km/hr; Ravi starts 20 min later at 5 km/hr: where does he catch up?
LESSONS[P + "f181bd86-5d01-4cda-bc40-12e4894d07ee"] = LESSON(
    B("Grandfather sets off from home at 3 kilometres an hour. Ravi starts from the same place 20 minutes later, walking the same way at 5 kilometres an hour. How far from home does Ravi catch up?",
      GIVEN("q", "Grandfather 3 km/hr. Ravi starts 20 min later at 5 km/hr")),
    B("When Ravi sets off, Grandfather is already ahead. So first: how far ahead is he?"),
    B("20 minutes is a third of an hour, because 3 lots of 20 make 60. In a third of an hour at 3 kilometres an hour, Grandfather walks 1 kilometre.",
      W("l1", "20/60 = 1/3"), W("l2", "3 × 1/3 = 1"), NOTE("l2", "1", "km head start", "below", 2)),
    B("Now both are walking. Each hour, by how much does Ravi close the gap?",
      ask=CHOOSE(["5 + 3 = 8 km", "5 − 3 = 2 km", "5 km"], 1,
                 "They walk the same way. In an hour Ravi goes 5 kilometres, but Grandfather also moves on 3. So Ravi only gains the difference.")),
    B("Ravi gains 2 kilometres every hour. The gap is 1 kilometre, which is half of 2, so he needs half an hour to catch up.",
      W("l3", "5 − 3 = 2"), W("l4", "1 ÷ 2 = 1/2")),
    B("How far from home is that? Ravi walks at 5 kilometres an hour for half an hour, and half of 5 is 2.5. He catches up 2.5 kilometres from home.",
      *ANSC("l5", "5 × 1/2 = 2.5", "2.5")),
    B("Careful: the 1 kilometre is only the head start, and the half hour is only a time. The question asks how far from home, so we need Ravi's distance."),
    B("Check with Grandfather. He walks 20 minutes and then 30 more, which is 50 minutes. He does 1 kilometre every 20 minutes, so that is 2.5 kilometres. The same spot!",
      W("l6", "20 + 30 = 50"), W("l7", "50 ÷ 20 = 2.5")),
    B("So in a catch-up problem: find the head start, find how fast the gap closes, and that gives the time. Then use the chaser's speed to get the distance."),
)
