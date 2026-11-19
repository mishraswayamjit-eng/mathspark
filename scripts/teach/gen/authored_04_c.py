"""Speed warm-ups 002 to 010, written one by one."""
from authored_04_lib import ANSC, ANSL, B, BOX, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, UL, W  # noqa: F401

LESSONS = {}

# 5 cm every minute for 8 minutes.
LESSONS["G5A_SPEED_002"] = LESSON(
    B("A snail crawls 5 centimetres every minute. How far does it crawl in 8 minutes?",
      GIVEN("q", "5 cm every minute, for 8 minutes. How far?")),
    B("Every minute adds another 5 centimetres. And there are 8 of those minutes.",
      UL("q", "every minute")),
    B("So which sum gives the whole distance?",
      ask=CHOOSE(["5 + 8", "8 − 5", "5 × 8"], 2,
                 "The snail does not crawl 5 centimetres just once. It crawls 5 centimetres in each of the 8 minutes, so we need 8 lots of 5.")),
    B("8 lots of 5 is 5 times 8, which is 40. The snail crawls 40 centimetres.",
      *ANSC("l1", "5 × 8 = 40", 40), NOTE("l1", "40", "cm")),
    B("Check by going back: 40 centimetres shared into steps of 5 is 8 steps, one for each minute.",
      W("l2", "40 ÷ 5 = 8")),
    B("So distance is speed times time. Here that is 40 centimetres."),
)

# 2 metres every second: time for 50 metres.
LESSONS["G5A_SPEED_003"] = LESSON(
    B("Ravi swims 2 metres every second. How long does he take to swim 50 metres?",
      GIVEN("q", "2 metres every second. Time for 50 metres?")),
    B("Each second carries him 2 metres further. So the real question is: how many lots of 2 metres fit into 50 metres?"),
    B("Which sum tells us that?",
      ask=CHOOSE(["50 × 2", "50 ÷ 2", "50 − 2"], 1,
                 "We are asking how many 2s fit into 50, and each one takes a second. Counting how many fit is a division.")),
    B("50 divided by 2 is 25. Ravi takes 25 seconds.",
      *ANSC("l1", "50 ÷ 2 = 25", 25), NOTE("l1", "25", "seconds")),
    B("Check: 25 seconds, at 2 metres each second, is 25 times 2, which is 50 metres.",
      W("l2", "25 × 2 = 50")),
    B("So time is distance divided by speed."),
)

# 4 km/hr: time for 12 km.
LESSONS["G5A_SPEED_004"] = LESSON(
    B("Rahul walks at a steady 4 kilometres an hour. How long does he take to walk 12 kilometres?",
      GIVEN("q", "4 km/hr. Time to walk 12 km?")),
    B("4 kilometres an hour means each hour of walking covers 4 kilometres.",
      UL("q", "4 km/hr")),
    B("So how do we find the number of hours for 12 kilometres?",
      ask=CHOOSE(["12 × 4", "12 + 4", "12 ÷ 4"], 2,
                 "Each hour covers 4 kilometres. So we need to know how many 4s fit into 12, and that is a division.")),
    B("12 divided by 4 is 3. Rahul takes 3 hours.",
      *ANSC("l1", "12 ÷ 4 = 3", 3), NOTE("l1", "3", "hours")),
    B("Check hour by hour: 4, then 4 more, then 4 more. After 3 hours that is 12 kilometres.",
      W("l2", "4 + 4 + 4 = 12")),
    B("So time is distance divided by speed. Here it is 3 hours."),
)

# 45 km in 3 hours: speed.
LESSONS["G5A_SPEED_005"] = LESSON(
    B("A boat travels 45 kilometres along a river in 3 hours, at a steady speed. What is its speed?",
      GIVEN("q", "45 km in 3 hours. Speed?")),
    B("Speed tells us how far the boat goes in just 1 hour. The boat is steady, so each of the 3 hours covers the same distance."),
    B("So how do we find the distance for 1 hour?",
      ask=CHOOSE(["45 × 3", "45 ÷ 3", "45 − 3"], 1,
                 "The 45 kilometres are spread equally over the 3 hours. To find the share for one hour, divide 45 by 3.")),
    B("45 divided by 3 is 15. The boat covers 15 kilometres each hour, so its speed is 15 kilometres an hour.",
      *ANSC("l1", "45 ÷ 3 = 15", 15), NOTE("l1", "15", "km/hr")),
    B("Check: 15 kilometres an hour for 3 hours is 15 times 3, which is 45 kilometres.",
      W("l2", "15 × 3 = 45")),
    B("So speed is distance divided by time."),
)

# 600 metres in 2 minutes: metres in one minute.
LESSONS["G5A_SPEED_006"] = LESSON(
    B("A horse gallops 600 metres in 2 minutes, at a steady speed. How many metres does it gallop in one minute?",
      GIVEN("q", "600 metres in 2 minutes. Metres in 1 minute?")),
    B("One minute is half of 2 minutes. The horse is steady, so in half the time it covers half the distance."),
    B("Which sum finds that?",
      ask=CHOOSE(["600 × 2", "600 ÷ 2", "600 − 2"], 1,
                 "The 600 metres are shared equally between the 2 minutes. So one minute gets 600 divided by 2.")),
    B("600 divided by 2 is 300. The horse gallops 300 metres in one minute.",
      *ANSC("l1", "600 ÷ 2 = 300", 300), NOTE("l1", "300", "metres")),
    B("Check: 300 metres in the first minute and 300 in the second make 600 metres.",
      W("l2", "300 + 300 = 600")),
    B("So the distance for one minute is the whole distance divided by the number of minutes."),
)

# 10 cm every second: time for 80 cm.
LESSONS["G5A_SPEED_007"] = LESSON(
    B("A toy car moves 10 centimetres every second. How long does it take to move 80 centimetres?",
      GIVEN("q", "10 cm every second. Time for 80 cm?")),
    B("Each second moves the car 10 centimetres on. So we want to know how many 10s there are in 80."),
    B("Which sum is that?",
      ask=CHOOSE(["80 × 10", "80 − 10", "80 ÷ 10"], 2,
                 "We are counting how many lots of 10 centimetres fit into 80 centimetres. Each lot takes 1 second. That is a division.")),
    B("80 divided by 10 is 8. The toy car takes 8 seconds.",
      *ANSC("l1", "80 ÷ 10 = 8", 8), NOTE("l1", "8", "seconds", "below", 2)),
    B("Check: 8 seconds at 10 centimetres each second is 10 times 8, which is 80 centimetres.",
      W("l2", "10 × 8 = 80")),
    B("So time is distance divided by speed. The car needs 8 seconds."),
)

# 100 metres in 50 seconds: speed.
LESSONS["G5A_SPEED_008"] = LESSON(
    B("Kavya walks 100 metres in 50 seconds, at a steady speed. What is her speed in metres per second?",
      GIVEN("q", "100 metres in 50 seconds. Metres per second?")),
    B("Metres per second means: how many metres does she walk in just 1 second?",
      UL("q", "per second")),
    B("So what do we do with the 100 and the 50?",
      ask=CHOOSE(["100 × 50", "100 ÷ 50", "100 − 50"], 1,
                 "The 100 metres are spread equally over 50 seconds. To find the share for one second, divide 100 by 50.")),
    B("100 divided by 50 is 2. Kavya walks 2 metres every second.",
      *ANSC("l1", "100 ÷ 50 = 2", 2), NOTE("l1", "2", "metres per second")),
    B("Check: 2 metres every second, for 50 seconds, is 2 times 50, which is 100 metres.",
      W("l2", "2 × 50 = 100")),
    B("So speed is distance divided by time. Her speed is 2 metres per second."),
)

# 40 km/hr for 5 hours.
LESSONS["G5A_SPEED_009"] = LESSON(
    B("A lorry travels at a steady 40 kilometres an hour for 5 hours. What distance does it cover?",
      GIVEN("q", "40 km/hr for 5 hours. Distance?")),
    B("40 kilometres an hour means the lorry covers 40 kilometres in each hour. And it keeps going for 5 hours.",
      UL("q", "40 km/hr")),
    B("So how do we find the whole distance?",
      ask=CHOOSE(["40 + 5", "40 ÷ 5", "40 × 5"], 2,
                 "The lorry covers 40 kilometres in every one of the 5 hours. That is 5 lots of 40, so we multiply.")),
    B("4 times 5 is 20, so 40 times 5 is 200. The lorry covers 200 kilometres.",
      W("l1", "4 × 5 = 20"), *ANSC("l2", "40 × 5 = 200", 200), NOTE("l2", "200", "km")),
    B("Check: 200 kilometres shared over 5 hours is 200 divided by 5, which is 40 kilometres each hour.",
      W("l3", "200 ÷ 5 = 40")),
    B("So distance is speed times time. Here it is 200 kilometres."),
)

# Four friends, 1 hour each: who was fastest?
LESSONS["G5A_SPEED_010"] = LESSON(
    B("Four friends each cycled for exactly 1 hour. Ravi covered 14 kilometres, Sana 11, Tina 16 and Uday 9. Who cycled at the greatest speed?",
      GIVEN("q", "1 hour each: Ravi 14 km, Sana 11, Tina 16, Uday 9")),
    B("Everyone rode for the same time, 1 hour. So the distance each one covered in that hour is their speed.",
      UL("q", "1 hour each")),
    B("When the time is the same for everyone, who is the fastest?",
      ask=CHOOSE(["the one who went furthest", "the one who went least far", "we cannot tell"], 0,
                 "Faster means covering more ground in the same time. So in one hour, the fastest rider is the one who went the furthest.")),
    B("So we just compare the distances. 16 is more than 14, 14 is more than 11, and 11 is more than 9.",
      W("l1", "16 > 14 > 11 > 9")),
    B("The greatest distance is 16 kilometres, and that is Tina's. So Tina cycled at the greatest speed.",
      CIRC("q", "Tina 16"), *ANSL("l2", "Tina: 16 km in 1 hour → fastest", "Tina")),
    B("So when the time is the same, the one who goes furthest is the fastest. Here that is Tina."),
)
