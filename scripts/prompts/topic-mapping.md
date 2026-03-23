# MathSpark Topic Mapping Reference

Use this reference when assigning `topicId` and `subTopic` to extracted questions.

---

## Grade 4 — Chapter Topics

| topicId | Name | Chapters | Example subTopics |
|---------|------|----------|-------------------|
| `ch01-05` | Number System & Place Value | 1-5 | Place value, Indian/International numeration, Comparison, Roman numerals, Rounding |
| `ch06` | Factors & Multiples | 6 | Factors, Multiples, HCF, LCM, Prime numbers, Divisibility rules |
| `ch07-08` | Fractions | 7-8 | Like/unlike fractions, Comparison, Addition/subtraction, Mixed numbers, Equivalent fractions |
| `ch09-10` | Operations & BODMAS | 9-10 | Addition, Subtraction, Multiplication, Division, BODMAS, Word problems |
| `ch11` | Decimal Fractions | 11 | Decimal place value, Decimal comparison, Decimal operations, Conversion |
| `ch12` | Decimal Units of Measurement | 12 | Length (m/cm/mm), Weight (kg/g), Capacity (L/mL), Unit conversion |
| `ch13` | Algebraic Expressions | 13 | Variables, Expressions, Simplification, Substitution |
| `ch14` | Equations | 14 | Simple equations, Solving for x, Word-to-equation, Verification |
| `ch15` | Puzzles & Magic Squares | 15 | Magic squares, Number puzzles, Pattern recognition |
| `ch16` | Sequence & Series | 16 | Arithmetic patterns, Number series, Missing terms, Rule finding |
| `ch17` | Measurement of Time & Calendar | 17 | Time conversion, Duration, Calendar problems, 12h/24h |
| `ch18` | Angles | 18 | Types of angles, Measuring angles, Complementary/supplementary, Angle pairs |
| `ch19` | Triangles | 19 | Types of triangles, Angle sum property, Perimeter, Classification |
| `ch20` | Quadrilaterals | 20 | Types of quadrilaterals, Properties, Angle sum, Perimeter |
| `ch21` | Circle | 21 | Radius, Diameter, Circumference, Parts of a circle |
| `dh` | Data Handling & Graphs | DH | Bar graph, Pictograph, Table reading, Data interpretation |

## Multi-Grade IPM Pool Topics

| topicId | Name | Grade | Use for |
|---------|------|-------|---------|
| `grade2` | Grade 2 — IPM Practice | 2 | All Grade 2 questions (worksheets, textbooks, past papers) |
| `grade3` | Grade 3 — IPM Practice | 3 | All Grade 3 questions |
| `grade4` | Grade 4 — IPM Past Papers | 4 | Grade 4 IPM past paper questions (NOT chapter-specific) |
| `grade5` | Grade 5 — IPM Practice | 5 | All Grade 5 questions |
| `grade6` | Grade 6 — IPM Practice | 6 | All Grade 6 questions |
| `grade7` | Grade 7 — IPM Practice | 7 | All Grade 7 questions |
| `grade8` | Grade 8 — IPM Practice | 8 | All Grade 8 questions |
| `grade9` | Grade 9 — IPM Practice | 9 | All Grade 9 questions |

---

## SubTopic Naming Conventions

For **Grade 4 chapter questions** (ch01-ch21, dh), use descriptive subTopics:
- `"Place value up to 9 digits"`
- `"HCF and LCM"`
- `"Fraction addition — unlike denominators"`
- `"BODMAS with brackets"`

For **multi-grade pool questions** (grade2-grade9), use this format:
- `"Grade {N} {Year} Q{Number}"` — for past paper questions (e.g., `"Grade 5 2020 Q15"`)
- `"Grade {N} — {Topic}"` — for worksheet/textbook questions (e.g., `"Grade 6 — Algebra basics"`)

---

## Difficulty Rubric

| Level | Criteria | Examples |
|-------|----------|---------|
| **Easy** | Single-step recall or direct application. Student needs one concept. | "What is 25 × 4?", "Name the angle type: 90°" |
| **Medium** | 2-3 step procedure. Requires applying a method or combining two concepts. | "Find HCF of 24 and 36", "Solve: 3x + 5 = 20" |
| **Hard** | Multi-concept reasoning, non-standard problems, or requires insight. 4+ steps. | "Arrange fractions in ascending order: 3/7, 2/5, 4/9", "Find the missing angle in a quadrilateral with 3 angles given" |

---

## ID Scheme for Extracted Questions

Format: `EXT_{GRADE}_{SOURCE}_{BATCH}_{NNN}`

- **GRADE:** `G2`, `G3`, `G4`, `G5`, `G6`, `G7`
- **SOURCE:** `WS` (worksheet), `PP` (past paper), `TB` (textbook), `MF` (mega final), `SC` (scanned)
- **BATCH:** `01`, `02`, etc. (sequential per source file)
- **NNN:** `001`, `002`, etc. (sequential within batch)

Examples:
- `EXT_G5_WS_01_042` — Grade 5, Worksheet, Batch 1, Question 42
- `EXT_G6_PP_01_015` — Grade 6, Past Paper, Batch 1, Question 15
- `EXT_G2_TB_01_003` — Grade 2, Textbook, Batch 1, Question 3

---

## Source Field Values

| Value | Meaning |
|-------|---------|
| `hand_crafted` | Human-written, fully verified (original 395) |
| `auto_generated` | Python-computed (original 1,950) |
| `auto_generated_v2` | Second-generation auto-generated |
| `official_ipm_{YEAR}` | Official IPM past paper (existing shells) |
| `pdf_extracted` | Extracted from PDF via Claude (new extractions) |
| `variant_of_{ID}` | Computational variant of a parent question |
