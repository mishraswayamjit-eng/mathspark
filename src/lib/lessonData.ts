import fs from 'fs';
import path from 'path';
import type { LessonTopic, LessonLevel, Lesson } from '@/types/lesson';

/**
 * Shared loader for static concept-lesson JSON (`data/lessons/<slug>.json`).
 * Extracted from the lessons route so the AI re-explain endpoint can reuse the
 * same cached, validated read path.
 */

const cache = new Map<string, LessonTopic | null>();
export const LESSON_SLUG_RE = /^[a-z0-9-]+$/;

/** Load a topic's lesson JSON, cached in-memory. Returns null if not found. */
export function loadTopic(slug: string): LessonTopic | null {
  if (!LESSON_SLUG_RE.test(slug)) return null;
  if (cache.has(slug)) return cache.get(slug) ?? null;

  const filePath = path.join(process.cwd(), 'data', 'lessons', `${slug}.json`);
  if (!fs.existsSync(filePath)) {
    cache.set(slug, null);
    return null;
  }
  const data = JSON.parse(fs.readFileSync(filePath, 'utf-8')) as LessonTopic;
  cache.set(slug, data);
  return data;
}

/** Find a specific level within a topic. */
export function findLevel(slug: string, levelId: number): LessonLevel | null {
  const topic = loadTopic(slug);
  if (!topic) return null;
  return topic.levels.find((l) => l.id === levelId) ?? null;
}

/** Find a specific lesson by slug + levelId + lessonId. */
export function findLesson(
  slug: string,
  levelId: number,
  lessonId: string,
): { topic: LessonTopic; level: LessonLevel; lesson: Lesson } | null {
  const topic = loadTopic(slug);
  if (!topic) return null;
  const level = topic.levels.find((l) => l.id === levelId);
  if (!level) return null;
  const lesson = level.lessons.find((ls) => ls.id === lessonId);
  if (!lesson) return null;
  return { topic, level, lesson };
}
