"""Small shortcuts for writing figures by hand (Past papers B). No rules live here:
every figure is decided per question in b_2021.py ... b_2025.py."""


def fig(kind, **kw):
    out = {"kind": kind}
    for k, v in kw.items():
        if v is not None:
            out[k] = v
    return out


def entry(figure=None, steps=None, **flags):
    out = {"origin": "authored"}
    if figure is not None:
        out["figure"] = figure
    if steps is not None:
        out["stepFigures"] = steps
    out.update(flags)
    return out


def bal(left, right, note=None, hl=None):
    return fig("balance", left=left, right=right, note=note, highlight=hl)


def tbl(rows, headers=None, note=None, hl=None):
    return fig("table", rows=rows, headers=headers, note=note, highlight=hl)


def nl(mn, mx, step, points=None, hops=None, note=None, hl=None):
    pts = None
    if points is not None:
        pts = [{"at": p} if not isinstance(p, tuple) else {"at": p[0], "label": p[1]} for p in points]
    hp = None
    if hops is not None:
        hp = []
        for h in hops:
            d = {"from": h[0], "to": h[1]}
            if len(h) > 2:
                d["label"] = h[2]
            hp.append(d)
    return fig("numberLine", min=mn, max=mx, step=step, points=pts, hops=hp, note=note, highlight=hl)


def seg(units, label=None, tone=None):
    s = {"units": units}
    if label is not None:
        s["label"] = label
    if tone is not None:
        s["tone"] = tone
    return s


def bar(segments, label=None, brace=None):
    b = {"segments": segments}
    if label is not None:
        b["label"] = label
    if brace is not None:
        b["brace"] = brace
    return b


def bars(bar_list, note=None, hl=None):
    return fig("barModel", bars=bar_list, note=note, highlight=hl)


def place(number, note=None, hl=None):
    return fig("placeChart", number=number, note=note, highlight=hl)


def journey(places, legs, note=None, hl=None):
    out = []
    for top, bottom in legs:
        leg = {}
        if top:
            leg["top"] = top
        if bottom:
            leg["bottom"] = bottom
        out.append(leg)
    return fig("journey", places=places, legs=out, note=note, highlight=hl)


def rect(hl=None, **kw):
    return fig("rectangle", highlight=hl, **kw)


def tri(shape, ab=None, bc=None, ca=None, hl=None, **kw):
    sides = {}
    for k, v in (("ab", ab), ("bc", bc), ("ca", ca)):
        if v is not None:
            sides[k] = v
    return fig("triangle", shape=shape, sides=sides or None, highlight=hl, **kw)


def clock(hour, minute, angle=None, note=None, hl=None):
    return fig("clock", hour=hour, minute=minute, showAngle=angle, note=note, highlight=hl)


def compass(facing, turns=None, end=None, note=None, hl=None):
    t = None
    if turns:
        t = [{"degrees": d, "direction": "clockwise" if c == "cw" else "anticlockwise"} for d, c in turns]
    return fig("compass", facing=facing, turns=t, showEnd=end, note=note, highlight=hl)


def angles(layout, parts, note=None, hl=None):
    ps = []
    for p in parts:
        if isinstance(p, tuple):
            ps.append({"label": p[0], "size": p[1]})
        else:
            ps.append({"label": p})
    return fig("angles", layout=layout, parts=ps, note=note, highlight=hl)


def fbars(bar_list, note=None, hl=None, shape=None):
    return fig("fractionBars", bars=[dict(zip(("parts", "shaded", "label"), b)) for b in bar_list], note=note, highlight=hl, shape=shape)
