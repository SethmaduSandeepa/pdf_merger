# Professional Installation Guide - PDF Merger App

## For End Users: Installing the Standalone Application

### System Requirements
- **Windows 7 or later** (Windows 10/11 recommended)
- **No Python required** - Application is fully standalone

### Installation Steps

1. **Download the installer file**: `TASMA_PDF_Merger_Setup.exe`

2. **Run the installer**:
   - Double-click `TASMA_PDF_Merger_Setup.exe`
   - Click "Next" on the welcome screen
   - Review and accept the license agreement
   - Choose installation location (default: `C:\Program Files\TASMA PDF Merger`)
   - Select "Create Desktop Icon" (optional)
   - Click "Install"
   - Wait for installation to complete

3. **Launch the application**:
   - Double-click the desktop shortcut, OR
   - Go to Start Menu → TASMA PDF Merger → TASMA PDF Merger

4. **First Run**:
   - The app will create necessary folders in `%LocalAppData%\TASMA PDF Merger\`
   - Input folder: Place PDFs to merge here
   - Output folder: Merged PDFs will be saved here

### Uninstallation
- Go to Control Panel → Programs → Uninstall a program
- Select "TASMA PDF Merger"
- Click "Uninstall"
- Confirm removal

---

## For Administrators: Creating the Installer

### Prerequisites
1. **Python 3.8+** installed
2. **Inno Setup 6** installed ([Download](https://jrsoftware.org/isdl.php))
3. PDF Merger application files

### Build Steps

#### Step 1: Build Standalone Executable
```bash
cd path\to\pdf_merger_app
python build_exe.py
```
This creates `dist\PDF Merger.exe` (standalone, no Python required)

**Output**: `e:\pdf_merger_app\dist\PDF Merger.exe` (~150-200 MB)

#### Step 2: Create Professional Installer
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss
```

**Output**: `TASMA_PDF_Merger_Setup.exe` in project root

#### Step 3: Distribute
- Share `TASMA_PDF_Merger_Setup.exe` with users
- No additional setup required on user machines

---

## Application Features

### Main Window
- **Select Letterhead PDF**: Choose the template/background document
- **Select Content PDF**: Choose the document to overlay
- **Set Output Filename**: Specify output filename (default: auto-generated)
- **Merge & Preview**: Combines PDFs and opens preview window

### Preview Window
- **Preview Canvas**: Shows merged PDF with overlay image
- **Image Controls**:
  - **Drag**: Click and drag the image to reposition
  - **Resize**: Drag corner/edge handles to resize
  - **Red Handles**: Indicate positioning points
- **Save Options**:
  - "Save with Image": Saves merged PDF with positioned image overlay
  - "Save without Image": Saves just the merged PDFs (no overlay)
- **Auto-Close**: Preview window closes automatically after successful save

### Output
- Saved to: `%LocalAppData%\TASMA PDF Merger\output\`
- Format: PDF with preserved quality

---

## Troubleshooting

### Application Won't Launch
1. Ensure Windows 7 or later
2. Check if output folder exists: `%LocalAppData%\TASMA PDF Merger\output\`
3. Try running as Administrator

### Missing Dependencies
- All dependencies are included in the standalone executable
- No additional installations needed

### File Permissions
- Ensure write access to output folder
- Default location is user's local AppData (always writable)

### Large PDF Processing
- PDFs with 100+ pages may take longer to render
- Preview rendering happens at 2x zoom for quality
- This is normal behavior

---

## Technical Details

### Bundled Libraries
- **PyMuPDF (fitz)**: PDF manipulation and rendering
- **pypdf**: PDF merging and page handling
- **Pillow (PIL)**: Image processing
- **tkinter**: GUI framework

### File Locations
- **Application**: `C:\Program Files\TASMA PDF Merger\` (Windows 10/11) or `C:\Program Files (x86)\TASMA PDF Merger\` (Windows 7)
- **User Data**: `%LocalAppData%\TASMA PDF Merger\`
  - Input folder: `input/`
  - Output folder: `output/`

### Architecture
- **OS**: Windows (x64 native)
- **Runtime**: Embedded CPython 3.12
- **Package Size**: ~150-200 MB (includes all dependencies)
- **Memory Usage**: ~200-400 MB typical operation

---

## Support

For issues or feature requests, contact the development team.

**Last Updated**: April 2026
**Version**: 1.0.1
