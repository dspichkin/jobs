#!/usr/bin/env bash
celery worker -A root.celery --concurrency=4 
#celery -A root.celery beat -l info

