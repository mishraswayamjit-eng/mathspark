import { withAuth } from 'next-auth/middleware';

// Protect /parent/* routes — requires an active parent session.
// All existing student routes (/chapters, /practice, etc.) remain unprotected.
export default withAuth({
  pages: {
    signIn: '/auth/login',
  },
});

export const config = {
  matcher: ['/parent/:path*'],
};
