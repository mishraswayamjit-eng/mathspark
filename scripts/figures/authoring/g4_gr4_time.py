"""Figures for Grade 4 "Measurement of Time & Calendar" (topic gr4_time).

    python -X utf8 scripts/figures/authoring/g4_gr4_time.py

Writes data/question-figures/parts/g4-gr4_time.json.

What is drawn:
  - a line of years with the weekday of one date on it ("Republic Day 2023 was a Thursday..."):
    a rule, the weekdays come from the real calendar and are checked against the question;
  - a line of dates inside one month ("the 17th is a Saturday...");
  - a strip of months for counting days between two dates;
  - a time line (the journey figure) for start, end and how long;
  - a clock for clock-angle and slow/fast watch questions;
  - a bar of equal pieces for changing units of time.
"""
import calendar
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_time_kit import Part, T, BM, NL, CL, J, FB, ANG, renote, weekday, ints, DAYS, MONTHS  # noqa: E402

P = Part("gr4_time")


# ── Rule: the weekday of one date, year after year ───────────────────────────

def yearline(qid, month, day, end, plan, ask=False, target=None, note=None, uses_options=False, expect=None):
    """The first year and its weekday are read from the question. plan: {step: (year reached, note[, hold])}.
    hold=True keeps the reached year's weekday as "?" (the step has not named it yet)."""
    text = P.text(qid)
    y0 = [n for n in ints(text) if 1900 <= n <= 2100][0]
    day0 = re.search("|".join(DAYS), text).group(0)
    if weekday(y0, month, day) != day0:
        P.problems.append("%s: the real calendar has %s for this date, the question says %s" % (qid, weekday(y0, month, day), day0))
        return

    def name(y):
        return weekday(y, month, day)[:3]

    def shift(a, b):
        return (datetime.date(b, month, day) - datetime.date(a, month, day)).days % 7

    last_year = max(v[0] for v in plan.values())
    key = P.answer(qid)
    if str(last_year) not in key and weekday(last_year, month, day) not in key and (expect is None or expect(last_year) != key):
        P.problems.append("%s: the calendar ends on %s %d, the key is %r" % (qid, weekday(last_year, month, day), last_year, key))
        return

    points = [(y0, day0[:3])]
    if ask:
        points.append((end, "?"))
    before = NL(y0, end, 1, points=points, note=note)

    steps = {}
    for i, spec in plan.items():
        reach, nt = spec[0], spec[1]
        hold = len(spec) > 2 and spec[2]
        alts = []
        for with_target in (True, False):
            extra = [(target, "?")] if (with_target and target and target > reach) else []
            if not with_target and not (target and target > reach):
                continue
            years = list(range(y0, reach + 1))[-(6 - len(extra)):]
            pts = [(y, "?" if (hold and y == reach) else name(y)) for y in years] + extra
            hl = ["p%d" % (len(years) - 1)] + (["h%d" % (len(years) - 2)] if len(years) > 1 else [])
            alts.append(NL(y0, end, 1, points=pts, hops=[(y - 1, y, "+%d" % shift(y - 1, y)) for y in years[1:]], note=nt, hl=hl))
            if reach > y0 + 1:
                ends = [(y0, name(y0)), (reach, "?" if hold else name(reach))] + extra
                alts.append(NL(y0, end, 1, points=ends, hops=[(y0, reach, "+%d" % shift(y0, reach))], note=nt, hl=["p1", "h0"]))
                alts.append(NL(y0, end, 1, points=ends, hops=[(y0, reach)], note=nt, hl=["p1", "h0"]))
        steps[i] = alts
    P.put(qid, before, steps, origin="rule", uses_options=uses_options)


for qid in ("EXT_G4_FP_2021_015", "PYQ_2018_Q28"):
    yearline(qid, 1, 1, 2010, {
        0: (2006, "An ordinary year moves a date on by 1 weekday"),
        1: (2008, "2006 and 2007 are ordinary years: on by 1 each time"),
        2: (2009, "2008 is a leap year, so the day moves on by 2"),
        3: (2010, "2009 is an ordinary year: 1st January 2010 is a Friday"),
    }, ask=True, target=2010, note="1st January, year by year")

yearline("EXT_G4_FP_2023_038", 1, 26, 2028, {
    1: (2024, "No leap day in between: 2024 gives Friday"),
    2: (2025, "Past 29th February 2024 the day moves on by 2"),
    3: (2027, "2026 gives Monday and 2027 gives Tuesday"),
    4: (2027, "Republic Day falls on a Tuesday in 2027"),
}, note="Republic Day, year by year", uses_options=True)

yearline("EXT_G4_FP_2024_036", 8, 15, 2031, {
    1: (2027, "2025 Friday, 2026 Saturday, 2027 Sunday"),
    2: (2028, "Past 29th February 2028 the day moves on by 2"),
    3: (2029, "One more year: Wednesday in 2029"),
}, note="Independence Day, year by year", uses_options=True)

yearline("PYQ_2016_Q27", 1, 26, 2022, {
    1: (2017, "2016 is a leap year: Tuesday moves on by 2 to Thursday"),
    2: (2019, "On by 1 each year: 2018 Friday, 2019 Saturday"),
    3: (2020, "No 29 February in between: on by 1 to Sunday"),
    4: (2020, "Republic Day falls on a Sunday in 2020"),
}, note="Republic Day, year by year", uses_options=True)

yearline("PYQ_2019_Q33", 4, 15, 2021, {
    0: (2019, "The 12th birthday is on 15th April 2021, two years later"),
    1: (2020, "Past 29th February 2020: Monday moves on by 2"),
    2: (2021, "No leap day this time: Wednesday moves on by 1"),
    3: (2021, "The 12th birthday falls on a Thursday"),
}, target=2021, note="10th birthday on a Monday. 12th birthday: ?")

yearline("Q_CH17_003", 1, 1, 2024, {
    0: (2023, "All of 2023 lies in between: 365 days"),
    1: (2023, "365 days is 52 weeks and 1 day"),
    2: (2024, "One day after Sunday: 1st January 2024 was a Monday"),
}, ask=True, target=2024, note="1st January, one year on")

yearline("Q_CH17_004", 1, 1, 2025, {
    0: (2024, "2024 is a leap year: 366 days"),
    1: (2025, "2 extra days: Monday + 2 = Wednesday"),
    2: (2025, "1st January 2025 is a Wednesday"),
}, ask=True, target=2025, note="1st January, one year on")

yearline("Q_CH17_005", 1, 26, 1997, {
    0: (1993, "From 1993 to 1997 is 4 years"),
    1: (1997, "Odd days: 1 + 1 + 1 + 2 = 5", True),
    2: (1997, "Tuesday + 5 days = Sunday"),
    3: (1997, "Republic Day 1997 was a Sunday"),
}, ask=True, target=1997, note="Republic Day, four years on")

yearline("Q_CH17_006", 1, 26, 2008, {
    0: (2007, "The leap day of 2008 comes later, in February"),
    1: (2007, "365 days is 52 weeks and 1 day"),
    2: (2008, "The day moves on by 1, from Friday to Saturday"),
}, ask=True, target=2008, note="Republic Day, one year on")

yearline("Q_CH17_016", 4, 1, 2004, {
    0: (2003, "29th February 2004 comes before 1st April: 366 days"),
    1: (2003, "366 days make 52 full weeks and 2 days"),
    2: (2004, "Only the 2 extra days matter", True),
    3: (2004, "Two days after Tuesday is Thursday"),
}, ask=True, target=2004, note="1st April, one year on")

yearline("Q_CH17_022", 8, 3, 2018, {
    0: (2015, "6th birthday, 2015: no leap day, so 1 day on"),
    1: (2016, "7th birthday, 2016: past 29th February, so 2 days on"),
    2: (2017, "8th birthday, 2017: 1 day on, a Thursday"),
    3: (2017, "The 8th birthday falls on a Thursday"),
}, note="5th birthday: 3rd August 2014, a Sunday", expect=lambda year: "%dth" % (5 + year - 2014))

yearline("Q_CH17_025", 10, 2, 2006, {
    0: (2000, "Usually 365 days: 52 weeks and 1 day, so on by 1"),
    1: (2003, "2001 Tuesday, 2002 Wednesday, 2003 Thursday"),
    2: (2004, "Past 29th February 2004: a jump of 2 days to Saturday"),
    3: (2005, "One more ordinary year: Saturday moves on to Sunday"),
}, note="2nd October, year by year", uses_options=True)


# ── Rule: a strip of months for counting days ────────────────────────────────

def strip(segs, brace=None, note=None, hl=None):
    """segs: (label, days). Drawn in proportion, except that a very short piece is widened to hold its label."""
    total = float(sum(d for _, d in segs))
    floor = min(0.11 * total, 0.6 * total / len(segs))
    if brace is None:
        brace = KEEP["brace"]   # a step keeps the brace of the figure before it unless it sets its own
    else:
        KEEP["brace"] = brace
    return BM([(None, [(max(d, floor), lab, "ab"[i % 2]) for i, (lab, d) in enumerate(segs)], brace)], note=note, hl=hl)


KEEP = {"brace": None}


_put = P.put


def put_then_forget(*args, **kwargs):
    """Every question starts with no brace carried over from the one before."""
    _put(*args, **kwargs)
    KEEP["brace"] = None


P.put = put_then_forget


def days_in(month, year=2023):
    return calendar.monthrange(year, month)[1]


def month_no(name):
    return [m.lower() for m in MONTHS].index(name[:3].lower()) + 1


def span(qid, year=2023, count_first=True, full=True):
    """Months and days from 'D Month' to 'D Month' in the question text. Returns [(month number, days)]."""
    found = re.findall(r"(\d+)(?:st|nd|rd|th)? (" + "|".join(calendar.month_name[1:]) + "|" + "|".join(MONTHS) + r")", P.text(qid))
    (d1, m1), (d2, m2) = [(int(d), month_no(m)) for d, m in found[:2]]
    out = []
    for m in range(m1, m2 + 1):
        if m == m1:
            n = days_in(m, year) - d1 + (1 if count_first else 0)
        elif m == m2:
            n = d2
        else:
            n = days_in(m, year)
        out.append((m, n))
    return out


def named(parts, full=True):
    return [(calendar.month_name[m] if full else MONTHS[m - 1], n) for m, n in parts]


def total_is(qid, parts):
    want = sum(n for _, n in parts)
    if float(want) not in P.allowed(qid, len(P.steps(qid)) - 1):
        P.problems.append("%s: the strip counts %d days, which the question never states" % (qid, want))
        return False
    return True


# 17th April to 3rd June
parts = span("EXT_G4_WS2_CH17_009")
if total_is("EXT_G4_WS2_CH17_009", parts):
    S = named(parts)
    P.put("EXT_G4_WS2_CH17_009",
          strip(S, brace="17 April to 3 June: ?", note="How many days long was the vacation?"),
          {0: strip(S, hl=["b0s0"], note="April: the 17th to the 30th, counting the 17th too, is 14 days"),
           1: strip(S, hl=["b0s1"], note="May has 31 days"),
           2: strip(S, hl=["b0s2"], note="June gives 3 days, from the 1st to the 3rd"),
           3: strip(S, brace="48 days", note="14 + 31 + 3 = 48 days")},
          origin="rule")

# 22nd April, 40 days
S = [("April", days_in(4) - 22 + 1), ("May", days_in(5))]
P.put("EXT_G4_WS2_CH17_010", None,
      {0: strip(S, hl=["b0s0"], note="April: count from the 22nd to the 30th, counting the 22nd too"),
       1: strip(S, brace="40 days", hl=["b0s1"], note="The vacation days left after April go into May"),
       2: strip(S, brace="40 days", hl=["b0s1"], note="May has exactly 31 days: the last day is 31st May"),
       3: strip(S, brace="40 days", note="School reopens the next day, 1st June")})

# June and July
S = [("June", days_in(6)), ("July", days_in(7))]
P.put("G4A_TIME_002",
      strip(S, brace="? days"),
      {0: strip(S, hl=["b0s0"], note="June has 30 days"),
       1: strip(S, hl=["b0s1"], note="July has 31 days"),
       3: strip(S, brace="61 days", note="June and July have 61 days altogether")})

# 20 February 2024 to 5 March 2024
parts = span("G4A_TIME_012", year=2024, count_first=False)
if total_is("G4A_TIME_012", parts):
    S = named(parts)
    P.put("G4A_TIME_012",
          strip(S, brace="20 Feb to 5 Mar: ? days", note="The year is 2024"),
          {0: strip(S, hl=["b0s0"], note="2024 is a leap year, so February has 29 days"),
           1: strip(S, hl=["b0s0"], note="Count the days left in February after the 20th"),
           2: strip(S, hl=["b0s1"], note="Add the 5 days of March"),
           3: strip(S, brace="14 days", note="5 March 2024 is 14 days after 20 February 2024")},
          origin="rule")

# 1st March to 1st May, both counted
parts = span("Q_CH17_002")
if total_is("Q_CH17_002", parts):
    S = [("March", parts[0][1]), ("April", parts[1][1]), ("1 May", parts[2][1])]
    P.put("Q_CH17_002",
          strip(S, brace="1 March to 1 May: ? days", note="Both dates are counted"),
          {0: strip(S, hl=["b0s0"], note="All of March, the 1st to the 31st: 31 days"),
           1: strip(S, hl=["b0s1"], note="All of April: 30 days"),
           2: strip(S, hl=["b0s2"], note="1 May itself: 1 more day"),
           3: strip(S, brace="62 days", note="31 + 30 + 1 = 62 days")},
          origin="rule")

# 15th August to 2nd October, the 15th not counted
parts = span("Q_CH17_020", count_first=False)
if total_is("Q_CH17_020", parts):
    S = named(parts)
    P.put("Q_CH17_020",
          strip(S, brace="15 Aug to 2 Oct: ? days", note="15th August itself is not counted"),
          {0: strip(S, hl=["b0s0"], note="August: the 16th to the 31st is 16 days"),
           1: strip(S, hl=["b0s1"], note="All 30 days of September are counted"),
           2: strip(S, hl=["b0s2"], note="October: the 1st and the 2nd, which is 2 days"),
           3: strip(S, brace="48 days", note="16 + 30 + 2 = 48 days")},
          origin="rule")

# 2nd October (Wednesday) to 14th November
parts = span("Q_CH17_009", count_first=False)
if total_is("Q_CH17_009", parts):
    S = named(parts)
    P.put("Q_CH17_009",
          strip(S, brace="2 Oct (Wed) → 14 Nov (?)", note="Count the days from Gandhi Jayanti to Children's Day"),
          {0: strip(S, note="29 days left in October + 14 in November = 43 days"),
           1: strip(S, note="43 days = 6 weeks + 1 day"),
           2: strip(S, brace="2 Oct Wed → 14 Nov Thu", note="Wednesday + 1 = Thursday")},
          origin="rule")

# 26 Jan 2020 (Sunday) to 15 Aug
parts = span("Q_CH17_010", year=2020, count_first=False)
if total_is("Q_CH17_010", parts):
    S = named(parts, full=False)
    P.put("Q_CH17_010",
          strip(S, brace="26 Jan (Sun)→15 Aug (?)", note="The year is 2020"),
          {0: strip(S, note="Days: 5 + 29 + 31 + 30 + 31 + 30 + 31 + 15"),
           1: strip(S, note="Total = 202 days"),
           2: strip(S, brace="26 Jan Sun → 15 Aug Sat", note="Sunday + 6 = Saturday")},
          origin="rule")

# World Cup: 17th March (Wednesday), final on the second Sunday in May
S = [("March", days_in(3) - 17), ("April", days_in(4)), ("May", 14)]
P.put("Q_CH17_015",
      strip(S, brace="17 March (Wed) → May", note="The final is on the second Sunday in May"),
      {0: strip(S, note="Mar(14) + Apr(30) + May(1) = 45 days to 1 May"),
       1: strip(S, note="45 ÷ 7 = 6 R 3. Wednesday + 3 = Saturday, so 1 May is a Saturday"),
       2: T([["Sat", "Sun", "Sun"]], headers=["1 May", "2 May", "9 May"], note="The second Sunday is the 9th of May")})

# 1 Jan 2019 (Tuesday) to 25 Dec
parts = span("Q_CH17_017", year=2019, count_first=False)
if total_is("Q_CH17_017", parts):
    S = named(parts, full=False)
    P.put("Q_CH17_017",
          strip(S, brace="1 Jan (Tue) → 25 Dec (?)", note="The year is 2019"),
          {0: strip(S, note="2019 is not a leap year. Count the days month by month"),
           1: strip(S, note="358 days = 51 weeks and 1 day"),
           2: strip(S, brace="1 Jan Tue → 25 Dec Wed", note="Tuesday + 1 = Wednesday")},
          origin="rule")

# Teachers' Day (5 Sep 2016, Monday) to Christmas
S = [("Sep", days_in(9) - 5), ("Oct", days_in(10)), ("Nov", days_in(11)), ("Dec", 25)]
P.put("Q_CH17_021",
      strip(S, brace="5 Sep (Mon) → Christmas", note="Count the days from Teachers' Day to Christmas"),
      {0: strip(S, note="Sep(25) + Oct(31) + Nov(30) + Dec(25) = 111 days"),
       1: strip(S, note="111 ÷ 7 = 15 R 6"),
       2: strip(S, brace="5 Sep Mon → 25 Dec Sun", note="Monday + 6 = Sunday")})

# All Fool's Day 2017 (Saturday) to Teachers' Day. The dates are part of what is asked, so no figure before.
S = [("Apr", 29), ("May", 31), ("Jun", 30), ("Jul", 31), ("Aug", 31), ("Sep", 5)]
P.put("PYQ_2017_Q13", None,
      {0: strip(S, brace="1 Apr (Sat) → 5 Sep (?)", note="Days after 1 April: 29 + 31 + 30 + 31 + 31 + 5"),
       1: strip(S, brace="1 Apr (Sat) → 5 Sep (?)", note="29 + 31 + 30 + 31 + 31 + 5 = 157 days"),
       2: strip(S, brace="1 Apr (Sat) → 5 Sep (?)", note="157 days is 22 weeks and 3 days"),
       3: strip(S, brace="1 Apr Sat → 5 Sep Tue", note="Three days after Saturday is Tuesday")})


# ── Dates inside one month ───────────────────────────────────────────────────

P.put("EXT_G4_FP_2020_009",
      NL(1, 17, points=[(17, "Sat"), (1, "?")], note="The 17th is a Saturday. Which day is the 1st?"),
      {0: NL(1, 17, points=[(17, "Sat"), (10, "Sat"), (1, "?")], hops=[(17, 10, "−7")], hl=["h0", "p1"],
             note="Go back 7 days: the 10th is also a Saturday"),
       1: NL(1, 17, points=[(17, "Sat"), (10, "Sat"), (3, "Sat")], hops=[(17, 10, "−7"), (10, 3, "−7")], hl=["h1", "p2"],
             note="Go back 7 more days: the 3rd is also a Saturday"),
       2: T([["Thu", "Fri", "Sat"]], headers=["1st", "2nd", "3rd"], note="Count back from the 3rd"),
       3: T([["Thu", "Fri", "Sat"]], headers=["1st", "2nd", "3rd"], note="The first day of the month was a Thursday")})

P.put("EXT_G4_FP_2025_027",
      NL(1, 31, points=[(15, "Thu")], note="August 2024. Which day came 5 times?"),
      {0: NL(1, 31, points=[(15, "Thu"), (8, "Thu"), (1, "Thu")], hops=[(15, 8, "1 week"), (8, 1, "1 week")], hl=["p1", "p2"],
             note="Count back in sevens: the 8th and the 1st are Thursdays too"),
       1: NL(1, 31, points=[(15, "Thu"), (8, "Thu"), (1, "Thu")], note="August has 31 days: 4 full weeks and 3 days more"),
       2: T([["Thu", "Fri", "Sat"]], headers=["29th", "30th", "31st"], note="The 3 extra dates: these three days come 5 times"),
       3: T([["Thu", "Fri", "Sat"]], headers=["29th", "30th", "31st"], note="Of the days in the choices, only Saturday is here")})

P.put("PYQ_2019_Q08",
      NL(1, 30, points=[(19, "Thu")], note="April 2018. Which days came 5 times?"),
      {0: NL(1, 30, points=[(19, "Thu"), (12, "Thu"), (5, "Thu")], hops=[(19, 12, "−7"), (12, 5, "−7")], hl=["p1", "p2"],
             note="Go back in steps of 7: the 12th and the 5th are Thursdays"),
       1: T([["Sun", "Mon", "Tue", "Wed", "Thu"]], headers=["1st", "2nd", "3rd", "4th", "5th"], note="Count back from Thursday the 5th"),
       2: T([["Sun", "Mon", "Sun", "Mon"]], headers=["1st", "2nd", "29th", "30th"], note="April has 30 days: 4 weeks and 2 days"),
       3: T([["Sun", "Mon", "Sun", "Mon"]], headers=["1st", "2nd", "29th", "30th"], note="Sunday and Monday come 5 times")})

P.put("Q_CH17_018",
      NL(1, 30, points=[(9, "Mon")], note="April 1990. Which days came five times?"),
      {0: NL(1, 30, points=[(9, "Mon"), (2, "Mon")], hops=[(9, 2, "−7")], hl=["p1"],
             note="Monday the 2nd, so the 1st of April was a Sunday"),
       1: NL(1, 30, points=[(9, "Mon"), (2, "Mon")], note="April has 30 days: 4 full weeks and 2 days more"),
       2: T([["Sun", "Mon", "Sun", "Mon"]], headers=["1st", "2nd", "29th", "30th"], note="The 2 extra days fall on the same days as the 1st and 2nd"),
       3: T([["Sundays", "1, 8, 15, 22, 29"], ["Mondays", "2, 9, 16, 23, 30"]], note="Sunday and Monday occurred five times")})

P.put("Q_CH17_008", None,
      {0: T([["like the 1st", "like the 2nd", "like the 3rd"]], headers=["29th", "30th", "31st"], note="July has 31 days: 4 weeks and 3 days"),
       1: T([["Wed", "Thu", "Fri"]], headers=["1 July", "2 July", "3 July"], note="The days that come 5 times start the month"),
       2: T([["Wed", "Thu", "Fri", "Sat", "Sun"]], headers=["1st", "2nd", "3rd", "4th", "5th"], note="5 July is the first Sunday"),
       3: T([["Sun", "Sun", "Sun", "Sun"]], headers=["5th", "12th", "19th", "26th"], note="Add 7 each time to find the other Sundays")})

P.put("G4A_TIME_005",
      NL(0, 10, points=[(0, "Wed"), (10, "?")], note="Today is Wednesday. Which day is it 10 days from today?"),
      {0: NL(0, 10, points=[(0, "Wed"), (7, "Wed"), (10, "?")], hops=[(0, 7, "+7")], hl=["h0", "p1"], note="After 7 days it is Wednesday again"),
       1: NL(0, 10, points=[(0, "Wed"), (7, "Wed"), (10, "?")], hops=[(0, 7, "+7"), (7, 10)], hl=["h1"], note="Count the days still to go, from day 7 to day 10"),
       2: NL(0, 10, points=[(0, "Wed"), (7, "Wed"), (10, "Sat")], hops=[(0, 7, "+7"), (7, 10, "Thu, Fri, Sat")], hl=["h1", "p2"],
             note="Three days after Wednesday"),
       3: NL(0, 10, points=[(0, "Wed"), (7, "Wed"), (10, "Sat")], hops=[(0, 7, "+7"), (7, 10)], hl=["p2"], note="It will be Saturday")})

P.put("G4A_TIME_011",
      NL(5, 23, points=[(5, "Tue"), (23, "?")], note="The 5th is a Tuesday. Which day is the 23rd?"),
      {0: NL(5, 23, points=[(5, "Tue"), (23, "?")], note="The Tuesdays are 7 days apart"),
       1: NL(5, 23, points=[(5, "Tue"), (19, "Tue"), (23, "?")], hops=[(5, 19, "+7 +7")], hl=["h0", "p1"], note="So the 19th is a Tuesday"),
       2: NL(5, 23, points=[(5, "Tue"), (19, "Tue"), (23, "?")], hops=[(5, 19, "+7 +7"), (19, 23)], hl=["h1"], note="Count the days from the 19th to the 23rd"),
       3: NL(5, 23, points=[(5, "Tue"), (19, "Tue"), (23, "?")], hops=[(5, 19, "+7 +7"), (19, 23, "Wed Thu Fri Sat")], hl=["h1"],
             note="Four days after Tuesday"),
       4: NL(5, 23, points=[(5, "Tue"), (19, "Tue"), (23, "Sat")], hops=[(5, 19, "+7 +7"), (19, 23)], hl=["p2"], note="The 23rd is a Saturday")})

P.put("G4A_TIME_014",
      NL(1, 30, points=[(1, "Sat")], note="A month of 30 days. How many Sundays?"),
      {0: NL(1, 30, points=[(2, "Sun")], hl=["p0"], note="The 1st is a Saturday, so the 2nd is the first Sunday"),
       1: NL(1, 30, points=[(2, "Sun"), (9, "Sun"), (16, "Sun"), (23, "Sun"), (30, "Sun")],
             hops=[(2, 9, "+7"), (9, 16, "+7"), (16, 23, "+7"), (23, 30, "+7")], note="Add 7 each time"),
       2: NL(1, 30, points=[(2, "Sun"), (9, "Sun"), (16, "Sun"), (23, "Sun"), (30, "Sun")], hl=["p4"], note="The 30th is still inside the month"),
       3: NL(1, 30, points=[(2, "Sun"), (9, "Sun"), (16, "Sun"), (23, "Sun"), (30, "Sun")], note="There are 5 Sundays in this month")})

P.put("Q_CH17_007",
      T([["14 Feb 1992", "Friday"], ["13 Feb 1993", "?"]], headers=["Date", "Day"]),
      {0: T([["14 Feb 1992", "Friday"], ["14 Feb 1993", "?"], ["13 Feb 1993", "?"]], headers=["Date", "Day"], hl=["r0", "r1"],
            note="1992 is a leap year: 366 days from 14 Feb 1992 to 14 Feb 1993"),
       1: T([["14 Feb 1992", "Friday"], ["14 Feb 1993", "Sunday"], ["13 Feb 1993", "?"]], headers=["Date", "Day"], hl=["r1"],
            note="Friday + 2 = Sunday"),
       2: T([["14 Feb 1992", "Friday"], ["14 Feb 1993", "Sunday"], ["13 Feb 1993", "Saturday"]], headers=["Date", "Day"], hl=["r2"],
            note="One day before Sunday is Saturday"),
       3: T([["14 Feb 1992", "Friday"], ["14 Feb 1993", "Sunday"], ["13 Feb 1993", "Saturday"]], headers=["Date", "Day"], hl=["r2"],
            note="13 Feb 1993 was a Saturday")})

P.put("EXT_G4_WS2_CH17_008",
      NL(1990, 2004, 1, ticks="ends", note="Leap years between 1990 and 2004 = ?"),
      {0: NL(1990, 2004, 1, ticks="ends", points=[(1992, "1992")], hl=["p0"], note="1990 does not divide by 4 exactly, but 1992 does"),
       1: NL(1990, 2004, 1, ticks="ends", points=[(1992, "1992"), (1996, "1996"), (2000, "2000")],
             hops=[(1992, 1996, "+4"), (1996, 2000, "+4"), (2000, 2004, "+4")], note="Keep adding 4 years. The next one would be 2004"),
       2: NL(1990, 2004, 1, ticks="ends", points=[(1992, "1992"), (1996, "1996"), (2000, "2000")],
             note="2004 is an end year, so it is not between 1990 and 2004"),
       3: NL(1990, 2004, 1, ticks="ends", points=[(1992, "1992"), (1996, "1996"), (2000, "2000")], hl=["p0", "p1", "p2"],
             note="1992, 1996 and 2000: that is 3 leap years")})


# ── Clocks ───────────────────────────────────────────────────────────────────

P.put("EXT_G4_FP_2020_033", None,
      {1: CL(6, 30, hl=["minute"], note="At half past six the minute hand points exactly at 6"),
       2: CL(6, 30, hl=["hour"], note="The hour hand has moved halfway from 6 to 7"),
       3: CL(6, 30, angle=True, hl=["angle"], note="Half of one 30° gap: the angle is 15°")})

P.put("EXT_G4_FP_2021_011", None,
      {2: ANG("single", [("30°", 30)], note="In 5 minutes the minute hand turns 30 degrees")})

P.put("EXT_G4_FP_2021_022", None,
      {1: CL(7, 30, hl=["hour", "minute"], note="At 7:30 the minute hand is on 6. The hour hand is past 7"),
       2: CL(7, 30, angle=True, note="From 6 to 7 is 30°. From 7 to the hour hand is 15°"),
       3: CL(7, 30, angle=True, hl=["angle"], note="30° + 15° = 45°, so the time is 07:30")})

P.put("EXT_G4_FP_2023_034",
      CL(8, 30, angle=True, note="Angle between the hands = ?"),
      {1: CL(8, 30, hl=["minute", "hour"], note="Minute hand on 6. Hour hand halfway between 8 and 9"),
       2: CL(8, 30, angle=True, note="From 6 to 8 is two gaps of 30°"),
       3: CL(8, 30, angle=True, hl=["hour"], note="The hour hand is half a gap, 15°, past 8"),
       4: CL(8, 30, angle=True, hl=["angle"], note="The angle is 75°, which is not listed")})

P.put("EXT_G4_WS2_CH17_005",
      CL(3, 45, note="Kriya's watch shows 3:45 pm. It is 5 minutes fast"),
      {0: CL(3, 40, note="Real time: 5 minutes before 3:45 pm is 3:40 pm"),
       1: CL(3, 40, hl=["minute"], note="Priya's watch is 10 minutes behind the real time"),
       2: CL(3, 30, note="Priya's watch shows 3:30 pm")})

P.put("EXT_G4_WS2_CH17_006",
      CL(6, 0, note="Real time 6:00 am. The clock loses 10 minutes every hour"),
      {0: CL(6, 0, note="Count the hours from 1:00 am to 6:00 am"),
       1: CL(6, 0, note="The clock loses 10 minutes in each of those hours"),
       2: CL(5, 10, note="50 minutes behind 6:00 am: the clock shows 5:10 am")})

P.put("EXT_G4_WS2_CH17_007", None,
      {1: CL(3, 15, note="The watch shows 3 hours 15 minutes after noon"),
       3: CL(3, 0, note="3 real hours after noon: the actual time is 3:00 pm")})

P.put("PYQ_2017_Q32",
      CL(8, 0, note="Real time 8:00 p.m. The watch gains 2 minutes every hour"),
      {0: CL(8, 0, note="From 8:00 a.m. to 8:00 p.m. is 12 hours"),
       1: CL(8, 0, note="In 12 hours the watch gains 24 minutes"),
       2: CL(8, 0, hl=["minute"], note="A watch that gains is ahead: add the 24 minutes"),
       3: CL(8, 24, note="24 minutes after 8:00 p.m.: the watch shows 8:24 p.m.")})

P.put("PYQ_2018_Q14",
      CL(10, 0, note="Real time 10 p.m. The watch loses 30 seconds every hour"),
      {0: CL(10, 0, note="From 8:00 a.m. to 10:00 p.m. is 14 hours"),
       1: CL(10, 0, note="In 14 hours the watch loses 420 seconds"),
       2: CL(10, 0, note="420 seconds is 7 minutes"),
       3: CL(9, 53, note="7 minutes before 10:00 p.m.: the watch shows 9:53 p.m.")})

P.put("G4A_TIME_001", None,
      {2: CL(5, 20, note="17:20 is 5:20 pm")})

P.put("G4A_TIME_007", None,
      {0: CL(6, 45, note="A quarter to 7 is 15 minutes before 7 o'clock: 6:45"),
       1: CL(6, 45, note="It is evening, so the time is 6:45 pm"),
       3: CL(6, 45, note="On the 24-hour clock 6:45 pm is 18:45")})

P.put("Q_CH17_013",
      CL(3, 45, note="3:45 PM"),
      {1: CL(3, 45, hl=["hour"], note="Add 12 to the 3 hours to get hour 15"),
       2: CL(3, 45, note="The minutes stay the same: 3:45 PM is 15:45")})

P.put("PYQ_2018_Q18", None,
      {1: FB([(4, 3, "45 min")], shape="circle", note="45 minutes is 3/4 of an hour"),
       2: FB([(4, 3, "0.75 hr")], shape="circle", note="3/4 is the same as 75/100, which is 0.75"),
       3: FB([(4, 3, "0.75 hr")], shape="circle", note="3 whole hours and 0.75 of an hour: 3.75 hr")})


# ── Time lines ───────────────────────────────────────────────────────────────

P.put("EXT_G4_FP_2022_026",
      CL(4, 30, note="4:30 pm on 15th April. The minute hand then turns 30 times"),
      {0: CL(4, 30, hl=["minute"], note="Each full turn of the minute hand is 1 hour: 30 hours"),
       2: J(["15 Apr 4:30pm", "16 Apr 4:30pm"], [("24 h", None)], hl=["l0"], note="24 hours later it is the same time on the next day"),
       3: J(["15 Apr 4:30pm", "16 Apr 4:30pm", "16 Apr 10:30pm"], [("24 h", None), ("6 h", None)], hl=["l1"],
            note="6 hours after 4:30 pm is 10:30 pm")})

P.put("EXT_G4_FP_2024_025",
      CL(10, 30, note="10:30 am on 21st April. The minute hand then turns 42 times"),
      {0: CL(10, 30, hl=["minute"], note="Each full turn of the minute hand is 1 hour: 42 hours"),
       2: J(["21 Apr 10:30am", "22 Apr 10:30am"], [("24 h", None)], hl=["l0"], note="24 hours later it is the same time on the next day"),
       3: J(["21 Apr 10:30am", "22 Apr 10:30am", "22 Apr 10:30pm"], [("24 h", None), ("12 h", None)], hl=["l1"],
            note="12 hours more. There are still 6 hours to add"),
       4: J(["22 Apr 10:30am", "22 Apr 10:30pm", "23 Apr 4:30am"], [("12 h", None), ("6 h", None)], hl=["l1"],
            note="6 hours after 10:30 pm is 4:30 am the next day")})

P.put("EXT_G4_FP_2023_002",
      J(["2 Mar 12:00am", "?"], [("2023 min", None)], note="What is the date and time 2023 minutes later?"),
      {0: J(["2 Mar 12:00am", "?"], [("2023 min", None)], note="33 hours use up 1980 minutes"),
       1: J(["2 Mar 12:00am", "?"], [("33 h 43 min", None)], hl=["l0"], note="2023 minutes is 33 hours 43 minutes"),
       3: J(["2 Mar 12:00am", "3 Mar 12:00am", "?"], [("24 h", None), None], hl=["l0"], note="24 hours later it is 12:00 am on 3rd March"),
       4: J(["2 Mar 12:00am", "3 Mar 12:00am", "3 Mar 9:43am"], [("24 h", None), ("9 h 43 min", None)], hl=["l1"],
            note="9 hours 43 minutes later it is 9:43 am on 3rd March")})

P.put("EXT_G4_FP_2025_029",
      J(["7:00 am", "next bus"], [("36 min", None)], note="A bus leaves every 36 min. You arrive at 8:50 am"),
      {0: T([["7:00 am", "7:36 am", "8:12 am", "8:48 am"]], note="The buses leave 36 minutes apart"),
       1: T([["7:00 am", "7:36 am", "8:12 am", "8:48 am"]], hl=["r0"], note="The 8:48 am bus has just left when you arrive at 8:50 am"),
       2: J(["8:48 am", "next bus"], [("36 min", None)], hl=["l0"], note="48 + 36 = 84 minutes, which is 1 hour 24 minutes"),
       3: J(["8:48 am", "9:24 am"], [("36 min", None)], note="The next bus is at 9:24 am")})

P.put("EXT_G4_WS2_CH17_003",
      J(["Pune", "Mumbai"], [("planned 3 h 40 min", "late by ?")], note="Left at quarter past eight, reached at quarter to 1"),
      {0: J(["Pune 8:15 am", "Mumbai 12:45pm"], [("planned 3 h 40 min", "late by ?")], note="Quarter past eight is 8:15 am. Quarter to 1 is 12:45 pm"),
       1: J(["Pune 8:15 am", "Mumbai 12:45pm"], [("took 4 h 30 min", "planned 3 h 40 min")], hl=["l0"], note="8:15 am to 12:15 pm is 4 hours, then 30 minutes more"),
       2: J(["Pune 8:15 am", "Mumbai 12:45pm"], [("took 270 min", "planned 3 h 40 min")], hl=["l0"], note="4 hours 30 minutes is 270 minutes"),
       3: J(["Pune 8:15 am", "Mumbai 12:45pm"], [("took 270 min", "planned 220 min")], hl=["l0"], note="3 hours 40 minutes is 220 minutes"),
       4: J(["Pune 8:15 am", "Mumbai 12:45pm"], [("took 270 min", "planned 220 min")], note="270 − 220: the train was late by 50 min")})

P.put("G4A_TIME_006",
      J(["8:00 am", "1:30 pm"], [("?", None)], note="How long is the school day?"),
      {0: J(["8:00 am", "12 noon", "1:30 pm"], [None, None], hl=["l0"], note="First count from 8:00 am to 12 noon"),
       1: J(["8:00 am", "12 noon", "1:30 pm"], [None, ("1 h 30 min", None)], hl=["l1"], note="From 12 noon to 1:30 pm is 1 hour 30 minutes"),
       2: J(["8:00 am", "12 noon", "1:30 pm"], [("4 h", None), ("1 h 30 min", None)], note="4 hours and 1 hour 30 minutes make 5 hours 30 minutes")})

P.put("G4A_TIME_009",
      J(["9:30 pm", "?"], [("6 h 45 min", None)], note="Bengaluru to Chennai by night bus"),
      {0: J(["9:30 pm", "3:30 am", "?"], [("6 h", None), None], hl=["l0"], note="Add 6 hours to 9:30 pm: 3:30 am the next day"),
       1: J(["9:30 pm", "3:30 am", "4:00 am", "?"], [("6 h", None), ("30 min", None), None], hl=["l1"], note="30 of the 45 minutes take the time to 4:00 am"),
       2: J(["9:30 pm", "3:30 am", "4:00 am", "?"], [("6 h", None), ("30 min", None), None], hl=["l2"], note="Find the minutes that remain: 45 − 30"),
       3: J(["9:30 pm", "3:30 am", "4:00 am", "4:15 am"], [("6 h", None), ("30 min", None), ("15 min", None)], hl=["l2"],
            note="The bus reaches Chennai at 4:15 am")})

P.put("G4A_TIME_010",
      J(["Mumbai 22:40", "Goa 05:10"], [("?", None)], note="How long is the journey?"),
      {0: J(["22:40", "midnight", "05:10"], [("1 h 20 min", None), None], hl=["l0"], note="From 22:40 to midnight is 1 hour 20 minutes"),
       1: J(["22:40", "midnight", "05:10"], [("1 h 20 min", None), ("5 h 10 min", None)], hl=["l1"], note="From midnight to 05:10 is 5 hours 10 minutes"),
       2: J(["22:40", "midnight", "05:10"], [("1 h 20 min", None), ("5 h 10 min", None)], note="1 h 20 min + 5 h 10 min = 6 h 30 min"),
       3: J(["Mumbai 22:40", "Goa 05:10"], [("6 h 30 min", None)], note="The journey takes 6 hours 30 minutes")})

P.put("G4A_TIME_015",
      J(["Leave home: ?", "At station", "Train 14:10"], [("35 min", None), ("25 min", None)], note="What is the latest time she can leave home?"),
      {0: J(["Leave home: ?", "At station", "Train 14:10"], [("35 min", None), ("25 min", None)], hl=["l0", "l1"], note="25 + 35 = 60 minutes are needed before 14:10"),
       1: J(["Leave home: ?", "At station", "Train 14:10"], [("35 min", None), ("25 min", None)], note="60 minutes is 1 hour"),
       2: J(["Leave: 13:10", "At station", "Train 14:10"], [("35 min", None), ("25 min", None)], note="One hour before 14:10 is 13:10"),
       3: J(["Leave: 13:10", "At station", "Train 14:10"], [("35 min", None), ("25 min", None)], note="Change 13:10 to the 12-hour clock"),
       4: J(["Leave: 1:10 pm", "At station", "Train 14:10"], [("35 min", None), ("25 min", None)], note="The latest she can leave home is 1:10 pm")})

P.put("Q_CH17_012",
      J(["2:40 PM", "5:10 PM"], [("?", None)], note="How long is the movie?"),
      {0: J(["2:40", "3:00", "5:10"], [("20 min", None), None], hl=["l0"], note="From 2:40 to 3:00 is 20 minutes"),
       1: J(["2:40", "3:00", "5:00", "5:10"], [("20 min", None), ("2 h", None), None], hl=["l1"], note="From 3:00 to 5:00 is 2 hours"),
       2: J(["2:40", "3:00", "5:00", "5:10"], [("20 min", None), ("2 h", None), ("10 min", None)], hl=["l2"], note="From 5:00 to 5:10 is 10 minutes"),
       3: J(["2:40", "3:00", "5:00", "5:10"], [("20 min", None), ("2 h", None), ("10 min", None)], note="2 hours, and 20 + 10 minutes: 2 hours 30 minutes")})

P.put("Q_CH17_019",
      J(["09:45", "?"], [("4 h 35 min", None)], note="Departs at 09:45. When does it arrive?"),
      {0: J(["09:45", "13:45", "?"], [("4 h", None), ("35 min", None)], hl=["l0"], note="Add the 4 hours first: 09:45 plus 4 hours is 13:45"),
       1: J(["09:45", "13:45", "?"], [("4 h", None), ("35 min", None)], hl=["l1"], note="Now add the minutes: 45 + 35 = 80"),
       2: J(["09:45", "13:45", "?"], [("4 h", None), ("35 min", None)], hl=["l1"], note="80 minutes is 1 hour and 20 minutes"),
       3: J(["09:45", "13:45", "14:20"], [("4 h", None), ("35 min", None)], note="14:20 is 2:20 PM on the 12-hour clock")})


# ── Bars of equal pieces: changing units, repeated gaps ──────────────────────

gap = "%d min" % 35
P.put("EXT_G4_WS2_CH17_002",
      BM([(None, [(1, gap)] * 4, None)], note="Rings: the 1st at 9:00 am, the 5th at ?"),
      {0: BM([(None, [(1, gap)] * 4, None)], hl=["b0"], note="From the 1st ring to the 5th ring there are 4 gaps"),
       1: BM([(None, [(1, gap)] * 4, "4 gaps")], note="Find the time for 4 gaps of 35 minutes"),
       2: BM([(None, [(1, gap)] * 4, "140 min = 2 h 20 min")], note="140 minutes is 2 hours 20 minutes"),
       3: BM([(None, [(1, gap)] * 4, "2 h 20 min")], note="2 hours 20 minutes after 9:00 am is 11:20 am")})

P.put("G4A_TIME_004", None,
      {0: BM([(None, [(60, "60 min"), (60, "60 min"), (15, "?")], "135 min")], hl=["b0s0", "b0s1"], note="Two full hours fit into 135 minutes"),
       1: BM([(None, [(60, "60 min"), (60, "60 min"), (15, "?")], "135 min")], hl=["b0s2"], note="Find the minutes left over"),
       2: BM([(None, [(60, "1 hour"), (60, "1 hour"), (15, "15 min")], "135 min")], note="135 minutes is 2 hours 15 minutes")})

P.put("G4A_TIME_008",
      BM([(None, [(1, "1 day")] * 3, "? hours")], note="The journey takes exactly 3 days"),
      {0: BM([(None, [(1, "24 h")] * 3, "? hours")], hl=["b0s0"], note="One full day has 24 hours"),
       1: BM([(None, [(1, "24 h")] * 3, "? hours")], hl=["b0"], note="Multiply 24 hours by 3 days"),
       2: BM([(None, [(1, "24 h")] * 3, "72 hours")], note="The journey takes 72 hours")})

P.put("G4A_TIME_013",
      BM([(None, [(1, "40 min")] * 7, "1 week = ?")], note="40 minutes every day for one week"),
      {0: BM([(None, [(1, "40 min")] * 7, "1 week = ?")], hl=["b0"], note="Find the minutes in one week"),
       1: BM([(None, [(1, "40 min")] * 7, "1 week = ?")], hl=["b0s%d" % i for i in range(6)], note="Four hours are 240 minutes"),
       2: BM([(None, [(1, "40 min")] * 7, "1 week = ?")], hl=["b0s6"], note="Find the minutes left over"),
       3: BM([(None, [(1, "40 min")] * 7, "4 h 40 min")], note="He practises for 4 hours 40 minutes in one week")})

P.put("Q_CH17_011",
      BM([(None, [(60, "1 hour")] * 3 + [(45, "45 min")], "? minutes")], note="3 hours 45 minutes"),
      {0: BM([(None, [(60, "60 min")] * 3 + [(45, "45 min")], "? minutes")], hl=["b0s0", "b0s1", "b0s2"], note="One hour is 60 minutes, so 3 hours is 180 minutes"),
       1: BM([(None, [(60, "60 min")] * 3 + [(45, "45 min")], "225 minutes")], hl=["b0s3"], note="Add the extra 45 minutes: 225 minutes")})

P.write()
