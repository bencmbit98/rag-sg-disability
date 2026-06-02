#!/bin/bash
echo "================================================"
echo " SEN & Disability RAG -- Backend Server"
echo "================================================"
echo ""

cd "$(dirname "$0")/backend"

source .venv/bin/activate

export PYTHONHTTPSVERIFY=0
export HF_HUB_DISABLE_SSL_VERIFICATION=1

echo "Starting FastAPI backend at http://localhost:8000"
echo "Press Ctrl+C to stop."
echo ""

uvicorn app.main:app --reload --port 8000
