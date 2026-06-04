@echo off
cd /d "%~dp0"

echo ============================================
echo   Fast KHQR Web UI (Anajak API)
echo ============================================
echo.
echo Starting the web interface...
echo The browser will open in a few seconds.
echo.
echo To stop the server, close this window.
echo.

:: Open browser after short delay
start "" http://127.0.0.1:5000

:: Small delay so browser opens after server starts
timeout /t 3 >nul

:: Run the Flask app
python app.py

echo.
echo Server stopped.
pause