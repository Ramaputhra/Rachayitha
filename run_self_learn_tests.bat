@echo off
chcp 65001 >nul
echo ========================================================
echo   Running Rachayitha Adaptive Self-Learning Test Suite
echo ========================================================
if exist "test_self_learn.py" (
    python "test_self_learn.py"
) else (
    python "rachayitha code files\test_self_learn.py"
)
echo.
pause
