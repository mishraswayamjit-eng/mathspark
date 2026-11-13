'use client';

import Sparky from '@/components/Sparky';

export interface ChatBubbleMsg {
  role: 'user' | 'assistant';
  content: string;
  /** Preview of a photo the child sent with this message. */
  imageUrl?: string;
}

interface MessageBubbleProps {
  msg: ChatBubbleMsg;
  studentInitial: string;
}

/**
 * Presentational chat bubble shared by the full `/chat` page and the floating
 * Sparky widget. Height-agnostic — no viewport assumptions so it slots into any
 * scroll container.
 */
export default function MessageBubble({ msg, studentInitial }: MessageBubbleProps) {
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

  return (
    <div className="flex items-end gap-2 mb-3">
      <div className="flex-shrink-0">
        <Sparky mood="happy" size={36} />
      </div>
      <div className="max-w-[85%] bg-white rounded-card rounded-bl-sm px-4 py-2.5 border-2 border-line">
        <p className="text-[15px] leading-relaxed text-ink font-medium whitespace-pre-wrap [overflow-wrap:anywhere]">{msg.content}</p>
      </div>
    </div>
  );
}
