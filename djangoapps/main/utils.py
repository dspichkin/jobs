from pprint import pprint
from datetime import datetime, date, timedelta

from main.models import HistoryUpdated, AdvHabrCalculated


class CalculateAdvHabr():

    def run(self, year, month):
        data = self.run_process(year, month)
        pprint(data)
        for speciality, value in data.items():
            obj, created = AdvHabrCalculated.objects.get_or_create(
                year=year,
                month=month,
                speciality=speciality,
            )
            obj.values = value
            obj.save()

        return

    def run_process(self, year, month):

        result = dict()
        dates = dict()
        dateformat = None

        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, self.last_day_of_month(date(year, month, 1)).day)
        qs = HistoryUpdated.objects.filter(
            created__gte=first_day,
            created__lte=last_day).distinct()

        dateformat = "%Y-%m-%d"
        for day in range(1, last_day.day):
            dates[datetime(year, month, day).strftime(dateformat)] = 0

        max_value_in_month = 0
        for obj in qs.order_by('created'):
            speciality = obj.advhabr.get_speciality()
            if speciality:
                obj_date = obj.created.strftime(dateformat)
                if speciality in result:
                    result[speciality]["count"] += 1
                    result[speciality]["values"][obj_date] += 1
                    if result[speciality]["values"][obj_date] > max_value_in_month:
                        max_value_in_month = result[speciality]["values"][obj_date]
                    if result[speciality]["values"][obj_date] > \
                            result[speciality]["max_value_in_speciality"]:
                        result[speciality]["max_value_in_speciality"] = \
                            result[speciality]["values"][obj_date]
                else:
                    result[speciality] = {
                        "count": 1,
                        "values": dates.copy(),
                        "max_value_in_speciality": 0
                    }
                    result[speciality]["values"][obj_date] = 1
                result[speciality]["max_value_in_month"] = max_value_in_month
        return result

    def last_day_of_month(self, any_day):
        next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
        return next_month - timedelta(days=next_month.day)