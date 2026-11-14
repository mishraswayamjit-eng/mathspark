"""Small constructors for figure specs, shared by the c_b*.py authoring batches."""


def _base(fig, note=None, hl=None):
    if note:
        fig["note"] = note
    if hl:
        fig["highlight"] = list(hl)
    return fig


def pc(number, note=None, hl=None):
    return _base({"kind": "placeChart", "number": number}, note, hl)


def table(rows, note=None, hl=None, headers=None):
    fig = {"kind": "table", "rows": rows}
    if headers:
        fig["headers"] = headers
    return _base(fig, note, hl)


def seg(label=None, units=1, tone=None):
    s = {"units": units}
    if label:
        s["label"] = label
    if tone:
        s["tone"] = tone
    return s


def bar(segments, label=None, brace=None):
    b = {"segments": segments}
    if label:
        b["label"] = label
    if brace:
        b["brace"] = brace
    return b


def bm(bars, note=None, hl=None):
    return _base({"kind": "barModel", "bars": bars}, note, hl)


def nl(lo, hi, step, points=None, hops=None, note=None, hl=None):
    fig = {"kind": "numberLine", "min": lo, "max": hi, "step": step}
    if points:
        fig["points"] = [({"at": p[0], "label": p[1]} if len(p) > 1 and p[1] else {"at": p[0]}) for p in points]
    if hops:
        fig["hops"] = [({"from": h[0], "to": h[1], "label": h[2]} if len(h) > 2 else {"from": h[0], "to": h[1]}) for h in hops]
    return _base(fig, note, hl)


def fb(bars, note=None, hl=None, shape=None):
    out = []
    for b in bars:
        d = {"parts": b[0], "shaded": b[1]}
        if len(b) > 2 and b[2]:
            d["label"] = b[2]
        out.append(d)
    fig = {"kind": "fractionBars", "bars": out}
    if shape:
        fig["shape"] = shape
    return _base(fig, note, hl)


def balance(left, right, note=None, hl=None):
    return _base({"kind": "balance", "left": left, "right": right}, note, hl)


def venn(lt, rt, left, both, right, note=None, hl=None):
    return _base({"kind": "venn", "leftTitle": lt, "rightTitle": rt, "left": left, "both": both, "right": right}, note, hl)


def ftree(number, note=None, hl=None):
    return _base({"kind": "factorTree", "number": number}, note, hl)


def rect(length=None, breadth=None, inside=None, square=False, note=None, hl=None):
    fig = {"kind": "rectangle"}
    if square:
        fig["square"] = True
    if length:
        fig["length"] = length
    if breadth:
        fig["breadth"] = breadth
    if inside:
        fig["inside"] = inside
    return _base(fig, note, hl)


def tri(shape, sides=None, angles=None, note=None, hl=None):
    fig = {"kind": "triangle", "shape": shape}
    if sides:
        fig["sides"] = sides
    if angles:
        fig["angles"] = angles
    return _base(fig, note, hl)


def clock(hour, minute, note=None, hl=None):
    return _base({"kind": "clock", "hour": hour, "minute": minute}, note, hl)


def setf(total, groups=None, item=None, note=None, hl=None, shaded=None):
    fig = {"kind": "set", "total": total}
    if groups:
        fig["groups"] = groups
    if shaded is not None:
        fig["shadedGroups"] = shaded
    if item:
        fig["item"] = item
    return _base(fig, note, hl)


def entry(figure=None, steps=None, essential=False, uses_options=False):
    e = {"origin": "authored"}
    if figure:
        e["figure"] = figure
    if steps:
        e["stepFigures"] = steps
    if essential:
        e["essential"] = True
    if uses_options:
        e["usesOptions"] = True
    return e
