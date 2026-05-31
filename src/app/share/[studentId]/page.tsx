'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

function masteryLabel(m: string) {
  if (m === 'Mastered')   return { label: 'Mastered',   color: 'bg-green-100 text-green-700' };
  if (m === 'Practicing') return { label: 'Practicing', color: 'bg-amber-100 text-amber-700' };
  return { label: 'Not started', color: 'bg-gray-100 text-gray-400' };
}

interface StudentData {
  id: string;
  name: string;
  grade: number;
}

interface ProgressEntry {
  topicId: string;
  topicName: string;
  mastery: string;
  attempted: number;
  correct: number;
}

export default function SharePage() {
  const params = useParams();
  const studentId = params.studentId as string;

  const [student, setStudent] = useState<StudentData | null>(null);
  const [progress, setProgress] = useState<ProgressEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    Promise.all([
      fetch(`/api/students/${studentId}`).then((r) => {
        if (!r.ok) { setNotFound(true); return null; }
        return r.json();
      }),
      fetch(`/api/progress?studentId=${studentId}`).then((r) => r.json()),
    ]).then(([stu, prog]) => {
      if (stu) setStudent(stu);
      if (prog && Array.isArray(prog)) setProgress(prog);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [studentId]);

  if (loading) return (
    <div className="flex items-center justify-center min-h-screen">
      <span className="text-4xl animate-bounce" aria-hidden="true">📊</span>
    </div>
  );

  if (notFound || !student) return (
    <div className="flex flex-col items-center justify-center min-h-screen px-6 text-center">
      <div className="text-6xl mb-4" aria-hidden="true">🔍</div>
      <h1 className="text-xl font-bold text-gray-700">Progress not found</h1>
      <p className="text-gray-400 text-sm mt-2">This link may have expired or the student ID is incorrect.</p>
    </div>
  );

  const mastered = progress.filter((p) => p.mastery === 'Mastered').length;
  const totalSolved = progress.reduce((s, p) => s + p.attempted, 0);

  return (
    <div className="max-w-lg mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <div className="text-5xl mb-3" aria-hidden="true">📚</div>
        <h1 className="text-2xl font-bold text-gray-800">This is {student.name}&apos;s MathSpark progress</h1>
        <p className="text-gray-400 text-sm mt-1">MathSpark — Grade {student.grade} Math</p>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-8">
        <div className="bg-white rounded-2xl p-4 text-center shadow-sm border border-gray-100">
          <div className="text-3xl font-bold text-blue-500">{totalSolved}</div>
          <div className="text-xs text-gray-400 mt-1">Questions answered</div>
        </div>
        <div className="bg-white rounded-2xl p-4 text-center shadow-sm border border-gray-100">
          <div className="text-3xl font-bold text-green-500">{mastered}</div>
          <div className="text-xs text-gray-400 mt-1">Topics mastered</div>
        </div>
      </div>

      <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wide mb-3">All topics</h2>
      <div className="space-y-2">
        {[...progress]
          .sort((a, b) => TOPIC_ORDER.indexOf(a.topicId) - TOPIC_ORDER.indexOf(b.topicId))
          .map((p) => {
            const { label, color } = masteryLabel(p.mastery);
            return (
              <div key={p.topicId} className="bg-white rounded-xl border border-gray-100 px-4 py-3 flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">{p.topicName || p.topicId}</span>
                <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${color}`}>{label}</span>
              </div>
            );
          })}
      </div>

      <p className="text-center text-xs text-gray-300 mt-8">
        Shared from MathSpark &middot; Read-only view
      </p>
    </div>
  );
}
