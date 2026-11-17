"""Hand-written narration for the imported Grade 5 geometry questions, where the rules do not give a line
a teacher would say.

SLOTS  one string, keyed by "<question id>:<slot>" where slot is q, o0..o3, h0..h2, s0, s1, ...
LINES  one string, keyed by the exact printed text (used wherever that text appears in an imported question).

A step may say the numbers of its text, or of its text followed by its maths line (see the README).
"""

_A = "AIGEN_grade5_"
_T = "IPMTB_grade5_"

SLOTS = {
    # ── Story problems ──────────────────────────────────────────────────────────────────────────
    _A + "0cefe8e7-7fc1-4460-b97e-d0a2d511127e:s2":
        "Now find the sides of the smaller tile. Each side is half the corresponding side of the garden triangle. "
        "The tile sides are 12 divided by 2, 16 divided by 2, and 20 divided by 2. "
        "That is 6 centimetres, 8 centimetres, and 10 centimetres.",
    _A + "2d8106ce-086a-4ba1-a8ae-c35ec1451036:s2":
        "Now list all three angles: 45 degrees, 65 degrees, and 70 degrees. Check each one: are any of them 90 degrees or more?",
    _A + "55700548-8de3-454e-9cda-14843e62777a:s1":
        "Since each tile is 1 metre by 1 metre, with an area of 1 square metre, the number of tiles needed equals the area. "
        "Number of tiles equals 45.",
    # A numbered list of three questions inside the question.
    _A + "7f314a77-bc15-46f9-81aa-6aa186eb0fd5:q":
        "Arjun is building a triangular frame out of colored sticks for a Pongal decoration. "
        "He picks sticks of lengths 9 centimetres, 12 centimetres, and 15 centimetres. "
        "After building the triangle, his teacher asks him three questions. "
        "Question 1: What type of triangle is it, based on its angles? "
        "Question 2: What is the perimeter? "
        "Question 3: If Arjun cuts the longest stick into two equal pieces, and tries to form a new triangle "
        "using these two pieces and the 9 centimetre stick, is that possible? "
        "Which of the following correctly answers all three questions?",
    # Three checks printed side by side on the maths line.
    _A + "7f314a77-bc15-46f9-81aa-6aa186eb0fd5:s4":
        "We need to check if a triangle can be formed with sides 7.5 centimetres, 7.5 centimetres, and 9 centimetres, "
        "using the Triangle Inequality Rule: the sum of any two sides must be greater than the third side. "
        "7.5 plus 7.5 equals 15, which is greater than 9. "
        "7.5 plus 9 equals 16.5, which is greater than 7.5. "
        "And 9 plus 7.5 equals 16.5, which is greater than 7.5.",
    _A + "8b35f7a2-1834-4508-a1e2-d5e13234deb9:s2":
        "The perimeter of the inner triangle is: a over 2, plus b over 2, plus c over 2. "
        "That equals a plus b plus c, all divided by 2, which is 84 divided by 2, or 42 centimetres.",
    # The maths lines name the angles with labels a voice cannot read; said in words instead.
    _A + "b2c0c32e-ebf3-4701-abe4-09f931109c0d:s0":
        "We have a triangle formed by the two parts of the kite string and the ground. "
        "The three angles of this triangle are: Priya's angle, 52 degrees, the kite's angle, 34 degrees, and Arjun's interior angle. "
        "Together, these three angles add up to 180 degrees.",
    _A + "b2c0c32e-ebf3-4701-abe4-09f931109c0d:s1":
        "Find Arjun's interior angle of the triangle. It equals 180 degrees, minus 52 degrees, minus 34 degrees, which is 94 degrees.",
    _A + "b2c0c32e-ebf3-4701-abe4-09f931109c0d:s2":
        "The question asks for the angle that the string on Arjun's side makes with the ground. "
        "Since Arjun stands on the ground and the string goes upward, the angle between the string and the ground "
        "is the interior angle of the triangle at Arjun's position. That angle is 94 degrees.",
    # A recurring decimal on the maths line.
    _A + "e9d46e9a-a871-492a-8574-e37fd925328d:s1":
        "Simplify and solve for x. 3 x plus 20 equals 180, so 3 x equals 160, so x equals 53 point 3 recurring, degrees.",
    # The printed question is longer than a narration may be; said a little more briefly, nothing left out of the maths.
    _A + "c16897be-8e91-47cf-99d3-4f234b1fd14d:q":
        "Tanvi is designing a triangular pennant flag for Republic Day. "
        "It must be isosceles, with two sides equal. "
        "The angle between the two equal sides is 40 degrees. "
        "She plans to sew lace along the longest side only. "
        "Her friend Sahil says, I need to know if the longest side is an equal side or the unequal side, before I cut the lace! "
        "Sahil works out all three angles. Then he notices: if Tanvi increases the angle between the equal sides to 100 degrees, "
        "keeping the triangle isosceles, the longest side switches! "
        "What is the difference between the two base angles of the new triangle, with the 100 degree angle, "
        "and the two base angles of the original triangle, with the 40 degree angle?",

    # ── Textbook, angles (chapter 18) ───────────────────────────────────────────────────────────
    _T + "ch18_q011:s6":
        "90 degrees equals 90 degrees. Yes! Option C adds up to exactly 90 degrees, so 50 degrees and 40 degrees are complementary!",
    _T + "ch18_q019:s1":
        "We're given one angle as 37 and a half degrees. Let's write that as a fraction to make subtraction easier. "
        "37 and a half degrees equals 75 over 2 degrees.",
    _T + "ch18_q022:s2":
        "Count the gaps between 12 and 4: from 12 to 1, 1 to 2, 2 to 3, and 3 to 4. That's 4 gaps.",
    _T + "ch18_q026:q":
        "If the measure of two complementary angles are x degrees and x plus x degrees. Find the value of x.",
    _T + "ch18_q027:h2":
        "Here's a similar problem: Which pair is not supplementary? "
        "50 degrees and 130 degrees: 50 plus 130 equals 180 degrees. Supplementary! "
        "90 degrees and 80 degrees: 90 plus 80 equals 170 degrees. Not supplementary! "
        "See? The pair that doesn't add to 180 degrees is the answer.",
    _T + "ch18_q029:s1":
        "An obtuse angle is any angle greater than 90 degrees but less than 180 degrees. "
        "So let's say one angle is obtuse, meaning: angle A is more than 90 degrees and less than 180 degrees.",
    _T + "ch18_q029:s2":
        "Since the two angles add up to 180 degrees, we can find the other angle: angle B equals 180 degrees minus angle A.",
    _T + "ch18_q035:h1":
        "A full circle is 360 degrees. The four main compass directions, North, East, South and West, "
        "divide the circle into 4 equal parts. What is 360 degrees divided by 4?",
    _T + "ch18_q035:s2":
        "Each neighboring pair of compass directions is separated by 90 degrees. "
        "The pairs are: North and East, East and South, South and West, and West and North.",
    _T + "ch18_q036:s0":
        "Let's recall the types of angles based on their measurements: an acute angle is more than 0 degrees and less than 90 degrees.",
    _T + "ch18_q036:s2":
        "An obtuse angle is bigger than a right angle, but smaller than a straight line, 180 degrees. "
        "So it is more than 90 degrees and less than 180 degrees.",

    # ── Textbook, perimeter (chapter 19) ────────────────────────────────────────────────────────
    _T + "ch19_q007:s1":
        "Use the perimeter formula for a rectangle and substitute l equals b plus 5. "
        "P equals 2 times, l plus b. So 50 equals 2 times, b plus 5 plus b.",

    # ── Textbook, area (chapter 20) ─────────────────────────────────────────────────────────────
    _T + "ch20_q001:h1":
        "Convert 1.2 metres into centimetres first. Remember: 1 metre equals 100 centimetres. "
        "So 1.2 metres equals how many centimetres?",
    _T + "ch20_q007:h1":
        "Start by letting the breadth be b. Then length equals 3 over 2, times b. "
        "Plug both into the perimeter formula: 2 times, length plus breadth, equals 50.",
    _T + "ch20_q007:s1":
        "Use the perimeter formula. Perimeter equals 2 times, Length plus Breadth, which is 50 centimetres. "
        "So 2 times, 3 over 2 b plus b, equals 50.",
    _T + "ch20_q007:s2":
        "Simplify inside the brackets. 3 over 2 times b, plus b, equals 3 b over 2 plus 2 b over 2, which is 5 b over 2. "
        "So 2 times 5 b over 2 equals 50.",
    _T + "ch20_q008:q":
        "Which playground is bigger? Playground 1: rectangular shape, having length 25 metres and breadth 20 metres. "
        "Playground 2: square shape, having each side 22 metres.",
    # The maths line ends in a round thousand, which cannot be read (see the rules file); the colon becomes a full stop.
    _T + "ch20_q010:s2":
        "Now, levelling charges are 5 rupees per square metre. Multiply the area by the rate to get the total cost.",
    _T + "ch20_q012:s0":
        "Write down what we know: Area equals 5 square centimetres. Height equals 2 centimetres. "
        "Base equals what? This is what we need to find.",
    _T + "ch20_q014:s3":
        "The area of the new rectangle is: 3 a over 2, times a over 2, which equals 3 a squared, over 4.",
    _T + "ch20_q014:s4":
        "Let's compare! The square's area is a squared, and the rectangle's area is three quarters of a squared. "
        "Since three quarters equals 0.75, the rectangle's area is only 75 percent of the square's area. That's 25 percent less!",
    _T + "ch20_q021:s4":
        "Since both the base and height are in centimetres, the area is in square centimetres. "
        "So the area equals 7.54 square centimetres.",
    _T + "ch20_q022:s2":
        "Let's multiply step by step. Break 6.1 times 6.1 into parts, using the identity: "
        "a plus b, all squared, equals a squared, plus 2 a b, plus b squared, where a equals 6 and b equals 0.1. "
        "So 6.1 squared equals 6 squared, plus 2 times 6 times 0.1, plus 0.1 squared. "
        "That is 36 plus 1.2 plus 0.01, which is 37.21.",
    _T + "ch20_q025:s5":
        "Option C says 60 millimetres, that's our height! Also notice that height is a length, so it should be in length units, "
        "millimetres, centimetres or metres, not in square centimetres or square millimetres. "
        "Option C is the only one with a proper length unit and the right value.",
    _T + "ch20_q027:h1":
        "Start by finding the side length: since a square has 4 equal sides, divide the perimeter by 4. "
        "So side equals 52 divided by 4, which is how many millimetres?",
    _T + "ch20_q027:s2":
        "Pay attention to the units! The perimeter was given in millimetres, so the side is in millimetres, "
        "and the area will be in square millimetres.",
}

LINES = {
}
