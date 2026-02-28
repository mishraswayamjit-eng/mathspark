'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function ForgotPasswordPage() {
  const [email,   setEmail]   = useState('');
  const [loading, setLoading] = useState(false);
  const [sent,    setSent]    = useState(false);
  const [error,   setError]   = useState('');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res  = await fetch('/api/auth/forgot-password', {
        method:  'POST',
        headers: { 'content-type': 'application/json' },
        body:    JSON.stringify({ email }),
      });
      const data = await res.json();
      if (!res.ok) { setError(data.error ?? 'Something went wrong.'); }
      else          { setSent(true); }
    } catch {
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#131F24] flex flex-col items-center justify-center px-6 py-12">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">🔑</div>
          <h1 className="text-2xl font-extrabold text-white">Reset password</h1>
          <p className="text-white/50 text-sm mt-1">We'll send you a reset link</p>
        </div>

        {sent ? (
          <div className="text-center space-y-4">
            <div className="text-4xl">📧</div>
            <p className="text-white font-semibold">Check your email!</p>
            <p className="text-white/50 text-sm">
              If an account exists for <strong className="text-white/70">{email}</strong>, you'll receive a reset link in the next few minutes.
            </p>
            <Link
              href="/auth/login"
              className="block w-full bg-[#1CB0F6] hover:bg-[#0a98dc] text-white font-extrabold py-4 rounded-2xl text-center transition-colors"
            >
              Back to Login
            </Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="email" placeholder="Your email address" required
              value={email} onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-[#1CB0F6]"
            />

            {error && <p className="text-[#FF4B4B] text-sm text-center font-semibold">{error}</p>}

            <button
              type="submit" disabled={loading}
              className="w-full bg-[#1CB0F6] hover:bg-[#0a98dc] disabled:opacity-50 text-white font-extrabold py-4 rounded-2xl text-lg transition-colors"
            >
              {loading ? 'Sending…' : 'Send Reset Link →'}
            </button>

            <p className="text-center">
              <Link href="/auth/login" className="text-white/40 text-sm hover:text-white/70 transition-colors">
                ← Back to login
              </Link>
            </p>
          </form>
        )}
      </div>
    </div>
  );
}
