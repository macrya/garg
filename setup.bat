@echo off
echo ============================================
echo Garage Management System - Quick Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo [OK] Python detected
python --version
echo.

REM Create virtual environment
echo [*] Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo [*] Installing dependencies...
pip install -r requirements.txt

REM Initialize database
echo [*] Initializing database with sample data...
python init_db.py

echo.
echo ============================================
echo [OK] Setup Complete!
echo ============================================
echo.
echo To start the application:
echo 1. Activate virtual environment:
echo    venv\Scripts\activate
echo 2. Run the application:
echo    python app.py
echo.
echo 3. Open your browser and go to:
echo    http://localhost:5000
echo.
echo Login Credentials:
echo    Admin: admin / admin123
echo    Staff: staff / staff123
echo.
echo ============================================
pause
