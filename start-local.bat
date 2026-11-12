@echo off
rem Serves this folder on http://localhost:8000 and opens it in the browser. Close this window to stop.
cd /d "%~dp0"
start "" http://localhost:8000/
python -m http.server 8000
if errorlevel 1 py -m http.server 8000
pause
