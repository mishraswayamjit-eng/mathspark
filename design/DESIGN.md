# Socratic — Style Reference
> A friendly maths notebook: graph paper, ink outlines, one indigo pen

**Theme:** light

`design/tokens.json` is the source of truth. `tailwind.config.ts` reads it directly, and `scripts/build_tokens.py` generates `src/app/tokens.css` (CSS variables) from it. Change a value in `tokens.json`, run `python scripts/build_tokens.py`, commit both files.

Socratic's interface looks like a child's maths notebook. The page is pale graph paper. Content sits on white cards drawn with a 2px outline, and the one card that matters most on a screen (the question, the greeting) gets a dark ink outline and a hard offset shadow, like a sticker lifted off the page. Headings are set in a rounded display face; everything a child has to read carefully is set in a plain, heavy sans. Colour carries meaning, not decoration: indigo means "do this next", green means "correct", yellow means "here is help", and a soft red means "not quite, look again".

The visual language was ported from the `ipm-maths-practice` app, which tested better with children than the earlier Duolingo-style skin.

## Tokens — Colors

| Name | Value | Tailwind | CSS variable | Role |
|------|-------|----------|--------------|------|
| Ink | `#1d2a4d` | `ink` | `--color-ink` | Primary text and headings; the outline and hard shadow on emphasised cards and buttons; fill of sticky headers |
| Muted Ink | `#5d6b8c` | `ink-muted` | `--color-ink-muted` | Secondary text: sub-labels, counts, helper copy. Never question text or options |
| Canvas | `#f2f7fc` | `canvas` | `--color-canvas` | Page background behind the grid |
| Grid Line | `#dce8f4` | `canvas-grid` | `--color-canvas-grid` | 1px graph-paper lines every 24px. Decorative only |
| Card White | `#ffffff` | `card` | `--color-card` | Card, option, button and nav surfaces; text on indigo, green and ink fills |
| Soft Fill | `#eef3fb` | `soft` | `--color-soft` | Quiet fills inside cards: number badges, chips, meter tracks, formula blocks |
| Line | `#d3deee` | `line` | `--color-line` | Default 2px border on cards, options, chips, meters |
| Action Indigo | `#4f46e5` | `action` | `--color-action` | The one primary action colour: primary button, progress fill, active nav tab, focus outline |
| Action Indigo Dark | `#3f37c9` | `action-dark` | `--color-action-dark` | Hover and pressed state of the primary action |
| Correct Green | `#12805c` | `success` | `--color-success` | Reserved for "correct" and "mastered" |
| Correct Wash | `#dff6ea` | `success-soft` | `--color-success-soft` | Background of correct options and correct feedback |
| Not-Quite Red | `#c62f3d` | `retry` | `--color-retry` | The chosen option that was not right; the "not quite" heading |
| Not-Quite Wash | `#fde8ea` | `retry-soft` | `--color-retry-soft` | Background of the not-right option and its feedback panel |
| Hint Yellow | `#fff1b8` | `hint` | `--color-hint` | Fill of the hint note |
| Hint Ink | `#5a4300` | `hint-ink` | `--color-hint-ink` | Text and dashed outline on the hint note |
| Star Gold | `#f5a400` | `star` | `--color-star` | Stars, XP and reward accents |
| Strong Teal | `#0e7490` | `strong` | `--color-strong` | The "strong" mastery band (75–89%) on mastery maps, legends and report rows only |
| Strong Wash | `#dff3f8` | `strong-soft` | `--color-strong-soft` | Background of "strong" mastery tiles and rows |

### Contrast (WCAG, computed)

| Pair | Ratio | Use |
|------|-------|-----|
| Ink on Card White | 14.1 : 1 | All primary text |
| Muted Ink on Card White | 5.3 : 1 | Secondary text |
| Muted Ink on Canvas | 4.9 : 1 | Secondary text on the page |
| Card White on Action Indigo | 6.3 : 1 | Primary button label |
| Card White on Correct Green | 4.9 : 1 | Green button label |
| Correct Green on Correct Wash | 4.3 : 1 | Bold text 15px and up only |
| Not-Quite Red on Not-Quite Wash | 4.6 : 1 | Feedback heading, option text |
| Hint Ink on Hint Yellow | 8.3 : 1 | Hint text |
| Ink on Star Gold | 6.8 : 1 | "Need more help?" button label |
| Strong Teal on Card White | 5.4 : 1 | Mastery label text |
| Strong Teal on Strong Wash | 4.7 : 1 | Mastery row text |

## Tokens — Typography

### Fredoka — Headings, card titles, header bars, reward numbers · `font-display` · `--font-fredoka`
- **Weights:** 500, 600, 700 (600 by default)
- **Sizes:** 18px, 22px, 28px
- **Line height:** 1.15–1.20
- **Letter spacing:** 0.2px
- **Role:** The friendly voice of the product. Applied automatically to every `h1`–`h3`. Free Google font, loaded with `next/font`.

### Nunito — Everything a child reads carefully · `font-sans` · `--font-nunito`
- **Weights:** 600 (body), 700 (questions, options), 800 (buttons, chips)
- **Sizes:** 13px, 15px, 17px, 19px
- **Line height:** 1.4–1.5
- **Letter spacing:** normal
- **Role:** Question text, answer options, body copy, buttons, labels. Emphasis comes from weight, never from a change of face, colour or case.

### Type Scale

| Role | Family | Weight | Size | Line Height | Tailwind | Used for |
|------|--------|--------|------|-------------|----------|----------|
| caption | Nunito | 800 | 13px | 1.4 | `text-caption` | Chips, badges, difficulty tags |
| label | Nunito | 700 | 15px | 1.4 | `text-label` | Sub-labels, hint and solution step text |
| body | Nunito | 600 | 17px | 1.5 | `text-body` | Reading text and answer options |
| question | Nunito | 700 | 19px | 1.5 | `text-question` | Question text |
| title | Fredoka | 600 | 18px | 1.2 | `text-title` | Card titles, sticky header title |
| heading | Fredoka | 600 | 22px | 1.15 | `text-heading` | Section and feedback headings |
| display | Fredoka | 600 | 28px | 1.15 | `text-display` | Page greeting, results headline |

13px is the floor for anything a child must read.

## Tokens — Spacing & Shapes

**Base unit:** 4px (Tailwind's default scale)

**Density:** comfortable; mobile-first, one column, `max-w-lg` centred

### Spacing Scale

| Value | Use |
|-------|-----|
| 8px | Gap between chips; icon-to-label gap in buttons |
| 10px | Gap between answer options |
| 12px | Gap between cards in a list or grid |
| 16px | Card padding; page side padding |
| 24px | Gap between page sections; graph-paper grid size |
| 48px | Minimum height of every button and tappable row |
| 96px | Bottom page padding that clears the bottom nav (`pb-24`) |

### Border Radius

| Element | Value | Tailwind |
|---------|-------|----------|
| Inline blocks (formula, answer strip) | 10px | `rounded-note` |
| Icon buttons, emoji tiles, stat pills | 12px | `rounded-tile` |
| Buttons, answer options, hint note | 14px | `rounded-control` |
| Cards and panels | 18px | `rounded-card` |
| Chips, meters, number badges | 9999px | `rounded-full` |

### Borders and Shadows

- **Every outline is 2px.** 1px borders are not part of the system.
- **Thick left edge (10px)** in a topic colour marks list cards such as chapters.
- **Hard shadows only** — a solid ink offset with no blur:

| Tailwind | Value | Use |
|----------|-------|-----|
| `shadow-hard-xs` | 1px 1px 0 ink | Pressed button |
| `shadow-hard-sm` | 3px 3px 0 ink | Button at rest |
| `shadow-hard` | 4px 4px 0 ink | Emphasised secondary card |
| `shadow-hard-lg` | 5px 5px 0 ink | Hero card and question card |

## Components

Classes prefixed `ui-` are defined in `src/app/globals.css`.

### Page Canvas — `bg-paper`
**Role:** Background of every light page

Canvas fill with a 24px graph-paper grid. Put it on the full-screen page wrapper; never on a card.

### Card — `ui-card`
**Role:** Default container

White fill, 2px Line border, 18px radius, 16px padding, no shadow.

### Emphasised Card — `ui-card ui-card-pop`
**Role:** The single most important card on a screen (question, greeting hero)

Ink border and a 5px hard ink shadow. At most one per screen, so it keeps its meaning.

### List Card
**Role:** Chapter, topic and "continue" rows

`ui-card` plus `border-l-[10px]` in a topic colour, an emoji tile on the left, a title in Fredoka, a muted sub-label and a thin progress bar.

### Primary Button — `ui-btn ui-btn-primary`, or `<DuoButton>` (default variant)
**Role:** The next step: "Continue", "Start practising", "Got it"

Action Indigo fill, white label at weight 800, 2px ink border, 14px radius, 3px hard shadow. On press it moves 2px down-right and the shadow shrinks to 1px. Sentence case, never uppercase. One per view.

### Secondary Button — `ui-btn`, or `<DuoButton variant="white">`
**Role:** Alternatives beside the primary: "Watch solution", "Previous"

Same shape as the primary, white fill, ink label.

### Answer Option
**Role:** One of four choices (`QuestionCard`)

White fill, 2px Line border, 14px radius, min-height 52px. A 32px round Soft badge holds the letter; option text is 17px at weight 700. Hover turns the border ink. After answering: the correct option takes Correct Wash with a green border and green badge; the chosen not-right option takes Not-Quite Wash with a red border; the rest fade to 40% opacity.

### Chip — `ui-chip`
**Role:** Topic, source and count labels above a question

Soft fill, 2px Line border, pill radius, 13px at weight 800.

### Hint Note — `ui-hint`
**Role:** Help after a not-right answer (`HintSystem`)

Hint Yellow fill, Hint Ink text and a 2px dashed Hint Ink outline. The dashed outline is unique to hints.

### Solved Solution
**Role:** Step-by-step worked answer (`StepByStep`)

2px ink outline around a white body, with an ink header bar reading "📖 Solved solution" in Fredoka. Steps are numbered in Soft round badges. The maths that changed in a step sits in a Correct Wash block with a 6px green left edge.

### Feedback Panel
**Role:** Result after answering (`ResultPanels`)

Correct: Correct Wash sheet, Fredoka heading from the approved praise list, XP in a white outlined pill. Not right: Not-Quite Wash sheet, heading "Not quite. Let's look again 🔍", then the verified correct answer in a Correct Wash strip.

### Progress Meter — `ui-meter`
**Role:** Lesson and chapter progress

Soft track with a 2px Line border, Action Indigo fill, pill radius.

### Progress Dots
**Role:** One square per question in a lesson

28px squares with a 9px radius and 2px border. Current: ink border with a 2px hard shadow. Correct: Correct Wash with green border. Not right: Not-Quite Wash with red border.

### Sticky Header
**Role:** Top bar on every page

Ink fill, white Fredoka title at 18px, back and utility icon buttons with 44px targets.

### Bottom Navigation
**Role:** Main app sections

White fill with a 2px ink top border. The active tab is Action Indigo at weight 800 with a 4px indigo top edge; inactive tabs are Muted Ink.

## Do's and Don'ts

### Do
- Use Action Indigo for the one thing the child should do next, and nothing else.
- Keep green for "correct" and "mastered" so it always means the same thing.
- Give every outline 2px, and every button a hard ink shadow that sinks on press.
- Put exactly one emphasised card (`ui-card-pop`) on a screen.
- Set question text at 19px/700 and options at 17px/700 in Ink.
- Keep every button and tappable row at least 48px tall.
- Use sentence case for buttons and labels.
- Mark decorative emoji with `aria-hidden="true"`.
- Use the role names (`bg-action`, `text-ink`, `border-line`) in new code.

### Don't
- Don't use gradients, blurred shadows or glass effects; surfaces are flat fills with outlines.
- Don't use `duo-*` classes or hard-coded hex values in new code. `duo-*` exists only for older call sites.
- Don't use green or red as decoration. A child should never wonder whether a green badge means they got something right.
- Don't write "Wrong!", "Incorrect!", "Failed" or "Error". Say "Not quite — let's think about this together!" or "Almost! Here's a hint."
- Don't set Fredoka below 18px, or use it for question text and options.
- Don't use uppercase tracking labels; they are harder for young readers.
- Don't put text smaller than 13px in front of a child.
- Don't put green text on Correct Wash below 15px bold (contrast is 4.3 : 1).
- Don't keep a separate theme for any screen. Flashcards use this system too: the card is the screen's one emphasised card, "got it" is green, "still learning" is hint yellow.

## Surfaces

| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 0 | Canvas | `#f2f7fc` | Graph-paper page |
| 1 | Card White | `#ffffff` | Cards, options, buttons, bottom nav |
| 2 | Soft Fill | `#eef3fb` | Quiet fills inside a card |
| 3 | Ink | `#1d2a4d` | Sticky header and solved-solution header, with white text |

## Imagery

Sparky, the mascot, appears beside feedback and in empty states, never as page decoration. Emoji stand in for icons: one per card, in a 44px rounded tile tinted with the topic colour. Maths is rendered with KaTeX in Ink. There is no photography. Topic colours (the hues on list-card edges and emoji tiles) are the only place a wider palette appears; they never colour buttons or text.

## Diagrams and the whiteboard

Interactive visuals (`src/components/visuals/`) are drawn like a clean textbook figure: plenty of white space, 2.5px Ink outlines, and one saturated fill for the thing being looked at. That fill is Star Gold with an Ink outline for geometry (angle wedges, tiles, bars) and Action Indigo for counted or selected items (shaded fraction parts, dots, the point on a number line). Draggable handles are a filled circle with an Ink outline. The sentence of working under a visual sits in a Soft block, centred, at 16px/700. Controls inside a visual use Line borders so the figure, not its controls, carries the weight. The whiteboard panel itself is a plain white card with a Line border; the conversation beside it keeps the emphasised Ink outline.

## Layout

One centred column, `max-w-lg`, with 16px side padding, on the graph-paper canvas. A page reads top to bottom: sticky ink header, one emphasised card, then plain cards with 12–16px gaps. Practice screens put the question card first, options below, and feedback in a sheet that slides up from the bottom. Bottom navigation is fixed; pages end with 96px of padding to clear it.

## Agent Prompt Guide

Quick Color Reference:
- text (primary): #1d2a4d
- text (secondary): #5d6b8c
- background (page): #f2f7fc with a #dce8f4 24px grid
- background (card): #ffffff
- border (default): 2px #d3deee
- border (emphasis): 2px #1d2a4d with a 5px 5px 0 #1d2a4d shadow
- primary action: #4f46e5 fill, #ffffff label
- correct: #12805c on #dff6ea
- not quite: #c62f3d on #fde8ea
- hint: #5a4300 on #fff1b8, dashed outline

Example Component Prompts:
1. Question card: `ui-card ui-card-pop`; chips row (`ui-chip`); question in Nunito 700 at 19px, colour #1d2a4d.
2. Answer option: white, 2px #d3deee border, 14px radius, min-height 52px, 32px round #eef3fb badge with the letter, text Nunito 700 at 17px.
3. Primary button: `ui-btn ui-btn-primary` — #4f46e5 fill, white Nunito 800, 2px #1d2a4d border, 14px radius, 3px 3px 0 #1d2a4d shadow.
4. Section heading: Fredoka 600 at 22px, colour #1d2a4d.
5. Hint: `ui-hint` — #fff1b8 fill, #5a4300 text at 15px/700, 2px dashed #5a4300 outline.

## Legacy

- `duo-*` Tailwind colours remain as aliases for older pages. `duo-dark` now equals Ink; `duo-green` is a darker green (`#15966a`); `duo-mint` and `duo-blush` equal the Correct and Not-Quite washes.
- Tailwind's `gray` scale is re-tinted to the Ink family, so `text-gray-500` is Muted Ink and `border-gray-200` is Line.
- Some pages still contain hard-coded hex values from the earlier skin (for example `#58CC02`). Replace them with role tokens when touching those pages.

## Quick Start

```tsx
<div className="min-h-screen bg-paper pb-24">
  <div className="sticky top-0 z-40 bg-ink px-4 py-3">
    <h1 className="text-title text-white">Fractions</h1>
  </div>

  <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">
    <div className="ui-card ui-card-pop">
      <span className="ui-chip">Fractions</span>
      <p className="text-question text-ink mt-3">What is half of 18?</p>
    </div>

    <div className="ui-hint">💡 Hint: split 18 into two equal groups.</div>

    <button className="ui-btn ui-btn-primary w-full">Continue →</button>
    <button className="ui-btn w-full">Watch solution</button>
  </div>
</div>
```
