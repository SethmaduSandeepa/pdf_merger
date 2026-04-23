; Inno Setup Script for TASMA PDF Merger App
; Standalone Executable Version (No Python Required)
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
SetupIconFile=app.ico
UninstallDisplayIcon={app}\app.ico
DisableProgramGroupPage=no
AllowUNCPath=no
CloseApplications=yes
CloseApplicationsFilter=*.exe

; Require Windows 7 or later
MinVersion=6.1

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
english.InstallingLabel=Installing PDF Merger...

[Types]
Name: "full"; Description: "Full Installation"; Flags: iscustom

[Components]
Name: "app"; Description: "TASMA PDF Merger (Standalone Executable)"; Types: full; Flags: fixed

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Components: app

[Files]
; Standalone Executable - the main application
Source: "dist\PDF Merger.exe"; DestDir: "{app}"; Components: app; Flags: ignoreversion; DestName: "PDF Merger.exe"

; Application Icon
Source: "app.ico"; DestDir: "{app}"; Components: app; Flags: ignoreversion

; Documentation (optional but recommended)
Source: "README.md"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "PROFESSIONAL_INSTALLATION.md"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "QUICKSTART.md"; DestDir: "{app}"; Components: app; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Components: app; Flags: ignoreversion

[Dirs]
Name: "{localappdata}\TASMA PDF Merger\input"
Name: "{localappdata}\TASMA PDF Merger\output"

[Icons]
Name: "{group}\TASMA PDF Merger"; Filename: "{app}\PDF Merger.exe"; IconFileName: "{app}\app.ico"; Comment: "TASMA PDF Merger - Professional PDF Merging Tool"
Name: "{autodesktop}\TASMA PDF Merger"; Filename: "{app}\PDF Merger.exe"; IconFileName: "{app}\app.ico"; Tasks: desktopicon; Comment: "TASMA PDF Merger - Professional PDF Merging Tool"

[Run]
Filename: "{app}\PDF Merger.exe"; Description: "Launch TASMA PDF Merger"; Flags: nowait postinstall skipifsilent; Components: app

[UninstallDelete]
Type: dirifempty; Name: "{localappdata}\TASMA PDF Merger\input"
Type: dirifempty; Name: "{localappdata}\TASMA PDF Merger\output"
Type: dirifempty; Name: "{localappdata}\TASMA PDF Merger"

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    Log('TASMA PDF Merger installation completed successfully.');
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    Log('TASMA PDF Merger has been uninstalled.');
  end;
end;
