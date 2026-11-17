"""Place value (gr5_placevalue): the question's number in the place-value chart, the digits asked about marked.

By rule: the number and the digits are read from the question text. Questions that
describe a number by clues, or name no number, get no figure (there is nothing given to draw).
"""
import re
from imported_other_lib import POOL, commas, staged

NUMBER = re.compile(r"(?<![\d,.])(\d{1,2}(?:,\d{2})*,\d{3}|\d{5,9})(?!\d|[,.]\d)")
ASKED = re.compile(r"(?:digit|value of(?: the)?|values of(?: the)?|and|&)\s+(\d)(?!\d|[,.]\d)")
PLACE = re.compile(r"(ten[- ]thousands?|thousands?|hundreds?|tens|units|ones|lakhs?)['’]? place", re.I)
NAMES = ["ones", "tens", "hundreds", "thousands", "ten thousands", "lakhs", "ten lakhs", "crores", "ten crores"]
POWER = {"one": 0, "unit": 0, "ten": 1, "hundred": 2, "thousand": 3, "ten thousand": 4, "ten-thousand": 4, "lakh": 5}


def chart(number, hl, note=None):
    fig = {"kind": "placeChart", "number": number}
    if hl:
        fig["highlight"] = ["d%d" % i for i in hl][:8]
    if note:
        fig["note"] = note
    return fig


def place_value(q):
    text = q["questionText"]
    if re.search(r"clue|where:|•", text, re.I):
        return
    m = NUMBER.search(text)
    if not m:
        return
    number = m.group(1).replace(",", "")
    if len(number) < 5 or len(number) > 9:
        return
    rest = text.replace(m.group(1), " ")
    spots = []
    for d in ASKED.findall(rest):
        spots += [i for i, c in enumerate(number) if c == d and i not in spots]
    for name in PLACE.findall(rest):
        power = POWER.get(name.lower().rstrip("s") if not name.lower().startswith("ten") or name.lower() == "tens" else name.lower().rstrip("s"))
        if name.lower() == "tens":
            power = 1
        if power is not None and power < len(number) and len(number) - 1 - power not in spots:
            spots.append(len(number) - 1 - power)
    spots.sort()
    before = chart(number, spots, "The digits the question asks about are marked" if spots else None)
    stages = []
    for i in spots:
        power = len(number) - 1 - i
        value = int(number[i]) * 10 ** power
        if power == 0 or value == 0:
            continue
        stages.append((value, [
            chart(number, [i], "The %s is in the %s place: it stands for %s" % (number[i], NAMES[power], commas(value))),
            chart(number, [i], "The %s is in the %s place" % (number[i], NAMES[power]))]))
    staged(q["id"], before, stages)


for _q in sorted(POOL.values(), key=lambda x: x["id"]):
    if _q["node"] == "gr5_placevalue":
        place_value(_q)
