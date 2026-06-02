@echo off
title SEN RAG — Frontend
echo ================================================
echo  SEN ^& Disability RAG -- Frontend Dev Server
echo ================================================
echo.

REM Add portable Node.js to PATH
for /d %%i in ("%USERPROFILE%\nodejs\node-*") do set "NODE_PATH=%%i"
if defined NODE_PATH (
    set "PATH=%NODE_PATH%;%PATH%"
    echo Using Node.js from: %NODE_PATH%
) else (
    echo Warning: Portable Node.js not found at %USERPROFILE%\nodejs\
    echo Make sure Node.js 18.17+ is installed.
)
echo.

cd /d "%~dp0frontend"

echo Starting Next.js frontend at http://localhost:3000
echo Press Ctrl+C to stop.
echo.

npm run dev
