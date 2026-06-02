#!/bin/bash
echo "================================================"
echo " SEN & Disability RAG -- Pull from GitHub"
echo "================================================"
echo ""

# ── TP Network fix ──────────────────────────────
# Uncomment if git pull fails with SSL error:
# export GIT_SSL_NO_VERIFY=true
# ────────────────────────────────────────────────

git pull origin main
if [ $? -ne 0 ]; then
    echo ""
    echo "Pull failed."
    echo "If on TP network, uncomment: export GIT_SSL_NO_VERIFY=true"
    exit 1
fi

echo ""
echo "Done! Latest changes pulled from GitHub."
