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

# ── The hand-written chapter questions whose hints and steps are still in note form.
HAND.update({
    "Q_CH19_009:h1": "Equilateral means all angles are 60 degrees. But right-angled means one angle is 90 degrees. "
                     "Can one angle be both 60 degrees and 90 degrees?",
    "Q_CH19_009:s0": "Equilateral: all angles are 60 degrees. Right-angled: one angle is 90 degrees. "
                     "60 degrees is not equal to 90 degrees.",
    "Q_CH19_009:s1": "These two properties contradict each other. It is impossible!",
    "Q_CH19_022:s0": "The rule: the longest side is opposite the largest angle.",
    "Q_CH19_022:s1": "The largest angle is 80 degrees. The longest side is opposite 80 degrees.",
    "Q_CH19_023:o2": "No, because 90 degrees plus 90 degrees equals 180 degrees, leaving 0 degrees for the third angle",
    "Q_CH19_023:h0": "If two angles were 90 degrees each, their sum is 180 degrees. "
                     "But the total for all three angles must be 180 degrees!",
    "Q_CH19_023:h1": "That leaves 180 degrees minus 180 degrees, which is 0 degrees, for the third angle. "
                     "An angle of 0 degrees doesn't exist!",
    "Q_CH19_023:s0": "If two angles are 90 degrees each: 90 degrees plus 90 degrees equals 180 degrees.",
    "Q_CH19_025:h0": "The area is half of base times height. We know the area and the base, so find the height.",
    "Q_CH19_025:h1": "42 equals half of 12 times h. So 42 equals 6 h.",
    "Q_CH19_025:s0": "The area is half of base times height. 42 equals half of 12 times h.",
    "Q_CH19_025:s1": "42 equals 6 h.",
})
