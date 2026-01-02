#!/bin/bash
# Setup script for Conky desktop calendar

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CONKY_CONFIG_DIR="$HOME/.config/conky"

echo "Setting up Conky desktop calendar..."

# Create conky config directory if it doesn't exist
mkdir -p "$CONKY_CONFIG_DIR"

# Activate virtual environment and generate calendar image
cd "$SCRIPT_DIR"
source .venv/bin/activate
python generate_conky_calendar.py

# Copy generated image to conky config directory
if [ -f "conky_calendar.png" ]; then
    cp conky_calendar.png "$CONKY_CONFIG_DIR/"
    echo "Calendar image copied to $CONKY_CONFIG_DIR/conky_calendar.png"
fi

# Copy conky configuration
cp conky_calendar.conf "$CONKY_CONFIG_DIR/"
echo "Conky configuration copied to $CONKY_CONFIG_DIR/conky_calendar.conf"

# Check if conky is installed
if ! command -v conky &> /dev/null; then
    echo ""
    echo "WARNING: Conky is not installed!"
    echo "Install it with: sudo apt install conky-all"
    echo ""
    exit 1
fi

# Start conky with the calendar configuration
echo ""
echo "Starting Conky calendar..."
conky -c "$CONKY_CONFIG_DIR/conky_calendar.conf" &

echo ""
echo "Conky calendar is now running on your desktop!"
echo ""
echo "To stop it: killall conky"
echo "To restart it: conky -c $CONKY_CONFIG_DIR/conky_calendar.conf &"
echo ""
echo "To make it start automatically on login, add this to your startup applications:"
echo "conky -c $CONKY_CONFIG_DIR/conky_calendar.conf"
echo ""
