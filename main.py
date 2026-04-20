"""
Legacy entry point - Use app.py instead for interactive menu
This file is kept for quick automated merging with existing files.
"""
from pathlib import Path
from pdf_merger import PDFMerger

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    merger = PDFMerger(base_dir / "input", base_dir / "output")
    merger.merge_pdfs("letterhead.pdf", "content.pdf")