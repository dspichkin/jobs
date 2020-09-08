from django.core.management.base import BaseCommand

from main.models import (
    AdvHabr, HistoryUpdated)


class Command(BaseCommand):

    def handle(self, *args, **options):
        HistoryUpdated.objects.all().delete()
        for obj in AdvHabr.objects.all():
            if obj.history_update:
                for hu in obj.history_update:
                    HistoryUpdated.objects.get_or_create(advhabr=obj, created=hu)