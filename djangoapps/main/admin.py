from django.contrib import admin
from django.db.models import Count

from main.models import Skill, Company, AdvHabr


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
    list_display = (
        'title', 'last_update', 'get_history_update', 'company', 'salary',
        'remote', 'get_skills', 'city')
    filter_horizontal = ('skills',)

    def get_skills(self, obj):
        return [t.title for t in obj.skills.all()]

    def get_history_update(self, obj):
        return len(obj.history_update)
