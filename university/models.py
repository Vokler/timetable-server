from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from common.models import CommonModel
from common.utils import TypeWeek


class Faculty(models.Model):
    title = models.CharField(max_length=256, unique=True)
    current_type_of_week = models.SmallIntegerField(choices=TypeWeek.all())

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'

    def __str__(self):
        return self.title

    @classmethod
    def content_type(cls):
        return ContentType.objects.get_for_model(cls)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # "modified" field should be updated for sync() method
        super(Faculty, self).save()
        UniversityInfo.objects.filter(content_type=self.content_type(), object_id=self.id). \
            update(modified=timezone.now())


class Occupation(models.Model):
    title = models.CharField(max_length=256, unique=True)
    code = models.CharField(max_length=10, unique=True)
    faculty = models.ForeignKey(Faculty, related_name='occupations', null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('title', 'code')
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        return f'{self.title}'


class Group(models.Model):
    number = models.CharField(max_length=10, unique=True)
    occupation = models.ForeignKey(Occupation, related_name='groups', null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Группа студента'
        verbose_name_plural = 'Группы студентов'

    def __str__(self):
        return self.number


class Subgroup(models.Model):
    number = models.CharField(max_length=1)
    group = models.ForeignKey(Group, related_name='subgroups', null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подгруппа студента'
        verbose_name_plural = 'Подгруппы студентов'

    def __str__(self):
        return f'{self.group.number}/{self.number}'


class Subscription(CommonModel):
    title = models.CharField(max_length=150)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    subgroup = models.ForeignKey(Subgroup, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)

    basename = 'subscriptions'

    class Meta:
        unique_together = ('user', 'subgroup')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.title


class Timetbale(CommonModel):
    type_of_week = models.SmallIntegerField(choices=TypeWeek.all(), help_text='Тип недели')
    subgroup = models.ForeignKey(Subgroup, on_delete=models.CASCADE)

    basename = 'timetables'

    class Meta:
        unique_together = ('subgroup', 'type_of_week')
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'

    def __str__(self):
        return f'Расписание для {self.subgroup} группы | {TypeWeek.get_by_value(self.type_of_week)}'

    def get_faculty(self):
        return self.subgroup.group.occupation.faculty.id


class ClassTime(models.Model):
    number = models.SmallIntegerField()
    start = models.TimeField()
    end = models.TimeField()

    class Meta:
        verbose_name = 'Номер пары'
        verbose_name_plural = 'Номера пар'

    def __str__(self):
        return f'{self.number}-ая пара'


class Lecturer(CommonModel):
    name = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)

    basename = 'lecturers'

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return f'{self.name} {self.surname}'


class Class(CommonModel):
    PRACTICE = 0
    LECTURE = 1

    TYPE_OF_CLASS = (
        (PRACTICE, 'Практическое занятие'),
        (LECTURE, 'Лекция')
    )

    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    WEEKDAYS = (
        (MONDAY, 'Понедельник'),
        (TUESDAY, 'Вторник'),
        (WEDNESDAY, 'Среда'),
        (THURSDAY, 'Четверг'),
        (FRIDAY, 'Пятница'),
        (SATURDAY, 'Суббота'),
        (SUNDAY, 'Воскресенье')
    )

    title = models.CharField(max_length=150)
    type_of_class = models.SmallIntegerField(choices=TYPE_OF_CLASS, help_text='Тип занятия')
    classroom = models.CharField(max_length=10)
    class_time = models.ForeignKey(ClassTime, on_delete=models.PROTECT, help_text='Время начала занятия')
    weekday = models.SmallIntegerField(choices=WEEKDAYS)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT)
    timetable = models.ForeignKey(Timetbale, on_delete=models.CASCADE)

    basename = 'classes'

    class Meta:
        unique_together = ('timetable', 'class_time', 'weekday')
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

    def __str__(self):
        return f'{self.title} | {self.timetable.subgroup}'


class UniversityInfo(CommonModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    @classmethod
    def get_info(self):
        """
        :return: list of faculty_id and their current_type_of_week
        """
        faculties_ids = self.objects.filter(content_type=Faculty.content_type()).values_list('object_id', flat=True)
        faculties = Faculty.objects.filter(id__in=faculties_ids)
        result = [{'faculty_id': f.id, 'current_type_of_week': f.current_type_of_week} for f in faculties]
        return result
