# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

app = Celery('root')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

# 18000 - 5 hours
# 10800 - 3 hours
# 3600 - 1 hours
app.conf.beat_schedule = {
    'add-every-1-hour': {
        'task': 'spiders.tasks.get_adv_habr',
        'schedule': 7200,
    },
}