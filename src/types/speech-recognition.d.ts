/**
 * Augment the Window interface with the webkit-prefixed Web Speech API.
 *
 * The standard `SpeechRecognition` and `SpeechRecognitionEvent` types are
 * already provided by TypeScript's `lib.dom.d.ts`.  Safari/older Chrome
 * expose the same API under the `webkit` prefix, so we add that here.
 */
interface Window {
  webkitSpeechRecognition: typeof SpeechRecognition;
}
