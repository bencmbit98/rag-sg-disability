@echo off
title SEN RAG — Deploy
echo ================================================
echo  SEN ^& Disability RAG -- Deploy to Production
echo ================================================
echo.

REM Add portable Node.js to PATH
for /d %%i in ("%USERPROFILE%\nodejs\node-*") do set "NODE_PATH=%%i"
if defined NODE_PATH (
    set "PATH=%NODE_PATH%;%PATH%"
)

REM ── TP Network SSL bypass ───────────────────────
set NODE_TLS_REJECT_UNAUTHORIZED=0
set GIT_SSL_NO_VERIFY=true
REM ────────────────────────────────────────────────

echo [1/3] Building frontend...
echo.
cd /d "%~dp0frontend"
call npm run build
if %errorlevel% neq 0 (
    echo.
    echo Build failed. Fix errors above before deploying.
    pause
    exit /b 1
)

echo.
echo [2/3] Deploying to Firebase Hosting...
echo.
call firebase deploy --only hosting
if %errorlevel% neq 0 (
    echo.
    echo Firebase deploy failed.
    pause
    exit /b 1
)

echo.
echo [3/3] Pushing to GitHub...
echo.
cd /d "%~dp0"
git add .
set /p msg=Commit message (Enter = "deploy: update frontend"):
if "%msg%"=="" set msg=deploy: update frontend
git commit -m "%msg%"
git push origin main

echo.
echo ================================================
echo  Deploy complete!
echo  Live at: https://tpsen-c1b69.web.app
echo ================================================
pause
