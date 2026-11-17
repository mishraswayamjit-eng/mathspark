"""Hand-written narration: lines of the imported story problems (AIGEN_grade5_...) that the
rules in ratio_imported_rules.py do not read well.

Only the lines that need it are here. "hints" and "steps" are {index: line}; every other line of
the question is spoken by rule. A step line may include the step's maths line, as the rules do.
"""

HAND = {
    # ── chained ratios, "Name = amount", proportion written as a fraction ──
    "AIGEN_grade5_1259a4d7-be6e-4797-9ba3-7ee28eabc280": {
        "hints": {
            1: "Let Rohit's original runs be 5 k, and Virat's original runs be 3 k. Set up the equation: 5 k plus 18 equals 3 k plus 42.",
        },
        "steps": {
            0: "Let the original runs be in the ratio 5 is to 3. So Rohit's original runs are 5 k, and Virat's original runs are 3 k.",
            1: "After the next match, Rohit's total is 5 k plus 18, and Virat's total is 3 k plus 42.",
            2: "Since the new ratio is 3 is to 3, which means they are equal, we set them equal to each other.",
        },
    },
    "AIGEN_grade5_458f85a6-4041-45af-8113-9c3d024fb8d5": {
        "hints": {
            1: "Start with Kabir is to Riya, as 3 is to 5. If Kabir has 1,800 rupees, find the value of one part, by dividing 1,800 by 3.",
            2: "Here's a similar problem. If A is to B, as 2 is to 3, and B is to C, as 5 is to 8, and A is 1,000 rupees, find C. Step 1: A is 2 parts, which is 1,000 rupees. So 1 part is 500 rupees, and B is 3 times 500, which is 1,500 rupees. Step 2: B is to C, as 5 is to 8. B is 5 parts, which is 1,500 rupees. So 1 part is 300 rupees, and C is 8 times 300, which is 2,400 rupees.",
        },
        "steps": {
            0: "We know Kabir is to Riya, as 3 is to 5, and Kabir has 1,800 rupees. Let's find the value of one ratio part.",
            2: "Now use the second ratio: Riya is to Sanya, as 4 is to 7. Riya's 3,000 rupees corresponds to 4 parts.",
        },
    },
    "AIGEN_grade5_29c81b6d-a4f6-47b3-930f-76d2073ba15e": {
        "hints": {
            1: "Sameer is 5 parts in the first ratio, and 2 parts in the second. Find the L C M of 5 and 2, which is 10, and scale both ratios so that Sameer is 10 parts.",
        },
    },
    "AIGEN_grade5_c0efac63-758c-4006-99a2-c341f01b58c2": {
        "steps": {
            1: "Simplify the ratio by dividing both sides by 50. So, 250 divided by 50, is to 200 divided by 50, which gives 5 is to 4.",
        },
    },
    "AIGEN_grade5_7b8396f6-95ba-4875-9c94-37a432c8cf78": {
        "hints": {
            1: "Start by finding Lakshmi's actual amount, using the ratio Kabir is to Lakshmi, as 3 is to 5, and Kabir's 360 rupees.",
            2: "Here's a similar problem. If A is to B, as 2 is to 3, and B is to C, as 5 is to 8, and A equals 100, then B equals 100 times 3 over 2, which is 150. Now, using B is to C, as 5 is to 8, we get C equals 150 times 8 over 5, which is 240. Notice how we found B first, then used it to find C!",
        },
        "steps": {
            0: "We know Kabir is to Lakshmi, as 3 is to 5, and Kabir has 360 rupees. Let's find Lakshmi's amount first.",
            1: "Substitute Kabir equals 360 into the ratio: 360 over Lakshmi equals 3 over 5.",
            2: "Cross multiply to find Lakshmi's amount: Lakshmi equals 360 times 5, divided by 3. That is 1800 divided by 3, which equals 600.",
            3: "Now we use the second ratio: Lakshmi is to Neha, as 4 is to 7, and Lakshmi has 600 rupees.",
            4: "Cross multiply to find Neha's amount: Neha equals 600 times 7, divided by 4. That is 4200 divided by 4, which equals 1050.",
        },
    },
    "AIGEN_grade5_20edeb68-701c-4afd-b23b-86f0128cc816": {
        "hints": {
            1: "Simplify 12 is to 8, to get 3 is to 2. So for any amount split in this ratio, Priya gets 3 parts out of every 5 parts in total.",
        },
        "steps": {
            0: "Simplify the ratio of ages: Priya is to Rohan, as 12 is to 8, which is the same as 3 is to 2.",
        },
    },
    "AIGEN_grade5_c8f3a7cb-530e-4e77-9630-f3e546143d59": {
        "hints": {
            1: "Set up the proportion: red over yellow equals 3 over 5. So red over 24 equals 3 over 5. Now solve for red.",
            2: "Here's a similar problem. If blue and green paint are mixed in the ratio 2 is to 7, and you use 21 litres of green, then blue over 21 equals 2 over 7. So blue equals 2 times 21, divided by 7, which is 6 litres. Try the same method with your numbers!",
        },
        "steps": {
            1: "We know yellow paint is 24 litres. Set up the proportion to find red paint.",
            2: "Cross multiply and solve: red equals 3 times 24, divided by 5. That is 72 divided by 5, which equals 14.4 litres.",
            3: "Let's verify: 14.4 is to 24 is 14.4 divided by 24, which equals 0.6, and 3 over 5 equals 0.6. The ratio checks out! So the answer is 14.4 litres.",
        },
    },
    "AIGEN_grade5_a3734b08-6e99-4148-8d42-f99c7bd5bdb6": {
        "steps": {
            4: "Since 41 and 43 share no common factor, as both are prime, the ratio is already in simplest form.",
        },
    },
    "AIGEN_grade5_fb12d557-0838-4285-b7a6-f6b167b31fff": {
        "hints": {
            2: "Here's a similar problem. Sam buys red and blue pens in the ratio 2 is to 3. He buys 20 pens in total. Red pens cost 10 rupees each, and blue pens cost 12 rupees each. Total parts are 2 plus 3, which is 5. Each part is 20 divided by 5, which is 4. Red pens are 2 times 4, which is 8. Blue pens are 3 times 4, which is 12. The total cost is 8 times 10 rupees, plus 12 times 12 rupees. That is 80 rupees plus 144 rupees, which equals 224 rupees.",
        },
    },
    # ── BODMAS stories ──
    "AIGEN_grade5_82f232bb-eec4-49fb-bffb-8a2a8ceeb543": {
        "steps": {
            2: "Next, do multiplication. Going left to right, it is before division here, since the times sign comes first.",
        },
    },
    "AIGEN_grade5_87f340c6-ac43-47ab-aeb2-c54122f05d17": {
        "steps": {
            0: "Identify the operations: we have multiplication, the times sign, addition, the plus sign, and subtraction, the minus sign.",
        },
    },
    "AIGEN_grade5_d9bb5286-5a2e-48de-a2cb-3853188571d0": {
        "hints": {
            2: "Here's a similar problem worked out: 80 rupees divided by, open bracket, 3 plus 1, close bracket, times 2, plus 30, minus 5 times 4. Step 1, brackets: 3 plus 1 equals 4. Step 2, division and multiplication, left to right: 80 divided by 4 equals 20, then 20 times 2 equals 40, and 5 times 4 equals 20. Step 3, addition and subtraction, left to right: 40 plus 30 minus 20 equals 50. Answer: 50 rupees.",
        },
    },
    "AIGEN_grade5_e4d78058-ffe3-43c7-8dfb-8107f58e4dba": {
        "q": "During Diwali, Arjun and his friends are decorating their colony with diyas. Arjun buys 4 packets of diyas with 15 diyas each. He gives away 2 packets of 6 diyas to his neighbours, and then his grandmother gifts him, open bracket, 3 plus 5, close bracket, times 3, more diyas. After all this, he breaks 4 diyas while arranging them. How many diyas does Arjun have at the end?",
        "hints": {
            2: "Here's a similar problem. Priya buys 3 packets of 10 candles, which is 30. She gives away 2 times 4, which is 8 candles. Her uncle gifts her, open bracket, 2 plus 3, close bracket, times 2, which is 10 candles. She drops 2. The total is 30 minus 8, plus 10, minus 2, which equals 30. See how we handle each part, step by step? Now try Arjun's problem the same way!",
        },
    },
    "AIGEN_grade5_f71c32d3-dbdc-4b1d-8bad-0746b5478f62": {
        "steps": {
            1: "Now handle Division and Multiplication from left to right. First, 120 divided by 6 equals 20. That leaves 20 times 3, minus 5 times 2, plus 15.",
            2: "Next, 20 times 3 equals 60. That leaves 60 minus 5 times 2, plus 15.",
            3: "Then, 5 times 2 equals 10. That leaves 60 minus 10 plus 15.",
            4: "Finally, handle Addition and Subtraction from left to right. 60 minus 10 equals 50, then 50 plus 15 equals 65.",
        },
    },
}
