'use client';

import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { usePathname } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { logError } from '@/lib/logger';
import { PARENT_SESSION_FLAG } from '@/lib/student/types';
import type { StudentBootstrap } from '@/lib/student/types';

export type { StudentBootstrap } from '@/lib/student/types';

export interface StudentContextValue {
  /** The signed-in child, or null when nobody is signed in. */
  student: StudentBootstrap | null;
  /** Refetch in the background. Whatever is showing now stays until the answer arrives. */
  refresh: () => void;
}

const StudentContext = createContext<StudentContextValue>({
  student: null,
  refresh: () => undefined,
});

/** The signed-in child for the app shell. Safe to call outside the provider (student is null). */
export function useStudent(): StudentContextValue {
  return useContext(StudentContext);
}

export default function StudentProvider({
  initialStudent,
  children,
}: {
  initialStudent: StudentBootstrap | null;
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const { status } = useSession();
  const [student, setStudent] = useState<StudentBootstrap | null>(initialStudent);
  const inFlight = useRef(false);
  const lastAutoTry = useRef('');

  // The server sends a fresh payload whenever the layout renders again
  // (full page load or router.refresh()).
  useEffect(() => {
    setStudent(initialStudent);
  }, [initialStudent]);

  const refresh = useCallback(() => {
    if (inFlight.current) return;
    inFlight.current = true;
    fetch('/api/home?shell=1', { cache: 'no-store' })
      .then((r) => {
        // Signed out (or the account is gone): stop showing a child.
        if (r.status === 401 || r.status === 404) {
          setStudent(null);
          return null;
        }
        // Anything else that is not OK: keep what we have.
        if (!r.ok) return null;
        return r.json() as Promise<{ student?: StudentBootstrap }>;
      })
      .then((body) => {
        if (body && body.student) setStudent(body.student);
      })
      .catch((err) => {
        // Offline or a server hiccup: keep showing the current data.
        logError('[StudentProvider] refresh', err);
      })
      .then(() => {
        inFlight.current = false;
      });
  }, []);

  // The layout does not render again on in-app navigation, so after a child
  // signs in (onboarding, login, a parent choosing a child) the server payload
  // above is out of date. Those flows store the child's id in localStorage and
  // then navigate; when that id is not the child we are showing, refetch once.
  useEffect(() => {
    let storedId: string | null = null;
    try { storedId = localStorage.getItem('mathspark_student_id'); } catch { /* storage unavailable */ }
    if (!storedId) return;
    if (student && student.id === storedId) return;
    const attempt = `${storedId}|${pathname}`;
    if (lastAutoTry.current === attempt) return;
    lastAutoTry.current = attempt;
    refresh();
  }, [pathname, student, refresh]);

  // Remember whether a parent is signed in on this device, so the landing page
  // knows when it must wait for the parent session before redirecting.
  useEffect(() => {
    try {
      if (status === 'authenticated') localStorage.setItem(PARENT_SESSION_FLAG, '1');
      else if (status === 'unauthenticated') localStorage.removeItem(PARENT_SESSION_FLAG);
    } catch { /* storage unavailable */ }
  }, [status]);

  const value = useMemo<StudentContextValue>(() => ({ student, refresh }), [student, refresh]);

  return <StudentContext.Provider value={value}>{children}</StudentContext.Provider>;
}
