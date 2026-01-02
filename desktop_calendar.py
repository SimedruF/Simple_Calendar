#!/usr/bin/env python3
"""
Desktop Calendar Widget - A transparent, draggable calendar for your desktop
"""
import dearpygui.dearpygui as dpg
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from PIL import Image
import tempfile
import os
from datetime import datetime
from pdf2image import convert_from_path

# Import the calendar generation functions from calendar_gui
import sys
sys.path.append(os.path.dirname(__file__))
from calendar_gui import draw_calendar, default_holidays, equinoxes_solstices, moon_phases, default_birthdays

def generate_desktop_calendar_image(year, num_months=6):
    """
    Generate a vertical calendar image for desktop display.
    Returns the path to the generated PNG file.
    """
    # Create temporary PDF
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
        tmp_pdf_path = tmp_pdf.name
    
    # Generate vertical layout calendar - one column
    page_width = 8 * cm  # Wider width for better visibility
    month_height = 5.5 * cm  # Height per month
    top_margin = 0.8 * cm  # Extra space at top for first month
    page_height = month_height * num_months + top_margin  # Total height
    
    c = canvas.Canvas(tmp_pdf_path, pagesize=(page_width, page_height))
    
    # Very light background that blends better
    month_font = ("Helvetica-Bold", 12)
    day_font = ("Helvetica", 10)
    bg_color = (0.98, 0.98, 0.98)  # Almost white background
    normal_text_color = (0, 0, 0)
    weekend_bg_color = (0.93, 0.93, 0.93)  # Light gray
    holiday_bg_color = (1, 0.85, 0.85)  # Light red
    week_num_text_color = (0.5, 0.5, 0.5)
    week_num_bg_color = (0.98, 0.98, 0.98)
    show_week_numbers = True
    highlight_holidays = True
    show_equinoxes = True
    equinox_circle_color = (0.8, 0.2, 0.2)  # Red for visibility
    show_moon_phases = True
    moon_phase_color = (0.2, 0.2, 0.5)
    moon_phase_size = 8
    show_birthdays = False
    birthdays_dict = default_birthdays
    birthday_square_color = (1, 0.75, 0.8)
    
    # Get current month to start from
    current_month = datetime.now().month
    
    # Draw months vertically in a single column
    for i in range(num_months):
        month = ((current_month - 1 + i) % 12) + 1
        
        # Position for this month (stacked vertically from top)
        x = 0.3 * cm
        y = page_height - top_margin - (i + 1) * month_height + 0.5 * cm
        
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
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_png:
        tmp_png_path = tmp_png.name
    
    if images:
        # Save directly without transparency processing (DearPyGUI doesn't support window transparency well on Linux)
        images[0].save(tmp_png_path, 'PNG')
    
    # Clean up PDF
    try:
        os.unlink(tmp_pdf_path)
    except:
        pass
    
    return tmp_png_path

def create_desktop_calendar():
    """Create the desktop calendar widget."""
    dpg.create_context()
    
    # Load Roboto font
    with dpg.font_registry():
        roboto_path = "/usr/share/fonts/truetype/Roboto-Regular.ttf"
        if os.path.exists(roboto_path):
            default_font = dpg.add_font(roboto_path, 16)
        else:
            default_font = None
    
    # Generate calendar image
    year = datetime.now().year
    calendar_image_path = generate_desktop_calendar_image(year, num_months=6)
    
    # Load the calendar image
    width, height, channels, data = dpg.load_image(calendar_image_path)
    
    # Create texture
    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="calendar_texture")
    
    # Calculate window size (minimal padding)
    window_width = width + 10
    window_height = height + 70
    
    # Create viewport with light background
    dpg.create_viewport(
        title="Desktop Calendar",
        width=window_width,
        height=window_height,
        resizable=True,
        decorated=True,  # Keep minimal title bar
        always_on_top=False,
        clear_color=(248, 248, 248, 255)  # Very light background to blend better
    )
    
    # Bind font if loaded
    if default_font:
        dpg.bind_font(default_font)
    
    # Create main window with minimal styling
    with dpg.window(
        label="",
        tag="calendar_window",
        width=window_width,
        height=window_height,
        no_close=False,
        no_collapse=True,
        no_scrollbar=True,
        no_title_bar=False
    ):
        # Minimal control panel at top
        with dpg.group(horizontal=True):
            dpg.add_checkbox(label="On Top", tag="always_on_top", default_value=False, callback=lambda s, a: dpg.configure_viewport(dpg.get_viewport(), always_on_top=a))
            dpg.add_spacer(width=5)
            dpg.add_button(label="↻", width=30, callback=lambda: refresh_calendar())
            dpg.add_spacer(width=5)
            dpg.add_button(label="✕", width=30, callback=lambda: dpg.stop_dearpygui())
        
        dpg.add_separator()
        
        # Calendar image
        dpg.add_image("calendar_texture", width=width, height=height, tag="calendar_image")
    
    def refresh_calendar():
        """Refresh the calendar image."""
        year = datetime.now().year
        new_image_path = generate_desktop_calendar_image(year, num_months=6)
        
        # Load new image
        new_width, new_height, new_channels, new_data = dpg.load_image(new_image_path)
        
        # Delete old texture completely
        try:
            if dpg.does_item_exist("calendar_texture"):
                dpg.delete_item("calendar_texture")
        except:
            pass
        
        # Create new texture with same tag
        with dpg.texture_registry():
            dpg.add_static_texture(new_width, new_height, new_data, tag="calendar_texture")
        
        # Update image
        dpg.configure_item("calendar_image", texture_tag="calendar_texture", width=new_width, height=new_height)
        
        # Clean up temp file
        try:
            os.unlink(new_image_path)
        except:
            pass
    
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("calendar_window", True)
    
    # Clean up temp file after display
    try:
        os.unlink(calendar_image_path)
    except:
        pass
    
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    create_desktop_calendar()
