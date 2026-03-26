/** Test student profiles — mirrors /dev page student registry. */
export interface TestStudent {
  id: string;
  name: string;
  grade: number;
  tier: number; // 0=Free, 1=Starter, 2=Advanced, 3=Unlimited
}

/** Default student for most tests — Grade 4, Unlimited tier, good data coverage. */
export const DEFAULT_STUDENT: TestStudent = {
  id: 'student_001',
  name: 'Aarav Sharma',
  grade: 4,
  tier: 3,
};

/** Free-tier student for paywall / limit tests. */
export const FREE_STUDENT: TestStudent = {
  id: 'student_test_gr2',
  name: 'Aarav',
  grade: 2,
  tier: 0,
};

/** Full registry of dev-page students. */
export const TEST_STUDENTS: Record<string, TestStudent> = {
  student_001:      { id: 'student_001',      name: 'Aarav Sharma',  grade: 4, tier: 3 },
  student_002:      { id: 'student_002',      name: 'Ananya Sharma', grade: 4, tier: 3 },
  student_003:      { id: 'student_003',      name: 'Vivaan Mehta',  grade: 4, tier: 2 },
  student_test_gr2: { id: 'student_test_gr2', name: 'Aarav',         grade: 2, tier: 0 },
  student_test_gr5: { id: 'student_test_gr5', name: 'Sneha',         grade: 5, tier: 3 },
  student_test_gr8: { id: 'student_test_gr8', name: 'Dhruv',         grade: 8, tier: 2 },
  student_test_gr9: { id: 'student_test_gr9', name: 'Ananya',        grade: 9, tier: 3 },
};
