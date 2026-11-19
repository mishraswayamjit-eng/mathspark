"""Lines written by hand for gr4_triangles, keyed "<question id>:<slot>".

Slots: q, o0..o3 (options), h0..h2 (hints), s0.. (steps). Anything not listed here is narrated by
the rules in gr4_triangles_rules.py.
"""

HAND = {
    # ── Past papers: the printed questions are in note form, so they are read as full sentences.
    "EXT_G4_FP_2022_018:q": "A right triangle has base 19 centimetres and height 16 centimetres. What is its area?",
    "EXT_G4_FP_2023_001:q": "Two sides of a triangle are 20 centimetres and 15 centimetres. Which cannot be the perimeter?",
    "EXT_G4_FP_2025_014:q": "Which base and height of a triangle give an area equal to a square of side 9 centimetres?",
    "EXT_G4_FP_2025_014:o0": "Base 12, height 4",
    "EXT_G4_FP_2025_014:o1": "Base 18, height 8",
    "EXT_G4_FP_2025_014:o2": "Base 12, height 14",
    "EXT_G4_FP_2025_014:o3": "Base 27, height 6",
    "EXT_G4_FP_2025_014:s4": "So the triangle with base 27 and height 6 has the same area as the square.",

    # ── Newly written questions.
    "G4A_TRIANGLES_018:h2": "Similar problem: in an isosceles triangle one angle is 2 times another and no angle is a right angle. "
                            "Parts 1, 1, 2 give 45 degrees, 45 degrees, 90 degrees, which has a right angle. "
                            "Parts 1, 2, 2 give 5 parts, which make 180 degrees, so one part is 36 degrees. "
                            "The smallest angle is 36 degrees.",
    "G4A_TRIANGLES_027:s0": "If the right angle were 4 times another angle, that angle would not be a whole number. "
                            "90 divided by 4 equals 22 and a half.",
}

# ── The hand-written chapter questions (Q_CH19_001 to 025): their hints and steps are in note form.
HAND.update({
    "Q_CH19_001:h1": "The sum of angles in any triangle is 180 degrees. If all 3 are equal: 180 degrees divided by 3 equals what?",
    "Q_CH19_001:h2": "180 degrees divided by 3 equals 60 degrees. Each angle is 60 degrees.",
    "Q_CH19_001:s0": "All 3 angles are equal. The sum is 180 degrees.",
    "Q_CH19_001:s1": "Each angle is 180 degrees divided by 3, which is 60 degrees.",
    "Q_CH19_001:s2": "Each angle is 60 degrees.",
    "Q_CH19_002:h0": "The perimeter is the sum of all sides. An equilateral triangle has 3 equal sides.",
    "Q_CH19_002:h1": "The perimeter is 3 times the side, which is 3 times 7.",
    "Q_CH19_002:s0": "Equilateral means all sides are equal, each 7 centimetres.",
    "Q_CH19_002:s1": "The perimeter is 3 times 7, which is 21 centimetres.",
    "Q_CH19_003:h0": "The sum of all three angles in a triangle is 180 degrees.",
    "Q_CH19_003:s0": "The sum is 180 degrees. 35 degrees plus 65 degrees plus what equals 180 degrees?",
    "Q_CH19_003:s1": "The missing angle is 180 degrees minus 35 degrees minus 65 degrees. "
                     "That is 180 degrees minus 100 degrees, which is 80 degrees.",
    "Q_CH19_004:s1": "107 degrees is greater than 90 degrees, so it is an obtuse angle.",
    "Q_CH19_004:s2": "The triangle is obtuse-angled.",
    "Q_CH19_005:h1": "A: 2 plus 5 equals 7, which is less than 9. It fails! "
                     "B: 6 plus 8 equals 14, which is greater than 12. 6 plus 12 equals 18, which is greater than 8. "
                     "8 plus 12 equals 20, which is greater than 6. "
                     "C: 1 plus 5 equals 6, which is equal to 6, not greater.",
    "Q_CH19_005:s0": "The rule: the sum of any 2 sides is greater than the third side. a plus b is greater than c.",
    "Q_CH19_005:s1": "A: 2 plus 5 equals 7, which is less than 9. It fails.",
    "Q_CH19_005:s2": "B: 6 plus 8 equals 14, which is greater than 12. All pairs work.",
    "Q_CH19_005:s3": "C: 1 plus 5 equals 6, which is equal to 6. It must be strictly greater.",
    "Q_CH19_006:h0": "Isosceles means at least two angles must be equal.",
    "Q_CH19_006:h1": "Check: A has 30, 60, 90, none equal. B has 50, 90, 40, none equal. "
                     "C has 40, 120, 20, none equal. D has 30, 75, 75, two equal!",
    "Q_CH19_006:h2": "D is isosceles. Check the sum: 30 plus 75 plus 75 equals 180 degrees.",
    "Q_CH19_007:h0": "In a right triangle, one angle is 90 degrees. The other two must add up to 90 degrees, "
                     "since the total is 180 degrees.",
    "Q_CH19_007:h2": "The other angle is 90 degrees minus 27 degrees, which is 63 degrees.",
    "Q_CH19_007:s0": "In a right triangle, 90 degrees plus the two acute angles equals 180 degrees.",
    "Q_CH19_007:s1": "The other acute angle is 90 degrees minus 27 degrees, which is 63 degrees.",
    "Q_CH19_008:h0": "One angle is 90 degrees, the right angle. The other two are equal, because it is isosceles.",
    "Q_CH19_008:s0": "90 degrees plus 2 x equals 180 degrees: the right angle plus two equal angles. "
                     "So 2 x equals 180 degrees minus 90 degrees, which is 90 degrees.",
    "Q_CH19_008:s1": "x equals 45 degrees. x equals 90 degrees divided by 2, which is 45 degrees.",
    "Q_CH19_008:s2": "Each equal angle is 45 degrees.",
    "Q_CH19_009:h1": "Equilateral means all angles are 60 degrees. But right-angled means one angle is 90 degrees. "
                     "Can one angle be both 60 degrees and 90 degrees?",
    "Q_CH19_009:s0": "Equilateral: all angles are 60 degrees. Right-angled: one angle is 90 degrees. "
                     "60 degrees is not equal to 90 degrees.",
    "Q_CH19_009:s1": "These two properties contradict each other. It is impossible!",
    "Q_CH19_010:h0": "Obtuse means one angle is greater than 90 degrees. Scalene means all three angles are different.",
    "Q_CH19_010:h1": "A has 90 degrees, so it is right, not obtuse. B has 90 degrees, so it is right. "
                     "C: 120 degrees is greater than 90 degrees, so it is obtuse, and all angles are different, so it is scalene! "
                     "D has two 15 degree angles, so it is isosceles, not scalene.",
    "Q_CH19_010:s0": "We need one angle greater than 90 degrees, which is obtuse, and all angles different, which is scalene.",
    "Q_CH19_010:s1": "C: 120 degrees is greater than 90 degrees, so it is obtuse. "
                     "40 degrees, 120 degrees and 20 degrees are all different, so it is scalene.",
    "Q_CH19_011:h1": "The exterior angle is 55 degrees plus 70 degrees.",
    "Q_CH19_011:s0": "The exterior angle theorem: the exterior angle equals the sum of the two remote interior angles. "
                     "That is 55 degrees plus 70 degrees.",
    "Q_CH19_011:s2": "Verify: the third interior angle is 180 degrees minus 55 degrees minus 70 degrees, which is 55 degrees. "
                     "The exterior angle is 180 degrees minus 55 degrees, which is 125 degrees.",
    "Q_CH19_012:h0": "The exterior angle equals the sum of the two remote interior angles.",
    "Q_CH19_012:h1": "130 degrees equals 50 degrees plus what?",
    "Q_CH19_012:h2": "The missing angle is 130 degrees minus 50 degrees, which is 80 degrees.",
    "Q_CH19_012:s0": "The exterior angle equals the sum of the remote interior angles: 130 degrees equals 50 degrees plus what?",
    "Q_CH19_012:s1": "The missing angle is 130 degrees minus 50 degrees, which is 80 degrees.",
    "Q_CH19_012:s2": "The other remote interior angle is 80 degrees.",
    "Q_CH19_013:h0": "The sum of the angles is 180 degrees. Both base angles are 70 degrees.",
    "Q_CH19_013:h1": "The vertex angle is 180 degrees minus 70 degrees minus 70 degrees.",
    "Q_CH19_013:s0": "The sum is 180 degrees. The base angles are 70 degrees each. "
                     "70 degrees plus 70 degrees plus the vertex angle equals 180 degrees.",
    "Q_CH19_013:s1": "The vertex angle is 180 degrees minus 140 degrees, which is 40 degrees.",
    "Q_CH19_014:h0": "The two base angles are equal. The vertex angle plus 2 times a base angle equals 180 degrees.",
    "Q_CH19_014:h1": "2 times the base angle is 180 degrees minus 50 degrees, which is 130 degrees.",
    "Q_CH19_014:h2": "The base angle is 130 degrees divided by 2, which is 65 degrees.",
    "Q_CH19_014:s0": "50 degrees plus 2 b equals 180 degrees. So 2 b equals 180 degrees minus 50 degrees, which is 130 degrees.",
    "Q_CH19_014:s2": "Each base angle is 65 degrees.",
    "Q_CH19_016:h2": "There is no axis of symmetry. The count is 0.",
    "Q_CH19_017:h0": "The perimeter is the sum of all three sides.",
    "Q_CH19_017:s0": "The perimeter is the first side, plus the second side, plus the third side. 8 plus 11 plus 15.",
    "Q_CH19_018:h0": "The perimeter is the sum of all sides. 36 equals 12 plus 9 plus the third side.",
    "Q_CH19_018:h1": "The third side is 36 minus 12 minus 9.",
    "Q_CH19_018:s0": "36 equals 12 plus 9 plus what? The missing side is 36 minus 12 minus 9.",
    "Q_CH19_018:s1": "The missing side is 15 centimetres.",
    "Q_CH19_019:h0": "The area of a right triangle is half of base times height. The two legs are the base and height!",
    "Q_CH19_019:h1": "The area is half of 6 times 8.",
    "Q_CH19_019:s0": "In a right triangle, the legs form the right angle, so they are the base and height. "
                     "The area is half of base times height.",
    "Q_CH19_019:s1": "The area is half of 6 times 8, which is 24 square centimetres.",
    "Q_CH19_019:s2": "The area is 24 square centimetres.",
    "Q_CH19_020:s1": "The answer is midpoint.",
    "Q_CH19_021:s0": "There is one median from each vertex. A triangle has 3 vertices. So 3 vertices give 3 medians.",
    "Q_CH19_022:s0": "The rule: the longest side is opposite the largest angle.",
    "Q_CH19_022:s1": "The largest angle is 80 degrees. The longest side is opposite 80 degrees.",
    "Q_CH19_023:o2": "No, because 90 degrees plus 90 degrees equals 180 degrees, leaving 0 degrees for the third angle",
    "Q_CH19_023:h0": "If two angles were 90 degrees each, their sum is 180 degrees. "
                     "But the total for all three angles must be 180 degrees!",
    "Q_CH19_023:h1": "That leaves 180 degrees minus 180 degrees, which is 0 degrees, for the third angle. "
                     "An angle of 0 degrees doesn't exist!",
    "Q_CH19_023:s0": "If two angles are 90 degrees each: 90 degrees plus 90 degrees equals 180 degrees.",
    "Q_CH19_024:h0": "Equilateral means all 3 sides are equal. The perimeter is 3 times the side.",
    "Q_CH19_024:h1": "The side is the perimeter divided by 3, which is 45 divided by 3.",
    "Q_CH19_024:s0": "The perimeter is 3 times the side. So 45 equals 3 times the side.",
    "Q_CH19_024:s1": "The side is 45 divided by 3, which is 15 centimetres.",
    "Q_CH19_025:h0": "The area is half of base times height. We know the area and the base, so find the height.",
    "Q_CH19_025:h1": "42 equals half of 12 times h. So 42 equals 6 h.",
    "Q_CH19_025:s0": "The area is half of base times height. 42 equals half of 12 times h.",
    "Q_CH19_025:s1": "42 equals 6 h.",
})
