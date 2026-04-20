"""
PDF Merger Application - Main Entry Point
A user-friendly app for merging PDFs with letterheads
"""
from pathlib import Path
from pdf_merger import PDFMerger
import os
import subprocess
import sys


class PDFMergerApp:
    def __init__(self):
        # Set up directories in AppData\Local
        self.app_data_dir = Path.home() / "AppData" / "Local" / "PDF Merger App"
        self.input_dir = self.app_data_dir / "input"
        self.output_dir = self.app_data_dir / "output"
        self.merger = PDFMerger(self.input_dir, self.output_dir)

    def clear_screen(self):
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Print app header."""
        print("\n" + "="*50)
        print("📄 PDF MERGER APP")
        print("="*50 + "\n")

    def show_menu(self):
        """Display main menu."""
        self.print_header()
        print("Main Menu:")
        print("1. Merge PDFs (Letterhead + Content)")
        print("2. View Input Files")
        print("3. View Output Files")
        print("4. Open Output Folder")
        print("5. Settings")
        print("6. Exit")
        print()

    def view_input_files(self):
        """Display available input files."""
        self.clear_screen()
        self.print_header()
        print("Input Files:\n")
        files = self.merger.list_input_files()
        if not files:
            print("❌ No PDF files found in input folder")
            print(f"📁 Folder: {self.input_dir}")
        else:
            for i, file in enumerate(files, 1):
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"{i}. {file.name} ({size_mb:.2f} MB)")
        input("\nPress Enter to continue...")

    def view_output_files(self):
        """Display available output files."""
        self.clear_screen()
        self.print_header()
        print("Output Files:\n")
        files = self.merger.list_output_files()
        if not files:
            print("❌ No merged PDFs found in output folder")
            print(f"📁 Folder: {self.output_dir}")
        else:
            for i, file in enumerate(files, 1):
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"{i}. {file.name} ({size_mb:.2f} MB)")
        input("\nPress Enter to continue...")

    def merge_pdfs(self):
        """Interactive merge process."""
        self.clear_screen()
        self.print_header()
        
        input_files = self.merger.list_input_files()
        if len(input_files) < 2:
            print("❌ You need at least 2 PDF files in the input folder:")
            print("   - One for the letterhead")
            print("   - One for the content")
            input("\nPress Enter to continue...")
            return

        print("Available PDF Files:")
        for i, file in enumerate(input_files, 1):
            print(f"{i}. {file.name}")
        print()

        try:
            letterhead_idx = int(input("Select letterhead PDF (enter number): ")) - 1
            content_idx = int(input("Select content PDF (enter number): ")) - 1

            if letterhead_idx < 0 or letterhead_idx >= len(input_files):
                print("❌ Invalid selection")
                input("\nPress Enter to continue...")
                return

            if content_idx < 0 or content_idx >= len(input_files):
                print("❌ Invalid selection")
                input("\nPress Enter to continue...")
                return

            letterhead_file = input_files[letterhead_idx].name
            content_file = input_files[content_idx].name

            if letterhead_file == content_file:
                print("❌ Please select different files for letterhead and content")
                input("\nPress Enter to continue...")
                return

            output_name = input("Enter output filename (default: print_ready_merged.pdf): ").strip()
            if not output_name:
                output_name = "print_ready_merged.pdf"

            print("\n" + "="*50)
            success = self.merger.merge_pdfs(letterhead_file, content_file, output_name)
            print("="*50)
            input("\nPress Enter to continue...")
        except ValueError:
            print("❌ Invalid input")
            input("\nPress Enter to continue...")

    def settings(self):
        """Settings menu."""
        self.clear_screen()
        self.print_header()
        print("Settings:\n")
        print(f"Input Folder:  {self.input_dir}")
        print(f"Output Folder: {self.output_dir}")
        print("\n1. Open input folder")
        print("2. Open output folder")
        print("3. Back to main menu")
        print()
        choice = input("Select option: ").strip()

        if choice == "1":
            self.open_folder(self.input_dir)
        elif choice == "2":
            self.open_folder(self.output_dir)

    def open_folder(self, folder_path):
        """Open folder in file explorer."""
        if sys.platform == 'win32':
            os.startfile(folder_path)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', folder_path])
        else:
            subprocess.Popen(['xdg-open', folder_path])

    def run(self):
        """Main app loop."""
        while True:
            self.clear_screen()
            self.show_menu()
            choice = input("Select option (1-6): ").strip()

            if choice == "1":
                self.merge_pdfs()
            elif choice == "2":
                self.view_input_files()
            elif choice == "3":
                self.view_output_files()
            elif choice == "4":
                self.open_folder(self.output_dir)
            elif choice == "5":
                self.settings()
            elif choice == "6":
                print("\n👋 Goodbye!")
                break
            else:
                print("\n❌ Invalid option. Please try again.")
                input("Press Enter to continue...")


if __name__ == "__main__":
    app = PDFMergerApp()
    app.run()
