@echo off
echo ========================================
echo HealthSync - Integrated Healthcare Platform
echo ========================================

echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "models" mkdir models
if not exist "data" mkdir data
if not exist "logs" mkdir logs

echo.
echo Starting HealthSync application...
echo.
echo ========================================
echo Web Interface: http://localhost:5000
echo Medical Imaging: http://localhost:5000/medical-imaging
echo Blood Bank: http://localhost:5000/blood-bank
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
