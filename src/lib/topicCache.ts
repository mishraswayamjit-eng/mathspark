import { prisma } from './db';

interface CachedTopic {
  id: string;
  name: string;
  grade: number;
  chapterNumber: string;
}

let _cache: CachedTopic[] | null = null;

export async function getTopicsCached(): Promise<CachedTopic[]> {
  if (!_cache) {
    _cache = await prisma.topic.findMany({
      select: { id: true, name: true, grade: true, chapterNumber: true },
    });
  }
  return _cache;
}
