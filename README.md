# 🚛 ELD Trip Planner

A FMCSA-compliant ELD (Electronic Logging Device) trip planner.

celery -A project worker  --loglevel=INFO

celery -A project worker flower

# python manage.py migrate --database=default
# python manage.py migrate --database=gis