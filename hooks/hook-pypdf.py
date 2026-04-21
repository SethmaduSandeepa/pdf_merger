"""
PyInstaller hook for pypdf
Ensures pypdf and all its submodules are properly included in the bundle
"""
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all pypdf submodules
hiddenimports = collect_submodules('pypdf')

# Collect data files if any
datas = collect_data_files('pypdf')
