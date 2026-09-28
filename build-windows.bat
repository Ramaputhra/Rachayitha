@echo off
echo ========================================================
echo   Rachayitha (రచయిత) - Windows Native Standalone Build
echo ========================================================

echo.
echo [1/3] Preparing application icons...
python scripts\setup_icons.py

echo.
echo [2/3] Checking Rust & Cargo environment...
where cargo >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Rust / Cargo is not found in your PATH!
    echo Please install Rust from https://rustup.rs and try again.
    pause
    exit /b 1
)

echo.
echo [3/3] Compiling standalone Rachayitha release binary...
cd src-tauri
cargo build --release
if %errorlevel% neq 0 (
    echo [ERROR] Build failed! Check compiler logs above.
    cd ..
    pause
    exit /b 1
)

cd ..
echo.
echo ========================================================
echo   SUCCESS! Standalone binary built:
echo   target\release\rachayitha.exe
echo ========================================================
pause
