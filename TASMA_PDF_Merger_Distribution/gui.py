"""
PDF Merger GUI Application - Tkinter-based user interface with preview and drag-drop
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from pdf_merger import PDFMerger
import threading
import shutil
import os
import subprocess
import sys
from PIL import Image, ImageTk
import fitz  # PyMuPDF for PDF rendering
from io import BytesIO


class PDFPreviewWindow:
    """Interactive PDF preview with drag-and-drop image placement."""
    
    def __init__(self, parent, pdf_path, merger, input_dir, output_dir):
        self.pdf_path = Path(pdf_path)
        self.merger = merger
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        # State variables
        self.current_page = 0
        self.dragged_image = None
        self.image_position = None
        self.image_data = None  # Store PIL image
        self.image_size = None  # Store current displayed size (width, height)
        self.original_image_size = None  # Store original image size
        self.pdf_doc = None
        self.page_images = {}  # Cache for rendered pages
        self.photo_images = []  # Keep references to all PhotoImages (prevent garbage collection)
        self.resizing = False  # Track if resizing
        self.resize_handle = None  # Which handle is being dragged
        self.resize_handle_size = 10  # Size of resize handles in pixels
        self.drag_start = None  # Starting position of drag
        
        # Create preview window
        self.window = tk.Toplevel(parent)
        self.window.title("PDF Preview - Drag & Drop Image")
        self.window.geometry("1000x800")
        self.window.attributes('-topmost', True)  # Keep preview window on top
        
        # Setup UI
        self._setup_ui()
        self._load_pdf()
        self._display_page()
        
    def _setup_ui(self):
        """Setup the preview UI."""
        # Top frame with controls
        control_frame = ttk.Frame(self.window)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        ttk.Label(control_frame, text="Page:").pack(side=tk.LEFT)
        self.page_var = tk.StringVar(value="1")
        self.page_spinbox = ttk.Spinbox(
            control_frame, from_=1, to=1, width=5, 
            textvariable=self.page_var, command=self._on_page_change
        )
        self.page_spinbox.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="/ 1").pack(side=tk.LEFT)
        
        # Image selection
        ttk.Button(control_frame, text="Select Image", 
                  command=self._select_image).pack(side=tk.LEFT, padx=20)
        
        self.image_label = ttk.Label(control_frame, text="No image selected", foreground="gray")
        self.image_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(control_frame, text="Clear Image", 
                  command=self._clear_image).pack(side=tk.LEFT, padx=5)
        
        # Save button - prominent
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Create a frame for save options
        save_frame = ttk.Frame(control_frame)
        save_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(save_frame, text="💾 Save PDF", 
                  command=self._save_with_image).pack(side=tk.LEFT, padx=5)
        
        # Help text for resizing
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        ttk.Label(control_frame, text="💡 Drag corners to resize | Drag center to move", foreground="blue").pack(side=tk.LEFT, padx=5)
        
        # Main preview area with scrollbars
        canvas_frame = ttk.Frame(self.window)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas for PDF preview with scrollbar
        self.canvas = tk.Canvas(canvas_frame, bg="gray50", cursor="arrow")
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.canvas.config(yscrollcommand=v_scrollbar.set)
        
        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.canvas.config(xscrollcommand=h_scrollbar.set)
        
        # Configure grid weights
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Bind events
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind("<Button-4>", self._on_mouse_wheel)  # Linux scroll up
        self.canvas.bind("<Button-5>", self._on_mouse_wheel)  # Linux scroll down
        
        # Status bar
        status_frame = ttk.Frame(self.window)
        status_frame.pack(side=tk.TOP, fill=tk.X, padx=10)
        
        self.status_label = ttk.Label(status_frame, text="Ready", foreground="blue")
        self.status_label.pack(side=tk.LEFT)
        
        # Bottom close button
        button_frame = ttk.Frame(self.window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="✕ Close", 
                  command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
        
    def _load_pdf(self):
        """Load PDF document."""
        try:
            self.pdf_doc = fitz.open(str(self.pdf_path))
            total_pages = len(self.pdf_doc)
            self.page_spinbox.config(to=total_pages)
            self.page_spinbox.pack_configure()
            self.status_label.config(text=f"Loaded PDF: {self.pdf_path.name} ({total_pages} pages)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF: {str(e)}", parent=self.window)
            self.window.destroy()
    
    def _display_page(self):
        """Display current PDF page."""
        if not self.pdf_doc:
            return
        
        try:
            # Render page if not cached
            if self.current_page not in self.page_images:
                page = self.pdf_doc[self.current_page]
                # Render at higher zoom for better quality
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_data = pix.tobytes("ppm")
                img = Image.open(BytesIO(img_data))
                self.page_images[self.current_page] = img
            
            img = self.page_images[self.current_page]
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Update canvas
            self.canvas.delete("all")
            self.canvas_img_id = self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.image = photo  # Keep a reference
            
            # Store image dimensions for later
            self.canvas_width = img.width
            self.canvas_height = img.height
            self.canvas.config(width=img.width, height=img.height, scrollregion=(0, 0, img.width, img.height))
            
            # Redraw image if placed
            if self.image_data and self.image_position:
                self._draw_placed_image()
                
        except Exception as e:
            self.status_label.config(text=f"Error rendering page: {str(e)}", foreground="red")
    
    def _on_page_change(self):
        """Handle page change."""
        try:
            page_num = int(self.page_var.get()) - 1
            if 0 <= page_num < len(self.pdf_doc):
                self.current_page = page_num
                self._display_page()
        except ValueError:
            pass
    
    def _select_image(self):
        """Select image to place on PDF."""
        file = filedialog.askopenfilename(
            parent=self.window,
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), 
                      ("PNG", "*.png"), ("JPEG", "*.jpg *.jpeg"), ("All files", "*.*")]
        )
        if file:
            try:
                # Open original image and store original size
                original_img = Image.open(file)
                self.original_image_size = original_img.size
                
                # Create a copy for display with max size
                self.image_data = original_img.copy()
                max_size = (300, 200)
                self.image_data.thumbnail(max_size, Image.Resampling.LANCZOS)
                self.image_size = self.image_data.size
                
                self.image_label.config(text=f"Selected: {Path(file).name}", foreground="green")
                self.status_label.config(text="Drag image corners to resize. Drag center to move.", foreground="blue")
                self.image_path = file
                
                # Set initial position
                self.image_position = (50, 50)
                self._draw_placed_image()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}", parent=self.window)
    
    def _clear_image(self):
        """Clear selected image."""
        self.image_data = None
        self.image_position = None
        self.image_size = None
        self.original_image_size = None
        self.image_label.config(text="No image selected", foreground="gray")
        self._display_page()
    
    def _redraw_placed_image_only(self):
        """Redraw only the placed image without clearing the PDF page (for fast updates during dragging)."""
        if not self.image_data or not self.image_position or not self.image_size:
            return
        
        # Delete previous placed image and handles (by tag, not clearing entire canvas)
        self.canvas.delete("placed_image", "placed_handle", "placed_position")
        
        # Resize image to current size (convert to int to avoid PIL errors)
        display_img = self.image_data.copy()
        size = (int(self.image_size[0]), int(self.image_size[1]))
        display_img = display_img.resize(size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(display_img)
        self.photo_images.append(photo)  # Keep reference to prevent garbage collection
        x, y = self.image_position
        w, h = self.image_size
        
        # Draw on canvas with tagged items
        self.image_id = self.canvas.create_image(x, y, image=photo, anchor=tk.NW, tags="placed_image")
        
        # Draw resize handles at corners and edges
        handle_size = self.resize_handle_size
        handles = {
            'nw': (x, y),  # top-left
            'ne': (x + w, y),  # top-right
            'sw': (x, y + h),  # bottom-left
            'se': (x + w, y + h),  # bottom-right
            'n': (x + w//2, y),  # top-middle
            's': (x + w//2, y + h),  # bottom-middle
            'w': (x, y + h//2),  # left-middle
            'e': (x + w, y + h//2),  # right-middle
        }
        
        # Draw handle rectangles
        for handle_name, (hx, hy) in handles.items():
            self.canvas.create_rectangle(
                hx - handle_size//2, hy - handle_size//2,
                hx + handle_size//2, hy + handle_size//2,
                fill="red", outline="white", width=2, tags="placed_handle"
            )
        
        # Draw position and size indicator
        self.canvas.create_text(x, y - 20, text=f"({int(x)}, {int(y)}) {int(w)}x{int(h)}", fill="yellow", tags="placed_position")
    
    def _draw_placed_image(self):
        """Draw image on the preview canvas with resize handles."""
        if not self.image_data or not self.image_position or not self.image_size:
            return
        
        # Delete any previous placed image/handles first
        self.canvas.delete("placed_image", "placed_handle", "placed_position")
        
        # Clear old photo references to prevent memory bloat
        self.photo_images.clear()
        
        # Resize image to current size (convert to int to avoid PIL errors)
        display_img = self.image_data.copy()
        size = (int(self.image_size[0]), int(self.image_size[1]))
        display_img = display_img.resize(size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(display_img)
        self.photo_images.append(photo)  # Keep reference to prevent garbage collection
        x, y = self.image_position
        w, h = self.image_size
        
        # Draw on canvas
        self.image_id = self.canvas.create_image(x, y, image=photo, anchor=tk.NW, tags="placed_image")
        
        # Draw resize handles at corners and edges
        handle_size = self.resize_handle_size
        handles = {
            'nw': (x, y),  # top-left
            'ne': (x + w, y),  # top-right
            'sw': (x, y + h),  # bottom-left
            'se': (x + w, y + h),  # bottom-right
            'n': (x + w//2, y),  # top-middle
            's': (x + w//2, y + h),  # bottom-middle
            'w': (x, y + h//2),  # left-middle
            'e': (x + w, y + h//2),  # right-middle
        }
        
        # Draw handle rectangles
        for handle_name, (hx, hy) in handles.items():
            self.canvas.create_rectangle(
                hx - handle_size//2, hy - handle_size//2,
                hx + handle_size//2, hy + handle_size//2,
                fill="red", outline="white", width=2, tags="placed_handle"
            )
        
        # Draw position and size indicator
        self.canvas.create_text(x, y - 20, text=f"({int(x)}, {int(y)}) {int(w)}x{int(h)}", fill="yellow", tags="placed_position")
    
    def _on_canvas_click(self, event):
        """Handle canvas click to start dragging or resizing."""
        if not self.image_data or not self.image_position:
            return
        
        # Convert event coordinates to canvas coordinates (accounting for scroll)
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        x, y = self.image_position
        w, h = self.image_size
        handle_size = self.resize_handle_size
        
        # Check if clicking on a resize handle
        handles = {
            'nw': (x, y),
            'ne': (x + w, y),
            'sw': (x, y + h),
            'se': (x + w, y + h),
            'n': (x + w//2, y),
            's': (x + w//2, y + h),
            'w': (x, y + h//2),
            'e': (x + w, y + h//2),
        }
        
        for handle_name, (hx, hy) in handles.items():
            if abs(canvas_x - hx) <= handle_size//2 and abs(canvas_y - hy) <= handle_size//2:
                self.resizing = True
                self.resize_handle = handle_name
                self.drag_start = (canvas_x, canvas_y)
                self.original_size = (w, h)
                self.original_pos = (x, y)
                return
        
        # Check if clicking on the image center for moving
        if x <= canvas_x <= x + w and y <= canvas_y <= y + h:
            self.dragged_image = (canvas_x, canvas_y)
    
    def _on_canvas_drag(self, event):
        """Handle dragging image or resizing."""
        if not self.image_data:
            return
        
        # Convert event coordinates to canvas coordinates (accounting for scroll)
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Handle resizing
        if self.resizing and self.resize_handle:
            x, y = self.image_position
            w, h = self.image_size
            orig_w, orig_h = self.original_size
            orig_x, orig_y = self.original_pos
            
            dx = canvas_x - self.drag_start[0]
            dy = canvas_y - self.drag_start[1]
            
            # Calculate new size based on handle
            handle = self.resize_handle
            
            if handle in ['nw', 'n', 'ne']:  # Top handles
                new_h = max(50, orig_h - dy)
                y_offset = orig_y + (orig_h - new_h)
            elif handle in ['sw', 's', 'se']:  # Bottom handles
                new_h = max(50, orig_h + dy)
                y_offset = orig_y
            else:
                new_h = orig_h
                y_offset = orig_y
            
            if handle in ['nw', 'w', 'sw']:  # Left handles
                new_w = max(50, orig_w - dx)
                x_offset = orig_x + (orig_w - new_w)
            elif handle in ['ne', 'e', 'se']:  # Right handles
                new_w = max(50, orig_w + dx)
                x_offset = orig_x
            else:
                new_w = orig_w
                x_offset = orig_x
            
            # Update size and position
            self.image_size = (new_w, new_h)
            self.image_position = (x_offset, y_offset)
            
            # Redraw (fast update, don't clear PDF page)
            self._redraw_placed_image_only()
            
            self.status_label.config(text=f"Size: {new_w}x{new_h} | Position: ({x_offset}, {y_offset})", foreground="blue")
        
        # Handle moving
        elif self.dragged_image:
            dx = canvas_x - self.dragged_image[0]
            dy = canvas_y - self.dragged_image[1]
            
            old_x, old_y = self.image_position
            w, h = self.image_size
            new_x = max(0, min(old_x + dx, self.canvas_width - w))
            new_y = max(0, min(old_y + dy, self.canvas_height - h))
            
            self.image_position = (new_x, new_y)
            self.dragged_image = (canvas_x, canvas_y)
            
            # Redraw (fast update, don't clear PDF page)
            self._redraw_placed_image_only()
            
            self.status_label.config(text=f"Position: ({new_x}, {new_y})", foreground="blue")
    
    def _on_canvas_release(self, event):
        """Handle release after dragging or resizing."""
        self.dragged_image = None
        self.resizing = False
        self.resize_handle = None
    
    def _on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.num == 5 or event.delta < 0:
            # Scroll down
            self.canvas.yview_scroll(3, "units")
        elif event.num == 4 or event.delta > 0:
            # Scroll up
            self.canvas.yview_scroll(-3, "units")
    
    def _show_save_options(self):
        """Show save options dialog."""
        if not self.image_data or not self.image_position:
            # No image selected, just save without image
            self._save_without_image()
            return
        
        # Create save options dialog
        dialog = tk.Toplevel(self.window)
        dialog.title("Save PDF")
        dialog.geometry("300x150")
        dialog.transient(self.window)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Save PDF as:", font=("Arial", 10, "bold")).pack(pady=15)
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="With Image", 
                  command=lambda: [self._save_with_image(), dialog.destroy()],
                  width=20).pack(pady=5)
        
        ttk.Button(button_frame, text="Without Image", 
                  command=lambda: [self._save_without_image(), dialog.destroy()],
                  width=20).pack(pady=5)
        
        ttk.Button(button_frame, text="Cancel", 
                  command=dialog.destroy,
                  width=20).pack(pady=5)
    
    def _save_with_image(self):
        """Save PDF with placed image."""
        if not self.image_data or not self.image_position:
            # No image selected - ask user what to do
            result = messagebox.askyesno("No Image", "No image placed on PDF.\n\nSave PDF without image?", parent=self.window)
            if result:
                self._save_without_image()
            return
        
        try:
            # Ask user where to save the file
            default_name = self.pdf_path.stem + "_with_image.pdf"
            output_path = filedialog.asksaveasfilename(
                parent=self.window,
                title="Save PDF with Image",
                defaultextension=".pdf",
                initialfile=default_name,
                initialdir=str(self.output_dir),
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            
            if not output_path:
                # User cancelled the save dialog
                return
            
            self.status_label.config(text="Saving PDF with image...", foreground="blue")
            self.window.update()
            
            # Convert pixel coordinates to PDF points
            # The canvas is rendered at 2x zoom, so divide by 2 to get original scale
            zoom_factor = 2  # Canvas is rendered at 2x zoom
            x_pdf = int(self.image_position[0] / zoom_factor)
            y_pdf = int(self.image_position[1] / zoom_factor)
            width_pdf = int(self.image_size[0] / zoom_factor)
            height_pdf = int(self.image_size[1] / zoom_factor)
            
            # Use merger to add image with scaled coordinates
            success = self.merger.add_image_to_pdf(
                str(self.pdf_path), 
                self.image_path, 
                output_path,  # Pass full path
                x_pdf, y_pdf,
                width_pdf,
                height_pdf
            )
            
            if success:
                messagebox.showinfo("✅ Success", f"PDF saved with image:\n{output_path}", parent=self.window)
                self.status_label.config(text="Saved successfully!", foreground="green")
            else:
                messagebox.showerror("Error", "Failed to save PDF", parent=self.window)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}", parent=self.window)
    
    def _save_without_image(self):
        """Save PDF without image."""
        try:
            # Ask user where to save the file
            default_name = self.pdf_path.name
            output_path = filedialog.asksaveasfilename(
                parent=self.window,
                title="Save PDF",
                defaultextension=".pdf",
                initialfile=default_name,
                initialdir=str(self.output_dir),
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            
            if not output_path:
                # User cancelled the save dialog
                return
            
            self.status_label.config(text="Saving PDF...", foreground="blue")
            self.window.update()
            
            # Copy the merged PDF to the chosen location
            shutil.copy2(self.pdf_path, output_path)
            messagebox.showinfo("✅ Success", f"PDF saved:\n{output_path}", parent=self.window)
            self.status_label.config(text="Saved successfully!", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}", parent=self.window)


class PDFMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TASMA PDF Merger App")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        
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
        title = ttk.Label(main_frame, text="📄 TASMA PDF MERGER", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Subtitle
        subtitle = ttk.Label(main_frame, text="PRODUCED BY TASMA IT DEPARTMENT", font=("Arial", 10))
        subtitle.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        # Letterhead Section
        letterhead_frame = ttk.LabelFrame(main_frame, text="Letterhead PDF", padding="10")
        letterhead_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(letterhead_frame, text="Selected:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(letterhead_frame, textvariable=self.letterhead_file, 
                 foreground="blue").grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Button(letterhead_frame, text="Browse", 
                  command=self.select_letterhead).grid(row=0, column=2)
        ttk.Button(letterhead_frame, text="From Input Folder", 
                  command=self.select_letterhead_from_folder).grid(row=0, column=3, padx=5)
        
        # Content Section
        content_frame = ttk.LabelFrame(main_frame, text="Content PDF", padding="10")
        content_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(content_frame, text="Selected:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(content_frame, textvariable=self.content_file, 
                 foreground="blue").grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Button(content_frame, text="Browse", 
                  command=self.select_content).grid(row=0, column=2)
        ttk.Button(content_frame, text="From Input Folder", 
                  command=self.select_content_from_folder).grid(row=0, column=3, padx=5)
        
        # Output Filename Section
        output_frame = ttk.LabelFrame(main_frame, text="Output Filename", padding="10")
        output_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(output_frame, text="Filename:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(output_frame, textvariable=self.output_filename, 
                 width=40).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(output_frame, text="Reset", 
                  command=lambda: self.output_filename.set("print_ready_merged.pdf")
                  ).grid(row=0, column=2)
        
        output_frame.columnconfigure(1, weight=1)
        
        # Status/Log Section
        log_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = tk.Text(log_frame, height=8, width=60, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Button Section
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(button_frame, text="🔀 Merge PDFs", command=self.merge_pdfs,
                  width=20).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="�📂 Open Input Folder", 
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
            self._copy_file_to_input(file)
            self.letterhead_file.set(Path(file).name)
            
    def select_content(self):
        """Browse for content file."""
        file = filedialog.askopenfilename(
            title="Select Content PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file:
            self._copy_file_to_input(file)
            self.content_file.set(Path(file).name)
    
    def _copy_file_to_input(self, file_path):
        """Copy selected file to input directory if it's not already there."""
        source = Path(file_path)
        dest = self.input_dir / source.name
        
        # Only copy if source is not already in input directory
        if source.resolve() != dest.resolve():
            try:
                shutil.copy2(source, dest)
                self.log(f"📋 Copied file to input directory: {source.name}")
            except Exception as e:
                self.log(f"⚠️ Warning: Could not copy file - {str(e)}")
                messagebox.showwarning("Copy Failed", f"Could not copy file:\n{str(e)}")
            
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
            self.log("Opening preview window...")
            
            # Schedule preview window on main thread
            self.root.after(0, lambda: self._show_preview(output_path))
        else:
            self.log("❌ Merge failed. Check the log above.")
            messagebox.showerror("Error", "PDF merge failed. See log for details.")
    
    def _show_preview(self, pdf_path):
        """Show preview window for the merged PDF."""
        try:
            preview = PDFPreviewWindow(self.root, pdf_path, self.merger, self.input_dir, self.output_dir)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open preview: {str(e)}")
    
    def open_input_folder(self):
        """Open input folder in file explorer."""
        if sys.platform == 'win32':
            os.startfile(self.input_dir)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', self.input_dir])
        else:
            subprocess.Popen(['xdg-open', self.input_dir])
            
    def open_output_folder(self):
        """Open output folder in file explorer."""
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
