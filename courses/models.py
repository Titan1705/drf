from django.db import models

from django.db import models
from users.models import User


class Course(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    preview = models.ImageField(
        upload_to="course_previews/", verbose_name="Фото", null=True, blank=True
    )
    description = models.TextField(verbose_name="Описание курса", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Название курса",
        related_name="lessons",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока", null=True, blank=True)
    preview = models.ImageField(
        upload_to="lesson_previews/", verbose_name="Фото", null=True, blank=True
    )
    video_url = models.URLField(verbose_name="Ссылка на видео", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
