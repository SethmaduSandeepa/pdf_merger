# PDF Merger App - Inno Setup Guide

## 🎯 What is Inno Setup?

Inno Setup is a professional, free installer creation system for Windows. It's:
- ✅ User-friendly
- ✅ Creates professional installers
- ✅ Small file size (~1 MB)
- ✅ Widely used and trusted
- ✅ Easier than NSIS for beginners
- ✅ Active community support

**Download:** https://jrsoftware.org/isdl.php

---

## 📦 Installation Setup Files Included

### **setup.iss**
- Inno Setup script file
- Defines how the installer works
- Pre-configured for PDF Merger App
- Ready to compile

### **build_inno_installer.bat**
- Helper batch file
- Automatically finds Inno Setup
- Compiles setup.iss
- Creates PDF_Merger_App_Setup.exe

---

## 🚀 Quick Start (5 Minutes)

### **Step 1: Download Inno Setup (2 minutes)**

1. Visit: https://jrsoftware.org/isdl.php
2. Download "Inno Setup 6" (or latest version)
3. Run the installer
4. Click "Next" through all dialogs
5. Complete installation
6. You're done!

### **Step 2: Build Your Installer (3 minutes)**

**Option A: Using the Batch Helper**
```batch
build_inno_installer.bat
```
- Automatically finds Inno Setup
- Compiles setup.iss
- Creates PDF_Merger_App_Setup.exe
- Done!

**Option B: Using Inno Setup GUI**
1. Open Inno Setup
2. File → Open → Select `setup.iss`
3. Click "Compile"
4. Wait for completion
5. Get `PDF_Merger_App_Setup.exe`

### **Step 3: Test & Share**
1. Run `PDF_Merger_App_Setup.exe`
2. Go through installation
3. Verify app works
4. Share with others!

---

## 📋 Detailed Instructions

### Installation Steps

**Step 1: Install Inno Setup**

1. **Download:**
   - Visit https://jrsoftware.org/isdl.php
   - Click "Download Inno Setup 6"
   - Or download latest version

2. **Run installer:**
   - Double-click downloaded file
   - Click "Next" on welcome screen
   - Accept license agreement
   - Choose "Full installation"
   - Click "Install"
   - Wait for completion (1-2 minutes)

3. **Verify installation:**
   - Inno Setup should be in Start Menu
   - Or at: `C:\Program Files (x86)\Inno Setup 6\`

**Step 2: Prepare Your Files**

Make sure you have in the app folder:
```
✅ setup.iss (included)
✅ gui.py, app.py, pdf_merger.py, main.py
✅ requirements.txt
✅ README.md, LICENSE.txt
✅ Other documentation files
✅ install.bat, install.ps1, install.sh
```

**Step 3: Build Installer**

### Method 1: Using Batch Helper (EASIEST)

```batch
build_inno_installer.bat
```

The batch file will:
1. Find Inno Setup automatically
2. Compile setup.iss
3. Create PDF_Merger_App_Setup.exe
4. Show success message

### Method 2: Using Inno Setup GUI

1. Open Inno Setup
   - Start Menu → Inno Setup → Inno Setup Compiler
   - Or run: `ISCC.exe`

2. Open the script:
   - File → Open
   - Select: `setup.iss`
   - Click "Open"

3. Compile:
   - Build → Compile
   - Or press: Ctrl+F9
   - Or click "Compile" button

4. Wait for completion:
   - Shows "Compile complete" when done
   - Check for errors
   - Get `PDF_Merger_App_Setup.exe`

### Method 3: Command Line

```batch
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss
```

Replace version number if using different version.

---

## 🎨 What Inno Setup Does

The `setup.iss` script is configured to:

### Installation Features
- ✅ Create `{autopf}\PDF Merger App` folder
- ✅ Copy all application files
- ✅ Create `input/` and `output/` directories
- ✅ Create Start Menu shortcuts
- ✅ Create desktop shortcut (optional)
- ✅ Run `install.bat` to set up Python environment
- ✅ Add to "Add/Remove Programs" in Control Panel

### User Options
- ✅ Full installation (all components)
- ✅ Compact installation (essentials only)
- ✅ Custom installation (choose what to install)
- ✅ Optional Python virtual environment
- ✅ Optional desktop shortcut
- ✅ Optional file associations

### Uninstallation
- ✅ Remove all files safely
- ✅ Preserve user PDFs in input/output folders
- ✅ Clean registry entries
- ✅ Appear in Control Panel → Add/Remove Programs

---

## 📊 Installer Output

After building, you get:

```
PDF_Merger_App_Setup.exe (~1-2 MB)
├── Contains all app files
├── Contains Python setup instructions
├── Professional Windows installer UI
├── Uninstall support
└── Add/Remove Programs support
```

**File Size: 1-2 MB** (small and fast to download)

---

## 🔧 Customizing the Installer

Edit `setup.iss` to customize:

### Change Application Name
```ini
[Setup]
AppName=My PDF Tool
AppVersion=1.0.0
```

### Change Installation Directory
```ini
DefaultDirName={autopf}\My PDF Tool
```

### Change Start Group Name
```ini
DefaultGroupName=My PDF Tool
```

### Change Output Filename
```ini
OutputBaseFilename=MyPDFTool_Setup
```

### Add Company Information
```ini
AppPublisher=Your Company
AppPublisherURL=https://yourwebsite.com
```

### Add Icon
```ini
SetupIconFile=myicon.ico
UninstallDisplayIcon={app}\myicon.ico
```

---

## 📋 Troubleshooting

### Issue: "ISCC.exe not found"
**Solution:**
- Install Inno Setup from https://jrsoftware.org/isdl.php
- Verify it's in: `C:\Program Files (x86)\Inno Setup 6\`

### Issue: "setup.iss not found"
**Solution:**
- Make sure `setup.iss` is in current directory
- Run command from app folder

### Issue: Build fails with file errors
**Solution:**
- Ensure all referenced files exist in folder:
  - gui.py, app.py, pdf_merger.py, etc.
  - requirements.txt, README.md, LICENSE.txt
- Check file names match exactly (case-sensitive)

### Issue: Installer runs but app won't start
**Solution:**
- User needs Python installed
- Run `install.bat` in app directory
- Check that dependencies installed correctly

### Issue: "Windows protected your PC" on install
**Solution:**
- Normal for unsigned installers
- Click "More info" → "Run anyway"
- Consider code signing for production use

---

## 🆚 Inno Setup vs NSIS vs setup_wizard

| Feature | Inno Setup | NSIS | setup_wizard |
|---------|-----------|------|--------------|
| **Ease** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Professional** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **File Size** | 1-2 MB | 1-2 MB | 20 KB |
| **Learning Curve** | Easy | Medium | N/A |
| **Customizable** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Limited |
| **Community** | Large | Large | N/A |
| **GUI Compiler** | ✅ Yes | ✅ Yes | N/A |

---

## 📦 Distribution

After building `PDF_Merger_App_Setup.exe`:

1. **Test it:**
   - Run on your computer
   - Go through installation
   - Verify app works

2. **Share it:**
   - Email the .exe file
   - Upload to cloud storage
   - Host on website

3. **Users just:**
   - Download the file
   - Double-click to install
   - App is ready to use!

---

## 🎯 Best Practices

1. **Test thoroughly:**
   - Install on clean machine
   - Test uninstall process
   - Verify shortcuts work
   - Check Python dependencies

2. **Include documentation:**
   - README.md inside app
   - QUICKSTART.md for first-time users
   - SETUP_GUIDE.md for troubleshooting

3. **Version your installer:**
   - Update AppVersion in setup.iss
   - Use version in filename: `PDF_Merger_v1.0.exe`
   - Document changes

4. **Distribute responsibly:**
   - Scan for viruses before sharing
   - Use HTTPS for web distribution
   - Include support contact info

---

## 📚 Resources

- **Inno Setup Official:** https://jrsoftware.org/
- **Documentation:** https://jrsoftware.org/isinfo.php
- **Script Examples:** Included in Inno Setup
- **Community Forums:** https://forums.jrsoftware.org/

---

## 🚀 Next Steps

1. **Download Inno Setup:**
   ```
   https://jrsoftware.org/isdl.php
   ```

2. **Run build command:**
   ```batch
   build_inno_installer.bat
   ```

3. **Test the installer:**
   ```batch
   PDF_Merger_App_Setup.exe
   ```

4. **Share with others:**
   - Email, upload, or share link

---

## 💡 Pro Tips

- **Faster building:** Use `build_inno_installer.bat`
- **Silent install:** Users can run: `PDF_Merger_App_Setup.exe /SILENT`
- **Custom location:** Users can choose install directory
- **Uninstall clean:** All files removed, user PDFs preserved
- **Update easy:** Just distribute new .exe with new version

---

## ✅ You're All Set!

You have:
- ✅ setup.iss (ready to compile)
- ✅ build_inno_installer.bat (easy build script)
- ✅ Complete documentation
- ✅ Customization guide

**Next: Install Inno Setup and build your installer! 🎉**

```
1. Download Inno Setup from https://jrsoftware.org/isdl.php
2. Run: build_inno_installer.bat
3. Share PDF_Merger_App_Setup.exe with others
```

Done!
