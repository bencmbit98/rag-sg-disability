'use client'

import { KeyboardEvent, useRef, useState } from 'react'

interface Props {
  onSend: (text: string) => void
  disabled: boolean
  error: string | null
}

export default function MessageInput({ onSend, disabled, error }: Props) {
  const [text, setText] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSend = () => {
    if (!text.trim() || disabled) return
    onSend(text)
    setText('')
    textareaRef.current?.focus()
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex-shrink-0 border-t border-gray-200 bg-white px-3 pt-2 pb-[calc(0.5rem+env(safe-area-inset-bottom))]">
      {error && (
        <p className="text-red-600 text-xs mb-2 px-1" role="alert" aria-live="assertive">
          {error}
        </p>
      )}
      <div className="flex items-end gap-2">
        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about SEN support, transport, care…"
          rows={2}
          disabled={disabled}
          className="flex-1 resize-none rounded-2xl border border-gray-300 px-4 py-3 leading-snug focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 min-h-[52px] max-h-32"
          aria-label="Type your question"
          style={{ fontSize: '16px' }}
        />
        <button
          onClick={handleSend}
          disabled={disabled || !text.trim()}
          className="flex-shrink-0 w-11 h-11 rounded-full bg-blue-600 text-white flex items-center justify-center hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
          aria-label="Send message"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5" aria-hidden="true">
            <path d="M3.105 2.288a.75.75 0 0 0-.826.95l1.414 4.926A1.5 1.5 0 0 0 5.135 9.25h6.115a.75.75 0 0 1 0 1.5H5.135a1.5 1.5 0 0 0-1.442 1.086l-1.414 4.926a.75.75 0 0 0 .826.95 28.897 28.897 0 0 0 15.293-7.155.75.75 0 0 0 0-1.114A28.897 28.897 0 0 0 3.105 2.288Z" />
          </svg>
        </button>
      </div>
      <p className="text-center text-xs text-gray-400 mt-1 pb-0.5">
        Enter to send · Shift+Enter for new line
      </p>
    </div>
  )
}
