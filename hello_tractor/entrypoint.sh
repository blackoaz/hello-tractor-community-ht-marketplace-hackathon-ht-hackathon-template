#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
project_name="hello_tractor"
exec gunicorn $project_name.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
