@echo off
echo Starting Coffee Shop POS Frontend...
echo.

cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    echo This may take a few minutes...
    call npm install
    echo.
)

REM Start the frontend server
echo Starting frontend development server...
echo Frontend will run on: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server.
echo.

call npm start

pause

