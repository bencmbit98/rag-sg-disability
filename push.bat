@echo off
title Push to GitHub
echo ================================================
echo  SEN ^& Disability RAG -- Push to GitHub
echo ================================================
echo.

REM ── TP Network SSL bypass (required on TP campus) ──
set GIT_SSL_NO_VERIFY=true
REM ────────────────────────────────────────────────

git add .

echo Current status:
git status
echo.

set /p msg=Commit message (Enter = "update"):
if "%msg%"=="" set msg=update

git commit -m "%msg%"
if %errorlevel% neq 0 (
    echo.
    echo Nothing to commit, or commit failed.
    pause
    exit /b 0
)

git push origin main
if %errorlevel% neq 0 (
    echo.
    echo Push failed.
    echo If on TP network, uncomment: set GIT_SSL_NO_VERIFY=true
    pause
    exit /b 1
)

echo.
echo Done! Changes pushed to GitHub.
pause
