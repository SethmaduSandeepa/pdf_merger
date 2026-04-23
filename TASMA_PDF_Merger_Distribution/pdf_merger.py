"""
PDF Merger Module - Core functionality for merging PDFs
"""
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image


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

    def add_image_to_pdf(self, pdf_path: str, image_path: str, output_file: str = None, x: int = 50, y: int = 50, width: int = 200, height: int = 100):
        """
        Add an image to a specific location on a PDF.
        
        Args:
            pdf_path: Path to the PDF file to add image to
            image_path: Path to the image file
            output_file: Full path or filename of output PDF. If just a filename, saves to output_dir. If None, overwrites input.
            x: X position in points from left (72 points = 1 inch)
            y: Y position in points from top (our canvas uses top-left origin)
            width: Width of image in points
            height: Height of image in points
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not Path(pdf_path).exists():
                print(f"❌ Error: PDF file not found: {pdf_path}")
                return False
            
            if not Path(image_path).exists():
                print(f"❌ Error: Image file not found: {image_path}")
                return False
            
            # Create output path
            if output_file:
                # Check if output_file is a full path or just a filename
                output_path = Path(output_file)
                if not output_path.is_absolute():
                    # It's just a filename, use output_dir
                    output_path = self.output_dir / output_file
            else:
                output_path = Path(pdf_path)
            
            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            print(f"🖼️ Adding image to PDF...")
            
            # Read the original PDF to get the actual page size
            original_reader = PdfReader(str(pdf_path))
            first_page = original_reader.pages[0]
            page_width = float(first_page.mediabox.width)
            page_height = float(first_page.mediabox.height)
            
            print(f"   Page size: {page_width} x {page_height} points")
            
            # Open the image to validate it
            img = Image.open(image_path)
            
            # Create a BytesIO object to hold the image overlay PDF
            overlay_buffer = BytesIO()
            
            # Create canvas with the ACTUAL page size from the PDF
            c = canvas.Canvas(overlay_buffer, pagesize=(page_width, page_height))
            
            # Convert y coordinate from top-left to bottom-left (PDF origin)
            # y_pdf = page_height - y - height
            y_pdf = page_height - y - height
            
            # Draw the image on the canvas
            # reportlab coordinates are from bottom-left
            c.drawImage(image_path, x, y_pdf, width=width, height=height)
            c.save()
            
            # Read the overlay PDF
            overlay_buffer.seek(0)
            overlay_reader = PdfReader(overlay_buffer)
            overlay_page = overlay_reader.pages[0]
            
            # Create writer and add image to first page
            writer = PdfWriter()
            first_page_copy = original_reader.pages[0]
            first_page_copy.merge_page(overlay_page)
            writer.add_page(first_page_copy)
            
            # Add remaining pages
            for page in original_reader.pages[1:]:
                writer.add_page(page)
            
            # Write output
            with open(output_path, "wb") as f:
                writer.write(f)
            
            print(f"✅ Image added successfully: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding image: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def add_image_to_all_pages(self, pdf_path: str, image_path: str, output_file: str = None, x: int = 50, y: int = 50, width: int = 200, height: int = 100):
        """
        Add an image to all pages of a PDF at the same location.
        
        Args:
            pdf_path: Path to the PDF file
            image_path: Path to the image file
            output_file: Name of output PDF (if None, overwrites input)
            x: X position in points
            y: Y position in points from bottom
            width: Width of image in points
            height: Height of image in points
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not Path(pdf_path).exists():
                print(f"❌ Error: PDF file not found: {pdf_path}")
                return False
            
            if not Path(image_path).exists():
                print(f"❌ Error: Image file not found: {image_path}")
                return False
            
            # Create output path
            if output_file:
                output_path = self.output_dir / output_file
            else:
                output_path = Path(pdf_path)
            
            print(f"🖼️ Adding image to all pages...")
            
            # Validate image
            img = Image.open(image_path)
            
            # Create a BytesIO object to hold the image overlay PDF
            overlay_buffer = BytesIO()
            
            # Create canvas
            c = canvas.Canvas(overlay_buffer, pagesize=letter)
            c.drawImage(image_path, x, y, width=width, height=height)
            c.save()
            
            # Read the overlay PDF
            overlay_buffer.seek(0)
            overlay_reader = PdfReader(overlay_buffer)
            overlay_page = overlay_reader.pages[0]
            
            # Read the original PDF
            original_reader = PdfReader(str(pdf_path))
            writer = PdfWriter()
            
            # Add image to all pages
            for i, page in enumerate(original_reader.pages, 1):
                page.merge_page(overlay_page)
                writer.add_page(page)
                print(f"   ✅ Image added to page {i}")
            
            # Write output
            with open(output_path, "wb") as f:
                writer.write(f)
            
            print(f"✅ Image added to all pages: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding image: {str(e)}")
            return False

    def list_output_files(self):
        """List all PDF files in output directory."""
        pdfs = list(self.output_dir.glob("*.pdf"))
        return pdfs
