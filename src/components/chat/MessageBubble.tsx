'use client';

import Sparky from '@/components/Sparky';
import VisualBoard from '@/components/visuals/VisualBoard';
import { extractVisual, type VisualSpec } from '@/lib/visuals/spec';
import { VISUAL_LIBRARY } from '@/lib/visuals/topicMap';

export interface ChatBubbleMsg {
  role: 'user' | 'assistant';
  content: string;
  /** Preview of a photo the child sent with this message. */
  imageUrl?: string;
}

interface MessageBubbleProps {
  msg: ChatBubbleMsg;
  studentInitial: string;
  /**
   * Provided when a whiteboard panel sits beside the conversation (wide
   * screens): the picture is then drawn there, and the bubble offers a button
   * to bring an earlier picture back onto the board. On narrow screens, and
   * when this is not provided, the picture is drawn inside the bubble.
   */
  onShowVisual?: (visual: VisualSpec) => void;
}

/**
 * Presentational chat bubble shared by the full `/chat` page and the floating
 * Sparky widget. Height-agnostic — no viewport assumptions so it slots into any
 * scroll container.
 */
export default function MessageBubble({ msg, studentInitial, onShowVisual }: MessageBubbleProps) {
  const isUser = msg.role === 'user';

  if (isUser) {
    return (
      <div className="flex justify-end items-end gap-2 mb-3">
        <div className="max-w-[78%] bg-action text-white rounded-card rounded-br-sm px-4 py-2.5">
          {msg.imageUrl && (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={msg.imageUrl}
              alt="Photo you sent"
              className="rounded-note border-2 border-white/40 mb-2 max-h-56 w-auto"
            />
          )}
          <p className="text-sm leading-relaxed font-medium whitespace-pre-wrap [overflow-wrap:anywhere]">{msg.content}</p>
        </div>
        <div className="w-8 h-8 rounded-full bg-ink flex items-center justify-center text-white font-extrabold text-sm flex-shrink-0">
          {studentInitial}
        </div>
      </div>
    );
  }

  // Sparky's reply may carry a whiteboard picture: draw it, never show its tag.
  const { text, visual } = extractVisual(msg.content);

  return (
    <div className="flex items-end gap-2 mb-3">
      <div className="flex-shrink-0">
        <Sparky mood="happy" size={36} />
      </div>
      <div className={`bg-white rounded-card rounded-bl-sm px-4 py-2.5 border-2 border-line ${visual ? 'w-[92%] lg:w-auto lg:max-w-[85%]' : 'max-w-[85%]'}`}>
        {visual && (
          <div className={`mb-3 pb-3 border-b-2 border-line ${onShowVisual ? 'lg:hidden' : ''}`}>
            <VisualBoard spec={visual} />
          </div>
        )}
        {text && (
          <p className="text-[15px] leading-relaxed text-ink font-medium whitespace-pre-wrap [overflow-wrap:anywhere]">{text}</p>
        )}
        {visual && onShowVisual && (
          <button
            type="button"
            onClick={() => onShowVisual(visual)}
            className="hidden lg:inline-flex items-center gap-2 mt-2 min-h-[48px] px-3 rounded-control border-2 border-line bg-soft text-ink text-[13px] font-extrabold hover:border-ink transition-colors"
          >
            <span aria-hidden="true">{VISUAL_LIBRARY[visual.type].emoji}</span>
            Show on the whiteboard
          </button>
        )}
      </div>
    </div>
  );
}
