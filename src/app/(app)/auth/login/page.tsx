'use client';

import { useState } from 'react';
import { signIn } from 'next-auth/react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { Suspense } from 'react';

function LoginForm() {
  const router       = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl  = searchParams.get('callbackUrl') ?? '/parent/dashboard';

  const [email,    setEmail]    = useState('');
  const [password, setPassword] = useState('');
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState('');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await signIn('credentials', {
      email:    email.toLowerCase().trim(),
      password,
      redirect: false,
    });

    if (result?.ok) {
      router.push(callbackUrl);
    } else if (result?.error === 'Configuration') {
      setError('Server configuration error — NEXTAUTH_SECRET or NEXTAUTH_URL may not be set in Vercel env vars.');
      setLoading(false);
    } else {
      setError("That email or password doesn't match. Please try again.");
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-paper flex flex-col items-center justify-center px-6 py-12 animate-fade-in">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">⚡</div>
          <h1 className="text-2xl font-extrabold text-ink">Parent sign in</h1>
          <p className="text-ink-muted text-sm mt-1">Welcome back to MathSpark</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email" placeholder="Email address" required autoComplete="email"
            aria-label="Email address"
            value={email} onChange={(e) => setEmail(e.target.value)}
            className="w-full bg-white border-2 border-line rounded-control px-4 py-3 text-ink placeholder:text-ink-muted outline-none focus:border-action focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2 focus-visible:ring-offset-canvas"
          />
          <input
            type="password" placeholder="Password" required autoComplete="current-password"
            aria-label="Password"
            value={password} onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-white border-2 border-line rounded-control px-4 py-3 text-ink placeholder:text-ink-muted outline-none focus:border-action focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2 focus-visible:ring-offset-canvas"
          />

          {error && <p className="text-retry bg-retry-soft border-2 border-retry rounded-control px-3 py-2 text-sm text-center font-semibold">{error}</p>}

          <button
            type="submit" disabled={loading}
            className="w-full bg-action hover:bg-action-dark disabled:opacity-50 text-white font-extrabold py-4 rounded-control border-2 border-ink shadow-hard-sm text-lg transition-colors"
          >
            {loading ? 'Signing in…' : 'Sign In →'}
          </button>
        </form>

        <p className="text-center mt-4">
          <Link href="/auth/forgot-password" className="text-ink-muted text-sm hover:text-ink transition-colors">
            Forgot your password?
          </Link>
        </p>

        <p className="text-center text-ink-muted text-sm mt-6">
          Don't have an account?{' '}
          <Link href="/auth/register" className="text-action font-semibold hover:underline">
            Create one free
          </Link>
        </p>

        <div className="mt-8 border-t-2 border-line pt-6">
          <p className="text-center text-ink-muted text-xs mb-3">Is your child logging in?</p>
          <Link
            href="/student/login"
            className="block w-full text-center bg-white border-2 border-ink shadow-hard-sm rounded-control py-3 text-ink text-sm font-semibold hover:bg-soft transition-colors"
          >
            Student login →
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-paper" />}>
      <LoginForm />
    </Suspense>
  );
}
