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

  function selectChild(child: Child) {
    localStorage.setItem('mathspark_student_id',   child.id);
    localStorage.setItem('mathspark_student_name', child.name);
    router.push('/chapters');
  }

  return (
    <div className="min-h-screen bg-[#131F24] flex flex-col items-center justify-center px-6 py-12">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">🌟</div>
          <h1 className="text-2xl font-extrabold text-white">Student login</h1>
          <p className="text-white/50 text-sm mt-1">Enter your parent's email to find your profile</p>
        </div>

        {children ? (
          <div className="space-y-3">
            <p className="text-white/60 text-sm text-center mb-4">Who are you?</p>
            {children.map((child) => (
              <button
                key={child.id}
                onClick={() => selectChild(child)}
                className="w-full bg-white/10 hover:bg-white/20 border border-white/10 rounded-2xl p-4 text-left flex items-center gap-4 transition-colors active:scale-[0.97]"
              >
                <span className="text-3xl">🧑‍🎓</span>
                <span className="text-white font-extrabold text-lg">{child.name}</span>
                <span className="text-white/40 ml-auto">→</span>
              </button>
            ))}
            <button
              onClick={() => setChildren(null)}
              className="w-full text-white/40 text-sm py-2 hover:text-white/70 transition-colors"
            >
              ← Use a different email
            </button>
          </div>
        ) : (
          <form onSubmit={handleLookup} className="space-y-4">
            <input
              type="email" placeholder="Parent's email address" required autoComplete="email"
              value={email} onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder:text-white/40 outline-none focus:border-[#58CC02]"
            />

            {error && <p className="text-[#FF4B4B] text-sm text-center font-semibold">{error}</p>}

            <button
              type="submit" disabled={loading}
              className="w-full bg-[#58CC02] hover:bg-[#46a302] disabled:opacity-50 text-white font-extrabold py-4 rounded-2xl text-lg transition-colors"
            >
              {loading ? 'Finding…' : 'Find My Profile →'}
            </button>
          </form>
        )}

        <p className="text-center text-white/30 text-xs mt-8">
          Are you a parent?{' '}
          <a href="/auth/login" className="text-[#1CB0F6] font-semibold">Sign in here →</a>
        </p>
      </div>
    </div>
  );
}
