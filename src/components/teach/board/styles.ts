/**
 * The board's animations. Every animated element's resting style is its
 * finished state, and the keyframes only describe where it starts from, so
 * removing the animation (an op that is no longer new, or reduced motion)
 * leaves the element fully drawn.
 */
export const BOARD_CSS = `
@keyframes wb-draw {
  0% { stroke-dashoffset: 1; opacity: 0; }
  2% { opacity: 1; }
  100% { stroke-dashoffset: 0; opacity: 1; }
}
@keyframes wb-fade {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes wb-write {
  from { -webkit-clip-path: inset(-25% 100% -25% -5%); clip-path: inset(-25% 100% -25% -5%); }
  to { -webkit-clip-path: inset(-25% -5% -25% -5%); clip-path: inset(-25% -5% -25% -5%); }
}
.wb-dash { stroke-dasharray: 1; }
@media (prefers-reduced-motion: reduce) {
  .wb-anim { animation: none !important; }
}
`;
