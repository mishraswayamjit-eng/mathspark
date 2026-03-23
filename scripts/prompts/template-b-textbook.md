# Template B — Textbook Exercise Extraction

> **Usage:** Paste this entire prompt into claude.ai, then attach a textbook PDF.
> Replace the `[PLACEHOLDERS]` below before pasting.

---

## Instructions for Claude

You are converting textbook exercises into MCQ format for a Grade [GRADE] math learning app (MathSpark — IPM exam prep).

Textbooks contain exercises that are NOT multiple-choice. Your job is to:
1. Read each exercise problem from the attached PDF
2. Solve it correctly (show your work mentally — NEVER guess)
3. Convert it into a 4-option MCQ with ONE correct answer and THREE plausible distractors
4. Generate full pedagogical content: hints, step-by-step, misconceptions

**CRITICAL RULES:**
- NEVER guess an answer. Compute every answer with certainty.
- Distractors (wrong options) must come from REAL student mistakes, not random numbers:
  - Common arithmetic errors (e.g., forgetting to carry)
  - Sign errors (e.g., subtracting instead of adding)
  - Off-by-one errors
  - Applying the wrong formula
  - Partial solutions (stopping one step early)
- If a problem is open-ended (e.g., "draw a triangle"), SKIP it — only convert problems that can become MCQs
- If a problem requires a diagram that can't be described in text, set `"flagged": true`
- For word problems, rewrite them in clear, kid-friendly English

---

## Configuration (REPLACE THESE)

- **Grade:** [GRADE]
- **Source file:** [FILENAME]
- **Batch number:** [BATCH] (e.g., 01)
- **topicId:** [TOPIC_ID] (e.g., "grade3")

---

## Topic Mapping Reference

| topicId | Grade | Use for |
|---------|-------|---------|
| `ch01-05` | 4 | Number System & Place Value |
| `ch06` | 4 | Factors & Multiples |
| `ch07-08` | 4 | Fractions |
| `ch09-10` | 4 | Operations & BODMAS |
| `ch11` | 4 | Decimal Fractions |
| `ch12` | 4 | Decimal Units of Measurement |
| `ch13` | 4 | Algebraic Expressions |
| `ch14` | 4 | Equations |
| `ch15` | 4 | Puzzles & Magic Squares |
| `ch16` | 4 | Sequence & Series |
| `ch17` | 4 | Measurement of Time & Calendar |
| `ch18` | 4 | Angles |
| `ch19` | 4 | Triangles |
| `ch20` | 4 | Quadrilaterals |
| `ch21` | 4 | Circle |
| `dh` | 4 | Data Handling & Graphs |
| `grade2` | 2 | All Grade 2 questions |
| `grade3` | 3 | All Grade 3 questions |
| `grade4` | 4 | Grade 4 IPM Past Papers |
| `grade5` | 5 | All Grade 5 questions |
| `grade6` | 6 | All Grade 6 questions |
| `grade7` | 7 | All Grade 7 questions |

---

## Distractor Generation Strategy

For each problem type, generate wrong answers using these strategies:

### Arithmetic
- **Off-by-one carry:** e.g., 47 × 8 = 376 (correct), distractors: 366 (forgot carry), 386 (extra carry), 356 (both digits wrong)
- **Wrong operation:** If the question asks for sum, one distractor uses difference

### Fractions
- **Add numerators AND denominators:** 1/3 + 1/4 → distractor "2/7" (common mistake)
- **Forget to simplify:** Give the unsimplified form as a distractor
- **Invert wrong fraction:** In division, invert the wrong one

### Algebra
- **Sign error:** Solve 2x - 5 = 11 → x = 3 (subtracted 5 instead of adding)
- **Divide wrong side:** x = 16/2 vs x = 2/16

### Geometry
- **Wrong formula:** Use perimeter formula for area, or vice versa
- **Forget a dimension:** e.g., area of triangle = base × height (forgot ÷ 2)

### Measurement
- **Wrong conversion factor:** cm to mm using ×10 instead of ×100 (wait, that's correct — use a real mistake)
- **Convert the wrong direction:** multiply instead of divide

---

## Difficulty Rubric

- **Easy:** Single-step, direct computation or recall
- **Medium:** 2-3 steps, apply a method or formula
- **Hard:** 4+ steps, combine multiple concepts, or requires insight

---

## Output JSON Schema

```json
{
  "extractionMeta": {
    "sourceFile": "[FILENAME]",
    "grade": [GRADE],
    "sourceType": "TB",
    "batch": "[BATCH]",
    "totalExtracted": 0,
    "totalFlagged": 0,
    "totalSkipped": 0,
    "extractedAt": ""
  },
  "questions": [
    {
      "id": "EXT_G[GRADE]_TB_[BATCH]_001",
      "topicId": "[TOPIC_ID]",
      "grade": [GRADE],
      "subTopic": "<descriptive sub-topic>",
      "difficulty": "Easy | Medium | Hard",
      "questionText": "<rewritten as clear MCQ>",
      "questionLatex": "<LaTeX if math-heavy, else empty string>",
      "options": [
        { "id": "A", "text": "<option>" },
        { "id": "B", "text": "<option>" },
        { "id": "C", "text": "<option>" },
        { "id": "D", "text": "<option>" }
      ],
      "correctAnswer": "A | B | C | D",
      "hints": [
        "<Strategic: identify the problem type>",
        "<Procedural: first step or formula>",
        "<Worked example: solve a similar problem with different numbers>"
      ],
      "stepByStep": [
        { "step": 1, "text": "<plain English>", "latex": "<LaTeX>" }
      ],
      "misconceptions": {
        "A": "<why a student might pick A>",
        "B": "<why a student might pick B>",
        "C": "<why a student might pick C>",
        "D": "<why a student might pick D>"
      },
      "source": "pdf_extracted",
      "flagged": false,
      "flagReason": "",
      "originalExercise": "<original exercise text from the textbook, for reference>"
    }
  ]
}
```

---

## Hint Guidelines

### Hint 1 — Strategic
Help the student identify the concept without giving the method.
Example: "This problem is about finding the area. What shape do you see?"

### Hint 2 — Procedural
Give the formula or first step.
Example: "Area of a triangle = (1/2) × base × height. What is the base here?"

### Hint 3 — Worked Example
Solve a DIFFERENT problem with the SAME method but DIFFERENT numbers.
Example: "Let's try: Find the area of a triangle with base 6 cm and height 4 cm. Area = (1/2) × 6 × 4 = 12 cm²."

---

## Step-by-Step Guidelines

- One logical operation per step
- Use LaTeX: `\frac{a}{b}`, `\times`, `\div`, `\boxed{answer}`
- Keep language at Grade [GRADE] reading level
- Final step: show the boxed answer

---

## What to SKIP (do not convert these)

- "Draw a ___" problems (no diagram support)
- "List all ___" problems (can't be MCQ)
- "Explain why ___" problems (subjective)
- Problems that rely on a specific figure/table in the textbook that can't be described in text
- Activities and projects

---

## NOW: Extract and convert all convertible exercises from the attached PDF.

Output ONLY the JSON object. No commentary before or after.
If more than 50 questions, output 50 and I will say "continue" for the next batch.
