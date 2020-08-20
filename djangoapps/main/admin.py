from django.contrib import admin
from django.db.models import Count, Sum
from django.conf.urls import url
from django.http import HttpResponseRedirect

from main.models import Skill, Company, AdvHabr, SkillPopularity
from spiders.runners.habr import GetAdvHabr

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


@admin.register(AdvHabr)
class AdvHabrAdmin(admin.ModelAdmin):
    change_list_template = "admin/main_change_list.html"
    list_display = (
        'title', 'last_update', 'get_history_update', 'company', 'salary',
        'remote', 'get_skills', 'city')
    filter_horizontal = ('skills',)

    def get_urls(self):
        urls = super(AdvHabrAdmin, self).get_urls()
        my_urls = [
            url('tasks_action/', self.get_tasks_action),
        ]
        return my_urls + urls

    def get_tasks_action(self, request):
        getAdv = GetAdvHabr()
        getAdv.run()
        self.message_user(request, "Get all the advs")
        return HttpResponseRedirect("../")

    def get_skills(self, obj):
        return [t.title for t in obj.skills.all()]

    def get_history_update(self, obj):
        return len(obj.history_update)


@admin.register(SkillPopularity)
class SkillPopularityAdmin(admin.ModelAdmin):
    change_list_template = 'admin/skill_popularity_change_list.html'
    date_hierarchy = 'created'

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
