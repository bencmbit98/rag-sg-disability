@echo off
title SEN RAG — Backend
echo ================================================
echo  SEN ^& Disability RAG -- Backend Server
echo ================================================
echo.

cd /d "%~dp0backend"

call .venv\Scripts\activate.bat

set PYTHONHTTPSVERIFY=0
set HF_HUB_DISABLE_SSL_VERIFICATION=1

echo Starting FastAPI backend at http://localhost:8000
echo Press Ctrl+C to stop.
echo.

uvicorn app.main:app --reload --port 8000
