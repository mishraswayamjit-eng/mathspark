/**
 * Prefix stored on a child's chat message that was sent with a photo.
 * The photo itself is shown to the model for that one turn and never stored;
 * this note is what remains in the saved history. Shared by the chat route
 * (which writes it) and the chat UI (which shows a camera in its place).
 */
export const PHOTO_NOTE = '[Sent a photo of their working]';
