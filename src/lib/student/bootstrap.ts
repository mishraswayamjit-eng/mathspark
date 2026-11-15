// SERVER ONLY: talks to the database. Never import this from a client component
// (import the type from '@/lib/student/types' instead).

import { prisma } from '@/lib/db';
import type { StudentBootstrap } from '@/lib/student/types';

export type { StudentBootstrap } from '@/lib/student/types';

/**
 * The small student payload the app shell shows on every page.
 * One indexed primary-key read. Returns null when the student does not exist.
 */
export async function loadStudentBootstrap(studentId: string): Promise<StudentBootstrap | null> {
  const student = await prisma.student.findUnique({
    where: { id: studentId },
    select: {
      id: true,
      name: true,
      grade: true,
      avatarColor: true,
      totalLifetimeXP: true,
      currentLeagueTier: true,
    },
  });
  if (!student) return null;

  return {
    id: student.id,
    name: student.name,
    grade: student.grade,
    avatarColor: student.avatarColor,
    totalXP: student.totalLifetimeXP ?? 0,
    leagueTier: student.currentLeagueTier ?? 1,
  };
}
