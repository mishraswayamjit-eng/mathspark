'use client';

import { useEffect, useState } from 'react';
import { useStudent } from '@/components/shell/StudentProvider';

/**
 * The signed-in child's grade, for pages that show grade-specific content.
 *
 * The grade comes from the student the app shell loaded on the server, so it
 * is known in the first paint. The grade stored on the device
 * (`mathspark_student_grade`) is only a fallback for the moment after sign-in,
 * before the shell has caught up; it can be missing or left over from another
 * child, so it is never preferred.
 *
 * Returns null until the grade is known (one render at most, and only when the
 * shell has no student yet). Callers show their loading state meanwhile, so a
 * list for the wrong grade is never shown first.
 */

const GRADE_KEY = 'mathspark_student_grade';
const DEFAULT_GRADE = 4;

function validGrade(grade: number | null | undefined): number | null {
  return typeof grade === 'number' && grade >= 2 && grade <= 9 ? Math.floor(grade) : null;
}

/** The grade stored on this device, or null when there is none (or storage is unavailable). */
export function storedStudentGrade(): number | null {
  try {
    return validGrade(Number(localStorage.getItem(GRADE_KEY)));
  } catch {
    return null;
  }
}

export function useStudentGrade(): number | null {
  const { student } = useStudent();
  const [stored, setStored] = useState<number | null>(null);
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    setStored(storedStudentGrade());
    setChecked(true);
  }, []);

  const fromStudent = validGrade(student ? student.grade : null);
  if (fromStudent !== null) return fromStudent;
  if (!checked) return null;
  return stored !== null ? stored : DEFAULT_GRADE;
}
