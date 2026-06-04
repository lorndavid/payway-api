@echo off
cd /d "%~dp0"

:menu
cls
echo ===================================================
echo          Fast KHQR Generator (Anajak API)
echo ===================================================
echo.
echo   1. Start Web UI (open in browser)
echo   2. Generate KHQR (enter amount)
echo   3. Check Anajak Service Health
echo   4. Exit
echo.
echo ===================================================
echo.

set /p choice="Please choose an option (1-4): "

if "%choice%"=="1" goto web
if "%choice%"=="2" goto generate
if "%choice%"=="3" goto health
if "%choice%"=="4" goto exit

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:web
echo.
echo Starting Web UI...
echo Browser will open automatically.
start "" http://127.0.0.1:5000
timeout /t 2 >nul
python app.py
goto menu

:generate
echo.
set /p amount="Enter amount in KHR (example: 1500): "
if "%amount%"=="" (
    echo No amount entered.
    pause
    goto menu
)
echo.
python fast_khqr.py %amount%
echo.
pause
goto menu

:health
echo.
echo Checking Anajak API health...
python fast_khqr.py --health
echo.
pause
goto menu

:exit
echo.
echo Goodbye!
timeout /t 1 >nul
exit /b
