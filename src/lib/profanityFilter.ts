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
export function isClean(name: string): boolean {
  const normalized = name.toLowerCase().replace(/[^a-z]/g, '');
  return !BLOCKLIST.some((word) => normalized.includes(word));
}
