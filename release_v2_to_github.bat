@echo off
chcp 65001 >nul
echo ======================================================================
echo   Rachayitha v2.0 - Official GitHub Release & Deployment Manager
echo ======================================================================
echo.

cd /d "%~dp0"

echo [1/4] Ensuring binary synchronization from installer_output...
set "SRC_SETUP=%~dp0rachayitha code files\installer_output\Rachayitha_Setup_V2.exe"
if exist "%SRC_SETUP%" (
    echo   Copying Rachayitha_Setup_V2.exe to root and WebSite...
    copy /y "%SRC_SETUP%" "%~dp0Rachayitha_Setup_V2.exe" >nul
    copy /y "%SRC_SETUP%" "%~dp0Rachayitha_Setup.exe" >nul
    copy /y "%SRC_SETUP%" "%~dp0WebSite\Rachayitha_Setup_V2.exe" >nul
    copy /y "%SRC_SETUP%" "%~dp0WebSite\Rachayitha_Setup.exe" >nul
    echo   [OK] Setup v2 binary synchronized.
) else (
    echo   [NOTE] Using existing root Rachayitha_Setup_V2.exe
)

if exist "%~dp0Rachayitha.exe" (
    copy /y "%~dp0Rachayitha.exe" "%~dp0Rachayitha_v2.exe" >nul
    copy /y "%~dp0Rachayitha.exe" "%~dp0WebSite\Rachayitha_v2.exe" >nul
    echo   [OK] Portable v2 binary synchronized.
)

echo.
echo [2/4] Checking GitHub CLI for automatic release upload...
where gh >nul 2>nul
if %ERRORLEVEL% NEQ 0 goto NO_GH

echo   Found GitHub CLI. Checking release Rachayitha_V2...
gh release view Rachayitha_V2 >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo   Release Rachayitha_V2 found. Uploading assets...
    gh release upload Rachayitha_V2 "%~dp0Rachayitha_Setup_V2.exe" "%~dp0Rachayitha_v2.exe" --clobber
    goto POST_UPLOAD
)

echo   Creating new release Rachayitha_V2 on GitHub...
git tag -f Rachayitha_V2
git push origin Rachayitha_V2 --force
gh release create Rachayitha_V2 "%~dp0Rachayitha_Setup_V2.exe" "%~dp0Rachayitha_v2.exe" --title "Rachayitha v2.0.0 Official Release" --notes-file "%~dp0RELEASE_NOTES_v2.0.0.md"
goto POST_UPLOAD

:NO_GH
echo   GitHub CLI is not installed or not in PATH.
echo   Opening GitHub Releases in browser and selecting file in Explorer...
start https://github.com/Ramaputhra/Rachayitha/releases
explorer.exe /select,"%~dp0Rachayitha_Setup_V2.exe"

:POST_UPLOAD
echo.
echo [3/4] Staging and committing website updates...
git add -A
git commit -m "feat(v2.0): update download link to releases/download/Rachayitha_V2/Rachayitha_Setup_V2.exe"

echo.
echo [4/4] Pushing to GitHub main branch to trigger Vercel deployment...
git push origin main

echo.
echo ======================================================================
echo   [DONE] GitHub Release and Website Deployment Synchronized!
echo   Website URL:  https://rachayitha.vercel.app/
echo   Download URL: https://github.com/Ramaputhra/Rachayitha/releases/download/Rachayitha_V2/Rachayitha_Setup_V2.exe
echo ======================================================================
echo.
pause
