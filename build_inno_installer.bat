@echo off
REM Build Inno Setup Installer
REM This script helps you create a professional PDF Merger App installer using Inno Setup

cls
echo.
echo =====================================================
echo  PDF MERGER APP - BUILD INNO SETUP INSTALLER
echo =====================================================
echo.

REM Check if Inno Setup is installed
echo Checking for Inno Setup installation...
echo.

if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
    goto found_inno
)

if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set INNO_PATH=C:\Program Files\Inno Setup 6\ISCC.exe
    goto found_inno
)

if exist "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" (
    set INNO_PATH=C:\Program Files (x86)\Inno Setup 5\ISCC.exe
    goto found_inno
)

if exist "C:\Program Files\Inno Setup 5\ISCC.exe" (
    set INNO_PATH=C:\Program Files\Inno Setup 5\ISCC.exe
    goto found_inno
)

echo [ERROR] Inno Setup is not installed on this computer
echo.
echo To create a professional installer with Inno Setup:
echo.
echo 1. Visit: https://jrsoftware.org/isdl.php
echo 2. Download the latest version
echo 3. Run the installer
echo 4. Complete installation
echo 5. Run this script again
echo.
echo Inno Setup is better than NSIS for many users!
echo.
pause
exit /b 1

:found_inno
echo [OK] Inno Setup found at: %INNO_PATH%
echo.
echo Building installer...
echo This may take 30-60 seconds...
echo.

REM Build the installer
"%INNO_PATH%" setup.iss

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to build installer
    echo.
    echo Troubleshooting:
    echo 1. Make sure all app files are in the current directory
    echo 2. Check setup.iss for syntax errors
    echo 3. Try running this script as Administrator
    echo.
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
    echo.
    for /f "tokens=5" %%A in ('dir "PDF_Merger_App_Setup.exe"') do (
        echo File size: %%A bytes
    )
    echo.
    echo Next steps:
    echo 1. Test the installer on this computer
    echo 2. Distribute PDF_Merger_App_Setup.exe to others
    echo 3. Users can double-click to install
    echo.
    echo Location: %cd%\PDF_Merger_App_Setup.exe
    echo.
    echo Installation path: C:\Program Files\PDF Merger App
    echo.
    pause
) else (
    echo [ERROR] Installer was not created
    echo.
    pause
    exit /b 1
)
