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
      <div className="text-center text-white/50 text-sm">
        Invalid reset link. <Link href="/auth/forgot-password" className="text-[#1CB0F6]">Request a new one.</Link>
      </div>
    );
  }

  return (
    <div className="w-full max-w-sm">
      <div className="text-center mb-8">
        <div className="text-5xl mb-3">🔒</div>
        <h1 className="text-2xl font-extrabold text-white">New password</h1>
      </div>

      {success ? (
        <div className="text-center space-y-3">
          <div className="text-4xl">✅</div>
          <p className="text-white font-semibold">Password updated!</p>
          <p className="text-white/50 text-sm">Redirecting to login…</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="password" placeholder="New password (min 8 characters)" required minLength={8}
            value={password} onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-[#58CC02]"
          />
          <input
            type="password" placeholder="Confirm new password" required
            value={confirm} onChange={(e) => setConfirm(e.target.value)}
            className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-[#58CC02]"
          />

          {error && <p className="text-[#FF4B4B] text-sm text-center font-semibold">{error}</p>}

          <button
            type="submit" disabled={loading}
            className="w-full bg-[#58CC02] hover:bg-[#46a302] disabled:opacity-50 text-white font-extrabold py-4 rounded-2xl text-lg transition-colors"
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
    <div className="min-h-screen bg-[#131F24] flex flex-col items-center justify-center px-6 py-12">
      <Suspense fallback={<div className="text-white/50">Loading…</div>}>
        <ResetForm />
      </Suspense>
    </div>
  );
}
