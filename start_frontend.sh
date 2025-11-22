#!/bin/bash

echo "Starting Coffee Shop POS Frontend..."
echo ""

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    echo "This may take a few minutes..."
    npm install
    echo ""
fi

# Start the frontend server
echo "Starting frontend development server..."
echo "Frontend will run on: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

npm start

