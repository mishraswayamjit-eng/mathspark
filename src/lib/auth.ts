import { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import bcrypt from 'bcryptjs';
import { prisma } from '@/lib/db';

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
          if (!parent) return null;

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
  secret: process.env.NEXTAUTH_SECRET,
};
