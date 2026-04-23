; Inno Setup Script for TASMA PDF Merger App
; 
; To build this installer:
; 1. Download Inno Setup from: https://jrsoftware.org/isdl.php
; 2. Install it
; 3. Right-click this file and select "Compile with Inno Setup"
; 
; Or use command line:
; "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss

[Setup]
AppName=TASMA PDF Merger
AppVersion=1.0.1
AppPublisher=TASMA IT Department
AppPublisherURL=https://github.com
DefaultDirName={autopf}\TASMA PDF Merger
DefaultGroupName=TASMA PDF Merger
OutputDir=.
OutputBaseFilename=TASMA_PDF_Merger_Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
WizardStyle=modern
; SetupIconFile=setup_icon.ico  (commented out - icon file not required)
UninstallDisplayIcon={app}\gui.py

; Require Windows 7 or later
MinVersion=6.1

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Types]
Name: "full"; Description: "Standard installation"

[Components]
Name: "app"; Description: "TASMA PDF Merger Application"; Types: full

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Application files
Source: "gui.py"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "app.py"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "pdf_merger.py"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "main.py"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "setup.py"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "build_exe.py"; DestDir: "{app}"; Components: app; Flags: ignoreversion

; Documentation
Source: "README.md"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "QUICKSTART.md"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "SETUP_GUIDE.md"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "DISTRIBUTION_GUIDE.md"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "DISTRIBUTION_CHECKLIST.md"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Components: app; Flags: ignoreversion

; Setup scripts
Source: "install.bat"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "install.ps1"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "install.sh"; DestDir: "{app}"; Components: app; Flags: ignoreversion

[Dirs]
Name: "{localappdata}\TASMA PDF Merger\input"
Name: "{localappdata}\TASMA PDF Merger\output"

[Icons]
Name: "{group}\TASMA PDF Merger"; Filename: "{app}\gui.py"; Comment: "TASMA PDF Merger Application"
Name: "{autodesktop}\TASMA PDF Merger"; Filename: "{app}\gui.py"; Tasks: desktopicon; Comment: "TASMA PDF Merger Application"

[Run]
Filename: "{app}\gui.py"; Flags: shellexec skipifsilent; Description: "Launch TASMA PDF Merger"

[UninstallDelete]
Type: dirifempty; Name: "{localappdata}\TASMA PDF Merger\input"
Type: dirifempty; Name: "{localappdata}\TASMA PDF Merger\output"
Type: dirifempty; Name: "{localappdata}\TASMA PDF Merger"
Type: dirifempty; Name: "{app}\input"
Type: dirifempty; Name: "{app}\output"
Type: dirifempty; Name: "{app}"

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    { Log installation completion }
    Log('TASMA PDF Merger installation completed successfully.');
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    { Log uninstall completion }
    Log('TASMA PDF Merger has been uninstalled.');
  end;
end;
