'use client'

import { useState } from 'react'
import { Source } from '@/lib/api'

export default function SourceCard({ source }: { source: Source }) {
  const [expanded, setExpanded] = useState(false)
  const preview = source.snippet.slice(0, 120) + (source.snippet.length > 120 ? '…' : '')

  return (
    <div className="border border-gray-200 rounded-xl bg-white shadow-sm text-xs overflow-hidden">
      <button
        className="w-full flex items-center justify-between px-3 py-2 text-left hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-inset min-h-[44px]"
        onClick={() => setExpanded((v) => !v)}
        aria-expanded={expanded}
        aria-label={`Source: ${source.title || source.label}. ${expanded ? 'Collapse' : 'Expand'} snippet.`}
      >
        <div className="flex items-center gap-2 min-w-0">
          <span className="flex-shrink-0 bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full font-medium">
            {source.label.replace(/_/g, ' ')}
          </span>
          <span className="text-gray-700 font-medium truncate">{source.title || source.url}</span>
        </div>
        <span className="flex-shrink-0 ml-2 text-gray-400">{expanded ? '▲' : '▼'}</span>
      </button>

      <div className="px-3 pb-3 border-t border-gray-100 pt-2 space-y-2">
        <p className="text-gray-600 leading-relaxed">
          {expanded ? source.snippet : preview}
        </p>
        <div className="flex items-center justify-between">
          {source.snippet.length > 120 && (
            <button
              onClick={() => setExpanded((v) => !v)}
              className="text-purple-600 hover:underline focus:outline-none focus:ring-2 focus:ring-purple-500 rounded text-xs"
            >
              {expanded ? 'Show less' : 'Show more'}
            </button>
          )}
          <a
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-purple-600 hover:underline focus:outline-none focus:ring-2 focus:ring-purple-500 rounded ml-auto"
            aria-label={`Open full source page for ${source.title} (opens in new tab)`}
          >
            View source →
          </a>
        </div>
      </div>
    </div>
  )
}
