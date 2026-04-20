@echo off
REM PDF Merger App Installer for Windows
REM This script sets up the PDF Merger app on another computer

setlocal enabledelayedexpansion

echo.
echo =====================================
echo   PDF MERGER APP - INSTALLATION
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [1/4] Python found: 
python --version
echo.

REM Create virtual environment
echo [2/4] Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully
echo.

REM Activate virtual environment and install dependencies
echo [3/4] Installing dependencies...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Create shortcuts and launch info
echo [4/4] Setup complete!
echo.
echo =====================================
echo   INSTALLATION COMPLETE!
echo =====================================
echo.
echo To run the app:
echo.
echo Option 1 - GUI (Recommended):
echo   Run: gui.py
echo   or double-click: gui.py
echo.
echo Option 2 - Command Line Menu:
echo   Run: app.py
echo.
echo To create a desktop shortcut, you can:
echo   1. Right-click on gui.py
echo   2. Select "Send to" ^> "Desktop (create shortcut)"
echo.
echo Input folder: %cd%\input
echo Output folder: %cd%\output
echo.
pause
