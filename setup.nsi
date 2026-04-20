; NSIS Installer Script for PDF Merger App
; This creates a professional installer executable
; 
; To build: Install NSIS from https://nsis.sourceforge.io/
; Then right-click this file and select "Compile NSIS Script"
; Or use: makensis.exe setup.nsi

; ============================================
; PDF MERGER APP INSTALLER
; ============================================

; The name of the installer
Name "PDF Merger App"

; The file to write
OutFile "PDF_Merger_App_Setup.exe"

; Default installation folder
InstallDir "$PROGRAMFILES\PDF Merger App"

; Request application privileges for Windows Vista+
RequestExecutionLevel admin

; ============================================
; Pages
; ============================================
Page license
Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

; ============================================
; License file
; ============================================
LicenseFile "LICENSE.txt"

; ============================================
; Installer Sections
; ============================================

Section "Install"
  SetOutPath "$INSTDIR"
  
  ; Copy all app files
  File "gui.py"
  File "app.py"
  File "pdf_merger.py"
  File "main.py"
  File "requirements.txt"
  File "setup.py"
  File "build_exe.py"
  File "README.md"
  File "QUICKSTART.md"
  File "DISTRIBUTION_GUIDE.md"
  File "install.bat"
  File "install.ps1"
  File "install.sh"
  
  ; Create input and output directories
  CreateDirectory "$INSTDIR\input"
  CreateDirectory "$INSTDIR\output"
  
  ; Check Python installation
  DetailPrint "Checking Python installation..."
  ExecDos::Exec 'python --version >nul 2>&1'
  ${If} $1 != 0
    MessageBox MB_ICONSTOP "Python is not installed!$\n$\nPlease install Python from:$\nhttps://www.python.org/$\n$\nMake sure to check 'Add Python to PATH' during installation."
    Abort
  ${EndIf}
  
  ; Create virtual environment
  DetailPrint "Creating Python virtual environment..."
  ExecDos::Exec 'python -m venv "$INSTDIR\.venv"'
  ${If} $1 != 0
    MessageBox MB_ICONSTOP "Failed to create virtual environment!"
    Abort
  ${EndIf}
  
  ; Install dependencies
  DetailPrint "Installing dependencies..."
  ExecDos::Exec '"$INSTDIR\.venv\Scripts\pip.exe" install --upgrade pip'
  ExecDos::Exec '"$INSTDIR\.venv\Scripts\pip.exe" install -r "$INSTDIR\requirements.txt"'
  ${If} $1 != 0
    MessageBox MB_ICONSTOP "Failed to install dependencies!$\n$\nPlease run: install.bat in the app folder manually."
    Abort
  ${EndIf}
  
  ; Create Start Menu shortcuts
  CreateDirectory "$SMPROGRAMS\PDF Merger App"
  CreateShortCut "$SMPROGRAMS\PDF Merger App\PDF Merger.lnk" "$INSTDIR\gui.py" "" "$INSTDIR\gui.py" 0
  CreateShortCut "$SMPROGRAMS\PDF Merger App\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  
  ; Create desktop shortcut
  CreateShortCut "$DESKTOP\PDF Merger.lnk" "$INSTDIR\gui.py" "" "$INSTDIR\gui.py" 0
  
  ; Write uninstaller
  WriteUninstaller "$INSTDIR\uninstall.exe"
  
  ; Write registry entries for Add/Remove Programs
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\PDFMergerApp" "DisplayName" "PDF Merger App"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\PDFMergerApp" "UninstallString" "$INSTDIR\uninstall.exe"
  
  DetailPrint "Installation complete!"
SectionEnd

; ============================================
; Uninstaller Section
; ============================================

Section "Uninstall"
  ; Remove installed files
  Delete "$INSTDIR\gui.py"
  Delete "$INSTDIR\app.py"
  Delete "$INSTDIR\pdf_merger.py"
  Delete "$INSTDIR\main.py"
  Delete "$INSTDIR\requirements.txt"
  Delete "$INSTDIR\setup.py"
  Delete "$INSTDIR\build_exe.py"
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\QUICKSTART.md"
  Delete "$INSTDIR\DISTRIBUTION_GUIDE.md"
  Delete "$INSTDIR\install.bat"
  Delete "$INSTDIR\install.ps1"
  Delete "$INSTDIR\install.sh"
  Delete "$INSTDIR\uninstall.exe"
  
  ; Remove virtual environment
  RMDir /r "$INSTDIR\.venv"
  RMDir /r "$INSTDIR\input"
  RMDir /r "$INSTDIR\output"
  RMDir /r "$INSTDIR\__pycache__"
  RMDir /r "$INSTDIR\build"
  RMDir /r "$INSTDIR\dist"
  
  ; Remove directory
  RMDir "$INSTDIR"
  
  ; Remove shortcuts
  Delete "$SMPROGRAMS\PDF Merger App\PDF Merger.lnk"
  Delete "$SMPROGRAMS\PDF Merger App\Uninstall.lnk"
  RMDir "$SMPROGRAMS\PDF Merger App"
  Delete "$DESKTOP\PDF Merger.lnk"
  
  ; Remove registry entries
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\PDFMergerApp"
SectionEnd
