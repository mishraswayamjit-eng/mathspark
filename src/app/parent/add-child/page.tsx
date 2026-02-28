'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';

export default function AddChildPage() {
  const router         = useRouter();
  const { status }     = useSession();
  const [name,    setName]    = useState('');
  const [grade,   setGrade]   = useState(4);
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState('');

  if (status === 'unauthenticated') {
    if (typeof window !== 'undefined') router.replace('/auth/login');
    return null;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res  = await fetch('/api/parent/children', {
        method:  'POST',
        headers: { 'content-type': 'application/json' },
        body:    JSON.stringify({ name: name.trim(), grade }),
      });
      const data = await res.json();

      if (!res.ok) { setError(data.error ?? 'Something went wrong.'); setLoading(false); return; }

      router.push('/parent/dashboard');
    } catch {
      setError('Something went wrong. Please try again.');
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#131F24] flex flex-col items-center justify-center px-6 py-12">
      <div className="w-full max-w-sm">
        <button
          onClick={() => router.back()}
          className="text-white/50 text-sm font-semibold mb-6 flex items-center gap-1 hover:text-white transition-colors"
        >
          ← Back
        </button>

        <div className="text-center mb-8">
          <div className="text-5xl mb-3">👦</div>
          <h1 className="text-2xl font-extrabold text-white">Add a child</h1>
          <p className="text-white/50 text-sm mt-1">Create your child's learning profile</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-white/60 text-xs font-semibold uppercase tracking-widest mb-2">
              Child's first name
            </label>
            <input
              type="text" placeholder="e.g. Arjun" required
              value={name} onChange={(e) => setName(e.target.value)}
              className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-[#58CC02]"
            />
          </div>

          <div>
            <label className="block text-white/60 text-xs font-semibold uppercase tracking-widest mb-2">
              Grade
            </label>
            <select
              value={grade} onChange={(e) => setGrade(Number(e.target.value))}
              className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white outline-none focus:border-[#58CC02]"
            >
              {[3, 4, 5].map((g) => (
                <option key={g} value={g} className="bg-[#131F24]">Grade {g}</option>
              ))}
            </select>
          </div>

          {error && <p className="text-[#FF4B4B] text-sm text-center font-semibold">{error}</p>}

          <button
            type="submit" disabled={loading}
            className="w-full bg-[#58CC02] hover:bg-[#46a302] disabled:opacity-50 text-white font-extrabold py-4 rounded-2xl text-lg transition-colors"
          >
            {loading ? 'Creating…' : 'Add Child →'}
          </button>
        </form>

        <p className="text-white/30 text-xs text-center mt-4">
          After adding your child, subscribe to unlock full access.
        </p>
      </div>
    </div>
  );
}
