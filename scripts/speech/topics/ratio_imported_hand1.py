"""Hand-written narration: the imported textbook questions (IPMTB_grade5_ch07_...).

These are bare BODMAS expressions with three kinds of bracket, typed with * and / for times and
divide. Every question, and every line with working in it, is written by hand. A line given as
None is plain prose and is spoken by the rules in ratio_imported_rules.py.

Brackets are named as the textbook names them: "open bracket" for ( ), "open curly bracket"
for { }, "open square bracket" for [ ].
"""

HAND = {
    "IPMTB_grade5_ch07_q003": {
        "q": "11 minus, open square bracket, 17 minus, open curly bracket, 15 minus 3, open bracket, 7 minus 4, close bracket, close curly bracket, close square bracket. What does it equal?",
        "hints": [
            "This is a BODMAS problem with nested brackets. Remember to work from the innermost bracket outward!",
            "Start with the innermost bracket first. What is 7 minus 4?",
            "Here's a similar problem worked out. 10 minus, open square bracket, 14 minus, open curly bracket, 12 minus 2, open bracket, 5 minus 3, close bracket, close curly bracket, close square bracket. Step 1, the innermost bracket: 5 minus 3 equals 2. Step 2, multiply: 2 times 2 equals 4. Step 3, the curly braces: 12 minus 4 equals 8. Step 4, the square brackets: 14 minus 8 equals 6. Step 5, the final step: 10 minus 6 equals 4. See how we peel off one layer at a time, like peeling an onion!",
        ],
        "steps": [
            "Start with the innermost bracket, 7 minus 4.",
            "Now handle the multiplication. The 3 before the bracket means multiply: 3 times 3.",
            "Now solve inside the curly braces: 15 minus 9 equals 6.",
            "Now solve inside the square brackets: 17 minus 6 equals 11.",
            None,
        ],
    },
    "IPMTB_grade5_ch07_q004": {
        "q": "Open bracket, 8 minus 7, close bracket, times, open square bracket, 8 plus 2 times, 5 minus 1 under a bar, close square bracket. What does it equal?",
        "hints": [
            "This is a BODMAS problem. Remember to work from the innermost brackets outward, and always do multiplication before addition!",
            "Start with the innermost expression first. What is the value inside the bar, called the vinculum? That is, 5 minus 1.",
            "Here's a similar problem. Open bracket, 3 minus 2, close bracket, times, open square bracket, 6 plus 2 times, 4 minus 1 under a bar, close square bracket. First, the bar: 4 minus 1 equals 3. Then multiply: 2 times 3 equals 6. Then add inside the square brackets: 6 plus 6 equals 12. Then the round brackets: 3 minus 2 equals 1. Finally, 1 times 12 equals 12.",
        ],
        "steps": [
            "Identify the innermost operation, the vinculum, or bar. Calculate what's inside it first: 5 minus 1 equals 4.",
            "Now substitute back, and look inside the square brackets. We have 8 plus 2 times 4. By BODMAS, do multiplication before addition: 2 times 4 equals 8.",
            None,
            "Now handle the round brackets: 8 minus 7 equals 1.",
            None,
            None,
        ],
    },
    "IPMTB_grade5_ch07_q006": {
        "q": "7 times 2, minus 7 divided by 7, plus 3 times 1. What does it equal?",
        "hints": [
            None,
            "Start by identifying all the multiplication and division operations. Do all of them first, from left to right, before touching the addition and subtraction.",
            "Here's a similar problem: 3 times 4, minus 6 divided by 3, plus 2 times 5. First, do the multiplications and the division: 3 times 4 equals 12, 6 divided by 3 equals 2, and 2 times 5 equals 10. Now rewrite: 12 minus 2 plus 10 equals 20. See how we handled all the multiplying and dividing, before the adding and subtracting? Try the same approach!",
        ],
        "steps": [
            None,
            "According to BODMAS, do multiplication and division first, from left to right. Let's start with 7 times 2.",
            "Next, do the division: 7 divided by 7.",
            "Now do the last multiplication: 3 times 1.",
            None,
            "Work left to right: 14 minus 1 equals 13, then 13 plus 3 equals 16.",
        ],
    },
    "IPMTB_grade5_ch07_q011": {
        "q": "16, minus 12 divided by 4, plus one half of 10. What does it equal?",
        "hints": [
            "This is a BODMAS problem! Remember the order: Brackets, then Orders, then Division, then Multiplication, then Addition, then Subtraction. And the word of means multiplication!",
            "Start by identifying all the operations: the subtraction from 16, the division, 12 divided by 4, and the word of, in one half of 10. Now handle of, which is multiplication, and division, before addition and subtraction.",
            "Here's a similar problem: 20, minus 8 divided by 2, plus one half of 6. Step 1: 8 divided by 2 equals 4. Step 2: one half of 6 equals 3. Step 3: 20 minus 4 plus 3 equals 19. See how we did division, and of, first, then went left to right for subtraction and addition?",
        ],
        "steps": [
            None,
            "According to BODMAS, the word of means multiplication, and comes first, along with division. Let's handle the division: 12 divided by 4 equals 3.",
            "Now handle of. Remember, of means multiply! So one half of 10 equals one half times 10, which is 5.",
            "Replace these back into the expression. Now we have 16 minus 3 plus 5.",
            "Now go left to right, subtraction first, then addition: 16 minus 3 equals 13, then 13 plus 5 equals 18.",
            None,
        ],
    },
    "IPMTB_grade5_ch07_q014": {
        "q": "10 plus 10 times 10, equals 100 plus a box. Which number from the given alternatives should replace the box?",
        "hints": [
            "This is a BODMAS problem! Remember, multiplication always comes before addition, even if addition appears first when you read left to right.",
            "Start by computing the left side. Apply BODMAS to 10 plus 10 times 10. Which operation do you do first, the addition or the multiplication?",
            "Here's a similar problem. What goes in the box for 5 plus 3 times 4, equals 10 plus a box? First, the left side: 3 times 4 equals 12, then 5 plus 12 equals 17. The right side: 10 plus the box equals 17, so the box equals 7. Now try the same approach with the original question!",
        ],
        "steps": [
            "Look at the left side of the equation: 10 plus 10 times 10. According to BODMAS, we must do multiplication before addition.",
            "Do the multiplication first: 10 times 10 equals 100.",
            "Now do the addition: 10 plus 100 equals 110. So the left side equals 110.",
            "Now look at the right side: 100 plus the box. We need this to equal 110.",
            "Subtract 100 from both sides: the box equals 110 minus 100, which is 10. So the answer is 10!",
        ],
    },
    "IPMTB_grade5_ch07_q015": {
        "q": "Which of the following expression is correct?",
        "options": [
            "7 plus 7 times 7 equals 77",
            "25 plus 7 times 0 equals 0",
            "6 plus 6, minus 6 times 6 divided by 6, equals 6",
            "16, open square bracket, 2 plus 3 times 2 minus 8, close square bracket, equals 16",
        ],
        "hints": [
            "This is a BODMAS question. Remember, multiplication and division come before addition and subtraction! Check each expression carefully, using the correct order of operations.",
            "Start by evaluating each expression, one at a time. For each one, do multiplication and division first, from left to right. Then do addition and subtraction, from left to right. See which one gives a true statement!",
            "Here's a similar problem. Is 3 plus 4 times 2 equal to 14, or 11? Using BODMAS, we do multiplication first: 4 times 2 equals 8. Then addition: 3 plus 8 equals 11. So 3 plus 4 times 2 equals 11, not 14. The person who got 14 added first: 3 plus 4 equals 7, then 7 times 2 equals 14. That's not following BODMAS!",
        ],
        "steps": [
            "Let's check Option A: 7 plus 7 times 7. Do multiplication first: 7 times 7 equals 49. Then add: 7 plus 49 equals 56. But the expression says it equals 77. That's not true!",
            "Let's check Option B: 25 plus 7 times 0. Do multiplication first: 7 times 0 equals 0. Then add: 25 plus 0 equals 25. But the expression says it equals 0. That's not true!",
            "Let's check Option C: 6 plus 6, minus 6 times 6 divided by 6. First, do multiplication and division from left to right. Start with 6 times 6 equals 36, then 36 divided by 6 equals 6.",
            "Now the expression becomes 6 plus 6 minus 6. Do addition and subtraction left to right: 6 plus 6 equals 12, then 12 minus 6 equals 6. The expression says it equals 6. That's true!",
            "Let's verify Option D too: 16, open square bracket, 2 plus 3 times 2 minus 8, close square bracket. Brackets first! Inside the brackets, do multiplication first: 3 times 2 equals 6. Then 2 plus 6 minus 8 equals 0. So 16 times 0 equals 0. But the expression says it equals 16. That's not true!",
            "Only Option C gives a correct equation. So the answer is C!",
        ],
    },
    "IPMTB_grade5_ch07_q016": {
        "q": "16 times 5, plus 5, minus 2 times 10 divided by 5, plus 5 times 2, minus 1. What does it equal?",
        "hints": [
            "This is a BODMAS problem! Remember the order: Brackets, Orders, Division, Multiplication, Addition, Subtraction. Multiplication and Division come before Addition and Subtraction!",
            "First, find all the multiplication and division parts in the expression, and solve them before doing any addition or subtraction. Identify each group: 16 times 5, 2 times 10 divided by 5, and 5 times 2.",
            "Here's a similar problem: 3 times 4, plus 2, minus 6 divided by 3, plus 1 times 5, minus 3. Step 1: do the multiplications and divisions first. 3 times 4, plus 2, minus 6 divided by 3, plus 1 times 5, minus 3, becomes 12 plus 2, minus 2, plus 5, minus 3. Step 2: now go left to right with plus and minus. 12 plus 2 equals 14. 14 minus 2 equals 12. 12 plus 5 equals 17. 17 minus 3 equals 14. The answer is 14.",
        ],
        "steps": [
            "Write out the full expression, and spot all the multiplication and division operations first.",
            "Solve 16 times 5 first: 16 times 5 equals 80.",
            "Now solve 2 times 10 divided by 5. Multiplication and division are at the same level, so go left to right: first 2 times 10 equals 20, then 20 divided by 5 equals 4.",
            "Now solve 5 times 2. So, 5 times 2 equals 10.",
            "Replace all the multiplication and division results back into the expression. Now we only have addition and subtraction left!",
            None,
            None,
            None,
            None,
            None,
        ],
    },
    "IPMTB_grade5_ch07_q018": {
        "q": "Open square bracket, 70 plus, open curly bracket, 5 times 8 minus, open bracket, 12 minus 3 times 5, close bracket, close curly bracket, close square bracket, times 3.",
        "hints": [
            "This is a BODMAS problem. Remember to work from the innermost brackets outward! Think of it like peeling layers of an onion.",
            "Start with the innermost parentheses first. Calculate 3 times 5, inside the round brackets, 12 minus 3 times 5. Remember, multiplication comes before subtraction, even inside brackets!",
            "Here's a similar problem worked out. Open square bracket, 50 plus, open curly bracket, 4 times 6 minus, open bracket, 10 minus 2 times 3, close bracket, close curly bracket, close square bracket, times 2. Step 1, the innermost brackets: 2 times 3 equals 6, then 10 minus 6 equals 4. Step 2, the curly brackets: 4 times 6 equals 24, then 24 minus 4 equals 20. Step 3, the square brackets: 50 plus 20 equals 70. Step 4, the final multiplication: 70 times 2 equals 140. The answer is 140.",
        ],
        "steps": [
            "Start with the innermost brackets: 12 minus 3 times 5. Inside here, multiplication comes first!",
            None,
            "Move to the curly brackets: 5 times 8, minus, open bracket, minus 3, close bracket. First do the multiplication: 5 times 8 equals 40.",
            "Now handle the subtraction of a negative number. Subtracting minus 3 is the same as adding 3! Think of it like this: if someone takes away a debt of 3 rupees, you actually gain 3 rupees!",
            None,
            None,
            None,
        ],
    },
    "IPMTB_grade5_ch07_q025": {
        "q": "35 divided by 7, plus 25 divided by 5, plus 15 divided by 5. What does it equal?",
        "hints": [
            "This is a BODMAS problem! Think about which operations you need to do first. Division comes before addition.",
            "Start by performing each division separately. Compute 35 divided by 7, then 25 divided by 5, then 15 divided by 5. After that, add all the results together.",
            "Here's a similar problem: 20 divided by 4, plus 12 divided by 3, plus 18 divided by 6. Step 1: 20 divided by 4 equals 5. Step 2: 12 divided by 3 equals 4. Step 3: 18 divided by 6 equals 3. Step 4: 5 plus 4 plus 3 equals 12.",
        ],
        "steps": [
            "According to BODMAS, Division, D, comes before Addition, A. So we do all the divisions first! Let's start with the first one: 35 divided by 7 equals 5.",
            None,
            None,
            None,
            None,
        ],
    },
    "IPMTB_grade5_ch07_q026": {
        "q": "Open bracket, 7 plus 2, minus 14 times one half, minus 5, minus 2, close bracket, times 0.",
        "hints": [
            "Before doing any heavy calculation inside the brackets, take a look at what's happening outside the brackets. Is there something special being multiplied?",
            "Remember the golden rule: anything multiplied by 0 equals 0. Check what the entire expression inside the parentheses is being multiplied by!",
            "Here's a similar problem: open bracket, 100 plus 55, minus 33 times 2, plus 17, close bracket, times 0. No matter how complicated the stuff inside the brackets is, the whole thing is multiplied by 0, so the answer is just 0! It's like having 0 boxes of samosas. No matter how many samosas each box holds, you still have 0 samosas!",
        ],
        "steps": [
            "Let's look at the structure of the expression. We have something in parentheses, multiplied by 0: open bracket, 7 plus 2, minus 14 times one half, minus 5, minus 2, close bracket, times 0.",
            "The entire expression inside the parentheses is being multiplied by 0. Remember the Zero Property of Multiplication: any number times 0 equals 0. It doesn't matter what the value inside the brackets is!",
            "But just to be thorough, let's verify the inside isn't undefined, like dividing by zero. Using BODMAS inside the brackets, first do multiplication: 14 times one half equals 7.",
            "The value inside the brackets is minus 5. Now multiply by 0: minus 5 times 0 equals 0.",
            "So the final answer is 0. The zero outside wipes everything out, like erasing a whole chalkboard in one swipe!",
        ],
    },
    "IPMTB_grade5_ch07_q027": {
        "q": "20, minus 8 divided by 2, plus one third of 18. What does it equal?",
        "hints": [
            "This is a BODMAS problem! Remember the order: Brackets, Orders, Division, Multiplication, Addition, Subtraction. But wait. The word of means multiplication, and it comes before division and multiplication in priority!",
            "Start by solving one third of 18 first, since of means multiplication, and is handled early. Then do the division, 8 divided by 2, and finally work left to right with addition and subtraction.",
            "Here's a similar problem. Solve 10, minus 6 divided by 3, plus one half of 12. Step 1: one half of 12 equals 6. Step 2: 6 divided by 3 equals 2. Step 3: 10 minus 2 plus 6 equals 14. So the answer is 14. See how we handled of, and division, first, then went left to right? Try the same approach on your question!",
        ],
        "steps": [
            None,
            "In BODMAS, of means multiplication, and is done first. It's part of the O in BODMAS. Some teachers group it there. Let's solve one third of 18.",
            "Now handle the division: 8 divided by 2.",
            None,
            None,
            None,
            None,
        ],
    },
    "IPMTB_grade5_ch07_q031": {
        "q": "Which of the following expressions is incorrect?",
        "options": [
            "1 over 5 of 125, divided by 25, minus 1, equals 0",
            "Open curly bracket, 9 minus 3 minus, open bracket, 7 plus 6, minus 6, minus 6, minus 7, close bracket, close curly bracket, times 0, equals 0",
            "8 divided by 2 times 6, minus 3 divided by 9, plus 27, equals 3",
            "One quarter, divided by three quarters, divided by 2 over 4, times 4 over 3, equals 8 over 9",
        ],
        "hints": [
            "This question asks you to find the expression that does not give the correct result. So you need to check each one using BODMAS, and see which equation is actually false!",
            "Start by carefully evaluating expression C. Remember, in BODMAS, division and multiplication are done left to right, as they have equal priority, and addition and subtraction are also done left to right.",
            "Here's a similar problem. Is, 6 divided by 2 times 3, minus 1, plus 2, equals 2, correct? Let's check: 6 divided by 2 equals 3, then 3 times 3 equals 9, then 9 minus 1 equals 8, then 8 plus 2 equals 10. Since 10 is not equal to 2, this expression would be the incorrect one! See how we go left to right for times and divide, then left to right for plus and minus?",
        ],
        "steps": [
            "Let's check Option A: 1 over 5 of 125, divided by 25, minus 1. Of means multiplication. By BODMAS, we handle division and multiplication left to right.",
            "Let's check Option B: open curly bracket, 9 minus 3 minus, open bracket, 7 plus 6, minus 6, minus 6, minus 7, close bracket, close curly bracket, times 0. First solve the inner bracket.",
            "Continue with Option B. Now the curly bracket becomes 9 minus 3 minus, open bracket, minus 6, close bracket. That is 9 minus 3 plus 6, which equals 12. Then 12 times 0 equals 0.",
            "Now let's check Option C: 8 divided by 2 times 6, minus 3 divided by 9, plus 27. Remember: division and multiplication go left to right, then addition and subtraction go left to right.",
            "Next multiplication, going left to right: 4 times 6 equals 24. Then handle the next division: 3 divided by 9 equals one third.",
            "Now do addition and subtraction left to right: 24 minus one third plus 27, equals 51 minus one third, which is 50 and two thirds. This is definitely not equal to 3!",
            "Let's verify Option D, just to be thorough: one quarter, divided by three quarters, divided by 2 over 4, times 4 over 3. Division by a fraction means multiply by its reciprocal. Going left to right: one quarter divided by three quarters, equals one quarter times 4 over 3, which is one third.",
            "Continue Option D: one third divided by 2 over 4, equals one third times 4 over 2, which is one third times 2, which is two thirds. Then two thirds times 4 over 3 equals 8 over 9.",
            "So Options A, B, and D all give correct results. Only Option C gives 50 and two thirds, instead of 3. That's our answer. C is the incorrect expression!",
        ],
    },
    "IPMTB_grade5_ch07_q032": {
        "q": "5 times 125 times 15, divided by 625, times 3 times 45. What does it equal?",
        "hints": [
            "This problem is all about following the order of operations carefully. When you see only multiplication and division, with no addition or subtraction, you work from left to right, like reading a sentence!",
            "Start from the left. First compute 5 times 125, then multiply by 15, then divide by 625, then multiply by 3, then multiply by 45. Take it one step at a time!",
            "Here's a similar problem: 2 times 50 times 4, divided by 100, times 3 times 10. Step 1: 2 times 50 equals 100. Step 2: 100 times 4 equals 400. Step 3: 400 divided by 100 equals 4. Step 4: 4 times 3 equals 12. Step 5: 12 times 10 equals 120. The answer is 120.",
        ],
        "steps": [
            "Start from the left. First, multiply 5 times 125.",
            None,
            "Now divide by 625. Notice something cool: 9375 divided by 625 is a nice number!",
            None,
            None,
            None,
        ],
    },
}
