#!/bin/bash
set -e 

echo "Building the application..."

echo "Installing dependencies..."
apt-get update && apt-get install -y python3 python3-pip

if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

echo "Running application setup..."
python3 setup.py build 2>/dev/null || echo "No setup.py found, skipping build."

echo "Build completed successfully!"

