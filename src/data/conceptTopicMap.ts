// Maps all 88 concept-map concepts → practice topics, flashcard decks, worked-example topics.
// Grade-aware: the same concept may map to different practice topicIds by grade.

export interface PracticeLink {
  grade: number;
  topicId: string;       // matches Question.topicId in DB
  subTopicKey?: string;  // optional ILIKE filter on Question.subTopic
}

export interface FlashcardLink {
  grade: number;
  topicId: string;       // topicId in concept_flashcards_all_grades.json
}

export interface ConceptMapping {
  practiceLinks: PracticeLink[];
  flashcardLinks: FlashcardLink[];
  exampleTopic: string | null;  // worked-examples topic keyword
}

// ── Full map: 88 concepts ────────────────────────────────────────────────────

export const CONCEPT_TOPIC_MAP: Record<string, ConceptMapping> = {
  // ─── numbers domain ────────────────────────────────────────────────────────
  CN_001: { // Counting
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'number' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'number' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'num' },
      { grade: 3, topicId: 'num' },
    ],
    exampleTopic: 'counting',
  },
  CN_002: { // Place Value System
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'number' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'number' },
      { grade: 4, topicId: 'ch01-05' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'num' },
      { grade: 3, topicId: 'num' },
      { grade: 4, topicId: 'numbers' },
      { grade: 5, topicId: 'pl' },
      { grade: 6, topicId: 'pl' },
    ],
    exampleTopic: 'place_value',
  },
  CN_003: { // Comparing & Ordering Numbers
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'number' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'number' },
      { grade: 4, topicId: 'ch01-05' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'num' },
      { grade: 3, topicId: 'num' },
      { grade: 4, topicId: 'numbers' },
    ],
    exampleTopic: 'place_value',
  },
  CN_004: { // Rounding Numbers
    practiceLinks: [
      { grade: 3, topicId: 'grade3', subTopicKey: 'number' },
      { grade: 4, topicId: 'ch01-05' },
    ],
    flashcardLinks: [
      { grade: 3, topicId: 'num' },
      { grade: 4, topicId: 'numbers' },
    ],
    exampleTopic: 'place_value',
  },
  CN_005: { // Roman Numerals
    practiceLinks: [
      { grade: 3, topicId: 'grade3', subTopicKey: 'number' },
      { grade: 4, topicId: 'ch01-05' },
    ],
    flashcardLinks: [
      { grade: 3, topicId: 'roman' },
      { grade: 4, topicId: 'roman' },
    ],
    exampleTopic: 'roman',
  },
  CN_006: { // Integers
    practiceLinks: [
      { grade: 6, topicId: 'grade6', subTopicKey: 'integer' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'int' },
    ],
    exampleTopic: 'integers',
  },
  CN_007: { // Even & Odd Numbers
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'number' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'number' },
      { grade: 4, topicId: 'ch01-05' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'num' },
      { grade: 3, topicId: 'num' },
      { grade: 4, topicId: 'numbers' },
    ],
    exampleTopic: 'place_value',
  },

  // ─── arithmetic domain ─────────────────────────────────────────────────────
  CN_008: { // Addition
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'addition' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'number' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'add' },
      { grade: 3, topicId: 'num' },
    ],
    exampleTopic: 'counting',
  },
  CN_009: { // Subtraction
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'addition' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'number' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'add' },
      { grade: 3, topicId: 'num' },
    ],
    exampleTopic: 'counting',
  },
  CN_010: { // Multiplication
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'number' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'multiplication' },
      { grade: 4, topicId: 'ch09-10' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'mul' },
      { grade: 3, topicId: 'mul' },
      { grade: 4, topicId: 'bodmas' },
    ],
    exampleTopic: 'bodmas',
  },
  CN_011: { // Division
    practiceLinks: [
      { grade: 3, topicId: 'grade3', subTopicKey: 'multiplication' },
      { grade: 4, topicId: 'ch09-10' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'decimal' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'div' },
      { grade: 3, topicId: 'mul' },
      { grade: 4, topicId: 'bodmas' },
    ],
    exampleTopic: 'bodmas',
  },
  CN_012: { // BODMAS / Order of Operations
    practiceLinks: [
      { grade: 4, topicId: 'ch09-10' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'decimal' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'integer' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'bodmas' },
      { grade: 5, topicId: 'dec' },
      { grade: 6, topicId: 'int' },
    ],
    exampleTopic: 'bodmas',
  },
  CN_013: { // Number Properties
    practiceLinks: [
      { grade: 4, topicId: 'ch01-05' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'decimal' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'integer' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'numbers' },
      { grade: 5, topicId: 'pl' },
      { grade: 6, topicId: 'int' },
    ],
    exampleTopic: 'place_value',
  },

  // ─── factors domain ────────────────────────────────────────────────────────
  CN_014: { // Divisibility Rules
    practiceLinks: [
      { grade: 4, topicId: 'ch06' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'factors' },
      { grade: 5, topicId: 'lcmhcf' },
    ],
    exampleTopic: 'hcf_lcm',
  },
  CN_015: { // Factors & Multiples
    practiceLinks: [
      { grade: 4, topicId: 'ch06' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'factors' },
      { grade: 5, topicId: 'lcmhcf' },
    ],
    exampleTopic: 'hcf_lcm',
  },
  CN_016: { // Prime & Composite Numbers
    practiceLinks: [
      { grade: 4, topicId: 'ch06' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'fraction' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'factors' },
      { grade: 5, topicId: 'lcmhcf' },
    ],
    exampleTopic: 'hcf_lcm',
  },
  CN_017: { // HCF (Highest Common Factor)
    practiceLinks: [
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'fraction' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'algebra' },
    ],
    flashcardLinks: [
      { grade: 5, topicId: 'lcmhcf' },
    ],
    exampleTopic: 'hcf_lcm',
  },
  CN_018: { // LCM (Least Common Multiple)
    practiceLinks: [
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'fraction' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'algebra' },
    ],
    flashcardLinks: [
      { grade: 5, topicId: 'lcmhcf' },
    ],
    exampleTopic: 'hcf_lcm',
  },

  // ─── fractions domain ──────────────────────────────────────────────────────
  CN_019: { // Understanding Fractions
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'number' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'fraction' },
      { grade: 4, topicId: 'ch07-08' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'frac' },
      { grade: 3, topicId: 'frac' },
      { grade: 4, topicId: 'fractions' },
    ],
    exampleTopic: 'fractions',
  },
  CN_020: { // Equivalent Fractions
    practiceLinks: [
      { grade: 3, topicId: 'grade3', subTopicKey: 'fraction' },
      { grade: 4, topicId: 'ch07-08' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
    ],
    flashcardLinks: [
      { grade: 3, topicId: 'frac' },
      { grade: 4, topicId: 'fractions' },
    ],
    exampleTopic: 'fractions',
  },
  CN_021: { // Comparing Fractions
    practiceLinks: [
      { grade: 3, topicId: 'grade3', subTopicKey: 'fraction' },
      { grade: 4, topicId: 'ch07-08' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
    ],
    flashcardLinks: [
      { grade: 3, topicId: 'frac' },
      { grade: 4, topicId: 'fractions' },
    ],
    exampleTopic: 'fractions',
  },
  CN_022: { // Adding & Subtracting Fractions
    practiceLinks: [
      { grade: 4, topicId: 'ch07-08' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'fraction' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'fractions' },
      { grade: 5, topicId: 'lcmhcf' },
      { grade: 6, topicId: 'pct' },
    ],
    exampleTopic: 'fractions',
  },
  CN_023: { // Multiplying & Dividing Fractions
    practiceLinks: [
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'fraction' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'percentage' },
    ],
    flashcardLinks: [
      { grade: 5, topicId: 'lcmhcf' },
      { grade: 6, topicId: 'pct' },
      { grade: 7, topicId: 'rational' },
    ],
    exampleTopic: 'fractions',
  },
  CN_024: { // Fraction of a Number
    practiceLinks: [
      { grade: 3, topicId: 'grade3', subTopicKey: 'fraction' },
      { grade: 4, topicId: 'ch07-08' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'fraction' },
    ],
    flashcardLinks: [
      { grade: 3, topicId: 'frac' },
      { grade: 4, topicId: 'fractions' },
    ],
    exampleTopic: 'fractions',
  },
  CN_025: { // Decimals
    practiceLinks: [
      { grade: 4, topicId: 'ch11' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'decimal' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'integer' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'decimals' },
      { grade: 5, topicId: 'dec' },
    ],
    exampleTopic: 'fractions',
  },

  // ─── percentage domain ─────────────────────────────────────────────────────
  CN_026: { // Percentage Basics
    practiceLinks: [
      { grade: 5, topicId: 'grade5', subTopicKey: 'percentage' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'percentage' },
    ],
    flashcardLinks: [
      { grade: 5, topicId: 'pct' },
      { grade: 6, topicId: 'pct' },
    ],
    exampleTopic: 'percentage',
  },
  CN_027: { // Finding Percentage of a Number
    practiceLinks: [
      { grade: 5, topicId: 'grade5', subTopicKey: 'percentage' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'percentage' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'percentage' },
    ],
    flashcardLinks: [
      { grade: 5, topicId: 'pct' },
      { grade: 6, topicId: 'pct' },
      { grade: 6, topicId: 'pct2' },
    ],
    exampleTopic: 'percentage',
  },
  CN_028: { // Percentage Increase & Decrease
    practiceLinks: [
      { grade: 6, topicId: 'grade6', subTopicKey: 'percentage' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'percentage' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'pct2' },
      { grade: 7, topicId: 'discount' },
    ],
    exampleTopic: 'percentage',
  },
  CN_029: { // Profit & Loss
    practiceLinks: [
      { grade: 6, topicId: 'grade6', subTopicKey: 'percentage' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'percentage' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'ratio' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'pct2' },
      { grade: 7, topicId: 'discount' },
      { grade: 6, topicId: 'partnership' },
    ],
    exampleTopic: 'percentage',
  },
  CN_030: { // Simple Interest
    practiceLinks: [
      { grade: 7, topicId: 'grade7', subTopicKey: 'percentage' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'ratio' },
    ],
    flashcardLinks: [
      { grade: 5, topicId: 'si' },
      { grade: 6, topicId: 'si6' },
      { grade: 7, topicId: 'ci' },
    ],
    exampleTopic: 'percentage',
  },
  CN_031: { // Compound Interest
    practiceLinks: [
      { grade: 8, topicId: 'grade8', subTopicKey: 'ratio' },
    ],
    flashcardLinks: [
      { grade: 7, topicId: 'ci' },
      { grade: 8, topicId: 'ci8' },
    ],
    exampleTopic: 'percentage',
  },

  // ─── ratio domain ──────────────────────────────────────────────────────────
  CN_032: { // Ratio Basics
    practiceLinks: [
      { grade: 4, topicId: 'ch07-08' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'fraction' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'ratio' },
    ],
    exampleTopic: 'ratio',
  },
  CN_033: { // Dividing in a Ratio
    practiceLinks: [
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'fraction' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'ratio' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'ratio' },
    ],
    exampleTopic: 'ratio',
  },
  CN_034: { // Proportion
    practiceLinks: [
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'fraction' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'ratio' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'ratio' },
    ],
    exampleTopic: 'ratio',
  },
  CN_035: { // Direct & Inverse Variation
    practiceLinks: [
      { grade: 6, topicId: 'grade6', subTopicKey: 'algebra' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'ratio' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'ratio' },
    ],
    flashcardLinks: [
      { grade: 8, topicId: 'variation' },
    ],
    exampleTopic: 'ratio',
  },
  CN_036: { // Unitary Method
    practiceLinks: [
      { grade: 3, topicId: 'grade3', subTopicKey: 'multiplication' },
      { grade: 4, topicId: 'ch09-10' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'percentage' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'percentage' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'ratio' },
    ],
    exampleTopic: 'ratio',
  },

  // ─── algebra domain ────────────────────────────────────────────────────────
  CN_037: { // Variables & Expressions
    practiceLinks: [
      { grade: 4, topicId: 'ch13' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'algebra' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'algebra' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'algebra' },
      { grade: 5, topicId: 'alg' },
      { grade: 6, topicId: 'alg6' },
    ],
    exampleTopic: 'algebra',
  },
  CN_038: { // Like Terms & Simplification
    practiceLinks: [
      { grade: 5, topicId: 'grade5', subTopicKey: 'algebra' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'algebra' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'algebra' },
    ],
    flashcardLinks: [
      { grade: 5, topicId: 'alg' },
      { grade: 6, topicId: 'alg6' },
      { grade: 8, topicId: 'algexp' },
    ],
    exampleTopic: 'algebra',
  },
  CN_039: { // One-Step Equations
    practiceLinks: [
      { grade: 3, topicId: 'grade3', subTopicKey: 'number' },
      { grade: 4, topicId: 'ch14' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'algebra' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'algebra' },
      { grade: 5, topicId: 'alg' },
    ],
    exampleTopic: 'algebra',
  },
  CN_040: { // Two-Step Equations
    practiceLinks: [
      { grade: 4, topicId: 'ch14' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'algebra' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'algebra' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'algebra' },
      { grade: 5, topicId: 'alg' },
      { grade: 6, topicId: 'alg6' },
    ],
    exampleTopic: 'algebra',
  },
  CN_041: { // Equations — Variables Both Sides
    practiceLinks: [
      { grade: 5, topicId: 'grade5', subTopicKey: 'algebra' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'algebra' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'algebra' },
    ],
    flashcardLinks: [
      { grade: 5, topicId: 'alg' },
      { grade: 6, topicId: 'alg6' },
      { grade: 7, topicId: 'lineq7' },
    ],
    exampleTopic: 'algebra',
  },
  CN_042: { // Equations with Brackets
    practiceLinks: [
      { grade: 6, topicId: 'grade6', subTopicKey: 'algebra' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'algebra' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'linear' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'alg6' },
      { grade: 7, topicId: 'lineq7' },
      { grade: 8, topicId: 'lineq' },
    ],
    exampleTopic: 'algebra',
  },
  CN_043: { // Fraction Equations
    practiceLinks: [
      { grade: 7, topicId: 'grade7', subTopicKey: 'algebra' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'linear' },
      { grade: 9, topicId: 'grade9', subTopicKey: 'polynomial' },
    ],
    flashcardLinks: [
      { grade: 7, topicId: 'lineq7' },
      { grade: 8, topicId: 'lineq' },
    ],
    exampleTopic: 'algebra',
  },
  CN_044: { // Polynomials
    practiceLinks: [
      { grade: 8, topicId: 'grade8', subTopicKey: 'polynomial' },
      { grade: 9, topicId: 'grade9', subTopicKey: 'polynomial' },
    ],
    flashcardLinks: [
      { grade: 8, topicId: 'poly' },
      { grade: 9, topicId: 'poly9' },
    ],
    exampleTopic: 'algebra',
  },
  CN_045: { // Algebraic Identities
    practiceLinks: [
      { grade: 8, topicId: 'grade8', subTopicKey: 'polynomial' },
      { grade: 9, topicId: 'grade9', subTopicKey: 'polynomial' },
    ],
    flashcardLinks: [
      { grade: 7, topicId: 'identity' },
      { grade: 8, topicId: 'poly' },
      { grade: 9, topicId: 'poly9' },
    ],
    exampleTopic: 'algebra',
  },
  CN_046: { // Quadratic Equations
    practiceLinks: [
      { grade: 8, topicId: 'grade8', subTopicKey: 'polynomial' },
      { grade: 9, topicId: 'grade9', subTopicKey: 'polynomial' },
    ],
    flashcardLinks: [
      { grade: 8, topicId: 'quad' },
    ],
    exampleTopic: 'algebra',
  },

  // ─── geometry domain ───────────────────────────────────────────────────────
  CN_047: { // 2D Shapes
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'shape' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'shape' },
      { grade: 4, topicId: 'ch20' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'shapes' },
      { grade: 3, topicId: 'geo' },
      { grade: 4, topicId: 'quadrilaterals' },
    ],
    exampleTopic: 'geometry',
  },
  CN_048: { // 3D Shapes
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'shape' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'shape' },
      { grade: 4, topicId: 'ch20' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'shapes' },
      { grade: 3, topicId: 'geo' },
    ],
    exampleTopic: 'geometry',
  },
  CN_049: { // Types of Angles
    practiceLinks: [
      { grade: 3, topicId: 'grade3', subTopicKey: 'shape' },
      { grade: 4, topicId: 'ch18' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'angle' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'angles' },
      { grade: 5, topicId: 'geo' },
    ],
    exampleTopic: 'geometry',
  },
  CN_050: { // Complementary & Supplementary
    practiceLinks: [
      { grade: 4, topicId: 'ch18' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'angle' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'geometry' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'angles' },
      { grade: 5, topicId: 'geo' },
      { grade: 6, topicId: 'geo' },
    ],
    exampleTopic: 'geometry',
  },
  CN_051: { // Triangle Properties
    practiceLinks: [
      { grade: 4, topicId: 'ch19' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'angle' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'geometry' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'triangle' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'triangles' },
      { grade: 7, topicId: 'congruence' },
    ],
    exampleTopic: 'geometry',
  },
  CN_052: { // Parallel Lines & Transversal
    practiceLinks: [
      { grade: 6, topicId: 'grade6', subTopicKey: 'geometry' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'triangle' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'quadrilateral' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'geo' },
      { grade: 7, topicId: 'congruence' },
    ],
    exampleTopic: 'geometry',
  },
  CN_053: { // Polygon Angles
    practiceLinks: [
      { grade: 6, topicId: 'grade6', subTopicKey: 'geometry' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'triangle' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'quadrilateral' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'geo' },
      { grade: 8, topicId: 'quad8' },
    ],
    exampleTopic: 'geometry',
  },
  CN_054: { // Congruence & Similarity
    practiceLinks: [
      { grade: 8, topicId: 'grade8', subTopicKey: 'quadrilateral' },
    ],
    flashcardLinks: [
      { grade: 7, topicId: 'congruence' },
      { grade: 8, topicId: 'sim' },
    ],
    exampleTopic: 'geometry',
  },
  CN_055: { // Pythagoras Theorem
    practiceLinks: [
      { grade: 7, topicId: 'grade7', subTopicKey: 'area' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'mensuration' },
    ],
    flashcardLinks: [
      { grade: 7, topicId: 'pyth' },
    ],
    exampleTopic: 'geometry',
  },
  CN_056: { // Circle — Basics
    practiceLinks: [
      { grade: 4, topicId: 'ch21' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'area' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'geometry' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'circles' },
      { grade: 6, topicId: 'circ6' },
    ],
    exampleTopic: 'geometry',
  },
  CN_057: { // Circle — Advanced
    practiceLinks: [
      { grade: 8, topicId: 'grade8', subTopicKey: 'mensuration' },
    ],
    flashcardLinks: [
      { grade: 8, topicId: 'circ8' },
    ],
    exampleTopic: 'geometry',
  },
  CN_058: { // Symmetry
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'shape' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'shape' },
      { grade: 4, topicId: 'ch20' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'shapes' },
      { grade: 3, topicId: 'geo' },
    ],
    exampleTopic: 'geometry',
  },

  // ─── mensuration domain ────────────────────────────────────────────────────
  CN_059: { // Perimeter
    practiceLinks: [
      { grade: 3, topicId: 'grade3', subTopicKey: 'shape' },
      { grade: 4, topicId: 'ch20' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'area' },
    ],
    flashcardLinks: [
      { grade: 3, topicId: 'meas' },
      { grade: 5, topicId: 'geo' },
    ],
    exampleTopic: 'mensuration',
  },
  CN_060: { // Area — Basic Shapes
    practiceLinks: [
      { grade: 4, topicId: 'ch20' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'area' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'geometry' },
    ],
    flashcardLinks: [
      { grade: 5, topicId: 'geo' },
      { grade: 6, topicId: 'geo' },
      { grade: 7, topicId: 'mens' },
    ],
    exampleTopic: 'mensuration',
  },
  CN_061: { // Area — Advanced Shapes
    practiceLinks: [
      { grade: 6, topicId: 'grade6', subTopicKey: 'geometry' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'area' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'mensuration' },
    ],
    flashcardLinks: [
      { grade: 7, topicId: 'mens' },
    ],
    exampleTopic: 'mensuration',
  },
  CN_062: { // Surface Area
    practiceLinks: [
      { grade: 8, topicId: 'grade8', subTopicKey: 'mensuration' },
      { grade: 9, topicId: 'grade9', subTopicKey: 'surface' },
    ],
    flashcardLinks: [
      { grade: 8, topicId: 'mens3d' },
    ],
    exampleTopic: 'mensuration',
  },
  CN_063: { // Volume
    practiceLinks: [
      { grade: 8, topicId: 'grade8', subTopicKey: 'mensuration' },
      { grade: 9, topicId: 'grade9', subTopicKey: 'surface' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'vol' },
      { grade: 8, topicId: 'mens3d' },
    ],
    exampleTopic: 'mensuration',
  },

  // ─── speed domain ──────────────────────────────────────────────────────────
  CN_064: { // Speed-Distance-Time Basics
    practiceLinks: [
      { grade: 4, topicId: 'ch17' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'decimal' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'percentage' },
    ],
    flashcardLinks: [
      { grade: 5, topicId: 'speed' },
      { grade: 6, topicId: 'sdt6' },
    ],
    exampleTopic: 'speed_distance',
  },
  CN_065: { // Speed Unit Conversion
    practiceLinks: [
      { grade: 5, topicId: 'grade5', subTopicKey: 'decimal' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'percentage' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'ratio' },
    ],
    flashcardLinks: [
      { grade: 5, topicId: 'speed' },
      { grade: 6, topicId: 'sdt6' },
    ],
    exampleTopic: 'speed_distance',
  },
  CN_066: { // Average Speed
    practiceLinks: [
      { grade: 6, topicId: 'grade6', subTopicKey: 'percentage' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'ratio' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'ratio' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'sdt6' },
    ],
    exampleTopic: 'speed_distance',
  },
  CN_067: { // Train Problems
    practiceLinks: [
      { grade: 7, topicId: 'grade7', subTopicKey: 'ratio' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'ratio' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'sdt6' },
    ],
    exampleTopic: 'speed_distance',
  },
  CN_068: { // Work & Time
    practiceLinks: [
      { grade: 7, topicId: 'grade7', subTopicKey: 'ratio' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'ratio' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'work' },
    ],
    exampleTopic: 'speed_distance',
  },

  // ─── statistics domain ─────────────────────────────────────────────────────
  CN_069: { // Average (Mean)
    practiceLinks: [
      { grade: 4, topicId: 'dh' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'decimal' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'integer' },
    ],
    flashcardLinks: [
      { grade: 6, topicId: 'data' },
      { grade: 7, topicId: 'data7' },
    ],
    exampleTopic: 'average',
  },
  CN_070: { // Median, Mode, Range
    practiceLinks: [
      { grade: 6, topicId: 'grade6', subTopicKey: 'integer' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'algebra' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'ratio' },
    ],
    flashcardLinks: [
      { grade: 7, topicId: 'data7' },
      { grade: 9, topicId: 'stats' },
    ],
    exampleTopic: 'average',
  },
  CN_071: { // Data Interpretation
    practiceLinks: [
      { grade: 4, topicId: 'dh' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'decimal' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'integer' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'data' },
      { grade: 3, topicId: 'data' },
      { grade: 6, topicId: 'data' },
      { grade: 7, topicId: 'data7' },
    ],
    exampleTopic: 'data',
  },

  // ─── squares domain ────────────────────────────────────────────────────────
  CN_072: { // Squares & Perfect Squares
    practiceLinks: [
      { grade: 4, topicId: 'ch06' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'integer' },
    ],
    flashcardLinks: [
      { grade: 7, topicId: 'squares' },
    ],
    exampleTopic: 'squares',
  },
  CN_073: { // Square Roots
    practiceLinks: [
      { grade: 5, topicId: 'grade5', subTopicKey: 'fraction' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'integer' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'algebra' },
    ],
    flashcardLinks: [
      { grade: 7, topicId: 'squares' },
    ],
    exampleTopic: 'squares',
  },
  CN_074: { // Cubes & Cube Roots
    practiceLinks: [
      { grade: 7, topicId: 'grade7', subTopicKey: 'algebra' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'polynomial' },
    ],
    flashcardLinks: [
      { grade: 7, topicId: 'squares' },
      { grade: 7, topicId: 'exp' },
    ],
    exampleTopic: 'squares',
  },
  CN_075: { // Laws of Indices
    practiceLinks: [
      { grade: 7, topicId: 'grade7', subTopicKey: 'algebra' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'polynomial' },
      { grade: 9, topicId: 'grade9', subTopicKey: 'number' },
    ],
    flashcardLinks: [
      { grade: 7, topicId: 'exp' },
    ],
    exampleTopic: 'squares',
  },
  CN_076: { // Surds
    practiceLinks: [
      { grade: 9, topicId: 'grade9', subTopicKey: 'number' },
    ],
    flashcardLinks: [
      { grade: 7, topicId: 'exp' },
    ],
    exampleTopic: 'squares',
  },

  // ─── patterns domain ───────────────────────────────────────────────────────
  CN_077: { // Simple Patterns
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'number' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'number' },
      { grade: 4, topicId: 'ch16' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'pattern' },
      { grade: 4, topicId: 'sequences' },
    ],
    exampleTopic: 'patterns',
  },
  CN_078: { // Arithmetic Progression
    practiceLinks: [
      { grade: 4, topicId: 'ch16' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'algebra' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'algebra' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'sequences' },
    ],
    exampleTopic: 'patterns',
  },
  CN_079: { // Geometric Progression
    practiceLinks: [
      { grade: 7, topicId: 'grade7', subTopicKey: 'algebra' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'polynomial' },
    ],
    flashcardLinks: [
      { grade: 7, topicId: 'exp' },
    ],
    exampleTopic: 'patterns',
  },
  CN_080: { // Special Sequences
    practiceLinks: [
      { grade: 7, topicId: 'grade7', subTopicKey: 'algebra' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'polynomial' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'sequences' },
      { grade: 7, topicId: 'squares' },
    ],
    exampleTopic: 'patterns',
  },

  // ─── practical domain ──────────────────────────────────────────────────────
  CN_081: { // Money & Transactions
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'addition' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'multiplication' },
      { grade: 4, topicId: 'ch11' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'money' },
    ],
    exampleTopic: 'money',
  },
  CN_082: { // Measurement & Units
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'shape' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'shape' },
      { grade: 4, topicId: 'ch12' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'meas' },
      { grade: 3, topicId: 'meas' },
      { grade: 4, topicId: 'measurement' },
    ],
    exampleTopic: 'measurement',
  },
  CN_083: { // Time & Calendar
    practiceLinks: [
      { grade: 2, topicId: 'grade2', subTopicKey: 'number' },
      { grade: 3, topicId: 'grade3', subTopicKey: 'number' },
      { grade: 4, topicId: 'ch17' },
    ],
    flashcardLinks: [
      { grade: 2, topicId: 'time' },
      { grade: 3, topicId: 'time' },
      { grade: 4, topicId: 'time_calendar' },
    ],
    exampleTopic: 'time_calendar',
  },
  CN_084: { // Age Problems
    practiceLinks: [
      { grade: 3, topicId: 'grade3', subTopicKey: 'number' },
      { grade: 4, topicId: 'ch14' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'algebra' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'algebra' },
    ],
    flashcardLinks: [
      { grade: 5, topicId: 'alg' },
      { grade: 6, topicId: 'alg6' },
    ],
    exampleTopic: 'age',
  },
  CN_085: { // Sets & Venn Diagrams
    practiceLinks: [
      { grade: 6, topicId: 'grade6', subTopicKey: 'integer' },
      { grade: 7, topicId: 'grade7', subTopicKey: 'algebra' },
      { grade: 8, topicId: 'grade8', subTopicKey: 'polynomial' },
    ],
    flashcardLinks: [
      { grade: 8, topicId: 'sets' },
    ],
    exampleTopic: 'sets',
  },
  CN_086: { // Counting & Combinatorics
    practiceLinks: [
      { grade: 4, topicId: 'ch15' },
      { grade: 5, topicId: 'grade5', subTopicKey: 'algebra' },
      { grade: 6, topicId: 'grade6', subTopicKey: 'algebra' },
    ],
    flashcardLinks: [
      { grade: 4, topicId: 'magic_squares' },
      { grade: 2, topicId: 'logic' },
    ],
    exampleTopic: 'counting',
  },

  // ─── advanced domain ───────────────────────────────────────────────────────
  CN_087: { // Logarithms
    practiceLinks: [
      { grade: 9, topicId: 'grade9', subTopicKey: 'number' },
    ],
    flashcardLinks: [
      { grade: 9, topicId: 'log' },
    ],
    exampleTopic: null,
  },
  CN_088: { // Trigonometry
    practiceLinks: [
      { grade: 9, topicId: 'grade9', subTopicKey: 'number' },
    ],
    flashcardLinks: [
      { grade: 9, topicId: 'trig' },
    ],
    exampleTopic: null,
  },
};

// ── Resolver ─────────────────────────────────────────────────────────────────

export interface ResolvedLinks {
  practice: { url: string; topicId: string; subTopicKey?: string; label: string } | null;
  flashcard: { url: string; topicId: string; grade: number; label: string } | null;
  example: { url: string; label: string } | null;
}

/** Resolve concept → URLs for a specific student grade. Exact match first, then closest (prefer lower). */
export function resolveLinksForGrade(conceptId: string, studentGrade: number): ResolvedLinks {
  const mapping = CONCEPT_TOPIC_MAP[conceptId];
  if (!mapping) return { practice: null, flashcard: null, example: null };

  // Helper: pick best link by grade — exact match first, else closest (prefer lower grade)
  function pickBest<T extends { grade: number }>(links: T[]): T | null {
    if (links.length === 0) return null;
    const exact = links.find((l) => l.grade === studentGrade);
    if (exact) return exact;
    // Sort by distance to studentGrade, tiebreak by preferring lower grade
    const sorted = [...links].sort((a, b) => {
      const da = Math.abs(a.grade - studentGrade);
      const db = Math.abs(b.grade - studentGrade);
      if (da !== db) return da - db;
      return a.grade - b.grade; // prefer lower
    });
    return sorted[0];
  }

  // Concept tracking params — appended so activity pages can return to the concept
  const conceptParams = `from=concept&conceptId=${conceptId}`;

  // Practice
  const pLink = pickBest(mapping.practiceLinks);
  const practice = pLink
    ? {
        url: `/practice/${pLink.topicId}?${pLink.subTopicKey ? `subTopic=${pLink.subTopicKey}&` : ''}${conceptParams}`,
        topicId: pLink.topicId,
        subTopicKey: pLink.subTopicKey,
        label: pLink.topicId,
      }
    : null;

  // Flashcard
  const fLink = pickBest(mapping.flashcardLinks);
  const flashcard = fLink
    ? {
        url: `/flashcards/session?deck=${encodeURIComponent(fLink.topicId)}&mode=classic&grade=${fLink.grade}&${conceptParams}`,
        topicId: fLink.topicId,
        grade: fLink.grade,
        label: fLink.topicId,
      }
    : null;

  // Worked examples
  const example = mapping.exampleTopic
    ? {
        url: `/learn/examples?topic=${encodeURIComponent(mapping.exampleTopic)}&grade=${studentGrade}&${conceptParams}`,
        label: mapping.exampleTopic.replace(/_/g, ' '),
      }
    : null;

  return { practice, flashcard, example };
}
