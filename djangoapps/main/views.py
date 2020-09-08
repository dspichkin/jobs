from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from main.models import AdvHabrCalculated


class SpecialityPopularityList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        speciality = request.GET.get('speciality')
        year = request.GET.get('year')
        month = request.GET.get('month')

        if not year:
            year = timezone.now().year
        else:
            year = int(year)
        if not month:
            month = timezone.now().month
        else:
            month = int(month)

        qs = AdvHabrCalculated.objects.filter(
            year=year,
            month=month)
        if speciality:
            qs = qs.filter(speciality=speciality)

        datasets = list()
        first_obj = None
        labels = []
        if qs.count() > 0:
            for index, obj in enumerate(qs):
                if index == 1:
                    first_obj = obj
                dataset = dict()
                dataset['name'] = obj.speciality
                dataset['type'] = 'line'
                dataset['smooth'] = True
                dataset["data"] = [value for key, value in obj.values["values"].items()]
                datasets.append(dataset)

            labels = [key for key, value in first_obj.values["values"].items()]
            specialties = [obj.speciality for obj in qs]

        response = {
            "series": datasets,
            "specialties": specialties,
            "labels": labels,
        }

        return Response(response, status=status.HTTP_200_OK)
