@echo off
setlocal

echo ========================================================
echo   Rachayitha (రచయిత) - Windows Application Installer
echo ========================================================

set "INSTALL_DIR=%LOCALAPPDATA%\Programs\Rachayitha"
set "EXE_SOURCE=dist\Rachayitha.exe"

if not exist "%EXE_SOURCE%" (
    echo [ERROR] %EXE_SOURCE% not found!
    echo Please run build_standalone.bat first to generate the executable.
    pause
    exit /b 1
)

echo.
echo [1/3] Copying application files to:
echo       %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
copy /Y "%EXE_SOURCE%" "%INSTALL_DIR%\Rachayitha.exe" >nul
if exist "rachayitha_logo.png" copy /Y "rachayitha_logo.png" "%INSTALL_DIR%\rachayitha_logo.png" >nul
if exist "icon.ico" copy /Y "icon.ico" "%INSTALL_DIR%\icon.ico" >nul
if exist "data" xcopy /E /I /Y "data" "%INSTALL_DIR%\data" >nul

echo.
echo [2/3] Creating Desktop and Windows Startup shortcuts...
powershell -NoProfile -Command "$ws = New-Object -ComObject WScript.Shell; $d = [Environment]::GetFolderPath('Desktop'); $s = $ws.CreateShortcut(\"$d\Rachayitha.lnk\"); $s.TargetPath = '%INSTALL_DIR%\Rachayitha.exe'; $s.WorkingDirectory = '%INSTALL_DIR%'; if (Test-Path '%INSTALL_DIR%\icon.ico') { $s.IconLocation = '%INSTALL_DIR%\icon.ico'; }; $s.Save(); $su = [Environment]::GetFolderPath('Startup'); $s2 = $ws.CreateShortcut(\"$su\Rachayitha.lnk\"); $s2.TargetPath = '%INSTALL_DIR%\Rachayitha.exe'; $s2.WorkingDirectory = '%INSTALL_DIR%'; if (Test-Path '%INSTALL_DIR%\icon.ico') { $s2.IconLocation = '%INSTALL_DIR%\icon.ico'; }; $s2.Save();"

echo.
echo [3/3] Launching Rachayitha now...
start "" "%INSTALL_DIR%\Rachayitha.exe"

echo.
echo ========================================================
echo   SUCCESS! Rachayitha has been installed to your PC:
echo   - Desktop shortcut created with official logo
echo   - Auto-start on Windows boot enabled
echo   - App is now running in your System Tray!
echo.
echo   Press Alt+T in any app to type Telugu.
echo   Click the 'తె'/'EN' tray icon to open Settings.
echo ========================================================
pause
