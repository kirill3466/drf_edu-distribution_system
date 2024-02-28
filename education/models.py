from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=100, null=False, blank=False
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=False, blank=False
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=False, blank=False
    )
    start_date = models.DateTimeField(
        null=False, blank=False
    )
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Продукт: {self.name} | Владелец: {self.owner}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Access(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="student_access",
        null=False, blank=False
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="product_access",
        null=False, blank=False
    )
    access_check = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"Доступ к продукту: {self.product.name} \
        для студента: {self.student}"

    class Meta:
        verbose_name = 'Доступ'
        verbose_name_plural = 'Доступы'


class Lesson(models.Model):
    title = models.CharField(
        max_length=255, null=False, blank=False
    )
    video_url = models.URLField(
        null=False, blank=False
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='lessons',
        null=False, blank=False
    )

    def __str__(self):
        return f"Урок: {self.title}"

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Group(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='groups',
        null=False, blank=False
    )
    name = models.CharField(
        max_length=255, null=False, blank=False
    )
    students = models.ManyToManyField(
        User, related_name='students_group',
    )
    min_students = models.PositiveIntegerField(
        null=False, blank=False, default=1,
        validators=[MinValueValidator(1)]
    )
    max_students = models.PositiveIntegerField(
        null=False, blank=False,
        validators=[MinValueValidator(1)]
    )

    def clean(self):
        super().clean()
        if self.pk is not None:
            students_count = self.students.count()
            if students_count > self.max_students:
                raise ValidationError(
                    f"Слишком много студентов, максимум {self.max_students}"
                )

    def __str__(self):
        return f"Группа: {self.name} продукта: {self.product.name}"

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
