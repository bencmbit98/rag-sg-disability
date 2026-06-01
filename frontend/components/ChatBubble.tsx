import { Message } from '@/store/chatStore'
import FeedbackWidget from './FeedbackWidget'
import SourceCard from './SourceCard'

export default function ChatBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} gap-1 mb-3`}>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap ${
          isUser
            ? 'bg-blue-600 text-white rounded-br-sm'
            : 'bg-gray-100 text-gray-900 rounded-bl-sm'
        }`}
        aria-label={isUser ? 'Your message' : 'Assistant response'}
      >
        {message.content}
      </div>

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
