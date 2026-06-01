#!/bin/bash
echo "================================================"
echo " SEN & Disability RAG -- Push to GitHub"
echo "================================================"
echo ""

# ── TP Network fix ──────────────────────────────
# Uncomment if git push fails with SSL error:
# export GIT_SSL_NO_VERIFY=true
# ────────────────────────────────────────────────

git add .

echo "Current status:"
git status
echo ""

read -rp "Commit message (Enter = 'update'): " msg
msg="${msg:-update}"

git commit -m "$msg"
if [ $? -ne 0 ]; then
    echo ""
    echo "Nothing to commit, or commit failed."
    exit 0
fi

git push origin main
if [ $? -ne 0 ]; then
    echo ""
    echo "Push failed."
    echo "If on TP network, uncomment: export GIT_SSL_NO_VERIFY=true"
    exit 1
fi

echo ""
echo "Done! Changes pushed to GitHub."
