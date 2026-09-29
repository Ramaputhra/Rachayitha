@echo off
chcp 65001 >nul
echo ========================================================
echo   Deploying Rachayitha Website to GitHub & Vercel
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/3] Staging changes...
git add WebSite/ All.md deploy_website.bat deploy_website.ps1

echo.
echo [2/3] Committing changes...
git commit -m "fix(vercel): configure outputDirectory and disable buildCommand for static site"

echo.
echo [3/3] Pushing to GitHub (main branch)...
git push origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo   [SUCCESS] Successfully pushed to GitHub!
    echo   Vercel is now automatically deploying your website.
    echo ========================================================
) else (
    echo ========================================================
    echo   [ERROR] Push failed. Please check your git credentials.
    echo ========================================================
)

echo.
pause
