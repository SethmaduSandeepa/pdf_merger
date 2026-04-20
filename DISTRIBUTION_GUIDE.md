# PDF Merger App - Installation & Distribution Guide

This guide explains how to install and distribute the PDF Merger App to other computers.

## Quick Start for End Users

### For Windows Users (Easiest)

1. **Extract the folder** to your computer
2. **Double-click `install.bat`** (Windows batch installer)
3. **Wait for installation** to complete
4. **Run the app** by double-clicking `gui.py`

### For macOS/Linux Users

1. **Extract the folder** to your computer
2. **Open Terminal** and navigate to the folder:
   ```
   cd /path/to/PDF\ Merger\ App
   ```
3. **Make install script executable** (macOS/Linux only):
   ```
   chmod +x install.sh
   ```
4. **Run installer** or manually:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
5. **Run the app:**
   ```
   python3 gui.py
   ```

---

## Distribution Methods

### Method 1: Standalone Executable (Windows Only)

**Easiest for non-technical users - No Python required!**

**Steps to create:**

1. Run the build script:
   ```
   python build_exe.py
   ```

2. You'll get a file: `dist/PDF Merger.exe`

3. **To distribute:**
   - Users can simply double-click `PDF Merger.exe` to run
   - No installation, no Python required
   - File size: ~50-100 MB

**Advantages:**
- ✅ Easiest for end users
- ✅ No Python installation needed
- ✅ Single executable file

**Disadvantages:**
- ❌ Larger file size
- ❌ Windows only

---

### Method 2: ZIP Archive with Installer

**Good balance of simplicity and compatibility**

**Steps to distribute:**

1. Collect these files in a folder:
   ```
   PDF Merger App/
   ├── gui.py
   ├── app.py
   ├── pdf_merger.py
   ├── main.py
   ├── requirements.txt
   ├── install.bat
   ├── install.ps1
   ├── README.md
   ├── input/
   └── output/
   ```

2. **Zip the folder:** Right-click → Send to → Compressed (zipped) folder

3. **Share the ZIP file** with others

4. **Installation instructions for recipients:**
   - Extract the ZIP file
   - Double-click `install.bat` (Windows) or run the PowerShell script
   - Done!

**Advantages:**
- ✅ Works on Windows, macOS, Linux
- ✅ Easy installation with automatic setup
- ✅ Smaller file size than executable
- ✅ Includes source code

**Disadvantages:**
- ❌ Requires Python to be installed
- ❌ Slightly more complex setup

---

### Method 3: Python Package (pip)

**For developers or advanced users**

**Create package:**

```
pip install wheel
python setup.py sdist bdist_wheel
```

**Upload to PyPI:**

1. Create PyPI account at https://pypi.org/
2. Install twine:
   ```
   pip install twine
   ```
3. Upload:
   ```
   twine upload dist/*
   ```

**Users can then install with:**

```
pip install pdf-merger-app
```

**Advantages:**
- ✅ Professional package distribution
- ✅ Easy version management
- ✅ Standard Python installation method

**Disadvantages:**
- ❌ Requires PyPI account
- ❌ More complex setup
- ❌ Requires developer knowledge

---

### Method 4: MSI Installer (Windows Only)

**Professional installation experience**

**Tools needed:**
- WiX Toolset or Inno Setup

**Benefits:**
- ✅ Professional installer with GUI
- ✅ Easy uninstall from Control Panel
- ✅ Can set up Start Menu shortcuts

**Note:** More complex to set up. Use Method 1 or 2 for simplicity.

---

## Comparison Table

| Method | Setup Ease | File Size | Windows | Mac/Linux | Python Required |
|--------|-----------|-----------|---------|-----------|-----------------|
| **Executable** | ⭐⭐⭐ | 100 MB | ✅ | ❌ | No |
| **ZIP + Installer** | ⭐⭐ | 10 MB | ✅ | ✅ | Yes |
| **Python Package** | ⭐ | 1 MB | ✅ | ✅ | Yes |
| **MSI Installer** | ⭐⭐⭐ | 50 MB | ✅ | ❌ | No |

---

## Recommended Distribution Methods

### For Non-Technical Users:
**→ Use the Standalone Executable** (`PDF Merger.exe`)

### For Small Teams:
**→ Use ZIP with Installer** (install.bat/install.ps1)

### For Developers/Advanced Users:
**→ Use Python Package** via pip

---

## Installation Troubleshooting

### Windows Users

**"Python is not installed" error:**
- Install Python from https://www.python.org/
- During installation, **check "Add Python to PATH"**

**"Access Denied" installing batch file:**
- Right-click `install.bat`
- Select "Run as Administrator"

**".venv" folder shows after installation:**
- This is normal - it contains Python dependencies
- Don't delete it

### macOS/Linux Users

**"Command not found: python3":**
- Install Python 3: `brew install python3` (macOS) or `apt install python3` (Linux)

**Permission denied on install script:**
```
chmod +x install.sh
./install.sh
```

---

## Sharing Instructions Template

Copy this for users:

```
=== PDF MERGER APP INSTALLATION ===

1. Download and extract the ZIP file
2. Windows users: Double-click 'install.bat'
   Mac/Linux users: 
   - Open Terminal
   - cd to app folder
   - Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

3. Run the app:
   - Windows: Double-click 'gui.py'
   - Mac/Linux: python3 gui.py

4. Place your PDFs in the 'input' folder
5. Click 'Merge PDFs' in the app
6. Find results in 'output' folder

Need help? See README.md
```

---

## Version Control & Updates

To track versions for distribution:

1. Update version in `setup.py`
2. Create git tag: `git tag v1.0.0`
3. Push to repository
4. Users can clone specific versions or download releases

---

## Support Files to Include

Always include with distribution:

- ✅ `README.md` - Instructions and features
- ✅ `requirements.txt` - Dependencies list
- ✅ `install.bat` / `install.ps1` - Installers
- ✅ `LICENSE` - License information (if applicable)
- ✅ `CHANGES.md` - Version history

---

## Quick Command Reference

```bash
# Create standalone executable
python build_exe.py

# Create Python package
python setup.py sdist bdist_wheel

# Install as development package
pip install -e .

# Run GUI version
python gui.py

# Run CLI version
python app.py
```

---

**Happy distributing! 🚀**
