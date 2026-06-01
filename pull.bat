@echo off
title Pull from GitHub
echo ================================================
echo  SEN ^& Disability RAG -- Pull from GitHub
echo ================================================
echo.

REM ── TP Network fix ──────────────────────────────
REM Uncomment the line below if git pull fails with
REM "SSL certificate problem: self signed certificate"
REM set GIT_SSL_NO_VERIFY=true
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
