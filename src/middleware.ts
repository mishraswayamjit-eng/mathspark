import { withAuth } from 'next-auth/middleware';

// Protect /parent/* routes — requires an active parent session.
// /parent/[studentId] is a public share link and is excluded.
// All existing student routes (/chapters, /practice, etc.) remain unprotected.
export default withAuth({
  pages: {
    signIn: '/auth/login',
  },
});

export const config = {
  matcher: ['/parent/dashboard', '/parent/add-child'],
};
