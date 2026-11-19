"""Percentage lessons for part 03, written one by one (second half)."""
from authored_03_lib import ANSC, ANSL, B, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, P, UL, W  # noqa: F401

LESSONS = {}

# 40% girls; 30% of girls and 50% of boys wear glasses.
LESSONS[P + "PERCENTAGE_009"] = LESSON(
    B("In a class, 40 percent of the children are girls and the rest are boys. 30 percent of the girls and 50 percent of the boys wear glasses. What percent of the whole class wears glasses?",
      GIVEN("q", "40% are girls, the rest are boys."), GIVEN("q2", "30% of the girls and 50% of the boys wear glasses.")),
    B("Each percent here is of a different group. So adding 30 and 50, or taking the number halfway between them, will not work. Let's picture real children.",
      UL("q2", "of the girls"), UL("q2", "of the boys")),
    B("Imagine a class of exactly 100 children. Then 40 percent girls means 40 girls.",
      LB("l1", "Class of 100: 40 girls")),
    B("And how many boys are there?",
      ask=CHOOSE(["40", "60", "50"], 1,
                 "The rest of the class are boys. Take the 40 girls away from the 100 children.")),
    B("100 minus 40 is 60 boys.",
      W("l2", "100 − 40 = 60"), NOTE("l2", "60", "boys")),
    B("Girls with glasses: 30 percent of the 40 girls. 10 percent of 40 is 4, so 30 percent is 12 girls.",
      W("l3", "30% of 40 = 12")),
    B("Boys with glasses: 50 percent of the 60 boys. How many is that?",
      ask=CHOOSE(["50", "30", "60"], 1,
                 "50 percent means half. And it is half of the boys, who number 60, not half of the whole class.")),
    B("Half of 60 is 30 boys.",
      W("l4", "50% of 60 = 30")),
    B("Altogether, 12 plus 30 is 42 children with glasses, out of 100. That is 42 percent of the class.",
      W("l5", "12 + 30 = 42"), *ANSC("l6", "42/100 = 42%", "42%")),
    B("Notice that 42 is nearer to 50 than to 30. There are more boys than girls, so the boys' percent pulls harder."),
    B("So when percents are of different groups, picture 100 people, count each group, and add up the real numbers."),
)

# 40 children, 30% girls; boys leave; now 40% girls.
LESSONS[P + "PERCENTAGE_010"] = LESSON(
    B("A class has 40 children, and 30 percent of them are girls. Some boys move to another class, and no girls leave. Now 40 percent of the class are girls. How many boys moved?",
      GIVEN("q", "40 children, 30% girls. Some boys leave. Now 40% girls.")),
    B("First, how many girls are there? 10 percent of 40 is 4, so 30 percent is 12 girls.",
      W("l1", "30% of 40 = 12"), NOTE("l1", "12", "girls")),
    B("Some boys move away, but no girls do. So there are still 12 girls. Hold on to that number: it is the one thing that does not change."),
    B("After the boys move, the girls are 40 percent. That is 40 percent of what?",
      ask=CHOOSE(["of the old class of 40", "of the new, smaller class", "of the boys"], 1,
                 "The new percent describes the class as it is now, after the boys have gone. So it is 40 percent of the new, smaller class.")),
    B("That is the trap. 40 percent of the old class would be 16 girls, but there are only 12. The percent went up because the class got smaller.",
      W("l2", "40% of 40 = 16")),
    B("So 12 girls are 40 percent of the new class. Divide by 4: 10 percent of the new class is 3 children.",
      W("l3", "12 ÷ 4 = 3"), NOTE("l3", "3", "10% of new class")),
    B("10 percent is 3 children, so the whole new class is 3 times 10, which is 30 children.",
      W("l4", "3 × 10 = 30")),
    B("The class shrank from 40 children to 30. 40 minus 30 is 10, so 10 boys moved.",
      *ANSC("l5", "40 − 30 = 10", 10)),
    B("Check: are 12 girls really 40 percent of 30 children? 10 percent of 30 is 3, so 40 percent is 12. Yes.",
      W("l6", "40% of 30 = 12")),
    B("So when a percent changes, find the thing that stayed the same, and use it to work out the new whole."),
)

# Each side of a square 50% longer: area increase.
LESSONS[P + "PERCENTAGE_011"] = LESSON(
    B("Each side of a square playground is made 50 percent longer. By what percent does the area of the playground increase?",
      GIVEN("q", "Each side of a square is made 50% longer."), GIVEN("q2", "Area increases by what percent?")),
    B("Before we work it out: the side grows by 50 percent. Does the area grow by 50 percent too?",
      ask=CHOOSE(["yes, by 50%", "no, by more than 50%", "no, by less than 50%"], 1,
                 "Area is side times side, so the longer side gets used twice. Let's try a real square and see how big the change is.")),
    B("No size is given, so choose an easy one. Take a side of 10 metres. The area is 10 times 10, which is 100 square metres.",
      W("l1", "10 × 10 = 100")),
    B("Now make the side 50 percent longer. Half of 10 is 5, so the new side is 15 metres.",
      W("l2", "10 + 5 = 15")),
    B("The new area is 15 times 15, which is 225 square metres.",
      W("l3", "15 × 15 = 225")),
    B("The area went from 100 to 225. What is the increase?",
      ask=CHOOSE(["225", "125", "50"], 1,
                 "The increase is only the extra part, the amount above what we started with. Take the old area away from the new area.")),
    B("225 minus 100 is 125 square metres more. And 125 more, on a start of 100, is an increase of 125 percent.",
      W("l4", "225 − 100 = 125"), *ANSC("l5", "125/100 = 125%", "125%")),
    B("Two traps here. 225 percent is the new area compared with the old one, not the increase. And 50 percent for each side, added up, is too small: the two increases multiply."),
    B("So when a side grows, the area grows by more, because area uses the side twice. Try an easy side like 10 and see. Here the area grows by 125 percent."),
)

# Rs 6,000 at 5% simple interest for 18 months: total.
LESSONS[P + "PERCENTAGE_012"] = LESSON(
    B("Rohan's mother puts 6000 rupees in a bank that pays simple interest of 5 percent per year. How much will she have in all after 18 months?",
      GIVEN("q", "₹6,000 at 5% simple interest per year."), GIVEN("q2", "How much in all after 18 months?")),
    B("The bank pays 5 percent for each whole year. So first find one year's interest. 1 percent of 6000 is 60, so 5 percent is 300 rupees.",
      W("l0", "1% of 6,000 = 60"), W("l1", "5% of 6,000 = 300"), NOTE("l1", "300", "for 1 year")),
    B("The time is 18 months, but the rate is for a year. How long is 18 months, in years?",
      LB("l2", "1 year = 12 months"),
      ask=CHOOSE(["18 years", "1 and a half years", "2 years"], 1,
                 "A year has 12 months. 18 months is 12 months and 6 more, and 6 months is half a year.")),
    B("18 months is 12 months plus 6 months: one and a half years. Using 18 as if it were years is the first trap.",
      W("l3", "12 + 6 = 18")),
    B("One year gives 300 rupees. Half a year gives half of that, 150 rupees. So the interest is 300 plus 150, which is 450 rupees.",
      W("l4", "300 ÷ 2 = 150"), W("l5", "300 + 150 = 450")),
    B("Is 450 rupees the answer to the question?",
      UL("q2", "in all"),
      ask=CHOOSE(["yes, 450", "no, add the 6,000 she put in"], 1,
                 "Read the question again. It asks how much she will have in all. That is her own 6000 rupees together with the interest.")),
    B("She still has the money she put in, and the interest on top. 6000 plus 450 is 6450 rupees.",
      *ANSC("l6", "6,000 + 450 = 6,450", "6,450")),
    B("So with simple interest: find one year's interest, scale it to the time in years, and check whether the question wants the interest or the total."),
)

# Winner got 60% and won by 240 votes.
LESSONS[P + "PERCENTAGE_013"] = LESSON(
    B("In a school election there were only two candidates, and every vote went to one of them. The winner got 60 percent of the votes and won by 240 votes. How many votes were cast in all?",
      GIVEN("q", "Two candidates. Winner: 60% of the votes, won by 240 votes.")),
    B("The winner got 60 percent, and every vote went to one of the two. What percent did the other candidate get?",
      ask=CHOOSE(["40%", "60%", "30%"], 0,
                 "All the votes together are the whole. If the winner took 60 percent of them, the rest went to the other candidate.")),
    B("100 minus 60 is 40. The other candidate got 40 percent of the votes.",
      W("l1", "100% − 60% = 40%")),
    B("Now, won by 240 means the gap between the two candidates. It is not the winner's votes, and it is not the other candidate's votes. That is the trap.",
      UL("q", "won by 240 votes")),
    B("What is that gap, as a percent of all the votes?",
      ask=CHOOSE(["60%", "20%", "40%"], 1,
                 "The gap is how far apart the two candidates are. One has 60 percent and the other has 40 percent, so take one from the other.")),
    B("60 minus 40 is 20. The lead is 20 percent of the votes, and we know the lead is 240 votes.",
      W("l2", "60% − 40% = 20%"), LB("l3", "20% of the votes = 240")),
    B("20 percent is one fifth. So all the votes are 5 times 240, which is 1200.",
      *ANSC("l4", "240 × 5 = 1,200", "1,200")),
    B("Check. 60 percent of 1200 is 720, and 40 percent is 480. And 720 minus 480 is 240, the winning gap.",
      W("l5", "60% of 1,200 = 720"), W("l6", "40% of 1,200 = 480"), W("l7", "720 − 480 = 240")),
    B("So when someone wins by a number of votes, that number is the gap. Find the gap as a percent, then scale up to the whole."),
)

# Exactly 35% are girls: smallest class.
LESSONS[P + "PERCENTAGE_014"] = LESSON(
    B("Exactly 35 percent of the children in a class are girls. What is the smallest number of children the class could have?",
      GIVEN("q", "Exactly 35% of a class are girls. Smallest class?")),
    B("35 percent means 35 out of every 100. So a class of 100 with 35 girls would fit. But could a smaller class fit too?",
      W("l1", "35% = 35/100")),
    B("The catch is that the number of girls must be a whole number. You cannot have half a girl! So let's make the fraction 35 out of 100 as simple as it can be."),
    B("Which number divides both 35 and 100 exactly?",
      ask=CHOOSE(["2", "5", "7"], 1,
                 "35 ends in 5 and 100 ends in 0. Any number that ends in 5 or 0 can be divided by 5.")),
    B("35 divided by 5 is 7, and 100 divided by 5 is 20. So 35 out of 100 is the same as 7 out of 20.",
      W("l2", "35 ÷ 5 = 7"), W("l3", "100 ÷ 5 = 20"), W("l4", "35/100 = 7/20")),
    B("7 and 20 share no other factor, so the fraction cannot get any simpler. The girls are 7 out of every 20 children."),
    B("So the smallest class has 20 children, with 7 girls.",
      *ANSL("l5", "Smallest class: 20 children, 7 girls", "20 children")),
    B("Check: multiply 7 and 20 both by 5, and you are back at 35 out of 100, which is 35 percent.",
      W("l6", "7 × 5 = 35"), W("l7", "20 × 5 = 100")),
    B("So for the smallest group that fits a percent: write the percent as a fraction, simplify it fully, and read the bottom number. Here that is 20."),
)

# Buy 4, get 1 free: the real percent discount.
LESSONS[P + "PERCENTAGE_015"] = LESSON(
    B("A shop says: buy 4, get 1 more free. Riya takes 5 notebooks of the same price and pays for 4. What percent discount is she really getting on the 5 notebooks?",
      GIVEN("q", "Buy 4, get 1 more free. Takes 5, pays for 4. Discount?")),
    B("No price is given, so choose an easy one. Say each notebook costs 10 rupees."),
    B("Riya takes home 5 notebooks. At full price they are worth 5 times 10, which is 50 rupees.",
      W("l1", "5 × 10 = 50"), NOTE("l1", "50", "full price")),
    B("She pays for 4, which is 40 rupees. So she saves 10 rupees.",
      W("l2", "4 × 10 = 40"), W("l3", "50 − 40 = 10")),
    B("A discount is a saving compared with a price. Which price do we compare her 10 rupees with?",
      ask=CHOOSE(["the 40 rupees she pays", "the full price, 50 rupees"], 1,
                 "A discount is always measured against the full price of everything you take home. Riya takes home 5 notebooks, worth 50 rupees.")),
    B("10 out of 50 is one fifth, because 50 divided by 10 is 5.",
      W("l4", "50 ÷ 10 = 5")),
    B("And one fifth is 20 percent. The discount is 20 percent.",
      *ANSC("l5", "10/50 = 20%", "20%")),
    B("The trap is 25 percent. That compares the 10 rupees saved with the 40 rupees she pays. But a discount is measured on the full 50 rupees.",
      W("l6", "10/40 = 25%")),
    B("So for any offer: find the full price of all you take home, find what you save, and compare the saving with the full price. Here it is 20 percent."),
)
