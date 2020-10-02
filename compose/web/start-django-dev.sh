#!/usr/bin/env bash
python /app/djangoapps/manage.py migrate --noinput && \
python /app/djangoapps/manage.py runserver 0.0.0.0:8000
