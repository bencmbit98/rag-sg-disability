@echo off
title Pull from GitHub
echo ================================================
echo  SEN ^& Disability RAG -- Pull from GitHub
echo ================================================
echo.

REM ── TP Network SSL bypass (required on TP campus) ──
set GIT_SSL_NO_VERIFY=true
REM ────────────────────────────────────────────────

git pull origin main
if %errorlevel% neq 0 (
    echo.
    echo Pull failed.
    echo If on TP network, uncomment: set GIT_SSL_NO_VERIFY=true
    pause
    exit /b 1
)

echo.
echo Done! Latest changes pulled from GitHub.
pause
