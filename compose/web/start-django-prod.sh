#!/usr/bin/env bash
python /app/djangoapps/manage.py migrate --noinput && \
python /app/djangoapps/manage.py collectstatic --noinput && \
gunicorn root.wsgi:application --bind 0.0.0.0:8080
