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
    
    # Build the executable using the spec file
    base_dir = Path(__file__).parent
    spec_file = base_dir / "PDF Merger.spec"
    
    print(f"Creating executable from spec file: {spec_file}...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        str(spec_file)
    ]
    
    subprocess.run(cmd, check=True)
    
    exe_path = base_dir / "dist" / "PDF Merger.exe"
    if exe_path.exists():
        print(f"\n✅ Success! Executable created:")
        print(f"   {exe_path}")
        print(f"\nYou can now distribute this .exe file to other computers!")
        return True
    else:
        print("❌ Build failed")
        return False

if __name__ == "__main__":
    build_exe()
