# PDF Merger App Installer for Windows (PowerShell)
# Run this script with: powershell -ExecutionPolicy Bypass -File install.ps1

Write-Host ""
Write-Host "====================================="
Write-Host "   PDF MERGER APP - INSTALLATION" -ForegroundColor Cyan
Write-Host "====================================="
Write-Host ""

# Check if Python is installed
Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Python found: $pythonCheck" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "[2/4] Creating virtual environment..." -ForegroundColor Yellow
python -m venv .venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Virtual environment created successfully" -ForegroundColor Green
Write-Host ""

# Activate virtual environment and install dependencies
Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "Dependencies installed successfully" -ForegroundColor Green
Write-Host ""

# Installation complete
Write-Host "[4/4] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "====================================="
Write-Host "   INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "====================================="
Write-Host ""
Write-Host "To run the app:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Option 1 - GUI (Recommended):" -ForegroundColor Yellow
Write-Host "  Run: python gui.py"
Write-Host ""
Write-Host "Option 2 - Command Line Menu:" -ForegroundColor Yellow
Write-Host "  Run: python app.py"
Write-Host ""
Write-Host "Input folder: $(Get-Location)\input"
Write-Host "Output folder: $(Get-Location)\output"
Write-Host ""
Read-Host "Press Enter to exit"
