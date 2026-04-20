"""
Build standalone executable using PyInstaller
Run this script to create a standalone .exe for distribution
"""
import subprocess
import sys
import os
from pathlib import Path

def build_exe():
    """Build standalone executable."""
    print("Building standalone executable...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyInstaller"])
    
    # Build the executable
    base_dir = Path(__file__).parent
    gui_file = base_dir / "gui.py"
    dist_dir = base_dir / "dist"
    build_dir = base_dir / "build"
    
    print(f"Creating executable from {gui_file}...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--icon=app_icon.ico" if (base_dir / "app_icon.ico").exists() else "",
        "--name=PDF Merger",
        "--distpath=dist",
        "--workpath=build",
        "--specpath=build",
        str(gui_file)
    ]
    
    # Remove empty strings
    cmd = [c for c in cmd if c]
    
    subprocess.run(cmd, check=True)
    
    exe_path = dist_dir / "PDF Merger.exe"
    if exe_path.exists():
        print(f"\n✅ Success! Executable created:")
        print(f"   {exe_path}")
        print(f"\nYou can now distribute this .exe file to other computers!")
    else:
        print("❌ Build failed")
        return False
    
    return True

if __name__ == "__main__":
    build_exe()
