"""authored-02, seventh group: measurement 001 to 006."""
from authored_02_lib import ANSC, ANSLC, B, CHOOSE, GIVEN, LB, LESSON, W

LESSONS = {}

# Sawing a log: pieces, cuts and rests.
LESSONS["G5A_MEASUREMENT_001"] = LESSON(
    B("A carpenter saws a log 3 metres 60 centimetres long into pieces of 45 centimetres. Each cut takes 4 minutes, and he rests 1 minute between cuts. How long is it from the start of the first cut to the end of the last?",
      GIVEN("q", "Log 3 m 60 cm. Pieces 45 cm. Cut 4 min, rest 1 min")),
    B("First, the number of pieces. Change the length to centimetres: 3 metres is 300 centimetres, so the log is 360 centimetres.",
      W("l0", "300 + 60 = 360"), LB("l1", "3 m 60 cm = 360 cm")),
    B("360 divided by 45. Two 45s make 90, and 90 times 4 is 360. So 45 goes in 8 times: 8 pieces.",
      W("l2", "45 × 2 = 90"), W("l3", "360 ÷ 45 = 8")),
    B("Now picture the log. How many cuts make 8 pieces?",
      ask=CHOOSE(["8 cuts", "7 cuts", "9 cuts"], 1,
                 "Try a short stick: 1 cut makes 2 pieces, and 2 cuts make 3 pieces. The cuts are always one fewer than the pieces.")),
    B("One cut makes 2 pieces, so the cuts are one fewer than the pieces. 8 pieces need 7 cuts.",
      W("l4", "8 − 1 = 7")),
    B("And the rests? He rests only between one cut and the next. How many rests fit between 7 cuts?",
      ask=CHOOSE(["7 rests", "6 rests", "8 rests"], 1,
                 "The rests are the gaps between the cuts. After the last cut the job is over, so there is no rest to count there. 7 cuts have 6 gaps.")),
    B("7 cuts have 6 gaps between them, so 6 rests.",
      W("l5", "7 − 1 = 6")),
    B("Cutting time: 7 cuts of 4 minutes is 28 minutes. Resting time: 6 rests of 1 minute is 6 minutes.",
      W("l6", "7 × 4 = 28"), W("l7", "6 × 1 = 6")),
    B("28 plus 6 is 34 minutes.",
      *ANSC("l8", "28 + 6 = 34", 34)),
    B("This question sets the same trap twice. Pieces, cuts, rests: each is one fewer than the one before. 8, then 7, then 6. The job takes 34 minutes."),
)

# 8 strips glued with overlaps.
LESSONS["G5A_MEASUREMENT_002"] = LESSON(
    B("Riya glues 8 strips of paper end to end. Each strip is 25 centimetres long, and at every join the two strips overlap by 15 millimetres. How long is the finished strip?",
      GIVEN("q", "8 strips of 25 cm. Overlap at each join: 15 mm")),
    B("Two things need care. First, the units: centimetres and millimetres. Let's work in millimetres. 25 centimetres is 250 millimetres.",
      W("l1", "25 × 10 = 250")),
    B("With no overlap at all, 8 strips would be 8 times 250, which is 2000 millimetres.",
      W("l2", "8 × 250 = 2000")),
    B("Second, the joins. How many joins are there in a row of 8 strips?",
      ask=CHOOSE(["8 joins", "7 joins", "9 joins"], 1,
                 "Try 2 strips: they have just 1 join. 3 strips have 2 joins. The joins are always one fewer than the strips, because the two ends are free.")),
    B("The two end strips each have a free end, so 8 strips have 7 joins.",
      W("l3", "8 − 1 = 7")),
    B("Each join hides 15 millimetres of paper. 7 times 15 is 105 millimetres hidden.",
      W("l4", "7 × 15 = 105")),
    B("Take the hidden length away: 2000 minus 105 is 1895 millimetres.",
      W("l5", "2000 − 105 = 1895")),
    B("Now back to centimetres. 10 millimetres make 1 centimetre, so 1895 millimetres is 189 centimetres and 5 millimetres.",
      W("l6", "1895 = 189 × 10 + 5"), *ANSLC("l7", "189 cm 5 mm", "189 cm 5 mm")),
    B("The traps: taking away 8 overlaps instead of 7, or taking away the 15 as if it were centimetres."),
    B("So put everything in one unit, count the joins as one fewer than the strips, and subtract. The strip is 189 centimetres 5 millimetres long."),
)

# Posts round a rectangular garden.
LESSONS["G5A_MEASUREMENT_003"] = LESSON(
    B("A rectangular garden is 12 metres long and 7 metres 50 centimetres wide. Posts go all the way round its boundary, 1 metre 50 centimetres apart, with a post at every corner. How many posts are needed?",
      GIVEN("q", "Garden 12 m by 7 m 50 cm. Posts 1 m 50 cm apart")),
    B("Work in centimetres, so there are no half metres to worry about. 12 metres is 1200 centimetres, 7 metres 50 is 750, and 1 metre 50 is 150.",
      LB("l1", "1200 cm by 750 cm.  Gap: 150 cm")),
    B("Imagine walking once round the whole boundary. One length and one width make 1950 centimetres. Twice that, for all four sides, is 3900.",
      W("l2", "1200 + 750 = 1950"), W("l3", "1950 × 2 = 3900")),
    B("How many gaps of 150 fit into 3900? Two gaps make 300, and 3900 divided by 300 is 13. So there are 13 times 2, which is 26 gaps.",
      W("l4", "150 × 2 = 300"), W("l5", "3900 ÷ 300 = 13"), W("l6", "3900 ÷ 150 = 26")),
    B("26 gaps. On a straight fence, the posts are one more than the gaps. Is that true here, going round a closed boundary?",
      ask=CHOOSE(["yes: 27 posts", "no: 26 posts, same as the gaps"], 1,
                 "Walk round in your head. The last gap brings you back to the post you started from, and it is already counted. So there is one post for each gap.")),
    B("Round a closed loop, the last gap ends at the first post. So posts and gaps are equal: 26 posts.",
      *ANSLC("l7", "closed loop: 26 gaps, 26 posts", "26 posts")),
    B("Do the corners work out? 1200 divided by 150 is 8, and 750 divided by 150 is 5. A whole number of gaps on each side, so a post lands on every corner.",
      W("l8", "1200 ÷ 150 = 8"), W("l9", "750 ÷ 150 = 5")),
    B("Another trap is counting each side on its own: 9 posts, 6, 9 and 6 make 30. But that counts every corner post twice. 30 minus 4 is 26.",
      W("l10", "9 + 6 + 9 + 6 = 30"), W("l11", "30 − 4 = 26")),
    B("So for posts round a closed boundary, divide the distance all the way round by the gap. Posts equal gaps: 26."),
)

# The leaking drum.
LESSONS["G5A_MEASUREMENT_004"] = LESSON(
    B("An empty drum holds 100 litres. Every morning Ravi pours in 40 litres, and every night 25 litres leak out. On which morning does the drum become full for the first time?",
      GIVEN("q", "Drum: 100 litres. Morning: + 40. Night: − 25")),
    B("Over a whole day and night the drum gains 40 minus 25, which is 15 litres. It is tempting to divide 100 by 15. But when in the day is the drum at its fullest?",
      W("l1", "40 − 25 = 15"),
      ask=CHOOSE(["just after the morning pour", "just after the night leak"], 0,
                 "The level goes up in the morning and down at night. So the highest level each day comes straight after the pouring, before the leak.")),
    B("So we watch the morning levels. Morning 1: the drum has 40 litres. That night it leaks down to 15.",
      W("m1", "0 + 40 = 40"), W("n1", "40 − 25 = 15")),
    B("Morning 2: 15 plus 40 is 55. Night: down to 30.",
      W("m2", "15 + 40 = 55"), W("n2", "55 − 25 = 30")),
    B("Morning 3: 30 plus 40 is 70. Night: down to 45.",
      W("m3", "30 + 40 = 70"), W("n3", "70 − 25 = 45")),
    B("Morning 4: 45 plus 40 is 85. Not full yet. Night: down to 60.",
      W("m4", "45 + 40 = 85"), W("n4", "85 − 25 = 60")),
    B("Morning 5 starts with 60 litres. What happens when Ravi pours in 40?",
      ask=CHOOSE(["it reaches 100: full", "it reaches 90", "it reaches 75"], 0,
                 "60 plus 40 is exactly 100, and the drum holds 100 litres. So it is full.")),
    B("60 plus 40 is 100. The drum is full on the 5th morning.",
      W("m5", "60 + 40 = 100"), *ANSLC("a", "full on the 5th morning", "5th")),
    B("See the pattern in the morning levels? 40, 55, 70, 85, 100. They go up by 15 each day, but they start from 40, not from 0."),
    B("The trap is 100 divided by 15, which points to the 7th morning. Always ask when the level is highest, and follow it. The answer is the 5th morning."),
)

# Bottle of juice: 1 kg 350 g full, 800 g half drunk.
LESSONS["G5A_MEASUREMENT_005"] = LESSON(
    B("A bottle full of juice weighs 1 kilogram 350 grams. When half the juice has been drunk, the bottle and the juice left weigh 800 grams. What does the empty bottle weigh?",
      GIVEN("q", "Full: 1 kg 350 g. Half the juice gone: 800 g")),
    B("Put both weights in grams first. 1 kilogram is 1000 grams, so the full bottle weighs 1350 grams.",
      W("l1", "1000 + 350 = 1350")),
    B("Between the two weighings, what went away?",
      ask=CHOOSE(["half the juice", "half the bottle and juice", "all the juice"], 0,
                 "Only juice was drunk. The bottle itself is still all there. So the drop in weight is exactly half of the juice.")),
    B("The drop is 1350 minus 800, which is 550 grams. That is half the juice.",
      W("l2", "1350 − 800 = 550")),
    B("So all the juice is twice as much: 550 times 2 is 1100 grams.",
      W("l3", "550 × 2 = 1100")),
    B("The full bottle is bottle plus juice. Take the juice away: 1350 minus 1100 is 250.",
      *ANSC("l4", "1350 − 1100 = 250", 250)),
    B("Check: the bottle, 250, plus half the juice, 550, makes 800 grams. That matches the second weighing.",
      W("l5", "250 + 550 = 800")),
    B("The trap is to halve a whole weighing, like half of 800. Only the juice was halved, never the bottle."),
    B("So compare the two weighings to find the juice, then take all the juice from the full weight. The empty bottle weighs 250 grams."),
)

# Mumbai to Dubai: two clocks.
LESSONS["G5A_MEASUREMENT_006"] = LESSON(
    B("A plane leaves Mumbai at 11:40 p.m. by Mumbai clocks. It lands in Dubai at 1:25 a.m. by Dubai clocks. Dubai clocks are always 1 hour 30 minutes behind Mumbai clocks. How long was the flight?",
      GIVEN("q", "Leaves 11:40 p.m. (Mumbai). Lands 1:25 a.m. (Dubai)")),
    B("The two times were read on clocks in two different cities. Can we just find the gap between 11:40 p.m. and 1:25 a.m.?",
      ask=CHOOSE(["yes, subtract them", "no, use one city's clock first"], 1,
                 "The clocks do not agree: Dubai's is 1 hour 30 minutes behind. To measure a length of time, both readings must come from the same clock.")),
    B("So let's put the landing on Mumbai's clock. Dubai is behind, which means Mumbai is ahead: at the same moment, Mumbai's clock shows a later time. So we add 1 hour 30 minutes."),
    B("1:25 a.m. plus 1 hour is 2:25 a.m. Then 30 minutes more: 25 plus 30 is 55. So the plane lands at 2:55 a.m. Mumbai time.",
      W("l1", "25 + 30 = 55"), LB("l2", "1:25 a.m. Dubai = 2:55 a.m. Mumbai")),
    B("Now both times are on Mumbai's clock: 11:40 p.m. to 2:55 a.m. We cross midnight, so go in two parts. How long from 11:40 p.m. to midnight?",
      ask=CHOOSE(["40 minutes", "20 minutes", "60 minutes"], 1,
                 "An hour has 60 minutes. From 40 minutes past up to the full hour is 60 minus 40, which is 20 minutes.")),
    B("20 minutes to midnight. Then from midnight to 2:55 a.m. is 2 hours 55 minutes.",
      W("l3", "60 − 40 = 20"), LB("l4", "20 min + 2 h 55 min")),
    B("Add the minutes: 20 plus 55 is 75 minutes, which is 1 hour and 15 minutes. With the 2 hours, that makes 3 hours 15 minutes.",
      W("l5", "20 + 55 = 75"), W("l6", "75 = 60 + 15"), *ANSLC("l7", "3 hours 15 minutes", "3 hours 15 minutes")),
    B("The traps: finding the gap between the two readings as they stand, on two different clocks. Or taking away the 1 hour 30 minutes instead of adding it, which gives a flight of only 15 minutes!"),
    B("So before finding how long something took, put both times on the same clock. The flight took 3 hours 15 minutes."),
)
