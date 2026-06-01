'use client'

import { useCallback } from 'react'
import { logQuery } from '@/lib/analytics'
import { postQuery } from '@/lib/api'
import { useChatStore } from '@/store/chatStore'
import { useSession } from './useSession'

export function useChat() {
  const { messages, isLoading, error, addMessage, updateMessage, setLoading, setError } =
    useChatStore()
  const sessionId = useSession()

  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim() || isLoading) return

      const userMsgId = crypto.randomUUID()
      addMessage({ id: userMsgId, role: 'user', content: text.trim(), timestamp: Date.now() })
      setLoading(true)
      setError(null)

      const start = Date.now()

      try {
        const history = messages.slice(-10).map((m) => ({ role: m.role, content: m.content }))
        const res = await postQuery(text.trim(), history)

        const assistantMsgId = crypto.randomUUID()
        addMessage({
          id: assistantMsgId,
          role: 'assistant',
          content: res.answer,
          sources: res.sources,
          timestamp: Date.now(),
        })

        if (sessionId) {
          logQuery({
            sessionId,
            userMessage: text.trim(),
            assistantAnswer: res.answer,
            sourcesUsed: res.sources.map((s) => s.label),
            sourceUrls: res.sources.map((s) => s.url),
            responseTimeMs: Date.now() - start,
            historyLength: messages.length,
          })
            .then((docId) => updateMessage(assistantMsgId, { docId }))
            .catch(() => {})
        }
      } catch {
        setError('Could not reach the server. Check your connection and try again.')
      } finally {
        setLoading(false)
      }
    },
    [messages, isLoading, sessionId, addMessage, updateMessage, setLoading, setError],
  )

  return { messages, isLoading, error, sendMessage }
}
