'use client';

import { useState, Suspense } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';

function ResetForm() {
  const router       = useRouter();
  const searchParams = useSearchParams();
  const token        = searchParams.get('token') ?? '';

  const [password,  setPassword]  = useState('');
  const [confirm,   setConfirm]   = useState('');
  const [loading,   setLoading]   = useState(false);
  const [error,     setError]     = useState('');
  const [success,   setSuccess]   = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (password !== confirm) { setError('Passwords do not match.'); return; }
    setLoading(true);
    setError('');

    try {
      const res  = await fetch('/api/auth/reset-password', {
        method:  'POST',
        headers: { 'content-type': 'application/json' },
        body:    JSON.stringify({ token, password }),
      });
      const data = await res.json();
      if (!res.ok) { setError(data.error ?? 'Something went wrong.'); }
      else          { setSuccess(true); setTimeout(() => router.push('/auth/login'), 2000); }
    } catch {
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  if (!token) {
    return (
      <div className="text-center text-ink-muted text-sm">
        Invalid reset link. <Link href="/auth/forgot-password" className="text-action font-semibold">Request a new one.</Link>
      </div>
    );
  }

  return (
    <div className="w-full max-w-sm">
      <div className="text-center mb-8">
        <div className="text-5xl mb-3">🔒</div>
        <h1 className="text-2xl font-extrabold text-ink">New password</h1>
      </div>

      {success ? (
        <div className="text-center space-y-3">
          <div className="text-4xl">✅</div>
          <p className="text-ink font-semibold">Password updated!</p>
          <p className="text-ink-muted text-sm">Redirecting to login…</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="password" placeholder="New password (min 8 characters)" required minLength={8}
            aria-label="New password (min 8 characters)"
            value={password} onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-white border-2 border-line rounded-control px-4 py-3 text-ink placeholder:text-ink-muted outline-none focus:border-action focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2 focus-visible:ring-offset-canvas"
          />
          <input
            type="password" placeholder="Confirm new password" required
            aria-label="Confirm new password"
            value={confirm} onChange={(e) => setConfirm(e.target.value)}
            className="w-full bg-white border-2 border-line rounded-control px-4 py-3 text-ink placeholder:text-ink-muted outline-none focus:border-action focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2 focus-visible:ring-offset-canvas"
          />

          {error && <p className="text-retry bg-retry-soft border-2 border-retry rounded-control px-3 py-2 text-sm text-center font-semibold">{error}</p>}

          <button
            type="submit" disabled={loading}
            className="w-full bg-action hover:bg-action-dark disabled:opacity-50 text-white font-extrabold py-4 rounded-control border-2 border-ink shadow-hard-sm text-lg transition-colors"
          >
            {loading ? 'Updating…' : 'Update Password →'}
          </button>
        </form>
      )}
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <div className="min-h-screen bg-paper flex flex-col items-center justify-center px-6 py-12 animate-fade-in">
      <Suspense fallback={<div className="text-ink-muted">Loading…</div>}>
        <ResetForm />
      </Suspense>
    </div>
  );
}
