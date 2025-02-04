'use client';

import { Message } from '../types';
import { Bot } from 'lucide-react';

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  return (
    <div className={`flex items-start gap-4 ${message.role === 'user' ? 'justify-end' : ''}`}>
      {message.role === 'assistant' && (
        <div className="w-8 h-8 rounded-full bg-violet-600 flex items-center justify-center">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}
      <div className={`max-w-[80%] rounded-lg p-4 ${
        message.role === 'assistant' 
          ? 'bg-gray-100' 
          : 'bg-violet-600 text-white'
      }`}>
        <p className="text-sm">{message.content}</p>
      </div>
    </div>
  );
}