'use client'

import { useEffect, useRef } from 'react'
import { Message } from '@/store/chatStore'
import ChatBubble from './ChatBubble'
import LoadingDots from './LoadingDots'

interface Props {
  messages: Message[]
  isLoading: boolean
}

export default function ChatWindow({ messages, isLoading }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  return (
    <div
      className="flex-1 overflow-y-auto px-4 py-4"
      role="log"
      aria-label="Conversation"
      aria-live="polite"
    >
      {messages.length === 0 && (
        <div className="flex flex-col items-center justify-center h-full text-center text-gray-400 gap-3 pt-12">
          <span className="text-5xl" aria-hidden="true">♿</span>
          <p className="text-base font-medium text-gray-600">How can I help you?</p>
          <p className="text-sm max-w-xs text-gray-400">
            Ask about SEN support at TP, disability transport, care services, or employment schemes in Singapore.
          </p>
        </div>
      )}

      {messages.map((msg) => (
        <ChatBubble key={msg.id} message={msg} />
      ))}

      {isLoading && (
        <div className="flex items-start mb-3">
          <div className="bg-gray-100 rounded-2xl rounded-bl-sm">
            <LoadingDots />
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  )
}
