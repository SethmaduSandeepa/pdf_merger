@echo off
REM Build NSIS Installer
REM This script helps you create a professional PDF Merger App installer

cls
echo.
echo =====================================================
echo  PDF MERGER APP - BUILD INSTALLER
echo =====================================================
echo.

REM Check if NSIS is installed
echo Checking for NSIS installation...
echo.

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
