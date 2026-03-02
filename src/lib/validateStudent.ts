import { getServerSession } from 'next-auth';
import { authOptions } from './auth';
import { prisma } from './db';

/**
 * Validate that a studentId is legitimate before processing a mutation.
 *
 * Rules:
 *  - The student must exist in the DB (prevents random-ID injection).
 *  - If a parent session is active, the student must belong to that parent.
 *    (Children accessing the app directly have no server session — that's expected.)
 *
 * Returns null on success, or an error string if access should be denied.
 */
export async function validateStudentAccess(studentId: string): Promise<string | null> {
  if (!studentId || typeof studentId !== 'string') return 'Invalid studentId';

  const student = await prisma.student.findUnique({
    where:  { id: studentId },
    select: { id: true, parentId: true },
  });

  if (!student) return 'Student not found';

  // If a parent is logged in via NextAuth, verify ownership.
  const session = await getServerSession(authOptions);
  if (session?.user?.id && student.parentId && student.parentId !== session.user.id) {
    return 'Forbidden';
  }

  return null; // access granted
}
