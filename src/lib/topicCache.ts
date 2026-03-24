import { prisma } from './db';

interface CachedTopic {
  id: string;
  name: string;
  grade: number;
  chapterNumber: string;
}

let _cache: CachedTopic[] | null = null;
let _cacheTime = 0;
const CACHE_TTL = 60 * 60 * 1000; // 1 hour

export async function getTopicsCached(): Promise<CachedTopic[]> {
  if (!_cache || Date.now() - _cacheTime > CACHE_TTL) {
    _cache = await prisma.topic.findMany({
      select: { id: true, name: true, grade: true, chapterNumber: true },
    });
    _cacheTime = Date.now();
  }
  return _cache;
}
