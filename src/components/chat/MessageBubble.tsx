'use client';

import Sparky from '@/components/Sparky';

export interface ChatBubbleMsg {
  role: 'user' | 'assistant';
  content: string;
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
        <div className="max-w-[78%] bg-duo-green text-white rounded-2xl rounded-br-sm px-4 py-2.5 shadow-sm">
          <p className="text-sm leading-relaxed font-medium">{msg.content}</p>
        </div>
        <div className="w-8 h-8 rounded-full bg-duo-blue flex items-center justify-center text-white font-extrabold text-sm flex-shrink-0">
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
      <div className="max-w-[78%] bg-white rounded-2xl rounded-bl-sm px-4 py-2.5 shadow-sm border border-gray-100">
        <p className="text-sm leading-relaxed text-gray-800 font-medium whitespace-pre-wrap">{msg.content}</p>
      </div>
    </div>
  );
}
