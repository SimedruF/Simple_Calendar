#!/usr/bin/env python3
"""
Generate calendar image for Conky desktop widget
"""
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from PIL import Image
import tempfile
import os
from datetime import datetime
from pdf2image import convert_from_path

# Import calendar generation functions
import sys
sys.path.append(os.path.dirname(__file__))
from calendar_gui import draw_calendar, default_holidays, equinoxes_solstices, moon_phases, default_birthdays

def generate_conky_calendar(year, num_months=6, output_path="conky_calendar.png"):
    """
    Generate a vertical calendar image for Conky display.
    """
    # Create temporary PDF
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
        tmp_pdf_path = tmp_pdf.name
    
    # Generate vertical layout calendar - one column
    page_width = 7.5 * cm  # Width for Conky display
    month_height = 5.2 * cm  # Height per month
    top_margin = 1 * cm  # Extra space at top
    page_height = month_height * num_months + top_margin
    
    c = canvas.Canvas(tmp_pdf_path, pagesize=(page_width, page_height))
    
    # Styling for Conky calendar
    month_font = ("Helvetica-Bold", 11)
    day_font = ("Helvetica", 9)
    bg_color = (1, 1, 1)  # White background (will be transparent)
    normal_text_color = (0.1, 0.1, 0.1)  # Dark text
    weekend_bg_color = (0.92, 0.92, 0.92)  # Light gray
    holiday_bg_color = (1, 0.88, 0.88)  # Light red
    week_num_text_color = (0.5, 0.5, 0.5)
    week_num_bg_color = (0.96, 0.96, 0.96)
    show_week_numbers = True
    highlight_holidays = True
    show_equinoxes = True
    equinox_circle_color = (0.85, 0.25, 0.25)  # Red
    show_moon_phases = True
    moon_phase_color = (0.25, 0.25, 0.6)  # Blue
    moon_phase_size = 7
    show_birthdays = False
    birthdays_dict = default_birthdays
    birthday_square_color = (1, 0.75, 0.8)
    
    # Get current month to start from
    current_month = datetime.now().month
    
    # Draw months vertically
    for i in range(num_months):
        month = ((current_month - 1 + i) % 12) + 1
        
        # Position for this month
        x = 0.25 * cm
        y = page_height - top_margin - (i + 1) * month_height + 0.6 * cm
        
        # Draw the month
        draw_calendar(c, year, month, x, y, 0, 0, 
                     default_holidays, month_font, day_font, 
                     bg_color, normal_text_color, weekend_bg_color, 
                     holiday_bg_color, week_num_text_color, week_num_bg_color,
                     show_week_numbers, highlight_holidays, show_equinoxes, 
                     equinox_circle_color, show_moon_phases, moon_phase_color, 
                     moon_phase_size, show_birthdays, birthdays_dict, birthday_square_color)
    
    c.save()
    
    # Convert PDF to PNG
    images = convert_from_path(tmp_pdf_path, dpi=200)
    
    if images:
        # Convert to RGBA and make white background transparent
        img = images[0].convert('RGBA')
        width_img, height_img = img.size
        pixels = img.load()
        
        # Make white and near-white pixels transparent
        for y in range(height_img):
            for x in range(width_img):
                r, g, b, a = pixels[x, y]
                # Make white background transparent (adjust threshold as needed)
                if r > 248 and g > 248 and b > 248:
                    pixels[x, y] = (255, 255, 255, 0)  # Fully transparent
        
        # Save the image
        img.save(output_path, 'PNG')
        print(f"Calendar image generated: {output_path}")
    
    # Clean up temp PDF
    try:
        os.unlink(tmp_pdf_path)
    except:
        pass
    
    return output_path

if __name__ == "__main__":
    year = datetime.now().year
    generate_conky_calendar(year, num_months=6)
