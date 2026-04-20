# PDF Merger App

A user-friendly application for merging PDF letterheads with content PDFs. Built with Python and featuring both GUI and command-line interfaces.

## Features

- 📄 **Easy PDF Merging** - Overlay letterhead PDFs onto content PDFs
- 🎨 **Modern GUI** - Intuitive Tkinter-based graphical interface
- 📂 **File Management** - Browse and select PDFs from input folder
- 🔧 **Customizable Output** - Name your merged PDFs
- 📊 **Live Status** - Real-time merge progress and feedback
- 🖱️ **One-Click Operation** - Simple button-based merging

## System Requirements

- **Windows 7 or later** (or macOS/Linux)
- **Python 3.8+** (if running from source)
- **500 MB free disk space**

## Installation Options

### Option 1: Quick Installation (Recommended)

**For Windows Users:**

1. Download or copy the `PDF Merger App` folder to your computer
2. Open a Command Prompt (cmd.exe) or PowerShell
3. Navigate to the app folder:
   ```
   cd path\to\PDF Merger App
   ```
4. Run the installer:
   ```
   install.bat
   ```
5. Follow the on-screen instructions

**For macOS/Linux Users:**

1. Download or copy the `PDF Merger App` folder
2. Open Terminal and navigate to the app folder:
   ```
   cd path/to/PDF\ Merger\ App
   ```
3. Create virtual environment:
   ```
   python3 -m venv .venv
   ```
4. Activate it:
   ```
   source .venv/bin/activate
   ```
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Option 2: Standalone Executable (Windows Only)

If you prefer not to install Python:

1. Run the pre-built executable: `PDF Merger.exe`
   - No installation or Python required
   - Just extract and double-click to run

## How to Use

### GUI Version (Recommended)

1. **Run the application:**
   - Windows: Double-click `gui.py` or `PDF Merger.exe`
   - macOS/Linux: Run `python3 gui.py`

2. **Select your PDFs:**
   - Click "Browse" or "From Input Folder" for Letterhead PDF
   - Click "Browse" or "From Input Folder" for Content PDF

3. **Set output filename** (optional):
   - Change the filename if desired, or keep default
   - Default: `print_ready_merged.pdf`

4. **Click "Merge PDFs"**
   - The status log shows real-time progress
   - Success message appears when complete

5. **Find your merged PDF:**
   - Click "Open Output Folder" to see the result
   - Located in the `output/` folder

### Command Line Version

1. **Run the app:**
   ```
   python app.py
   ```

2. **Select from menu:**
   ```
   1. Merge PDFs
   2. View Input Files
   3. View Output Files
   4. Open Output Folder
   5. Settings
   6. Exit
   ```

## Folder Structure

```
PDF Merger App/
├── gui.py                 # Graphical User Interface (recommended)
├── app.py                 # Command-line menu interface
├── pdf_merger.py          # Core PDF merging logic
├── main.py                # Legacy entry point
├── requirements.txt       # Python dependencies
├── install.bat            # Windows installer script
├── README.md             # This file
├── input/                # Place PDFs to merge here
│   ├── letterhead.pdf
│   └── content.pdf
└── output/               # Merged PDFs appear here
    └── print_ready_merged.pdf
```

## Workflow

1. **Place your PDFs:**
   - Letterhead PDF in `input/` folder
   - Content PDF in `input/` folder

2. **Run the application:**
   - GUI: Double-click `gui.py`
   - Command Line: Run `python app.py`

3. **Select files and merge:**
   - Choose letterhead and content PDFs
   - Click "Merge PDFs"
   - Wait for completion

4. **Get your result:**
   - Merged PDF appears in `output/` folder
   - Ready to print!

## Troubleshooting

### "Python not found" error
- **Solution:** Install Python from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

### "Module not found" error
- **Solution:** Run the installer again or manually:
  ```
  python -m pip install -r requirements.txt
  ```

### PDF merge shows errors
- **Solution:** Ensure:
  - Both PDFs are valid PDF files
  - Both files exist in the input folder
  - Files are not corrupted

### GUI window won't open
- **Solution:** Try the command-line version:
  ```
  python app.py
  ```

## Dependencies

The app requires these Python packages (auto-installed):

- **pypdf** (6.10.2+) - PDF manipulation
- **reportlab** (4.4.10+) - PDF generation
- **pillow** - Image processing (auto-installed with reportlab)

## Uninstallation

**Windows:**
- Simply delete the `PDF Merger App` folder
- No registry entries or system files are modified

**macOS/Linux:**
- Simply delete the `PDF Merger App` folder

## Creating an Executable

To create a standalone .exe file for distribution:

```
python build_exe.py
```

This creates a single `PDF Merger.exe` file that requires no Python installation.

## Creating Desktop Shortcut

### Windows:
1. Right-click on `gui.py`
2. Select "Send to" → "Desktop (create shortcut)"
3. Name it "PDF Merger"

### Or manually:
1. Right-click on Desktop
2. Create new shortcut
3. Target: `python path\to\gui.py`
4. Name: "PDF Merger"

## Support & Feedback

If you encounter issues or have suggestions:
1. Check the troubleshooting section above
2. Check that Python and dependencies are properly installed
3. Try re-running the installer script

## License

Free to use and distribute

## Version History

- **1.0** - Initial release
  - GUI interface with Tkinter
  - PDF merging functionality
  - Command-line menu interface
  - File browser and folder management

---

**Happy PDF Merging! 📄**
