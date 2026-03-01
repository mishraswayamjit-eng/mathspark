// Grade access rules for multi-grade system.
// tier: 0 = free, 1 = Starter, 2 = Advanced, 3 = Unlimited

export function getAccessibleGrades(
  studentGrade: number,
  tier: number,
): { fullAccess: number[]; sampleOnly: number[] } {
  const below = Array.from({ length: studentGrade - 2 }, (_, i) => i + 2); // 2..studentGrade-1

  if (!tier || tier === 0) {
    return { fullAccess: [studentGrade, ...below], sampleOnly: [] };
  }
  if (tier === 1) {
    const above = studentGrade < 9 ? [studentGrade + 1] : [];
    return { fullAccess: [studentGrade, ...below], sampleOnly: above };
  }
  if (tier === 2) {
    const above = [1, 2].map((d) => studentGrade + d).filter((g) => g <= 9);
    return { fullAccess: [studentGrade, ...below, ...above], sampleOnly: [] };
  }
  // Unlimited
  return { fullAccess: [2, 3, 4, 5, 6, 7, 8, 9], sampleOnly: [] };
}

export function isGradeAccessible(
  target: number,
  studentGrade: number,
  tier: number,
): { full: boolean; sample: boolean; locked: boolean } {
  const { fullAccess, sampleOnly } = getAccessibleGrades(studentGrade, tier);
  return {
    full:   fullAccess.includes(target),
    sample: sampleOnly.includes(target),
    locked: !fullAccess.includes(target) && !sampleOnly.includes(target),
  };
}

/** Derive the grade from a topicId: gradeN → N; ch-series/dh → 4 */
export function getTopicGrade(topicId: string): number {
  const m = topicId.match(/^grade(\d)$/);
  return m ? parseInt(m[1], 10) : 4;
}
