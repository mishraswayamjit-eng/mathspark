'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

interface Child {
  id:   string;
  name: string;
}

export default function StudentLoginPage() {
  const router = useRouter();
  const [email,    setEmail]    = useState('');
  const [children, setChildren] = useState<Child[] | null>(null);
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState('');
  const [pinChild, setPinChild] = useState<Child | null>(null);
  const [pin,      setPin]      = useState('');

  async function handleLookup(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res  = await fetch(`/api/student/lookup?email=${encodeURIComponent(email.trim().toLowerCase())}`);
      const data = await res.json();

      if (!res.ok || !data.children?.length) {
        setError('No account found for that email, or no children added yet.');
      } else {
        setChildren(data.children);
      }
    } catch {
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  async function selectChild(child: Child, pinValue?: string) {
    setLoading(true);
    setError('');
    try {
      const res = await fetch('/api/student/session', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ studentId: child.id, ...(pinValue ? { pin: pinValue } : {}) }),
      });
      const data = await res.json();

      if (!res.ok) {
        // If PIN is required, show PIN input
        if (data.requiresPin) {
          setPinChild(child);
          setLoading(false);
          return;
        }
        // Legacy account with no PIN — a parent must set one before login.
        if (data.requiresPinSetup) {
          setError('This account needs a PIN. Ask a parent to set one in the Parent dashboard.');
          setLoading(false);
          return;
        }
        setError(data.error || 'Login failed');
        setLoading(false);
        return;
      }

      localStorage.setItem('mathspark_student_id',   child.id);
      localStorage.setItem('mathspark_student_name', child.name);
      router.push('/home');
    } catch {
      setError('Something went wrong. Please try again.');
      setLoading(false);
    }
  }

  async function handlePinSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!pinChild || !pin) return;
    await selectChild(pinChild, pin);
  }

  return (
    <div className="min-h-screen bg-paper flex flex-col items-center justify-center px-6 py-12 animate-fade-in">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">🌟</div>
          <h1 className="text-2xl font-extrabold text-ink">Student login</h1>
          <p className="text-ink-muted text-sm mt-1">Enter your parent's email to find your profile</p>
        </div>

        {pinChild ? (
          <form onSubmit={handlePinSubmit} className="space-y-4">
            <p className="text-ink-muted text-sm text-center mb-2">
              Enter PIN for <span className="text-ink font-bold">{pinChild.name}</span>
            </p>
            <input
              type="password"
              inputMode="numeric"
              maxLength={4}
              autoFocus
              value={pin}
              onChange={(e) => { setPin(e.target.value.replace(/\D/g, '').slice(0, 4)); setError(''); }}
              placeholder="••••"
              aria-label="4-digit PIN"
              className="w-full text-3xl font-bold text-center tracking-[0.5em] bg-white border-2 border-line rounded-control px-4 py-3 text-ink placeholder:text-ink-muted outline-none focus:border-action focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2 focus-visible:ring-offset-canvas"
            />
            {error && <p className="text-retry bg-retry-soft border-2 border-retry rounded-control px-3 py-2 text-sm text-center font-semibold">{error}</p>}
            <button
              type="submit" disabled={loading || pin.length !== 4}
              className="w-full bg-action hover:bg-action-dark disabled:opacity-50 text-white font-extrabold py-4 rounded-control border-2 border-ink shadow-hard-sm text-lg transition-colors"
            >
              {loading ? 'Verifying…' : 'Enter →'}
            </button>
            <button
              type="button"
              onClick={() => { setPinChild(null); setPin(''); setError(''); }}
              className="w-full text-ink-muted text-sm py-2 hover:text-ink transition-colors"
            >
              ← Pick a different profile
            </button>
          </form>
        ) : children ? (
          <div className="space-y-3">
            <p className="text-ink-muted text-sm text-center mb-4">Who are you?</p>
            {children.map((child) => (
              <button
                key={child.id}
                onClick={() => selectChild(child)}
                disabled={loading}
                className="w-full bg-white hover:bg-soft border-2 border-ink shadow-hard-sm rounded-control p-4 text-left flex items-center gap-4 transition-colors active:scale-[0.97]"
              >
                <span className="text-3xl">🧑‍🎓</span>
                <span className="text-ink font-extrabold text-lg">{child.name}</span>
                <span className="text-ink-muted ml-auto">→</span>
              </button>
            ))}
            <button
              onClick={() => setChildren(null)}
              className="w-full text-ink-muted text-sm py-2 hover:text-ink transition-colors"
            >
              ← Use a different email
            </button>
          </div>
        ) : (
          <form onSubmit={handleLookup} className="space-y-4">
            <input
              type="email" placeholder="Parent's email address" required autoComplete="email"
              aria-label="Parent's email address"
              value={email} onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-white border-2 border-line rounded-control px-4 py-3 text-ink placeholder:text-ink-muted outline-none focus:border-action focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2 focus-visible:ring-offset-canvas"
            />

            {error && <p className="text-retry bg-retry-soft border-2 border-retry rounded-control px-3 py-2 text-sm text-center font-semibold">{error}</p>}

            <button
              type="submit" disabled={loading}
              className="w-full bg-action hover:bg-action-dark disabled:opacity-50 text-white font-extrabold py-4 rounded-control border-2 border-ink shadow-hard-sm text-lg transition-colors"
            >
              {loading ? 'Finding…' : 'Find My Profile →'}
            </button>
          </form>
        )}

        <p className="text-center text-ink-muted text-xs mt-8">
          Are you a parent?{' '}
          <a href="/auth/login" className="text-action font-semibold">Sign in here →</a>
        </p>
      </div>
    </div>
  );
}
