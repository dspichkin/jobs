# import time
# import os
# import requests

# from django.apps import apps
import logging
from django.core.management import call_command
# from django.conf import settings
# from django.utils import timezone
# from django.apps import apps

from root.celery import app
from spiders.runners.habr import GetAdvHabr


@app.task
def get_adv_habr():
    getAdv = GetAdvHabr()
    getAdv.run()