"""Equation stories (gr5_equations, and one in gr5_operations2): the total as one bar,
made of equal unknown pieces and the amounts the question states."""
from imported_other_lib import model, ratio, staged, S, H, U, commas


def M(v, tag=""):
    return S("₹" + commas(v) + (" " + tag if tag else ""), v)


def eq(sid, whole, parts, **kw):
    kw.setdefault("note", "The equal pieces are what we want. Take the rest away first.")
    kw.setdefault("unote", "Each equal piece: %s")
    model(sid, [("", parts, whole)], **kw)


def count(sid, whole, parts, each, **kw):
    """The unknown is HOW MANY equal amounts of `each` make up the "?" piece."""
    kw.setdefault("note", "Find the ? piece first, then see how many equal amounts fit in it")
    kw.setdefault("unote", "The ? piece is %s")
    model(sid, [("", parts, whole)], ans=lambda u: u / each, **kw)


# n equal unknown pieces and something extra make the total.
eq("1e9b4c2eb461", ("₹133", 133), [U("x", 9), M(25)])
eq("7f8eda5033ac", ("₹50", 50), [U("x", 3), M(14)])
eq("6e15afe16349", ("52 laddoos", 52), [U("?", 3), S("7", 7)], unit="")
eq("391ba724f0b6", ("34 petals", 34), [U("n", 3), S("7", 7)], unit="")
eq("b53657e7176d", ("₹136", 136), [M(45), U("?", 7)])
eq("145465cdffdb", ("35 lamps", 35), [U("n", 4), S("7", 7)], unit="")
eq("e1ce8aea0162", ("₹51", 51), [U("x", 6), M(15)], note="4 notebooks on Day 1 and 2 on Day 2, each ₹x, and ₹15 more")
eq("e7c3391e0316", ("₹100", 100), [U("?", 5), M(15)])
eq("d76a3f40c650", ("21 samosas", 21), [U("n", 3), S("2", 2), S("2", 2), S("2", 2)], unit="",
   note="3 boxes of n samosas, and 2 extra on top of each box")
eq("a32d3aa348dc", ("₹58", 58), [U("x", 8), M(10)], note="3 cups in the morning and 5 in the evening, each ₹x, and ₹10 more")
eq("c521b420d4cb", ("₹62", 62), [M(23), U("x", 3)])
eq("0b00b5eca4cf", ("₹50", 50), [U("x", 8), M(10)], note="3 samosas, then 5 samosas, each ₹x, and a ₹10 tip")
eq("e57fae114164", ("₹47", 47), [U("x", 5), H("4 × ₹3", 12)])
eq("4d00ba50dd78", ("53 sachets", 53), [U("?", 4), S("9", 9)], unit="")
eq("ddf8a961608d", ("54 bags", 54), [U("?", 5), S("9", 9)], unit="")
eq("c2d9b7c060bf", ("₹98", 98), [M(35), U("n", 3)])
eq("d24b31ccaf20", ("₹95", 95), [U("x", 5), H("3 × ₹10", 30)])
eq("9c877724c1ac", ("₹255", 255), [U("x", 5), H("3 × ₹15", 45), M(40)])
eq("c5dfe7e00bcf", ("₹47", 47), [U("x", 3), M(5)], ans=lambda u: 5 * u + 5, note="Monday's bill. Find x, then price 5 samosas and a plate.")
eq("IPMTB_grade5_ch06_q009", ("Rs. 140", 140), [U("?", 10), H("5 × Rs. 8", 40)], unit="Rs.",
   note="10 books at the same price, and 5 notebooks")

# Equal pieces on one bar, what they come to on the other.
model("030501241cb8", [("Had and earned", [M(32), U("?", 7)]), ("Spent and left", [M(15), M(150, "left")])],
      note="7 weeks of equal pay. Both bars are the same money.", unote="Each week: %s")
model("f992cc3350e1", [("5 boxes", [U("?", 5)]), ("", [S("7 eaten", 7), S("93 left", 93)])], unit="",
      note="5 equal boxes are the 7 eaten and the 93 left", unote="Each box: %s")

# How many equal amounts?
count("c144eba526bf", ("₹99", 99), [U("? × ₹9"), M(18)], 9)
count("89ce874aab16", ("52 chocolates", 52), [U("? bags × 5"), S("7", 7)], 5, unit="")
count("df74786af6ec", ("₹500", 500), [U("? × ₹45"), M(120), M(55), M(10, "change")], 45)
count("b63ef273b4c5", ("₹72", 72), [M(23), U("? weeks × ₹7")], 7)
count("0196254e3656", ("₹57", 57), [U("? × ₹7"), M(15)], 7)
count("282ddf535887", ("₹75", 75), [U("? × ₹9"), M(12)], 9)
count("3edc611d90bd", ("88 diyas", 88), [U("? packets × 9"), S("7", 7)], 9, unit="")
count("53bfd0774c0b", ("₹47", 47), [U("? × ₹6"), M(11)], 6)
count("c398094e7069", ("₹67", 67), [M(18), U("? weeks × ₹7")], 7)
count("b4a5fcdde87d", ("₹60", 60), [M(18), U("? × ₹7")], 7)
count("b42fee37bc1f", ("₹91", 91), [U("? × ₹8"), M(19)], 8)
count("84eb3d4682ec", ("53 chairs", 53), [U("? rows × 8"), S("5", 5)], 8, unit="")
count("f23f2905f79c", ("₹31", 31), [M(3), U("? rings × ₹4")], 4)
count("22d74100cce9", ("₹73", 73), [M(17), U("w weeks × ₹8")], 8)
count("bd53eb6da489", ("₹500", 500), [M(140), U("d days × ₹45")], 45)
count("cad010472f07", ("₹30", 30), [M(9), U("w weeks × ₹3")], 3)
model("d35d81dee279", [("Bill", [U("? × ₹12"), M(33)]), ("", [M(120, "paid"), M(9, "discount")])], ans=lambda u: u / 12,
      note="The bill before the discount is what she paid plus the discount", unote="The ? piece is %s")
model("043b8fdd5db2", [("Bill", [U("? × ₹15"), M(22)]), ("", [M(120, "paid"), M(7, "coupon")])], ans=lambda u: u / 15,
      note="The bill before the coupon is what she paid plus the coupon", unote="The ? piece is %s")
model("078f5e508830", [("Sales", [U("x cups × ₹12")]), ("", [M(35, "costs"), M(109, "profit")])], ans=lambda u: u / 12,
      note="Sales are the costs and the profit together", unote="Sales: %s")

# One share is a number of times the other.
ratio("96093512df64", ["Rohan", "Ananya"], (1, 3), total=("48 samosas", 48), ask=1, ans=lambda s, o: s[1] * 12,
      note="Ananya sells 3 times as many as Rohan. Together: 48 samosas")


# Two ages with a known difference and a known sum: the older bar is the younger bar and the difference.
def ages(sid, young, old, diff, note, y, o):
    def bars(a, b):
        return {"kind": "barModel", "bars": [
            {"label": young, "segments": [{"units": 4, "label": a, "tone": "unknown" if a == "?" else "a"}]},
            {"label": old, "segments": [{"units": 4, "label": b, "tone": "unknown" if b == "?" else "a"},
                                         {"units": 1.5, "label": str(diff), "tone": "b"}]}]}
    before = dict(bars("?", "?"), note=note)
    done = dict(bars(str(y), str(y)), note="%s is %d, so %s is %d + %d = %d" % (young, y, old, y, diff, o), highlight=["b1"])
    hint = dict(bars("?", "?"), note="Take the extra piece away: two equal pieces are left", highlight=["b1s1"])
    staged(sid, before, [("final", [done, hint])])


ages("IPMTB_grade5_ch05_q040", "Reeta", "Seeta", 6, "Together 12 years. Seeta is 6 years older.", 3, 9)
ages("IPMTB_grade5_ch08_q014", "Madhavi", "Rekha", 5, "Together 25 years. Rekha is 5 years older.", 10, 15)
