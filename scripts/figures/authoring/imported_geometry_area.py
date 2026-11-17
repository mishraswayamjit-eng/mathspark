"""Figures for the imported Grade 5 Area & Perimeter questions (node gr5_area).
Run through imported_geometry.py."""
from imported_geometry_lib import add, skip, n, R, T, P, tri_sides, hexagon, l_shape, strip_frame

X = " × "


def area_notes(a, b, u, lead="Area"):
    return ["%s%s%s = %s sq. %s" % (n(a), X, n(b), n(a * b), u), "%s = %s%s%s" % (lead, n(a), X, n(b))]


# ── A rectangle with a piece taken out (corner or middle) ────────────────────

def cutout(key, length, breadth, u, cut_l, cut_b, thing, where, ask, s_whole=0, s_cut=1, s_left=2):
    """`where` is 'corner' (drawn as an L-shape) or 'middle' (the contract has no shape with a
    hole, so the piece is named inside the rectangle). The steps: whole area, piece, what is left."""
    dims = "%s %s%s%s %s" % (n(cut_l), u, X, n(cut_b), u)
    outer_sq = length == breadth
    whole, piece = length * breadth, cut_l * cut_b
    left_notes = ["%s − %s = %s sq. %s" % (n(whole), n(piece), n(whole - piece), u), "Whole area − the piece taken out"]
    L, B = "%s %s" % (n(length), u), "%s %s" % (n(breadth), u)
    if where == "corner":
        before = l_shape(length, breadth, cut_l, cut_b, L, B, dims, note=ask)
        left = l_shape(length, breadth, cut_l, cut_b, L, B, dims, note=left_notes, hl=["fill"])
    else:
        inside = "%s %s" % (thing, dims)
        if len(inside) > 24:
            inside = dims
        before = R(L, B, inside=inside, square=outer_sq, prop=length / breadth, note=ask)
        left = R(L, B, inside=inside, square=outer_sq, prop=length / breadth, note=left_notes)
    add(key, figure=before, steps={
        s_whole: R(L, B, square=outer_sq, prop=length / breadth, hl=["fill"], note=area_notes(length, breadth, u)),
        s_cut: R("%s %s" % (n(cut_l), u), "%s %s" % (n(cut_b), u), square=cut_l == cut_b, prop=cut_l / cut_b, hl=["fill"],
                 note=area_notes(cut_l, cut_b, u)),
        s_left: left})


cutout("0c769cf5", 12, 8, "m", 3, 3, "rangoli", "corner", "The rest is painted at ₹45 per sq. m. Cost = ?")
cutout("2f271f17", 15, 8, "cm", 5, 3, "diya", "corner", "Area covered with coloured powder = ?")
cutout("3490db5c", 12, 8, "cm", 4, 3, "diya", "corner", "Area left = ?")
cutout("46c8ae29", 12, 8, "m", 3, 3, "mat", "corner", "Each tile covers 500 sq. cm. Tiles for the rest = ?")
cutout("938739a9", 12, 8, "m", 3, 3, "rangoli", "corner", "Tiles are squares of side 50 cm. Tiles for the rest = ?")
cutout("9b1b91fa", 12, 8, "m", 2, 2, "pillar", "corner", "Tiles for the rest cost ₹15 per sq. m. Cost = ?")
cutout("ab9fa105", 9, 7, "m", 1.5, 1.5, "pillar", "corner", "Tiles cost ₹120 per sq. m. Cost for the rest = ?")
cutout("e478fc9b", 12, 9, "m", 1.5, 1.5, "pillar", "corner", "Tiles are squares of side 30 cm. Tiles for the rest = ?")
cutout("fb3af582", 90, 60, "cm", 30, 20, "piece", "corner", "Area left = ?")

cutout("05f02aa9", 9, 7, "m", 1.5, 1.5, "pillar", "middle", "Each tile covers 0.25 sq. m. Tiles for the rest = ?")
cutout("121d3f62", 12, 8, "m", 3, 3, "rangoli", "middle", "The rest is painted at ₹15 per sq. m. Cost = ?")
cutout("12e17c4c", 24, 18, "cm", 10, 10, "photo", "middle", "Area around the photo = ?")
cutout("2f3e11f6", 18, 12, "cm", 5, 5, "sticker", "middle", "Area not covered by the sticker = ?")
cutout("3a609c88", 12, 9, "m", 8, 5, "carpet", "middle", "Tiles are squares of side 50 cm. Tiles for the rest = ?")
cutout("479434d4", 12, 8, "m", 3, 3, "mat", "middle", "One can of paint covers 15 sq. m. Cans for the rest = ?")
cutout("65379f85", 8, 6, "m", 1, 1, "pillar", "middle", "Tiles: 25 cm squares at ₹12 each. Cost for the rest = ?")
cutout("70b6e4ec", 14, 14, "cm", 8, 5, "mirror", "middle", "Area not covered by the mirror = ?")
cutout("73cf3a7b", 20, 20, "cm", 12, 12, "square", "middle", "Area between the two squares = ?")
cutout("92e372bf", 24, 18, "cm", 10, 10, "photo", "middle", "Glitter costs ₹2 per sq. cm. Cost for the rest = ?")
cutout("ba446241", 8, 5, "m", 2, 2, "window", "middle", "Area to paint = ?")
cutout("ef6cb45e", 12, 9, "m", 3, 3, "rangoli", "middle", "Tiles cost ₹45 per sq. m. Cost for the rest = ?")
cutout("a87f8d98", 8, 5, "m", 2, 1, "window", "middle", "Paper needed for the rest of the wall = ?")
cutout("e0f58b33", 6, 4, "m", 1, 1, "window", "middle", "One can covers 5 sq. m. Cans for the rest = ?")

# A wall with two square windows and a door.
add("bec57c6e", origin="authored",
    figure=R("10 m", "4 m", inside="2 windows and 1 door", prop=2.5, note="Windows: 1.5 m squares. Door: 2 m by 3 m. Area to paint = ?"),
    steps={0: R("10 m", "4 m", prop=2.5, hl=["fill"], note=area_notes(10, 4, "m")),
           1: R("1.5 m", "1.5 m", square=True, hl=["fill"], note=["One window: 1.5 × 1.5 = 2.25 sq. m", "One window: 1.5 × 1.5"]),
           3: R("3 m", "2 m", prop=1.5, hl=["fill"], note=["Door: 2 × 3 = 6 sq. m", "Door: 2 × 3"])})
add("e3d6e974", origin="authored",
    figure=R("15 m", "8 m", inside="1 door and 2 windows", prop=15 / 8.0, note="Door: 2 m by 3 m. Windows: 1.5 m squares. Cans of paint = ?"),
    steps={0: R("15 m", "8 m", prop=15 / 8.0, hl=["fill"], note=area_notes(15, 8, "m")),
           1: R("3 m", "2 m", prop=1.5, hl=["fill"], note=["Door: 2 × 3 = 6 sq. m", "Door: 2 × 3"]),
           2: R("1.5 m", "1.5 m", square=True, hl=["fill"], note=["Two windows: 2 × 1.5 × 1.5 = 4.5 sq. m", "Two windows: 2 × 1.5 × 1.5"])})


# ── A path or border of the same width all round ─────────────────────────────

def minus2(a, w):
    return "%s − %s − %s" % (n(a), n(w), n(w))


def inner_strip(key, length, breadth, u, w, ask, whole_name, s_whole, s_len, s_wid, s_inner, s_last=None, last_note=None):
    """The strip runs round the INSIDE of a length × breadth rectangle."""
    W = "%s %s" % (n(w), u)
    steps = {
        s_whole: R("%s %s" % (n(length), u), "%s %s" % (n(breadth), u), prop=length / breadth, hl=["fill"], note=area_notes(length, breadth, u)),
        s_len: strip_frame(length, breadth, w, lwidth=W, lmid_top=minus2(length, w), hl=["e1"],
                           note="The strip takes %s off each end of the length" % W),
        s_wid: strip_frame(length, breadth, w, lwidth=W, lmid_left=minus2(breadth, w), hl=["e10"],
                           note="And %s off each end of the width" % W),
        s_inner: R("%s %s" % (minus2(length, w), u), "%s %s" % (minus2(breadth, w), u), prop=(length - 2.0 * w) / (breadth - 2.0 * w), hl=["fill"],
                   note=["%s%s%s = %s sq. %s" % (n(length - 2 * w), X, n(breadth - 2 * w), n((length - 2 * w) * (breadth - 2 * w)), u),
                         "Inner part = its length × its width"]),
    }
    if s_last is not None:
        steps[s_last] = strip_frame(length, breadth, w, lwidth=W, note=last_note)
    add(key, figure=strip_frame(length, breadth, w, lwidth=W, note=ask), steps=steps)


inner_strip("08bfdcbd", 18, 12, "m", 2, "Garden 18 m by 12 m. Path 2 m wide. Middle patch = ?", "garden", 0, 1, 2, 3)
inner_strip("37f1c808", 12, 8, "m", 1, "Courtyard 12 m by 8 m. Border 1 m wide. Border area = ?", "courtyard", 0, 1, 2, 3, 4,
            ["96 − 60 = 36 sq. m", "Border = whole courtyard − inner part"])
inner_strip("f5ea4cf7", 120, 80, "cm", 10, "Cloth 120 cm by 80 cm. Border 10 cm wide. Border area = ?", "cloth", 0, 1, 2, 3, 4,
            ["9600 − 6000 = 3600 sq. cm", "Border = whole cloth − inner part"])

add("75be410e",
    figure=strip_frame(20, 20, 2, lwidth="2 m", note="Courtyard 20 m by 20 m. Border 2 m wide. Powder fills the middle."),
    steps={0: strip_frame(20, 20, 2, lwidth="2 m", note="The border takes 2 m off every side"),
           1: strip_frame(20, 20, 2, lwidth="2 m", lmid_top="16 m", lmid_left="16 m", hl=["e1", "e10"], note="20 − 2 − 2 = 16 m"),
           2: R("16 m", "16 m", square=True, hl=["fill"], note=area_notes(16, 16, "m"))})

# The path runs round the OUTSIDE.
add("0866e5c1",
    figure=strip_frame(29, 29, 2, lwidth="2 m", note="Courtyard in the middle: 625 sq. m. Path 2 m wide. Path area = ?"),
    steps={0: R("25 m", "25 m", square=True, inside="625 sq. m", note="25 × 25 = 625, so each side is 25 m"),
           1: strip_frame(29, 29, 2, lwidth="2 m", lmid_top="25 m", note="25 + 2 + 2 = 29 m"),
           2: R("29 m", "29 m", square=True, hl=["fill"], note=area_notes(29, 29, "m")),
           3: strip_frame(29, 29, 2, lwidth="2 m", lmid_top="25 m", note=["841 − 625 = 216 sq. m", "Path = big square − courtyard"])})
add("f86da0d0",
    figure=strip_frame(130, 90, 5, lwidth="5 m", lmid_top="120 m", lmid_left="80 m",
                       note="The track runs all round the ground. Grass costs ₹12 per sq. m."),
    steps={0: R("120 m", "80 m", prop=1.5, note="The ground itself is the inner rectangle"),
           1: strip_frame(130, 90, 5, lwidth="5 m", lmid_top="120 m", lmid_left="80 m", note="Outer sides: 120 + 5 + 5 and 80 + 5 + 5"),
           2: R("120 + 5 + 5 m", "80 + 5 + 5 m", prop=130 / 90.0, hl=["fill"], note=area_notes(130, 90, "m", "Outer area")[:1] + ["Outer area = its length × its breadth"]),
           3: R("120 m", "80 m", prop=1.5, hl=["fill"], note=area_notes(120, 80, "m")),
           4: strip_frame(130, 90, 5, lwidth="5 m", lmid_top="120 m", lmid_left="80 m", note=["11700 − 9600 = 2100 sq. m", "Track = outer rectangle − ground"])})


# ── Plain rectangles ─────────────────────────────────────────────────────────

def plain(key, length, breadth, u, ask, s_area, extra=None, inside=None):
    L, B = "%s %s" % (n(length), u), "%s %s" % (n(breadth), u)
    steps = {s_area: R(L, B, prop=length / breadth, hl=["fill"], note=area_notes(length, breadth, u))}
    steps.update(extra or {})
    add(key, figure=R(L, B, prop=length / breadth, inside=inside, note=ask), steps=steps)


def tile(side, u, step):
    return {step: R("%s %s" % (n(side), u), "%s %s" % (n(side), u), square=True, hl=["fill"], note=area_notes(side, side, u, "One tile"))}


plain("03e12fba", 8, 5, "m", "Each sheet covers 4 sq. m. Sheets needed = ?", 0)
plain("2ccc6511", 12, 9, "m", "Each tile is a square of side 3 m. Tiles = ?", 0, tile(3, "m", 1))
plain("bfa55199", 12, 8, "m", "Each tile is a square of side 2 m. Tiles = ?", 0, tile(2, "m", 1))
plain("d157d455", 9, 5, "m", "Each packet covers 3 sq. m. Packets = ?", 0)
plain("ch20_q009", 16, 10, "m", "Each sq. m costs Rs. 1000. Cost = ?", 1)
plain("ch20_q010", 30, 20, "m", "Levelling costs Rs. 5 per sq. m. Cost = ?", 1)
plain("ch20_q017", 5, 4, "m", "Each tile is a square of side 25 cm. Tiles = ?", 4,
      {4: R("20 tiles", "16 tiles", prop=1.25, hl=["fill"], note="20 tiles along, 16 tiles across: 20 × 16 = 320")})
plain("ch20_q008", 25, 20, "m", "Which is bigger: this, or a square of side 22 m?", 0,
      {1: R("22 m", "22 m", square=True, hl=["fill"], note=area_notes(22, 22, "m"))})

add("55700548", origin="authored",
    figure=R("9 m", "5 m", grid=(9, 5), note="Each tile is 1 m by 1 m and costs ₹45. Cost = ?"),
    steps={0: R("9 m", "5 m", grid=(9, 5), hl=["fill"], note=area_notes(9, 5, "m")),
           1: R("9 m", "5 m", grid=(9, 5), note="One tile for each square: 45 tiles")})
add("91e7ed21", origin="authored",
    figure=R("50 cm", "50 cm", square=True, note="Each tile is a square of side 5 cm. Tiles = ?"),
    steps={0: R("50 cm", "50 cm", square=True, hl=["fill"], note=area_notes(50, 50, "cm")),
           1: R("5 cm", "5 cm", square=True, hl=["fill"], note=area_notes(5, 5, "cm", "One tile")),
           2: R("50 cm", "50 cm", grid=(10, 10), note="10 tiles fit along each side: 10 × 10 = 100")})
add("ch20_q001", origin="authored",
    figure=R("1.2 m", "50 cm", inside="Area = ?", prop=2.4),
    steps={1: R("120 cm", "50 cm", prop=2.4, note="Both sides are now in centimetres"),
           2: R("120 cm", "50 cm", prop=2.4, hl=["fill"], note=["120 × 50 = 6000 sq. cm", "Area = 120 × 50"])})
add("ch20_q022", origin="authored",
    figure=R("6.1 cm", "6.1 cm", square=True, inside="Area = ?"),
    steps={1: R("6.1 cm", "6.1 cm", square=True, hl=["fill"], note="Area = 6.1 × 6.1"),
           3: R("6.1 cm", "6.1 cm", square=True, hl=["fill"], note="6.1 × 6.1 = 37.21 sq. cm")})
add("ch20_q023", origin="authored",
    figure=R("30 cm", "1.1 cm", inside="Area = ?", prop=3, note="A long thin rectangle (not drawn to scale)"),
    steps={1: R("30 cm", "1.1 cm", prop=3, hl=["fill"], note="Area = 1.1 × 30"),
           2: R("30 cm", "1.1 cm", prop=3, hl=["fill"], note=["11 × 30 = 330, and 330 ÷ 10 = 33 sq. cm", "1.1 × 30 = 33 sq. cm"])})

# A rectangle cut along its diagonal, with a square bed in the painted half.
_diag = [(0, 0), (12, 0), (12, 8), (0, 8)]
add("8d2c4e7b", origin="authored",
    figure=P(_diag, edges=[None, None, "18 m", "12 m"], dashed=[(0, 2)], note="One half is painted. A square bed of side 4 m sits inside it."),
    steps={0: R("18 m", "12 m", prop=1.5, hl=["fill"], note=area_notes(18, 12, "m")),
           1: P([(0, 0), (12, 8), (0, 8)], edges=[None, "18 m", "12 m"], right=[2], hl=["fill"],
                note=["216 ÷ 2 = 108 sq. m", "The painted triangle is half of the rectangle"]),
           2: R("4 m", "4 m", square=True, hl=["fill"], note=area_notes(4, 4, "m", "Flower bed"))})

# A triangle inside a square: base on one side, tip on the opposite side.
_tip = [(0, 0), (4, 0), (10, 0), (10, 10), (0, 10)]
_tip_edges = [None, None, "20 m", "20 m", None]
add("de0dda2b", origin="authored",
    figure=P(_tip, edges=_tip_edges, dashed=[(1, 3), (1, 4)], note="Gold paint goes outside the triangle: ₹12 per sq. m. Cost = ?"),
    steps={0: R("20 m", "20 m", square=True, hl=["fill"], note=area_notes(20, 20, "m")),
           1: T("scalene", sides={"bc": "20 m"}, height="20 m", enclose=True, hl=["fill"],
                note=["½ × 20 × 20 = 200 sq. m", "Triangle = ½ × 20 × 20"]),
           2: P(_tip, edges=_tip_edges, dashed=[(1, 3), (1, 4)], note=["400 − 200 = 200 sq. m", "Gold part = square − triangle"])})

# A square sheet with a small square cut from each corner, folded into a tray.
_tray = [(2, 0), (8, 0), (8, 2), (10, 2), (10, 8), (8, 8), (8, 10), (2, 10), (2, 8), (0, 8), (0, 2), (2, 2)]
_folds = [(11, 2), (2, 5), (5, 8), (8, 11)]


def tray(note=None, top=None, hl=None):
    corners = [None] * 12
    corners[2] = "4 cm × 4 cm"
    edges = [None] * 12
    edges[0] = top
    return P(_tray, edges=edges, corners=corners, dashed=_folds, note=note, hl=hl)


add("fc28c7c1", origin="authored",
    figure=tray("A 20 cm square sheet. The sides fold up on the dashed lines. Base = ?"),
    steps={0: R("20 cm", "20 cm", square=True, note="The sheet before cutting"),
           1: tray("A 4 cm square is cut from each of the 4 corners"),
           2: tray("Each side loses 4 cm at both ends: 20 − 4 − 4", top="20 − 4 − 4", hl=["e0"]),
           4: R("12 cm", "12 cm", square=True, hl=["fill"], note=["12 × 12 = 144 sq. cm", "Base = 12 × 12"])})


# ── Rectangles and squares found from a perimeter, an area or a rule ─────────

def sq_from_perimeter(key, per, u, side, s_first=None, s_side=None, s_area=None):
    """A square whose perimeter is given; the side (and perhaps the area) is asked."""
    area = side * side
    want_area = s_area is not None
    P_, S = "%s %s" % (n(per), u), "%s %s" % (n(side), u)
    steps = {}
    if s_first is not None:
        steps[s_first] = R("?", "?", square=True, hl=["border"], note="A square has 4 equal sides")
    steps[s_side] = [R(S, S, square=True, hl=["length"], note=["%s ÷ 4 = %s" % (n(per), S), "Side = %s" % S]),
                     R("?", "?", square=True, hl=["length"], note="Side = %s ÷ 4" % n(per))]
    if want_area:
        steps[s_area] = [R(S, S, square=True, hl=["fill"], note=["%s%s%s = %s sq. %s" % (n(side), X, n(side), n(area), u), "Area = side × side"]),
                         R("%s ÷ 4 %s" % (n(per), u), "%s ÷ 4 %s" % (n(per), u), square=True, hl=["fill"], note="Area = side × side")]
    add(key, figure=R("?", square=True, inside="Area = ?" if want_area else None, note="Perimeter = %s" % P_), steps=steps)


sq_from_perimeter("ch19_q002", 16, "cm", 4, s_first=0, s_side=2)
sq_from_perimeter("ch19_q014", 24.4, "cm", 6.1, s_first=1, s_side=3)
sq_from_perimeter("ch19_q006", 20, "cm", 5, s_first=0, s_side=1, s_area=2)
sq_from_perimeter("ch19_q017", 36, "cm", 9, s_first=0, s_side=1, s_area=2)
sq_from_perimeter("ch20_q027", 52, "mm", 13, s_side=0, s_area=1)


def sq_from_area(key, area, u, side, s_side, s_per):
    """A square whose area is given; the perimeter is asked."""
    S = "%s %s" % (n(side), u)
    inside = "%s sq. %s" % (n(area), u)
    add(key, figure=R("?", square=True, inside=inside, note="Perimeter = ?"), steps={
        s_side: R(S, S, square=True, inside=inside, hl=["length"], note="%s%s%s = %s" % (n(side), X, n(side), n(area))),
        s_per: R(S, S, square=True, hl=["border"], note=["4%s%s = %s %s" % (X, n(side), n(4 * side), u), "Perimeter = 4%s%s" % (X, n(side))])})


sq_from_area("ch19_q008", 441, "cm", 21, 1, 2)
sq_from_area("ch19_q019", 676, "cm", 26, 1, 2)
sq_from_area("ch20_q011", 144, "cm", 12, 1, 2)

add("ch19_q012", origin="authored",
    figure=R("4.6 cm", "4.6 cm", square=True, note="Perimeter = ?"),
    steps={0: R("4.6 cm", "4.6 cm", square=True, hl=["border"], note="The perimeter is the distance all the way round"),
           2: R("4.6 cm", "4.6 cm", square=True, hl=["border"], note=["Perimeter = 4 × 4.6", "Perimeter = side + side + side + side"]),
           3: R("4.6 cm", "4.6 cm", square=True, hl=["border"], note="4 × 4.6 = 18.4 cm")})

add("ch19_q003", origin="authored",
    figure=R("12 cm", "?", prop=1.5, note="Perimeter = 40 cm"),
    steps={0: R("12 cm", "?", prop=1.5, hl=["border"], note="All the way round is 40 cm"),
           3: R("12 cm", "?", prop=1.5, hl=["length", "breadth"], note=["12 + breadth = 20", "12 + breadth = 40 ÷ 2"]),
           4: R("12 cm", "8 cm", prop=1.5, hl=["breadth"], note=["20 − 12 = 8 cm", "Breadth = 8 cm"])})
add("ch19_q015", origin="authored",
    figure=R("14 cm", "?", prop=1.4, note="Perimeter = 48 cm"),
    steps={1: R("14 cm", "?", prop=1.4, hl=["border"], note="All the way round is 48 cm"),
           2: R("14 cm", "?", prop=1.4, hl=["length", "breadth"], note=["14 + breadth = 24", "14 + breadth = 48 ÷ 2"]),
           3: R("14 cm", "10 cm", prop=1.4, hl=["breadth"], note=["24 − 14 = 10 cm", "Breadth = 10 cm"])})

add("ch19_q005", origin="authored",
    figure=R("2 × breadth", "breadth", prop=2, note="Perimeter = 42 cm"),
    steps={1: R("2b cm", "b cm", prop=2, note="Call the breadth b: the length is 2b"),
           4: R("2b cm", "b cm", prop=2, hl=["border"], note="All the way round: 2 × 3b = 42"),
           6: R("14 cm", "7 cm", prop=2, note="b = 7, so the length is 2 × 7 = 14 cm")})
add("ch19_q020", origin="authored",
    figure=R("2 × breadth", "breadth", prop=2, note="Perimeter = 78 cm"),
    steps={0: R("2b cm", "b cm", prop=2, note="Call the breadth b: the length is 2b"),
           4: R("2b cm", "b cm", prop=2, hl=["border"], note="All the way round: 6b = 78"),
           6: R("26 cm", "13 cm", prop=2, note="b = 13, so the length is 2 × 13 = 26 cm")})
add("ch19_q025", origin="authored",
    figure=R("thrice the breadth", "?", prop=3, note="Perimeter = 64 cm"),
    steps={0: R("3b cm", "b cm", prop=3, note="Call the breadth b: the length is 3b"),
           4: R("3b cm", "b cm", prop=3, hl=["border"], note="All the way round: 8b = 64"),
           6: R("24 cm", "8 cm", prop=3, hl=["breadth"], note="b = 8 cm, and the length is 3 × 8 = 24 cm")})
add("ch20_q007", origin="authored",
    figure=R("3/2 × breadth", "breadth", prop=1.5, inside="Area = ?", note="Perimeter = 50 cm"),
    steps={0: R("3/2 × b", "b", prop=1.5, note="Call the breadth b"),
           5: R("15 cm", "10 cm", prop=1.5, note="Breadth 10 cm, length 3/2 × 10 = 15 cm"),
           6: R("15 cm", "10 cm", prop=1.5, hl=["fill"], note="15 × 10 = 150 sq. cm")})
add("ch19_q007", origin="authored",
    figure=R("breadth + 5 cm", "breadth", prop=1.5, inside="Area = ?", note="Perimeter = 50 cm"),
    steps={1: R("b + 5", "b", prop=1.5, hl=["border"], note="All the way round is 50 cm"),
           5: [R("15 cm", "10 cm", prop=1.5, note="Length = 10 + 5 = 15 cm"), R("10 + 5 cm", "10 cm", prop=1.5)],
           6: R("15 cm", "10 cm", prop=1.5, hl=["fill"], note=["15 × 10 = 150 sq. cm", "Area = 15 × 10"])})
add("ch19_q018", origin="authored",
    figure=R("breadth + 8 cm", "breadth", prop=14 / 6.0, inside="Area = ?", note="Perimeter = 40 cm"),
    steps={0: R("b + 8", "b", prop=14 / 6.0, note="Call the breadth b: the length is b + 8"),
           1: R("b + 8", "b", prop=14 / 6.0, hl=["border"], note="All the way round is 40 cm"),
           6: R("14 cm", "6 cm", prop=14 / 6.0, note="Breadth 6 cm, length 6 + 8 = 14 cm"),
           7: R("14 cm", "6 cm", prop=14 / 6.0, hl=["fill"], note="14 × 6 = 84 sq. cm")})
add("ch19_q009", origin="authored",
    figure=R("2 × breadth", "breadth", prop=2, inside="98 sq. cm", note="Perimeter = ?"),
    steps={1: R("2b", "b", prop=2, inside="98 sq. cm", note="Call the breadth b: the length is 2b"),
           5: R("2b", "b", prop=2, inside="98 sq. cm", note="b × b = 49, so b = 7"),
           6: [R("14 cm", "7 cm", prop=2, inside="98 sq. cm"), R("2 × 7 cm", "7 cm", prop=2, inside="98 sq. cm")],
           8: R("14 cm", "7 cm", prop=2, hl=["border"], note=["14 + 7 + 14 + 7 = 42 cm", "Perimeter = 42 cm"])})

add("56d7bc6f", origin="authored",
    figure=R("2 × breadth", "breadth", prop=2, inside="hole 5 m × 5 m", note="Rope round the edge: 120 m. Area left after the hole = ?"),
    steps={0: R("2b", "b", prop=2, note="Call the breadth b: the length is 2b"),
           1: R("2b", "b", prop=2, hl=["border"], note="The 120 m of rope goes all the way round"),
           2: R("2b", "b", prop=2, hl=["border"], note="2 × 3b = 6b = 120"),
           3: R("40 m", "20 m", prop=2, note="b = 120 ÷ 6 = 20 m, and the length is 2 × 20 = 40 m"),
           4: R("40 m", "20 m", prop=2, hl=["fill"], note="40 × 20 = 800 sq. m"),
           5: R("5 m", "5 m", square=True, hl=["fill"], note="The hole: 5 × 5 = 25 sq. m"),
           6: R("40 m", "20 m", prop=2, inside="hole 5 m × 5 m", note="800 − 25 = 775 sq. m")})
add("f1073203", origin="authored",
    figure=R("3 × breadth", "breadth", prop=3, note="Ribbon round the edge: ₹640 at ₹8 per cm. Powder: ₹2 per sq. cm."),
    steps={1: R("3b", "b", prop=3, hl=["border"], note="The ribbon is 80 cm long: that is the perimeter"),
           2: R("3b", "b", prop=3, hl=["border"], note="2 × (3b + b) = 80"),
           3: [R("30 cm", "10 cm", prop=3), R("3 × 10 cm", "10 cm", prop=3)],
           4: [R("30 cm", "10 cm", prop=3, hl=["fill"], note="30 × 10 = 300 sq. cm"),
               R("3 × 10 cm", "10 cm", prop=3, hl=["fill"], note="Area = 300 sq. cm")]})

# A room: the floor, then its four walls opened out into one strip.
add("ch20_q013", origin="authored",
    figure=R("5 m", "4 m", prop=1.25, note="This is the floor. The four walls: 108 sq. m. Height = ?"),
    steps={1: R("5 m", "4 m", prop=1.25, hl=["border"], note=["2 × (5 + 4) = 18 m", "Perimeter = 2 × (5 + 4)"]),
           2: R("5 + 4 + 5 + 4 m", "?", prop=3, inside="108 sq. m", note="Open the four walls out into one long strip"),
           4: [R("18 m", "?", prop=3, inside="108 sq. m", note="108 ÷ 18 = 6 m"), R("5 + 4 + 5 + 4 m", "?", prop=3, inside="108 sq. m")],
           5: [R("18 m", "6 m", prop=3, inside="108 sq. m", hl=["breadth"]), R("5 + 4 + 5 + 4 m", "6 m", prop=3, inside="108 sq. m", hl=["breadth"])]})

# A square stretched one way and squeezed the other: no figure before answering.
add("ch20_q014", origin="authored",
    steps={0: R("a", "a", square=True, inside="a × a"),
           3: R("a + half of a", "half of a", prop=3, note="One side grows by half, the other shrinks by half"),
           5: R("15", "5", prop=3, note="Try a = 10: 15 × 5 = 75, smaller than 10 × 10 = 100")})

# A wire bent into a square, then into a rectangle.
add("ch20_q018", origin="authored",
    figure=R("?", square=True, note="The 100 cm wire is bent into this square"),
    steps={0: R("25 cm", "25 cm", square=True, hl=["border"], note=["100 ÷ 4 = 25 cm", "The four equal sides share the 100 cm: 25 cm each"]),
           1: R("25 cm", "25 cm", square=True, hl=["fill"], note="25 × 25 = 625 sq. cm"),
           2: R("25 + 5 cm", "25 − 5 cm", prop=1.5, note="The same wire, bent into a rectangle"),
           3: R("25 + 5 cm", "25 − 5 cm", prop=1.5, hl=["fill"], note=["30 × 20 = 600 sq. cm", "Area = 600 sq. cm"])})


# ── Regular hexagons ─────────────────────────────────────────────────────────

ALL6 = ["e0", "e1", "e2", "e3", "e4", "e5"]
ONE = lambda label: [label, None, None, None, None, None]  # noqa: E731

add("ch19_q004", origin="authored",
    figure=hexagon(ONE("?"), note="A regular hexagon: all sides equal. Perimeter = 54 cm"),
    steps={0: hexagon(["s"] * 6, hl=ALL6, note="6 equal sides"),
           3: hexagon(ONE("9 cm"), hl=["e0"], note="54 ÷ 6 = 9 cm")})
add("ch19_q016", origin="authored",
    figure=hexagon(ONE("?"), note="A regular hexagon: all sides equal. Perimeter = 72 cm"),
    steps={0: hexagon(["s"] * 6, hl=ALL6, note="6 equal sides"),
           3: hexagon(ONE("12 cm"), hl=["e0"], note="72 ÷ 6 = 12 cm")})
add("ch19_q022", origin="authored",
    figure=hexagon(hl=ALL6[:5], note="A regular hexagon. Perimeter = 42 cm. Sum of 5 sides = ?"),
    steps={1: [hexagon(ONE("7 cm"), hl=["e0"], note="42 ÷ 6 = 7 cm"), hexagon(ONE("?"), hl=["e0"], note="One side = 42 ÷ 6")],
           2: hexagon(["7 cm"] * 5 + [None], hl=ALL6[:5], note="5 × 7 = 35 cm")})
add("ch19_q023", origin="authored",
    figure=hexagon(ONE("6.1 cm"), note="A regular hexagon: all sides equal. Perimeter = ?"),
    steps={2: hexagon(["6.1 cm"] * 6, hl=ALL6, note="Perimeter = 6 × 6.1"),
           3: hexagon(["6.1 cm"] * 6, hl=ALL6, note="6 × 6.1 = 36.6 cm")})


# ── Triangles ────────────────────────────────────────────────────────────────

SIDES3 = ["ab", "bc", "ca"]


def eq(label, note=None, hl=None, only_base=False):
    sides = {"bc": label} if only_base else {"ab": label, "bc": label, "ca": label}
    return T("equilateral", sides=sides, note=note, hl=hl)


add("ch19_q001", origin="authored",
    figure=eq("5.3 cm", "Perimeter = ?"),
    steps={1: eq("5.3 cm", "Perimeter = 3 × side", SIDES3),
           3: eq("5.3 cm", "3 × 5.3 = 15.9 cm", SIDES3)})
add("ch19_q013", origin="authored",
    figure=eq("5.4 cm", "Perimeter = ?"),
    steps={3: eq("5.4 cm", "Perimeter = 3 × 5.4", SIDES3),
           5: eq("5.4 cm", "3 × 5.4 = 16.2 cm", SIDES3)})
add("ch19_q010", origin="authored",
    figure=eq("?", "All three sides are equal. Perimeter = 23.1 cm", only_base=True),
    steps={2: eq("?", "One side = 23.1 ÷ 3", ["bc"], only_base=True),
           3: eq("7.7 cm", "23.1 ÷ 3 = 7.7 cm")})
add("ch19_q021", origin="authored",
    figure=eq("?", "All three sides are equal. Perimeter = 29.1 cm", only_base=True),
    steps={0: eq("?", "Perimeter = 3 × side", SIDES3, only_base=True),
           2: eq("9.7 cm", "29.1 ÷ 3 = 9.7 cm")})

add("dc9f4799", origin="authored",
    figure=tri_sides(10, 13, 13, "10 cm", "13 cm", "13 cm", note="Perimeter = ?"),
    steps={1: tri_sides(10, 13, 13, "10 cm", "13 cm", "13 cm", hl=["e0", "e1", "e2"], note="Add all three sides: 13 + 13 + 10"),
           2: tri_sides(10, 13, 13, "10 cm", "13 cm", "13 cm", hl=["e0", "e1", "e2"], note="13 + 13 + 10 = 36 cm")})
add("ch19_q011", origin="authored",
    figure=tri_sides(10, 8, 8, "?", "8 cm", "8 cm", note="Perimeter = 26 cm"),
    steps={3: tri_sides(10, 8, 8, "?", "8 cm", "8 cm", hl=["e0", "e2"], note=["8 + 8 = 16 cm", "Add the two equal sides: 8 + 8"]),
           4: tri_sides(10, 8, 8, "10 cm", "8 cm", "8 cm", hl=["e1"], note=["26 − 16 = 10 cm", "Third side = 10 cm"])})
add("ch19_q026", origin="authored",
    figure=tri_sides(14, 9, 9, "?", "9 cm", "9 cm", note="Perimeter = 32 cm"),
    steps={2: tri_sides(14, 9, 9, "?", "9 cm", "9 cm", hl=["e0", "e2"], note=["9 + 9 = 18 cm", "Add the two equal sides: 9 + 9"]),
           4: tri_sides(14, 9, 9, "14 cm", "9 cm", "9 cm", hl=["e1"], note=["32 − 18 = 14 cm", "Third side = 14 cm"])})
add("ch19_q024", origin="authored",
    figure=tri_sides(5.3, 3.2, 4.6, "5.3 cm", "3.2 cm", "4.6 cm", note="Perimeter = ?"),
    steps={1: tri_sides(5.3, 3.2, 4.6, "5.3 cm", "3.2 cm", "4.6 cm", hl=["e0", "e2"], note="3.2 + 4.6 = 7.8"),
           2: tri_sides(5.3, 3.2, 4.6, "5.3 cm", "3.2 cm", "4.6 cm", hl=["e0", "e1", "e2"], note="7.8 + 5.3 = 13.1 cm")})

# Sides in the ratio 3 : 4 : 5 (drawn to that shape; the right angle is marked only once it is found).
add("9bea442a", origin="authored",
    figure=tri_sides(24, 18, 30, "4 parts", "3 parts", "5 parts", note="Perimeter = 72 m. Area = ?"),
    steps={0: tri_sides(24, 18, 30, "4x", "3x", "5x", note="3x + 4x + 5x = 72"),
           2: tri_sides(24, 18, 30, "24 m", "18 m", "30 m"),
           4: tri_sides(24, 18, 30, "24 m", "18 m", "30 m", right_at_b=True, hl=["e0", "e1"],
                        note=["½ × 18 × 24 = 216 sq. m", "Area = ½ × 18 × 24"])})
add("a7c1fcb5", origin="authored",
    figure=tri_sides(12, 9, 15, "12 cm", "9 cm", "15 cm", note="Every side is doubled. How much bigger is the area?"),
    steps={1: tri_sides(12, 9, 15, "12 cm", "9 cm", "15 cm", right_at_b=True, hl=["e0", "e1"], note=["½ × 9 × 12 = 54 sq. cm", "Area = ½ × 9 × 12"]),
           2: tri_sides(24, 18, 30, "24 cm", "18 cm", "30 cm", right_at_b=True, hl=["e0", "e1"], note=["½ × 18 × 24 = 216 sq. cm", "Area = ½ × 18 × 24"])})
add("d3681d12", origin="authored",
    figure=tri_sides(20, 15, 25, "20 cm", "15 cm", "25 cm", right_at_b=True, note="Cloth costs ₹2 per sq. cm. Cost = ?"),
    steps={1: tri_sides(20, 15, 25, "20 cm", "15 cm", "25 cm", right_at_b=True, hl=["e0", "e1"], note="The 15 cm and 20 cm sides meet at the right angle"),
           2: tri_sides(20, 15, 25, "20 cm", "15 cm", "25 cm", right_at_b=True, hl=["fill"], note=["½ × 15 × 20 = 150 sq. cm", "Area = ½ × 15 × 20"])})
add("f49a4fc2", origin="authored",
    figure=tri_sides(16, 12, 20, "16 cm", "12 cm", "20 cm", right_at_b=True, note="Area = ?"),
    steps={1: tri_sides(16, 12, 20, "16 cm", "12 cm", "20 cm", right_at_b=True, hl=["e0", "e1"], note="The 12 cm and 16 cm sides make the right angle"),
           3: tri_sides(16, 12, 20, "16 cm", "12 cm", "20 cm", right_at_b=True, hl=["fill"], note=["½ × 12 × 16 = 96 sq. cm", "Area = ½ × 12 × 16"])})

# Base and height.
add("ch20_q021", origin="authored",
    figure=T("scalene", sides={"bc": "5.2 cm"}, height="2.9 cm", note="Area = ?"),
    steps={0: T("scalene", sides={"bc": "base"}, height="height", enclose=True, hl=["bc", "height"], note="The triangle is half of the rectangle around it"),
           1: T("scalene", sides={"bc": "5.2 cm"}, height="2.9 cm", hl=["bc", "height"], note="Area = ½ × 5.2 × 2.9"),
           4: T("scalene", sides={"bc": "5.2 cm"}, height="2.9 cm", enclose=True, hl=["fill"], note="½ × 5.2 × 2.9 = 7.54 sq. cm")})
add("ch20_q012", origin="authored",
    figure=T("isosceles", sides={"bc": "?"}, height="2 cm", note="Area = 5 sq. cm"),
    steps={1: T("isosceles", sides={"bc": "base"}, height="height", enclose=True, hl=["bc", "height"], note="Area = ½ × base × height"),
           3: T("isosceles", sides={"bc": "?"}, height="2 cm", hl=["height"], note="Half of 2 is 1, so the area is 1 × base"),
           4: T("isosceles", sides={"bc": "5 cm"}, height="2 cm", hl=["bc"])})
add("ch20_q025", origin="authored",
    figure=T("scalene", sides={"bc": "40 cm"}, height="?", note="Area = 120 sq. cm"),
    steps={0: T("scalene", sides={"bc": "base"}, height="height", enclose=True, hl=["bc", "height"], note="Area = ½ × base × height"),
           2: T("scalene", sides={"bc": "40 cm"}, height="?", hl=["bc"], note="½ × 40 = 20, so 120 = 20 × height"),
           3: T("scalene", sides={"bc": "40 cm"}, height="6 cm", hl=["height"], note="120 ÷ 20 = 6 cm"),
           4: T("scalene", sides={"bc": "40 cm"}, height="60 mm", hl=["height"], note="6 cm = 60 mm")})


# ── Left without a figure ────────────────────────────────────────────────────

skip("352cbeaf", "contradiction",
     "equal angles three times the third give about 77°, 77°, 26°, but sides 5, 5, 3.4 cm make about 70°, 70°, 40°")
skip("ch20_q006", "no-picture", "a square whose area and perimeter are the same number: algebra on one unknown side, nothing to see")
