@echo off
echo Starting Coffee Shop POS Backend...
echo.

cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo ERROR: .env file not found!
    echo.
    echo Please create a .env file in the backend directory.
    echo You can copy env_template.txt and rename it to .env
    echo Then edit .env with your MySQL credentials.
    echo.
    pause
    exit /b 1
)

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo Installing/updating dependencies...
    pip install -r requirements.txt --quiet
)

REM Check if database is initialized
echo.
echo Checking database initialization...
echo Run 'python init_db.py' if you haven't initialized the database yet.
echo.

REM Start the Flask server
echo Starting Flask server...
echo Backend will run on: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server.
echo.

python run.py

pause

