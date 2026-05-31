export interface Achievement {
  id: string;
  emoji: string;
  title: string;
  description: string;
  earned: boolean;
}

export interface AchievementInput {
  totalAttempts: number;
  totalCorrect: number;
  streakDays: number;
  topicsMastered: number;
  topicsStarted: number;   // topics with at least 1 attempt
  totalTopics: number;
}

export function computeAchievements(input: AchievementInput): Achievement[] {
  const { totalAttempts, totalCorrect, streakDays, topicsMastered, topicsStarted, totalTopics } = input;

  return [
    {
      id: 'first_answer',
      emoji: '🌱',
      title: 'First Step!',
      description: 'Answer your first question',
      earned: totalAttempts >= 1,
    },
    {
      id: 'ten_questions',
      emoji: '🔟',
      title: 'Getting Warmed Up',
      description: 'Answer 10 questions',
      earned: totalAttempts >= 10,
    },
    {
      id: 'hundred_questions',
      emoji: '💯',
      title: 'Century!',
      description: 'Answer 100 questions',
      earned: totalAttempts >= 100,
    },
    {
      id: 'five_hundred',
      emoji: '🚀',
      title: 'Math Rocket',
      description: 'Answer 500 questions',
      earned: totalAttempts >= 500,
    },
    {
      id: 'first_master',
      emoji: '⭐',
      title: 'Topic Master',
      description: 'Master your first topic',
      earned: topicsMastered >= 1,
    },
    {
      id: 'five_mastered',
      emoji: '🏆',
      title: 'Champion',
      description: 'Master 5 topics',
      earned: topicsMastered >= 5,
    },
    {
      id: 'all_mastered',
      emoji: '👑',
      title: 'Math King/Queen',
      description: 'Master all 16 topics',
      earned: topicsMastered >= 16,
    },
    {
      id: 'streak_3',
      emoji: '🔥',
      title: 'On Fire!',
      description: '3-day streak',
      earned: streakDays >= 3,
    },
    {
      id: 'streak_7',
      emoji: '⚡',
      title: 'Week Warrior',
      description: '7-day streak',
      earned: streakDays >= 7,
    },
    {
      id: 'streak_30',
      emoji: '🌟',
      title: 'Unstoppable',
      description: '30-day streak',
      earned: streakDays >= 30,
    },
    {
      id: 'explorer',
      emoji: '🗺️',
      title: 'Explorer',
      description: 'Start all 16 topics',
      earned: topicsStarted >= totalTopics,
    },
    {
      id: 'sharp_shooter',
      emoji: '🎯',
      title: 'Sharp Shooter',
      description: '80% accuracy across all attempts',
      earned: totalAttempts >= 20 && totalCorrect / totalAttempts >= 0.8,
    },
  ];
}
