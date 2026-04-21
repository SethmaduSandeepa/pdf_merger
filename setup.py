"""
Setup configuration for PDF Merger App
Allows installation via: pip install -e .
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="pdf-merger-app",
    version="1.0.1",
    author="PDF Merger",
    description="A user-friendly application for merging PDF letterheads with content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pypdf>=6.10.2",
        "reportlab>=4.4.10",
    ],
    entry_points={
        "console_scripts": [
            "pdf-merger=app:PDFMergerApp",
        ],
        "gui_scripts": [
            "pdf-merger-gui=gui:PDFMergerGUI",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
