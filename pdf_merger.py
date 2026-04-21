"""
PDF Merger Module - Core functionality for merging PDFs
"""
from pathlib import Path
from pypdf import PdfReader, PdfWriter


class PDFMerger:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def list_input_files(self):
        """List all PDF files in input directory."""
        pdfs = list(self.input_dir.glob("*.pdf"))
        return pdfs

    def merge_pdfs(self, letterhead_file: str, content_file: str, output_file: str = "print_ready_merged.pdf"):
        """
        Merge content PDF on top of letterhead PDF.
        
        Args:
            letterhead_file: Name of letterhead PDF in input directory
            content_file: Name of content PDF in input directory
            output_file: Name of output PDF file
        
        Returns:
            bool: True if successful, False otherwise
        """
        letterhead_path = self.input_dir / letterhead_file
        content_path = self.input_dir / content_file
        output_path = self.output_dir / output_file

        if not letterhead_path.exists():
            print(f"❌ Error: Letterhead file '{letterhead_file}' not found in {self.input_dir}")
            print(f"   Expected at: {letterhead_path}")
            return False
        
        if not content_path.exists():
            print(f"❌ Error: Content file '{content_file}' not found in {self.input_dir}")
            print(f"   Expected at: {content_path}")
            return False

        try:
            print(f"📖 Reading documents...")
            content_reader = PdfReader(str(content_path))
            writer = PdfWriter()

            print(f"🔄 Merging pages (content ON TOP, letterhead UNDERNEATH)...")
            for i, page in enumerate(content_reader.pages, 1):
                # Create a fresh copy of letterhead for each page
                lh_reader = PdfReader(str(letterhead_path))
                lh_copy = lh_reader.pages[0]
                lh_copy.merge_page(page)  # Overlay content on top of letterhead
                writer.add_page(lh_copy)
                print(f"   ✅ Page {i} merged")

            print(f"💾 Saving print-ready PDF...")
            with open(output_path, "wb") as f:
                writer.write(f)
            print(f"🖨️ Ready to print: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error during merge: {str(e)}")
            return False

    def list_output_files(self):
        """List all PDF files in output directory."""
        pdfs = list(self.output_dir.glob("*.pdf"))
        return pdfs
