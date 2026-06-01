# CLAUDE.md — SEN & Disability Support RAG Web App
# 100% Free & Open Source — Zero Cost Stack

> This file is the single source of truth for Claude Code.
> Read it fully before making any changes. Update it when decisions change.
> **Total infrastructure cost: $0.00**

---

## Project Purpose

A **mobile-friendly Progressive Web App (PWA) RAG chatbot** that helps students,
persons with disabilities, and caregivers in Singapore find relevant support services
by asking natural-language questions.

Users open it in any mobile or desktop browser — no app store, no install.
"Add to Home Screen" on iOS Safari and Chrome Android gives a native app feel.

Beyond answering questions, the app **logs every interaction to Firestore** so
the team can analyse what users ask, which sources help most, and collect
thumbs-up/down feedback to continuously improve the app.

---

## Source URLs (Confirmed)

| # | Label | URL | Owner | Topic |
|---|---|---|---|---|
| 1 | `tp_sen` | https://www.tp.edu.sg/life-at-tp/special-educational-needs-sen-support.html | Temasek Polytechnic | SEN support for poly students |
| 2 | `enabling_transport` | https://www.enablingguide.sg/im-looking-for-disability-support/transport | SG Enable (govt) | Disability transport schemes |
| 3 | `enabling_care` | https://www.enablingguide.sg/im-looking-for-disability-support/child-adult-care | SG Enable (govt) | Child & adult care services |
| 4 | `enabling_employment` | https://www.enablingguide.sg/im-looking-for-disability-support/training-employment | SG Enable (govt) | Training & employment support |

### Scraping Notes
- `enablingguide.sg` is a **Next.js SPA** — JS-rendered. Use `crawl4ai` + Playwright.
- `tp.edu.sg` may be traditional CMS — try `httpx + BeautifulSoup` first, fallback Playwright.
- Store raw scraped markdown in `backend/data/raw/<label>.md`.

---

## Target Users

1. **TP students** with special educational needs
2. **Persons with disabilities (PWDs)** seeking transport, care, or employment help
3. **Caregivers and family members** researching schemes
4. **School counsellors / social workers**

Primary device: **mobile browser** (Chrome Android, Safari iOS). Also desktop.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│  USER'S BROWSER (phone or desktop)              │
│                                                 │
│  Next.js 14 PWA (static export)                 │
│  ├── Chat UI (mobile-first, Tailwind)           │
│  ├── Feedback widget (👍 👎 + comment)          │
│  ├── Service Worker (offline shell)             │
│  └── manifest.json (Add to Home Screen)         │
│         │                        │              │
│    POST /query              Firestore SDK        │
│    (fetch answer)      (log query + feedback)    │
└─────────┼────────────────────────┼──────────────┘
          │                        │
┌─────────▼──────────┐   ┌────────▼──────────────┐
│  HuggingFace Space │   │  Firebase (Google)     │
│  FastAPI backend   │   │                        │
│  ├── RAG /query    │   │  Firestore DB          │
│  ├── /ingest       │   │  ├── queries/          │
│  ├── /health       │   │  │   └── {sessionId,   │
│  └── /sources      │   │  │       message,      │
│                    │   │  │       answer,        │
│  sentence-trans-   │   │  │       sources,      │
│  formers (embed)   │   │  │       feedback,     │
│  ChromaDB (vectors)│   │  │       timestamp}    │
│  Groq API (LLM)    │   │  │                    │
└────────────────────┘   │  Firebase Hosting      │
                         │  (PWA static files)    │
                         │                        │
                         │  Google Analytics 4    │
                         │  (page views, sessions)│
                         └───────────────────────┘
```

---

## Firebase vs Vercel — Decision Record

| Factor | Firebase (chosen ✅) | Vercel |
|---|---|---|
| **Hosting** | Firebase Hosting — CDN, HTTPS, free | Edge CDN, HTTPS, free |
| **Next.js support** | Static export only (fine for this app) | Full SSR — perfect |
| **Query/feedback storage** | **Firestore built-in — perfect** | ❌ None — need extra service |
| **Analytics** | **GA4 free + unlimited + Firestore logs** | 2,500 events/month free (very limited) |
| **BigQuery export** | ✅ Free 1TB/month — SQL on all query data | ❌ Not available |
| **CI/CD** | GitHub Actions + firebase-actions | Auto GitHub integration |
| **Custom domain** | Free SSL | Free SSL |
| **Free DB limit** | 1GB, 50K reads/day, 20K writes/day | N/A |
| **Verdict** | ✅ **Best for analytics + feedback** | Best for pure hosting DX |

**Why static export is not a limitation here:**
The entire chat UI is client-side React (no SSR needed). All data fetching goes
directly to the FastAPI backend on HuggingFace. No Next.js API routes are used.
Static export = faster loads (pure CDN) + free Firebase Hosting.

---

## Free & Open Source Stack — $0 Total Cost

| Layer | Choice | Cost | Sign-up |
|---|---|---|---|
| **LLM** | Groq API `llama-3.1-8b-instant` | Free | console.groq.com |
| **Embeddings** | sentence-transformers `all-MiniLM-L6-v2` | Free | No key — local |
| **Vector DB** | ChromaDB (disk-persisted) | Free | No key — local |
| **Scraper** | crawl4ai + Playwright | Free | Open source |
| **Backend framework** | FastAPI (Python 3.11) | Free | Open source |
| **Backend hosting** | HuggingFace Spaces (Docker) | Free | huggingface.co |
| **Frontend framework** | Next.js 14 static export | Free | Open source |
| **Frontend styling** | Tailwind CSS v3 | Free | Open source |
| **PWA** | next-pwa plugin | Free | Open source |
| **Frontend hosting** | Firebase Hosting | Free | firebase.google.com |
| **Analytics DB** | Firestore (Spark free plan) | Free | firebase.google.com |
| **Web analytics** | Google Analytics 4 | Free | Same Firebase project |
| **CI/CD** | GitHub Actions | Free | github.com |

**Total: $0.00 — no credit card required for any service**

---

## Firestore Analytics Data Model

Every user interaction is written to Firestore from the **browser** using the
Firebase client SDK (no backend involvement — keeps FastAPI simple).

### Collection: `queries`
One document per conversation turn:

```typescript
interface QueryLog {
  // Session
  sessionId: string;          // anonymous UUID stored in localStorage
  timestamp: Timestamp;       // Firestore server timestamp

  // Query
  userMessage: string;        // exactly what the user typed
  assistantAnswer: string;    // full answer returned
  sourcesUsed: string[];      // labels e.g. ["tp_sen", "enabling_transport"]
  sourceUrls: string[];       // full URLs of cited sources

  // Performance
  responseTimeMs: number;     // time from send → answer received

  // Feedback (updated after user rates)
  feedbackRating: number | null;   // 1 (👎) or 5 (👍), null if no feedback
  feedbackComment: string | null;  // optional text feedback

  // Context
  userAgent: string;          // browser/device string
  screenWidth: number;        // px — mobile vs desktop
  language: string;           // browser language e.g. "en-SG"
  historyLength: number;      // how many turns into the conversation
}
```

### Collection: `sessions`
One document per browser session (created on first load):

```typescript
interface SessionLog {
  sessionId: string;
  startedAt: Timestamp;
  lastActiveAt: Timestamp;
  totalQueries: number;
  device: 'mobile' | 'desktop' | 'tablet';
  isPWA: boolean;             // true if running in standalone (Add to Home Screen)
  referrer: string;
}
```

### What You Can Answer with This Data

- What are the most common questions users ask?
- Which of the 4 sources is cited most often?
- What questions get low feedback ratings? (gaps in content)
- Are users on mobile or desktop?
- How many users have added to home screen (PWA)?
- What's the average response time?
- What time of day / day of week is the app most used?
- What questions get no good answer? (improve ingestion)

---

## Project Structure

```
rag-sg-disability/
├── CLAUDE.md
│
├── frontend/                          ← Next.js 14 static export PWA
│   ├── app/
│   │   ├── layout.tsx                 ← root layout: metadata, GA4 script, viewport
│   │   ├── page.tsx                   ← home = chat screen
│   │   ├── about/
│   │   │   └── page.tsx               ← data sources + privacy info
│   │   └── globals.css
│   ├── components/
│   │   ├── ChatWindow.tsx             ← scrollable message list
│   │   ├── ChatBubble.tsx             ← user / assistant bubble
│   │   ├── MessageInput.tsx           ← bottom-fixed textarea + send
│   │   ├── SourceCard.tsx             ← expandable snippet + external link
│   │   ├── FeedbackWidget.tsx         ← 👍 👎 + optional comment, writes to Firestore
│   │   ├── LoadingDots.tsx            ← typing indicator
│   │   └── Header.tsx                 ← app bar
│   ├── hooks/
│   │   ├── useChat.ts                 ← POST /query, manage history, log to Firestore
│   │   └── useSession.ts              ← create/update sessionId in localStorage
│   ├── lib/
│   │   ├── api.ts                     ← typed fetch client for FastAPI backend
│   │   ├── firebase.ts                ← Firebase app init (client SDK)
│   │   └── analytics.ts              ← Firestore write helpers (logQuery, logFeedback)
│   ├── store/
│   │   └── chatStore.ts               ← Zustand: messages[], isLoading, error
│   ├── public/
│   │   ├── manifest.json              ← PWA manifest
│   │   ├── icon-192.png
│   │   └── icon-512.png
│   ├── next.config.js                 ← output: 'export', next-pwa config
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── .firebaserc                    ← Firebase project alias
│   ├── firebase.json                  ← Firebase Hosting config (public: out/)
│   ├── package.json
│   └── .env.local.example
│
├── backend/                           ← FastAPI on HuggingFace Spaces
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── ingestion/
│   │   │   ├── scraper.py
│   │   │   ├── chunker.py
│   │   │   └── embedder.py
│   │   ├── retrieval/
│   │   │   └── vector_store.py
│   │   ├── llm/
│   │   │   └── groq_client.py
│   │   └── api/
│   │       ├── routes.py
│   │       └── schemas.py
│   ├── data/
│   │   ├── raw/
│   │   └── chroma_db/                 ← gitignored
│   ├── tests/
│   ├── scripts/
│   │   └── ingest.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
└── .github/
    └── workflows/
        ├── backend-test.yml           ← pytest on PR
        ├── hf-deploy.yml              ← push main → HuggingFace Space
        └── firebase-deploy.yml        ← push main → Firebase Hosting
```

---

## Environment Variables

### `frontend/.env.local`

```bash
# FastAPI backend on HuggingFace (use localhost:8000 for local dev)
NEXT_PUBLIC_API_URL=https://YOUR-HF-USERNAME-rag-sg-disability.hf.space

# Firebase client config — all public values (safe to expose)
NEXT_PUBLIC_FIREBASE_API_KEY=
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
NEXT_PUBLIC_FIREBASE_PROJECT_ID=
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
NEXT_PUBLIC_FIREBASE_APP_ID=
NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=   # GA4 measurement ID
```

### `backend/.env`

```bash
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3.1-8b-instant
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHROMA_PERSIST_DIR=./data/chroma_db
CHROMA_COLLECTION=sg_disability_support
SOURCE_URLS=https://www.tp.edu.sg/life-at-tp/special-educational-needs-sen-support.html,https://www.enablingguide.sg/im-looking-for-disability-support/transport,https://www.enablingguide.sg/im-looking-for-disability-support/child-adult-care,https://www.enablingguide.sg/im-looking-for-disability-support/training-employment
CHUNK_SIZE=512
CHUNK_OVERLAP=64
TOP_K=5
APP_ENV=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,https://YOUR-PROJECT.web.app
```

---

## Firebase Configuration Files

### `frontend/firebase.json`
```json
{
  "hosting": {
    "public": "out",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [{ "source": "**", "destination": "/index.html" }],
    "headers": [
      {
        "source": "/sw.js",
        "headers": [{ "key": "Cache-Control", "value": "no-cache" }]
      }
    ]
  }
}
```

### `frontend/next.config.js`
```js
const withPWA = require('next-pwa')({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
})

/** @type {import('next').NextConfig} */
module.exports = withPWA({
  output: 'export',        // static export for Firebase Hosting
  trailingSlash: true,     // required for Firebase Hosting SPA routing
  images: { unoptimized: true },  // required for static export
})
```

---

## Firestore Security Rules

```javascript
// Allow browser to write query logs; never allow reads from browser
// (reads happen in your admin dashboard only, protected separately)
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /queries/{docId} {
      allow create: if true;   // anonymous logging — no auth needed
      allow read, update, delete: if false;  // admin only via Firebase Console
    }
    match /sessions/{docId} {
      allow create, update: if true;
      allow read, delete: if false;
    }
  }
}
```

---

## Analytics Helpers (`frontend/lib/analytics.ts`)

```typescript
import { db } from './firebase'
import { collection, addDoc, updateDoc, doc, serverTimestamp } from 'firebase/firestore'

export async function logQuery(data: {
  sessionId: string
  userMessage: string
  assistantAnswer: string
  sourcesUsed: string[]
  sourceUrls: string[]
  responseTimeMs: number
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
  return ref.id   // return docId so feedback can update the same document
}

export async function logFeedback(docId: string, rating: number, comment?: string) {
  await updateDoc(doc(db, 'queries', docId), {
    feedbackRating: rating,
    feedbackComment: comment ?? null,
  })
}
```

---

## API Contract (FastAPI backend — unchanged)

### `GET /health`
```json
{ "status": "ok", "llm": "groq/llama-3.1-8b-instant", "chunks_indexed": 142 }
```

### `POST /query`
```jsonc
// Request
{ "message": "How do I apply for SEN support at TP?", "history": [...] }

// Response
{
  "answer": "To apply for SEN support...",
  "sources": [
    { "label": "tp_sen", "url": "https://...", "title": "...", "snippet": "..." }
  ]
}
```

---

## Mobile-First UI Design Principles

- Minimum 16px font on inputs (prevents iOS Safari auto-zoom)
- Bottom-fixed `MessageInput` — keyboard pushes it up naturally
- `env(safe-area-inset-bottom)` padding for iPhone home bar
- Auto-scroll to latest message on new response
- 44×44px minimum touch targets
- WCAG AA colour contrast (≥4.5:1)
- Offline banner when FastAPI backend unreachable

---

## Accessibility Requirements

- [ ] All interactive elements: `aria-label`, `role`, `aria-describedby`
- [ ] Colour contrast ≥ 4.5:1 throughout
- [ ] Keyboard fully navigable (Tab, Enter, Escape)
- [ ] Visible focus ring on all interactive elements
- [ ] `aria-live="polite"` for new messages and loading state
- [ ] `aria-live="assertive"` for errors
- [ ] Text resizable to 200% without horizontal scroll
- [ ] Tested: iOS VoiceOver (Safari) + Android TalkBack (Chrome)

---

## Claude Code Instructions

1. **Always read CLAUDE.md in full** before writing any code
2. **Update this file** when any decision changes
3. Frontend: `output: 'export'` in next.config.js — no server components that need SSR
4. Frontend: Firebase client SDK only — never Firebase Admin SDK in browser
5. Frontend: every `logQuery` call captures the returned `docId` for later feedback update
6. Frontend: Tailwind only, TypeScript strict, zero `any`
7. Frontend: all interactive elements get full ARIA attributes
8. Backend: async FastAPI, `asyncio.to_thread()` for sentence-transformers
9. Backend: structured JSON errors `{"detail": "..."}` not plain text
10. Backend: never log `userMessage` content server-side (privacy) — Firestore only
11. Firestore writes are fire-and-forget (don't block the UI on analytics)

---

## Build Phases & Checklist

### ✅ Phase 0 — Planning (DONE)
- [x] Define source URLs
- [x] Choose 100% free open source stack
- [x] Decide PWA over native app
- [x] Choose Firebase over Vercel (analytics requirement)
- [x] Design Firestore data model
- [x] Write CLAUDE.md

### 🔲 Phase 1 — Backend Scaffold
- [ ] `backend/` Python project (`requirements.txt`)
- [ ] `app/config.py` — Pydantic Settings
- [ ] `app/main.py` — FastAPI + CORS + lifespan
- [ ] `GET /health` endpoint
- [ ] ChromaDB persistent client init
- [ ] sentence-transformers load test
- [ ] Groq API connection test

### 🔲 Phase 2 — Ingestion Pipeline
- [ ] `ingestion/scraper.py` — crawl4ai, test each URL
- [ ] Save raw markdown to `data/raw/`
- [ ] `ingestion/chunker.py`
- [ ] `ingestion/embedder.py` — embed + ChromaDB upsert
- [ ] `scripts/ingest.py` — end-to-end runner
- [ ] Verify chunks via direct ChromaDB query

### 🔲 Phase 3 — Retrieval + LLM
- [ ] `retrieval/vector_store.py` — cosine search + metadata
- [ ] `llm/groq_client.py` — prompt builder + Groq completion
- [ ] `api/schemas.py` — Pydantic models
- [ ] `POST /query` wired end-to-end
- [ ] `GET /sources` endpoint
- [ ] Manual QA: 10 questions across all 4 sources

### 🔲 Phase 4 — Frontend PWA
- [ ] Next.js 14 init: TypeScript + Tailwind + next-pwa + `output: 'export'`
- [ ] Firebase project created, Firestore enabled, Hosting enabled
- [ ] `lib/firebase.ts` — Firebase client init
- [ ] `lib/analytics.ts` — `logQuery` + `logFeedback` helpers
- [ ] `hooks/useSession.ts` — anonymous sessionId
- [ ] `hooks/useChat.ts` — POST /query + logQuery to Firestore
- [ ] Zustand chat store
- [ ] `ChatBubble`, `MessageInput`, `SourceCard`, `LoadingDots`, `Header`
- [ ] `FeedbackWidget` — 👍 👎 buttons + optional comment → `logFeedback`
- [ ] `about/page.tsx` — sources + privacy notice
- [ ] `public/manifest.json` + PWA icons
- [ ] Firestore security rules deployed
- [ ] Accessibility audit
- [ ] Test: Add to Home Screen (iOS Safari + Chrome Android)
- [ ] Test: offline behaviour (service worker)

### 🔲 Phase 5 — Deployment
- [ ] `Dockerfile` for backend (HuggingFace Spaces, port 7860)
- [ ] Create HuggingFace Space (Docker), set `GROQ_API_KEY` secret
- [ ] Push backend, run ingestion, verify `/health`
- [ ] `firebase.json` + `.firebaserc` configured
- [ ] `firebase deploy --only hosting` — verify PWA live at `*.web.app`
- [ ] Set `NEXT_PUBLIC_API_URL` + Firebase env vars in `.env.local`, rebuild
- [ ] Update `CORS_ORIGINS` in HF Space to Firebase Hosting URL
- [ ] GitHub Actions: pytest on PR, HF deploy + Firebase deploy on `main`
- [ ] End-to-end test on real phone browser
- [ ] Verify Firestore receiving query documents
- [ ] Verify GA4 receiving page view events

---

## Free Service Sign-Up URLs

| Service | URL | No Credit Card? |
|---|---|---|
| Groq API | https://console.groq.com | ✅ Yes |
| Hugging Face | https://huggingface.co/join | ✅ Yes |
| Firebase | https://firebase.google.com | ✅ Yes (Google account) |
| GitHub | https://github.com/signup | ✅ Yes |

---

## References

- [Next.js Static Export Docs](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
- [next-pwa](https://github.com/shadowwalker/next-pwa)
- [Firebase Hosting Docs](https://firebase.google.com/docs/hosting)
- [Firestore Docs](https://firebase.google.com/docs/firestore)
- [Firebase JS SDK](https://firebase.google.com/docs/web/setup)
- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
- [Google Analytics 4 + Firebase](https://firebase.google.com/docs/analytics)
- [Groq API Docs](https://console.groq.com/docs/quickstart)
- [sentence-transformers](https://www.sbert.net)
- [ChromaDB Docs](https://docs.trychroma.com)
- [crawl4ai Docs](https://docs.crawl4ai.com)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [HuggingFace Spaces Docker](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/)

---

## Deep Crawling Strategy

The 4 seed URLs are entry points, not limits. The scraper follows
links within strict boundaries to build a richer knowledge base.

### Crawl Boundaries

| Seed Label | Seed URL | Allowed URL Prefix (stay within) | Max Depth | Max Pages |
|---|---|---|---|---|
| `tp_sen` | https://www.tp.edu.sg/life-at-tp/special-educational-needs-sen-support.html | `https://www.tp.edu.sg/life-at-tp/` | 2 | 20 |
| `enabling_transport` | https://www.enablingguide.sg/im-looking-for-disability-support/transport | `https://www.enablingguide.sg/im-looking-for-disability-support/` | 2 | 30 |
| `enabling_care` | https://www.enablingguide.sg/im-looking-for-disability-support/child-adult-care | `https://www.enablingguide.sg/im-looking-for-disability-support/` | 2 | 30 |
| `enabling_employment` | https://www.enablingguide.sg/im-looking-for-disability-support/training-employment | `https://www.enablingguide.sg/im-looking-for-disability-support/` | 2 | 30 |

**Rules enforced per crawled link:**
- ✅ Same domain as seed
- ✅ URL starts with the allowed prefix
- ✅ Not already visited (dedup by URL)
- ❌ External domains — skip
- ❌ Non-HTML resources (PDF, docx, images) — skip for now, log URL for manual review
- ❌ Anchor-only links (`#section`) — skip
- ❌ Auth-required pages — skip (detected by redirect to login)

**Scale:** ~110 pages max → ~1,500–2,500 chunks → well within ChromaDB + HuggingFace free limits.

### Crawl Config in `backend/app/config.py`

```python
CRAWL_SOURCES = [
    {
        "label": "tp_sen",
        "seed_url": "https://www.tp.edu.sg/life-at-tp/special-educational-needs-sen-support.html",
        "allowed_prefix": "https://www.tp.edu.sg/life-at-tp/",
        "max_depth": 2,
        "max_pages": 20,
    },
    {
        "label": "enabling_transport",
        "seed_url": "https://www.enablingguide.sg/im-looking-for-disability-support/transport",
        "allowed_prefix": "https://www.enablingguide.sg/im-looking-for-disability-support/",
        "max_depth": 2,
        "max_pages": 30,
    },
    {
        "label": "enabling_care",
        "seed_url": "https://www.enablingguide.sg/im-looking-for-disability-support/child-adult-care",
        "allowed_prefix": "https://www.enablingguide.sg/im-looking-for-disability-support/",
        "max_depth": 2,
        "max_pages": 30,
    },
    {
        "label": "enabling_employment",
        "seed_url": "https://www.enablingguide.sg/im-looking-for-disability-support/training-employment",
        "allowed_prefix": "https://www.enablingguide.sg/im-looking-for-disability-support/",
        "max_depth": 2,
        "max_pages": 30,
    },
]
```

### Chunk Metadata (extended for deep crawl)

Each chunk stored in ChromaDB carries:
```python
{
    "source_label": "enabling_transport",   # which of the 4 seeds it belongs to
    "source_url": "https://...",            # exact page URL (may be a sub-page)
    "seed_url": "https://...",              # the original seed URL
    "page_title": "Taxi Subsidy Scheme",
    "crawl_depth": 1,                       # 0 = seed page, 1 = one hop, 2 = two hops
    "chunk_index": 3,
    "char_count": 487,
    "fetched_at": "2026-05-31T10:00:00Z",
}
```

---

## Query Guardrails

Queries are confined to indexed content through **4 layered defences**.
Each layer catches what the previous might miss.

### Guardrail Flow

```
User message
    │
    ▼
┌─────────────────────────────────────────────┐
│  LAYER 1 — Retrieval Gate                   │
│                                             │
│  Embed query → ChromaDB cosine search       │
│  Get top-5 chunks + their distances         │
│                                             │
│  Best distance > MAX_DISTANCE (0.65)?       │
│  (i.e. nothing in the index is relevant)    │
└──────────┬──────────────────────────────────┘
           │ YES — out of scope               │ NO — proceed
           ▼                                  ▼
  Return OUT_OF_SCOPE_MSG        ┌────────────────────────────────┐
  Log: {isInScope: false,        │  LAYER 2 — Strict System Prompt│
        refusalReason:           │                                │
        'low_similarity'}        │  "Answer ONLY from CONTEXT.    │
                                 │   If not in context, output    │
                                 │   exactly: [OUT_OF_SCOPE]"     │
                                 └──────────────┬─────────────────┘
                                                │
                                                ▼
                                 ┌──────────────────────────────────┐
                                 │  LAYER 3 — Response Sentinel     │
                                 │  Check                           │
                                 │                                  │
                                 │  Does LLM response contain       │
                                 │  "[OUT_OF_SCOPE]" ?              │
                                 └──────────────┬───────────────────┘
                                                │
                              YES ──────────────┴────────────── NO
                               │                                 │
                               ▼                                 ▼
                    Return OUT_OF_SCOPE_MSG          Return answer + sources ✅
                    Log: {isInScope: false,          Log: {isInScope: true,
                          refusalReason:                   topSimilarityScore,
                          'llm_refusal'}                   sourcesUsed}
```

### Layer 1 — Retrieval Gate (in `retrieval/vector_store.py`)

```python
MAX_DISTANCE = 0.65   # ChromaDB cosine distance; tune after ingestion
                      # distance 0 = identical, 2 = opposite
                      # 0.65 ≈ similarity score of 0.35 — "barely related"

def is_in_scope(distances: list[float]) -> bool:
    """Return True if at least one retrieved chunk is relevant enough."""
    return min(distances) < MAX_DISTANCE
```

**Effect on real queries:**
- "How do I apply for SEN support at TP?" → distance ~0.18 ✅
- "What transport subsidies exist for wheelchair users?" → ~0.22 ✅
- "What is the weather in Singapore?" → ~0.78 ❌ rejected
- "How do I cook chicken rice?" → ~0.91 ❌ rejected

### Layer 2 — Strict System Prompt (in `llm/groq_client.py`)

```
SYSTEM PROMPT:

You are a helpful assistant for persons with disabilities,
students with special educational needs, and caregivers in Singapore.

You MUST answer using ONLY the information in the CONTEXT section below.
Do not use any outside knowledge. Do not make up information.

If the CONTEXT does not contain enough information to answer the question,
you MUST respond with exactly this text and nothing else:
[OUT_OF_SCOPE]

Keep answers clear, warm, and jargon-free.
Cite the source name at the end of your answer.

CONTEXT:
{retrieved_chunks}
```

### Layer 3 — Sentinel Check (in `api/routes.py`)

```python
OUT_OF_SCOPE_SENTINEL = "[OUT_OF_SCOPE]"

OUT_OF_SCOPE_MESSAGE = """I can only answer questions about:
• SEN (Special Educational Needs) support at Temasek Polytechnic
• Disability transport schemes in Singapore
• Child and adult care services for persons with disabilities
• Training and employment support for persons with disabilities

Your question appears to be outside these topics. For other enquiries:
• SG Enable: https://www.sg-enable.org.sg
• Ministry of Social and Family Development: https://www.msf.gov.sg
• TP Student Services: https://www.tp.edu.sg/student-services"""

def check_response(llm_text: str) -> str:
    if OUT_OF_SCOPE_SENTINEL in llm_text:
        return OUT_OF_SCOPE_MESSAGE
    return llm_text
```

### Layer 4 — Topic Pre-screening (optional, activate if needed)

If layers 1–3 produce too many false positives or negatives, add a
zero-shot topic classifier using sentence-transformers before Layer 1:

```python
ALLOWED_TOPICS = [
    "special educational needs support",
    "disability services Singapore",
    "wheelchair transport subsidy",
    "caregiver support",
    "employment for persons with disabilities",
    "SEN student accommodation",
    "early intervention programme",
]
# Embed these at startup. At query time, embed the user message and
# compute cosine similarity to each topic. If max similarity < 0.3,
# reject immediately before even hitting ChromaDB.
```

**Only implement Layer 4 if real-world testing shows layers 1–3 are insufficient.**

### Guardrail Tuning

After deployment, use Firestore data to tune `MAX_DISTANCE`:

```
Review queries where isInScope = false:
  → Were they genuinely off-topic? (good rejection) ✅
  → Were they valid but rejected? (threshold too strict) → lower MAX_DISTANCE

Review queries where isInScope = true but feedbackRating = 1 (👎):
  → Was the answer wrong/hallucinated? (threshold too loose) → raise MAX_DISTANCE
  → Was the content just not indexed? → expand crawl depth
```

### Updated Firestore QueryLog Schema

```typescript
interface QueryLog {
  // Session
  sessionId: string;
  timestamp: Timestamp;

  // Query
  userMessage: string;
  assistantAnswer: string;
  sourcesUsed: string[];          // source labels
  sourceUrls: string[];           // exact page URLs (may be sub-pages)

  // Guardrail fields (NEW)
  isInScope: boolean;             // did it pass the retrieval gate?
  topSimilarityScore: number;     // best chunk distance score (for threshold tuning)
  refusalReason: 'low_similarity' | 'llm_refusal' | null;
  pagesSearched: number;          // how many unique pages contributed chunks

  // Performance
  responseTimeMs: number;

  // Feedback
  feedbackRating: number | null;
  feedbackComment: string | null;

  // Context
  userAgent: string;
  screenWidth: number;
  language: string;
  historyLength: number;
}
```

### Analytics You Can Now Answer

- What % of queries are out of scope? (tune threshold or expand crawl)
- What are the most common rejected queries? (should we add a 5th source?)
- Which sub-pages (from deep crawl) are cited most often?
- Do deep-crawled sub-pages improve answer quality vs seed pages only?
- What's the correlation between similarity score and feedback rating?

---

## Updated Build Phases

### 🔲 Phase 2 — Ingestion Pipeline (updated for deep crawl)
- [ ] `ingestion/scraper.py` — crawl4ai with `allowed_prefix`, `max_depth`, `max_pages`
- [ ] Log every crawled URL and its depth
- [ ] Dedup URLs before scraping (same page may be linked from multiple places)
- [ ] Save raw markdown to `data/raw/<label>/<slug>.md` (one file per page)
- [ ] `ingestion/chunker.py` — chunk each page, carry full metadata
- [ ] `ingestion/embedder.py` — embed + upsert with extended metadata
- [ ] `scripts/ingest.py` — orchestrate, print summary table per seed
- [ ] Verify: query ChromaDB directly, check sub-page chunks appear

### 🔲 Phase 3 — Retrieval + LLM (updated for guardrails)
- [ ] `retrieval/vector_store.py` — return distances alongside chunks
- [ ] `retrieval/vector_store.py` — `is_in_scope()` function with `MAX_DISTANCE`
- [ ] `llm/groq_client.py` — strict system prompt with `[OUT_OF_SCOPE]` sentinel
- [ ] `api/routes.py` — sentinel check + `OUT_OF_SCOPE_MESSAGE`
- [ ] `api/schemas.py` — add `is_in_scope`, `top_similarity_score`, `refusal_reason` to response
- [ ] Test guardrails: 5 in-scope + 5 clearly out-of-scope queries
- [ ] Test edge cases: vaguely related queries, partial matches
- [ ] Tune `MAX_DISTANCE` based on test results
- [ ] `POST /query` response includes guardrail fields for Firestore logging
