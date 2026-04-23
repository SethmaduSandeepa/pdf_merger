"""
Create app icon - Blue circular icon with white J shape
"""
from PIL import Image, ImageDraw
import os

# Create a 256x256 icon with blue circular background and white J
size = 256
img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))

draw = ImageDraw.Draw(img, 'RGBA')

# Draw blue circular background - Cyan color (#00BCD4)
center_x, center_y = size // 2, size // 2
radius = size // 2 - 2
blue_color = (0, 188, 212, 255)
draw.ellipse([center_x - radius, center_y - radius, center_x + radius, center_y + radius], 
             fill=blue_color)

# Draw white J shape
white_color = (255, 255, 255, 255)

# J parameters
j_center_x = center_x - 10
j_top_y = 50
j_middle_y = 160
j_bottom_y = 180
j_width = 30  # Width of the stroke

# Vertical part of J (top and middle)
draw.rectangle([j_center_x - j_width//2, j_top_y, j_center_x + j_width//2, j_middle_y], 
               fill=white_color)

# Round the top
draw.ellipse([j_center_x - j_width//2 - 8, j_top_y - 15, j_center_x + j_width//2 + 8, j_top_y + 15],
             fill=white_color)

# Curved bottom of J - create a smooth curve
# Draw an arc-like curve using multiple circles
curve_start_x = j_center_x - j_width//2
curve_end_x = j_center_x - 60
curve_y = j_middle_y + 20

# Create points for a smooth curve from vertical to horizontal
for i in range(0, 91, 5):
    import math
    angle = math.radians(i)
    x = j_center_x - 40 - (40 * math.sin(angle))
    y = j_middle_y + 40 * (1 - math.cos(angle))
    draw.ellipse([x - j_width//2, y - j_width//2, x + j_width//2, y + j_width//2], 
                 fill=white_color)

# Horizontal part at bottom (right)
draw.rectangle([j_center_x - 50, j_middle_y + 35, j_center_x + 60, j_middle_y + 65], 
               fill=white_color)

# Round the right end
draw.ellipse([j_center_x + 50, j_middle_y + 35 - 15, j_center_x + 80, j_middle_y + 65 + 15],
             fill=white_color)

# Horizontal part at bottom (left) 
draw.rectangle([j_center_x - 80, j_middle_y + 35, j_center_x - 50, j_middle_y + 65],
               fill=white_color)

# Round the left end
draw.ellipse([j_center_x - 80 - 15, j_middle_y + 35 - 15, j_center_x - 50 + 15, j_middle_y + 65 + 15],
             fill=white_color)

# Save as ICO file
icon_path = "e:\\pdf_merger_app\\app.ico"
img.save(icon_path, format='ICO', sizes=[(256, 256)])
print(f"✅ Icon created: {icon_path}")
