# Local Setup Guide — SEN & Disability Support RAG App
# Follow every step in order. Each section tells you what to do, exactly.

---

## Before You Start

**What OS is this guide written for?**
Commands are shown for all three. Use the tab that matches your machine:
- 🪟 **Windows** — use PowerShell (not Command Prompt)
- 🍎 **macOS** — use Terminal
- 🐧 **Linux** — use any terminal

**What you'll have at the end of this guide:**
- A working local copy of the app running on your laptop
- Backend API at `http://localhost:8000`
- Frontend PWA at `http://localhost:3000`
- All 4 accounts created and configured
- Claude Code ready to scaffold Phase 1

**Estimated time:** 45–90 minutes (mostly waiting for downloads)

---

## SECTION A — Local Machine Prerequisites

These are tools that must be installed before anything else.

---

### A1 — Check or Install Python 3.11+

Open your terminal and run:

```bash
python --version
```

**Expected output:** `Python 3.11.x` or `Python 3.12.x`

If you see `Python 3.10` or lower, or `command not found`:

🪟 **Windows:**
```
Download from: https://www.python.org/downloads/
During install — CHECK "Add Python to PATH" ✅
After install, restart PowerShell and re-run: python --version
```

🍎 **macOS:**
```bash
# Install Homebrew first if you don't have it:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install Python:
brew install python@3.11
python3 --version
```

🐧 **Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip -y
python3.11 --version
```

✅ **Done when:** `python3 --version` shows 3.11 or higher.

---

### A2 — Check or Install Node.js 18+

```bash
node --version
```

**Expected output:** `v18.x.x` or `v20.x.x`

If not installed:

🪟 **Windows / 🍎 macOS:**
```
Download the LTS version from: https://nodejs.org
Run the installer. Restart terminal after.
```

🍎 **macOS (with Homebrew):**
```bash
brew install node@20
node --version
npm --version
```

🐧 **Linux:**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y
node --version
```

✅ **Done when:** `node --version` shows v18+ and `npm --version` shows 9+.

---

### A3 — Check or Install Git

```bash
git --version
```

If not installed:

🪟 **Windows:** Download from https://git-scm.com/download/win — use all defaults.

🍎 **macOS:**
```bash
brew install git
# or just run: git --version  (macOS will prompt you to install Xcode tools)
```

🐧 **Linux:**
```bash
sudo apt install git -y
```

Configure your identity (required for commits):
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

✅ **Done when:** `git --version` returns a version number.

---

### A4 — Install Visual Studio Code

VS Code is the recommended editor. Claude Code works inside it.

Download from: **https://code.visualstudio.com**

After installing, open VS Code and install these extensions
(click the Extensions icon in the left sidebar, search each name):

| Extension | Why |
|---|---|
| **Python** (Microsoft) | Python language support |
| **Pylance** | Python type checking |
| **ESLint** | JavaScript/TypeScript linting |
| **Tailwind CSS IntelliSense** | Autocomplete for Tailwind classes |
| **Prettier** | Code formatting |
| **GitLens** | Git history in editor |

✅ **Done when:** VS Code opens and you can see the Extensions panel.

---

### A5 — Install Claude Code

Claude Code is the AI agent that will write most of the application code.
It runs in your terminal and reads `CLAUDE.md` as its instructions.

```bash
npm install -g @anthropic-ai/claude-code
```

Verify:
```bash
claude --version
```

> **Note:** Claude Code requires an Anthropic account to use.
> Go to **https://claude.ai** and sign up for a free account.
> When you first run `claude` in a project folder, it will ask you to log in.

✅ **Done when:** `claude --version` prints a version number.

---

## SECTION B — Free Account Sign-Ups

Sign up for all 4 services. None require a credit card.

---

### B1 — GitHub (Code Repository + CI/CD)

1. Go to **https://github.com/signup**
2. Enter username, email, password
3. Verify your email
4. Choose the **Free** plan

**Then set up SSH authentication** (so you can push code without typing passwords):

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your@email.com"
# Press Enter 3 times to accept defaults

# Copy the public key to clipboard
# macOS:
cat ~/.ssh/id_ed25519.pub | pbcopy
# Windows PowerShell:
cat ~/.ssh/id_ed25519.pub | clip
# Linux:
cat ~/.ssh/id_ed25519.pub
```

Go to **GitHub → Settings → SSH and GPG keys → New SSH key**
Paste the key, title it "My Laptop", click **Add SSH key**.

Test it:
```bash
ssh -T git@github.com
# Expected: "Hi username! You've successfully authenticated..."
```

✅ **Done when:** SSH test says "successfully authenticated".

---

### B2 — Groq (Free LLM API — your only API key)

1. Go to **https://console.groq.com**
2. Click **Sign Up** — use Google or GitHub sign-in (no credit card)
3. Once in the dashboard, click **API Keys** in the left sidebar
4. Click **Create API Key**
5. Name it: `rag-sg-disability`
6. **Copy the key immediately** — it starts with `gsk_`
7. Save it somewhere safe (password manager, or a local text file — never commit to GitHub)

Free limits: 14,400 requests/day, no credit card ever needed.

✅ **Done when:** You have a `gsk_...` key saved somewhere safe.

---

### B3 — Hugging Face (Backend Hosting — needed at Phase 5)

You don't need this until deployment, but sign up now:

1. Go to **https://huggingface.co/join**
2. Enter username, email, password
3. Verify your email
4. Choose the **Free** plan

✅ **Done when:** You can log in to huggingface.co.

---

### B4 — Firebase (Frontend Hosting + Analytics — needed at Phase 4)

You need a Google account (Gmail). If you don't have one: https://accounts.google.com/signup

1. Go to **https://firebase.google.com**
2. Click **Get started**
3. Sign in with your Google account
4. You'll land on the Firebase Console — leave it open, you'll come back in Section F

✅ **Done when:** You can see the Firebase Console dashboard.

---

## SECTION C — GitHub Repository Setup

---

### C1 — Create the Repository

1. Go to **https://github.com/new**
2. Fill in:
   - **Repository name:** `rag-sg-disability`
   - **Description:** `RAG chatbot for SEN and disability support in Singapore`
   - **Visibility:** Public (required for free GitHub Actions minutes)
   - ✅ Check **Add a README file**
   - ✅ Check **Add .gitignore** → choose **Python** template
3. Click **Create repository**

---

### C2 — Clone to Your Computer

```bash
# Replace YOUR-USERNAME with your GitHub username
git clone git@github.com:bencmbit98/rag-sg-disability.git
cd rag-sg-disability
```

🪟 **Windows note:** Run this in PowerShell, not Command Prompt.

✅ **Done when:** You see the folder `rag-sg-disability` on your computer.

---

### C3 — Add CLAUDE.md

Copy the `CLAUDE.md` file you downloaded earlier into the repo root:

```bash
# macOS/Linux — adjust source path to where you saved CLAUDE.md
cp ~/Downloads/CLAUDE.md ./CLAUDE.md

# Windows PowerShell
Copy-Item "$HOME\Downloads\CLAUDE.md" -Destination ".\CLAUDE.md"
```

---

### C4 — Create a Proper .gitignore

Replace the default Python .gitignore with this project-specific one:

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
*.egg-info/

# Environment variables — NEVER commit these
.env
.env.local
.env.*.local
backend/.env

# Data — too large for git, recreate by running ingest.py
backend/data/chroma_db/
backend/data/raw/

# Node / Next.js
node_modules/
frontend/.next/
frontend/out/
frontend/.env.local

# Firebase
.firebase/
firebase-debug.log

# VS Code
.vscode/settings.json

# macOS
.DS_Store

# Logs
*.log
EOF
```

Commit everything so far:
```bash
git add .
git commit -m "chore: initial project structure with CLAUDE.md and .gitignore"
git push origin main
```

✅ **Done when:** You can see the files in your GitHub repo on github.com.

---

## SECTION D — Python Backend Local Setup

---

### D1 — Create the Folder Structure

From the repo root:

```bash
mkdir -p backend/app/ingestion
mkdir -p backend/app/retrieval
mkdir -p backend/app/llm
mkdir -p backend/app/api
mkdir -p backend/data/raw
mkdir -p backend/tests
mkdir -p backend/scripts
```

---

### D2 — Create the Python Virtual Environment

```bash
cd backend

# Create venv
python3 -m venv .venv

# Activate it
# macOS/Linux:
source .venv/bin/activate

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# You should see (.venv) at the start of your prompt
```

> **Important:** Always activate the venv before working on the backend.
> You'll need to run `source .venv/bin/activate` every time you open a new terminal.

---

### D3 — Create requirements.txt and Install

Create `backend/requirements.txt`:

```text
# API framework
fastapi==0.111.0
uvicorn[standard]==0.29.0
python-multipart==0.0.9

# Config
pydantic-settings==2.2.1
python-dotenv==1.0.1

# LLM
groq==0.9.0

# Embeddings (local, no API key)
sentence-transformers==3.0.0
torch==2.3.0

# Vector database
chromadb==0.5.0

# Web scraping
crawl4ai==0.3.0
playwright==1.44.0
httpx==0.27.0
beautifulsoup4==4.12.3

# Text processing
langchain-text-splitters==0.2.0

# Utilities
tenacity==8.3.0

# Testing
pytest==8.2.0
pytest-asyncio==0.23.7
httpx==0.27.0
```

Install everything:
```bash
pip install -r requirements.txt
```

> This will take **5–10 minutes** — sentence-transformers and torch are large.
> That's normal.

---

### D4 — Install Playwright Browser

```bash
playwright install chromium
```


This downloads a headless Chromium browser (~150MB) used by crawl4ai
to scrape JavaScript-rendered pages like enablingguide.sg.

✅ **Done when:** You see `Chromium X.X.X downloaded` in the output.

---

### D5 — Create the .env File

```bash
# Still inside backend/
cp .env.example .env 2>/dev/null || touch .env
```

Open `backend/.env` in VS Code and add:

```bash
# LLM — paste your Groq key from Step B2
GROQ_API_KEY=gsk_YOUR_KEY_HERE
GROQ_MODEL=llama-3.1-8b-instant

# Embeddings — local, no key needed
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Vector DB — ChromaDB on disk, no key needed
CHROMA_PERSIST_DIR=./data/chroma_db
CHROMA_COLLECTION=sg_disability_support

# Ingestion
SOURCE_URLS=https://www.tp.edu.sg/life-at-tp/special-educational-needs-sen-support.html,https://www.enablingguide.sg/im-looking-for-disability-support/transport,https://www.enablingguide.sg/im-looking-for-disability-support/child-adult-care,https://www.enablingguide.sg/im-looking-for-disability-support/training-employment
CHUNK_SIZE=512
CHUNK_OVERLAP=64
TOP_K=5
MAX_DISTANCE=0.65

# Guardrails
OUT_OF_SCOPE_SENTINEL=[OUT_OF_SCOPE]

# App
APP_ENV=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
```

Also create `backend/.env.example` (safe to commit — no real secrets):

```bash
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.1-8b-instant
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHROMA_PERSIST_DIR=./data/chroma_db
CHROMA_COLLECTION=sg_disability_support
SOURCE_URLS=https://...
CHUNK_SIZE=512
CHUNK_OVERLAP=64
TOP_K=5
MAX_DISTANCE=0.65
OUT_OF_SCOPE_SENTINEL=[OUT_OF_SCOPE]
APP_ENV=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
```

✅ **Done when:** `backend/.env` exists and has your Groq key.

---

### D6 — Create Minimal FastAPI App to Test the Setup

Create `backend/app/__init__.py` (empty file):
```bash
touch backend/app/__init__.py
touch backend/app/ingestion/__init__.py
touch backend/app/retrieval/__init__.py
touch backend/app/llm/__init__.py
touch backend/app/api/__init__.py
```

Create `backend/app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SG Disability RAG API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Backend is running"}
```

Run it:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Open your browser: **http://localhost:8000/health**

Expected response:
```json
{"status": "ok", "message": "Backend is running"}
```

Also open: **http://localhost:8000/docs** — you'll see the auto-generated API docs.

✅ **Done when:** `/health` returns OK in the browser.

---

## SECTION E — Frontend Local Setup

Open a **new terminal tab** (keep the backend running in the other one).

---

### E1 — Create the Next.js App

From the repo root:

```bash
cd frontend  # if frontend/ doesn't exist yet, navigate to repo root first
# If frontend/ doesn't exist:
cd ..  # go back to repo root if you're in backend/

npx create-next-app@14 frontend \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --no-src-dir \
  --import-alias "@/*"
```

Answer the prompts:
- Would you like to use App Router? → **Yes**
- Would you like to customize the default import alias? → **No**

---

### E2 — Install Additional Frontend Dependencies

```bash
cd frontend
npm install zustand axios next-pwa
npm install -D @types/node
```

---

### E3 — Create the Frontend .env.local

```bash
cat > .env.local << 'EOF'
# Backend API — use localhost for local dev
# Change to HuggingFace Space URL when deploying
NEXT_PUBLIC_API_URL=http://localhost:8000

# Firebase config — leave blank for now, fill in Section F
NEXT_PUBLIC_FIREBASE_API_KEY=
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
NEXT_PUBLIC_FIREBASE_PROJECT_ID=
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
NEXT_PUBLIC_FIREBASE_APP_ID=
NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=
EOF
```

---

### E4 — Test the Frontend Dev Server

```bash
npm run dev
```

Open: **http://localhost:3000**

You should see the default Next.js starter page.

✅ **Done when:** Both servers run simultaneously:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

---

## SECTION F — Firebase Project Setup

Do this now so the Firebase config is ready for Phase 4.

---

### F1 — Create Firebase Project

1. Go to **https://console.firebase.google.com**
2. Click **Add project**
3. Project name: `rag-sg-disability`
4. **Enable Google Analytics** → Yes (it's free, keep it on)
5. Select or create a Google Analytics account → **Default Account for Firebase**
6. Click **Create project** — wait ~30 seconds
7. Click **Continue**

---

### F2 — Enable Firestore Database

1. In left sidebar → **Build → Firestore Database**
2. Click **Create database**
3. Choose **Start in production mode** (we'll set proper rules)
4. Choose region: **asia-southeast1 (Singapore)** ← important for latency
5. Click **Enable**

---

### F3 — Enable Firebase Hosting

1. In left sidebar → **Build → Hosting**
2. Click **Get started**
3. Follow the wizard — click through (you'll configure it properly via CLI)
4. Click **Next** on each screen, then **Continue to console**

---

### F4 — Get Your Firebase Web App Config

1. In the Firebase console, click the **gear icon** (⚙️) → **Project settings**
2. Scroll down to **Your apps**
3. Click the **web icon** (`</>`)
4. App nickname: `rag-sg-disability-web`
5. ✅ Check **Also set up Firebase Hosting for this app**
6. Click **Register app**
7. You'll see a config object like this — **copy it**:

```javascript
const firebaseConfig = {
  apiKey: "AIza...",
  authDomain: "rag-sg-disability.firebaseapp.com",
  projectId: "rag-sg-disability",
  storageBucket: "rag-sg-disability.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123",
  measurementId: "G-XXXXXXXX"
};
```

8. Open `frontend/.env.local` and fill in each value:

```bash
NEXT_PUBLIC_FIREBASE_API_KEY=AIza...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=rag-sg-disability.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=rag-sg-disability
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=rag-sg-disability.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
NEXT_PUBLIC_FIREBASE_APP_ID=1:123456789:web:abc123
NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=G-XXXXXXXX
```

---

### F5 — Install Firebase CLI

```bash
npm install -g firebase-tools
firebase --version  # should show 13.x.x
```

---

### F6 — Log In to Firebase CLI

```bash
firebase login
```

This opens a browser window. Sign in with your Google account.
Return to terminal — you should see: `✔ Success! Logged in as your@email.com`

---

### F7 — Initialise Firebase in the Frontend Folder

```bash
cd frontend
firebase init
```

Select with **spacebar**, confirm with **Enter**:

```
? Which Firebase features do you want to set up?
  ◉ Firestore
  ◉ Hosting

? Please select an option: Use an existing project
? Select a default Firebase project: rag-sg-disability

? What file should be used for Firestore Rules? firestore.rules  (press Enter)
? What file should be used for Firestore indexes? firestore.indexes.json  (press Enter)

? What do you want to use as your public directory? out
? Configure as a single-page app? Yes
? Set up automatic builds with GitHub? No  (we'll do this in Phase 5)
```

---

### F8 — Set Firestore Security Rules

Open `frontend/firestore.rules` and replace with:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Allow browser to write query logs anonymously
    // Nobody can read from the browser — only Firebase Console / admin
    match /queries/{docId} {
      allow create: if request.resource.data.keys().hasAll([
        'sessionId', 'userMessage', 'timestamp'
      ]);
      allow update: if request.resource.data.keys().hasAny([
        'feedbackRating', 'feedbackComment'
      ]);
      allow read, delete: if false;
    }

    match /sessions/{docId} {
      allow create, update: if true;
      allow read, delete: if false;
    }
  }
}
```

Deploy the rules:
```bash
firebase deploy --only firestore:rules
```

✅ **Done when:** Firebase CLI says `✔ Deploy complete!`

---

## SECTION G — Claude Code First Run

Everything is now set up. Time to start building with Claude Code.

---

### G1 — Open the Project in VS Code

```bash
# From the repo root
code .
```

---

### G2 — Launch Claude Code

Open a terminal **inside VS Code** (Terminal → New Terminal) and run:

```bash
# Make sure you're in the repo root
claude
```

First time: it will ask you to log in with your Anthropic account.
Follow the browser authentication flow.

---

### G3 — Your First Claude Code Prompt

Once Claude Code is running, type this:

```
Read CLAUDE.md carefully, then scaffold Phase 1 of the backend:
- app/config.py with Pydantic Settings reading from .env
- app/main.py with FastAPI, CORS, lifespan, and /health endpoint
  that reports: status, LLM model name, embedding model, vector DB status,
  and chunk count from ChromaDB
- verify the Groq API key connects successfully at startup
- verify sentence-transformers loads the embedding model at startup
- write a test in tests/test_api.py for the /health endpoint
```

Claude Code will read `CLAUDE.md` and generate all the files.
Review what it creates, then run:

```bash
cd backend
source .venv/bin/activate   # macOS/Linux
# or: .venv\Scripts\Activate.ps1  (Windows)
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/health` to confirm it's working.

---

## Quick Reference — Daily Workflow

Every time you sit down to work on this project:

```bash
# Terminal 1 — Backend
cd rag-sg-disability/backend
source .venv/bin/activate    # macOS/Linux
uvicorn app.main:app --reload

# Terminal 2 — Frontend
cd rag-sg-disability/frontend
npm run dev

# Terminal 3 — Claude Code
cd rag-sg-disability
claude
```

---

## Summary — What You've Set Up

| Item | Location | Status |
|---|---|---|
| Python 3.11+ | System | ✅ |
| Node.js 18+ | System | ✅ |
| Git | System | ✅ |
| VS Code + extensions | System | ✅ |
| Claude Code | System (global npm) | ✅ |
| GitHub account + SSH | github.com | ✅ |
| Groq API key (`gsk_...`) | backend/.env | ✅ |
| Hugging Face account | huggingface.co | ✅ (use in Phase 5) |
| Firebase project | console.firebase.google.com | ✅ |
| Firestore DB (Singapore region) | Firebase | ✅ |
| Firebase Hosting enabled | Firebase | ✅ |
| Firebase CLI logged in | Local machine | ✅ |
| Python venv + dependencies | backend/.venv | ✅ |
| Playwright + Chromium | backend/.venv | ✅ |
| FastAPI running locally | localhost:8000 | ✅ |
| Next.js running locally | localhost:3000 | ✅ |
| Firebase config in .env.local | frontend/.env.local | ✅ |
| Firestore rules deployed | Firebase | ✅ |

**Next step:** Run Claude Code and scaffold Phase 1 (Section G3).

---

## SECTION H — Known Issues & Fixes (TP Network)

This section documents problems encountered when running this project on
Temasek Polytechnic's network, which performs SSL inspection using a
self-signed certificate. All HTTPS connections fail without a bypass.

---

### H1 — `pip install` Goes to Wrong Python

**Symptom:** Packages install but Python can't find them (`ModuleNotFoundError`).

**Cause:** The system `pip` command points to a different Python than the activated venv.

**Fix:** Always use `python -m pip` instead of `pip`:

```powershell
# Wrong
pip install -r requirements.txt

# Correct
python -m pip install -r requirements.txt
```

**Verify:** Both should point to the same path:
```powershell
python -c "import sys; print(sys.executable)"
python -m pip -V
```

---

### H2 — Node.js Cannot Be Installed (No Admin Rights)

**Symptom:** Cannot run the Node.js installer; blocked by UAC.

**Fix:** Use the portable zip from nodejs.org (no installer needed):

1. Go to **https://nodejs.org/dist/latest-lts/** and download `node-vXX.X.X-win-x64.zip`
2. Extract it to your user folder:
```powershell
Expand-Archive -Path "$env:USERPROFILE\Downloads\node-v20*-win-x64.zip" -DestinationPath "$env:USERPROFILE\nodejs" -Force
```
3. Add to your user-level PATH (no admin needed):
```powershell
$nodePath = (Get-ChildItem "$env:USERPROFILE\nodejs" -Directory | Select-Object -First 1).FullName
[Environment]::SetEnvironmentVariable("PATH", "$nodePath;$([Environment]::GetEnvironmentVariable('PATH', 'User'))", "User")
$env:PATH = "$nodePath;$env:PATH"
node --version
```

---

### H3 — SSL Errors in Python (huggingface_hub, Groq, requests)

**Symptom:**
```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain
```

**Fix:** Set these environment variables before running any Python backend command:
```powershell
$env:PYTHONHTTPSVERIFY = "0"
$env:HF_HUB_DISABLE_SSL_VERIFICATION = "1"
```

These are also patched in code in `app/main.py` and `scripts/ingest.py` via:
- `ssl._create_default_https_context = ssl._create_unverified_context`
- `httpx.Client.__init__` monkey-patch to default `verify=False`
- `requests.Session.request` monkey-patch to default `verify=False`

---

### H4 — SSL Errors in Node.js (Firebase CLI, npm, Playwright)

**Symptom:**
```
Error: self-signed certificate in certificate chain
```

**Fix:** Set this before running any Node.js command that makes HTTPS requests:
```powershell
$env:NODE_TLS_REJECT_UNAUTHORIZED = "0"
```

Required for: `playwright install chromium`, `firebase login`, `firebase init`, `firebase deploy`, `npm install -g`.

---

### H5 — `huggingface_hub` + Python 3.12 + `asyncio.to_thread` Conflict

**Symptom:**
```
ERROR: Failed to load embedding model: Cannot send a request, as the client has been closed.
```

**Cause:** `huggingface_hub` 1.x uses httpx AsyncClient internally. Python 3.12 does not create an event loop in `asyncio.to_thread` worker threads, causing a conflict.

**Fix:** Create a new event loop inside the thread function:
```python
def _load_in_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return SentenceTransformer(settings.embedding_model)
    finally:
        loop.close()
        asyncio.set_event_loop(None)

model = await asyncio.to_thread(_load_in_thread)
```

---

### H6 — Firebase CLI Login Fails (SSL)

**Symptom:** `firebase login` fails with SSL error.

**Fix:**
```powershell
$env:NODE_TLS_REJECT_UNAUTHORIZED = "0"
firebase login
```

Also needed for `firebase init` and `firebase deploy`.

---

### H7 — `hf` CLI Upload Fails (SSL)

**Symptom:** `hf upload` or `hf auth login` fails with httpx SSL error.

**Fix:** Use the provided Python upload script which patches httpx before importing huggingface_hub:
```powershell
python scripts/deploy_to_hf.py
```

---

## SECTION I — Deployment

---

### I1 — Deploy Backend to HuggingFace Spaces

**Prerequisites:** HuggingFace account, Write token from https://huggingface.co/settings/tokens

**Step 1 — Create a new Space:**
1. Go to https://huggingface.co/new-space
2. Name: `rag-sg-disability`, SDK: **Docker**, Visibility: Public
3. Click Create Space

**Step 2 — Add secrets:**
In Space Settings → Repository secrets:
- `GROQ_API_KEY` = your `gsk_...` key
- `CORS_ORIGINS` = `https://YOUR-PROJECT.web.app,http://localhost:3000`

**Step 3 — Upload backend:**
```powershell
cd backend
python scripts/deploy_to_hf.py
# Enter your HuggingFace Write token when prompted
# Enter repo ID: YOUR-USERNAME/rag-sg-disability
```

**Step 4 — Wait for first startup:**
- Build logs: Docker image builds (~5 min)
- Container logs: ingestion runs automatically (~15 min on first start)
- Status turns 🟢 Running when ready

**Step 5 — Verify:**
Open `https://YOUR-USERNAME-rag-sg-disability.hf.space/health` — should return:
```json
{"status": "ok", "chunks_indexed": 4065, "groq_connected": true, ...}
```

> **Note:** HuggingFace free Spaces sleep after inactivity. First request after waking takes ~30 seconds.

---

### I2 — Deploy Frontend to Firebase Hosting

**Prerequisites:** Firebase CLI installed and logged in (see Section F5–F6)

**Step 1 — Update API URL:**

Open `frontend/.env.local` and set:
```bash
NEXT_PUBLIC_API_URL=https://YOUR-USERNAME-rag-sg-disability.hf.space
```

**Step 2 — Build:**
```powershell
cd frontend
npm run build
```

If build fails with `Cannot find type definition file for 'minimatch'`:
```powershell
npm install -D @types/minimatch
npm run build
```

**Step 3 — Deploy:**
```powershell
$env:NODE_TLS_REJECT_UNAUTHORIZED = "0"
firebase deploy --only hosting
```

**Step 4 — Verify:**
Open the Hosting URL printed in the output (e.g. `https://tpsen-c1b69.web.app`).
Ask a question — you should get an answer sourced from the indexed content.

---

### I3 — Re-deploy After Code Changes

**Backend changes:**
```powershell
cd backend
python scripts/deploy_to_hf.py
```
HuggingFace rebuilds automatically. Ingestion re-runs on first container start.

**Frontend changes:**
```powershell
cd frontend
npm run build
$env:NODE_TLS_REJECT_UNAUTHORIZED = "0"
firebase deploy --only hosting
```

---

### I3 — Daily Development Workflow

The easiest way is to use the startup scripts included in the repo root.

**Windows — double-click or run from any terminal:**

| Script | What it does |
|---|---|
| `start-backend.bat` | Activates venv, sets SSL env vars, starts uvicorn on port 8000 |
| `start-frontend.bat` | Sets portable Node.js path, starts Next.js dev server on port 3000 |

```powershell
# Terminal 1
.\start-backend.bat

# Terminal 2
.\start-frontend.bat
```

**Mac / Linux — make executable first (one-time only):**
```bash
chmod +x start-backend.sh start-frontend.sh
```
Then run:
```bash
./start-backend.sh    # Terminal 1
./start-frontend.sh   # Terminal 2
```

> **Note (Windows):** `start-frontend.bat` automatically adds the portable Node.js
> folder (`%USERPROFILE%\nodejs\node-*`) to PATH. If Node.js was installed normally
> (not portable), this is harmless — the system Node will be used instead.

**Manual alternative (if scripts don't work):**
```powershell
# Terminal 1 — Backend
cd backend
.venv\Scripts\Activate.ps1
$env:PYTHONHTTPSVERIFY = "0"
$env:HF_HUB_DISABLE_SSL_VERIFICATION = "1"
uvicorn app.main:app --reload --port 8000

# Terminal 2 — Frontend (set portable Node path first if needed)
$nodePath = (Get-ChildItem "$env:USERPROFILE\nodejs" -Directory | Select-Object -First 1).FullName
$env:PATH = "$nodePath;$env:PATH"
cd frontend
npm run dev

# Terminal 3 — Claude Code
cd rag-sg-disability
claude
```

---

## SECTION J — Making Frontend UI Changes

Use this workflow whenever you want to update the chat UI, components, pages, or styles.

---

### J1 — Files You Will Edit

| What to change | File(s) |
|---|---|
| Chat bubbles, layout | `frontend/components/ChatBubble.tsx`, `ChatWindow.tsx` |
| Input bar | `frontend/components/MessageInput.tsx` |
| Header / nav | `frontend/components/Header.tsx` |
| Source cards | `frontend/components/SourceCard.tsx` |
| Feedback widget | `frontend/components/FeedbackWidget.tsx` |
| Home/chat page | `frontend/app/page.tsx` |
| About page | `frontend/app/about/page.tsx` |
| Global styles | `frontend/app/globals.css` |
| PWA config | `frontend/next.config.mjs`, `frontend/public/manifest.json` |

---

### J2 — Preview Changes Locally

**Step 1 — Start the backend** (Terminal 1):
```powershell
cd backend
.venv\Scripts\Activate.ps1
$env:PYTHONHTTPSVERIFY = "0"
$env:HF_HUB_DISABLE_SSL_VERIFICATION = "1"
uvicorn app.main:app --reload --port 8000
```

**Step 2 — Start the frontend dev server** (Terminal 2):
```powershell
cd frontend
npm run dev
```

**Step 3 — Open http://localhost:3000** in your browser.

Changes to any `frontend/` file auto-reload in the browser instantly — no restart needed.

---

### J3 — Deploy Changes Live

Once you are happy with the changes:

**Step 1 — Build the production bundle:**
```powershell
cd frontend
npm run build
```

**Step 2 — Deploy to Firebase Hosting:**
```powershell
$env:NODE_TLS_REJECT_UNAUTHORIZED = "0"
firebase deploy --only hosting
```

The live site at `https://tpsen-c1b69.web.app` updates within ~30 seconds.

**Step 3 — Push to GitHub:**
```powershell
cd ..
.\push.bat
```

Enter a short commit message describing what you changed (e.g. `"update chat bubble colours"`).

---

### J4 — Can You Edit Directly on GitHub?

You **can** edit files on github.com (click a file → pencil icon), but:

- Changes to UI code **will not go live** automatically — you still need to pull locally, build, and deploy to Firebase.
- Direct GitHub edits are only practical for **documentation files** (README.md, CLAUDE.md, SETUP_GUIDE.md) where no build step is needed.

For UI changes, always use the local workflow in J2–J3.

---

### J5 — Sync Changes from GitHub to Another Machine

On the second machine, after cloning the repo:
```powershell
.\pull.bat        # Windows
# or
bash pull.sh      # Mac / Linux
```

Then follow J2 to start the local servers.
