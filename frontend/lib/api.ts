export interface Source {
  label: string
  url: string
  title: string
  snippet: string
}

export interface QueryResponse {
  answer: string
  sources: Source[]
  is_in_scope: boolean
  top_similarity_score: number
  refusal_reason: string | null
  pages_searched: number
}

export interface HistoryMessage {
  role: 'user' | 'assistant'
  content: string
}

export async function postQuery(
  message: string,
  history: HistoryMessage[],
): Promise<QueryResponse> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error((err as { detail?: string }).detail ?? 'Query failed')
  }
  return res.json()
}
