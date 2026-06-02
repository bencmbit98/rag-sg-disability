'use client'

import Link from 'next/link'
import { useChatStore } from '@/store/chatStore'

export default function Header() {
  const { messages, clear } = useChatStore()

  return (
    <header className="fixed top-0 left-0 right-0 z-10 bg-purple-700 text-white px-4 py-3 flex items-center justify-between shadow-md">
      <div>
        <h1 className="text-lg font-semibold leading-tight">Special Education Needs Support</h1>
        <p className="text-xs text-purple-200">Temasek Polytechnic (Singapore)</p>
      </div>
      <div className="flex items-center gap-2">
        {messages.length > 0 && (
          <button
            onClick={clear}
            className="text-xs text-purple-200 hover:text-white border border-purple-400 hover:border-white rounded-lg px-3 py-1.5 min-h-[44px] flex items-center focus:outline-none focus:ring-2 focus:ring-white transition-colors"
            aria-label="Clear chat history"
          >
            Clear chat
          </button>
        )}
        <Link
          href="/about"
          className="text-sm text-purple-100 hover:text-white underline underline-offset-2 focus:outline-none focus:ring-2 focus:ring-white rounded px-1 min-h-[44px] flex items-center"
          aria-label="About this app and data sources"
        >
          About
        </Link>
      </div>
    </header>
  )
}
