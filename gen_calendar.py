from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, black, gray
from calendar import month_name, Calendar
from datetime import date

# List of holiday dates (example)
holidays = {
    1: [1,6,7,24],  # January 1
    4: [18,20,21],  # April holidays
    5: [1],
    6: [1,8, 9],
    8: [15],
    12: [1, 25, 26]  # December 25 and 26
}

def draw_calendar(c, year, month, x, y, width_offset, height_offset, month_font=("Helvetica-Bold", 12), day_font=("Helvetica-Bold", 11)):
    """
    Draws the calendar for a specific month.

    Parameters:
    c (canvas.Canvas): The canvas object to draw on.
    year (int): The year to draw the calendar for.
    month (int): The month to draw the calendar for.
    x (float): Starting X position for drawing.
    y (float): Starting Y position for drawing.
    width_offset (float): X-axis offset for drawing.
    height_offset (float): Y-axis offset for drawing.
    month_font (tuple): Font for month name (font_name, font_size).
    day_font (tuple): Font for weekday names (font_name, font_size).
    """
    cal = Calendar()
    month_days = cal.monthdayscalendar(year, month)  # Get the month's days as weeks
    month_name_str = month_name[month]  # Get the month name
    
    # Draw the border around the month, including week numbers
    c.setLineWidth(1)
    #c.rect(x + width_offset - 1.5 * cm, y + height_offset + 55, 8.5 * cm, 5.5 * cm)  # Adjust height to 8 cm

    # Draw the month name
    c.setFont(month_font[0], month_font[1])
    c.setFillColor(black)
    c.drawCentredString(x + width_offset + 2.5 * cm, y + height_offset + 7 * cm, month_name_str)
    
    add_y_offset = 10
    add_x_offset = -0.1

    # Draw weekday names
    c.setFont(day_font[0], day_font[1])
    day_names = ["Mo", "Tue", "We", "Th", "Fr", "Sat", "Sun"]
    for i, day_name in enumerate(day_names):
        # Draw light gray background
        c.setFillColorRGB(0.9, 0.9, 0.9)  # Set fill color to light gray
        c.setLineWidth(0)  # Set line width to 0 to avoid drawing outline
        # Draw weekday text
        c.setFillColor(black)  # Reset fill color to black
        c.drawCentredString(x + width_offset + (i + add_x_offset) * cm, y + (height_offset+10) + 6 * cm, day_name)

    week_num = 1
    for week in month_days:
        # Calculate global week number
        first_day_of_week = next(day for day in week if day != 0)
        week_number = date(year, month, first_day_of_week).isocalendar()[1]
        
        # Draw week number
        c.setFillColor(black)
        c.drawString(x + width_offset - 1.2 * cm, y + (height_offset) + (9 - week_num) * 0.7 * cm, str(week_number))
        
        # Draw month days
        for i, day in enumerate(week):
            if day != 0:
                if day in holidays.get(month, []):  # Check if day is a holiday
                    c.setFillColor(red)
                elif i == 5:  # Saturday
                    c.setFillColor(gray)
                elif i == 6:  # Sunday
                    c.setFillColor(red)
                else:
                    c.setFillColor(black)
                c.drawCentredString(x + width_offset + (i + add_x_offset) * cm, y + (height_offset) + (9 - week_num) * 0.7 * cm, str(day))
        week_num += 1
    c.setFillColor(black)  # Reset color to black for other elements

def create_calendar_pdf(filename, year):
    """
    Creates a PDF file with the calendar for a specific year.

    Parameters:
    filename (str): Name of the PDF file to create.
    year (int): Year to create the calendar for.
    """
    c = canvas.Canvas(filename, pagesize=A4)  # Create canvas object for PDF
    width, height = A4  # A4 page dimensions
    
    for month in range(1, 13, 4):  # Iterate through months, four per page (two columns)
        c.setLineWidth(1)

        inner_x = (width - 16.5 * cm) / 2  # Calculate X position for centering
        inner_y = (height - 1 * cm) / 2  # Calculate Y position for centering

        # Draw first month in upper half
        draw_calendar(c, year, month, inner_x, inner_y, 0, 5.7 * cm)  # Adjust distance between months

        # Draw second month in first column, lower half
        if month + 1 <= 12:
            draw_calendar(c, year, month + 1, inner_x, inner_y, 0, 0)  # Adjust distance between months

        # Draw third month in second column, upper half
        if month + 2 <= 12:
            draw_calendar(c, year, month + 2, inner_x, inner_y, 10 * cm, 5.7 * cm)  # Adjust distance between months and columns

        # Draw fourth month in second column, lower half
        if month + 3 <= 12:
            draw_calendar(c, year, month + 3, inner_x, inner_y, 10 * cm, 0)  # Adjust distance between months and columns

        c.showPage()  # Add new page
    
    c.save()  # Save PDF

def create_full_year_calendar_pdf(filename, year):
    """
    Creates a PDF file with all months of a year on a single A4 sheet.

    Parameters:
    filename (str): Name of the PDF file to create.
    year (int): Year to create the calendar for.
    """
    c = canvas.Canvas(filename, pagesize=landscape(A4))  # Create canvas object for PDF
    width, height = landscape(A4)  # A4 page dimensions
    
    # Draw year at the top of the page
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 0.5 * cm, str(year))
    
    # Dimensions and offsets for month placement on page
    x_offsets = [2 * cm, 12 * cm, 22 * cm]  # X positions for three columns
    y_offsets = [height - 8.5 * cm - i * 5 * cm for i in range(4)]  # Y positions for four rows

    month = 1
    for y_offset in y_offsets:
        for x_offset in x_offsets:
            if month <= 12:
                draw_calendar(c, year, month, x_offset, y_offset, 13, 12)
                month += 1

    c.save()  # Save PDF
    
create_calendar_pdf("calendar_2025_for_office.pdf",2025)    
create_full_year_calendar_pdf("full_year_calendar.pdf", 2025)