// Simple blocklist profanity filter for display names
// Only blocks the most egregious terms — this is a Grade 4 app

const BLOCKLIST = [
  'fuck', 'shit', 'ass', 'bitch', 'cunt', 'dick', 'cock', 'pussy',
  'nigger', 'nigga', 'faggot', 'retard', 'whore', 'slut', 'bastard',
  'damn', 'crap', 'piss', 'sex', 'porn', 'rape', 'kill', 'die', 'dead',
  'hate', 'nazi', 'hitler',
];

/**
 * Returns true if the name contains no blocked words.
 * Case-insensitive, strips non-alpha chars for comparison.
 */
/**
 * Returns true unless the whole word IS a blocked word. Unlike `isClean`, this
 * does not look inside the word, so real first names that happen to contain a
 * blocked string (Hassan, Eddie, Sadie) pass.
 */
export function isCleanWord(word: string): boolean {
  const normalized = word.toLowerCase().replace(/[^a-z]/g, '');
  return BLOCKLIST.indexOf(normalized) === -1;
}

export function isClean(name: string): boolean {
  const normalized = name.toLowerCase().replace(/[^a-z]/g, '');
  return !BLOCKLIST.some((word) => normalized.includes(word));
}
