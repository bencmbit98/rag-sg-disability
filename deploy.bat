@echo off
title SEN RAG — Deploy
echo ================================================
echo  SEN ^& Disability RAG -- Deploy to Production
echo ================================================
echo.
echo NOTE: Firebase Hosting deploys automatically via GitHub Actions when you push.
echo       This script just commits and pushes. GitHub Actions handles the build + deploy.
echo.

REM Add portable Node.js to PATH
for /d %%i in ("%USERPROFILE%\nodejs\node-*") do set "NODE_PATH=%%i"
if defined NODE_PATH (
    set "PATH=%NODE_PATH%;%PATH%"
)

REM ── TP Network SSL bypass ───────────────────────
set GIT_SSL_NO_VERIFY=true
REM ────────────────────────────────────────────────

cd /d "%~dp0"
git add .

set /p msg=Commit message (Enter = "deploy: update"):
if "%msg%"=="" set msg=deploy: update
git commit -m "%msg%"
git push origin main

echo.
echo ================================================
echo  Push complete! GitHub Actions is now building.
echo  Watch: https://github.com/bencmbit98/rag-sg-disability/actions
echo  Live at: https://tpsen-c1b69.web.app (~2 min)
echo ================================================
pause
