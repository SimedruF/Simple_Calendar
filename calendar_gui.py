import dearpygui.dearpygui as dpg
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, black, gray
from calendar import month_name, Calendar
from datetime import date, datetime
import os

# Default holidays (Romanian legal holidays - non-working days)
default_holidays = {
    1: [1, 2, 6, 7, 24],  # 1-2 Jan: New Year's Day | 6 Jan: Epiphany | 7 Jan: John the Baptist | 24 Jan: Unification Day
    2: [],
    3: [],
    4: [10, 12, 13],  # Easter 2026: Good Friday (10 Apr), Easter Sunday (12 Apr), Easter Monday (13 Apr)
    5: [1, 31],  # 1 May: Labour Day | 31 May: Pentecost Sunday
    6: [1],  # 1 June: Children's Day + Pentecost Monday
    7: [],
    8: [15],  # 15 Aug: Assumption of Mary
    9: [],
    10: [],
    11: [30],  # 30 Nov: Saint Andrew's Day
    12: [1, 25, 26]  # 1 Dec: National Day | 25-26 Dec: Christmas
}

# Astronomical events (equinoxes and solstices)
equinoxes_solstices = {
    3: [20],  # Spring Equinox
    6: [21],  # Summer Solstice
    9: [23],  # Autumn Equinox
    12: [21]  # Winter Solstice
}

# Moon phases for 2026 (main phases)
moon_phases = {
    1: [(3, 'new'), (10, 'first'), (18, 'full'), (25, 'last')],  # New, First Q, Full, Last Q
    2: [(1, 'new'), (9, 'first'), (16, 'full'), (24, 'last')],
    3: [(3, 'new'), (11, 'first'), (18, 'full'), (25, 'last')],
    4: [(1, 'new'), (9, 'first'), (16, 'full'), (24, 'last')],
    5: [(1, 'new'), (9, 'first'), (16, 'full'), (23, 'last'), (30, 'new')],
    6: [(7, 'first'), (14, 'full'), (22, 'last'), (29, 'new')],
    7: [(7, 'first'), (14, 'full'), (21, 'last'), (28, 'new')],
    8: [(5, 'first'), (12, 'full'), (20, 'last'), (27, 'new')],
    9: [(4, 'first'), (11, 'full'), (18, 'last'), (25, 'new')],
    10: [(3, 'first'), (10, 'full'), (18, 'last'), (25, 'new')],
    11: [(2, 'first'), (9, 'full'), (16, 'last'), (23, 'new')],
    12: [(1, 'first'), (8, 'full'), (16, 'last'), (23, 'new'), (30, 'first')]
}

# Default birthdays (empty by default, user can add custom birthdays)
default_birthdays = {
    1: [], 2: [], 3: [], 4: [], 5: [], 6: [],
    7: [], 8: [], 9: [], 10: [], 11: [], 12: []
}

def draw_cutting_border(c, x, y, width, height):
    """
    Draws a cutting border for easier paper trimming.
    """
    c.setLineWidth(0.5)
    c.setStrokeColorRGB(0.5, 0.5, 0.5)  # Gray color
    c.setDash(3, 3)  # Dashed line
    c.rect(x, y, width, height)
    c.setDash()  # Reset to solid line
    c.setStrokeColorRGB(0, 0, 0)  # Black color

def draw_calendar(c, year, month, x, y, width_offset, height_offset, holidays_dict, month_font=("Helvetica-Bold", 12), day_font=("Helvetica-Bold", 11), bg_color=(1, 1, 1), normal_text_color=(0, 0, 0), weekend_bg_color=(0.94, 0.94, 0.94), holiday_bg_color=(1, 0.9, 0.9), week_num_text_color=(0.5, 0.5, 0.5), week_num_bg_color=(1, 1, 1), show_week_numbers=True, highlight_holidays=True, show_equinoxes=False, equinox_circle_color=(0, 0.5, 1), show_moon_phases=False, moon_phase_color=(0.3, 0.3, 0.6), moon_phase_size=10, show_birthdays=False, birthdays_dict={}, birthday_square_color=(1, 0.75, 0.8)):
    """
    Draws the calendar for a specific month.
    """
    cal = Calendar()
    month_days = cal.monthdayscalendar(year, month)
    month_name_str = month_name[month]
    
    # Draw background
    c.setFillColorRGB(bg_color[0], bg_color[1], bg_color[2])
    c.rect(x + width_offset - 1.5 * cm, y + height_offset - 0.5 * cm, 8 * cm, 7.5 * cm, fill=1, stroke=0)
    
    c.setLineWidth(1)
    c.setFont(month_font[0], month_font[1])
    c.setFillColorRGB(normal_text_color[0], normal_text_color[1], normal_text_color[2])
    c.drawCentredString(x + width_offset + 2.5 * cm, y + height_offset + 7 * cm, month_name_str)
    
    add_y_offset = 10
    add_x_offset = -0.1

    c.setFont(day_font[0], day_font[1])
    day_names = ["Mo", "Tue", "We", "Th", "Fr", "Sat", "Sun"]
    for i, day_name in enumerate(day_names):
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.setLineWidth(0)
        c.setFillColorRGB(normal_text_color[0], normal_text_color[1], normal_text_color[2])
        c.drawCentredString(x + width_offset + (i + add_x_offset) * cm, y + (height_offset+10) + 6 * cm, day_name)

    week_num = 1
    for week in month_days:
        first_day_of_week = next((day for day in week if day != 0), None)
        if first_day_of_week:
            week_number = date(year, month, first_day_of_week).isocalendar()[1]
        
        # Draw day backgrounds first
        for i, day in enumerate(week):
            if day != 0:
                # Determine background color and draw it
                day_bg_color = bg_color  # default
                if highlight_holidays and day in holidays_dict.get(month, []):
                    day_bg_color = holiday_bg_color
                elif i == 5 or i == 6:  # Saturday or Sunday
                    day_bg_color = weekend_bg_color
                
                # Draw day background - scale with font size
                cell_width = 0.95 * cm * (day_font[1] / 11)  # Scale based on font size
                cell_height = 0.65 * cm * (day_font[1] / 11)
                cell_x = x + width_offset + (i + add_x_offset) * cm - cell_width / 2
                cell_y = y + (height_offset) + (9 - week_num) * 0.7 * cm - cell_height / 2
                c.setFillColorRGB(day_bg_color[0], day_bg_color[1], day_bg_color[2])
                c.rect(cell_x, cell_y, cell_width, cell_height, fill=1, stroke=0)
        
        # Draw week number (after backgrounds so it's not covered)
        if show_week_numbers and first_day_of_week:
            week_num_x = x + width_offset - 1.6 * cm  # Moved further left
            week_num_y = y + (height_offset) + (9 - week_num) * 0.7 * cm
            
            # Draw week number background
            c.setFillColorRGB(week_num_bg_color[0], week_num_bg_color[1], week_num_bg_color[2])
            c.rect(week_num_x - 0.15 * cm, week_num_y - 0.15 * cm, 0.6 * cm, 0.45 * cm, fill=1, stroke=0)
            
            # Draw week number text
            c.setFillColorRGB(week_num_text_color[0], week_num_text_color[1], week_num_text_color[2])
            c.drawString(week_num_x, week_num_y, str(week_number))
        
        # Draw day numbers
        for i, day in enumerate(week):
            if day != 0:
                # Determine text color
                if highlight_holidays and day in holidays_dict.get(month, []):
                    c.setFillColor(red)
                elif i == 5:  # Saturday
                    c.setFillColor(gray)
                elif i == 6:  # Sunday
                    c.setFillColor(red)
                else:
                    c.setFillColorRGB(normal_text_color[0], normal_text_color[1], normal_text_color[2])
                c.drawCentredString(x + width_offset + (i + add_x_offset) * cm, y + (height_offset) + (9 - week_num) * 0.7 * cm, str(day))
        week_num += 1
    
    # Draw circles around equinoxes and solstices (on top of everything)
    if show_equinoxes:
        week_num = 1
        for week in month_days:
            for i, day in enumerate(week):
                if day != 0 and day in equinoxes_solstices.get(month, []):
                    circle_x = x + width_offset + (i + add_x_offset) * cm
                    circle_y = y + (height_offset) + (9 - week_num) * 0.7 * cm + 0.15 * cm  # Moved up by 1.5mm
                    circle_radius = (0.35 * cm - 0.07 * cm) * (day_font[1] / 11)  # Reduced by 0.7mm and scale with font size
                    
                    c.setStrokeColorRGB(equinox_circle_color[0], equinox_circle_color[1], equinox_circle_color[2])
                    c.setLineWidth(1.5)
                    c.circle(circle_x, circle_y, circle_radius, stroke=1, fill=0)
            week_num += 1
    
    # Draw moon phase symbols (on top of everything)
    if show_moon_phases:
        month_moon_phases = {day: phase_type for day, phase_type in moon_phases.get(month, [])}
        week_num = 1
        for week in month_days:
            for i, day in enumerate(week):
                if day != 0 and day in month_moon_phases:
                    phase_type = month_moon_phases[day]
                    moon_x = x + width_offset + (i + add_x_offset) * cm + 0.38 * cm + 0.1 * cm
                    moon_y = y + (height_offset) + (9 - week_num) * 0.7 * cm + 0.25 * cm
                    radius = moon_phase_size / 2.8  # Convert font size to radius
                    
                    c.setStrokeColorRGB(moon_phase_color[0], moon_phase_color[1], moon_phase_color[2])
                    c.setFillColorRGB(moon_phase_color[0], moon_phase_color[1], moon_phase_color[2])
                    c.setLineWidth(1)
                    
                    if phase_type == 'new':  # New moon - filled circle
                        c.circle(moon_x, moon_y, radius, stroke=1, fill=1)
                    elif phase_type == 'full':  # Full moon - empty circle
                        c.circle(moon_x, moon_y, radius, stroke=1, fill=0)
                    elif phase_type == 'first':  # First quarter - right half filled
                        c.circle(moon_x, moon_y, radius, stroke=1, fill=0)
                        # Fill right half
                        path = c.beginPath()
                        path.moveTo(moon_x, moon_y - radius)
                        path.lineTo(moon_x, moon_y + radius)
                        path.arcTo(moon_x - radius, moon_y - radius, moon_x + radius, moon_y + radius, 270, 180)
                        c.drawPath(path, stroke=0, fill=1)
                    elif phase_type == 'last':  # Last quarter - left half filled
                        c.circle(moon_x, moon_y, radius, stroke=1, fill=0)
                        # Fill left half
                        path = c.beginPath()
                        path.moveTo(moon_x, moon_y - radius)
                        path.lineTo(moon_x, moon_y + radius)
                        path.arcTo(moon_x - radius, moon_y - radius, moon_x + radius, moon_y + radius, 90, 180)
                        c.drawPath(path, stroke=0, fill=1)
            week_num += 1
    
    # Draw squares around birthdays (on top of everything)
    if show_birthdays:
        month_birthdays = birthdays_dict.get(month, [])
        week_num = 1
        for week in month_days:
            for i, day in enumerate(week):
                if day != 0 and day in month_birthdays:
                    square_x = x + width_offset + (i + add_x_offset) * cm
                    square_y = y + (height_offset) + (9 - week_num) * 0.7 * cm
                    square_size = (0.35 * cm) * (day_font[1] / 11)  # Scale with font size
                    
                    c.setStrokeColorRGB(birthday_square_color[0], birthday_square_color[1], birthday_square_color[2])
                    c.setLineWidth(1.5)
                    c.rect(square_x - square_size, square_y - square_size, 
                           square_size * 2, square_size * 2, stroke=1, fill=0)
            week_num += 1
    
    c.setFillColorRGB(normal_text_color[0], normal_text_color[1], normal_text_color[2])  # Reset color

def create_calendar_pdf(filename, year, holidays_dict, month_font=("Helvetica-Bold", 12), day_font=("Helvetica-Bold", 11), bg_color=(1, 1, 1), normal_text_color=(0, 0, 0), weekend_bg_color=(0.94, 0.94, 0.94), holiday_bg_color=(1, 0.9, 0.9), week_num_text_color=(0.5, 0.5, 0.5), week_num_bg_color=(1, 1, 1), show_week_numbers=True, highlight_holidays=True, show_equinoxes=False, equinox_circle_color=(0, 0.5, 1), show_moon_phases=False, moon_phase_color=(0.3, 0.3, 0.6), moon_phase_size=10, show_birthdays=False, birthdays_dict={}, birthday_square_color=(1, 0.75, 0.8)):
    """
    Creates a PDF file with the calendar for a specific year (4 months per page).
    """
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Border dimensions: 10 cm x 13 cm
    border_width = 10 * cm
    border_height = 13 * cm
    
    for month in range(1, 13, 4):
        c.setLineWidth(1)
        inner_x = (width - 16.5 * cm) / 2
        inner_y = (height - 1 * cm) / 2
        
        # Calculate border positions for left column (2 months)
        left_border_x = inner_x - 2.0 * cm
        left_border_y = inner_y + 0.7 * cm
        
        # Calculate border positions for right column (2 months)
        right_border_x = inner_x + 10 * cm - 2.0 * cm
        right_border_y = inner_y + 0.7 * cm

        # Draw calendars first
        draw_calendar(c, year, month, inner_x, inner_y, 0, 5.7 * cm, holidays_dict, month_font, day_font, bg_color, normal_text_color, weekend_bg_color, holiday_bg_color, week_num_text_color, week_num_bg_color, show_week_numbers, highlight_holidays, show_equinoxes, equinox_circle_color, show_moon_phases, moon_phase_color, moon_phase_size, show_birthdays, birthdays_dict, birthday_square_color)
        
        if month + 1 <= 12:
            draw_calendar(c, year, month + 1, inner_x, inner_y, 0, 0, holidays_dict, month_font, day_font, bg_color, normal_text_color, weekend_bg_color, holiday_bg_color, week_num_text_color, week_num_bg_color, show_week_numbers, highlight_holidays, show_equinoxes, equinox_circle_color, show_moon_phases, moon_phase_color, moon_phase_size, show_birthdays, birthdays_dict, birthday_square_color)
        
        if month + 2 <= 12:
            draw_calendar(c, year, month + 2, inner_x, inner_y, 10 * cm, 5.7 * cm, holidays_dict, month_font, day_font, bg_color, normal_text_color, weekend_bg_color, holiday_bg_color, week_num_text_color, week_num_bg_color, show_week_numbers, highlight_holidays, show_equinoxes, equinox_circle_color, show_moon_phases, moon_phase_color, moon_phase_size, show_birthdays, birthdays_dict, birthday_square_color)
        
        if month + 3 <= 12:
            draw_calendar(c, year, month + 3, inner_x, inner_y, 10 * cm, 0, holidays_dict, month_font, day_font, bg_color, normal_text_color, weekend_bg_color, holiday_bg_color, week_num_text_color, week_num_bg_color, show_week_numbers, highlight_holidays, show_equinoxes, equinox_circle_color, show_moon_phases, moon_phase_color, moon_phase_size, show_birthdays, birthdays_dict, birthday_square_color)

        # Draw cutting borders on top (after all calendars)
        draw_cutting_border(c, left_border_x, left_border_y, border_width, border_height)
        draw_cutting_border(c, right_border_x, right_border_y, border_width, border_height)

        c.showPage()
    
    c.save()

def create_full_year_calendar_pdf(filename, year, holidays_dict, month_font=("Helvetica-Bold", 12), day_font=("Helvetica-Bold", 11), bg_color=(1, 1, 1), normal_text_color=(0, 0, 0), weekend_bg_color=(0.94, 0.94, 0.94), holiday_bg_color=(1, 0.9, 0.9), week_num_text_color=(0.5, 0.5, 0.5), week_num_bg_color=(1, 1, 1), show_week_numbers=True, highlight_holidays=True, show_equinoxes=False, equinox_circle_color=(0, 0.5, 1), show_moon_phases=False, moon_phase_color=(0.3, 0.3, 0.6), moon_phase_size=10, show_birthdays=False, birthdays_dict={}, birthday_square_color=(1, 0.75, 0.8)):
    """
    Creates a PDF file with all months of a year on a single A4 sheet.
    """
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    c.setFont(month_font[0], 18)
    c.setFillColorRGB(normal_text_color[0], normal_text_color[1], normal_text_color[2])
    c.drawCentredString(width / 2, height - 0.5 * cm, str(year))
    
    x_offsets = [2 * cm, 12 * cm, 22 * cm]
    y_offsets = [height - 8.5 * cm - i * 5 * cm for i in range(4)]

    month = 1
    for y_offset in y_offsets:
        for x_offset in x_offsets:
            if month <= 12:
                draw_calendar(c, year, month, x_offset, y_offset, 13, 12, holidays_dict, month_font, day_font, bg_color, normal_text_color, weekend_bg_color, holiday_bg_color, week_num_text_color, week_num_bg_color, show_week_numbers, highlight_holidays, show_equinoxes, equinox_circle_color, show_moon_phases, moon_phase_color, moon_phase_size, show_birthdays, birthdays_dict, birthday_square_color)
                month += 1

    c.save()

def generate_calendar_callback():
    """Callback function for generating calendar PDFs."""
    year = dpg.get_value("year_input")
    format_type = dpg.get_value("format_combo")
    
    # Get font settings
    font_family = dpg.get_value("font_family")
    font_style = dpg.get_value("font_style")
    month_font_size = dpg.get_value("month_font_size")
    day_font_size = dpg.get_value("day_font_size")
    
    # Build font names based on family
    if font_family == "Times-Roman":
        font_map = {
            "Normal": "Times-Roman",
            "Bold": "Times-Bold",
            "Italic": "Times-Italic",
            "Bold-Italic": "Times-BoldItalic"
        }
        font_name = font_map[font_style]
    else:  # Helvetica or Courier
        style_suffix = {
            "Normal": "",
            "Bold": "-Bold",
            "Italic": "-Oblique",
            "Bold-Italic": "-BoldOblique"
        }
        font_name = font_family + style_suffix[font_style]
    
    month_font = (font_name, month_font_size)
    day_font = (font_name, day_font_size)
    
    # Get color settings (convert from 0-255 to 0-1 range for ReportLab)
    bg_color_rgb = dpg.get_value("bg_color")
    bg_color = (bg_color_rgb[0]/255, bg_color_rgb[1]/255, bg_color_rgb[2]/255)
    
    normal_text_rgb = dpg.get_value("normal_text_color")
    normal_text_color = (normal_text_rgb[0]/255, normal_text_rgb[1]/255, normal_text_rgb[2]/255)
    
    weekend_bg_rgb = dpg.get_value("weekend_bg_color")
    weekend_bg_color = (weekend_bg_rgb[0]/255, weekend_bg_rgb[1]/255, weekend_bg_rgb[2]/255)
    
    holiday_bg_rgb = dpg.get_value("holiday_bg_color")
    holiday_bg_color = (holiday_bg_rgb[0]/255, holiday_bg_rgb[1]/255, holiday_bg_rgb[2]/255)
    
    week_num_text_rgb = dpg.get_value("week_num_text_color")
    week_num_text_color = (week_num_text_rgb[0]/255, week_num_text_rgb[1]/255, week_num_text_rgb[2]/255)
    
    week_num_bg_rgb = dpg.get_value("week_num_bg_color")
    week_num_bg_color = (week_num_bg_rgb[0]/255, week_num_bg_rgb[1]/255, week_num_bg_rgb[2]/255)
    
    show_week_numbers = dpg.get_value("show_week_numbers")
    highlight_holidays = dpg.get_value("highlight_holidays")
    show_equinoxes = dpg.get_value("show_equinoxes")
    
    equinox_circle_rgb = dpg.get_value("equinox_circle_color")
    equinox_circle_color = (equinox_circle_rgb[0]/255, equinox_circle_rgb[1]/255, equinox_circle_rgb[2]/255)
    
    show_moon_phases = dpg.get_value("show_moon_phases")
    
    moon_phase_rgb = dpg.get_value("moon_phase_color")
    moon_phase_color = (moon_phase_rgb[0]/255, moon_phase_rgb[1]/255, moon_phase_rgb[2]/255)
    
    moon_phase_size = dpg.get_value("moon_phase_size")
    
    show_birthdays = dpg.get_value("show_birthdays")
    
    birthday_square_rgb = dpg.get_value("birthday_square_color")
    birthday_square_color = (birthday_square_rgb[0]/255, birthday_square_rgb[1]/255, birthday_square_rgb[2]/255)
    
    # Get birthdays from input fields
    birthdays_dict = {}
    for month in range(1, 13):
        birthdays_input = dpg.get_value(f"birthdays_{month}")
        if birthdays_input:
            try:
                birthday_days = [int(d.strip()) for d in birthdays_input.split(',') if d.strip()]
                birthdays_dict[month] = [d for d in birthday_days if 1 <= d <= 31]
            except ValueError:
                birthdays_dict[month] = []
        else:
            birthdays_dict[month] = []
    
    # Get holidays from checkboxes
    holidays_dict = {}
    for month in range(1, 13):
        holidays_dict[month] = []
        for day in default_holidays.get(month, []):
            if dpg.get_value(f"holiday_{month}_{day}"):
                holidays_dict[month].append(day)
    
    # Get custom holidays from input fields
    for month in range(1, 13):
        custom_input = dpg.get_value(f"custom_{month}")
        if custom_input:
            try:
                custom_days = [int(d.strip()) for d in custom_input.split(',') if d.strip()]
                holidays_dict[month].extend([d for d in custom_days if 1 <= d <= 31 and d not in holidays_dict[month]])
            except ValueError:
                pass
    
    try:
        if format_type == "4 months/page (A4)":
            filename = f"calendar_{year}_office.pdf"
            create_calendar_pdf(filename, year, holidays_dict, month_font, day_font, bg_color, normal_text_color, weekend_bg_color, holiday_bg_color, week_num_text_color, week_num_bg_color, show_week_numbers, highlight_holidays, show_equinoxes, equinox_circle_color, show_moon_phases, moon_phase_color, moon_phase_size, show_birthdays, birthdays_dict, birthday_square_color)
        elif format_type == "12 months/page (A4 landscape)":
            filename = f"calendar_{year}_full.pdf"
            create_full_year_calendar_pdf(filename, year, holidays_dict, month_font, day_font, bg_color, normal_text_color, weekend_bg_color, holiday_bg_color, week_num_text_color, week_num_bg_color, show_week_numbers, highlight_holidays, show_equinoxes, equinox_circle_color, show_moon_phases, moon_phase_color, moon_phase_size, show_birthdays, birthdays_dict, birthday_square_color)
        else:  # Both
            filename1 = f"calendar_{year}_office.pdf"
            filename2 = f"calendar_{year}_full.pdf"
            create_calendar_pdf(filename1, year, holidays_dict, month_font, day_font, bg_color, normal_text_color, weekend_bg_color, holiday_bg_color, week_num_text_color, week_num_bg_color, show_week_numbers, highlight_holidays, show_equinoxes, equinox_circle_color, show_moon_phases, moon_phase_color, moon_phase_size, show_birthdays, birthdays_dict, birthday_square_color)
            create_full_year_calendar_pdf(filename2, year, holidays_dict, month_font, day_font, bg_color, normal_text_color, weekend_bg_color, holiday_bg_color, week_num_text_color, week_num_bg_color, show_week_numbers, highlight_holidays, show_equinoxes, equinox_circle_color, show_moon_phases, moon_phase_color, moon_phase_size, show_birthdays, birthdays_dict, birthday_square_color)
            filename = f"{filename1} and {filename2}"
        
        dpg.set_value("status_text", f"✓ Successfully generated: {filename}")
        dpg.configure_item("status_text", color=(0, 255, 0))
    except Exception as e:
        dpg.set_value("status_text", f"✗ Error: {str(e)}")
        dpg.configure_item("status_text", color=(255, 0, 0))

def switch_section(sender, app_data, user_data):
    """Callback to switch between sections."""
    sections = ["basic_section", "fonts_section", "colors_section", "features_section", "holidays_section", "birthdays_section"]
    for section in sections:
        dpg.hide_item(section)
    dpg.show_item(user_data)

def create_gui():
    """Creates the Dear PyGui interface."""
    dpg.create_context()
    dpg.create_viewport(title="Calendar Generator", width=1000, height=750)
    
    current_year = datetime.now().year
    
    # Load icons as textures
    icon_textures = {}
    icon_names = ["basic", "fonts", "colors", "features", "holidays", "birthdays"]
    for icon_name in icon_names:
        icon_path = f"icons/{icon_name}.png"
        if os.path.exists(icon_path):
            width, height, channels, data = dpg.load_image(icon_path)
            
            with dpg.texture_registry():
                icon_textures[icon_name] = dpg.add_static_texture(width, height, data, tag=f"{icon_name}_texture")
    
    with dpg.window(label="Calendar Generator", tag="primary_window", width=1000, height=750, no_close=True):
        # Top bar with title and generate button
        with dpg.group(horizontal=True):
            dpg.add_text("PDF Calendar Generator", color=(100, 200, 255))
            dpg.add_spacer(width=400)
            dpg.add_button(label="Generate Calendar", callback=generate_calendar_callback, width=250, height=35)
        
        dpg.add_separator()
        dpg.add_spacer(height=10)
        
        # Status text
        dpg.add_text("", tag="status_text", color=(255, 255, 255))
        dpg.add_spacer(height=5)
        
        # Main layout: sidebar on left, content on right
        with dpg.group(horizontal=True):
            # Left sidebar with navigation buttons
            with dpg.child_window(width=180, height=600):
                dpg.add_text("Settings", color=(100, 200, 255))
                dpg.add_separator()
                dpg.add_spacer(height=10)
                
                # Create buttons with icons if available
                for icon_name, label, section in [
                    ("basic", "Basic", "basic_section"),
                    ("fonts", "Fonts", "fonts_section"),
                    ("colors", "Colors", "colors_section"),
                    ("features", "Features", "features_section"),
                    ("holidays", "Holidays", "holidays_section"),
                    ("birthdays", "Birthdays", "birthdays_section")
                ]:
                    if icon_name in icon_textures:
                        with dpg.group(horizontal=True):
                            dpg.add_image(f"{icon_name}_texture", width=32, height=32)
                            dpg.add_button(label=label, width=120, height=32, callback=switch_section, user_data=section)
                    else:
                        dpg.add_button(label=label, width=160, height=40, callback=switch_section, user_data=section)
                    dpg.add_spacer(height=5)
            
            # Right content area
            with dpg.child_window(width=790, height=600):
                # Basic Settings Section
                with dpg.group(tag="basic_section"):
                    dpg.add_spacer(height=10)
                    dpg.add_text("Basic Settings", color=(100, 200, 255))
                    dpg.add_separator()
                    dpg.add_spacer(height=10)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text("Year:")
                        dpg.add_spacer(width=90)
                        dpg.add_input_int(tag="year_input", default_value=current_year, width=100, min_value=1900, max_value=2100, min_clamped=True, max_clamped=True)
                    
                    dpg.add_spacer(height=15)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text("Format:")
                        dpg.add_spacer(width=72)
                        dpg.add_combo(["4 months/page (A4)", "12 months/page (A4 landscape)", "Both"], 
                                     default_value="Both", tag="format_combo", width=300)
                
                # Font Settings Section
                with dpg.group(tag="fonts_section", show=False):
                    dpg.add_spacer(height=10)
                    dpg.add_text("Font Settings", color=(100, 200, 255))
                    dpg.add_separator()
                    dpg.add_spacer(height=10)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text("Font Family:")
                        dpg.add_spacer(width=60)
                        dpg.add_combo(["Helvetica", "Times-Roman", "Courier"], 
                                     default_value="Helvetica", tag="font_family", width=200)
                    
                    dpg.add_spacer(height=15)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text("Font Style:")
                        dpg.add_spacer(width=68)
                        dpg.add_combo(["Normal", "Bold", "Italic", "Bold-Italic"], 
                                     default_value="Bold", tag="font_style", width=200)
                    
                    dpg.add_spacer(height=15)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text("Month name size:")
                        dpg.add_spacer(width=20)
                        dpg.add_slider_int(tag="month_font_size", default_value=12, min_value=8, max_value=20, width=300)
                    
                    dpg.add_spacer(height=15)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text("Day numbers size:")
                        dpg.add_spacer(width=20)
                        dpg.add_slider_int(tag="day_font_size", default_value=11, min_value=6, max_value=16, width=300)
                
                # Color Settings Section
                with dpg.group(tag="colors_section", show=False):
                    dpg.add_spacer(height=10)
                    dpg.add_text("Color Settings", color=(100, 200, 255))
                    dpg.add_separator()
                    dpg.add_spacer(height=10)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text("Background:")
                        dpg.add_spacer(width=95)
                        dpg.add_color_edit(tag="bg_color", default_value=(255, 255, 255, 255), width=150, no_alpha=True, input_mode=dpg.mvColorEdit_input_rgb)
                    
                    dpg.add_spacer(height=15)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text("Normal days text:")
                        dpg.add_spacer(width=55)
                        dpg.add_color_edit(tag="normal_text_color", default_value=(0, 0, 0, 255), width=150, no_alpha=True, input_mode=dpg.mvColorEdit_input_rgb)
                    
                    dpg.add_spacer(height=15)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text("Weekend background:")
                        dpg.add_spacer(width=15)
                        dpg.add_color_edit(tag="weekend_bg_color", default_value=(240, 240, 240, 255), width=150, no_alpha=True, input_mode=dpg.mvColorEdit_input_rgb)
                    
                    dpg.add_spacer(height=15)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text("Holiday background:")
                        dpg.add_spacer(width=25)
                        dpg.add_color_edit(tag="holiday_bg_color", default_value=(255, 230, 230, 255), width=150, no_alpha=True, input_mode=dpg.mvColorEdit_input_rgb)
                    
                    dpg.add_spacer(height=15)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text("Week number text:")
                        dpg.add_spacer(width=35)
                        dpg.add_color_edit(tag="week_num_text_color", default_value=(128, 128, 128, 255), width=150, no_alpha=True, input_mode=dpg.mvColorEdit_input_rgb)
                    
                    dpg.add_spacer(height=15)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text("Week number background:")
                        dpg.add_spacer(width=5)
                        dpg.add_color_edit(tag="week_num_bg_color", default_value=(255, 255, 255, 255), width=150, no_alpha=True, input_mode=dpg.mvColorEdit_input_rgb)
                
                # Features Section
                with dpg.group(tag="features_section", show=False):
                    dpg.add_spacer(height=10)
                    dpg.add_text("Features", color=(100, 200, 255))
                    dpg.add_separator()
                    dpg.add_spacer(height=10)
                    
                    dpg.add_checkbox(label="Show week numbers", tag="show_week_numbers", default_value=True)
                    dpg.add_spacer(height=15)
                    
                    dpg.add_checkbox(label="Highlight holidays with color", tag="highlight_holidays", default_value=True)
                    dpg.add_spacer(height=15)
                    
                    dpg.add_checkbox(label="Mark equinoxes & solstices", tag="show_equinoxes", default_value=False)
                    dpg.add_spacer(height=10)
                    with dpg.group(horizontal=True):
                        dpg.add_text("    Circle color:")
                        dpg.add_spacer(width=55)
                        dpg.add_color_edit(tag="equinox_circle_color", default_value=(0, 128, 255, 255), width=150, no_alpha=True, input_mode=dpg.mvColorEdit_input_rgb)
                    
                    dpg.add_spacer(height=15)
                    
                    dpg.add_checkbox(label="Show moon phases", tag="show_moon_phases", default_value=False)
                    dpg.add_spacer(height=10)
                    with dpg.group(horizontal=True):
                        dpg.add_text("    Symbol color:")
                        dpg.add_spacer(width=50)
                        dpg.add_color_edit(tag="moon_phase_color", default_value=(76, 76, 153, 255), width=150, no_alpha=True, input_mode=dpg.mvColorEdit_input_rgb)
                    dpg.add_spacer(height=10)
                    with dpg.group(horizontal=True):
                        dpg.add_text("    Symbol size:")
                        dpg.add_spacer(width=60)
                        dpg.add_slider_int(tag="moon_phase_size", default_value=10, min_value=6, max_value=14, width=300)
                
                
                # Holidays Section
                with dpg.group(tag="holidays_section", show=False):
                    dpg.add_spacer(height=10)
                    dpg.add_text("Legal Holidays (check to include)", color=(100, 200, 255))
                    dpg.add_separator()
                    dpg.add_spacer(height=10)
                    
                    # Holidays selection in columns
                    with dpg.group(horizontal=True):
                        # Column 1 (Jan-Apr)
                        with dpg.child_window(width=240, height=500):
                            month_names_en = ["", "January", "February", "March", "April", "May", "June",
                                            "July", "August", "September", "October", "November", "December"]
                            for month in range(1, 5):
                                dpg.add_text(f"{month_names_en[month]}:", color=(150, 150, 255))
                                for day in default_holidays.get(month, []):
                                    dpg.add_checkbox(label=f"  Day {day}", tag=f"holiday_{month}_{day}", default_value=True)
                                dpg.add_text("  Custom days (e.g., 10,15):", color=(180, 180, 180))
                                dpg.add_input_text(tag=f"custom_{month}", width=200)
                                dpg.add_spacer(height=5)
                        
                        # Column 2 (May-Aug)
                        with dpg.child_window(width=240, height=500):
                            for month in range(5, 9):
                                dpg.add_text(f"{month_names_en[month]}:", color=(150, 150, 255))
                                for day in default_holidays.get(month, []):
                                    dpg.add_checkbox(label=f"  Day {day}", tag=f"holiday_{month}_{day}", default_value=True)
                                dpg.add_text("  Custom days (e.g., 10,15):", color=(180, 180, 180))
                                dpg.add_input_text(tag=f"custom_{month}", width=200)
                                dpg.add_spacer(height=5)
                        
                        # Column 3 (Sep-Dec)
                        with dpg.child_window(width=240, height=500):
                            for month in range(9, 13):
                                dpg.add_text(f"{month_names_en[month]}:", color=(150, 150, 255))
                                for day in default_holidays.get(month, []):
                                    dpg.add_checkbox(label=f"  Day {day}", tag=f"holiday_{month}_{day}", default_value=True)
                                dpg.add_text("  Custom days (e.g., 10,15):", color=(180, 180, 180))
                                dpg.add_input_text(tag=f"custom_{month}", width=200)
                                dpg.add_spacer(height=5)
                
                # Birthdays Section
                with dpg.group(tag="birthdays_section", show=False):
                    dpg.add_spacer(height=10)
                    dpg.add_text("Birthdays", color=(100, 200, 255))
                    dpg.add_separator()
                    dpg.add_spacer(height=10)
                    
                    dpg.add_checkbox(label="Show birthdays", tag="show_birthdays", default_value=False)
                    dpg.add_spacer(height=10)
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text("Square color:")
                        dpg.add_spacer(width=20)
                        dpg.add_color_edit(tag="birthday_square_color", default_value=(255, 191, 204, 255), width=150, no_alpha=True, input_mode=dpg.mvColorEdit_input_rgb)
                    
                    dpg.add_spacer(height=15)
                    dpg.add_text("Enter birthday days for each month (comma-separated):", color=(180, 180, 180))
                    dpg.add_spacer(height=10)
                    
                    # Birthday input in columns
                    with dpg.group(horizontal=True):
                        # Column 1 (Jan-Apr)
                        with dpg.child_window(width=240, height=450):
                            month_names_en = ["", "January", "February", "March", "April", "May", "June",
                                            "July", "August", "September", "October", "November", "December"]
                            for month in range(1, 5):
                                dpg.add_text(f"{month_names_en[month]}:", color=(150, 150, 255))
                                dpg.add_input_text(tag=f"birthdays_{month}", hint="e.g., 5,12,25", width=200)
                                dpg.add_spacer(height=10)
                        
                        # Column 2 (May-Aug)
                        with dpg.child_window(width=240, height=450):
                            for month in range(5, 9):
                                dpg.add_text(f"{month_names_en[month]}:", color=(150, 150, 255))
                                dpg.add_input_text(tag=f"birthdays_{month}", hint="e.g., 5,12,25", width=200)
                                dpg.add_spacer(height=10)
                        
                        # Column 3 (Sep-Dec)
                        with dpg.child_window(width=240, height=450):
                            for month in range(9, 13):
                                dpg.add_text(f"{month_names_en[month]}:", color=(150, 150, 255))
                                dpg.add_input_text(tag=f"birthdays_{month}", hint="e.g., 5,12,25", width=200)
                                dpg.add_spacer(height=10)
    
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("primary_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    create_gui()
