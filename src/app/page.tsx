'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';

export default function RootPage() {
  const router = useRouter();
  const [studentName, setStudentName] = useState<string | null>(null);

  useEffect(() => {
    const id   = localStorage.getItem('mathspark_student_id');
    const name = localStorage.getItem('mathspark_student_name');

    if (!id) {
      router.replace('/start');
      return;
    }

    // Show welcome back briefly, then navigate
    setStudentName(name ?? 'there');
    const t = setTimeout(() => router.replace('/chapters'), 400);
    return () => clearTimeout(t);
  }, [router]);

  // New student — show nothing (redirect happens instantly)
  if (!studentName) {
    return (
      <motion.div
        className="flex items-center justify-center min-h-screen"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.2 }}
      >
        <span className="text-5xl animate-bounce" aria-hidden="true">⭐</span>
      </motion.div>
    );
  }

  // Returning student — brief welcome
  return (
    <motion.div
      className="flex flex-col items-center justify-center min-h-screen gap-4 text-center px-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.2 }}
    >
      <div className="text-7xl animate-bounce">👋</div>
      <h1 className="text-3xl font-bold text-gray-800">
        Welcome back, {studentName}!
      </h1>
      <p className="text-gray-400 text-base">Ready to practise? Let&apos;s go! 🚀</p>
      <div className="flex gap-1 mt-2">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="w-2 h-2 rounded-full bg-blue-400 animate-bounce"
            style={{ animationDelay: `${i * 0.15}s` }}
          />
        ))}
      </div>
    </motion.div>
  );
}
