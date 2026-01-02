@echo off

REM Get the directory where the batch file is located
cd /d "%~dp0"

REM Activate virtual environment and run the calendar GUI
call .venv\Scripts\activate.bat
python calendar_gui.py
pause
