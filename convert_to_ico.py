"""
Convert image to Windows ICO format for app icon
Usage: python convert_to_ico.py <image_file>
"""
from PIL import Image
import sys
from pathlib import Path

def convert_to_ico(image_path, output_path='app.ico'):
    """Convert image to ICO format"""
    try:
        # Open image
        img = Image.open(image_path)
        
        # ICO files typically use 256x256 as the standard size
        # Convert to RGBA if necessary
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Resize to standard icon size (256x256)
        # Use high-quality resampling
        img = img.resize((256, 256), Image.Resampling.LANCZOS)
        
        # Save as ICO
        img.save(output_path, format='ICO')
        
        print(f"✅ Success! Icon converted:")
        print(f"   Source: {image_path}")
        print(f"   Output: {output_path}")
        print(f"   Size: 256x256 pixels")
        print(f"\nYour app icon is ready! You can now:")
        print(f"  1. Rebuild the executable: python build_exe.py")
        print(f"  2. Build the installer: build_installer.bat")
        
        return True
    except FileNotFoundError:
        print(f"❌ Error: Image file not found: {image_path}")
        return False
    except Exception as e:
        print(f"❌ Error converting image: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python convert_to_ico.py <image_file>")
        print("\nExample:")
        print("  python convert_to_ico.py pdf_icon.png")
        sys.exit(1)
    
    image_file = sys.argv[1]
    if not Path(image_file).exists():
        print(f"❌ Image file not found: {image_file}")
        sys.exit(1)
    
    success = convert_to_ico(image_file)
    sys.exit(0 if success else 1)
