export type Difficulty = 'Easy' | 'Medium' | 'Hard';
export type MasteryLevel = 'NotStarted' | 'Practicing' | 'Mastered';
export type AnswerKey = 'A' | 'B' | 'C' | 'D';

export interface Student {
  id: string;
  name: string;
  grade: number;
  createdAt: string;
}

export interface Topic {
  id: string;
  name: string;
  chapterNumber: string;
}

export interface StepItem {
  step: number;
  text: string;
  latex?: string;
}

export interface Question {
  id: string;
  topicId: string;
  subTopic: string;
  difficulty: Difficulty;
  questionText: string;
  questionLatex: string;
  option1: string;
  option2: string;
  option3: string;
  option4: string;
  correctAnswer: AnswerKey;
  hint1: string;
  hint2: string;
  hint3: string;
  stepByStep: StepItem[];  // already parsed from JSON
  misconceptionA: string;
  misconceptionB: string;
  misconceptionC: string;
  misconceptionD: string;
  source: string;
}

export interface Progress {
  id: string;
  studentId: string;
  topicId: string;
  attempted: number;
  correct: number;
  mastery: MasteryLevel;
  updatedAt: string;
  topic?: Topic;
}

export interface TopicWithProgress extends Topic {
  mastery: MasteryLevel;
  attempted: number;
  correct: number;
}

export interface DiagnosticAnswer {
  topicId: string;
  questionId: string;
  isCorrect: boolean;
}

export interface DiagnosticResult {
  topicId: string;
  topicName: string;
  correct: number;
  total: number;
  status: 'Strong' | 'Learning' | 'NotYet';
}

export interface DashboardData {
  student: Student;
  stats: {
    totalSolved: number;
    topicsMastered: number;
    streakDays: number;
  };
  topics: TopicWithProgress[];
  weeklyData: Array<{ date: string; count: number }>;
  weakestTopicId: string | null;
}
