#!/bin/sh
python manage.py migrate
python manage.py collectstatic
/usr/local/bin/gunicorn bike_store.wsgi:application -w 2 -b :8000 -t 120 --access-logfile=- --error-logfile=-
