#!/bin/bash
echo "================================================"
echo " SEN & Disability RAG -- Frontend Dev Server"
echo "================================================"
echo ""

cd "$(dirname "$0")/frontend"

echo "Starting Next.js frontend at http://localhost:3000"
echo "Press Ctrl+C to stop."
echo ""

npm run dev
