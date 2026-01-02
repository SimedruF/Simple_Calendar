# Simple Calendar

A customizable calendar generator for creating PDF calendars with full control over fonts, colors, holidays, astronomical events, moon phases, and birthdays.

## Features

- **Two PDF formats**: 4 months per page (A4 portrait) and 12 months per page (A4 landscape)
- **Font customization**: Choose from Helvetica, Times-Roman, or Courier with Normal, Bold, Italic, or Bold-Italic styles
- **Separate font sizes**: Configure month name size and day number size independently
- **Color customization**:
  - Background color
  - Text color
  - Weekend background color
  - Holiday background color
  - Week number text color
  - Week number background color
  - Equinox/solstice circle color
  - Moon phase symbol color
  - Birthday square color
- **Week numbers**: Optional display with customizable position and colors
- **Holiday highlighting**: Toggle highlighting of Romanian legal holidays
- **Astronomical events**: Optional marking of equinoxes and solstices with circles
- **Moon phases**: Display new moon, first quarter, full moon, and last quarter with configurable symbols
- **Birthdays**: Mark special dates with colored squares around the day numbers
- **Cutting borders**: Dashed 10cm x 13cm borders for trimming printed calendars

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate.bat  # On Windows
```

2. Install required packages:
```bash
pip install reportlab dearpygui pillow
```

## Usage

### Using the GUI Application (Recommended)

**Linux/Mac:**
```bash
./run_calendar.sh
```

**Windows:**
```
Double-click run_calendar.bat
```

Or manually:
```bash
python calendar_gui.py
```

### Using the Command Line

```bash
python gen_calendar.py
```

## GUI Application

The GUI application (`calendar_gui.py`) provides an intuitive interface with six main sections accessible via the sidebar:

### Basic Settings
- **Year**: Enter the year for the calendar
- **Format**: Choose between "4 Months/Page" or "12 Months/Page"

### Fonts
- **Font Family**: Helvetica, Times-Roman, or Courier
- **Font Style**: Normal, Bold, Italic, or Bold-Italic
- **Month Font Size**: Size for month names (default: 14)
- **Day Font Size**: Size for day numbers (default: 11)

### Colors
- **Background Color**: Calendar background
- **Text Color**: Normal day numbers
- **Weekend Background**: Saturday and Sunday background
- **Holiday Background**: Highlighted holiday dates
- **Week Number Text**: Week number color
- **Week Number Background**: Week number background
- **Equinox Circle Color**: Color for equinox/solstice markers
- **Moon Phase Color**: Color for moon phase symbols

### Features
- **Show Week Numbers**: Toggle week number display
- **Highlight Holidays**: Toggle holiday background coloring
- **Mark Equinoxes & Solstices**: Show circular markers on astronomical events
- **Show Moon Phases**: Display lunar phases (new, first quarter, full, last quarter)
- **Moon Phase Size**: Adjust symbol size (6-14)

### Holidays
- **Default Holidays**: Checkboxes for Romanian legal holidays
- **Custom Holidays**: Add comma-separated dates for each month (e.g., "5,12,25")

### Birthdays
- **Show Birthdays**: Toggle birthday marking
- **Square Color**: Color for the birthday markers
- **Birthday Dates**: Enter comma-separated dates for each month (e.g., "5,12,25")
  - Birthdays are marked with colored squares around the day numbers
  - Enter dates in the input field for each month separately

## Customization

### Romanian Legal Holidays

The default holidays are configured for Romania. To customize for other countries, edit the `default_holidays` dictionary in `calendar_gui.py`:

```python
default_holidays = {
    1: [1, 2],  # January 1-2: New Year
    4: [18, 19, 20, 21],  # Easter days (2026 dates)
    5: [1],  # May 1: Labour Day
    6: [1, 7, 8],  # Pentecost + National Day
    8: [15],  # August 15: Assumption Day
    11: [30],  # November 30: St. Andrew's Day
    12: [1, 25, 26]  # December 1: National Day, 25-26: Christmas
}
```

### Astronomical Events

Equinoxes and solstices for 2026 are pre-configured:
- Spring Equinox: March 20
- Summer Solstice: June 21
- Autumn Equinox: September 23
- Winter Solstice: December 21

## Output

Generated PDF files are saved in the same directory:
- `calendar_4_months_2026.pdf` - Four months per page format
- `calendar_full_year_2026.pdf` - Twelve months per page format

## Requirements

- Python 3.8+
- reportlab - PDF generation
- dearpygui - GUI framework
- pillow - Icon generation

## Icons

The application includes custom-generated icons for each section:
- **Basic**: Gear icon for general settings
- **Fonts**: Letter 'A' icon
- **Colors**: Palette icon
- **Features**: Star icon
- **Holidays**: Calendar grid icon
- **Birthdays**: Gift box icon

To regenerate icons, run:
```bash
python create_icons.py
```

## License

Open source - free to use and modify.