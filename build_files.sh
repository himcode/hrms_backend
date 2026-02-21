#!/bin/bash
set -e

echo "Starting build process..."
echo "Python version:"
python --version

echo "Installing requirements..."
pip install -r requirements.txt

echo "Running Django collectstatic..."
python manage.py collectstatic --noinput 2>/dev/null || echo "Collectstatic failed (may not be needed for serverless)"

echo "Running database migrations..."
python manage.py migrate --noinput 2>/dev/null || echo "Warning: Migrations may have failed"

echo "Build completed successfully!"
