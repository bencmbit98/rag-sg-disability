#!/bin/bash
# Frontend deploys automatically via GitHub Actions when you push to main.
# This script is kept as a local fallback only (e.g. off-campus without TP SSL issues).
#
# Normal workflow: just run push.sh (or push.bat on Windows) and GitHub Actions
# will build + deploy to Firebase Hosting automatically in ~2 minutes.

echo "================================================"
echo " SEN & Disability RAG -- Deploy to Production"
echo "================================================"
echo ""
echo "NOTE: Firebase Hosting is normally deployed automatically by GitHub Actions."
echo "      Only use this script as a fallback when GitHub Actions is unavailable."
echo ""

REPO_ROOT="$(dirname "$0")"

echo "[1/2] Pushing to GitHub (GitHub Actions will build + deploy)..."
echo ""
cd "$REPO_ROOT"
git add .

read -rp "Commit message (Enter = 'deploy: update'): " msg
msg="${msg:-deploy: update}"

git commit -m "$msg"
git push origin main

echo ""
echo "================================================"
echo " Push complete! GitHub Actions is now building."
echo " Watch progress: https://github.com/bencmbit98/rag-sg-disability/actions"
echo " Live at: https://tpsen-c1b69.web.app (~2 min)"
echo "================================================"
