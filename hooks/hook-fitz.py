"""
PyInstaller hook for PyMuPDF (fitz)
Ensures the fitz module and its dependencies are properly bundled
"""
from PyInstaller.utils.hooks import get_module_file_attribute
import os

# Get the location of the fitz module
fitz_module = get_module_file_attribute('fitz')

# Collect any binary/data files from the fitz package directory
binaries = []
datas = []

if fitz_module:
    fitz_dir = os.path.dirname(fitz_module)
    # Include the fitz directory itself if it's a package
    datas = [(fitz_dir, 'fitz')]

# Hidden imports that fitz depends on
hiddenimports = []
