# PDF Merger App - Setup & Installation Guide

This guide explains how to create professional setup files for installing the PDF Merger App on other computers.

## Setup Files Included

### 1. **setup_wizard.bat** (RECOMMENDED - Windows Only)
A professional batch-based installer with menu interface.

**Features:**
- ✅ Professional menu system
- ✅ Install, Uninstall, Repair options
- ✅ Automatic Python checking
- ✅ Virtual environment setup
- ✅ Dependency installation
- ✅ Shortcut creation
- ✅ No external tools needed

**How to use:**
```bash
# Run as Administrator
setup_wizard.bat
```

**Advantages:**
- Single executable file
- User-friendly interface
- Works on all Windows versions
- No additional tools needed
- Only ~50 KB in size

---

### 2. **setup.nsi** (PROFESSIONAL - Windows Only)
NSIS installer script for creating a professional .exe installer.

**Features:**
- ✅ Professional Windows installer look
- ✅ License agreement page
- ✅ Directory selection
- ✅ Start Menu shortcuts
- ✅ Desktop shortcut
- ✅ Uninstall support
- ✅ Registry entries for Add/Remove Programs

**Requirements:**
- NSIS (Nullsoft Scriptable Install System)
- Download from: https://nsis.sourceforge.io/

**How to create installer:**

1. **Install NSIS:**
   - Download from https://nsis.sourceforge.io/
   - Run installer
   - Complete installation

2. **Build the installer:**
   - Option A: Right-click `setup.nsi` → "Compile NSIS Script"
   - Option B: Open Command Prompt and run:
     ```
     "C:\Program Files (x86)\NSIS\makensis.exe" setup.nsi
     ```

3. **Output:**
   - Creates: `PDF_Merger_App_Setup.exe` (~1-2 MB)
   - Ready to distribute!

**Advantages:**
- Professional installer experience
- Windows standard installation
- Easy uninstall from Control Panel
- Add/Remove Programs integration
- Start Menu shortcuts

---

## Installation Methods for End Users

### Method 1: Setup Wizard (EASIEST)

**For users:**
1. Run `setup_wizard.bat` as Administrator
2. Select "Install PDF Merger App"
3. Follow prompts
4. Done!

**Command line:**
```batch
setup_wizard.bat
```

---

### Method 2: Professional NSIS Installer

**For users:**
1. Download `PDF_Merger_App_Setup.exe`
2. Double-click to run
3. Follow installation wizard
4. Done!

**Can be uninstalled via:**
- Add/Remove Programs (Control Panel)
- Windows Settings → Apps

---

### Method 3: Manual Installation

**For advanced users:**
1. Extract app folder
2. Run: `install.bat`
3. Or run: `python gui.py` directly

---

## Step-by-Step: Creating Installer

### Quick Start (5 minutes)

1. **Install NSIS:**
   - Visit https://nsis.sourceforge.io/
   - Download and run installer
   - Complete installation (takes 2-3 minutes)

2. **Build installer:**
   - Right-click `setup.nsi`
   - Select "Compile NSIS Script"
   - Wait ~30 seconds
   - Get `PDF_Merger_App_Setup.exe`

3. **Test it:**
   - Run the .exe file
   - Follow the installation wizard
   - Verify app works after installation

4. **Share it:**
   - Distribute `PDF_Merger_App_Setup.exe` to others
   - Users just double-click and it installs!

---

## Customizing the NSIS Installer

Edit `setup.nsi` to customize:

```nsi
; Change app name
Name "PDF Merger App v1.0"

; Change installer filename
OutFile "MyCustomSetup.exe"

; Change install location default
InstallDir "$PROGRAMFILES\My PDF Tool"

; Add icon (optional)
Icon "path\to\icon.ico"
BrandingText "Company Name"
```

---

## Distribution Checklist

Before distributing, ensure you have:

- ✅ `setup_wizard.bat` (for users without NSIS)
- ✅ `setup.nsi` (for building .exe installer)
- ✅ `PDF_Merger_App_Setup.exe` (pre-built installer)
- ✅ `README.md` (user guide)
- ✅ `QUICKSTART.md` (quick start guide)
- ✅ `LICENSE.txt` (license file)
- ✅ All Python source files (gui.py, app.py, pdf_merger.py, etc.)
- ✅ `requirements.txt` (dependencies)

---

## Installer Troubleshooting

### Issue: "Windows protected your PC" message
**Solution:**
- Click "More info"
- Click "Run anyway"
- This is normal for unsigned installers

### Issue: "Admin privileges required"
**Solution:**
- Right-click installer
- Select "Run as Administrator"

### Issue: Installation fails due to Python
**Solution:**
- User needs to install Python first
- Visit https://www.python.org/
- Check "Add Python to PATH" during installation

### Issue: Uninstall doesn't work
**Solution:**
- Run as Administrator
- Delete folder manually: `C:\Program Files\PDF Merger App`

---

## Installer Comparison

| Feature | setup_wizard.bat | setup.nsi .exe |
|---------|------------------|-----------------|
| **File Size** | 20 KB | 1-2 MB |
| **Professional Look** | ⭐⭐ | ⭐⭐⭐ |
| **Ease of Use** | ⭐⭐⭐ | ⭐⭐⭐ |
| **Add/Remove Programs** | ❌ | ✅ |
| **Desktop Shortcut** | ⭐ | ✅ |
| **Start Menu Entry** | ⭐ | ✅ |
| **Requires Tools** | ❌ | NSIS |
| **Creation Time** | 1 min | 5 min |

---

## Creating a Complete Distribution Package

### For Distribution (All-in-One ZIP):

1. Create folder structure:
   ```
   PDF Merger App/
   ├── setup_wizard.bat
   ├── setup.nsi
   ├── gui.py
   ├── app.py
   ├── pdf_merger.py
   ├── main.py
   ├── requirements.txt
   ├── README.md
   ├── QUICKSTART.md
   ├── LICENSE.txt
   ├── input/
   └── output/
   ```

2. Create ZIP file:
   - Right-click folder
   - "Send to" → "Compressed folder"
   - Name it: `PDF_Merger_App_v1.0.zip`

3. Share with users:
   - Upload to cloud storage
   - Email file
   - Share on website

---

## Creating Professional Installer (With NSIS)

### Step 1: Prepare Files
```
Ensure you have:
- setup.nsi
- All Python files (gui.py, app.py, etc.)
- requirements.txt
- LICENSE.txt
- README.md files
```

### Step 2: Install NSIS
- Download from https://nsis.sourceforge.io/
- Run installer
- Complete installation

### Step 3: Build
```batch
cd path\to\app
"C:\Program Files (x86)\NSIS\makensis.exe" setup.nsi
```

### Step 4: Output
- Get `PDF_Merger_App_Setup.exe`
- Test it on a clean machine
- Distribute!

---

## Advanced: Code Signing (Optional)

To remove "Windows protected your PC" warnings:

1. Get a code signing certificate
2. Sign your .exe file:
   ```
   signtool.exe sign /f certificate.pfx PDF_Merger_App_Setup.exe
   ```

This requires a certificate from a trusted authority (paid).

---

## Recommended Distribution Strategy

### For Small Teams/Individuals:
**→ Use `setup_wizard.bat`**
- Just run it
- No setup needed
- Works perfectly

### For Professional Distribution:
**→ Use `setup.nsi` → Create `PDF_Merger_App_Setup.exe`**
- Professional appearance
- Better user experience
- Easy to uninstall

### For Web Distribution:
**→ Use ZIP with `setup_wizard.bat`**
- Can host anywhere
- Users extract and run
- No installation tool needed

---

## Next Steps

1. **Test locally:**
   - Run `setup_wizard.bat` as administrator
   - Verify installation works
   - Test the app after installation

2. **Create professional installer (optional):**
   - Install NSIS
   - Run `setup.nsi`
   - Get `.exe` installer

3. **Package for distribution:**
   - ZIP all files
   - Or distribute `.exe` file
   - Include README for instructions

4. **Share with others:**
   - Upload to cloud
   - Email links
   - Share on USB drive

---

## Support Resources

- **NSIS Documentation:** https://nsis.sourceforge.io/
- **Python Installation:** https://www.python.org/
- **Setup Issues:** Check README.md troubleshooting section

---

**You're ready to distribute! 🚀**
