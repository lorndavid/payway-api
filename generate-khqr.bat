@echo off
cd /d "%~dp0"

echo ============================================
echo   Fast KHQR Generator - Anajak API
echo ============================================
echo.
echo This will quickly generate a KHQR code using the Anajak API.
echo.

:: Ask user for amount
set /p amount="Enter amount in KHR (e.g. 1000): "

if "%amount%"=="" (
    echo.
    echo [Error] No amount was entered.
    pause
    exit /b
)

echo.
echo Generating KHQR for %amount% KHR...
echo Please wait...
echo.

:: Run the fast CLI
python fast_khqr.py %amount%

echo.
echo Done! Check for the generated .png file in this folder.
echo.
pause