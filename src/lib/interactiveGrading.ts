/**
 * Server-side grading for interactive question types.
 * Each type parses the student's answer string and validates against the config.
 */
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

      default:
        return false;
    }
  } catch {
    return false;
  }
}
