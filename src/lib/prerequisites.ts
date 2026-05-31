// Soft prerequisite map: topicId → prerequisite topicId(s)
// Meaning: "to get the most out of this topic, finish these first"
export const PREREQUISITES: Record<string, string[]> = {
  'ch07-08': ['ch01-05'],           // Fractions → Number System
  'ch09-10': ['ch01-05', 'ch06'],   // BODMAS → Numbers + Factors
  'ch11':    ['ch07-08'],            // Decimals → Fractions
  'ch12':    ['ch11'],               // Decimal Units → Decimals
  'ch13':    ['ch09-10'],            // Algebra → BODMAS
  'ch14':    ['ch13'],               // Equations → Algebra
  'ch15':    ['ch09-10'],            // Puzzles → BODMAS
  'ch16':    ['ch09-10'],            // Sequences → BODMAS
  'ch19':    ['ch18'],               // Triangles → Angles
  'ch20':    ['ch18'],               // Quadrilaterals → Angles
  'ch21':    ['ch18'],               // Circle → Angles
};

export function getUnmetPrerequisites(
  topicId: string,
  masteryMap: Record<string, string>, // topicId → mastery level
): string[] {
  const prereqs = PREREQUISITES[topicId] ?? [];
  return prereqs.filter((p) => {
    const m = masteryMap[p];
    return !m || m === 'NotStarted';
  });
}
