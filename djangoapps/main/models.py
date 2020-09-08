import jsonfield

from django.db import models
from django.db.models import Q


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

    def get_speciality(self):
        if 'DevOps' in self.title:
            return 'DevOps'
        if 'тестиров' in self.title:
            return 'Тестирование'
        if 'налитик' in self.title:
            return 'Аналитика'
        if 'SAP' in self.title:
            return 'SAP'
        if 'Swift' in self.title:
            return 'iOS разработчик'

        if self.skills.filter(
            Q(title__icontains='Фронтенд') |
            Q(title__icontains='JavaScript') |
            Q(title__icontains='PHP') |
            Q(title__icontains='Vue.js') |
            Q(title__icontains='Веб-разработка') |
            Q(title__icontains='React')
                ).exists():
            return 'Веб разработка'

        if self.skills.filter(title__icontains='Тестирование').exists():
            return 'Тестирование'
        if self.skills.filter(title__icontains='Python').exists():
            return 'Python разработчик'
        if self.skills.filter(title__icontains='1с').exists():
            return '1C разработка'
        if self.skills.filter(
            Q(title__icontains='DevOps') |
                Q(title__icontains='Администрирование')).exists():
            return 'DevOps'
        if self.skills.filter(
            Q(title__icontains='.NET') |
                Q(title__icontains='C#')).exists():
            return '.NET разработка'
        if self.skills.filter(title__icontains='Java').exists():
            return 'Java разработчик'
        if self.skills.filter(
            Q(title__icontains='Менеджмент') |
                Q(title__icontains='Управление разработкой')).exists():
            return 'IT Менеджмент'
        if self.skills.filter(title__icontains='SAP').exists():
            return 'SAP'
        if self.skills.filter(
            Q(title__icontains='Objective-С') | Q(title__icontains='Swift')
                ).exists():
            return 'iOS разработчик'
        if self.skills.filter(
            Q(title__icontains='Android') | Q(title__icontains='Kotlin')
                ).exists():
            return 'Android разработчик'
        if self.skills.filter(title__icontains='Scala').exists():
            return 'Scala разработчик'
        if self.skills.filter(title__icontains='Маркетинг').exists():
            return 'Маркетинг'
        if self.skills.filter(
            Q(title__icontains='Аналитика') |
                Q(title__icontains='анализ')).exists():
            return 'Аналитика'
        if self.skills.filter(title__icontains='Кадры').exists():
            return 'HR'
        if self.skills.filter(title__icontains='C++').exists():
            return 'C++ разработчик'
        if self.skills.filter(title__icontains='Журналистика').exists():
            return 'IT журналистика'
        if self.skills.filter(
            Q(title__icontains='Веб-дизайн') |
            Q(title__icontains='UI/UX дизайн')
                ).exists():
            return 'Веб-дизайн'
        return None

    get_speciality.short_description = 'Категория'


class HistoryUpdated(models.Model):
    created = models.DateTimeField()
    advhabr = models.ForeignKey(AdvHabr, on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Дата обновления объявления с Хабр.Карьера'
        verbose_name_plural = u'Дата обновления объявлений с Хабр.Карьера'
        ordering = ('-created',)

    def __str__(self):
        return f"{self.created}"


class AdvHabrCalculated(models.Model):
    year = models.SmallIntegerField(verbose_name=u'год')
    month = models.SmallIntegerField(verbose_name=u'месяц', null=True, blank=True)
    speciality = models.CharField(verbose_name=u'специальность', max_length=256)
    values = jsonfield.JSONField(verbose_name=u'значения', default={})

    class Meta:
        verbose_name = u'Посчитанные кол-во объявлений с Хабр.Карьера'
        verbose_name_plural = u'Посчитанные кол-во объявлений с Хабр.Карьера'
        ordering = ('-year', 'month')

    def __str__(self):
        return f"{self.year}-{self.month}: {self.speciality}"


class SkillPopularity(Skill):
    class Meta:
        proxy = True
        verbose_name = 'Популярные языки программирования'
        verbose_name_plural = 'Популярные языки программирования'


class SpecialityPopularity(AdvHabr):
    class Meta:
        proxy = True
        verbose_name = 'Популярные специальность'
        verbose_name_plural = 'Популярные специальности'
