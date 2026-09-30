@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ======================================================================
echo    Rachayitha (రచయిత) — Building Windows Final Single Installer
echo ======================================================================
echo.

cd /d "%~dp0rachayitha code files"

:: Check for python executable
set "PYTHON_EXE="
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_EXE=python"
) else (
    where py >nul 2>nul
    if !ERRORLEVEL! EQU 0 (
        set "PYTHON_EXE=py -3"
    )
)

if "%PYTHON_EXE%"=="" (
    echo [ERROR] Python was not found in your PATH.
    echo Please install Python 3.10+ or add python.exe to your System PATH.
    pause
    exit /b 1
)

echo [1/3] Running clean single installer builder with %PYTHON_EXE%...
echo       - Compiling Rachayitha.exe (Halant-First + Casual 58k+ engine)
echo       - Compiling Rachayitha_Setup.exe (Graphical setup wizard with live showcase)
echo       - Syncing binaries to root workspace and WebSite/
echo.

%PYTHON_EXE% make_single_installer.py
set BUILD_STATUS=%ERRORLEVEL%

if %BUILD_STATUS% EQU 0 (
    echo.
    echo ======================================================================
    echo   [SUCCESS] Final Windows Installation Package Built Successfully!
    echo ======================================================================
    echo   Installer Location:
    echo     1. %~dp0rachayitha code files\installer_output\Rachayitha_Setup.exe
    echo     2. %~dp0Rachayitha_Setup.exe
    echo     3. %~dp0WebSite\Rachayitha_Setup.exe
    echo.
    echo   Portable App Location:
    echo     * %~dp0Rachayitha.exe
    echo     * %~dp0WebSite\Rachayitha.exe
    echo ======================================================================
    echo.
    echo Opening output folder in Windows Explorer...
    start "" explorer.exe /select,"%~dp0rachayitha code files\installer_output\Rachayitha_Setup.exe"
) else (
    echo.
    echo ======================================================================
    echo   [ERROR] Installer build failed with error code: %BUILD_STATUS%
    echo   Please check the error trace above.
    echo ======================================================================
)

echo.
pause
