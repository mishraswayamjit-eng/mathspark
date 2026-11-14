"""Tiny shorthand used by the a_y*.py authoring files. No rules live here."""


def F(kind, note=None, hl=None, **fields):
    """A figure of the given kind."""
    fig = {"kind": kind}
    fig.update(fields)
    if hl:
        fig["highlight"] = hl
    if note:
        fig["note"] = note
    return fig


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


def bars(*bs, **kw):
    return F("barModel", bars=list(bs), **kw)


def fb(*items, **kw):
    """Fraction bars: each item is (parts, shaded) or (parts, shaded, label)."""
    out = []
    for it in items:
        b = {"parts": it[0], "shaded": it[1]}
        if len(it) > 2:
            b["label"] = it[2]
        out.append(b)
    return F("fractionBars", bars=out, **kw)


def V(figure=None, steps=None, **flags):
    """One question's visual."""
    v = {"origin": "authored"}
    if figure is not None:
        v["figure"] = figure
    if steps is not None:
        v["stepFigures"] = steps
    v.update(flags)
    return v
