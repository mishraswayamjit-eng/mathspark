# Template D — Enrich Existing Shell Questions

> **Usage:** Paste this prompt into claude.ai along with a JSON array of shell questions exported from the seed file.
> These are existing questions that have question text and options but are MISSING: correct answers, hints, step-by-step solutions, and misconception explanations.

---

## Instructions for Claude

You are enriching existing math questions in the MathSpark database. These questions were extracted from official IPM past papers and already have:
- ✅ Question ID
- ✅ Question text
- ✅ 4 answer options (A, B, C, D)
- ✅ Grade and year info

But they are MISSING:
- ❌ `correctAnswer` (empty string)
- ❌ `hints` (all empty strings)
- ❌ `stepByStep` (empty array)
- ❌ `misconceptions` (empty object)

**Your job:** Fill in ALL missing fields for every question.

**CRITICAL RULES:**
1. **COMPUTE every answer.** Show your work mentally. Do NOT guess. These are for children — wrong answers are harmful.
2. If you cannot determine the answer with certainty, set `"correctAnswer": ""` and `"flagged": true` with a reason.
3. All hints, step-by-step, and misconceptions must be genuinely helpful and age-appropriate.
4. **Preserve the existing ID, questionText, options, topicId, and source.** Only ADD the missing fields.

---

## Input Format

You will receive a JSON array of questions like this:

```json
[
  {
    "id": "IPM2020_G5_Q02",
    "topicId": "grade5",
    "grade": 5,
    "year": 2020,
    "questionNumber": 2,
    "subTopic": "Grade 5 2020 Q2",
    "difficulty": "Medium",
    "questionText": "Arnav sent 'm' texts/hour for 5 hours, Pranav sent 'p' texts/hour for 4 hours. Total messages?",
    "questionLatex": "",
    "options": [
      { "id": "A", "text": "9mp" },
      { "id": "B", "text": "9(m+p)" },
      { "id": "C", "text": "5m+4p" },
      { "id": "D", "text": "20mp" }
    ],
    "correctAnswer": "",
    "hints": ["", "", ""],
    "stepByStep": [],
    "misconceptions": {},
    "source": "official_ipm_2020"
  }
]
```

---

## Output Format

Return the SAME array with all missing fields filled in:

```json
[
  {
    "id": "IPM2020_G5_Q02",
    "topicId": "grade5",
    "grade": 5,
    "year": 2020,
    "questionNumber": 2,
    "subTopic": "Grade 5 — Algebraic expressions",
    "difficulty": "Medium",
    "questionText": "Arnav sent 'm' texts/hour for 5 hours, Pranav sent 'p' texts/hour for 4 hours. Total messages?",
    "questionLatex": "\\text{Total} = 5m + 4p",
    "options": [
      { "id": "A", "text": "9mp" },
      { "id": "B", "text": "9(m+p)" },
      { "id": "C", "text": "5m+4p" },
      { "id": "D", "text": "20mp" }
    ],
    "correctAnswer": "C",
    "hints": [
      "Think about what 'rate × time' gives you for each person separately.",
      "Arnav's total = m texts/hour × 5 hours = 5m. Now do the same for Pranav.",
      "Try a similar problem: If Riya reads 'r' pages/hour for 3 hours, and Siya reads 's' pages/hour for 2 hours, total pages = 3r + 2s."
    ],
    "stepByStep": [
      {
        "step": 1,
        "text": "Find Arnav's total messages: rate × time",
        "latex": "\\text{Arnav} = m \\times 5 = 5m"
      },
      {
        "step": 2,
        "text": "Find Pranav's total messages: rate × time",
        "latex": "\\text{Pranav} = p \\times 4 = 4p"
      },
      {
        "step": 3,
        "text": "Add both totals together",
        "latex": "\\text{Total} = 5m + 4p = \\boxed{5m + 4p}"
      }
    ],
    "misconceptions": {
      "A": "9mp multiplies the rates together AND adds the hours — texts aren't computed by multiplying rates with each other.",
      "B": "9(m+p) adds the rates first, then multiplies by total hours. But they worked different hours, so you can't combine them this way.",
      "C": "This is the correct answer. Rate × time for each person, then add: 5m + 4p.",
      "D": "20mp multiplies everything together. This would only make sense if rates multiplied each other, which they don't."
    },
    "source": "official_ipm_2020",
    "flagged": false
  }
]
```

---

## What You Must Do for Each Question

### 1. Compute the Correct Answer
- Work through the problem step by step
- Verify your answer matches one of the four options
- If none match, flag the question (the options might have a typo in the source)

### 2. Update subTopic (optional but recommended)
- If the current subTopic is just "Grade 5 2020 Q2", update it to be more descriptive
- Format: `"Grade {N} — {Topic area}"` (e.g., "Grade 5 — Algebraic expressions")

### 3. Add questionLatex (if applicable)
- If the question involves math expressions, add a LaTeX representation
- If it's purely verbal, leave as empty string

### 4. Generate 3 Hints (progressive)
- **Hint 1 (Strategic):** Help identify the problem type without giving the method
- **Hint 2 (Procedural):** Give the formula or first step
- **Hint 3 (Worked Example):** Solve a SIMILAR problem with DIFFERENT numbers

### 5. Generate Step-by-Step Solution
- One step per logical operation
- Use LaTeX for all math
- Final step should show `\boxed{answer}`
- Language appropriate for the grade level

### 6. Generate Misconception Explanations
- For EVERY option (A, B, C, D), explain why a student might choose it
- For the correct answer: "This is the correct answer." + brief explanation
- For wrong answers: explain the specific MISTAKE (not just "this is wrong")

---

## Batch Size

- Process up to 30 questions per paste
- If you receive more than 30, process the first 30 and say "Ready for next batch"

---

## NOW: Enrich all questions in the JSON array below.

Output ONLY the enriched JSON array. No commentary before or after.
Preserve ALL existing fields (id, topicId, grade, year, questionNumber, source).
Only ADD/UPDATE: correctAnswer, hints, stepByStep, misconceptions, subTopic (improved), questionLatex, flagged.
