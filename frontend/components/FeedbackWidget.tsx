'use client'

import { useState } from 'react'
import { logFeedback } from '@/lib/analytics'

export default function FeedbackWidget({ docId }: { docId?: string }) {
  const [rating, setRating] = useState<number | null>(null)
  const [comment, setComment] = useState('')
  const [submitted, setSubmitted] = useState(false)

  if (!docId) return null
  if (submitted) return <p className="text-xs text-gray-400 mt-1">Thanks for your feedback!</p>

  const handleSubmit = async (selectedRating: number) => {
    setRating(selectedRating)
    try {
      await logFeedback(docId, selectedRating, comment || undefined)
      setSubmitted(true)
    } catch {
      // fire-and-forget — never block UI on analytics failure
    }
  }

  return (
    <div className="mt-1" aria-label="Rate this response">
      {rating === null ? (
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-400">Helpful?</span>
          <button
            onClick={() => handleSubmit(5)}
            className="text-lg leading-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded hover:scale-110 transition-transform min-h-[44px] min-w-[44px] flex items-center justify-center"
            aria-label="Thumbs up — helpful"
          >
            👍
          </button>
          <button
            onClick={() => setRating(1)}
            className="text-lg leading-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded hover:scale-110 transition-transform min-h-[44px] min-w-[44px] flex items-center justify-center"
            aria-label="Thumbs down — not helpful"
          >
            👎
          </button>
        </div>
      ) : (
        <div className="flex flex-col gap-1.5">
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="What went wrong? (optional)"
            rows={2}
            className="text-xs border border-gray-200 rounded-lg px-2 py-1.5 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 w-full max-w-xs"
            aria-label="Optional feedback comment"
            style={{ fontSize: '16px' }}
          />
          <button
            onClick={() => handleSubmit(rating)}
            className="self-start text-xs bg-blue-600 text-white px-3 py-1.5 rounded-full hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1"
            aria-label="Submit feedback"
          >
            Submit feedback
          </button>
        </div>
      )}
    </div>
  )
}
