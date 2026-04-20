"""
PDF Merger GUI Application - Tkinter-based user interface
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from pdf_merger import PDFMerger
import threading


class PDFMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger App")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Set up directories in AppData\Local
        self.app_data_dir = Path.home() / "AppData" / "Local" / "PDF Merger App"
        self.input_dir = self.app_data_dir / "input"
        self.output_dir = self.app_data_dir / "output"
        self.merger = PDFMerger(self.input_dir, self.output_dir)
        
        # Variables
        self.letterhead_file = tk.StringVar()
        self.content_file = tk.StringVar()
        self.output_filename = tk.StringVar(value="print_ready_merged.pdf")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="📄 PDF MERGER", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Letterhead Section
        letterhead_frame = ttk.LabelFrame(main_frame, text="Letterhead PDF", padding="10")
        letterhead_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(letterhead_frame, text="Selected:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(letterhead_frame, textvariable=self.letterhead_file, 
                 foreground="blue").grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Button(letterhead_frame, text="Browse", 
                  command=self.select_letterhead).grid(row=0, column=2)
        ttk.Button(letterhead_frame, text="From Input Folder", 
                  command=self.select_letterhead_from_folder).grid(row=0, column=3, padx=5)
        
        # Content Section
        content_frame = ttk.LabelFrame(main_frame, text="Content PDF", padding="10")
        content_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(content_frame, text="Selected:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(content_frame, textvariable=self.content_file, 
                 foreground="blue").grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Button(content_frame, text="Browse", 
                  command=self.select_content).grid(row=0, column=2)
        ttk.Button(content_frame, text="From Input Folder", 
                  command=self.select_content_from_folder).grid(row=0, column=3, padx=5)
        
        # Output Filename Section
        output_frame = ttk.LabelFrame(main_frame, text="Output Filename", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(output_frame, text="Filename:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(output_frame, textvariable=self.output_filename, 
                 width=40).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(output_frame, text="Reset", 
                  command=lambda: self.output_filename.set("print_ready_merged.pdf")
                  ).grid(row=0, column=2)
        
        output_frame.columnconfigure(1, weight=1)
        
        # Status/Log Section
        log_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = tk.Text(log_frame, height=8, width=60, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Button Section
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(button_frame, text="🔀 Merge PDFs", command=self.merge_pdfs,
                  width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📂 Open Input Folder", 
                  command=self.open_input_folder, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📂 Open Output Folder", 
                  command=self.open_output_folder, width=20).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        self.log("Ready to merge PDFs!")
        
    def log(self, message):
        """Add message to log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
        
    def select_letterhead(self):
        """Browse for letterhead file."""
        file = filedialog.askopenfilename(
            title="Select Letterhead PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file:
            self.letterhead_file.set(Path(file).name)
            
    def select_content(self):
        """Browse for content file."""
        file = filedialog.askopenfilename(
            title="Select Content PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file:
            self.content_file.set(Path(file).name)
            
    def select_letterhead_from_folder(self):
        """Select letterhead from input folder."""
        files = self.merger.list_input_files()
        if not files:
            messagebox.showwarning("No Files", f"No PDF files in {self.input_dir}")
            return
            
        self.show_file_selector("Select Letterhead", files, 
                               lambda f: self.letterhead_file.set(f.name))
        
    def select_content_from_folder(self):
        """Select content from input folder."""
        files = self.merger.list_input_files()
        if not files:
            messagebox.showwarning("No Files", f"No PDF files in {self.input_dir}")
            return
            
        self.show_file_selector("Select Content", files, 
                               lambda f: self.content_file.set(f.name))
        
    def show_file_selector(self, title, files, callback):
        """Show a dialog to select from available files."""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text=f"{title}:").pack(pady=10)
        
        # Listbox with scrollbar
        frame = ttk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        listbox = tk.Listbox(frame)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        
        for f in files:
            listbox.insert(tk.END, f.name)
            
        def select():
            selection = listbox.curselection()
            if selection:
                callback(files[selection[0]])
                dialog.destroy()
                
        ttk.Button(dialog, text="Select", command=select).pack(pady=10)
        
    def merge_pdfs(self):
        """Merge the selected PDFs."""
        if not self.letterhead_file.get():
            messagebox.showerror("Error", "Please select a letterhead PDF")
            return
            
        if not self.content_file.get():
            messagebox.showerror("Error", "Please select a content PDF")
            return
            
        if self.letterhead_file.get() == self.content_file.get():
            messagebox.showerror("Error", "Letterhead and content must be different files")
            return
            
        # Run merge in background thread to avoid freezing UI
        thread = threading.Thread(
            target=self._merge_thread,
            args=(self.letterhead_file.get(), self.content_file.get(), 
                  self.output_filename.get())
        )
        thread.daemon = True
        thread.start()
        
    def _merge_thread(self, letterhead, content, output):
        """Merge PDFs in background thread."""
        self.log(f"Starting merge...")
        self.log(f"Letterhead: {letterhead}")
        self.log(f"Content: {content}")
        self.log(f"Output: {output}")
        self.log("=" * 50)
        
        success = self.merger.merge_pdfs(letterhead, content, output)
        
        if success:
            output_path = self.output_dir / output
            self.log(f"✅ Success! Merged PDF: {output_path}")
            messagebox.showinfo("Success", f"PDF merged successfully!\n\n{output_path}")
        else:
            self.log("❌ Merge failed. Check the log above.")
            messagebox.showerror("Error", "PDF merge failed. See log for details.")
            
    def open_input_folder(self):
        """Open input folder in file explorer."""
        import subprocess
        import sys
        import os
        
        if sys.platform == 'win32':
            os.startfile(self.input_dir)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', self.input_dir])
        else:
            subprocess.Popen(['xdg-open', self.input_dir])
            
    def open_output_folder(self):
        """Open output folder in file explorer."""
        import subprocess
        import sys
        import os
        
        if sys.platform == 'win32':
            os.startfile(self.output_dir)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', self.output_dir])
        else:
            subprocess.Popen(['xdg-open', self.output_dir])


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerGUI(root)
    root.mainloop()
