"""Profit and loss (gr5_profitloss): money spent on one bar, money earned on the other.
The bars are drawn to scale, so the profit (or loss) is the part where one bar is longer."""
from imported_other_lib import model, S, H, commas


def M(v, tag=""):
    return S("₹" + commas(v) + (" " + tag if tag else ""), v)


def pl(sid, cost, sales, ans=None, note="Money spent and money earned. How far apart are the bars?", unote="The gap between the bars: %s"):
    model(sid, [("Spent", cost), ("Earned", sales)], ans=ans, note=note, unote=unote)


pl("70575c3fc403", [H("40 × ₹12", 480), M(80), M(40)], [H("40 × ₹20", 800)])
pl("8b380c7e73c1", [M(120), M(80)], [H("10 × ₹30", 300)])
pl("8f8863a25b2e", [M(400)], [H("(50 − 10) × ₹12", 480)], ans=lambda u: u * 100 / 400,
   note="10 of the 50 rakhis were not sold. Profit as a % of ₹400 = ?")
pl("9ca4a02c3c02", [M(150), M(90)], [H("60 × ₹7", 420)])
pl("c4c5d16ee728", [H("5 kg × ₹60", 300), H("2 kg × ₹45", 90), M(50)], [H("120 × ₹5", 600)])
pl("5c079919c27f", [H("25 × ₹20", 500), M(150)], [H("25 × ₹35", 875)])
pl("032180de75cb", [M(240), M(60)], [H("60 × ₹8", 480)], ans=lambda u: u * 25 / 100, note="Find the profit first. 25% of it goes to charity.")
pl("2af03f292636", [M(200), M(100)], [H("60 × ₹8", 480)])
pl("823594f456f3", [H("40 × ₹75", 3000)], [H("30 at 20% profit", 2700), H("10 at 10% below", 675)])
pl("785360dbcbfe", [H("40 × ₹75", 3000)], [H("30 at 20% profit", 2700), H("10 at 10% below", 675)])
pl("13bd0af0b0b3", [H("20 × ₹45", 900)], [H("20 × ₹63", 1260)])
pl("6b07b78468f0", [M(200), M(100)], [H("15 × ₹30", 450)])
pl("572dcba4acdb", [H("80 × ₹4", 320), M(80)], [H("80 × ₹7", 560)])
pl("c15dbaa7f6f6", [M(250)], [M(350)], ans=lambda u: u * 20 / 100, note="Find the profit first. 20% of it goes to charity.")
pl("e3c8bce6ccff", [H("50 kg × ₹40", 2000), M(200)], [H("50 kg × ₹52", 2600)])
pl("6ce871b2846e", [H("5 kg × ₹40", 200), M(50)], [H("50 × ₹9", 450)])
pl("175eac6373cd", [H("25 × ₹8", 200)], [H("25 × ₹12", 300)])
pl("8f5b24a9b8ec", [M(180), M(90), M(30)], [H("60 × ₹8", 480)])
pl("3c9e5c359547", [M(250), M(150), M(100)], [H("100 × ₹8", 800)])
pl("5e5610b73daa", [H("60 × ₹12", 720), M(120)], [H("60 × ₹16", 960)])
pl("cb56a9c75ce3", [H("25 × ₹6", 150)], [H("25 × ₹10", 250)])
pl("828f19d49eb1", [H("40 × ₹15", 600), M(100)], [H("40 × ₹22", 880)])
pl("339a822eb01a", [H("12 × ₹15", 180), M(60)], [H("20 × ₹18", 360)])
pl("56fc347640a1", [H("12 × ₹35", 420), H("12 × ₹5", 60)], [H("12 × ₹56", 672)])
pl("2f99d861cf8b", [H("3 × ₹160", 480), M(120), M(80)], [H("40 × ₹25", 1000)])
pl("db049a135cf4", [H("40 × ₹75, 20% off", 2400), M(200, "rent")], [H("40 × ₹80", 3200)])
pl("ab5922c4d895", [M(120), M(80)], [H("10 × ₹32", 320)])
pl("f43ac235050e", [M(500), M(100)], [H("50 × ₹16", 800)])
pl("5abd4db084cb", [M(600)], [H("(200 − 30) × ₹5", 850)], note="30 of the 200 samosas were not sold. Profit or loss?")
pl("eb58601b522c", [M(300), M(150), M(50)], [H("10 × ₹65", 650)])
pl("ba3c1641da1d", [M(600)], [H("90% of 200 × ₹8", 1440)])
model("b069fbacd7fa", [("Spent", [M(600)]), ("Earned", [H("(200 − 40) × ₹5", 800)])], check=False,   # key: "33⅓% profit" = 200 out of 600
      note="40 of the 200 samosas were not sold. Profit or loss as a % of ₹600?", unote="The gap between the bars: %s")
