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
  const ref = await addDoc(collection(db, 'queries'), {
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
  await updateDoc(doc(db, 'queries', docId), {
    feedbackRating: rating,
    feedbackComment: comment ?? null,
  })
}
