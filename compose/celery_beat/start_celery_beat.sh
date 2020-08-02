#!/usr/bin/env bash
# rm celerybeat.pid
celery -A root.celery beat -l info

