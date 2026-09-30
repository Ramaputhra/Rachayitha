@echo off
chcp 65001 > nul
echo ========================================================
echo   Rachayitha (రచయిత) - Pushing Latest Changes to GitHub
echo ========================================================
echo.
cd /d "%~dp0"

echo [1/4] Checking Git Status...
git status -s
echo.

echo [2/4] Staging all updated project files...
git add -A
echo.

echo [3/4] Committing changes...
git commit -m "feat(casual-typing): implement 58k dictionary, Sandhi conjugations, cyber showcase UI, and installer pipeline"
echo.

echo [4/4] Pushing to GitHub (origin main)...
git push origin main
echo.

if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo   [SUCCESS] Successfully pushed all changes to GitHub!
    echo   Vercel / GitHub Actions will automatically deploy.
    echo ========================================================
) else (
    echo ========================================================
    echo   [NOTICE] Git push encountered an issue.
    echo   If prompted, please authenticate or check remote branch.
    echo ========================================================
)

echo.
pause
