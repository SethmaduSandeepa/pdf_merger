#!/bin/bash
# PDF Merger App Installer for macOS/Linux
# Run this script with: bash install.sh

echo ""
echo "====================================="
echo "   PDF MERGER APP - INSTALLATION"
echo "====================================="
echo ""

# Check if Python is installed
echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "  Other: Visit https://www.python.org/"
    echo ""
    read -p "Press Enter to exit"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Python found: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "[2/4] Creating virtual environment..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    read -p "Press Enter to exit"
    exit 1
fi
echo "✅ Virtual environment created successfully"
echo ""

# Activate virtual environment and install dependencies
echo "[3/4] Installing dependencies..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    read -p "Press Enter to exit"
    exit 1
fi

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    read -p "Press Enter to exit"
    exit 1
fi
echo "✅ Dependencies installed successfully"
echo ""

# Installation complete
echo "[4/4] Setup complete!"
echo ""
echo "====================================="
echo "   INSTALLATION COMPLETE!"
echo "====================================="
echo ""
echo "To run the app:"
echo ""
echo "Option 1 - GUI (Recommended):"
echo "  python3 gui.py"
echo ""
echo "Option 2 - Command Line Menu:"
echo "  python3 app.py"
echo ""
echo "Or activate the virtual environment first:"
echo "  source .venv/bin/activate"
echo "  python3 gui.py"
echo ""
echo "Input folder: $(pwd)/input"
echo "Output folder: $(pwd)/output"
echo ""
read -p "Press Enter to exit"
