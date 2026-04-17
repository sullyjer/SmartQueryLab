@echo off
cd /d "%~dp0"

echo Starting SmartQueryLab...

start "" cmd /c "python -m streamlit run app.py"

pause