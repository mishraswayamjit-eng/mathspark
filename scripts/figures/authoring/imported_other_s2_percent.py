"""Percentage of a whole (gr5_percentage): the money as one bar, each spend a piece of it."""
from imported_other_lib import model, S, H, U


def left(sid, whole, segs, ans=None, note="How much is left?", unote="Left: %s"):
    model(sid, [("", segs, whole)], ans=ans, note=note, unote=unote)


left("b7ce060504a8", ("₹1,200", 1200), [H("25% saved", 300), H("40% of the rest", 360), U()], ans=lambda u: u / 15,
     note="The last piece buys samosas at ₹15 each")
left("6d4bf8620665", ("₹600", 600), [H("20%", 120), S("₹150", 150), U()])
left("4dc4f177e4a3", ("₹650", 650), [H("40%", 260), S("₹110", 110), U()])
left("055ce493faa5", ("₹800", 800), [H("15%", 120), S("₹95", 95), U()])
left("91bafb1cd786", ("₹500", 500), [H("30%", 150), S("₹80", 80), U()])
left("7d4c85adc075", ("₹2,000", 2000), [H("40% saved", 800), H("25% of the rest", 300), S("₹150", 150), U()],
     ans=lambda u: u / 2, note="Half of the last piece goes to charity")
left("79b100a1d81d", ("₹800", 800), [H("35%", 280), H("4 × ₹30", 120), U()])
left("ae4e3ff983b6", ("₹750", 750), [H("40%", 300), S("₹120", 120), U()])
left("ff6d5018232e", ("₹500", 500), [H("40%", 200), S("₹75", 75), U()])
left("b4f3ad05ab93", ("₹750", 750), [S("₹300", 300), H("20% of the rest", 90), U()])
left("5d8a145faf89", ("₹1,200", 1200), [H("25%", 300), H("40% of the rest", 360), U()], note="How much goes in the piggy bank?")
left("9f2fbcccbd59", ("₹900", 900), [H("30%", 270), S("₹135", 135), U()])
left("d010b06d1afa", ("₹350", 350), [S("₹80", 80), H("25% of the rest", 67.5), U()])
left("e9c43f37a749", ("₹600", 600), [S("₹150", 150), H("20% of the rest", 90), U()])
left("7d037c983e2f", ("₹2,000", 2000), [H("20%", 400), H("25% of the rest", 400), S("₹150", 150), U()])
left("ce1e4247e16f", ("₹1,500", 1500), [H("40% in bank", 600), S("₹180", 180), H("1/3 of the rest", 240), U()],
     note="How much is left at home?")
left("53356d70258f", ("₹1,200", 1200), [H("25%", 300), S("₹150", 150), U()])
left("42bd7ae234c5", ("₹500", 500), [H("35%", 175), S("₹80", 80), U()])
left("564c229fd691", ("₹1,200", 1200), [H("25% saved", 300), H("8 × ₹45", 360), U()])
left("e25e0afcb538", ("₹360", 360), [H("25%", 90), S("₹95", 95), U()])
left("5527a3cd1924", ("₹500", 500), [H("30%", 150), H("25% of the rest", 87.5), U()])
left("0705016115e8", ("₹500", 500), [H("30%", 150), H("40% of the rest", 140), U()])
left("e89afed624bb", ("₹400", 400), [H("25%", 100), S("₹90", 90), U()])
left("7702d7f3dce7", ("₹1,200", 1200), [H("50% saved", 600), H("25% of the rest", 150), U()])
left("e03f2c039ce4", ("₹900", 900), [H("20%", 180), S("₹180", 180), U()])
left("8ee267f16ce2", ("₹250", 250), [S("₹90", 90), H("40% of the rest", 64), U()])
left("785e8ae30e0a", ("₹400", 400), [S("₹120", 120), H("25% of the rest", 70), U()])
left("a782adfdd00c", ("24 × ₹15", 360), [H("20% to charity", 72), U()])
left("e99a697457c3", ("₹2,000", 2000), [H("40% saved", 800), H("25% of the rest", 300), U("?", 3)],
     note="The 3 equal pieces are the gifts for 3 friends", unote="Each gift: %s")
left("e581dea4bc8f", ("₹450", 450), [H("20%", 90), S("₹110", 110), U()])
left("2006935776cc", ("₹650", 650), [S("₹200", 200), H("30% of the rest", 135), U()])

# A discount: the price before on one bar, what is paid plus the discount on the other.
model("dc3a6181980f", [("Bill", [H("8 × ₹15", 120), H("12 × ₹20", 240)]), ("Pays", [U(), H("10% off", 36)])],
      note="The discount is 10% of the whole bill", unote="He pays %s")
model("3e6f5c9d7ec0", [("Marked price", [S("₹1,500", 1500), H("40% more", 600)]), ("Sale price", [U(), H("10% off", 210)])],
      note="The 10% discount is taken off the marked price", unote="Sale price: %s")
