"""Hand-written lines for imported measurement-speed questions, where the rules in
measurement_speed_imported.py do not give a line a teacher would say.

HAND[question id] = {"q": str, "options": {index: str}, "hints": {index: str}, "steps": {index: str}}
Only the strings listed here are replaced; every other string of the question goes through the rules.
"""

P = "AIGEN_grade5_"

HAND = {
    P + "005fc3f8-e2b5-4c4a-85d9-7ce326980c6f": {"steps": {
        5: "Add up all the times: driving plus break. 1 hour 30 minutes, plus 30 minutes, plus 1 hour 30 minutes, "
           "plus 1 hour, equals 4 hours 30 minutes.",
    }},
    P + "033e5e03-1780-45bd-b614-2ff77ce829e4": {"steps": {
        1: "Going to Pondicherry, with the distance split equally. First half: 60 kilometres at 40 kilometres per hour. "
           "Second half: 60 kilometres at 60 kilometres per hour. Time 1 equals 60 divided by 40, which is 1.5 hours. "
           "Time 2 equals 60 divided by 60, which is 1 hour.",
        2: "Total time going there equals 1.5 plus 1, which is 2.5 hours. Average speed going there: "
           "120 divided by 2.5, which is 48 kilometres per hour.",
        4: "But the return distance is also 120 kilometres, so 50 T equals 120, giving T equals 2.4 hours. "
           "Average speed coming back equals 120 divided by 2.4, which is 50 kilometres per hour.",
        5: "We can also see this directly: when time is split equally, the average speed is simply the arithmetic mean "
           "of the two speeds. Average speed coming back equals 40 plus 60, all divided by 2, which is 50 kilometres per hour.",
    }},
    P + "10d2ce3d-f46f-486a-8d20-0dfa4359d91a": {"steps": {
        1: "Find the total distance Arjun travels. He cycles from home to grandma's, 30 kilometres, then from grandma's "
           "back home, 30 kilometres, then from home to grandma's again, 30 kilometres. "
           "Arjun's total distance equals 30 plus 30 plus 30, which is 90 kilometres.",
    }},
    P + "2ba5dc32-4f7d-4ba2-b99e-762057eb2571": {
        "hints": {
            0: "Think about it this way: if you call the distance at 80 kilometres per hour d, then the remaining distance "
               "at 40 kilometres per hour is 240 minus d. The total time for both parts equals 4 hours.",
            1: "Write the time equation: d divided by 80, plus, open bracket, 240 minus d, close bracket, divided by 40, "
               "equals 4. Now try to solve for d!",
            2: "Here's a similar problem, solved. A car travels a total of 180 kilometres. It goes at 60 kilometres per hour "
               "for the first part, and 30 kilometres per hour for the rest, taking 4 hours total. Let the first distance be x. "
               "Then x over 60, plus, open bracket, 180 minus x, close bracket, over 30, equals 4. Multiply everything by 60: "
               "x plus 2 times, open bracket, 180 minus x, close bracket, equals 240. So x plus 360 minus 2 x equals 240. "
               "So minus x equals minus 120, which gives x equals 120 kilometres, at 60 kilometres per hour. "
               "Use the same approach for your problem!",
        },
        "steps": {
            0: "Let the distance travelled at 80 kilometres per hour be d kilometres. Then the distance at 40 kilometres "
               "per hour is 240 minus d kilometres. d, plus 240 minus d, equals 240.",
            1: "Write the time equation. Time equals distance divided by speed. Total time is 4 hours. "
               "d over 80, plus, open bracket, 240 minus d, close bracket, over 40, equals 4.",
        },
    },
    P + "4c99bde9-c14b-4e70-aa8f-93924d069dfc": {"steps": {
        5: "Total time: three quarters plus two thirds plus one third, which is three quarters plus 1, "
           "which is 7 over 4 hours, or 1 hour 45 minutes.",
    }},
    P + "597a64d3-34f5-4bb7-8a42-f7d971e33595": {"hints": {
        2: "Here's a similar problem. If someone walks at 8 kilometres per hour for 15 minutes, and then at 4 kilometres "
           "per hour for 30 minutes, the first distance is 8 times 15 over 60, which is 8 times 0.25, or 2 kilometres. "
           "The second is 4 times 30 over 60, which is 4 times 0.5, or 2 kilometres. That gives a total of 4 kilometres.",
    }},
    P + "6ce388ca-8012-4430-aaed-00b85ef1bbd3": {"hints": {
        1: "In 30 minutes, Deepa covers 8 times 0.5, which is 4 kilometres. Now Arjun gains on her at a rate of "
           "12 minus 8 kilometres per hour. How long does it take him to close a 4-kilometre gap?",
    }},
    P + "7c4fc3bc-d48a-4421-952e-19b607aebd1b": {"steps": {
        5: "So Priya cycles at 4.8 kilometres per hour! Notice this is not the simple average of 6 and 4, which would be 5. "
           "When distances are equal, we use the harmonic mean formula: 2 times a times b, divided by, open bracket, "
           "a plus b, close bracket. That is 2 times 6 times 4, divided by, open bracket, 6 plus 4, close bracket, "
           "which is 48 divided by 10, or 4.8.",
    }},
    P + "7dad391b-e598-40db-bb55-7906d0be05d0": {"hints": {
        2: "Here's a similar problem: A boat goes 10 kilometres downstream at 5 kilometres per hour, taking 2 hours. "
           "It returns at 4 kilometres per hour, taking 10 divided by 4, which is 2.5 hours. A cyclist covers "
           "12 kilometres at 6 kilometres per hour, taking 2 hours. The cyclist is faster by 0.5 hours, which is 30 minutes. "
           "See how we compared the two travel times?",
    }},
    P + "9abd6007-86c6-467f-b518-630d3c6e25fb": {"hints": {
        1: "The perimeter of a rectangle equals 2 times, open bracket, length plus width, close bracket. "
           "Calculate this in metres, then convert to kilometres before using the speed.",
    }},
    P + "9f8bd7db-3343-405c-b559-a286aa6f9dcb": {"steps": {
        0: "Find the total journey time from 7 30 a m to 12 30 p m. 12 30, minus 7 30, equals 5 hours.",
    }},
    P + "9fab80d7-4e4f-464f-bccd-3901d2bbe536": {"hints": {
        1: "Time to meet equals total distance, divided by Neha's speed plus Kavitha's speed. That is 600 divided by, "
           "open bracket, 5 plus 3, close bracket. Then find how far Neha ran in that time.",
    }},
    P + "a954701c-ebae-486b-be8d-2cf78ac8a526": {"hints": {
        1: "Start by finding the expressway distance: 75 kilometres per hour times 3 hours equals how many kilometres? "
           "Then subtract from 450 kilometres to get the ghat road distance.",
    }},
    P + "b1cb3843-2972-4747-99e6-6cf02d5cd394": {"hints": {
        1: "Start by finding the time for the first 120 kilometres: time equals distance divided by speed, "
           "which is 120 divided by 60. How many hours is that?",
    }},
    P + "b30339a8-4dda-4ae6-bd0f-f5558340ce4e": {"hints": {
        1: "Convert each time from minutes to hours by dividing by 60. For example, 40 minutes equals "
           "40 divided by 60 hours, which is two thirds of an hour.",
    }},
    P + "bfca9ba2-08fe-452f-8f60-22e5cfdf8a40": {"hints": {
        2: "Here's a similar problem. A cyclist rides at 15 kilometres per hour for 20 minutes to reach a park. "
           "She returns at 10 kilometres per hour. How long does the return take? First, 20 minutes is one third of an hour, "
           "so the distance is 15 times one third, which is 5 kilometres. Then, the return time is 5 divided by 10, "
           "which is half an hour, or 30 minutes. See the pattern?",
    }},
    P + "cabecb79-a128-4dda-b5ee-2d5c24c3f7f8": {
        "hints": {
            2: "Here's a similar problem. A car travels 200 kilometres total. It goes at 50 kilometres per hour for part, "
               "and 40 kilometres per hour for the rest, taking 4.5 hours total. If the fast part is d, then d over 50, "
               "plus, open bracket, 200 minus d, close bracket, over 40, equals 4.5. Solving: 4 d over 200, plus 5 times, "
               "open bracket, 200 minus d, close bracket, over 200, equals 4.5. So 4 d plus 1000 minus 5 d equals 900, "
               "which gives d equals 100 kilometres. So the slower part is 100 kilometres. "
               "Try the same approach for Rohan's train!",
        },
        "steps": {
            1: "Write the total time equation, using time equals distance divided by speed. "
               "d 1 over 90, plus d 2 over 60, equals 5.",
            3: "Substitute into the time equation. Open bracket, 360 minus d 2, close bracket, over 90, "
               "plus d 2 over 60, equals 5.",
        },
    },
    P + "e0aab10d-53f6-4e15-b3c9-090d5246eaa3": {"steps": {
        1: "The chai stop lasts 30 minutes, which is 0.5 hours.",
    }},
    P + "eae4d773-e97d-467f-91eb-84abe609cb03": {"hints": {
        2: "Here's a similar problem. Suppose someone cycles 6 kilometres per hour one way, and 12 kilometres per hour back, "
           "and the total time is 3 hours. Then d over 6, plus d over 12, equals 3. So, open bracket, 2 d plus d, "
           "close bracket, over 12, equals 3. So 3 d equals 36, which gives d equals 12 kilometres. "
           "Use the same method for your question!",
    }},
    P + "ec5a09e1-2ca2-4258-8914-651929f1dfb6": {
        "hints": {
            1: "The houseboat goes downstream at 12 kilometres per hour for 1.5 hours. What distance is that? "
               "Distance equals speed times time.",
        },
        "steps": {
            1: "Convert Arjun's travel time to hours. 1 hour 12 minutes equals 1 plus 12 over 60 hours. "
               "So 1 hour 12 minutes is 1 plus 12 divided by 60, which is 1.2 hours.",
        },
    },
    P + "f181bd86-5d01-4cda-bc40-12e4894d07ee": {"hints": {
        2: "Here's a similar problem. If person A starts walking at 2 kilometres per hour, and person B starts 30 minutes "
           "later at 5 kilometres per hour, then A's head start is 2 times 30 over 60, which is 1 kilometre. "
           "B gains on A at 5 minus 2, which is 3 kilometres per hour. Time for B to catch up is 1 divided by 3, "
           "which is one third of an hour. Distance B covers is 5 times one third, which is 5 over 3, "
           "or about 1.67 kilometres.",
    }},
}
