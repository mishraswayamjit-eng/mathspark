"""Cricket stories: totals over two innings, targets to tie or win, and comparing teams."""
from imported_10_lib import ANS, ASK, B, FIG, GIVEN, L, M, N, RING, W, add, bar, bars, f, pick, table, take


# ── What must the second innings be, to tie or to win by so many? ────────────

def second(key, A, a1, a2, Bn, b1, kind, k, intro, recap):
    """kind: 'tie', 'by' (win by exactly k) or 'min' (the fewest runs that win)."""
    ta = a1 + a2
    target = ta + k
    ans = target - b1
    beats = [
        B(intro, GIVEN("q", "%s: %d and %d.   %s: %d and ?" % (A, a1, a2, Bn, b1))),
        B(pick(key, "t", ["First, %s's total. %d plus %d is %d.", "Start with %s's two innings. %d plus %d is %d."]) % (A, a1, a2, ta),
          W("ta", "%d + %d = %d" % (a1, a2, ta)), N("ta", "= %d" % ta, "%s's total" % A)),
    ]
    if kind == "tie":
        beats.append(ASK(key, "a1", "To tie the match, what must %s's total be at the end?" % Bn,
                         "%d, the same as %s" % (ta, A), ["%d, one more than %s" % (ta + 1, A), "%d, what they have now" % b1],
                         "A tie means both teams finish on exactly the same total. So %s must end on %d, no more and no less." % (Bn, ta)))
    elif kind == "by":
        beats.append(ASK(key, "a1", "%s must finish exactly %d %s ahead of %s. So what is %s's total?" % (Bn, k, "run" if k == 1 else "runs", A, Bn),
                         "%d + %d" % (ta, k), ["%d − %d" % (ta, k), "just %d" % ta],
                         "Winning by %d means finishing %d above the other team. %s has %d, so %s's total is %d plus %d." % (k, k, A, ta, Bn, ta, k)))
    else:
        beats.append(ASK(key, "a1", "To win, %s must finish above %d. What is the smallest total that does it?" % (Bn, ta),
                         "%d" % (ta + 1), ["%d" % ta, "%d + %d" % (ta, b1)],
                         "%d would only tie the match. To win, %s needs at least 1 run more than that." % (ta, Bn)))
    if k:
        beats.append(B("%d plus %d is %d. That is the total %s needs." % (ta, k, target, Bn),
                       W("tg", "%d + %d = %d" % (ta, k, target)), N("tg", "= %d" % target, "%s's target" % Bn)))
    beats += take(key, target, b1, "ans",
                  "%s already has %d from the first innings, so the second innings must bring the rest." % (Bn, b1), "answer")
    beats.append(B(pick(key, "so", ["So %s needs %d runs in the second innings.", "So the second innings for %s must be %d runs."]) % (Bn, ans),
                   RING("ans", "= %d" % ans)))
    if kind == "tie":
        beats.append(B("Careful not to answer %d. That is the whole total %s needs, and %d of it is already on the scoreboard." % (ta, Bn, b1)))
        beats.append(B("Check: %d plus %d is %d, level with %s. A tie." % (b1, ans, ta, A),
                       W("c", "%d + %d = %d" % (b1, ans, ta))))
    elif k == 1:
        beats.append(B("Careful: %d runs would only bring the scores level, and that is a tie. The 1 extra run is what makes it a win." % (ta - b1),
                       W("tie", "%d − %d = %d" % (ta, b1, ta - b1)), N("tie", "= %d" % (ta - b1), "only a tie")))
        beats.append(B("Check: %d plus %d is %d, which is 1 more than %d." % (b1, ans, target, ta),
                       W("c", "%d + %d = %d" % (b1, ans, target))))
    else:
        beats.append(B("The trap is to forget the %d. Reaching %d only ties the match. The %d extra runs are what make the win." % (k, ta, k)))
        beats.append(B("Check: %d plus %d is %d, and %d is %d more than %d." % (b1, ans, target, target, k, ta),
                       W("c", "%d + %d = %d" % (b1, ans, target)), W("c2", "%d − %d = %d" % (target, ta, k))))
    beats.append(B(recap))
    add(key, *beats)


second("28ada5d8", "Team A", 247, 189, "Team B", 312, "tie", 0,
       "Team A scored 247 runs and then 189 runs. Team B scored 312 in the first innings. How many must Team B score in the second innings to tie the match?",
       "So for a tie: find the other team's total, then subtract what you already have.")
second("9fcdcd29", "Team India", 247, 189, "Team Australia", 312, "tie", 0,
       "Team India scored 247 and 189 in their two innings. Team Australia scored 312 in their first. How many runs does Team Australia need in the second innings to tie?",
       "So a target question has two steps: build the total to be matched, then take away the runs already scored.")
second("33da2932", "Team A", 287, 194, "Team B", 315, "by", 38,
       "Team A scored 287 and 194. Team B scored 315 in the first innings, and won the match by exactly 38 runs. How many did Team B score in the second innings?",
       "So for a win by so many runs: the other team's total, plus the winning gap, minus the runs already scored.")
second("3a43f7d1", "Team A", 247, 183, "Team B", 198, "by", 15,
       "Team A scored 247 and 183. Team B scored 198 in the first innings, and must win by exactly 15 runs. How many must Team B score in the second innings?",
       "So build the target first: the other team's total plus the gap. Then subtract what is already scored.")
second("b2bc5126", "Team A", 247, 189, "Team B", 315, "by", 1,
       "Team A scored 247 and 189. Team B scored 315 in the first innings. How many runs does Team B need in the second innings to beat Team A by exactly 1 run?",
       "So to win by 1: the other team's total, plus 1, minus the runs you already have.")
second("bc224c31", "Team A", 247, 189, "Team B", 312, "min", 1,
       "Team A scored 247 and 189. Team B scored 312 in the first innings. What is the smallest number of runs Team B can score in the second innings and still win?",
       "So the smallest winning total is 1 more than the other team's total. Then take away the runs already scored.")


# ── Which team won, and by how many? ─────────────────────────────────────────

def compare(key, a1, a2, b1, b2, intro, recap):
    ta, tb = a1 + a2, b1 + b2
    sub = take(key, ta, tb, "ans", "%d is more than %d, so Team A wins. By how many?" % (ta, tb), "answer")
    add(key,
        B(intro, GIVEN("q", "Team A: %d and %d.   Team B: %d and %d." % (a1, a2, b1, b2)),
          FIG("t", table(["Team", "1st innings", "2nd innings"], [["A", str(a1), str(a2)], ["B", str(b1), str(b2)]]))),
        ASK(key, "a1", "Team A scored more in the first innings, and Team B scored more in the second. Can we name the winner yet?",
            "No: add each team's two innings", ["Yes: Team A, it has the top score", "Yes: Team B, it won the last innings"],
            "A match is decided by the runs over both innings together. One good innings is not enough, so add up each team's two scores."),
        B("Team A first. %d plus %d is %d." % (a1, a2, ta),
          W("ta", "%d + %d = %d" % (a1, a2, ta)), N("ta", "= %d" % ta, "Team A")),
        B("Now Team B. %d plus %d is %d." % (b1, b2, tb),
          W("tb", "%d + %d = %d" % (b1, b2, tb)), N("tb", "= %d" % tb, "Team B")),
        sub[0],
        B("So Team A won by %d runs." % (ta - tb), RING("ans", "= %d" % (ta - tb))),
        B("Careful: comparing just one innings gives a different gap. Only the totals decide a match."),
        B("Check by adding on. Team B's %d plus %d is %d, which is Team A's total." % (tb, ta - tb, ta),
          W("c", "%d + %d = %d" % (tb, ta - tb, ta))),
        B(recap),
        )


compare("9a6b3e78", 248, 176, 195, 213,
        "Team A scored 248 and 176 in its two innings. Team B scored 195 and 213. We want to know by how many runs the winning team won.",
        "So to find a winning margin: total each team, see which is bigger, and subtract the smaller from it.")
compare("d529fc5b", 247, 189, 198, 215,
        "Team A scored 247 and 189. Team B scored 198 and 215. The team with the higher total wins, and we want to know by how many runs.",
        "So add each team's innings first. The margin is the bigger total minus the smaller one.")

# ── Team Rajasthan's missing Day 3 score ─────────────────────────────────────

Q = "1b46a3a2"
sub = take(Q, 708, 445, "ans", "So Day 3 is whatever is still missing from 708.", "answer")
add(Q,
    B("Here is the scorecard for 3 days. Rajasthan's Day 3 score is missing. But we know that over all 3 days, Rajasthan scored exactly 50 runs more than their opponents.",
      GIVEN("q", "Rajasthan's total = opponents' total + 50"),
      FIG("t", table(["Day", "Rajasthan", "Opponents"], [["1", "247", "189"], ["2", "198", "256"], ["3", "?", "213"]]))),
    B("The opponents' column is complete, so start there. 189 plus 256 is 445, and 213 more makes 658.",
      W("o1", "189 + 256 = 445"), W("o2", "445 + 213 = 658"), N("o2", "= 658", "opponents' total")),
    ASK(Q, "a1", "Rajasthan finished 50 runs ahead of the opponents. So what is Rajasthan's total for the 3 days?",
        "658 + 50", ["658 − 50", "just 658"],
        "Ahead means more. Rajasthan's total is 50 runs bigger than the opponents' 658, so we add the 50."),
    B("658 plus 50 is 708. That is what Rajasthan's 3 days must add up to.",
      W("r", "658 + 50 = 708"), N("r", "= 708", "Rajasthan's total")),
    B("We know 2 of Rajasthan's days. 247 plus 198 is 445.",
      W("k", "247 + 198 = 445"), N("k", "= 445", "Days 1 and 2")),
    sub[0],
    B("Rajasthan scored 263 runs on Day 3.", RING("ans", "= 263")),
    B("Here is a lovely check. After 2 days both sides had 445, dead level. So on Day 3 Rajasthan had to beat the opponents' 213 by exactly 50, and 213 plus 50 is 263.",
      W("c", "213 + 50 = 263")),
    B("So when one score is missing, finish the complete column first, use the clue to get the other total, and subtract what you already know."),
    )

# ── Four teams: the top two totals ───────────────────────────────────────────

Q = "228c971f"
add(Q,
    B("4 teams each played 3 matches. The 2 teams with the highest total runs go to the finals, and we want those 2 totals added together.",
      GIVEN("q", "Top 2 teams by total runs. Their totals added = ?"),
      FIG("t", table(["Team", "Match 1", "Match 2", "Match 3"],
                     [["A", "247", "183", "312"], ["B", "198", "276", "159"], ["C", "305", "144", "268"], ["D", "172", "289", "231"]]))),
    B("We cannot pick the top 2 by looking, so total every team. Team A: 247 plus 183 is 430, and 312 more makes 742.",
      W("a1", "247 + 183 = 430"), W("a2", "430 + 312 = 742"), N("a2", "= 742", "Team A")),
    B("Team B: 198 plus 276 is 474, and 159 more makes 633.",
      W("b1", "198 + 276 = 474"), W("b2", "474 + 159 = 633"), N("b2", "= 633", "Team B")),
    B("Team C: 305 plus 144 is 449, and 268 more makes 717.",
      W("c1", "305 + 144 = 449"), W("c2", "449 + 268 = 717"), N("c2", "= 717", "Team C")),
    B("Team D: 172 plus 289 is 461, and 231 more makes 692.",
      W("d1", "172 + 289 = 461"), W("d2", "461 + 231 = 692"), N("d2", "= 692", "Team D")),
    ASK(Q, "a1", "The totals are 742, 633, 717 and 692. Which 2 teams go to the finals?",
        "A and C", ["A and D", "C and D", "A and B"],
        "Put the totals in order, biggest first: 742, 717, 692, 633. The 2 biggest belong to Team A and Team C."),
    B("So Team A and Team C qualify. 742 plus 717 is 1459.",
      M("a2", "= 742", "box"), M("c2", "= 717", "box"), ANS("ans", "742 + 717 = 1,459"), RING("ans", "1,459")),
    B("Careful with Team D. Its 692 is close behind Team C's 717, so it is an easy one to mix up. Always put the totals in order before choosing."),
    B("Check by taking one away. 1459 minus 742 leaves 717, which is Team C's total.",
      W("ch", "1,459 − 742 = 717")),
    B("So when a question says top 2 by total: total everyone, put the totals in order, and only then add the 2 biggest."),
    )

# ── Teams A, B and C: more than, fewer than ──────────────────────────────────

Q = "ce3e7583"
sub = take(Q, 7461, 3210, "ans", "Team C scored 3210 fewer than that. Fewer means take away.", "answer")
add(Q,
    B("Team A scored 2748 runs. Team B scored 1965 runs more than Team A. Team C scored 3210 runs fewer than Team A and Team B put together. We want Team C's runs.",
      GIVEN("q", "A = 2,748.   B = A + 1,965.   C = (A + B) − 3,210.")),
    ASK(Q, "a1", "Team B scored 1965 runs more than Team A. So how many runs did Team B score?",
        "2748 + 1965", ["just 1965", "2748 − 1965"],
        "1965 is not Team B's score. It is how far ahead of Team A they finished. So start from Team A's 2748 and add 1965."),
    B("2748 plus 1965 is 4713. That is Team B's score. Look at the bars: Team B's bar is Team A's bar with 1965 more on the end.",
      W("b", "2,748 + 1,965 = 4,713"), N("b", "= 4,713", "Team B"),
      FIG("bars", bars(bar([(5.5, "2,748", "a")], None, "A"), bar([(5.5, "2,748", "a"), (3.9, "1,965 more", "b")], None, "B")))),
    ASK(Q, "a2", "Next we need Team A and Team B combined. Which sum is that?",
        "2748 + 4713", ["2748 + 1965", "just 4713"],
        "Combined means both whole scores together. Team A's score is 2748 and Team B's whole score is 4713, so add those two."),
    B("2748 plus 4713 is 7461. Careful: 2748 plus 1965 was only Team B's score. The combined total counts Team A's runs as well.",
      W("ab", "2,748 + 4,713 = 7,461"), N("ab", "= 7,461", "A and B together")),
    sub[0],
    B("So Team C scored 4251 runs.", RING("ans", "= 4,251")),
    B("Check by adding back. 4251 plus 3210 is 7461, the combined score of Team A and Team B.",
      W("c", "4,251 + 3,210 = 7,461")),
    B("So take a chain of clues one link at a time. More than means add, fewer than means subtract, and each answer feeds the next step."),
    )
