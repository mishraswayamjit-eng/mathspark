"""Ratio and sharing (gr5_variation): one bar per sharer, cut into equal pieces."""
from imported_other_lib import ratio, staged, table

R = "₹"

ratio("c2df49d90fd9", ["Kavya", "Lakshmi"], (2, 3), total=("90 packets", 90), ask=0, ans=lambda s, o: s[0] / 2)
ratio("baac6d95cf43", ["Priya", "Rohan"], (4, 5), total=("₹540", 540), unit=R, ask=1, ans=lambda s, o: s[1] - 80)
ratio("615fbd2d6d11", ["Rohit", "Virat"], (5, 4), total=("180 runs", 180), ask=0, ans=lambda s, o: 2 * s[0])
ratio("4111239c6f6c", ["Ananya", "Bhavna"], (3, 5), total=("₹480", 480), unit=R, ask=0, ans=lambda s, o: s[0] - 40)
ratio("86f0128cc816", ["Priya", "Rohan"], (3, 2), shown=(12, 8), what="Ages", total=("₹180", 180), unit=R, ask=0,
      ans=lambda s, o: s[0] - 45 + 30)
ratio("3df44e5e1e9e", ["Priya", "Rohan"], (4, 5), total=("₹180", 180), unit=R, ask=1, ans=lambda s, o: s[1] - 95)
ratio("99938e64c6b3", ["1st innings", "2nd innings"], (3, 5), total=("96 runs", 96), ask=1, ans=lambda s, o: s[1])
ratio("85ea48000016", ["Priya", "Rohan"], (2, 3), total=("₹1,800", 1800), unit=R, ask=0, ans=lambda s, o: s[0] * 5 / 8)
ratio("da41901e4f83", ["Riya", "Sana"], (4, 7), total=("₹770", 770), unit=R, ask=1, ans=lambda s, o: s[1] / 14)
ratio("be673798b2c3", ["Morning", "Evening"], (3, 5), total=("72 samosas", 72), ask=0, ans=lambda s, o: 2 * s[0])
ratio("372b0b1a9ca5", ["Rohit", "Virat"], (5, 4), total=("126 runs", 126), ask=0, ans=lambda s, o: s[0])
ratio("ce7cdca23a73", ["Kabir", "Priya", "Zara"], (2, 3, 5), total=("₹450", 450), unit=R, ask=0, ans=lambda s, o: s[0] / 2)
ratio("a73ce04feb8f", ["Rohan", "Sahil"], (5, 3), total=("₹480", 480), unit=R, ans=lambda s, o: s[0] - s[1],
      note="Prize money ₹480 shared in the ratio 5 : 3. How much more for Rohan?")
ratio("caa6ecc410d0", ["Arjun", "Bharat", "Chetan"], (3, 5, 7), total=("225 runs", 225), ans=lambda s, o: (s[2] - s[0]) * 10)
ratio("f925ed48537b", ["Ravi", "Sunil"], (5, 3), total=("96 runs", 96), ask=0, ans=lambda s, o: s[0] / 4)
ratio("0b98c176dae8", ["Sneha", "Tanvi"], (5, 7), shown=(35, 49), what="Money paid", total=("84 balloons", 84), ask=1,
      ans=lambda s, o: s[1])
ratio("cc87d7cf3e53", ["Riya", "Karan"], (4, 5), total=("₹540", 540), unit=R, ask=1, ans=lambda s, o: s[1] * 3 / 5)
ratio("c38dd5222e83", ["Kabir", "Sahil"], (3, 5), total=("₹480", 480), unit=R, ask=1, ans=lambda s, o: s[1],
      note="₹480 shared in the same ratio as the runs, 3 : 5")
ratio("715a30546cee", ["Ravi", "Sanjay"], (3, 4), total=("84 runs", 84), ask=1, ans=lambda s, o: s[1],
      note="For every 3 runs by Ravi, Sanjay scored 4. Together: 84 runs")
ratio("546626d6d990", ["Priya", "Kavya"], (3, 5), total=("640 grams", 640), ans=lambda s, o: s[1] - s[0],
      note="Ratio 3 : 5. Together: 640 grams. How much more for Kavya?")
ratio("f99c7bd5bdb6", ["Team Sixer", "Team Boundary"], (3, 4), total=("84 balls", 84))
ratio("083becdacf97", ["Arjun", "Kabir"], (4, 5), total=("108 runs", 108), ans=lambda s, o: s[1] - s[0],
      note="Ratio 4 : 5. Together: 108 runs. How many more for Kabir?")
ratio("88e328e5115f", ["Priya", "Rohan"], (2, 1), shown=(60, 30), what="Money paid", total=("90 sparklers", 90),
      ans=lambda s, o: s[0] - s[1])
ratio("beceede72eda", ["Ananya", "Bhavesh"], (3, 5), what="Hours worked", total=("₹640", 640), unit=R,
      ans=lambda s, o: s[1] - s[0])
ratio("5c10c6ce3c2c", ["Priya", "Rohan"], (3, 2), shown=(9, 6), what="Ages", total=("₹270", 270), unit=R, ask=0,
      ans=lambda s, o: s[0])
ratio("ca04c7b91bd5", ["Priya", "Rohan"], (4, 5), total=("90 sparklers", 90), ask=1, ans=lambda s, o: s[1] - 6)
ratio("c341f01b58c2", ["Riya", "Karan"], (5, 4), shown=(250, 200), what="Money paid", total=("18 accessories", 18), ask=0,
      ans=lambda s, o: s[0])
ratio("f3e546143d59", ["Red", "Yellow"], (3, 5), share=(1, "24 litres", 24), ask=0, ans=lambda s, o: s[0])
ratio("6c281a37a100", ["Priya", "Sneha"], (4, 5), total=("270 packets", 270), ask=1, ans=lambda s, o: s[1] * 2 / 3)
ratio("87d5a50b5020", ["Ananya", "Bhavna"], (5, 4), total=("₹360", 360), unit=R, ask=0, ans=6)
ratio("9275c420f09b", ["Riya", "Karan"], (3, 2), shown=(9, 6), what="Ages", total=("₹360", 360), unit=R, ask=0,
      ans=lambda s, o: s[0] / 12)
ratio("200367f21204", ["Ananya", "Bhavya"], (3, 5), total=("₹480", 480), unit=R, ans=lambda s, o: s[1] - s[0],
      note="Ratio 3 : 5. Together: ₹480. How much more for Bhavya?")
ratio("f6b167b31fff", ["Pink", "Yellow"], (3, 2), total=("25 packets", 25), ans=lambda s, o: s[0] * 15 + s[1] * 20)


# Two ratios that share one person: a ratio table.
def chain(sid, names, r1, r2, known_i, known, mid, last, unit=""):
    """names A, B, C; A : B = r1; B : C = r2; one of A or C is known."""
    cell = lambda v: (R + v if unit == R else v)
    row3 = ["?", "–", "–"]
    row3[known_i] = cell(known)
    row3[2 - known_i] = "?"
    row3[1] = "–"
    rows = [[str(r1[0]), str(r1[1]), "–"], ["–", str(r2[0]), str(r2[1])]]
    mid_row = list(row3)
    mid_row[1] = cell(mid)
    end_row = list(mid_row)
    end_row[2 - known_i] = cell(last)
    staged(sid, table(rows + [row3], headers=names, note="Two ratios. %s is in both of them." % names[1]), [
        (float(mid.replace(",", "")), table(rows + [mid_row], headers=names, hl=["r0" if known_i == 0 else "r1"],
                                           note="Use the ratio with the known amount to find %s" % names[1])),
        ((float(last.replace(",", "")), "final"), table(rows + [end_row], headers=names, hl=["r2"], note="Then use the other ratio")),
    ])


chain("76d2073ba15e", ["Riya", "Sameer", "Tina"], (3, 5), (2, 3), 2, "45", "30", "18")
chain("9c3d024fb8d5", ["Kabir", "Riya", "Sanya"], (3, 5), (4, 7), 0, "1,800", "3,000", "5,250", unit=R)
chain("37a432c8cf78", ["Kabir", "Lakshmi", "Neha"], (3, 5), (4, 7), 0, "360", "600", "1,050", unit=R)
