@echo off
setlocal

echo ======================================================================
echo    Rachayitha v2.0 - Building Windows Final Single Installer
echo ======================================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "CODE_DIR=%SCRIPT_DIR%rachayitha code files"

echo [1/3] Running canonical workspace cleanup...
python "%SCRIPT_DIR%clean_workspace.py"

cd /d "%CODE_DIR%"

echo.
echo [2/3] Running 100%% accuracy test suite...
python test_casual_type.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ======================================================================
    echo   [ERROR] Tests failed! Aborting installer build to guarantee quality.
    echo ======================================================================
    pause
    exit /b 1
)

echo.
echo [3/3] Compiling fresh standalone app and setup installer...
python make_single_installer.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo   [SUCCESS] Final Windows Installation Package Built Successfully!
    echo ======================================================================
    copy /y "%SCRIPT_DIR%Rachayitha.exe" "%SCRIPT_DIR%Rachayitha_v2.exe" >nul
    copy /y "%SCRIPT_DIR%Rachayitha.exe" "%SCRIPT_DIR%WebSite\Rachayitha_v2.exe" >nul
    echo   Installer Location:
    echo     1. %CODE_DIR%\installer_output\Rachayitha_Setup.exe
    echo     2. %SCRIPT_DIR%Rachayitha_Setup.exe
    echo     3. %SCRIPT_DIR%WebSite\Rachayitha_Setup.exe
    echo.
    echo   Portable App Location:
    echo     * %SCRIPT_DIR%Rachayitha.exe
    echo     * %SCRIPT_DIR%Rachayitha_v2.exe
    echo     * %SCRIPT_DIR%WebSite\Rachayitha.exe
    echo     * %SCRIPT_DIR%WebSite\Rachayitha_v2.exe
    echo ======================================================================
    echo.
    start "" explorer.exe /select,"%CODE_DIR%\installer_output\Rachayitha_Setup.exe"
) else (
    echo.
    echo ======================================================================
    echo   [ERROR] Installer build failed with error code: %ERRORLEVEL%
    echo ======================================================================
)

echo.
pause
