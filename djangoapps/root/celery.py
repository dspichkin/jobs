import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

app = Celery('root')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-1-hour': {
        'task': 'spiders.tasks.get_adv_habr',
        'schedule': crontab(minute=16, hour='9,12,15,18,21,22,23'),
    },
}