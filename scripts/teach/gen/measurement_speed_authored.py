"""Lessons written by hand for the one-off measurement-speed questions (past papers and worksheets).

Each function returns the lesson for one question. AUTHORED at the bottom maps question id to function.
"""
from measurement_speed_lib import (answer, beat, choose, fig, given, lab, lesson, mark, note, ring, strike, w)


def ws_b3_021(q):
    """126 words in 3 minutes; how many in half a minute? (21)"""
    qid = q["id"]
    return lesson("authored", [
        beat("Anay types 126 words in 3 minutes. We want to know how many words he types in just half a minute.",
             given("q1", "126 words in 3 minutes"), given("q2", "? words in half a minute"),
             fig("f1", {"kind": "barModel", "bars": [{"segments": [{"units": 1, "label": "1 minute"}] * 3, "brace": "126 words"}]})),
        beat("3 minutes is a long way from half a minute, so let's use a stepping stone: 1 minute. How do we find the words for 1 minute?",
             ask=choose(qid + "a1", "126 ÷ 3", ["126 × 3", "126 − 3"],
                        "The 126 words are spread evenly over 3 minutes. 1 minute is one of 3 equal parts, so we divide by 3.")),
        beat("126 is 120 and 6. 120 divided by 3 is 40, and 6 divided by 3 is 2. So he types 42 words in 1 minute.",
             w("c1", "120 ÷ 3 = 40"), w("c2", "6 ÷ 3 = 2"), w("c3", "126 ÷ 3 = 42"), lab("c4", "1 minute: 42 words"),
             fig("f1", {"kind": "barModel", "bars": [{"segments": [{"units": 1, "label": "42 words"}] * 3, "brace": "126 words"}]})),
        beat("Careful now. 42 is one of the choices, but the question does not ask about 1 minute. It asks about half a minute. So what do we do with 42?",
             mark("q2", "half a minute"),
             ask=choose(qid + "a2", "halve it: 42 ÷ 2", ["double it: 42 × 2", "leave it as 42"],
                        "Half a minute is less time than 1 minute, so he types fewer words, not more. Half the time means half the words.")),
        beat("Half of 42 is 21. So Anay types 21 words in half a minute.",
             w("c5", "42 ÷ 2 = 21"), answer("ans", "Half a minute: 21 words"), ring("ans", "21 words")),
        beat("Check it. 3 minutes holds 6 half minutes, and 6 times 21 is 126. Exactly what we were told.",
             w("chk", "21 × 6 = 126")),
        beat("So when the numbers do not match up, go through 1. Find what happens in 1 minute, then shrink it or grow it to what you need."),
    ])


def ws_b3_036(q):
    """36 toys in a 9 hour day, 56 workers; toys every hour? (224)"""
    qid = q["id"]
    return lesson("authored", [
        beat("One worker makes 36 toys in a day of 9 hours, and the factory has 56 workers. How many toys does the whole factory make every hour?",
             given("q1", "1 worker: 36 toys in 9 hours"), given("q2", "56 workers: ? toys in 1 hour")),
        beat("There is a lot going on here, so let's shrink it to the smallest piece: one worker, for one hour. How many toys is that?",
             ask=choose(qid + "a1", "36 ÷ 9", ["36 × 9", "56 ÷ 9"],
                        "One worker's 36 toys are spread evenly over 9 hours. For one hour's share, split 36 into 9 equal parts.")),
        beat("36 divided by 9 is 4. So each worker makes 4 toys every hour.",
             w("c1", "36 ÷ 9 = 4"), lab("c2", "1 worker, 1 hour: 4 toys"),
             fig("f1", {"kind": "barModel", "bars": [{"segments": [{"units": 1, "label": "4"}] * 9, "brace": "36 toys in 9 hours"}]})),
        beat("Now bring back all 56 workers. In that one hour, each of them makes 4 toys. What shall we work out?",
             ask=choose(qid + "a2", "56 × 4", ["56 + 4", "56 ÷ 4"],
                        "Every one of the 56 workers adds 4 toys to the pile. That is 56 lots of 4, so we multiply.")),
        beat("56 times 4 in two pieces. 50 times 4 is 200, and 6 times 4 is 24. Together, that makes 224.",
             w("m1", "50 × 4 = 200"), w("m2", "6 × 4 = 24"), w("m3", "200 + 24 = 224")),
        beat("So the factory produces 224 toys every hour.",
             w("m4", "56 × 4 = 224"), answer("ans", "224 toys every hour"), ring("ans", "224 toys")),
        beat("Notice we never multiplied by 9. The 9 hours were only there to help us find what one worker does in one hour. Using them twice is the slip to watch for.",
             mark("q1", "9 hours")),
        beat("Check with a whole day. 224 toys an hour for 9 hours is 2016 toys. And 56 workers making 36 each is 2016 too. They match.",
             w("k1", "224 × 9 = 2016"), w("k2", "56 × 36 = 2016")),
        beat("So for a big rate question, shrink it down to one worker and one hour, then build back up."),
    ])


def fp_2016_013(q):
    """Walk + ride = 37 min, walk both ways = 55 min; ride both ways? (19 minutes)"""
    qid = q["id"]
    return lesson("authored", [
        beat("Amar walks from A to B and rides back, and that takes 37 minutes. Walking both ways takes 55 minutes. We want the time to ride both ways.",
             given("q1", "1 walk + 1 ride = 37 min"), given("q2", "2 walks = 55 min"), given("q3", "2 rides = ?"),
             fig("f1", {"kind": "journey", "places": ["A", "B"], "legs": [{"top": "walk →", "bottom": "← ride"}]})),
        beat("We are never told how far it is, and we will not need it. Here is a neat idea: imagine Amar does his walk and ride trip twice. What has he done altogether?",
             ask=choose(qid + "a1", "2 walks and 2 rides", ["4 walks", "1 walk and 1 ride"],
                        "Each trip is 1 walk and 1 ride. Do the trip twice and you get 2 walks and 2 rides.")),
        beat("Twice 37 minutes is 74 minutes. So 2 walks and 2 rides together take 74 minutes.",
             w("c1", "37 × 2 = 74"), lab("d", "2 walks + 2 rides = 74 min")),
        beat("But we already know how long 2 walks take: 55 minutes. Take the 2 walks away, and only the 2 rides are left.",
             mark("q2", "55 min"), strike("d", "2 walks", "− 55")),
        beat("74 minus 55 is 19. So riding both ways takes 19 minutes.",
             w("c2", "74 − 55 = 19"), answer("ans", "2 rides = 19 minutes"), ring("ans", "19 minutes")),
        beat("A tempting slip is to take 37 away from 55 straight off. That only tells you how much longer a walk is than a ride, not the time for two rides."),
        beat("Check with single trips. Half of 55 is 27.5 minutes for one walk, and half of 19 is 9.5 for one ride. 27.5 plus 9.5 is 37 minutes. It matches.",
             w("k1", "55 ÷ 2 = 27.5"), w("k2", "19 ÷ 2 = 9.5"), w("k3", "27.5 + 9.5 = 37")),
        beat("So the trick here: build the first fact up until it holds the piece you already know, then take that piece away."),
    ])


def fp_2017_007(q):
    """16500 miles at 125 miles a day (132 days)"""
    qid = q["id"]
    return lesson("authored", [
        beat("A seagull flew 16500 miles from Finland to Australia, covering 125 miles every day. How many days did it take?",
             given("q1", "16500 miles at 125 miles per day"), given("q2", "Number of days = ?"),
             fig("f1", {"kind": "journey", "places": ["Finland", "Australia"], "legs": [{"top": "16500 miles", "bottom": "? days"}],
                        "note": "125 miles every day"})),
        beat("Each day uses up 125 miles of the journey. So what are we really asking?",
             ask=choose(qid + "a1", "how many 125s fit in 16500", ["16500 × 125", "16500 − 125"],
                        "Every day the seagull covers one more lot of 125 miles. Counting how many lots fit into 16500 is a division.")),
        beat("So it is 16500 divided by 125. That looks scary, but here is a friendly fact: 125 times 8 is exactly 1000. So every 1000 miles takes 8 days.",
             lab("f", "Days = distance ÷ miles per day"), w("c0", "16500 ÷ 125 = ?"), w("c1", "125 × 8 = 1000"),
             note("c1", "1000", "8 days", "below")),
        beat("Now split 16500 into 16000 and 500. 16000 is 16 thousands, and each thousand takes 8 days. 16 times 8 is 128 days.",
             w("c2", "16500 = 16000 + 500"), w("c3", "16 × 8 = 128")),
        beat("What about the last 500 miles? How many days is that?",
             mark("c2", "500", nth=2),
             ask=choose(qid + "a2", "4 days", ["5 days", "8 days"],
                        "8 lots of 125 make 1000, and 500 is half of 1000. So we need half of 8, which is 4.")),
        beat("125 times 4 is 500, so the last stretch takes 4 more days.",
             w("c4", "125 × 4 = 500")),
        beat("128 days plus 4 days makes 132 days. That is how long the seagull took.",
             w("c5", "128 + 4 = 132"), answer("ans", "132 days"), ring("ans", "132 days")),
        beat("Check by multiplying back. 125 times 132 is 16500 miles. Exactly the whole journey.",
             w("chk", "125 × 132 = 16500")),
        beat("So, how many days means how many day sized pieces fit into the distance, and that is division. A friendly fact, like 125 times 8, can tame a big one."),
    ])


def fp_2017_029(q):
    """30 m/s in km/hr (108)"""
    qid = q["id"]
    return lesson("authored", [
        beat("A motorcycle moves at 30 metres per second. We want that same speed in kilometres per hour.",
             given("q1", "30 m/s = ? km/hr")),
        beat("Kilometres per hour means: how many kilometres in one hour. So let's follow the motorcycle for one whole hour. First, how many seconds are in 1 hour?",
             ask=choose(qid + "a1", "3600", ["60", "360"],
                        "60 seconds make a minute, and 60 minutes make an hour. So 1 hour is 60 times 60 seconds, which is 3600.")),
        beat("60 seconds in a minute, 60 minutes in an hour. 60 times 60 is 3600 seconds.",
             w("c1", "60 × 60 = 3600"), lab("c2", "1 hour = 3600 seconds")),
        beat("Every second the motorcycle goes 30 metres. So in 3600 seconds it goes 30 times 3600. 3 times 36 is 108, then put the three zeros back: 108000 metres.",
             w("c3", "3 × 36 = 108"), w("c4", "30 × 3600 = 108000")),
        beat("That is how far it goes in one hour, but in metres. A kilometre is bigger than a metre. So to change 108000 metres into kilometres, what do we do?",
             lab("f", "1 km = 1000 m"),
             ask=choose(qid + "a2", "divide by 1000", ["multiply by 1000", "divide by 60"],
                        "It takes 1000 metres to make just 1 kilometre. A bigger unit means fewer of them, so the number goes down: we divide by 1000.")),
        beat("108000 divided by 1000 is 108. So 30 metres per second is 108 kilometres per hour.",
             w("c5", "108000 ÷ 1000 = 108"), answer("ans", "30 m/s = 108 km/hr"), ring("ans", "108 km/hr")),
        beat("Here is the shortcut hiding in what we did. Times 3600, then divide by 1000, is the same as times 18, divided by 5.",
             w("s1", "3600 ÷ 1000 = 18 ÷ 5")),
        beat("Try the shortcut as a check. 30 divided by 5 is 6, and 6 times 18 is 108. Same answer.",
             w("s2", "30 ÷ 5 = 6"), w("s3", "6 × 18 = 108")),
        beat("So to turn metres per second into kilometres per hour, ask how far it goes in one hour, then change the metres into kilometres."),
    ])


def fp_2017_038(q):
    """Train 200 m long passes a pole in 9 seconds; speed in km/hr (80)"""
    qid = q["id"]
    return lesson("authored", [
        beat("A train 200 metres long passes a pole in 9 seconds. We want its speed in kilometres per hour.",
             given("q1", "Train 200 m long passes a pole in 9 seconds"), given("q2", "Speed = ? km/hr")),
        beat("First picture it. The front of the train reaches the pole, and the train keeps going until its back end clears the pole. How far has the train moved in that time?",
             ask=choose(qid + "a1", "200 metres, its own length", ["9 metres", "0 metres, the pole stands still"],
                        "Watch the front of the train. It starts level with the pole, and when the back end clears the pole, the front is one whole train length ahead. That is 200 metres.")),
        beat("So the train covers 200 metres in 9 seconds.",
             lab("c1", "200 m in 9 seconds"),
             fig("f1", {"kind": "journey", "places": ["Pole", "Front of train"], "legs": [{"top": "200 m", "bottom": "9 seconds"}]})),
        beat("Kilometres per hour asks how far it goes in one hour. 1 hour is 3600 seconds, so how many 9 second chunks fit in an hour? 3600 divided by 9 is 400.",
             lab("c2", "1 hour = 3600 seconds"), w("c3", "3600 ÷ 9 = 400")),
        beat("In every chunk the train goes 200 metres, and there are 400 chunks. 400 times 200 is 80000 metres in one hour.",
             w("c4", "400 × 200 = 80000")),
        beat("Now change 80000 metres into kilometres. 1000 metres make 1 kilometre. How many kilometres is that?",
             lab("f", "1 km = 1000 m"),
             ask=choose(qid + "a2", "80 km", ["800 km", "8 km"],
                        "Count the thousands in 80000. A bigger unit means a smaller number, so we divide by 1000.")),
        beat("80000 divided by 1000 is 80. So the speed of the train is 80 kilometres per hour.",
             w("c5", "80000 ÷ 1000 = 80"), answer("ans", "Speed = 80 km/hr"), ring("ans", "80 km/hr")),
        beat("Notice what we dodged. 200 divided by 9 does not go exactly, so metres per second would have been messy. Going through one hour kept every number whole."),
        beat("So for a train passing a pole, the distance is the train's own length. Then ask how far it would go in one hour."),
    ])


def fp_2018_020(q):
    """6 km/hr for 3 minutes (300 m)"""
    qid = q["id"]
    return lesson("authored", [
        beat("Someone walks at 6 kilometres per hour. We want to know how far he gets in 3 minutes.",
             given("q1", "6 km/hr for 3 minutes"), given("q2", "Distance = ? metres")),
        beat("The speed is in kilometres and hours, but the question is about minutes, and the choices are in metres. So let's rewrite the speed in metres and minutes. How many metres is 6 kilometres?",
             lab("f", "1 km = 1000 m"),
             ask=choose(qid + "a1", "6000 metres", ["600 metres", "60 metres"],
                        "Kilo means a thousand, so 1 kilometre is 1000 metres. 6 kilometres is 6 times 1000.")),
        beat("6 times 1000 is 6000 metres. And 1 hour is 60 minutes. So he walks 6000 metres in 60 minutes.",
             w("c1", "6 × 1000 = 6000"), lab("c2", "1 hour = 60 minutes"), lab("c3", "6000 m in 60 minutes")),
        beat("Now find the distance for just 1 minute. What do we work out?",
             ask=choose(qid + "a2", "6000 ÷ 60", ["6000 × 60", "6000 − 60"],
                        "The 6000 metres are spread evenly over 60 minutes. For one minute's share, we split 6000 into 60 equal parts.")),
        beat("Take a zero off each number: 6000 divided by 60 is the same as 600 divided by 6, which is 100. So he walks 100 metres every minute.",
             w("c4", "6000 ÷ 60 = 600 ÷ 6"), w("c5", "600 ÷ 6 = 100"), lab("c6", "1 minute: 100 m")),
        beat("3 minutes is 3 lots of 100 metres. So he covers 300 metres.",
             w("c7", "3 × 100 = 300"), answer("ans", "Distance = 300 metres"), ring("ans", "300 metres")),
        beat("Check it. 3 minutes fits into an hour 20 times, and 20 times 300 metres is 6000 metres. That is the full 6 kilometres.",
             w("k1", "60 ÷ 3 = 20"), w("k2", "20 × 300 = 6000")),
        beat("So when the units do not match the question, rewrite the speed in the units you need first. After that it is one small step at a time."),
    ])


def fp_2018_036(q):
    """Train 100 m long at 36 km/hr passes a man (10 sec)"""
    qid = q["id"]
    return lesson("authored", [
        beat("A train 100 metres long runs at 36 kilometres per hour. How long does it take to pass a man standing by the rails?",
             given("q1", "Train 100 m long, speed 36 km/hr"), given("q2", "Time to pass a man = ?")),
        beat("To pass the man, the whole train has to go by him, front to back. So the train must travel its own length: 100 metres.",
             mark("q1", "100 m"),
             fig("f1", {"kind": "journey", "places": ["Man", "Front of train"], "legs": [{"top": "100 m", "bottom": "? seconds"}]})),
        beat("The distance is in metres and the choices are in seconds. But the speed is in kilometres per hour. Which units should the speed be in?",
             mark("q1", "km/hr"),
             ask=choose(qid + "a1", "metres per second", ["kilometres per second", "leave it in km per hour"],
                        "We want metres to match the train, and seconds to match the answer. So we change the speed into metres per second.")),
        beat("In 1 hour the train goes 36 kilometres. 1 kilometre is 1000 metres, so that is 36000 metres.",
             lab("f", "1 km = 1000 m"), w("c1", "36 × 1000 = 36000")),
        beat("And 1 hour is 60 times 60 seconds, which is 3600 seconds. So the train goes 36000 metres in 3600 seconds.",
             w("c2", "60 × 60 = 3600"), lab("c3", "36000 m in 3600 seconds")),
        beat("36000 is 10 lots of 3600. So in each second the train goes 10 metres.",
             w("c4", "36000 ÷ 3600 = 10"), lab("c5", "36 km/hr = 10 m/s"), mark("c5", "10 m/s", "box")),
        beat("10 metres every second, and 100 metres to cover. How long does that take?",
             ask=choose(qid + "a2", "10 seconds", ["100 seconds", "36 seconds"],
                        "Each second the train moves 10 metres. Count how many lots of 10 fit into 100.")),
        beat("100 divided by 10 is 10. The train passes the man in 10 seconds.",
             w("c6", "100 ÷ 10 = 10"), answer("ans", "Time = 10 seconds"), ring("ans", "10 seconds")),
        beat("The slip to watch for is dividing 100 by 36 straight away. That mixes metres with kilometres, and seconds with hours."),
        beat("So match the units first: metres with metres, seconds with seconds. Then time is distance divided by speed."),
    ])


def fp_2019_006(q):
    """900 metres in 18 minutes; distance in an hour (3 km)"""
    qid = q["id"]
    return lesson("authored", [
        beat("A man walks 900 metres in 18 minutes. We want to know how far he walks in an hour.",
             given("q1", "900 metres in 18 minutes"), given("q2", "Distance in 1 hour = ?")),
        beat("18 minutes does not fit neatly into an hour, so let's use a stepping stone: 1 minute. How do we find how far he walks in 1 minute?",
             ask=choose(qid + "a1", "900 ÷ 18", ["900 × 18", "900 − 18"],
                        "The 900 metres are spread evenly over 18 minutes. One minute's share is 900 split into 18 equal parts.")),
        beat("18 times 5 is 90, so 18 times 50 is 900. That means 900 divided by 18 is 50. He walks 50 metres every minute.",
             w("c1", "18 × 5 = 90"), w("c2", "18 × 50 = 900"), w("c3", "900 ÷ 18 = 50"), lab("c4", "1 minute: 50 m")),
        beat("An hour is 60 minutes, so in an hour he walks 60 lots of 50 metres. 6 times 5 is 30, and two more zeros make 3000 metres.",
             lab("c5", "1 hour = 60 minutes"), w("c6", "6 × 5 = 30"), w("c7", "60 × 50 = 3000")),
        beat("The choices are in kilometres, so we are not finished. 1000 metres make 1 kilometre. What is 3000 metres in kilometres?",
             lab("f", "1 km = 1000 m"),
             ask=choose(qid + "a2", "3 km", ["30 km", "300 km"],
                        "A kilometre is a bigger unit, so we need fewer of them. Count the thousands in 3000.")),
        beat("3000 divided by 1000 is 3. So he covers 3 kilometres in an hour.",
             w("c8", "3000 ÷ 1000 = 3"), answer("ans", "3 km in an hour"), ring("ans", "3 km")),
        beat("Check the first step. 50 metres a minute, for 18 minutes, is 900 metres. That matches what we were told.",
             w("chk", "50 × 18 = 900")),
        beat("So: go down to 1 minute, build up to 60 minutes, and change the units at the end to match the choices."),
    ])


def fp_2019_023(q):
    """18 km at 72 km/hr (15 min)"""
    qid = q["id"]
    return lesson("authored", [
        beat("A car drives at 72 kilometres per hour. We want to know how long it takes to cover 18 kilometres.",
             given("q1", "18 km at 72 km/hr"), given("q2", "Time = ? minutes"),
             fig("f1", {"kind": "journey", "places": ["Start", "End"], "legs": [{"top": "18 km", "bottom": "? minutes"}],
                        "note": "72 km in every hour"})),
        beat("72 kilometres per hour means 72 kilometres in 1 hour. Our trip is only 18 kilometres, much less than that. So the time will be just a part of an hour.",
             lab("f", "72 km/hr means 72 km in 1 hour")),
        beat("So, what part of 72 is 18?",
             ask=choose(qid + "a1", "one quarter", ["one half", "one third"],
                        "Try doubling. Double 18 is not yet 72, but double it again and you are there. So it takes 4 lots of 18, and 18 is one quarter of 72.")),
        beat("18 times 4 is 72. So 18 kilometres is one quarter of what the car does in an hour, and it needs one quarter of an hour.",
             w("c1", "18 × 4 = 72"), w("c2", "18 ÷ 72 = 1/4"),
             fig("f1", {"kind": "barModel", "bars": [{"segments": [{"units": 1, "label": "18 km"}] * 4, "brace": "72 km in 1 hour"}],
                        "highlight": ["b0s0"]})),
        beat("The choices are in minutes, and 1 hour is 60 minutes. So how long is a quarter of an hour?",
             lab("c3", "1 hour = 60 minutes"),
             ask=choose(qid + "a2", "15 minutes", ["25 minutes", "4 minutes"],
                        "A quarter means one of 4 equal parts. Split the 60 minutes into 4 equal parts.")),
        beat("60 divided by 4 is 15. So the car takes 15 minutes.",
             w("c4", "60 ÷ 4 = 15"), answer("ans", "Time = 15 minutes"), ring("ans", "15 minutes")),
        beat("Check it. 4 quarter hours make 1 hour, and 4 lots of 18 kilometres make 72 kilometres. That is exactly the speed we were given."),
        beat("So time is distance divided by speed. When that comes out as a part of an hour, turn it into minutes using 60."),
    ])


def fp_2020_020(q):
    """15 feet per minute for 24 minutes 40 seconds (370 ft)"""
    qid = q["id"]
    return lesson("authored", [
        beat("An ant moves 15 feet every minute. We want to know how far it travels in 24 minutes and 40 seconds.",
             given("q1", "15 feet per minute"), given("q2", "24 minutes 40 seconds: ? feet")),
        beat("The time has two parts, whole minutes and some extra seconds. Let's take them one at a time, starting with the 24 whole minutes. What do we work out?",
             mark("q2", "24 minutes"),
             ask=choose(qid + "a1", "24 × 15", ["24 + 15", "24 ÷ 15"],
                        "Every minute adds another 15 feet. 24 minutes means 24 lots of 15, so we multiply.")),
        beat("24 times 15 in two pieces. 24 times 10 is 240. 5 is half of 10, so 24 times 5 is half of 240, which is 120. Together, 360 feet.",
             w("c1", "24 × 10 = 240"), w("c2", "24 × 5 = 120"), w("c3", "240 + 120 = 360"), lab("c4", "24 minutes: 360 feet")),
        beat("Careful: 360 is one of the choices, and it is tempting to stop here. But the ant keeps walking for 40 more seconds.",
             mark("q2", "40 seconds")),
        beat("The speed is per minute, so we need the 40 seconds as a part of a minute. A minute has 60 seconds. What part of a minute is 40 seconds?",
             lab("f", "1 minute = 60 seconds"),
             ask=choose(qid + "a2", "2/3 of a minute", ["0.4 of a minute", "1/2 of a minute"],
                        "A minute has 60 seconds, not a hundred, so 40 seconds is not 0.4 of a minute. 40 out of 60 is the same as 4 out of 6, which is two thirds.")),
        beat("40 out of 60 is two thirds. One third of 15 feet is 5 feet, so two thirds is 10 feet.",
             w("c5", "40/60 = 2/3"), w("c6", "15 ÷ 3 = 5"), w("c7", "2 × 5 = 10"), lab("c8", "40 seconds: 10 feet")),
        beat("Now put the two parts together. 360 plus 10 is 370. The ant travels 370 feet.",
             w("c9", "360 + 10 = 370"), answer("ans", "370 feet"), ring("ans", "370 feet")),
        beat("Sense check. A full 25 minutes would be 375 feet. Our time is a little under 25 minutes, and 370 is a little under 375. It fits.",
             w("chk", "25 × 15 = 375")),
        beat("So when a time has minutes and seconds, work out each part on its own, and turn the seconds into a part of a minute using 60."),
    ])


def fp_2020_040(q):
    """10 m/sec in km/hr (36)"""
    qid = q["id"]
    return lesson("authored", [
        beat("An insect flies at 10 metres per second. We want that speed in kilometres per hour.",
             given("q1", "10 m/sec = ? km/hr")),
        beat("Kilometres per hour means how far it flies in one whole hour. Let's build up to an hour, starting with 1 minute. How far does the insect fly in 1 minute?",
             lab("c1", "1 minute = 60 seconds"),
             ask=choose(qid + "a1", "600 metres", ["60 metres", "100 metres"],
                        "A minute has 60 seconds, and the insect flies 10 metres in every one of them. That is 60 lots of 10.")),
        beat("60 times 10 is 600 metres in 1 minute.",
             w("c2", "60 × 10 = 600")),
        beat("Careful: 600 is only one minute of flying, not the hour. An hour has 60 minutes, so we need 60 lots of 600. 6 times 6 is 36, with three zeros: 36000 metres.",
             lab("c3", "1 hour = 60 minutes"), w("c4", "6 × 6 = 36"), w("c5", "60 × 600 = 36000")),
        beat("So in one hour the insect flies 36000 metres. A kilometre is 1000 metres. How many kilometres is 36000 metres?",
             lab("f", "1 km = 1000 m"),
             ask=choose(qid + "a2", "36 km", ["360 km", "3600 km"],
                        "A kilometre is a much bigger unit, so we need far fewer of them. Count the thousands in 36000: we divide by 1000.")),
        beat("36000 divided by 1000 is 36. So 10 metres per second is the same as 36 kilometres per hour.",
             w("c6", "36000 ÷ 1000 = 36"), answer("ans", "10 m/sec = 36 km/hr"), ring("ans", "36 km/hr")),
        beat("That is a handy pair to remember: 10 metres per second is 36 kilometres per hour. So 1 metre per second is 3.6 kilometres per hour.",
             w("s1", "36 ÷ 10 = 3.6")),
        beat("So for metres per second into kilometres per hour: find how far it goes in an hour, in metres, then divide by 1000."),
    ])


def fp_2021_033(q):
    """6:20 p.m. to 8:50 p.m. at 212.5 m/s (1912.5 km)"""
    qid = q["id"]
    return lesson("authored", [
        beat("An aeroplane leaves Mumbai at 6 20 p m and lands in Dubai at 8 50 p m. It flies at 212.5 metres per second. How far apart are the two cities?",
             given("q1", "Leaves 6:20 p.m., arrives 8:50 p.m."), given("q2", "Speed 212.5 m/s. Distance = ? km"),
             fig("f1", {"kind": "journey", "places": ["Mumbai", "Dubai"], "legs": [{"top": "? km", "bottom": "6:20 to 8:50"}]})),
        beat("First we need the flying time. Count on from 6 20 in friendly jumps. How long is it until 8 50?",
             ask=choose(qid + "a1", "2 hours 30 minutes", ["2 hours 70 minutes", "3 hours 30 minutes"],
                        "Jump from 6 20 to 8 20 first: that is 2 whole hours. Then from 8 20 to 8 50 is 30 minutes more.")),
        beat("From 6 20 to 8 20 is 2 hours. From 8 20 to 8 50 is 30 minutes more. So the flight lasts 2 hours 30 minutes.",
             fig("f2", {"kind": "journey", "places": ["6:20", "8:20", "8:50"], "legs": [{"top": "2 hours"}, {"top": "30 minutes"}]}),
             lab("c1", "Flying time = 2 hours 30 minutes")),
        beat("Now look at the speed: metres per second. Hours and seconds do not mix. So what should we change the flying time into?",
             mark("q2", "m/s"),
             ask=choose(qid + "a2", "seconds", ["minutes", "leave it in hours"],
                        "The speed tells us the distance for each second. To use it, we need to know how many seconds the flight lasts.")),
        beat("2 hours is 120 minutes, and 30 more makes 150 minutes. Each minute is 60 seconds, so 150 times 60 is 9000 seconds.",
             w("c2", "2 × 60 = 120"), w("c3", "120 + 30 = 150"), w("c4", "150 × 60 = 9000")),
        beat("Every second the plane flies 212.5 metres, so in 9000 seconds it flies 212.5 times 9000 metres. Let's do 212.5 times 9 first.",
             lab("r", "Distance = speed × time"), w("c5", "212.5 × 9000 = ?")),
        beat("200 times 9 is 1800. 12.5 times 9 is 112.5. Together, that makes 1912.5.",
             w("m1", "200 × 9 = 1800"), w("m2", "12.5 × 9 = 112.5"), w("m3", "1800 + 112.5 = 1912.5")),
        beat("We multiplied by 9, not 9000, so the distance is 1912.5 thousand metres. And here is the nice part: 1000 metres is exactly 1 kilometre.",
             w("m4", "212.5 × 9000 = 1912.5 × 1000"), lab("f", "1000 m = 1 km")),
        beat("So 1912.5 thousand metres is 1912.5 kilometres. That is the distance from Mumbai to Dubai.",
             answer("ans", "Distance = 1912.5 km"), ring("ans", "1912.5 km")),
        beat("Sense check. At about 200 metres per second we got 1800, and the real speed is a little more. So 1912.5 kilometres is sensible."),
        beat("So: find the time by counting on, put it in the same unit as the speed, multiply, then change the answer into the unit the question wants."),
    ])


def fp_2022_012(q):
    """Train 120 m long at 36 km/hr passes a pole (12 seconds)"""
    qid = q["id"]

    def table(minute, second):
        return {"kind": "table", "headers": ["time", "distance"],
                "rows": [["1 hour", "36000 m"], ["1 minute", minute], ["1 second", second]]}

    return lesson("authored", [
        beat("A train 120 metres long runs at 36 kilometres per hour. In how many seconds will it pass a pole?",
             given("q1", "Train 120 m long, speed 36 km/hr"), given("q2", "Passes a pole in ? seconds")),
        beat("From the moment the front reaches the pole until the back end clears it, how far does the train travel?",
             ask=choose(qid + "a1", "120 metres, its own length", ["36 kilometres", "0 metres, the pole stands still"],
                        "The pole stays put, so the whole train has to slide past it. The train moves forward exactly its own length, 120 metres.")),
        beat("So we need the time to travel 120 metres. But the speed is in kilometres per hour, and we want metres and seconds. Let's bring the speed down, one step at a time.",
             mark("q1", "120 m"), mark("q1", "km/hr")),
        beat("In 1 hour the train goes 36 kilometres. 1 kilometre is 1000 metres, so that is 36000 metres.",
             lab("f", "1 km = 1000 m"), w("c1", "36 × 1000 = 36000"), fig("f1", table("?", "?"))),
        beat("An hour is 60 minutes. Share 36000 metres over 60 minutes, and the train goes 600 metres in each minute.",
             w("c2", "36000 ÷ 60 = 600"), fig("f1", table("600 m", "?"))),
        beat("A minute is 60 seconds. Share 600 metres over 60 seconds, and the train goes 10 metres in each second.",
             w("c3", "600 ÷ 60 = 10"), lab("c4", "36 km/hr = 10 m/s"), fig("f1", table("600 m", "10 m"))),
        beat("10 metres every second, and 120 metres to travel. What do we work out?",
             ask=choose(qid + "a2", "120 ÷ 10", ["120 × 10", "120 ÷ 36"],
                        "Each second takes care of 10 metres. Count how many lots of 10 fit into 120.")),
        beat("120 divided by 10 is 12. The train passes the pole in 12 seconds.",
             w("c5", "120 ÷ 10 = 12"), answer("ans", "Time = 12 seconds"), ring("ans", "12 seconds")),
        beat("Check it. 12 seconds, at 10 metres each second, is 120 metres. Exactly one train length.",
             w("chk", "12 × 10 = 120")),
        beat("So for a train passing a pole: the distance is its own length, the speed goes into metres per second, and then time is distance divided by speed."),
    ])


def fp_2022_030(q):
    """600 metres in 25 sec; distance in 1 hour (86.4 km, so None of these)"""
    qid = q["id"]
    return lesson("authored", [
        beat("A car travels 600 metres in 25 seconds. We want to know how far it goes in 1 hour.",
             given("q1", "600 metres in 25 seconds"), given("q2", "Distance in 1 hour = ?")),
        beat("25 seconds and 1 hour are far apart, so take a stepping stone: 1 second. How do we find how far the car goes in 1 second?",
             ask=choose(qid + "a1", "600 ÷ 25", ["600 × 25", "600 − 25"],
                        "The 600 metres are spread evenly over 25 seconds. One second's share is 600 split into 25 equal parts.")),
        beat("There are 4 lots of 25 in every 100. 600 is 6 hundreds, so that is 6 times 4, which is 24. The car goes 24 metres every second.",
             w("c1", "100 ÷ 25 = 4"), w("c2", "6 × 4 = 24"), w("c3", "600 ÷ 25 = 24")),
        beat("1 hour is 60 times 60 seconds, which is 3600 seconds. So we need 24 times 3600.",
             w("c4", "60 × 60 = 3600"), lab("c5", "1 hour = 3600 seconds")),
        beat("First 24 times 36. 20 times 36 is 720, and 4 times 36 is 144. Together, 864. Put the two zeros back: 86400 metres in 1 hour.",
             w("m1", "20 × 36 = 720"), w("m2", "4 × 36 = 144"), w("m3", "720 + 144 = 864"), w("m4", "24 × 3600 = 86400")),
        beat("The choices are in kilometres. 1000 metres make 1 kilometre. What is 86400 metres in kilometres?",
             lab("f", "1 km = 1000 m"),
             ask=choose(qid + "a2", "86.4 km", ["864 km", "8.64 km"],
                        "Dividing by 1000 moves every digit three places to the right. 86400 becomes 86.4.")),
        beat("86400 divided by 1000 is 86.4. So the car covers 86.4 kilometres in 1 hour.",
             w("c6", "86400 ÷ 1000 = 86.4")),
        beat("Now look closely at the choices: 84.6, 80 and 85.4. Careful, 84.6 looks very like our 86.4, but the digits are swapped. Our answer is not on the list.",
             lab("c7", "Choices: 84.6 km, 80 km, 85.4 km")),
        beat("So the right choice is none of these. When your working is sound, trust it, even if the answer is not on the list.",
             answer("ans", "86.4 km: None of these"), ring("ans", "None of these")),
        beat("Here is the plan again: go down to 1 second, build up to 3600 seconds, change metres to kilometres, then compare carefully with the choices."),
    ])


def fp_2023_003(q):
    """5 rounds of 400 m: 100 m at 4 m/s, 300 m at 5 m/s (7 min 5 s, so none of these)"""
    qid = q["id"]

    def track(first, second):
        return {"kind": "journey", "places": ["Start", "100 m mark", "Finish"],
                "legs": [{"top": "100 m", "bottom": first}, {"top": "300 m", "bottom": second}]}

    return lesson("authored", [
        beat("Shraddha runs 5 rounds of a 400 metre track. In every round she runs the first 100 metres at 4 metres per second, and the other 300 metres at 5 metres per second. How long do the 5 rounds take?",
             given("q1", "5 rounds of a 400 m track"), given("q2", "Each round: 100 m at 4 m/s, 300 m at 5 m/s"), given("q3", "Total time = ?"),
             fig("f1", track("4 m/s", "5 m/s"))),
        beat("Every round is the same, so let's time just one round, in two parts, because she changes speed. First part: 100 metres, at 4 metres each second. How many seconds?",
             ask=choose(qid + "a1", "100 ÷ 4", ["100 × 4", "100 − 4"],
                        "Each second she covers 4 metres. So we count how many lots of 4 fit into 100, and that is a division.")),
        beat("100 divided by 4 is 25 seconds. The second part works the same way: 300 divided by 5 is 60 seconds.",
             lab("r", "Time = distance ÷ speed"), w("c1", "100 ÷ 4 = 25"), w("c2", "300 ÷ 5 = 60"),
             fig("f1", track("25 seconds", "60 seconds"))),
        beat("So one round takes 25 plus 60, which is 85 seconds. Notice we timed each part with its own speed. Dividing the whole 400 by one speed would not work, because the speed changes.",
             w("c3", "25 + 60 = 85"), lab("c4", "1 round: 85 seconds")),
        beat("Now 5 rounds. 80 times 5 is 400, and 5 times 5 is 25. So 85 times 5 is 425 seconds.",
             w("m1", "80 × 5 = 400"), w("m2", "5 × 5 = 25"), w("m3", "85 × 5 = 425")),
        beat("The choices are in minutes and seconds. A minute is 60 seconds. So what is 425 seconds?",
             lab("f", "1 minute = 60 seconds"),
             ask=choose(qid + "a2", "7 minutes 5 seconds", ["4 minutes 25 seconds", "7 minutes 25 seconds"],
                        "A minute is 60 seconds, not 100, so we cannot just split 425 into 4 and 25. Count in lots of 60 instead: 7 of them fit, and 5 seconds are left.")),
        beat("7 times 60 is 420. That leaves 5 seconds. So 425 seconds is 7 minutes 5 seconds.",
             w("c5", "7 × 60 = 420"), w("c6", "425 = 7 × 60 + 5")),
        beat("Now look at the choices: 6 minutes 45, 7 minutes 15, and 7 minutes 25. Close, but none of them is 7 minutes 5 seconds.",
             lab("c7", "Choices: 6 min 45 s, 7 min 15 s, 7 min 25 s")),
        beat("So the right choice is none of these. Our working is sound, so we trust it.",
             answer("ans", "7 min 5 s: none of these"), ring("ans", "none of these")),
        beat("The plan: time one round, a part at a time. Multiply by the number of rounds. Then change seconds into minutes using 60, not 100."),
    ])


def fp_2024_008(q):
    """680 km in 8 hours; back 17 km/hr slower (600 minutes)"""
    qid = q["id"]
    return lesson("authored", [
        beat("Nirav travels 680 kilometres from A to B in 8 hours. Coming back, he drives 17 kilometres per hour slower. How long does the return journey take?",
             given("q1", "A to B: 680 km in 8 hours"), given("q2", "B to A: 17 km/hr slower. Time = ?"),
             fig("f1", {"kind": "journey", "places": ["A", "B"], "legs": [{"top": "680 km", "bottom": "8 hours"}]})),
        beat("To slow a speed down, we first need to know the speed. Speed means how far in one hour. How do we find his speed from A to B?",
             ask=choose(qid + "a1", "680 ÷ 8", ["680 × 8", "680 − 8"],
                        "The 680 kilometres are spread evenly over 8 hours. One hour's share is 680 split into 8 equal parts.")),
        beat("680 is 640 and 40. 640 divided by 8 is 80, and 40 divided by 8 is 5. So he drives 85 kilometres every hour.",
             w("c1", "640 ÷ 8 = 80"), w("c2", "40 ÷ 8 = 5"), w("c3", "680 ÷ 8 = 85"), lab("c4", "A to B: 85 km/hr")),
        beat("On the way back he is 17 kilometres per hour slower. 85 minus 17 is 68 kilometres per hour.",
             w("c5", "85 − 17 = 68"), lab("c6", "B to A: 68 km/hr"),
             fig("f1", {"kind": "journey", "places": ["B", "A"], "legs": [{"top": "680 km", "bottom": "? hours"}],
                        "note": "68 km in every hour"})),
        beat("It is the same road, so the distance back is still 680 kilometres. Now he covers 68 kilometres each hour. How many hours will it take?",
             ask=choose(qid + "a2", "680 ÷ 68", ["680 ÷ 17", "8 + 17"],
                        "Each hour takes care of 68 kilometres. Count how many lots of 68 fit into 680.")),
        beat("68 times 10 is 680. So the return journey takes 10 hours.",
             w("c7", "68 × 10 = 680"), w("c8", "680 ÷ 68 = 10")),
        beat("Careful, we are not finished: the choices are in minutes. 1 hour is 60 minutes, so 10 hours is 10 times 60, which is 600 minutes.",
             lab("f", "1 hour = 60 minutes"), w("c9", "10 × 60 = 600"), answer("ans", "Time = 600 minutes"), ring("ans", "600 minutes")),
        beat("Sense check. He drove slower on the way back, so it should take longer than the 8 hours going. 10 hours is longer. Good."),
        beat("So: find the first speed, change it, then use the new speed with the same distance. And always read which unit the choices want."),
    ])


def fp_2024_023(q):
    """6:45 pm to 9:15 pm at 32.5 m/s (292.5 km)"""
    qid = q["id"]
    return lesson("authored", [
        beat("A train leaves London at 6 45 p m and reaches Paris at 9 15 p m. Its speed is 32.5 metres per second. How far is it from London to Paris?",
             given("q1", "Leaves 6:45 pm, arrives 9:15 pm"), given("q2", "Speed 32.5 m/s. Distance = ? km"),
             fig("f1", {"kind": "clock", "hour": 6, "minute": 45, "note": "The train leaves at 6:45 pm"})),
        beat("First, the journey time. Count on from 6 45 in friendly jumps: up to 7 o'clock, on to 9 o'clock, then the last bit to 9 15. How long is that altogether?",
             ask=choose(qid + "a1", "2 hours 30 minutes", ["3 hours 30 minutes", "2 hours 15 minutes"],
                        "Careful: 6 45 is nearly 7 o'clock, so it is less than 3 hours to 9 15. Jump 15 minutes to 7, then 2 hours to 9, then 15 minutes more.")),
        beat("15 minutes takes us to 7 o'clock. 2 hours takes us to 9 o'clock. 15 more minutes takes us to 9 15. That is 2 hours and 30 minutes.",
             fig("f2", {"kind": "journey", "places": ["6:45", "7:00", "9:00", "9:15"],
                        "legs": [{"top": "15 min"}, {"top": "2 hours"}, {"top": "15 min"}]}),
             w("c1", "15 + 15 = 30"), lab("c2", "Journey time = 2 hours 30 minutes")),
        beat("The speed is in metres per second, but our time is in hours and minutes. Those do not mix. What is a good way to fix it?",
             mark("q2", "m/s"),
             ask=choose(qid + "a2", "find how far it goes in 1 hour", ["multiply 32.5 by 2 hours 30 minutes"],
                        "32.5 metres is what the train does in 1 second, so we cannot multiply it by hours. First let's find what it does in a whole hour.")),
        beat("1 hour is 60 times 60 seconds, which is 3600. So in one hour the train goes 32.5 times 3600 metres.",
             w("c3", "60 × 60 = 3600"), w("c4", "32.5 × 3600 = ?")),
        beat("3600 is 4 times 9 times 100, so we can multiply in easy steps. 32.5 times 4 is 130. 130 times 9 is 1170. Times 100 gives 117000 metres.",
             w("m1", "4 × 9 × 100 = 3600"), w("m2", "32.5 × 4 = 130"), w("m3", "130 × 9 = 1170"), w("m4", "1170 × 100 = 117000")),
        beat("1000 metres make 1 kilometre, so 117000 metres is 117 kilometres. The train's speed is 117 kilometres per hour.",
             lab("f", "1 km = 1000 m"), w("c5", "117000 ÷ 1000 = 117"), lab("c6", "32.5 m/s = 117 km/hr"), mark("c6", "117 km/hr", "box")),
        beat("Now the units match. 2 hours at 117 kilometres per hour is 234 kilometres. Half an hour is half of 117, which is 58.5 kilometres.",
             w("d1", "117 × 2 = 234"), w("d2", "117 ÷ 2 = 58.5")),
        beat("234 plus 58.5 is 292.5. So London to Paris is 292.5 kilometres.",
             w("d3", "234 + 58.5 = 292.5"), answer("ans", "Distance = 292.5 km"), ring("ans", "292.5 km")),
        beat("Check with the whole time at once. 2 and a half hours, times 117, is 292.5. It matches.",
             w("chk", "2.5 × 117 = 292.5")),
        beat("So: count on to find the time, make the speed and the time use the same units, then distance is speed times time."),
    ])


def fp_2025_008(q):
    """Crosses a pole in 28 seconds at 108 km/hr; length of train (840 m)"""
    qid = q["id"]
    return lesson("authored", [
        beat("A train running at 108 kilometres per hour crosses a pole in 28 seconds. We want the length of the train.",
             given("q1", "Speed 108 km/hr, crosses a pole in 28 seconds"), given("q2", "Length of train = ? m")),
        beat("While the train crosses the pole, from its front reaching the pole to its back end clearing it, how far does it travel?",
             ask=choose(qid + "a1", "exactly its own length", ["108 kilometres", "28 metres"],
                        "The pole stands still while the whole train slides past. So the train moves forward by exactly one train length.")),
        beat("So the length of the train is the distance it covers in 28 seconds. But the speed is per hour, and our time is in seconds. Let's change the speed into metres per second.",
             lab("c0", "Length = distance covered in 28 seconds"), mark("q1", "km/hr"),
             fig("f1", {"kind": "journey", "places": ["Pole", "Front of train"], "legs": [{"top": "? m", "bottom": "28 seconds"}]})),
        beat("In 1 hour the train goes 108 kilometres. 1 kilometre is 1000 metres, so that is 108000 metres.",
             lab("f", "1 km = 1000 m"), w("c1", "108 × 1000 = 108000")),
        beat("An hour has 60 minutes, and 108000 shared over 60 is 1800 metres each minute. A minute has 60 seconds, and 1800 shared over 60 is 30 metres each second.",
             w("c2", "108000 ÷ 60 = 1800"), w("c3", "1800 ÷ 60 = 30"), lab("c4", "108 km/hr = 30 m/s"), mark("c4", "30 m/s", "box")),
        beat("Now the units match. 30 metres every second, for 28 seconds. What do we work out?",
             ask=choose(qid + "a2", "30 × 28", ["108 × 28", "28 ÷ 30"],
                        "Every second adds another 30 metres, so 28 seconds means 28 lots of 30. And we use 30, the speed in metres per second, so that the units match.")),
        beat("3 times 28 is 84, so 30 times 28 is 840. The train is 840 metres long.",
             w("c5", "3 × 28 = 84"), w("c6", "30 × 28 = 840"), answer("ans", "Length of train = 840 m"), ring("ans", "840 m")),
        beat("Check it. 840 metres, at 30 metres each second, takes 840 divided by 30, which is 28 seconds. That matches.",
             w("chk", "840 ÷ 30 = 28")),
        beat("So when a train crosses a pole, the distance is the train's own length. Get the speed into metres per second, then multiply by the seconds."),
    ])


def fp_2025_027(q):
    """432 km at 24 m/s (5 hours, so None of these)"""
    qid = q["id"]
    return lesson("authored", [
        beat("We need to cover 432 kilometres, travelling at 24 metres per second. How much time will that take?",
             given("q1", "432 km at 24 m/s"), given("q2", "Time = ?")),
        beat("Look at the units before anything else. The distance is in kilometres, but the speed is in metres per second. What should we do first?",
             mark("q1", "km"), mark("q1", "m/s"),
             ask=choose(qid + "a1", "make the units match", ["divide 432 by 24"],
                        "432 divided by 24 would mix kilometres with metres, and the answer would mean nothing. First we make the units match.")),
        beat("The choices are in hours, so let's turn the speed into kilometres per hour. That means: how far does it go in one hour? 1 hour is 60 times 60 seconds, which is 3600.",
             w("c1", "60 × 60 = 3600"), lab("c2", "1 hour = 3600 seconds")),
        beat("Each second it goes 24 metres, so we need 24 times 3600. 20 times 36 is 720, 4 times 36 is 144, and together 864. With the two zeros, 86400 metres.",
             w("m1", "20 × 36 = 720"), w("m2", "4 × 36 = 144"), w("m3", "720 + 144 = 864"), w("m4", "24 × 3600 = 86400")),
        beat("1000 metres make 1 kilometre, so 86400 metres is 86.4 kilometres. The speed is 86.4 kilometres per hour.",
             lab("f", "1 km = 1000 m"), w("c3", "86400 ÷ 1000 = 86.4"), lab("c4", "24 m/s = 86.4 km/hr"), mark("c4", "86.4 km/hr", "box")),
        beat("Now both are in kilometres and hours. Each hour covers 86.4 kilometres, and we have 432 to go. Have a guess: roughly how many hours?",
             ask=choose(qid + "a2", "about 5 hours", ["about 18 hours", "about 50 hours"],
                        "Round both numbers to something friendly, and see how many of the smaller one fit into the bigger one. Then we test the guess by multiplying.")),
        beat("Let's test 5. 80 times 5 is 400, and 6.4 times 5 is 32. Together, 432. Exactly right.",
             w("t1", "80 × 5 = 400"), w("t2", "6.4 × 5 = 32"), w("t3", "86.4 × 5 = 432")),
        beat("So the journey takes 5 hours.",
             w("c5", "432 ÷ 86.4 = 5"), lab("c6", "Time = 5 hours")),
        beat("Now the choices: 4 hours 40 minutes, 5.5 hours, and 4 hours. 5 hours is not there, so the right choice is none of these.",
             lab("c7", "Choices: 4 hr 40 min, 5.5 hours, 4 hrs"), answer("ans", "5 hours: None of these"), ring("ans", "None of these")),
        beat("So: match the units first, then time is distance divided by speed. And trust careful working, even when the answer is not on the list."),
    ])


AUTHORED = {
    "EXT_G5_FP_2023_003": fp_2023_003,
    "EXT_G5_FP_2024_008": fp_2024_008,
    "EXT_G5_FP_2024_023": fp_2024_023,
    "EXT_G5_FP_2025_008": fp_2025_008,
    "EXT_G5_FP_2025_027": fp_2025_027,
    "EXT_G5_FP_2020_020": fp_2020_020,
    "EXT_G5_FP_2020_040": fp_2020_040,
    "EXT_G5_FP_2021_033": fp_2021_033,
    "EXT_G5_FP_2022_012": fp_2022_012,
    "EXT_G5_FP_2022_030": fp_2022_030,
    "EXT_G5_WS_B3_021": ws_b3_021,
    "EXT_G5_WS_B3_036": ws_b3_036,
    "EXT_G5_FP_2016_013": fp_2016_013,
    "EXT_G5_FP_2017_007": fp_2017_007,
    "EXT_G5_FP_2017_029": fp_2017_029,
    "EXT_G5_FP_2017_038": fp_2017_038,
    "EXT_G5_FP_2018_020": fp_2018_020,
    "EXT_G5_FP_2018_036": fp_2018_036,
    "EXT_G5_FP_2019_006": fp_2019_006,
    "EXT_G5_FP_2019_023": fp_2019_023,
}
