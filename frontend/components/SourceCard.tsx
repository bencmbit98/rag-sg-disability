'use client'

import { useState } from 'react'
import { Source } from '@/lib/api'

export default function SourceCard({ source }: { source: Source }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className="border border-gray-200 rounded-lg bg-white shadow-sm text-xs overflow-hidden">
      <button
        className="w-full flex items-center justify-between px-3 py-2 text-left hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-inset min-h-[44px]"
        onClick={() => setExpanded((v) => !v)}
        aria-expanded={expanded}
        aria-label={`Source: ${source.title || source.label}. ${expanded ? 'Collapse' : 'Expand'} snippet.`}
      >
        <div className="flex items-center gap-2 min-w-0">
          <span className="flex-shrink-0 bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-medium">
            {source.label.replace(/_/g, ' ')}
          </span>
          <span className="text-gray-700 font-medium truncate">{source.title || source.url}</span>
        </div>
        <span className="flex-shrink-0 ml-2 text-gray-400">{expanded ? '▲' : '▼'}</span>
      </button>

      {expanded && (
        <div className="px-3 pb-3 space-y-2 border-t border-gray-100">
          <p className="text-gray-600 leading-relaxed pt-2">{source.snippet}</p>
          <a
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block text-blue-600 hover:underline focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
            aria-label={`Open full source page for ${source.title} (opens in new tab)`}
          >
            View full source →
          </a>
        </div>
      )}
    </div>
  )
}
