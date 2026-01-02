#!/usr/bin/env python3
"""
Script to generate simple icons for the Calendar Generator application.
"""
from PIL import Image, ImageDraw
import os

def create_icon(filename, draw_func, size=64):
    """Create an icon with the given drawing function."""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Call the drawing function
    draw_func(draw, size)
    
    # Save the image
    img.save(filename, 'PNG')
    print(f"Created: {filename}")

def draw_basic_icon(draw, size):
    """Draw a gear/settings icon."""
    center = size // 2
    outer_r = size // 2 - 4
    inner_r = size // 4
    
    # Draw gear teeth
    import math
    teeth = 8
    for i in range(teeth):
        angle1 = (i * 2 * math.pi / teeth) - math.pi/16
        angle2 = (i * 2 * math.pi / teeth) + math.pi/16
        
        x1_out = center + outer_r * math.cos(angle1)
        y1_out = center + outer_r * math.sin(angle1)
        x2_out = center + outer_r * math.cos(angle2)
        y2_out = center + outer_r * math.sin(angle2)
        
        x1_in = center + (inner_r + 8) * math.cos(angle1)
        y1_in = center + (inner_r + 8) * math.sin(angle1)
        x2_in = center + (inner_r + 8) * math.cos(angle2)
        y2_in = center + (inner_r + 8) * math.sin(angle2)
        
        draw.polygon([(x1_out, y1_out), (x2_out, y2_out), (x2_in, y2_in), (x1_in, y1_in)], 
                     fill=(100, 200, 255, 255))
    
    # Draw center circle
    draw.ellipse([center - inner_r, center - inner_r, 
                  center + inner_r, center + inner_r], 
                 fill=(100, 200, 255, 255))

def draw_fonts_icon(draw, size):
    """Draw an 'A' for fonts."""
    # Draw letter A
    draw.polygon([(size//2, 8), (size-10, size-8), (size//2+4, size-8), (size//2-4, size-8), (10, size-8)],
                 fill=(100, 200, 255, 255))
    # Draw horizontal line in A
    draw.rectangle([size//4, size//2+4, size*3//4, size//2+8], fill=(40, 40, 60, 255))

def draw_colors_icon(draw, size):
    """Draw a palette icon."""
    # Draw palette shape
    draw.ellipse([8, 8, size-8, size-8], fill=(100, 200, 255, 255))
    
    # Draw color spots
    spots = [
        (size//3, size//3, 6),
        (size*2//3, size//3, 6),
        (size//3, size*2//3, 6),
        (size*2//3, size*2//3, 6),
    ]
    for x, y, r in spots:
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(40, 40, 60, 255))

def draw_features_icon(draw, size):
    """Draw a star icon."""
    import math
    center = size // 2
    outer_r = size // 2 - 8
    inner_r = size // 4
    
    points = []
    for i in range(5):
        # Outer point
        angle = (i * 2 * math.pi / 5) - math.pi/2
        x = center + outer_r * math.cos(angle)
        y = center + outer_r * math.sin(angle)
        points.append((x, y))
        
        # Inner point
        angle = (i * 2 * math.pi / 5) - math.pi/2 + math.pi/5
        x = center + inner_r * math.cos(angle)
        y = center + inner_r * math.sin(angle)
        points.append((x, y))
    
    draw.polygon(points, fill=(100, 200, 255, 255))

def draw_holidays_icon(draw, size):
    """Draw a calendar icon."""
    # Draw calendar outline
    draw.rectangle([8, 12, size-8, size-8], outline=(100, 200, 255, 255), width=3)
    
    # Draw header
    draw.rectangle([8, 12, size-8, 24], fill=(100, 200, 255, 255))
    
    # Draw grid
    for i in range(1, 4):
        y = 24 + i * (size - 32) // 3
        draw.line([(12, y), (size-12, y)], fill=(100, 200, 255, 255), width=2)
    
    for i in range(1, 3):
        x = 8 + i * (size - 16) // 3
        draw.line([(x, 28), (x, size-12)], fill=(100, 200, 255, 255), width=2)

def draw_birthdays_icon(draw, size):
    """Draw a gift box icon for birthdays."""
    margin = size // 5
    box_width = size - 2 * margin
    box_height = box_width * 0.6
    
    # Draw gift box
    box_top = margin + box_width * 0.2
    draw.rectangle(
        [margin, box_top, size - margin, box_top + box_height],
        fill=(255, 150, 200, 255), outline=(255, 255, 255, 255), width=2
    )
    
    # Draw ribbon vertical
    ribbon_width = box_width // 8
    center_x = size // 2
    draw.rectangle(
        [center_x - ribbon_width, box_top, center_x + ribbon_width, box_top + box_height],
        fill=(255, 100, 150, 255)
    )
    
    # Draw ribbon horizontal
    ribbon_y = box_top + box_height // 3
    ribbon_height = box_height // 5
    draw.rectangle(
        [margin, ribbon_y, size - margin, ribbon_y + ribbon_height],
        fill=(255, 100, 150, 255)
    )
    
    # Draw bow on top
    bow_size = box_width // 4
    bow_y = margin + box_width * 0.1
    draw.ellipse(
        [center_x - bow_size, bow_y, center_x, bow_y + bow_size],
        fill=(255, 200, 220, 255)
    )
    draw.ellipse(
        [center_x, bow_y, center_x + bow_size, bow_y + bow_size],
        fill=(255, 200, 220, 255)
    )
    draw.ellipse(
        [center_x - bow_size//3, bow_y + bow_size//4, center_x + bow_size//3, bow_y + bow_size//2],
        fill=(255, 150, 200, 255)
    )

def main():
    """Generate all icons."""
    # Create icons directory if it doesn't exist
    icons_dir = "icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    print("Generating icons...")
    
    create_icon(os.path.join(icons_dir, "basic.png"), draw_basic_icon, 64)
    create_icon(os.path.join(icons_dir, "fonts.png"), draw_fonts_icon, 64)
    create_icon(os.path.join(icons_dir, "colors.png"), draw_colors_icon, 64)
    create_icon(os.path.join(icons_dir, "features.png"), draw_features_icon, 64)
    create_icon(os.path.join(icons_dir, "holidays.png"), draw_holidays_icon, 64)
    create_icon(os.path.join(icons_dir, "birthdays.png"), draw_birthdays_icon, 64)
    
    print("\nAll icons created successfully in 'icons/' directory!")
    print("You can now use these icons in the calendar_gui.py application.")

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("Error: PIL (Pillow) is required to generate icons.")
        print("Install it with: pip install Pillow")
