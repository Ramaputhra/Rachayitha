@echo off
echo ========================================================
echo   Building Rachayitha (రచయిత) Standalone Windows App
echo ========================================================

echo.
echo [1/3] Preparing application icons from rachayitha_logo.png...
python prepare_icons.py

echo.
echo [2/3] Checking PyInstaller...
pip show pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing pyinstaller...
    pip install pyinstaller
)

echo.
echo [3/3] Compiling standalone Rachayitha.exe with Halant-First engine...
pyinstaller --noconsole --onefile --name="Rachayitha" --icon="icon.ico" --add-data "data;data" --add-data "engine;engine" --add-data "ui;ui" --add-data "rachayitha_logo.png;." main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] PyInstaller compilation failed! Check logs above.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo   SUCCESS! Standalone Windows App created at:
echo   dist\Rachayitha.exe
echo ========================================================
pause
