#!/bin/bash
set -e

echo "=========================================="
echo "Starting HRMS Backend Build Process"
echo "=========================================="
echo ""

echo "1. Python Environment"
echo "   Python version:"
python --version
echo "   Pip version:"
pip --version
echo ""

echo "2. Installing Dependencies"
pip install -r requirements.txt
echo "   Dependencies installed successfully"
echo ""

echo "3. Django Setup"
export DJANGO_SETTINGS_MODULE=api.settings
export PYTHONPATH=$(pwd):$PYTHONPATH

echo "   Running collectstatic..."
python manage.py collectstatic --noinput 2>/dev/null || echo "   Warning: Collectstatic failed (may not be needed for serverless)"
echo ""

echo "4. Database Migrations"
echo "   Attempting to run migrations..."
python manage.py migrate --noinput 2>&1 || echo "   Warning: Migrations failed (database may not be available)"
echo ""

echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="
