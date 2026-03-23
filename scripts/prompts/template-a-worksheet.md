# Template A — Worksheet / Past Paper Extraction

> **Usage:** Paste this entire prompt into claude.ai, then attach a worksheet or past paper PDF.
> Replace the `[PLACEHOLDERS]` below before pasting.

---

## Instructions for Claude

You are extracting math MCQ questions from an IPM (Institute for Promotion of Mathematics) worksheet or past paper PDF for a Grade [GRADE] student learning app.

**Your job:**
1. Extract EVERY multiple-choice question from the attached PDF
2. Compute the correct answer for each question (show your work mentally — do NOT guess)
3. Generate pedagogical content: hints, step-by-step solution, and misconception explanations
4. Output valid JSON matching the exact schema below

**CRITICAL RULES:**
- NEVER guess an answer. If you cannot compute the answer with certainty, set `"correctAnswer": ""` and add `"flagged": true` with a reason.
- Every hint must be genuinely helpful, not just "try again"
- Step-by-step solutions must use proper LaTeX for math expressions
- Misconception explanations must explain WHY a student might choose each wrong option
- If a question has a diagram/figure that is essential and cannot be described in text, set `"flagged": true, "flagReason": "requires diagram"`

---

## Configuration (REPLACE THESE)

- **Grade:** [GRADE] (e.g., 5)
- **Source file:** [FILENAME] (e.g., "Grade 5_IPM worksheets.pdf")
- **Source type:** [SOURCE_TYPE] (WS = worksheet, PP = past paper, MF = mega final)
- **Batch number:** [BATCH] (e.g., 01)
- **topicId:** [TOPIC_ID] (e.g., "grade5" — see topic mapping below)

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

## Difficulty Rubric

- **Easy:** Single-step recall or direct application (e.g., "What is 25 × 4?")
- **Medium:** 2-3 step procedure or combining two concepts (e.g., "Find HCF of 24 and 36")
- **Hard:** Multi-concept reasoning, 4+ steps, or non-standard (e.g., "Which fraction is largest: 3/7, 2/5, 4/9?")

---

## Output JSON Schema

Output a single JSON object with this exact structure:

```json
{
  "extractionMeta": {
    "sourceFile": "[FILENAME]",
    "grade": [GRADE],
    "sourceType": "[SOURCE_TYPE]",
    "batch": "[BATCH]",
    "totalExtracted": <number>,
    "totalFlagged": <number>,
    "extractedAt": "<ISO date>"
  },
  "questions": [
    {
      "id": "EXT_G[GRADE]_[SOURCE_TYPE]_[BATCH]_001",
      "topicId": "[TOPIC_ID]",
      "grade": [GRADE],
      "subTopic": "<descriptive sub-topic name>",
      "difficulty": "Easy | Medium | Hard",
      "questionText": "<full question text, plain English>",
      "questionLatex": "<LaTeX version of the question if it contains math, otherwise empty string>",
      "options": [
        { "id": "A", "text": "<option A text>" },
        { "id": "B", "text": "<option B text>" },
        { "id": "C", "text": "<option C text>" },
        { "id": "D", "text": "<option D text>" }
      ],
      "correctAnswer": "A | B | C | D",
      "hints": [
        "<Hint 1: Strategic — guide the student to identify what TYPE of problem this is>",
        "<Hint 2: Procedural — give the first step or key formula to use>",
        "<Hint 3: Worked example — solve a SIMILAR problem (different numbers) step by step>"
      ],
      "stepByStep": [
        {
          "step": 1,
          "text": "<explanation of this step in plain English>",
          "latex": "<LaTeX expression showing the math for this step>"
        },
        {
          "step": 2,
          "text": "<next step>",
          "latex": "<LaTeX>"
        }
      ],
      "misconceptions": {
        "A": "<Why a student might incorrectly choose A — explain the mistake>",
        "B": "<Why a student might incorrectly choose B>",
        "C": "<Why a student might incorrectly choose C>",
        "D": "<Why a student might incorrectly choose D>"
      },
      "source": "pdf_extracted",
      "flagged": false,
      "flagReason": ""
    }
  ]
}
```

**Note on misconceptions:** For the CORRECT answer, still write a brief note like "This is the correct answer." For wrong answers, explain the specific computational or conceptual mistake that leads to that wrong answer.

---

## Hint Guidelines

### Hint 1 — Strategic (What type of problem is this?)
- Help the student recognize the concept: "This is a problem about finding LCM..."
- Point to the key information: "Look at what the question is really asking..."
- Do NOT give away the method yet

### Hint 2 — Procedural (What's the first step?)
- Give the specific method or formula: "To find LCM, first find the prime factorization..."
- Show the first step of the solution: "Start by dividing both numbers by 2..."
- Do NOT solve the entire problem

### Hint 3 — Worked Example (Solve a similar problem)
- Create a DIFFERENT problem with DIFFERENT numbers but the SAME concept
- Solve it completely step by step
- The student can then apply the same method to the original problem
- Example: "Let's try a similar problem: Find the LCM of 6 and 8. Step 1: 6 = 2 × 3, 8 = 2³. Step 2: LCM = 2³ × 3 = 24."

---

## Step-by-Step Guidelines

- Each step should be ONE logical operation
- Use LaTeX for ALL mathematical expressions (fractions: `\frac{a}{b}`, multiplication: `\times`, etc.)
- The final step should clearly show the boxed answer: `\boxed{answer}`
- Keep explanations kid-friendly (Grade [GRADE] level vocabulary)

---

## NOW: Extract all questions from the attached PDF.

Output ONLY the JSON object. No commentary before or after the JSON.
If the PDF has more than 50 questions, split into chunks of 50 and I will ask for "continue" to get the next chunk.
