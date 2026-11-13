'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';

export default function AddChildPage() {
  const router         = useRouter();
  const { status }     = useSession();
  const [name,    setName]    = useState('');
  const [grade,   setGrade]   = useState<number | null>(null);
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
        body:    JSON.stringify({ name: name.trim(), grade: grade ?? 4 }),
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
    <div className="min-h-screen bg-paper flex flex-col items-center justify-center px-6 py-12">
      <div className="w-full max-w-sm">
        <button
          onClick={() => window.history.length > 1 ? router.back() : router.push('/parent/dashboard')}
          className="text-ink-muted text-sm font-semibold mb-6 flex items-center gap-1 hover:text-ink transition-colors"
        >
          ← Back
        </button>

        <div className="text-center mb-8">
          <div className="text-5xl mb-3">👦</div>
          <h1 className="text-2xl font-extrabold text-ink">Add a child</h1>
          <p className="text-ink-muted text-sm mt-1">Create your child's learning profile</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-ink-muted text-xs font-semibold mb-2">
              Child's first name
            </label>
            <input
              type="text" placeholder="e.g. Arjun" required
              value={name} onChange={(e) => setName(e.target.value)}
              className="w-full bg-white border-2 border-line rounded-control px-4 py-3 text-ink placeholder:text-ink-muted outline-none focus:border-action"
            />
          </div>

          <div>
            <label className="block text-ink-muted text-xs font-semibold mb-2">
              Grade
            </label>
            <select
              value={grade ?? ''} onChange={(e) => setGrade(Number(e.target.value))}
              className="w-full bg-white border-2 border-line rounded-control px-4 py-3 text-ink outline-none focus:border-action"
            >
              <option value="" disabled className="bg-white">Select grade</option>
              {[2, 3, 4, 5, 6, 7, 8, 9].map((g) => (
                <option key={g} value={g} className="bg-white">Grade {g}</option>
              ))}
            </select>
          </div>

          {error && <p className="text-retry bg-retry-soft border-2 border-retry rounded-control px-3 py-2 text-sm text-center font-semibold">{error}</p>}

          <button
            type="submit" disabled={loading || !grade}
            className="w-full bg-action hover:bg-action-dark disabled:opacity-50 text-white font-extrabold py-4 rounded-control border-2 border-ink shadow-hard-sm text-lg transition-colors"
          >
            {loading ? 'Creating…' : 'Add Child →'}
          </button>
        </form>

        <p className="text-ink-muted text-xs text-center mt-4">
          After adding your child, subscribe to unlock full access.
        </p>
      </div>
    </div>
  );
}
