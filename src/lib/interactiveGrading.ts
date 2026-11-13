/**
 * Grading for interactive question types.
 * Each type parses the student's answer string and validates against the config.
 *
 * `validateInteractiveAnswer` is the server-side authority (called by
 * /api/attempts). The two small pure helpers below are also imported by the
 * tile-build and number-line components for instant feedback, so the client
 * and server can never disagree about what counts as right.
 */

function sameStrings(a: string[], b: string[]): boolean {
  if (a.length !== b.length) return false;
  for (let i = 0; i < a.length; i++) {
    if (a[i] !== b[i]) return false;
  }
  return true;
}

/** True when the filled-in tiles match the solution or one of its accepted alternatives. */
export function isTileBuildCorrect(
  config: { solution: string[]; alsoCorrect?: string[][] },
  filled: string[],
): boolean {
  if (sameStrings(config.solution, filled)) return true;
  const others = config.alsoCorrect ?? [];
  for (let i = 0; i < others.length; i++) {
    if (sameStrings(others[i], filled)) return true;
  }
  return false;
}

/** True when the chosen point sits on the correct snap position of the number line. */
export function isNumberLineCorrect(
  config: { min: number; step: number; correctValue: number },
  value: number,
): boolean {
  if (typeof value !== 'number' || !isFinite(value) || !(config.step > 0)) return false;
  const chosen  = Math.round((value - config.min) / config.step);
  const correct = Math.round((config.correctValue - config.min) / config.step);
  return chosen === correct;
}

export function validateInteractiveAnswer(
  type: string,
  data: unknown,
  answer: string,
): boolean {
  try {
    switch (type) {
      case 'tapToColor': {
        const config = data as {
          correctCount: number;
          correctIndices?: number[];
        };
        const selected: number[] = JSON.parse(answer);
        if (!Array.isArray(selected)) return false;
        // If exact indices are specified, check them; otherwise check count
        if (config.correctIndices) {
          const sorted = [...selected].sort((a, b) => a - b);
          const expected = [...config.correctIndices].sort((a, b) => a - b);
          return (
            sorted.length === expected.length &&
            sorted.every((v, i) => v === expected[i])
          );
        }
        return selected.length === config.correctCount;
      }

      case 'dragToSort': {
        const config = data as { correctOrder: number[] };
        const submitted: number[] = JSON.parse(answer);
        if (!Array.isArray(submitted)) return false;
        return (
          submitted.length === config.correctOrder.length &&
          submitted.every((v, i) => v === config.correctOrder[i])
        );
      }

      case 'chartTap': {
        const config = data as { correctRegion: string };
        const region: string = JSON.parse(answer);
        return region === config.correctRegion;
      }

      case 'tileBuild': {
        const config = data as { solution: string[]; alsoCorrect?: string[][] };
        const filled: unknown = JSON.parse(answer);
        if (!Array.isArray(filled) || !filled.every((t) => typeof t === 'string')) return false;
        return isTileBuildCorrect(config, filled as string[]);
      }

      case 'numberLine': {
        const config = data as { min: number; step: number; correctValue: number };
        const value: unknown = JSON.parse(answer);
        if (typeof value !== 'number') return false;
        return isNumberLineCorrect(config, value);
      }

      default:
        return false;
    }
  } catch {
    return false;
  }
}
