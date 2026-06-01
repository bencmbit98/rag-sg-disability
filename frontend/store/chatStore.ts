import { create } from 'zustand'
import { Source } from '@/lib/api'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  sources?: Source[]
  docId?: string
  timestamp: number
}

interface ChatState {
  messages: Message[]
  isLoading: boolean
  error: string | null
  addMessage: (msg: Message) => void
  updateMessage: (id: string, update: Partial<Message>) => void
  setLoading: (v: boolean) => void
  setError: (v: string | null) => void
  clear: () => void
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isLoading: false,
  error: null,
  addMessage: (msg) => set((s) => ({ messages: [...s.messages, msg] })),
  updateMessage: (id, update) =>
    set((s) => ({
      messages: s.messages.map((m) => (m.id === id ? { ...m, ...update } : m)),
    })),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  clear: () => set({ messages: [], error: null }),
}))
