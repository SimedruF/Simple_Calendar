#!/bin/bash
# Launcher script for Desktop Calendar Widget

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to that directory
cd "$SCRIPT_DIR"

# Activate virtual environment and run the desktop calendar
source .venv/bin/activate
python desktop_calendar.py
