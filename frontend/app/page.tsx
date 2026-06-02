'use client'

import ChatWindow from '@/components/ChatWindow'
import Header from '@/components/Header'
import MessageInput from '@/components/MessageInput'
import { useChat } from '@/hooks/useChat'

export default function Home() {
  const { messages, isLoading, error, sendMessage } = useChat()

  return (
    <div className="flex flex-col h-screen bg-white">
      <Header />
      <div className="flex flex-col flex-1 overflow-hidden mt-[68px]">
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          onSuggestedQuestion={sendMessage}
        />
        <MessageInput onSend={sendMessage} disabled={isLoading} error={error} />
      </div>
    </div>
  )
}
