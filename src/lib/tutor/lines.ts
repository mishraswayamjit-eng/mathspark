/**
 * The tutor's lines: everything it can say in reaction to the child.
 *
 * Every line is spoken by a text-to-speech voice, so a line is speakable words
 * only: letters, digits, commas, full stops, question marks, the odd
 * exclamation mark and apostrophes. No emoji, no symbols, no hyphens.
 *
 * Placeholders, filled in by `tutorLine`:
 *   ", {name}"  the child's first name. Always written with the comma in
 *               front, so the line still reads well when the name is unknown
 *               and the whole ", {name}" is removed.
 *   "{n}"       the length of a long run of right answers.
 *   "{c}" "{t}" right answers and questions in a finished session.
 *   "{topic}"   the topic practised ("this topic" when it is not known).
 *
 * Tone rules the tests hold these to: never "wrong", "incorrect", "oops",
 * "failed" or "error"; a miss never hears the word "no"; praise is for effort,
 * method and persistence, never for being clever; about one line in eight uses
 * the name; well under a third end in an exclamation mark.
 *
 * Most pools have a prime number of lines (7, 11, 13, 17). The picker steps
 * through a pool by the turn number, and with a prime length it visits every
 * line before repeating whatever the gap between turns happens to be.
 */

// ── A question appears ───────────────────────────────────────────────────────

/** The first question of a session. */
const welcome: string[] = [
  "Hello, {name}. Let's begin. Take your time with each one.",
  "Ready? Read the first one carefully, and off we go.",
  "Good to see you. Let's warm up with this one.",
  "Here we go. Keep a pencil ready, if you like to write things down.",
  "Let's start. There is plenty of time, so read it properly.",
  "Welcome back. The first question is up.",
  "All set? Here comes the first one.",
];

/** A later question. Said only now and then: mostly the child is left to read. */
const nextQuestion: string[] = [
  "Next one.",
  "Here is another.",
  "Read this one slowly.",
  "On to the next.",
  "Fresh question. Take your time.",
  "See what this one is asking.",
  "Look for what it wants before you start.",
];

// ── A right answer ───────────────────────────────────────────────────────────

/** Right, and fast. */
const correctQuick: string[] = [
  "That was quick!",
  "Quick and right. You know this one well.",
  "You have practised this, I can tell.",
  "Straight to it. Good.",
  "Fast work, and correct.",
  "That did not take long at all.",
  "Quick one for you!",
  "You did not waste a second there.",
  "You saw that at once. Nice.",
  "Done already? Correct.",
  "Nicely done, {name}. That was fast.",
  "That one gave you little trouble.",
  "Right, and quickly too.",
];

/** Right after a long time on the question: praise the staying power. */
const correctHardWon: string[] = [
  "You stuck with that one. Well done.",
  "That took some thinking, and you did it.",
  "Good. You did not rush, and it paid off.",
  "Slow and careful got you there.",
  "That was a hard one. You stayed with it!",
  "Worth the time you gave it. Correct.",
  "I like how you kept at it.",
  "Patience, {name}. That is what solved it.",
  "You worked that through properly. Correct.",
  "Not an easy one, and you got it.",
  "See what careful work does? Right answer.",
  "You took your time over it. Very good.",
  "You thought it through to the end. That is the habit to keep.",
];

/** Right after opening a hint. */
const correctAfterHint: string[] = [
  "See, the hint was all you needed.",
  "Good use of the hint.",
  "You took the hint and did the rest yourself.",
  "A small push, and you finished it.",
  "That is what hints are for. Well done.",
  "Asking for help and then solving it. That is good learning.",
  "The hint opened it up, and you did the working.",
  "Right. Next time you may not need the hint for this kind.",
  "Good, {name}. You used the hint well.",
  "Hint first, then your own steps. Correct.",
  "You read the clue properly. That is why it worked.",
];

/** Right straight after a miss. */
const correctComeback: string[] = [
  "There you go. That is how you come back.",
  "Better. You did not let the last one bother you.",
  "Back on track.",
  "Good recovery!",
  "See? One miss does not decide anything.",
  "That is the way. Shake it off and carry on.",
  "Nicely picked up, {name}.",
];

/** An ordinary right answer. Some of these are skipped altogether. */
const correctPlain: string[] = [
  "Correct.",
  "Yes, that is it.",
  "Very good.",
  "Right. Carry on.",
  "Good work.",
  "That is the one.",
  "Well done!",
  "Yes. Nicely worked out.",
  "Right you are.",
  "Full marks for that one.",
  "Good, {name}. Keep going.",
  "Correct, and neatly done.",
  "That is right.",
  "You got it.",
  "Exactly.",
  "Good going.",
  "Spot on.",
];

/** The third right answer in a row. */
const streakThree: string[] = [
  "Three in a row!",
  "That makes 3 in a row. You are in rhythm now.",
  "Three right, one after another. Keep that going.",
  "Hat trick!",
  "3 on the trot. Steady work.",
  "Three in a row, {name}. Nice and steady.",
  "One, two, three, all correct.",
];

/** The fifth right answer in a row. */
const streakFive: string[] = [
  "Five in a row!",
  "That is 5 straight. You are really concentrating today.",
  "Five without a slip. Good focus.",
  "5 in a row, {name}. That is steady work.",
  "Five on the trot! Keep the same care on the next one.",
  "Five correct, back to back. Your practice is showing.",
  "That is five. Same care on the next, please.",
];

/** A long run: 10, 15, 20 and so on. */
const streakLong: string[] = [
  "{n} in a row!",
  "That is {n} in a row. I am just watching now.",
  "{n} straight. You are on a fine run.",
  "{n} right, one after another. Wonderful concentration.",
  "Still going. {n} in a row.",
  "{n} without a slip, {name}. Superb effort.",
  "{n} now. Lovely steady work.",
];

// ── A miss ───────────────────────────────────────────────────────────────────

/** The first miss, when the question has no note on why the choice tempts. */
const missFirst: string[] = [
  "Not quite. Have another look.",
  "Hmm, not this one. Read the question once more.",
  "Almost. Go through your steps once more.",
  "Let's look again. What is the question really asking?",
  "Not yet. Take a breath and try once more.",
  "That is not it, but you are thinking. Try again.",
  "Do one thing. Read it again, slowly, and then choose.",
  "Have a second look, {name}. Something small may have slipped.",
  "Good try. Go back over the numbers in the question.",
  "Let's think about this together. Where did you start?",
  "Not quite there. Try it one more time.",
  "Check that step again. You can get this.",
  "Something slipped along the way. Have another go.",
];

/** The second miss in a row: slow down, and a hint is on offer. */
const missSecond: string[] = [
  "Still not it. Slow down and write the steps out.",
  "Let's take it step by step. What do we know first?",
  "Not yet. A hint might help here.",
  "This one is tricky. Try the pencil pad and work it out there.",
  "Hold on. Read each choice carefully before you pick.",
  "Don't guess, {name}. Work it out, and take the hint if you need it.",
  "It is fine to find this hard. Shall we look at a hint?",
  "Try a different way this time. The hint can show you where to begin.",
  "Not this one either. Go line by line this time.",
  "Let's slow it down. Which part are you sure about?",
  "Have one more careful try, or open the hint.",
];

/** Three or more misses in a row: time for real help. */
const missMany: string[] = [
  "This one is being stubborn. Tap Explain it to me and we will do it together.",
  "Let's not struggle alone. Take a hint, or ask me to explain it.",
  "Time for some help. Open the hint and read it slowly.",
  "You have tried hard on this. Let me explain it, just tap Explain it to me.",
  "Some questions need a second teaching. Try Explain it to me.",
  "Keep calm, {name}. A hint will show you the first step.",
  "It happens to everyone. Let's go through it together with Explain it to me.",
];

/** Said before the question's own note on why the chosen answer tempts. */
const missFrames: string[] = [
  "Ah, I can see how you got there.",
  "I see what happened.",
  "That is a very common slip.",
  "Easy one to fall for.",
  "I know why that looked right.",
  "Many children pick that one.",
  "That choice is tempting.",
];

/** Said after the note, when there is room, to point the child forward. */
const missTails: string[] = [
  "Have another go.",
  "Try once more.",
  "Now try again.",
  "Give it one more try.",
  "See if that changes your answer.",
];

// ── A hint is opened ─────────────────────────────────────────────────────────

/** Hint 1: an idea. */
const hintIdea: string[] = [
  "Here is an idea to start you off.",
  "A small clue. See what it reminds you of.",
  "Think about this first.",
  "Just a pointer, the rest is yours.",
  "Read this clue, then look at the question again.",
  "Here is something to think about.",
  "A little nudge. Read it and think.",
];

/** Hint 2: a first move. */
const hintFirstMove: string[] = [
  "Here is the first step. You take it from there.",
  "Let's get you started. Do this bit first.",
  "This shows you where to begin.",
  "One step is given. See if you can do the next.",
  "Start the way this says, then carry on yourself.",
  "A bigger clue this time. Try the first move.",
  "Here is how to open it up. Then it is over to you.",
];

/** Hint 3: an example to copy. */
const hintExample: string[] = [
  "Here is a similar one, solved. Do yours the same way.",
  "Look at this example, then copy the method.",
  "Watch how this one is done. Yours works the same way.",
  "An example for you. Follow the same steps with your numbers.",
  "See the worked example. Now try yours, step by step.",
  "This one is solved for you. Use it as a pattern.",
  "Here is one like it, worked out. Notice each step.",
];

// ── A long pause ─────────────────────────────────────────────────────────────

/** A short pause: suggest writing it out. */
const idleSoft: string[] = [
  "Take your time. Writing it on the pencil pad may help.",
  "Still thinking? That is fine. Try working it out on the pad.",
  "There is time. Jot the numbers down if it helps.",
  "Thinking is good. Read the question once more if you are stuck.",
  "I am here. Try the first step on the pencil pad.",
  "Slowly is fine. What is the question asking for?",
  "Good that you are thinking it over. Try drawing it on the pad.",
];

/** A longer pause: offer a hint. */
const idleHint: string[] = [
  "Stuck? There is a hint if you want one.",
  "Would a hint help? It is right there.",
  "You can open a hint any time. It is not cheating.",
  "If it is not coming, take the first hint.",
  "Try the hint, {name}. It will give you a place to start.",
  "A hint may get you moving. Have a look.",
  "Want a clue? The first hint is a gentle one.",
];

/** A very long pause: offer to explain. */
const idleLong: string[] = [
  "Shall we do this one together? Tap Explain it to me.",
  "This has taken a while. A hint, or Explain it to me, will help.",
  "Still with me? Take a hint and let's get going.",
  "Let me help. Explain it to me will walk you through it.",
  "It is okay to ask. Open the hint, or let me explain.",
  "If you need a break, take one. Otherwise, try the hint.",
  "We have been on this one a while. Let me explain it, if you like.",
];

// ── The pencil pad ───────────────────────────────────────────────────────────

/** The child started writing their working. Said only now and then. */
const startedWorking: string[] = [
  "Good, write it out.",
  "That is the way. Working on paper helps.",
  "Nice. Show your steps.",
  "Yes, put it down on the pad.",
  "Writing it out. I like that.",
  "Good habit, {name}.",
  "Neat steps make fewer slips.",
];

// ── The end of a session ─────────────────────────────────────────────────────

/** Every answer right. */
const endAllRight: string[] = [
  "All {t} right. That was careful work from start to finish.",
  "{c} out of {t}! Every single one. Your practice is showing.",
  "A full score, {name}. You earned it with steady work.",
  "Not one slip in {t} questions. Well done today.",
  "All correct. Next time we can try something a little harder.",
  "{t} out of {t}. You concentrated the whole way through.",
];

/** Three quarters or more right. */
const endMostRight: string[] = [
  "{c} out of {t}. Good session. Look again at the ones that slipped.",
  "Most of them right. {c} out of {t} is solid work.",
  "{c} right out of {t}. A little more care and you will have them all.",
  "Well done, {name}. {c} out of {t}, and you kept going throughout.",
  "Good practice today. {c} out of {t}, with only a few to revise.",
  "{c} out of {t}! Go over the misses once and you are set.",
];

/** Around half right. */
const endAboutHalf: string[] = [
  "{c} out of {t}. A fair start. We will practise {topic} some more.",
  "About half right. The other half will come with practice.",
  "{c} out of {t} today. Have a look at the solutions for the ones you missed.",
  "You got {c} of {t}. Good effort. Next time, use the hints a little earlier.",
  "Some went well, some did not. {c} out of {t}. Let's keep at it.",
  "{c} right out of {t}. You are getting there, {name}. More practice tomorrow.",
];

/** A hard session. Honest: credit the effort, and name what comes next. */
const endHard: string[] = [
  "That was a hard session, and you finished it. Next we go through the solutions together.",
  "{c} out of {t} today. These were tough. Try Explain it to me on the ones you missed.",
  "Not your easiest day, but you did not give up. We will take {topic} slower next time.",
  "You kept trying right to the end. Now let's look at where it went off, one question at a time.",
  "Tough set. The effort counts, {name}. Next, read the solutions and try these again.",
  "This needs more time, and that is all right. Start with the hints next session.",
];

/** A session too short to score (fewer than 3 questions). */
const endShort: string[] = [
  "That is all for now. See you next time.",
  "Done for now. Come back soon.",
  "Short session today. Good that you practised.",
  "We stop here. See you soon.",
  "Finished for today. A little practice every day adds up.",
  "That is the lot. Until next time.",
];

export const LINES = {
  welcome,
  nextQuestion,
  correctQuick,
  correctHardWon,
  correctAfterHint,
  correctComeback,
  correctPlain,
  streakThree,
  streakFive,
  streakLong,
  missFirst,
  missSecond,
  missMany,
  missFrames,
  missTails,
  hintIdea,
  hintFirstMove,
  hintExample,
  idleSoft,
  idleHint,
  idleLong,
  startedWorking,
  endAllRight,
  endMostRight,
  endAboutHalf,
  endHard,
  endShort,
};

export type LinePool = keyof typeof LINES;
