"""Hand-written narration for the rewritten hints and steps of gr4_numbers (see
data/bank-import/g4/RENARRATE-BRIEF.md). None means: use the rules for that line."""

N = None

HAND = {
    "PYQ_2017_Q02": {
        "hints": [N, "To make M N minus N M as large as possible, make M as big as you can and N as small as you can. Read the rules carefully: neither digit may be zero."],
        "steps": ["M N has tens digit M and units digit N, and N M is the same two digits swapped. For a large difference, M N should be big and N M should be small."],
    },
    "PYQ_2018_Q03": {
        "hints": [N, N, "Here is a similar one. Suppose p is even and q is odd, and we look at 7 p plus q. 7 p is even because p is even, and even plus odd is odd. Trying p equals 2 and q equals 3 gives 14 plus 3, which is 17, and that is odd."],
        "steps": [N, N, "In 3 m plus 4 n, and in 5 m plus 6 n, both parts are even, so the totals are even. 5 m n has the even number m as a factor, so it is even too."],
    },
}

LINES = {}
