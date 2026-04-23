@echo off
REM Build professional Inno Setup installer for PDF Merger App
REM
REM This script requires:
REM 1. Inno Setup 6 installed (https://jrsoftware.org/isdl.php)
REM 2. Standalone executable already built (run build_exe.py first)

echo.
echo ========================================
echo PDF Merger - Professional Installer Build
echo ========================================
echo.

REM Check if Inno Setup is installed
set INNO_SETUP=C:\Program Files (x86)\Inno Setup 6\ISCC.exe

if not exist "%INNO_SETUP%" (
    echo ERROR: Inno Setup 6 not found!
    echo.
    echo Please install Inno Setup 6 from:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo After installation, run this script again.
    pause
    exit /b 1
)

REM Check if standalone executable exists
if not exist "dist\PDF Merger.exe" (
    echo ERROR: Standalone executable not found!
    echo.
    echo Please run 'python build_exe.py' first to create the executable.
    pause
    exit /b 1
)

echo [1] Building Inno Setup installer...
echo.

"%INNO_SETUP%" setup.iss

if errorlevel 1 (
    echo.
    echo ERROR: Inno Setup compilation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Installer created:
echo ========================================
echo.
echo File: TASMA_PDF_Merger_Setup.exe
echo Location: %CD%\TASMA_PDF_Merger_Setup.exe
echo.
echo You can now distribute this .exe file to users!
echo.
echo Installation Instructions for Users:
echo   1. Share TASMA_PDF_Merger_Setup.exe with users
echo   2. Users double-click the .exe to install
echo   3. No Python or additional software required!
echo   4. Desktop shortcut created automatically
echo.
pause

if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    set NSIS_PATH=C:\Program Files (x86)\NSIS\makensis.exe
    goto found_nsis
)

if exist "C:\Program Files\NSIS\makensis.exe" (
    set NSIS_PATH=C:\Program Files\NSIS\makensis.exe
    goto found_nsis
)

echo [ERROR] NSIS is not installed on this computer
echo.
echo To create a professional installer, you need NSIS:
echo.
echo 1. Visit: https://nsis.sourceforge.io/
echo 2. Download the latest version
echo 3. Run the installer
echo 4. Complete installation
echo 5. Run this script again
echo.
echo Or use: setup_wizard.bat for a simpler installation method
echo.
pause
exit /b 1

:found_nsis
echo [OK] NSIS found at: %NSIS_PATH%
echo.
echo Building installer...
echo.

REM Build the installer
"%NSIS_PATH%" setup.nsi

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to build installer
    pause
    exit /b 1
)

REM Check if installer was created
if exist "PDF_Merger_App_Setup.exe" (
    echo.
    echo =====================================================
    echo  BUILD SUCCESSFUL!
    echo =====================================================
    echo.
    echo Installer created: PDF_Merger_App_Setup.exe
    echo File size: 
    for /f "tokens=5" %%A in ('dir "PDF_Merger_App_Setup.exe"') do echo   %%A bytes
    echo.
    echo Next steps:
    echo 1. Test the installer on this computer
    echo 2. Distribute PDF_Merger_App_Setup.exe to others
    echo 3. Users can double-click to install
    echo.
    echo Location: %cd%\PDF_Merger_App_Setup.exe
    echo.
) else (
    echo [ERROR] Installer was not created
    pause
    exit /b 1
)

pause
