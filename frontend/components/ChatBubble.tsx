import { Message } from '@/store/chatStore'
import FeedbackWidget from './FeedbackWidget'
import SourceCard from './SourceCard'

export default function ChatBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user'
  const isOutOfScope = !isUser && message.isInScope === false

  const time = new Date(message.timestamp).toLocaleTimeString('en-SG', {
    hour: '2-digit',
    minute: '2-digit',
  })

  return (
    <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} gap-1 mb-4`}>
      <div
        className={`max-w-[85%] rounded-3xl px-4 py-3 text-base leading-relaxed whitespace-pre-wrap shadow-md ${
          isUser
            ? 'bg-purple-600 text-white rounded-br-sm'
            : isOutOfScope
            ? 'bg-amber-50 text-amber-900 border border-amber-200 rounded-bl-sm'
            : 'bg-gray-100 text-gray-900 rounded-bl-sm'
        }`}
        aria-label={isUser ? 'Your message' : 'Assistant response'}
      >
        {isOutOfScope && (
          <p className="text-amber-600 text-sm font-medium mb-1.5 flex items-center gap-1">
            <span aria-hidden="true">ℹ️</span> Outside my knowledge area
          </p>
        )}
        {message.content}
      </div>

      <p className={`text-xs text-gray-400 px-1 ${isUser ? 'text-right' : 'text-left'}`}>
        {time}
      </p>

      {!isUser && message.sources && message.sources.length > 0 && (
        <div className="max-w-[85%] w-full space-y-1.5 mt-0.5">
          {message.sources.map((source) => (
            <SourceCard key={source.url} source={source} />
          ))}
        </div>
      )}

      {!isUser && <FeedbackWidget docId={message.docId} />}
    </div>
  )
}
