from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from main import views

urlpatterns = format_suffix_patterns([
    re_path(r'speciality/?', views.SpecialityPopularityList.as_view()),
])
