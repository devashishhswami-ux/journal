#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit  # Exit on error

echo "========================================="
echo "Starting Render Build Process"
echo "========================================="

echo "Step 1/5: Upgrading pip..."
pip install --upgrade pip

echo "Step 2/5: Installing dependencies..."
pip install -r requirements.txt

echo "Step 3/5: Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Step 4/5: Running database migrations..."
python manage.py migrate --no-input

echo "Step 5/5: Creating admin user..."
python manage.py ensure_admin || echo "Warning: Could not create admin user automatically. You may need to create one manually."

echo "========================================="
echo "Build completed successfully!"
echo "========================================="
