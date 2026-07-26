'use client'

import { useEffect, useRef } from 'react'
import { Message } from '@/store/chatStore'
import ChatBubble from './ChatBubble'
import LoadingDots from './LoadingDots'

const SUGGESTED_QUESTIONS = [
  'What are the SEN funds I can tap on to apply for Assistive Technology (Specialised Support)?',
  'I want to get assistive technology.',
  'How do I make an appointment with a SEN officer?',
]

interface Props {
  messages: Message[]
  isLoading: boolean
  onSuggestedQuestion: (question: string) => void
}

export default function ChatWindow({ messages, isLoading, onSuggestedQuestion }: Props) {
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
        <div className="flex flex-col items-center justify-center h-full text-center gap-4 pt-8">
          <span className="text-5xl" aria-hidden="true">♿</span>
          <div>
            <p className="text-base font-semibold text-gray-700">How can I help you today?</p>
            <p className="text-sm text-gray-400 mt-1">
              Ask about SEN support, transport, care, or employment for persons with disabilities in Singapore.
            </p>
          </div>
          <div className="flex flex-wrap justify-center gap-2 max-w-sm mt-2">
            {SUGGESTED_QUESTIONS.map((q) => (
              <button
                key={q}
                onClick={() => onSuggestedQuestion(q)}
                className="text-sm bg-purple-50 text-purple-700 border border-purple-200 rounded-full px-4 py-2 hover:bg-purple-100 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-colors text-left"
                aria-label={`Ask: ${q}`}
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {messages.map((msg) => (
        <ChatBubble key={msg.id} message={msg} />
      ))}

      {isLoading && (
        <div className="flex items-start mb-3">
          <div className="bg-gray-100 rounded-3xl rounded-bl-sm shadow-md">
            <LoadingDots />
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  )
}
