#!/bin/bash

echo "Starting Coffee Shop POS Backend..."
echo ""

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "ERROR: .env file not found!"
    echo ""
    echo "Please create a .env file in the backend directory."
    echo "You can copy env_template.txt and rename it to .env"
    echo "Then edit .env with your MySQL credentials."
    echo ""
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing/updating dependencies..."
    pip install -r requirements.txt -q
fi

# Check if database is initialized
echo ""
echo "Checking database initialization..."
echo "Run 'python init_db.py' if you haven't initialized the database yet."
echo ""

# Start the Flask server
echo "Starting Flask server..."
echo "Backend will run on: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

python run.py

