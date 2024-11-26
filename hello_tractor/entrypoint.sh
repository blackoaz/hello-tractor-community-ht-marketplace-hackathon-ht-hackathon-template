#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations --noinput || echo "Failed to make migrations"
python manage.py migrate --noinput || echo "Failed to migrate database"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Failed to collect static files"

# Start Gunicorn server
echo "Starting Gunicorn..."
project_name="hello_tractor"
exec gunicorn $project_name.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
