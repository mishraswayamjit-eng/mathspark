# Template C — Scanned Document Extraction

> **Usage:** Paste this entire prompt into claude.ai, then attach a scanned PDF.
> Replace the `[PLACEHOLDERS]` below before pasting.

---

## Instructions for Claude

You are extracting math questions from a SCANNED document (possibly low-quality scan, handwritten portions, or mixed print). This requires extra care with OCR interpretation.

**Your job:**
1. Read and interpret every question from the scanned PDF
2. For each question, assess your OCR confidence
3. Compute correct answers (NEVER guess — if numbers are unclear, FLAG the question)
4. Convert to MCQ format with full pedagogical content
5. Output valid JSON

**SPECIAL RULES FOR SCANNED DOCUMENTS:**
- **Ambiguous characters:** If you're unsure whether a digit is 6 or 8, 1 or 7, 0 or O, etc., flag the question with `"ocrConfidence": "low"` and explain in `"flagReason"`
- **Blurry/unreadable sections:** Skip questions where critical information is unreadable. Note them in the metadata.
- **Handwritten text:** Interpret as best you can; flag anything uncertain
- **Mixed quality:** Some pages may be clear, others blurry. Process what you can, flag the rest.
- Rate EVERY question's OCR confidence: `"high"` (clearly readable), `"medium"` (some ambiguity but interpretable), `"low"` (uncertain — needs human review)

---

## Configuration (REPLACE THESE)

- **Grade:** [GRADE]
- **Source file:** [FILENAME]
- **Batch number:** [BATCH]
- **topicId:** [TOPIC_ID]
- **Document type:** [DOC_TYPE] (worksheet / textbook / past paper / mixed)

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
| `ch15`-`ch21` | 4 | See topic-mapping.md |
| `dh` | 4 | Data Handling & Graphs |
| `grade2`-`grade7` | 2-7 | Multi-grade IPM pools |

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
    "sourceType": "SC",
    "batch": "[BATCH]",
    "totalExtracted": 0,
    "totalFlagged": 0,
    "totalSkipped": 0,
    "skippedReasons": [
      "<list of page numbers / question numbers that were skipped and why>"
    ],
    "overallOcrQuality": "high | medium | low",
    "extractedAt": ""
  },
  "questions": [
    {
      "id": "EXT_G[GRADE]_SC_[BATCH]_001",
      "topicId": "[TOPIC_ID]",
      "grade": [GRADE],
      "subTopic": "<descriptive sub-topic>",
      "difficulty": "Easy | Medium | Hard",
      "questionText": "<full question text — clean up OCR artifacts>",
      "questionLatex": "<LaTeX if math, else empty>",
      "options": [
        { "id": "A", "text": "<option>" },
        { "id": "B", "text": "<option>" },
        { "id": "C", "text": "<option>" },
        { "id": "D", "text": "<option>" }
      ],
      "correctAnswer": "A | B | C | D",
      "hints": [
        "<Strategic hint>",
        "<Procedural hint>",
        "<Worked example hint>"
      ],
      "stepByStep": [
        { "step": 1, "text": "<plain English>", "latex": "<LaTeX>" }
      ],
      "misconceptions": {
        "A": "<explanation>",
        "B": "<explanation>",
        "C": "<explanation>",
        "D": "<explanation>"
      },
      "source": "pdf_extracted",
      "ocrConfidence": "high | medium | low",
      "flagged": false,
      "flagReason": "",
      "originalText": "<raw text as read from scan, before cleanup>"
    }
  ]
}
```

---

## OCR Confidence Guidelines

### High Confidence
- Text is clearly printed, no ambiguity
- All digits, operators, and symbols are unambiguous
- Set `"ocrConfidence": "high"`, `"flagged": false`

### Medium Confidence
- Mostly readable but one or two characters could be ambiguous
- You're >80% sure of your interpretation
- Set `"ocrConfidence": "medium"`, `"flagged": false`
- In `"originalText"`, note the ambiguous characters

### Low Confidence
- Key numbers or operators are unclear
- Could be multiple valid interpretations
- Set `"ocrConfidence": "low"`, `"flagged": true`
- In `"flagReason"`, explain: "Digit in position X could be 6 or 8 — affects answer"
- Still provide your best interpretation but set `"correctAnswer": ""` if you can't be certain

---

## Common OCR Pitfalls to Watch For

| Confusion | Example | How to Handle |
|-----------|---------|---------------|
| 6 vs 8 | "Find 6×7" vs "Find 8×7" | Check if context/answer key helps disambiguate |
| 1 vs 7 | "13" vs "73" | Look at handwriting style elsewhere in document |
| 0 vs O | "102" vs "1O2" | In math context, always treat as zero |
| × vs x | "3×4" vs "3x4" | In arithmetic context, treat as multiplication |
| ÷ vs + | Division vs addition | Check if answer makes sense |
| 2 vs Z | In algebra problems | Context: number → 2, variable → Z |
| - vs = | Minus vs equals | Check surrounding context |
| ½ vs 1/2 | Unicode fractions | Normalize to fraction format |

---

## Hint Guidelines (same as Template A)

- **Hint 1 (Strategic):** Identify the problem type
- **Hint 2 (Procedural):** First step or key formula
- **Hint 3 (Worked Example):** Solve a similar problem with different numbers

---

## What to SKIP

- Questions where more than 30% of the text is unreadable
- Questions that rely entirely on a diagram that can't be described
- Questions where the answer options are completely illegible
- Note all skipped questions in `extractionMeta.skippedReasons`

---

## NOW: Extract all questions from the attached scanned PDF.

Output ONLY the JSON object. No commentary before or after.
If more than 50 questions, output 50 and I will say "continue" for the next batch.
For each question, always include the `ocrConfidence` field.
