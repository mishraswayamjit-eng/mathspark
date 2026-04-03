import type { Lesson, Slide } from '@/types/lesson';
import { LESSON_VISUALS } from '@/data/lessonVisuals';

/**
 * Converts an old-format Lesson (steps/explanation/rule/tip) into a Slide[]
 * array at runtime. Existing lessons automatically get slide mode with no
 * JSON migration needed.
 */
export function toSlides(lesson: Lesson): Slide[] {
  const slides: Slide[] = [];

  // 1. Intro slide from title + intro
  const introSlide: Slide = {
    type: 'intro',
    text: lesson.title,
    subtext: lesson.intro,
    emoji: '📖',
  };
  // Attach illustration from visual string if mapped
  if (lesson.visual && LESSON_VISUALS[lesson.visual]) {
    introSlide.illustration = LESSON_VISUALS[lesson.visual];
  }
  slides.push(introSlide);

  // 2. If steps exist, one concept slide per step
  if (lesson.steps?.length) {
    for (const step of lesson.steps) {
      slides.push({
        type: 'concept',
        text: step.text,
        notation: step.notation || undefined,
        subtext: step.tip || undefined,
      });
    }
  }

  // 3. If explanation exists (and no steps), one concept slide per paragraph
  if (lesson.explanation?.length && !lesson.steps?.length) {
    for (const para of lesson.explanation) {
      slides.push({ type: 'concept', text: para });
    }
  }

  // 4. Rule slide
  if (lesson.rule) {
    slides.push({ type: 'rule', text: lesson.rule, emoji: '📝' });
  }

  // 5. Tip slide
  if (lesson.tip) {
    slides.push({ type: 'tip', text: lesson.tip, emoji: '💡' });
  }

  return slides;
}
