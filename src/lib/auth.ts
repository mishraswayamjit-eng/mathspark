import { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import bcrypt from 'bcryptjs';
import { prisma } from '@/lib/db';

/**
 * Lazy getter for NEXTAUTH_SECRET — read at request time, not module init.
 * This avoids the module-load order issue where env vars from .env aren't
 * yet attached on Vercel cold start. Throws so NextAuth surfaces a
 * "Configuration" error rather than silently signing with `undefined`.
 */
function getNextAuthSecret(): string {
  const secret = process.env.NEXTAUTH_SECRET;
  if (!secret) {
    throw new Error('NEXTAUTH_SECRET is not set — configure it in your Vercel env vars.');
  }
  return secret;
}

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email:    { label: 'Email',    type: 'email'    },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;

        try {
          const parent = await prisma.parent.findUnique({
            where: { email: credentials.email.toLowerCase().trim() },
          });
          // Treat soft-deleted accounts as if they don't exist so a deleted
          // user cannot resurrect their session by re-entering credentials.
          if (!parent || parent.deletedAt) return null;

          const valid = await bcrypt.compare(credentials.password, parent.passwordHash);
          if (!valid) return null;

          return { id: parent.id, email: parent.email, name: parent.name };
        } catch (err) {
          console.error('[authorize] DB error:', err);
          // Re-throw so NextAuth surfaces a Configuration error rather than
          // silently returning "Incorrect email or password"
          throw err;
        }
      },
    }),
  ],
  session: {
    strategy: 'jwt',
    maxAge:   7 * 24 * 60 * 60, // 7 days for parents
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) token.id = user.id;
      return token;
    },
    async session({ session, token }) {
      if (token) session.user.id = token.id as string;
      return session;
    },
  },
  pages: {
    signIn: '/auth/login',
    error:  '/auth/login',
  },
  // Lazy getter ensures we read the env var at request time, not module init time.
  get secret() {
    return getNextAuthSecret();
  },
};
