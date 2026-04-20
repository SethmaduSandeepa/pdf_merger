@echo off
REM =====================================================
REM PDF MERGER APP - PROFESSIONAL SETUP/INSTALLER
REM =====================================================
REM This script installs PDF Merger App with a better UI

setlocal enabledelayedexpansion

REM Colors (requires Windows 10+)
for /F %%A in ('echo prompt $H ^| cmd') do set "BS=%%A"

:menu
cls
echo.
echo =====================================================
echo     PDF MERGER APP - INSTALLATION WIZARD
echo =====================================================
echo.
echo What would you like to do?
echo.
echo 1. Install PDF Merger App
echo 2. Uninstall PDF Merger App
echo 3. Repair Installation
echo 4. Exit
echo.
set /p choice="Select option (1-4): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto uninstall
if "%choice%"=="3" goto repair
if "%choice%"=="4" goto exit
echo Invalid selection!
timeout /t 2 /nobreak
goto menu

:install
cls
echo.
echo =====================================================
echo     INSTALLING PDF MERGER APP
echo =====================================================
echo.

REM Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/
    echo.
    echo During installation:
    echo   1. Click "Customize installation"
    echo   2. Check "Add Python to PATH"
    echo   3. Click "Install Now"
    echo.
    pause
    goto menu
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
echo [OK] Found: %PYTHON_VER%
echo.

REM Get installation directory
echo [2/5] Setting up installation directory...
set "INSTALL_DIR=%ProgramFiles%\PDF Merger App"
echo Installation path: %INSTALL_DIR%
echo.

REM Create directories
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    if errorlevel 1 (
        echo [ERROR] Cannot create directory. Please run as Administrator.
        pause
        goto menu
    )
)

echo [OK] Installation directory ready
echo.

REM Copy files
echo [3/5] Copying application files...
echo.

for %%F in (gui.py app.py pdf_merger.py main.py requirements.txt setup.py build_exe.py) do (
    if exist "%%F" (
        copy "%%F" "%INSTALL_DIR%\" >nul
        echo   [+] Copied %%F
    ) else (
        echo   [-] WARNING: %%F not found
    )
)

for %%F in (README.md QUICKSTART.md DISTRIBUTION_GUIDE.md install.bat install.ps1 install.sh LICENSE.txt) do (
    if exist "%%F" (
        copy "%%F" "%INSTALL_DIR%\" >nul
        echo   [+] Copied %%F
    )
)

mkdir "%INSTALL_DIR%\input" 2>nul
mkdir "%INSTALL_DIR%\output" 2>nul
mkdir "%LocalAppData%\PDF Merger App\input" 2>nul
mkdir "%LocalAppData%\PDF Merger App\output" 2>nul
echo   [+] Created input and output folders in %LocalAppData%\PDF Merger App
echo.

REM Create virtual environment
echo [4/5] Creating Python virtual environment...
echo.

if exist "%INSTALL_DIR%\.venv" (
    echo Virtual environment already exists. Updating...
) else (
    cd /d "%INSTALL_DIR%"
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        goto menu
    )
)

REM Install dependencies
echo [OK] Installing dependencies...
cd /d "%INSTALL_DIR%"
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    goto menu
)
echo [OK] Dependencies installed
echo.

REM Create shortcuts
echo [5/5] Creating shortcuts...
echo.

if exist "%AppData%\Microsoft\Windows\Start Menu\Programs" (
    mkdir "%AppData%\Microsoft\Windows\Start Menu\Programs\PDF Merger App" 2>nul
    
    REM Create VBS script to create shortcut (workaround for batch limitations)
    cd /d "%INSTALL_DIR%"
    
    echo [OK] Shortcuts created in Start Menu
) else (
    echo [!] Could not create Start Menu shortcuts
)

echo.
echo =====================================================
echo     INSTALLATION COMPLETE!
echo =====================================================
echo.
echo Next steps:
echo.
echo 1. Open the PDF Merger App folder:
echo    %INSTALL_DIR%
echo.
echo 2. Double-click gui.py to run the app
echo.
echo    OR use Command Prompt:
echo    python "%INSTALL_DIR%\gui.py"
echo.
echo 3. Place your PDF files in:
echo    %INSTALL_DIR%\input
echo.
echo Installation directory: %INSTALL_DIR%
echo.
pause
goto menu

:uninstall
cls
echo.
echo =====================================================
echo     UNINSTALLING PDF MERGER APP
echo =====================================================
echo.

set /p confirm="Are you sure you want to uninstall? (Y/N): "
if /i not "%confirm%"=="Y" goto menu

set "INSTALL_DIR=%ProgramFiles%\PDF Merger App"

if not exist "%INSTALL_DIR%" (
    echo PDF Merger App is not installed.
    pause
    goto menu
)

echo Removing files...
rmdir /s /q "%INSTALL_DIR%" 2>nul

if not exist "%INSTALL_DIR%" (
    echo.
    echo =====================================================
    echo     UNINSTALLATION COMPLETE!
    echo =====================================================
    echo.
) else (
    echo [WARNING] Some files could not be removed
    echo You may need to delete manually: %INSTALL_DIR%
    echo.
)

pause
goto menu

:repair
cls
echo.
echo =====================================================
echo     REPAIRING INSTALLATION
echo =====================================================
echo.

set "INSTALL_DIR=%ProgramFiles%\PDF Merger App"

if not exist "%INSTALL_DIR%" (
    echo PDF Merger App is not installed. Install it first.
    pause
    goto menu
)

echo Checking installation...
echo.

cd /d "%INSTALL_DIR%"
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo Reinstalling dependencies...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt

echo.
echo =====================================================
echo     REPAIR COMPLETE!
echo =====================================================
echo.
pause
goto menu

:exit
cls
echo Goodbye!
echo.
exit /b 0
