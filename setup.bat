@echo off
REM Quick setup script for Rakk Ilis RGB Controller - Windows only

echo 🎮 Rakk Ilis RGB Setup
echo ====================

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found
    echo Install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo ✓ Python %python_version% found

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ✗ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

REM Find keyboard
echo.
echo Scanning for Rakk Ilis keyboard...
echo.

python find_keyboard.py

echo.
echo ====================
echo ✓ Setup complete!
echo.
echo Next steps:
echo 1. Run the test suite:  python test.py
echo 2. Start RGB sync:      python main.py
echo.

pause
