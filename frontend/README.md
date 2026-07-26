# SEN & Disability Support — Frontend

Next.js 14 static-export PWA for the SEN & Disability Support RAG chatbot.

**Live:** https://tpsen-c1b69.web.app

## Local development

```bash
cp .env.local.example .env.local   # fill in your Firebase config
npm install
npm run dev                         # http://localhost:3000
```

## Deploy

Deployments are automatic. Any push to `main` that touches `frontend/**` triggers GitHub Actions, which builds and deploys to Firebase Hosting. No manual steps needed.

## Environment variables

All `NEXT_PUBLIC_*` variables must be set — either in `.env.local` (local dev) or as GitHub repository Secrets (CI/CD). See `.env.local.example` for the full list.

## Stack

- Next.js 14 (`output: 'export'`) + TypeScript + Tailwind CSS
- next-pwa (PWA / Add to Home Screen)
- Zustand (chat state)
- Firebase JS SDK v12 (Firestore analytics, hosted on Firebase Hosting)
- Groq LLM + ChromaDB backend on HuggingFace Spaces
