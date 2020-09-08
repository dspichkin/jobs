from datetime import datetime, date, timedelta

from django.contrib import admin
from django.db.models import Count
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.contrib.admin import SimpleListFilter

from main.models import (
    Skill, Company, AdvHabr, SkillPopularity,
    SpecialityPopularity, HistoryUpdated, AdvHabrCalculated)
from spiders.runners.habr import GetAdvHabr
from main.utils import CalculateAdvHabr

from pprint import pprint


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'get_weight')

    def get_queryset(self, request):
        return Skill.objects.annotate(weight=Count('advhabr')).order_by('-weight')

    def get_weight(self, obj):
        return obj.weight

    get_weight.short_description = 'weight'
    get_weight.admin_order_field = 'weight'


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(HistoryUpdated)
class HistoryUpdatedAdmin(admin.ModelAdmin):
    list_display = ('created', 'advhabr', 'get_speciality')
    date_hierarchy = 'created'

    def get_speciality(self, obj):
        return obj.advhabr.get_speciality()


class HistoryUpdatedInline(admin.TabularInline):
    model = HistoryUpdated
    extra = 1


@admin.register(AdvHabr)
class AdvHabrAdmin(admin.ModelAdmin):
    change_list_template = "admin/main_change_list.html"
    list_display = (
        'title', 'last_update', 'get_history_update', 'company', 'salary',
        'remote', 'get_skills', 'city', 'get_speciality')
    filter_horizontal = ('skills',)
    inlines = [HistoryUpdatedInline, ]
    # actions = [calcualte_adv_habr_action, ]

    def get_urls(self):
        urls = super(AdvHabrAdmin, self).get_urls()
        my_urls = [
            url('tasks_action/', self.get_tasks_action),
            url('calc_action/', self.get_calc_action),
        ]
        return my_urls + urls

    def get_tasks_action(self, request):
        getAdv = GetAdvHabr()
        getAdv.run()
        self.message_user(request, "Get all the advs")
        return HttpResponseRedirect("../")

    def get_calc_action(self, request):
        year = request.POST.get('year', None)
        month = request.POST.get('month', None)
        calculateAdvHabr = CalculateAdvHabr()
        if year and month:
            calculateAdvHabr.run(int(year), int(month))
        if year and month is None:
            for month in range(1, 13):
                calculateAdvHabr.run(int(year), int(month))

        self.message_user(request, "Пересчет выполнен")
        return HttpResponseRedirect("../")

    def get_skills(self, obj):
        return [t.title for t in obj.skills.all()]

    def get_history_update(self, obj):
        return len(obj.history_update)

    get_history_update.short_description = 'Обнов.'


@admin.register(SkillPopularity)
class SkillPopularityAdmin(admin.ModelAdmin):
    change_list_template = 'admin/skill_popularity_change_list.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'weight': Count('advhabr'),
        }
        required_skills = [
            'Node.js', 'PHP', 'JavaScript', 'Ruby', 'Ruby on Rails', 'Python',
            'C++', 'Java', 'SQL', 'Objective-С', 'Swift', 'Net']

        response.context_data['summary'] = list(
            qs
            .filter(title__in=required_skills)
            .values('title')
            .annotate(**metrics)
            .order_by('-weight')
        )

        summary_total = 0
        for value in response.context_data['summary']:
            summary_total += value['weight']
        response.context_data['summary_total'] = summary_total
        return response


class SpecialityFilter(SimpleListFilter):
    title = 'Специальность'
    parameter_name = 'speciality'

    def lookups(self, request, model_admin):
        return [
            ('Веб разработка', 'Веб разработка'),
            ('Java разработчик', 'Java разработчик'),
            ('Тестирование', 'Тестирование'),
            ('DevOps', 'DevOps'),
            ('.NET разработка', '.NET разработка'),
        ]

    def queryset(self, request, queryset):
        return queryset.all()


@admin.register(SpecialityPopularity)
class SpecialityPopularityAdmin(admin.ModelAdmin):
    change_list_template = 'admin/speciality_popularity_change_list.html'
    date_hierarchy = 'created'
    list_filter = (SpecialityFilter,)

    def changelist_view(self, request, extra_context=None):
        first_day, last_day, period = self.get_date_range(request)
        inputed_speciality = request.GET.get('speciality')

        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        qs = HistoryUpdated.objects.filter(
            created__gte=first_day,
            created__lte=last_day).distinct()

        result = dict()
        hight_value = 0
        dates = dict()
        dateformat = None
        if period == 'hour':
            dateformat = "%Y-%m-%d %H"
            year = first_day.year
            month = first_day.month
            day = first_day.day
            for hour in range(1, 24):
                dates[datetime(year, month, day, hour).strftime(dateformat)] = 0

        if period == 'day':
            dateformat = "%Y-%m-%d"
            year = first_day.year
            month = first_day.month
            for day in range(1, self.last_day_of_month(date(year, month, 1)).day):
                dates[datetime(year, month, day).strftime(dateformat)] = 0

        if period == 'month':
            dateformat = "%Y-%m"
            year = first_day.year
            for month in range(1, 13):
                dates[datetime(year, month, 1).strftime(dateformat)] = 0

        for obj in qs.order_by('created'):
            speciality = obj.advhabr.get_speciality()
            if speciality:

                if inputed_speciality:
                    if inputed_speciality != speciality:
                        continue

                obj_date = obj.created.strftime(dateformat)
                if speciality in result:
                    result[speciality]["count"] += 1
                    result[speciality]["dates"][obj_date] += 1
                    if result[speciality]["dates"][obj_date] > hight_value:
                        hight_value = result[speciality]["dates"][obj_date]
                else:
                    result[speciality] = {
                        "count": 1,
                        "dates": dates.copy()
                    }
                    result[speciality]["dates"][obj_date] = 1
        
        # pprint(sorted(result.items(), key=lambda kv: kv[1]["count"],  reverse=True))
        # print("hight_value", hight_value)
        response.context_data['summary'] = sorted(result.items(), key=lambda kv: kv[1]["count"],  reverse=True)

        return response

    def last_day_of_month(self, any_day):
        next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
        return next_month - timedelta(days=next_month.day)

    def get_date_range(self, request):
        year = request.GET.get('created__year')
        month = request.GET.get('created__month')
        day = request.GET.get('created__day')
        if year:
            year = int(year)
        if month:
            month = int(month)
        if day:
            day = int(day)

        start_day = None
        end_day = None
        period = None
        if year is None:
            year = datetime.now().year

        if year and month and day:
            start_day = datetime(year, month, day, 0, 0, 0)
            end_day = datetime(year, month, day, 23, 59, 59)
            period = 'hour'
        elif year and month and not day:
            start_day = datetime(year, month, 1, 0, 0, 0)
            end_day = datetime(year, month, self.last_day_of_month(date(year, month, 1)).day, 23, 59, 59)
            period = 'day'
        elif year and not month and not day:
            start_day = datetime(year, 1, 1, 0, 0, 0)
            end_day = datetime(year, 12, self.last_day_of_month(date(year, 12, 1)).day, 23, 59, 59)
            period = 'month'
        return [start_day, end_day, period]

    def get_next_in_date_hierarchy(self, request, date_hierarchy):
        if date_hierarchy + '__day' in request.GET:
            return 'hour'
        if date_hierarchy + '__month' in request.GET:
            return 'day'
        if date_hierarchy + '__year' in request.GET:
            return 'week'
        return 'month'


@admin.register(AdvHabrCalculated)
class AdvHabrCalculatedAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'speciality')