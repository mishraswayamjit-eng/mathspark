"""Textbook questions in batch 12 that share a structure: one builder each, fed the question's numbers."""
from imported_12_lib import A, AL, B, CH, CIRC, E, G, GM, LB, LESSON, MINUS, NOTE, STRIKE, UL, W, n, shuffled, split_times  # noqa: F401

T = "IPMTB_grade5_ch06_"

LESSONS = {}


# ── "Multiply / divide the sum of a and b by their difference" ──────────────

def sumdiff_head(a, b, job, given):
    s, d = a + b, a - b
    return [
        B("This sentence packs three jobs into one: a sum, a difference, and then a %s. Let's unpack it." % job,
          G("q", given)),
        B("Sum means add. What does difference mean here?",
          ask=CH(["%d + %d" % (a, b), "%d − %d" % (a, b), "%d ÷ %d" % (a, b)], 1,
                 "The difference between two numbers is how far apart they are. We find it by taking the smaller from the larger.")),
        B("First the sum. %d plus %d is %d." % (a, b, s), E("s", "%d + %d" % (a, b)), UL("s", str(s))),
        B("Now the difference. %d minus %d is %d." % (a, b, d), E("d", "%d − %d" % (a, b)), UL("d", str(d))),
    ]


LESSONS[T + "q004"] = LESSON(
    sumdiff_head(325, 315, "multiply", "(sum of 325 and 315) × (their difference)"),
    B("Now multiply the sum by the difference: 640 times 10. To multiply by 10, write a zero on the end. That gives 6400.",
      A("p", "640 × 10")),
    B("Careful: 640 and 10 are both among the choices. They are only the two ingredients. The question asks for their product."),
    B("Check by dividing back. 6400 divided by 10 is 640, our sum.", E("k", "6400 ÷ 10")),
    B("So read the sentence in pieces: find the sum, find the difference, then multiply the two."),
)

LESSONS[T + "q037"] = LESSON(
    sumdiff_head(470, 245, "multiply", "(sum of 470 and 245) × (their difference)"),
    B("Now multiply the sum by the difference: 715 times 225. Split 225 into 200, 20 and 5.",
      W("sp", "715 × 225 = 715 × 200 + 715 × 20 + 715 × 5"), UL("sp", "200")),
    B("715 times 200 is 1,43,000. 715 times 20 is 14,300. And 715 times 5 is 3575.",
      E("m1", "715 × 200"), E("m2", "715 × 20"), E("m3", "715 × 5")),
    B("Add them up. 1,43,000 plus 14,300 is 1,57,300, and 3575 more makes 1,60,875.",
      E("t1", "1,43,000 + 14,300"), A("t", "1,57,300 + 3575")),
    B("The choices all end in the same three digits, so the ending cannot help us. A rough check can: 700 times 225 is 1,57,500, and 715 is a little more than 700. So 1,60,875 fits.",
      E("k", "700 × 225")),
    B("So read the sentence in pieces: find the sum, find the difference, then multiply the two, one piece at a time."),
)

LESSONS[T + "q005"] = LESSON(
    sumdiff_head(535, 525, "divide", "(sum of 535 and 525) ÷ (their difference)"),
    B("Now divide the sum by the difference: 1060 divided by 10. Dividing by 10 takes the zero off the end. That leaves 106.",
      A("p", "1060 ÷ 10")),
    B("Careful: 1060 and 10 are both among the choices. They are only the two ingredients. The question asks for one divided by the other."),
    B("Check by multiplying back. 106 times 10 is 1060, our sum.", E("k", "106 × 10")),
    B("So read the sentence in pieces: find the sum, find the difference, then divide the first by the second."),
)

LESSONS[T + "q038"] = LESSON(
    sumdiff_head(580, 420, "divide", "(sum of 580 and 420) ÷ (their difference)"),
    B("Now divide the sum by the difference: 1000 divided by 160. 6 lots of 160 make 960, and that leaves 40.",
      E("p1", "160 × 6"), E("p2", "1000 − 960")),
    B("That 40 still has to be shared into 160. What part of 160 is 40?",
      ask=CH(["one half", "one quarter", "one sixth"], 1,
             "4 lots of 40 make 160. So 40 is one of 4 equal parts of 160, and that is one quarter.")),
    B("40 out of 160 is one quarter, and one quarter as a decimal is 0.25. So the answer is 6 and a quarter: 6.25.",
      W("p3", "40/160 = 1/4"), W("p4", "1/4 = 0.25"), A("p", "1000 ÷ 160")),
    B("Careful not to stop at 6 just because the division does not come out evenly. The 40 left over becomes the decimal part."),
    B("Check: 160 times 6 is 960, and a quarter of 160 is 40. 960 plus 40 is 1000, our sum.", E("k", "960 + 40")),
    B("So find the sum, find the difference, then divide. If something is left over, carry on into decimals."),
)


# ── "If a × b = p, then (a with a zero) × (b with two zeros) = ?" ───────────

def zeros(a, b):
    p = a * b
    big_a, big_b = a * 10, b * 100
    h = big_a - 50
    return LESSON(
        B("We are handed a fact: %d times %d is %d. The new sum has the same digits with some zeros on the end, so we should not have to start again." % (a, b, p),
          GM("q", "%d × %d = %d" % (a, b, p)), W("q2", "%d × %d = ?" % (big_a, big_b), "given")),
        B("Look at %d. It is %d with one zero on the end, so it is %d times 10." % (big_a, a, a),
          UL("q2", str(big_a)), W("l1", "%d = %d × 10" % (big_a, a))),
        B("And %d is %d times what?" % (big_b, b),
          ask=CH(["10", "100", "1000"], 1,
                 "%d has two zeros after the %d. Two zeros means times 100." % (big_b, b))),
        B("%d is %d times 100." % (big_b, b),
          UL("q2", str(big_b)), W("l2", "%d = %d × 100" % (big_b, b))),
        B("So the new sum is the old one, times 10, and times 100. And we already know that %d times %d is %d." % (a, b, p),
          W("l3", "%d × %d = %d × %d × 10 × 100" % (big_a, big_b, a, b)),
          UL("l3", "%d × %d" % (a, b)), NOTE("l3", "%d × %d" % (a, b), str(p))),
        B("10 times 100 is 1000. So we need %d times 1000." % p, E("l4", "10 × 100")),
        B("To multiply by 1000, write three zeros after %d. That gives %s." % (p, n(p * 1000)),
          A("l5", "%d × 1000" % p)),
        B("The choices differ only in their zeros, so count them: one zero from the first number and two from the second. Three zeros in all."),
        B("Check the long way. %d times %d is %s, and 50 times %d is %s. Together that is %s." % (
            h, big_b, n(h * big_b), big_b, n(50 * big_b), n(p * 1000)),
          E("k1", "%d × %d" % (h, big_b)), E("k2", "50 × %d" % big_b),
          E("k3", "%s + %s" % (n(h * big_b), n(50 * big_b)))),
        B("So when zeros are added to a fact you know, keep the fact and put the zeros back at the end."),
    )


LESSONS[T + "q012"] = zeros(15, 16)
LESSONS[T + "q030"] = zeros(25, 26)


# ── "The continued product of three numbers is P; two of them are a and b" ──

def third(qid, a, b, product):
    ab = a * b
    assert ab * 25 == product
    tens, ones = b // 10 * 10, b % 10
    rem = product - ab * 20
    assert rem == ab * 5
    choices, at = shuffled(qid, "ask", "%s ÷ (%d × %d)" % (n(product), a, b),
                           ["%s − %d − %d" % (n(product), a, b), "%s × %d × %d" % (n(product), a, b)])
    return LESSON(
        B("Continued product just means the numbers multiplied one after another. Three numbers multiply to make %s, and we know two of them: %d and %d." % (n(product), a, b),
          W("q", "%d × %d × ? = %s" % (a, b, n(product)), "given"), CIRC("q", "?")),
        B("How can we find the missing number?",
          ask=CH(choices, at,
                 "The three numbers were multiplied together, and divide undoes multiply. So we divide the product by the two numbers we know.")),
        B("First multiply the two we know. %d times %d is %d, %d times %d is %d, and together that is %d." % (
            a, tens, a * tens, a, ones, a * ones, ab),
          E("m1", "%d × %d" % (a, tens)), E("m2", "%d × %d" % (a, ones)), E("m", "%d × %d" % (a, b))),
        B("So %d times the missing number is %s. We need to know how many lots of %d fit into %s." % (ab, n(product), ab, n(product)),
          W("l", "%d × ? = %s" % (ab, n(product)))),
        B("Build up in easy steps. 10 lots of %d is %s, so 20 lots is %s." % (ab, n(ab * 10), n(ab * 20)),
          E("b1", "%d × 10" % ab), E("b2", "%d × 20" % ab)),
        B("Take that away from %s, and %s is still left." % (n(product), n(rem)),
          E("b3", "%s − %s" % (n(product), n(ab * 20)))),
        B("Look at the board. How many lots of %d make %s?" % (ab, n(rem)),
          ask=CH(["10 lots", "5 lots", "2 lots"], 1,
                 "10 lots made %s, and %s is exactly half of that. Half of 10 lots is 5 lots." % (n(ab * 10), n(rem)))),
        B("5 lots of %d is %s. So we have 20 lots and 5 lots: the missing number is 25." % (ab, n(rem)),
          E("b4", "%d × 5" % ab), A("ans", "20 + 5")),
        B("Careful not to divide by just one of the known numbers. Both of them have to come out of the product."),
        B("Check by multiplying all three. %d times %d times 25 does come back to %s." % (a, b, n(product)),
          W("k", "%d × %d × 25 = %s" % (a, b, n(product)))),
        B("So for a missing number in a product: multiply the ones you know, then divide the product by that."),
    )


LESSONS[T + "q014"] = third(T + "q014", 16, 34, 13600)
LESSONS[T + "q032"] = third(T + "q032", 13, 14, 4550)


# ── "Product of the greatest 3-digit number and the smallest k-digit number" ─

def greatest_smallest(digits, slips):
    small = 10 ** (digits - 1)
    zeros_word = {2: "two", 4: "four"}[digits - 1]
    return LESSON(
        B("This question does not hand us the numbers. It describes them, so our first job is to work out which two numbers it means.",
          G("q", "greatest 3-digit number × smallest %d-digit number" % digits)),
        B("The greatest number with 3 digits has the biggest digit, 9, in every place. That is 999.",
          LB("g", "Greatest 3-digit number = 999"), UL("g", "999")),
        B("And what is the smallest number with %d digits?" % digits,
          ask=CH([slips[0], n(small), slips[1]], 1,
                 "The smallest number with %d digits is a 1 followed by zeros. It needs the 1 because a number cannot begin with zero, and zeros are the smallest digits there are." % digits)),
        B("So the smallest is %s: a 1 and then %s zeros." % (n(small), zeros_word),
          LB("s", "Smallest %d-digit number = %s" % (digits, n(small))), UL("s", n(small))),
        B("Product means multiply. To multiply 999 by %s, write 999 and then %s zeros. That gives %s." % (n(small), zeros_word, n(999 * small)),
          A("p", "999 × %s" % n(small))),
        B("The choices differ only in how many nines and zeros they have. So count: three nines, then exactly %s zeros." % zeros_word),
        B("Check another way. 999 is 1 less than 1000. 1000 times %s is %s, and taking one lot of %s away leaves %s." % (
            n(small), n(1000 * small), n(small), n(999 * small)),
          E("k1", "1000 × %s" % n(small)), E("k2", "%s − %s" % (n(1000 * small), n(small)))),
        B("So turn the words into numbers first. Then multiplying by a 1 with zeros just means writing those zeros on the end."),
    )


LESSONS[T + "q017"] = greatest_smallest(3, ["111", "101"])
LESSONS[T + "q041"] = greatest_smallest(5, ["11,111", "1000"])


# ── "A number divided by d gives quotient q and remainder r. Find the number." ─

def dividend(qid, d, q, r, intro):
    full = d * q
    number = full + r
    choices, at = shuffled(qid, "ask", "%d × %d + %d" % (d, q, r),
                           ["%d × %d − %d" % (d, q, r), "%d + %d + %d" % (d, q, r)])
    return LESSON(
        B(intro, G("q", "? ÷ %d = %d, remainder %d" % (d, q, r)), CIRC("q", "?")),
        B("Picture it as sharing. The number was put into groups of %d. That made %d full groups, and %d were left over." % (d, q, r),
          NOTE("q", "remainder %d" % r, "left over")),
        B("Which sum rebuilds the number?",
          ask=CH(choices, at,
                 "The number is the %d full groups of %d, together with the %d that were left over. Left over means still there, so we add it on." % (q, d, r))),
        B("Here is the rule in words. It works for every division.",
          LB("f", "Number = divisor × quotient + remainder")),
        B("%d groups of %d make %d." % (q, d, full), E("m", "%d × %d" % (d, q)), UL("m", str(full))),
        B("Now add the %d left over. %d plus %d is %d." % (r, full, r, number), A("ans", "%d + %d" % (full, r))),
        B("Careful: %d on its own would divide by %d with nothing left. The remainder has to be added back." % (full, d)),
        B("Check by dividing. %d lots of %d use up %d of the %d. And %d minus %d leaves %d, just as the question said." % (
            q, d, full, number, number, full, r),
          E("k", "%d − %d" % (number, full))),
        B("So to find the number that was divided: divisor times quotient, plus the remainder."),
    )


LESSONS[T + "q022"] = dividend(T + "q022", 15, 6, 13,
                               "A student divided a number by 15. The quotient was 6 and the remainder was 13. The number itself is hidden, and we are going to rebuild it.")
LESSONS[T + "q035"] = dividend(T + "q035", 15, 6, 14,
                               "Somebody divided a number by 15 and got 6, with 14 left over. We have the pieces, so let's put the number back together.")


# ── "So much a month. How much in one and a half years?" ────────────────────

def year_half(rate, intro, given, ending, trap):
    return LESSON(
        B(intro, G("q", given)),
        B("The amount is for one month, but the time is in years. How many months are in one and a half years?",
          ask=CH(["12", "15", "18"], 2,
                 "One year is 12 months. Half a year is half of 12, which is 6 months. Put the two together.")),
        B("12 months and 6 months make 18 months.", E("mo", "12 + 6"), UL("mo", "18")),
        split_times(rate, 18, 20, MINUS, 2, "t",
                    "So we want %s times 18. 18 is 2 less than 20, so find %s times 20 and take off %s times 2." % (n(rate), n(rate), n(rate)),
                    end="%s minus %s is %s. %s" % (n(rate * 20), n(rate * 2), n(rate * 18), ending), final=True),
        B("Check year by year. One year gives %s, the half year gives %s, and together that is %s." % (
            n(rate * 12), n(rate * 6), n(rate * 18)),
          E("k1", "%s × 12" % n(rate)), E("k2", "%s × 6" % n(rate)), E("k3", "%s + %s" % (n(rate * 12), n(rate * 6)))),
        B(trap),
        B("So change the time into months first. Then multiply the monthly amount by the number of months."),
    )


LESSONS[T + "q008"] = year_half(
    5500, "Mr. A earns 5500 rupees every month. We want his total income for one and a half years.",
    "Rs. 5,500 a month, for one and a half years", "His income is 99,000 rupees.",
    "Careful not to stop at 12 months. That would leave out the half year, which is 6 more months of salary.")
LESSONS[T + "q024"] = year_half(
    1500, "A unit makes 1500 radios every month. We want its production for one and a half years.",
    "1500 radios a month, for one and a half years", "It makes 27,000 radios.",
    "Notice that 18,000 is among the choices. That is one year on its own, and it leaves out the half year.")
