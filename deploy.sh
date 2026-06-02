#!/bin/bash
echo "================================================"
echo " SEN & Disability RAG -- Deploy to Production"
echo "================================================"
echo ""

REPO_ROOT="$(dirname "$0")"

echo "[1/3] Building frontend..."
echo ""
cd "$REPO_ROOT/frontend"
npm run build
if [ $? -ne 0 ]; then
    echo ""
    echo "Build failed. Fix errors above before deploying."
    exit 1
fi

echo ""
echo "[2/3] Deploying to Firebase Hosting..."
echo ""
firebase deploy --only hosting
if [ $? -ne 0 ]; then
    echo ""
    echo "Firebase deploy failed."
    exit 1
fi

echo ""
echo "[3/3] Pushing to GitHub..."
echo ""
cd "$REPO_ROOT"
git add .

read -rp "Commit message (Enter = 'deploy: update frontend'): " msg
msg="${msg:-deploy: update frontend}"

git commit -m "$msg"
git push origin main

echo ""
echo "================================================"
echo " Deploy complete!"
echo " Live at: https://tpsen-c1b69.web.app"
echo "================================================"
