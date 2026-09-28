; Inno Setup Script for Rachayitha (రచయిత)
; Creates a single standalone Windows Installer (Rachayitha_Setup.exe)

[Setup]
AppName=Rachayitha
AppVersion=1.0.0
AppPublisher=Ramaputhra
AppComments=Cross-Platform Real-Time Telugu Phonetic Transliteration Tool
DefaultDirName={autopf}\Rachayitha
DefaultGroupName=Rachayitha
OutputDir=installer_output
OutputBaseFilename=Rachayitha_Setup
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
DisableProgramGroupPage=yes

[Files]
Source: "dist\Rachayitha.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Rachayitha"; Filename: "{app}\Rachayitha.exe"; WorkingDir: "{app}"
Name: "{group}\Uninstall Rachayitha"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Rachayitha"; Filename: "{app}\Rachayitha.exe"; WorkingDir: "{app}"
Name: "{autostartup}\Rachayitha"; Filename: "{app}\Rachayitha.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\Rachayitha.exe"; Description: "Launch Rachayitha now (sits in System Tray)"; Flags: nowait postinstall skipifsilent
