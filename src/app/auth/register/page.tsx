'use client';

import { useState } from 'react';
import { signIn } from 'next-auth/react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function RegisterPage() {
  const router = useRouter();
  const [form,    setForm]    = useState({ name: '', email: '', password: '', phone: '' });
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState('');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await fetch('/api/auth/register', {
        method:  'POST',
        headers: { 'content-type': 'application/json' },
        body:    JSON.stringify(form),
      });
      const data = await res.json();

      if (!res.ok) { setError(data.error ?? 'Registration failed.'); setLoading(false); return; }

      // Auto-login after registration
      const result = await signIn('credentials', {
        email:    form.email,
        password: form.password,
        redirect: false,
      });

      if (result?.ok) router.push('/parent/dashboard');
      else { setError('Account created! Please sign in.'); router.push('/auth/login'); }
    } catch {
      setError('Something went wrong. Please try again.');
      setLoading(false);
    }
  }

  function field(k: keyof typeof form) {
    return (e: React.ChangeEvent<HTMLInputElement>) =>
      setForm((f) => ({ ...f, [k]: e.target.value }));
  }

  return (
    <div className="min-h-screen bg-[#131F24] flex flex-col items-center justify-center px-6 py-12">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">🌱</div>
          <h1 className="text-2xl font-extrabold text-white">Create your account</h1>
          <p className="text-white/50 text-sm mt-1">Start your child's IPM journey today</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text" placeholder="Your name" required
            value={form.name} onChange={field('name')}
            className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-[#58CC02]"
          />
          <input
            type="email" placeholder="Email address" required
            value={form.email} onChange={field('email')}
            className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-[#58CC02]"
          />
          <input
            type="password" placeholder="Password (min 8 characters)" required minLength={8}
            value={form.password} onChange={field('password')}
            className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-[#58CC02]"
          />
          <input
            type="tel" placeholder="Phone number (optional)"
            value={form.phone} onChange={field('phone')}
            className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-[#58CC02]"
          />

          {error && <p className="text-[#FF4B4B] text-sm text-center font-semibold">{error}</p>}

          <button
            type="submit" disabled={loading}
            className="w-full bg-[#58CC02] hover:bg-[#46a302] disabled:opacity-50 text-white font-extrabold py-4 rounded-2xl text-lg transition-colors mt-2"
          >
            {loading ? 'Creating account…' : 'Create Account →'}
          </button>
        </form>

        <p className="text-center text-white/40 text-sm mt-6">
          Already have an account?{' '}
          <Link href="/auth/login" className="text-[#1CB0F6] font-semibold hover:underline">
            Sign in
          </Link>
        </p>
        <p className="text-center mt-4">
          <Link href="/pricing" className="text-white/30 text-xs hover:text-white/60 transition-colors">
            View plans & pricing →
          </Link>
        </p>
      </div>
    </div>
  );
}
