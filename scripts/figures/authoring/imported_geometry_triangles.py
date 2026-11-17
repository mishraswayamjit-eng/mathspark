"""Figures for the imported Grade 5 Triangles questions (node gr5_triangles).
Run through imported_geometry.py.

A triangle whose sides or angles are all fixed by the question is drawn to that
shape. One whose shape is what the child has to work out (angles given only as
"3 times the second") is the renderer's plain triangle, so the picture does not
give the type away. Eight questions give sides and angles that cannot belong to
the same triangle; they are left without a figure (see the skips at the end)."""
from imported_geometry_lib import add, skip, T, P, BM, tri_sides, tri_angles, _tri_points
import math

SUM = "The three angles of a triangle add up to 180°"
ACUTE = "All three angles are less than 90°: an acute triangle"


def tri(a, b, c, note=None, sides=None, hl=None):
    """The plain triangle with angle labels a (top), b (left), c (right)."""
    return T("scalene", sides=sides, angles={"a": a, "b": b, "c": c}, note=note, hl=hl)


# ── Angles given by a rule: what type of triangle, or which angle is largest ──

def by_rule(key, top, left, right, ask, x_top, x_left, x_right, equation, true, s_x, s_eq, s_found, s_last, last_note):
    """`true` is (top, left, right) as (degrees, label) once the steps have found them."""
    (ta, la), (tb, lb), (tc, lc) = true
    add(key, figure=tri(top, left, right, note=ask), steps={
        s_x: tri(x_top, x_left, x_right),
        s_eq: tri(x_top, x_left, x_right, note=equation),
        s_found: tri_angles(ta, tb, tc, la, lb, lc),
        s_last: tri_angles(ta, tb, tc, la, lb, lc, note=last_note)})


OBTUSE_96 = ((96, "96°"), (32, "32°"), (52, "52°"))
by_rule("09382572", "3 × second", "second", "second + 20°", "What type of triangle is it?",
        "3x°", "x°", "(x + 20)°", "3x + x + (x + 20) = 180", OBTUSE_96, 0, 1, 5, 7, "96° is more than 90°: an obtuse angle")
by_rule("3a216919", "3 × smallest", "smallest", "smallest + 20°", "Largest angle = ?",
        "3x°", "x°", "(x + 20)°", "x + 3x + (x + 20) = 180", OBTUSE_96, 0, 1, 5, 6, "The largest angle is 96°")
by_rule("a125fe02", "3 × second", "second", "second + 20°", "Largest angle = ? What type of triangle is it?",
        "3x", "x", "x + 20°", "3x + x + (x + 20°) = 180°", OBTUSE_96, 1, 2, 4, 5, "96° is more than 90°: an obtuse triangle")
by_rule("c139ad61", "three × smallest", "smallest", "smallest + 20°", "What type of triangle is it?",
        "3x", "x", "(x + 20)°", "x + 3x + (x + 20) = 180", OBTUSE_96, 0, 1, 3, 4, "96° is more than 90°: an obtuse angle")
by_rule("cd2d25aa", "second + 25°", "second", "second + 15°", "What type of triangle is it?",
        "(x + 25)°", "x°", "(x + 15)°", "(x + 15) + x + (x + 25) = 180",
        ((215 / 3.0, "71⅔°"), (140 / 3.0, "46⅔°"), (185 / 3.0, "61⅔°")), 0, 1, 4, 6, "Every angle is less than 90°: an acute-angled triangle")

add("df22c72e",
    figure=tri("three × smallest", "smallest", "2 × smallest", note="Largest angle = ?"),
    steps={1: tri("3x", "x", "2x"),
           2: tri("3x", "x", "2x", note="x + 2x + 3x = 180°"),
           6: [tri_angles(60, 90, 30, "60°", "90°", "30°", note="The largest angle is 90°: a right angle"),
               tri_angles(60, 90, 30, "2x", "90°", "x", note="The largest angle is 90°: a right angle")]})

add("5c40eab7",
    figure=tri("2 × 50°", "50°", "?", note="What type of triangle is it?"),
    steps={0: tri("100°", "50°", "?", note="Twice 50° is 100°"),
           1: tri("100°", "50°", "?", note="100° + 50° + ? = 180°"),
           2: tri_angles(100, 50, 30, "100°", "50°", "30°", note="180° − 100° − 50° = 30°"),
           3: tri_angles(100, 50, 30, "100°", "50°", "30°", note="100° is more than 90°: an obtuse triangle")})

add("b0d31ddd",
    figure=tri("7 parts", "3 parts", "5 parts", sides={"ca": "12 m"}, note="The angles are in the ratio 3 : 5 : 7"),
    steps={0: tri("7x", "3x", "5x", note="3x + 5x + 7x = 180°"),
           3: tri_angles(84, 36, 60, "84°", "36°", "60°", note="3 × 12° = 36°, 5 × 12° = 60°, 7 × 12° = 84°"),
           5: tri_angles(84, 36, 60, "84°", "36°", "60°", note="All three are less than 90°: an acute-angled triangle")})


# ── Two angles given: the third, and often the type ──────────────────────────

add("1f04f2bb", origin="authored",
    figure=tri_angles(70, 55, 55, "70°", "55°", "?", note="Third angle = ? What type of triangle is it?"),
    steps={0: tri_angles(70, 55, 55, "70°", "55°", "?", note=SUM),
           1: tri_angles(70, 55, 55, "70°", "55°", "?", hl=["a", "b"], note="Add the two known angles: 55° + 70°"),
           2: tri_angles(70, 55, 55, "70°", "55°", "?", hl=["c"], note="? = 180° − 55° − 70°"),
           3: tri_angles(70, 55, 55, "70°", "55°", "55°", hl=["c"], note="180° − 55° − 70° = 55°"),
           4: tri_angles(70, 55, 55, "70°", "55°", "55°", note=ACUTE)})
add("2d8106ce", origin="authored",
    figure=tri_angles(70, 45, 65, "?", "45°", "65°", note="What type of triangle is it?"),
    steps={0: tri_angles(70, 45, 65, "?", "45°", "65°", note=SUM),
           1: tri_angles(70, 45, 65, "?", "45°", "65°", hl=["a"], note="? = 180° − 45° − 65°"),
           2: tri_angles(70, 45, 65, "70°", "45°", "65°", hl=["a"], note="180° − 45° − 65° = 70°"),
           3: tri_angles(70, 45, 65, "70°", "45°", "65°", note=ACUTE)})
add("4e7b0c83", origin="authored",
    figure=tri_angles(70, 50, 60, "70°", "50°", "60°", note="What type of triangle is it?"),
    steps={0: tri_angles(70, 50, 60, "70°", "50°", "60°", note="50° + 60° + 70° = 180°"),
           1: tri_angles(70, 50, 60, "70°", "50°", "60°", hl=["a", "b", "c"], note="Every angle is less than 90°")})
add("5e6fe38d", origin="authored",
    figure=tri_angles(67, 48, 65, "67°", "48°", "?", note="All three sides are different lengths"),
    steps={0: tri_angles(67, 48, 65, "67°", "48°", "?", hl=["c"], note="? = 180° − 48° − 67°"),
           1: tri_angles(67, 48, 65, "67°", "48°", "65°", note="48°, 67° and 65°: every angle is less than 90°"),
           2: tri_angles(67, 48, 65, "67°", "48°", "65°", hl=["ab", "bc", "ca"], note="All three sides are different: scalene")})
add("9460cd3a", origin="authored",
    figure=tri_angles(75, 50, 55, "75°", "?", "55°", note="Third angle = ? What type of triangle is it?"),
    steps={0: tri_angles(75, 50, 55, "75°", "?", "55°", note=SUM),
           1: tri_angles(75, 50, 55, "75°", "50°", "55°", hl=["b"], note="180° − 55° − 75° = 50°"),
           2: tri_angles(75, 50, 55, "75°", "50°", "55°", note=ACUTE)})
add("9b4803d2", origin="authored",
    figure=tri_angles(70, 50, 60, "70°", "?", "60°", note="What type of triangle is it?"),
    steps={0: tri_angles(70, 50, 60, "70°", "?", "60°", note=SUM),
           1: tri_angles(70, 50, 60, "70°", "?", "60°", hl=["b"], note="? = 180° − 60° − 70°"),
           2: tri_angles(70, 50, 60, "70°", "50°", "60°", hl=["b"], note="60°, 70° and 50°: every angle is less than 90°")})
add("cad77791", origin="authored",
    figure=tri_angles(55, 90, 35, "?", "90°", "35°"),
    steps={0: tri_angles(55, 90, 35, "?", "90°", "35°", note=SUM),
           1: tri_angles(55, 90, 35, "?", "90°", "35°", hl=["b", "c"], note="90° + 35° = 125°"),
           2: tri_angles(55, 90, 35, "?", "90°", "35°", hl=["a"], note="? = 180° − 125°"),
           3: tri_angles(55, 90, 35, "55°", "90°", "35°", hl=["a"], note="180° − 125° = 55°")})

# Two 60° angles: drawn as a plain shape (not named) so the picture does not say "equilateral".
for _key, _last in (("625e57c9", "All three angles are equal"), ("af918b14", "All three angles are equal, so all three sides are equal")):
    add(_key, origin="authored",
        figure=tri_angles(60, 60, 60, "?", "60°", "60°", poly=True, note="Third angle = ? What type of triangle is it?"),
        steps={0: tri_angles(60, 60, 60, "?", "60°", "60°", poly=True, note=SUM),
               1: tri_angles(60, 60, 60, "60°", "60°", "60°", poly=True, note="180° − 60° − 60° = 60°"),
               2: tri_angles(60, 60, 60, "60°", "60°", "60°", poly=True, note=_last)})
add("d510200e", origin="authored",
    figure=tri_angles(40, 70, 70, "?", "70°", "70°", poly=True, note="Third angle = ? Is the triangle acute? Is it isosceles?"),
    steps={0: tri_angles(40, 70, 70, "40°", "70°", "70°", poly=True, note="180° − 70° − 70° = 40°"),
           1: tri_angles(40, 70, 70, "40°", "70°", "70°", poly=True, note="Two angles are equal, so it is isosceles"),
           2: tri_angles(40, 70, 70, "40°", "70°", "70°", poly=True, note="All three are less than 90°, so it is acute")})

# The corners are where the story puts them: top, left on the ground, right on the ground.
add("7e937a6a", origin="authored",
    figure=tri_angles(52, 74, 54, "52°", "74°", "?"),
    steps={0: tri_angles(52, 74, 54, "52°", "74°", "?", note=SUM),
           1: tri_angles(52, 74, 54, "52°", "74°", "?", note="Add the two known angles: 52° + 74°"),
           2: tri_angles(52, 74, 54, "52°", "74°", "?", note="? = 180° − 52° − 74°"),
           3: tri_angles(52, 74, 54, "52°", "74°", "54°", note="180° − 52° − 74° = 54°")})
add("9207ef7a", origin="authored",
    figure=tri_angles(67, 65, 48, "?", "65°", "48°"),
    steps={0: tri_angles(67, 65, 48, "?", "65°", "48°", note="The plank and the two sticks make a triangle"),
           1: tri_angles(67, 65, 48, "?", "65°", "48°", note=SUM),
           2: tri_angles(67, 65, 48, "?", "65°", "48°", note="Add the two known angles: 65° + 48°"),
           3: tri_angles(67, 65, 48, "67°", "65°", "48°", note="180° − 65° − 48° = 67°")})
add("b2c0c32e", origin="authored",
    figure=tri_angles(34, 52, 94, "34°", "52°", "?", note="Kite at the top, 52° at Priya's end, ? at Arjun's end"),
    steps={0: tri_angles(34, 52, 94, "34°", "52°", "?", note=SUM),
           1: tri_angles(34, 52, 94, "34°", "52°", "94°", note="180° − 52° − 34° = 94°")})


# ── Isosceles triangles ──────────────────────────────────────────────────────

add("a41aeda1", origin="authored",
    figure=tri_angles(40, 70, 70, "40°", "?", "?", note="Two equal sides, so the two angles marked ? are equal"),
    steps={1: tri_angles(40, 70, 70, "40°", "?", "?", note=SUM),
           2: tri_angles(40, 70, 70, "40°", "?", "?", hl=["b", "c"], note="? + ? = 180° − 40° = 140°"),
           3: tri_angles(40, 70, 70, "40°", "70°", "70°", hl=["b", "c"], note="140° ÷ 2 = 70°")})
EQ5 = {"ab": "5 cm", "ca": "5 cm"}
add("7597470a", origin="authored",
    figure=tri_angles(80, 50, 50, "80°", "?", "?", sides=EQ5),
    steps={0: tri_angles(80, 50, 50, "80°", "?", "?", sides=EQ5, note=SUM),
           1: tri_angles(80, 50, 50, "80°", "?", "?", sides=EQ5, note="? + ? = 180° − 80° = 100°"),
           2: tri_angles(80, 50, 50, "80°", "?", "?", sides=EQ5, hl=["ab", "ca"], note="Equal sides face equal angles"),
           3: tri_angles(80, 50, 50, "80°", "50°", "50°", sides=EQ5, note="100° ÷ 2 = 50°")})
EQ7 = {"ab": "7 cm", "ca": "7 cm"}
add("df55bd02", origin="authored",
    figure=tri_angles(60, 60, 60, "60°", "?", "?", sides=EQ7, poly=True),
    steps={1: tri_angles(60, 60, 60, "60°", "?", "?", sides=EQ7, poly=True, hl=["ab", "ca"], note="Equal sides face equal angles"),
           2: tri_angles(60, 60, 60, "60°", "?", "?", sides=EQ7, poly=True, note="60° + ? + ? = 180°"),
           4: tri_angles(60, 60, 60, "60°", "60°", "60°", sides=EQ7, poly=True, note="All three angles are 60°: the triangle is equilateral")})
add("c16897be", origin="authored",
    figure=tri_angles(40, 70, 70, "40°", "?", "?", note="Then the top angle becomes 100°. How much do the ? angles change?"),
    steps={0: tri_angles(40, 70, 70, "40°", "70°", "70°", hl=["b", "c"], note="(180° − 40°) ÷ 2 = 70°"),
           1: tri_angles(100, 40, 40, "100°", "40°", "40°", note="(180° − 100°) ÷ 2 = 40°"),
           2: tri_angles(100, 40, 40, "100°", "40°", "40°", note="70° − 40° = 30°")})

add("87ad8698", origin="authored",
    figure=tri_sides(24, 16, 16, "side + 8 cm", "side", "side", note="Perimeter = 56 cm. Which side does the largest angle face?"),
    steps={0: tri_sides(24, 16, 16, "s + 8", "s", "s"),
           1: tri_sides(24, 16, 16, "s + 8", "s", "s", hl=["e0", "e1", "e2"], note="s + s + (s + 8) = 56"),
           3: tri_sides(24, 16, 16, "24 cm", "16 cm", "16 cm"),
           5: tri_sides(24, 16, 16, "24 cm", "16 cm", "16 cm", corners=["largest angle", None, None], hl=["e1"],
                        note="The largest angle faces the longest side")})


# ── Sides 6-8-10, 9-12-15, 12-16-20 ──────────────────────────────────────────

S6 = ("8 cm", "6 cm", "10 cm")
add("60493d60", origin="authored",
    figure=tri_sides(8, 6, 10, *S6, right_at_b=True, note="Name it by its sides, and by its angles"),
    steps={0: tri_sides(8, 6, 10, *S6, right_at_b=True, hl=["e0", "e1", "e2"], note="6 cm, 8 cm and 10 cm: are any two sides equal?"),
           2: tri_sides(8, 6, 10, *S6, right_at_b=True, hl=["e0", "e1"], note="The 6 cm and 8 cm sides meet at 90°")})
add("f2300d21", origin="authored",
    figure=tri_sides(8, 6, 10, *S6, note="What type of triangle is it?"),
    steps={0: tri_sides(8, 6, 10, *S6, hl=["e0", "e1"], note="Work out 6 × 6 + 8 × 8"),
           1: tri_sides(8, 6, 10, *S6, hl=["e2"], note="10 × 10 = 100"),
           2: tri_sides(8, 6, 10, *S6, right_at_b=True, hl=["e0", "e1"], note="So the 6 cm and 8 cm sides meet at a right angle")})

S12 = ("16 cm", "12 cm", "20 cm")
HALF12 = ("half of 16 cm", "half of 12 cm", "half of 20 cm")
add("0cefe8e7", origin="authored",
    figure=tri_sides(16, 12, 20, *S12, note="A tile has sides half as long. Add the largest angle of each."),
    steps={1: tri_sides(16, 12, 20, *S12, right_at_b=True, hl=["e0", "e1"], note="12² + 16² = 20², so the largest angle is 90°"),
           2: tri_sides(16, 12, 20, *HALF12, note="The tile: every side is half as long"),
           4: tri_sides(16, 12, 20, *HALF12, right_at_b=True, note="Same shape, so its largest angle is 90° too")})

S9 = ("12 cm", "9 cm", "15 cm")
add("7f314a77", origin="authored",
    figure=tri_sides(12, 9, 15, *S9, note="Its type? Its perimeter? Then the 15 cm stick is cut in half."),
    steps={1: tri_sides(12, 9, 15, *S9, right_at_b=True, hl=["e0", "e1"], note="9² + 12² = 15², so there is a right angle"),
           2: tri_sides(12, 9, 15, *S9, hl=["e0", "e1", "e2"], note=["9 + 12 + 15 = 36 cm", "Perimeter = 9 + 12 + 15"]),
           4: tri_sides(9, 7.5, 7.5, "9 cm", "7.5 cm", "7.5 cm", note="The two halves and the 9 cm stick"),
           5: tri_sides(9, 7.5, 7.5, "9 cm", "7.5 cm", "7.5 cm", hl=["e0", "e2"], note="The two halves reach past the 9 cm stick, so they can meet")})


# ── Can the sides make a triangle? Shown as sticks laid side by side. ────────

add("6cb0fd51", origin="authored",
    figure=BM([[(8, "8 cm", "a")], [(15, "15 cm", "b")], [(6, "6 cm", "a")]], note="Can these three sides close up into a triangle?"),
    steps={1: BM([[(8, "8 cm", "a")], [(15, "15 cm", "b")], [(6, "6 cm", "a")]], hl=["b1"], note="The longest side is 15 cm"),
           2: BM([[(15, "15 cm", "b")], [(8, "8 cm", "a"), (6, "6 cm", "a")]], note=["8 + 6 = 14", "Lay the two shorter sides end to end"]),
           3: BM([[(15, "15 cm", "b")], [(8, "8 cm", "a"), (6, "6 cm", "a")]], hl=["b1"], note="14 is less than 15: the two shorter sides cannot meet")})
add("8b6664e9", origin="authored",
    figure=BM([[(6, "6 m", "a")], [(6, "6 m", "a")], [(10, "10 m", "b")]], note="Can these three sides make a triangle?"),
    steps={0: BM([[(6, "6 m", "a")], [(6, "6 m", "a")], [(10, "10 m", "b")]], hl=["b0", "b1"], note="Two sides are equal"),
           2: BM([[(10, "10 m", "b")], [(6, "6 m", "a"), (6, "6 m", "a")]], hl=["b1"], note="6 + 6 = 12, which is more than 10"),
           5: tri_sides(10, 6, 6, "10 m", "6 m", "6 m", note="The two shorter sides reach past the longest, so they meet")})


# ── The triangle through the midpoints ───────────────────────────────────────

def midpoint_triangle(note=None, hl=None):
    a, b, c = (math.radians(v) for v in (70, 50, 60))
    A_, B_, C_ = _tri_points(math.sin(a), math.sin(c), math.sin(b))

    def mid(p, q):
        return ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)

    pts = [A_, mid(A_, B_), B_, mid(B_, C_), C_, mid(C_, A_)]
    return P(pts, corners=["70°", None, "50°", None, "60°", None], dashed=[(1, 3), (3, 5), (5, 1)], note=note, hl=hl)


add("8b35f7a2", origin="authored",
    figure=midpoint_triangle("Outer triangle: perimeter 84 cm. The dashed one joins the midpoints."),
    steps={1: midpoint_triangle("Each dashed side is half of the side it runs beside"),
           2: midpoint_triangle("84 ÷ 2 = 42 cm"),
           4: midpoint_triangle("Same shape at half the size: still 50°, 60° and 70°")})


# ── Left without a figure: the question's sides and angles cannot both be true ──

skip("28e0cae9", "contradiction", "sides 5, 5, 7 m put about 89° between the equal sides, not the stated 84°")
skip("5293d35a", "contradiction", "sides 8, 10, 15 cm make angles of about 112°, 38°, 30°, not the stated 108° and 27°")
skip("73792540", "contradiction", "sides 5, 5, 7 cm make base angles of about 46°, not the stated 55°")
skip("7f275cb5", "contradiction", "sides 5, 5, 8 cm make angles of about 106°, 37°, 37°: no angle is the stated 110°")
skip("c29423a2", "contradiction", "sides 32, 32, 20 cm put about 36° between the equal sides, not the stated 40°")
skip("d316dfa5", "contradiction", "sides 8, 8, 15 cm make base angles of about 20°, not the stated 28°")
skip("d38bd58a", "contradiction", "angles 2 : 3 : 5 make a right angle, but sides 7, 9, 13 cm do not (49 + 81 is not 169)")
skip("e9d46e9a", "contradiction", "sides 20, 20, 15 cm put about 44° between the equal sides; the angle rule gives about 73°")
