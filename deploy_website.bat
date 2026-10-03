@echo off
chcp 65001 >nul
echo ========================================================
echo   Deploying Rachayitha Website to GitHub & Vercel
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/4] Ensuring Rachayitha_Setup_V2.exe and Rachayitha_v2.exe binaries are synced...
if exist "%~dp0rachayitha code files\installer_output\Rachayitha_Setup_V2.exe" (
    copy /y "%~dp0rachayitha code files\installer_output\Rachayitha_Setup_V2.exe" "%~dp0Rachayitha_Setup_V2.exe" >nul 2>nul
    copy /y "%~dp0rachayitha code files\installer_output\Rachayitha_Setup_V2.exe" "%~dp0Rachayitha_Setup.exe" >nul 2>nul
    copy /y "%~dp0rachayitha code files\installer_output\Rachayitha_Setup_V2.exe" "%~dp0WebSite\Rachayitha_Setup_V2.exe" >nul 2>nul
    copy /y "%~dp0rachayitha code files\installer_output\Rachayitha_Setup_V2.exe" "%~dp0WebSite\Rachayitha_Setup.exe" >nul 2>nul
)
copy /y "%~dp0Rachayitha.exe" "%~dp0Rachayitha_v2.exe" >nul 2>nul
copy /y "%~dp0Rachayitha.exe" "%~dp0WebSite\Rachayitha_v2.exe" >nul 2>nul

echo [2/4] Staging changes...
git add -A

echo.
echo [3/4] Committing changes...
git commit -m "feat(v2.0): update official release links to Rachayitha_Setup_V2.exe and clean website CTA"

echo.
echo [4/4] Pushing to GitHub (main branch)...
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
