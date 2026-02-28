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
    } else {
      setError('Incorrect email or password. Please try again.');
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#131F24] flex flex-col items-center justify-center px-6 py-12">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">⚡</div>
          <h1 className="text-2xl font-extrabold text-white">Parent sign in</h1>
          <p className="text-white/50 text-sm mt-1">Welcome back to MathSpark</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email" placeholder="Email address" required autoComplete="email"
            value={email} onChange={(e) => setEmail(e.target.value)}
            className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-[#1CB0F6]"
          />
          <input
            type="password" placeholder="Password" required autoComplete="current-password"
            value={password} onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-[#1CB0F6]"
          />

          {error && <p className="text-[#FF4B4B] text-sm text-center font-semibold">{error}</p>}

          <button
            type="submit" disabled={loading}
            className="w-full bg-[#1CB0F6] hover:bg-[#0a98dc] disabled:opacity-50 text-white font-extrabold py-4 rounded-2xl text-lg transition-colors"
          >
            {loading ? 'Signing in…' : 'Sign In →'}
          </button>
        </form>

        <p className="text-center mt-4">
          <Link href="/auth/forgot-password" className="text-white/40 text-sm hover:text-white/70 transition-colors">
            Forgot your password?
          </Link>
        </p>

        <p className="text-center text-white/40 text-sm mt-6">
          Don't have an account?{' '}
          <Link href="/auth/register" className="text-[#58CC02] font-semibold hover:underline">
            Create one free
          </Link>
        </p>

        <div className="mt-8 border-t border-white/10 pt-6">
          <p className="text-center text-white/30 text-xs mb-3">Is your child logging in?</p>
          <Link
            href="/student/login"
            className="block w-full text-center bg-white/5 border border-white/10 rounded-xl py-3 text-white/60 text-sm font-semibold hover:bg-white/10 transition-colors"
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
    <Suspense fallback={<div className="min-h-screen bg-[#131F24]" />}>
      <LoginForm />
    </Suspense>
  );
}
