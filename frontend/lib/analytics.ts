import { addDoc, collection, doc, serverTimestamp, updateDoc } from 'firebase/firestore'
import { db } from './firebase'

export async function logQuery(data: {
  sessionId: string
  userMessage: string
  assistantAnswer: string
  sourcesUsed: string[]
  sourceUrls: string[]
  responseTimeMs: number
  historyLength: number
}): Promise<string> {
  const store = db
  if (!store) return ''
  const ref = await addDoc(collection(store, 'queries'), {
    ...data,
    feedbackRating: null,
    feedbackComment: null,
    userAgent: navigator.userAgent,
    screenWidth: window.innerWidth,
    language: navigator.language,
    timestamp: serverTimestamp(),
  })
  return ref.id
}

export async function logFeedback(
  docId: string,
  rating: number,
  comment?: string,
): Promise<void> {
  const store = db
  if (!store) return
  await updateDoc(doc(store, 'queries', docId), {
    feedbackRating: rating,
    feedbackComment: comment ?? null,
  })
}
