"""Helpers for the gr4_counting lessons. The beat and board helpers are shared with gr4_units."""
from g4_units_lib import (a, arc, b, box, c, fig, finish, g, grp, l, n, pick, qfig, questions,  # noqa: F401
                          ring, think, u, w, write_part, x)

TOPIC = "gr4_counting"


def qf(qid, step=None, id="fg"):
    """The figure already drawn for this question (or one of its steps), as a board op."""
    return fig(id, qfig(TOPIC, qid, step))
