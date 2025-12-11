#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit  # Exit on error

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Build completed successfully!"
python manage.py ensure_admin
