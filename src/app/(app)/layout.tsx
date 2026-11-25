import BottomNav from '@/components/BottomNav';
import SparkyWidget from '@/components/SparkyWidget';
import ServiceWorkerRegistrar from '@/components/ServiceWorkerRegistrar';
import AddToHomeScreen from '@/components/AddToHomeScreen';
import StudentProvider from '@/components/shell/StudentProvider';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { loadStudentBootstrap } from '@/lib/student/bootstrap';
import type { StudentBootstrap } from '@/lib/student/types';
import { logError } from '@/lib/logger';

// This layout reads the child's session cookie, so everything under (app) is
// rendered per request (never prerendered or shared between children).
export const dynamic = 'force-dynamic';

export default async function AppLayout({ children }: { children: React.ReactNode }) {
  // Signed-out visitors are fine here: /start, /auth/*, /student/login, /dev and
  // others live under this layout. Never redirect from the layout.
  // The check throws when the database cannot confirm the account (see
  // studentAuth). The shell must not take the page down for that: it renders
  // without the child's data, and each page and route reports its own failure.
  let studentId: string | null = null;
  try {
    studentId = await getAuthenticatedStudentId();
  } catch (err) {
    logError('[app/layout] could not confirm the signed-in child', err);
  }

  let student: StudentBootstrap | null = null;
  if (studentId) {
    try {
      student = await loadStudentBootstrap(studentId);
    } catch (err) {
      // The shell must not take the page down. The provider refetches in the
      // background on the client when it finds a signed-in child without data.
      logError('[app/layout] student bootstrap failed', err);
    }
  }

  return (
    <StudentProvider initialStudent={student}>
      <main className="bg-paper max-w-lg mx-auto min-h-screen">
        {children}
      </main>
      <BottomNav />
      <SparkyWidget />
      <AddToHomeScreen />
      <ServiceWorkerRegistrar />
    </StudentProvider>
  );
}
