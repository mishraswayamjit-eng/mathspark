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
    <div className="min-h-screen bg-paper flex flex-col items-center justify-center px-6 py-12 animate-fade-in">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">🔑</div>
          <h1 className="text-2xl font-extrabold text-ink">Reset password</h1>
          <p className="text-ink-muted text-sm mt-1">We'll send you a reset link</p>
        </div>

        {sent ? (
          <div className="text-center space-y-4">
            <div className="text-4xl">📧</div>
            <p className="text-ink font-semibold">Check your email!</p>
            <p className="text-ink-muted text-sm">
              If an account exists for <strong className="text-ink">{email}</strong>, you'll receive a reset link in the next few minutes.
            </p>
            <Link
              href="/auth/login"
              className="block w-full bg-action hover:bg-action-dark text-white font-extrabold py-4 rounded-control border-2 border-ink shadow-hard-sm text-center transition-colors"
            >
              Back to Login
            </Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="email" placeholder="Your email address" required
              aria-label="Your email address"
              value={email} onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-white border-2 border-line rounded-control px-4 py-3 text-ink placeholder:text-ink-muted outline-none focus:border-action"
            />

            {error && <p className="text-retry bg-retry-soft border-2 border-retry rounded-control px-3 py-2 text-sm text-center font-semibold">{error}</p>}

            <button
              type="submit" disabled={loading}
              className="w-full bg-action hover:bg-action-dark disabled:opacity-50 text-white font-extrabold py-4 rounded-control border-2 border-ink shadow-hard-sm text-lg transition-colors"
            >
              {loading ? 'Sending…' : 'Send Reset Link →'}
            </button>

            <p className="text-center">
              <Link href="/auth/login" className="text-ink-muted text-sm hover:text-ink transition-colors">
                ← Back to login
              </Link>
            </p>
          </form>
        )}
      </div>
    </div>
  );
}
