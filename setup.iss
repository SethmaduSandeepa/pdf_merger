; Inno Setup Script for PDF Merger App
; 
; To build this installer:
; 1. Download Inno Setup from: https://jrsoftware.org/isdl.php
; 2. Install it
; 3. Right-click this file and select "Compile with Inno Setup"
; 
; Or use command line:
; "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss

[Setup]
AppName=PDF Merger App
AppVersion=1.0.0
AppPublisher=PDF Merger
AppPublisherURL=https://github.com
DefaultDirName={autopf}\PDF Merger App
DefaultGroupName=PDF Merger App
OutputDir=.
OutputBaseFilename=PDF_Merger_App_Setup
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
Name: "full"; Description: "Full installation"
Name: "compact"; Description: "Compact installation"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "app"; Description: "PDF Merger Application"; Types: full compact custom
Name: "python"; Description: "Python Virtual Environment"; Types: full compact
Name: "shortcuts"; Description: "Start Menu Shortcuts"; Types: full
Name: "desktop"; Description: "Desktop Shortcut"; Types: full

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "python_path"; Description: "Add Python to PATH"; GroupDescription: "Python Configuration"
Name: "associate_pdf"; Description: "Associate PDF with PDF Merger"; GroupDescription: "File Associations"; Flags: unchecked

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
Name: "{localappdata}\PDF Merger App\input"
Name: "{localappdata}\PDF Merger App\output"
Name: "{app}\.venv"; Components: python

[Icons]
Name: "{group}\PDF Merger"; Filename: "{app}\gui.py"; Components: shortcuts; Comment: "PDF Merger Application"
Name: "{group}\Uninstall PDF Merger"; Filename: "{uninstallexe}"; Components: shortcuts
Name: "{autodesktop}\PDF Merger"; Filename: "{app}\gui.py"; Tasks: desktopicon; Comment: "PDF Merger Application"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\PDF Merger"; Filename: "{app}\gui.py"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\install.bat"; Parameters: "auto"; Flags: runhidden; StatusMsg: "Installing Python dependencies..."; Description: "Install Python dependencies"
Filename: "{app}\gui.py"; Flags: shellexec skipifsilent; StatusMsg: "Launching PDF Merger..."; Description: "Launch application"

[UninstallDelete]
Type: dirifempty; Name: "{localappdata}\PDF Merger App\input"
Type: dirifempty; Name: "{localappdata}\PDF Merger App\output"
Type: dirifempty; Name: "{localappdata}\PDF Merger App"
Type: dirifempty; Name: "{app}\input"
Type: dirifempty; Name: "{app}\output"
Type: dirifempty; Name: "{app}\.venv"
Type: dirifempty; Name: "{app}"

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    { Log installation completion }
    Log('PDF Merger App installation completed successfully.');
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    { Log uninstall completion }
    Log('PDF Merger App has been uninstalled.');
  end;
end;
