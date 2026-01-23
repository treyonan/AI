@echo off

REM Set the path to your Python script
set PYTHON_SCRIPT="C:\Python\AI\src\flask_test.py"

REM Explicitly set Python path
set PYTHON_EXEC=C:\Python\AI\venv\Scripts\python.exe

REM Activate the virtual environment
call C:\Python\AI\venv\Scripts\activate.bat

REM Run the Python script
%PYTHON_EXEC% %PYTHON_SCRIPT%

