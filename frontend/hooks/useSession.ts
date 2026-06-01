'use client'

import { useEffect, useState } from 'react'

export function useSession(): string {
  const [sessionId, setSessionId] = useState('')

  useEffect(() => {
    let id = localStorage.getItem('sg_disability_session')
    if (!id) {
      id = crypto.randomUUID()
      localStorage.setItem('sg_disability_session', id)
    }
    setSessionId(id)
  }, [])

  return sessionId
}
