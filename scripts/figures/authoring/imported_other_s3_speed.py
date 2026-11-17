"""Speed, distance and time (gr5_speed): the journey as a road in stretches."""
from fractions import Fraction
from imported_other_lib import journey, leg, mins, staged

journey("7ce326980c6f", ["Hyderabad", "Stop 30 min", "Point B", "Vijayawada"],
        [leg(d=90, s=60), leg(d=120, s=80), leg(s=60, hd=60)], note="270 km in all. They leave at 7:00 AM. Arrival time = ?")
journey("dd1777aad834", ["Chennai", "Vellore 30 min", "Bangalore"], [leg(d=120, s=80), leg(d=240, s=120)],
        note="The train leaves at 6:00 AM. Arrival time = ?")
journey("ad89d80895a8", ["Home", "Halfway", "Station"], [leg(s=36, hd=9), leg(s=24, hd=9)],
        note="18 km in all, in two equal halves. Total minutes = ?")
journey("0dfa4359d91a", ["Home", "Grandmother"], [leg(d=30, s=10)],
        note="Deepa: 10 km/hr, one way. Arjun: 15 km/hr, three times the way")
journey("d9052a77bd67", ["Pune", "Chai 30 min", "Picnic spot"], [leg(s=40, t=2), leg(s=60, t=1)],
        note="Average speed for the whole trip, break included = ?")
journey("18234b041e34", ["Shore", "Island", "Shore"], [leg(s=6, t=mins(20), tl="20 min"), leg(s=4)],
        note="The same route there and back. Total time = ?")
journey("494f11811187", ["Start", "Turn", "Start"], [leg(d=3, s=15), leg(d=3, s=5)], note="Average speed for the whole trip = ?")
journey("d35305b5b385", ["Start", "Temple", "Start"], [leg(s=6, t=2), leg(s=12, hd=12)],
        note="Average speed, not counting the 1 hour of prayers = ?")
journey("d08dc12a1c73", ["Bangalore", "Dhaba", "Mysore"], [leg(d=75, s=50), leg(s=25, hd=75)],
        note="150 km in all. Average speed = ?")
journey("762057eb2571", ["Home", "Slow zone", "Village"], [leg(s=80), leg(s=40)], note="240 km in 4 hours. How far at 80 km/hr?")
journey("cc20a033d160", ["Start", "Turn", "Start"], [leg(d=18, t=2), leg(d=18, t=3)], note="Average speed for the round trip = ?")
journey("fd2916b35bc3", ["Bank", "Far bank", "Bank"], [leg(d=600, s=3), leg(d=600, s=2)], du="m", su="m/s",
        note="Average speed for the round trip = ?")
journey("2ac2b7d2e2cd", ["Jaipur", "Half the time", "Udaipur"], [leg(s=80), leg(s=40)],
        note="400 km. The same TIME at each speed. Average speed = ?")
journey("513758c9b397", ["School", "Halfway", "Park"], [leg(s=10, hd=30), leg(s=20, hd=30)],
        note="Kiran's ride. Priya rides all 60 km at 15 km/hr.")
journey("93924d069dfc", ["Pune", "Ghat", "Town", "End"],
        [leg(s=60, t=mins(45), tl="45 min"), leg(s=30, t=mins(40), tl="40 min"), leg(s=15, t=mins(20), tl="20 min")],
        note="Average speed for the whole journey = ?")
journey("fa6bfec7cb40", ["Pune", "Dhaba 30 min", "Mahabaleshwar"], [leg(d=60, s=60), leg(d=60, s=30)],
        note="120 km in all. Average speed, break included = ?")
journey("dac42c105c56", ["Jaipur", "Chai 30 min", "Udaipur"], [leg(s=80, t=2), leg(s=60, hd=240)],
        note="400 km in all. Total time, break included = ?")
journey("f7d971e33595", ["Home", "Market", "Friend"], [leg(s=10, t=mins(30), tl="30 min"), leg(s=6, t=mins(20), tl="20 min")],
        note="Total distance = ?")
journey("a9cb4a1aaf1c", ["Home", "Ground", "Home"], [leg(d=4, s=8), leg(d=4, s=4)], note="Total time there and back = ?")
journey("00b85ef1bbd3", ["Mysore", "Village"], [leg(d=24)],
        note="Deepa: 8:00 AM at 8 km/hr. Arjun: 8:30 AM at 12 km/hr.")
journey("ea9b483d01fc", ["Jaipur", "Halfway", "Dhaba"], [leg(s=60, hd=60), leg(s=40, hd=60)],
        note="120 km in all, in two equal halves. Total time = ?")
journey("99386bad9471", ["Start", "Temple", "Start"], [leg(s=18, t=mins(40), tl="40 min"), leg(s=12, hd=12)],
        note="Average speed, not counting the 30 minutes at the temple = ?")
journey("19b607aebd1b", ["Home", "Park", "Home"], [leg(d=6, s=6), leg(d=6, s=4)],
        note="Priya cycles both ways in the same total time. Her speed = ?")
journey("22c5f7f76efb", ["Delhi", "Signal", "Agra"], [leg(s=90, t=1, tl="1 h"), leg(s=60, t=mins(30), tl="30 min")],
        note="Average speed for the whole journey = ?")
journey("6d8fc378eefd", ["Pune", "Hills begin", "Hill station"], [leg(s=60, t=2), leg(s=30, t=1)],
        note="Average speed for the whole journey = ?")
journey("a286aa6f9dcb", ["Chennai", "Stop 30 min", "Bengaluru"], [leg(s=60, t=2), leg(s=90)],
        note="Leaves 7:30 AM, arrives 12:30 PM. Total distance = ?")
journey("3901d2bbe536", ["Neha", "Kavitha"], [leg(d=600)], du="m",
        note="They run towards each other: Neha at 5 m/s, Kavitha at 3 m/s")
journey("060e8e11c0d8", ["Chennai", "A", "B", "Bengaluru"], [leg(d=120, s=60), leg(d=80, s=40), leg(d=100, s=50)],
        note="Deepa's bus does all 300 km in the same time. Its speed = ?")
journey("db3b1a1ec170", ["Home", "Library", "Home"], [leg(d=24, s=12), leg(d=24, s=8)], note="Average speed for the whole trip = ?")
journey("2cf78ac8a526", ["Pune", "Chai 30 min", "Goa"], [leg(s=75, t=3), leg(s=50, hd=225)],
        note="450 km in all. Average speed, not counting the break = ?")
journey("6cf02d5cd394", ["Chennai", "Stop 30 min", "Bengaluru"], [leg(d=120, s=60), leg(d=240, s=80)],
        note="The train leaves at 6:15 AM. Arrival time = ?")
journey("f5558340ce4e", ["Delhi", "A", "B", "Agra"],
        [leg(s=90, t=mins(40), tl="40 min"), leg(s=60, t=mins(30), tl="30 min"), leg(s=120, t=mins(20), tl="20 min")],
        note="Total distance = ?")
journey("c218966ff709", ["Shop", "Customer 1", "Customer 2"], [leg(d=6, s=12), leg(d=4, s=8)],
        note="Average speed for the whole trip = ?")
journey("22e5cfdf8a40", ["Start", "Temple", "Start"], [leg(s=18, t=mins(40), tl="40 min"), leg(s=12, hd=12)],
        note="How many minutes does the trip back take?")
journey("2d5c24c3f7f8", ["Chennai", "Repairs begin", "Bengaluru"], [leg(s=90), leg(s=60)],
        note="360 km in 5 hours. How far at the slower speed?")
journey("090d5246eaa3", ["Chennai", "Chai 30 min", "Traffic", "Pondicherry"], [leg(d=60, s=40), leg(d=60, s=60), leg(d=30, s=15)],
        note="150 km in all. Average speed, chai stop included = ?")
journey("1a6b0085e7db", ["House", "Main road", "Station"], [leg(s=15, t=mins(20), tl="20 min"), leg(s=30, t=mins(30), tl="30 min")],
        note="Total distance = ?")
journey("a8eb5d429699", ["Jaipur", "Lunch 30 min", "Udaipur"], [leg(s=60, t=3), leg(s=80, hd=240)],
        note="420 km in all. Average speed, not counting lunch = ?")
journey("84abe609cb03", ["House", "Market", "House"], [leg(s=4), leg(s=20)], note="The round trip takes 3 hours. How far is the market?")
journey("651929f1dfb6", ["Start", "Temple"], [leg(s=12)],
        note="Houseboat: 1 hour 30 minutes. Arjun: same way in 1 hour 12 minutes")
journey("12e4894d07ee", ["Home", "Catch-up point"], [leg(dl="? km")],
        note="Grandfather walks at 3 km/hr. Ravi starts 20 minutes later at 5 km/hr.")
journey("16bb5fe2098b", ["Home", "Midway", "School"], [leg(s=30, t=mins(10), tl="10 min"), leg(s=60, t=mins(10), tl="10 min")],
        note="Total distance = ?")

# A walk round a rectangular park: the picture is the park.
staged("630d3c6e25fb", {"kind": "rectangle", "length": "400 m", "breadth": "200 m", "proportion": 2,
                        "note": "Once round the boundary at 3 km/hr. Minutes = ?"},
       [(1200, [{"kind": "rectangle", "length": "400 m", "breadth": "200 m", "proportion": 2, "highlight": ["border"],
                 "note": "Once round: 400 + 200 + 400 + 200 = 1200 m"},
                {"kind": "rectangle", "length": "400 m", "breadth": "200 m", "proportion": 2, "highlight": ["border"],
                 "note": "Once round is the whole boundary: two lengths and two breadths"}])], origin="authored")
