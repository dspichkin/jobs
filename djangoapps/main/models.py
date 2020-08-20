import jsonfield

from django.db import models


class Skill(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    title = models.CharField(verbose_name=u'тайтл', max_length=1024, null=True, blank=True)

    class Meta:
        verbose_name = u'Скилл с Хабр.Карьера'
        verbose_name_plural = u'Скиллы с Хабр.Карьера'

    def __str__(self):
        return f"{self.title}"


class Company(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    title = models.CharField(verbose_name=u'тайтл', max_length=1024, null=True, blank=True)
    logo = models.CharField(verbose_name=u'лого компании', max_length=1024, null=True, blank=True)
    url = models.CharField(verbose_name=u'сайт', max_length=512)
    about = models.CharField(verbose_name=u'', max_length=2048)

    class Meta:
        verbose_name = u'Компания с Хабр.Карьера'
        verbose_name_plural = u'Компании с Хабр.Карьера'

    def __str__(self):
        return f"{self.title}"


WORK_TYPE_ANY = 1
WORK_TYPE_PART = 5
WORK_TYPE_FULL = 10

WORK_TYPES = (
    (WORK_TYPE_ANY, u'Любой'),
    (WORK_TYPE_PART, u'Полный рабочий день'),
    (WORK_TYPE_FULL, u'Неполный рабочий день'),
)


class AdvHabr(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    title = models.CharField(verbose_name=u'тайтл', max_length=1024, null=True, blank=True)
    url = models.CharField(verbose_name=u'url объявления', max_length=512)

    history_update = jsonfield.JSONField(verbose_name=u'даты обновления', default=[])
    last_update = models.DateTimeField(verbose_name=u'даты обновления', null=True, blank=True)
    salary = models.CharField(verbose_name=u'зараплата', max_length=255, null=True, blank=True)
    skills = models.ManyToManyField(Skill, verbose_name=u"требуемые навыки")

    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.DO_NOTHING)

    description = models.TextField(verbose_name=u'описание', null=True, blank=True)

    work_type = models.IntegerField(choices=WORK_TYPES, null=True, blank=True)
    remote = models.BooleanField(null=True, blank=True)

    city = models.CharField(verbose_name=u'город', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = u'Объявление с Хабр.Карьера'
        verbose_name_plural = u'Объявления с Хабр.Карьера'
        ordering = ('-last_update',)

    def __str__(self):
        return f"{self.title}"


class SkillPopularity(Skill):
    class Meta:
        proxy = True
        verbose_name = 'Skill Popularity'
        verbose_name_plural = 'Skill Popularity'
