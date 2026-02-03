from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class User(AbstractUser):
    """Модель пользователь"""

    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]


class Payment(models.Model):
    """Модель оплата"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateField()
    paid_course = models.ForeignKey('materials.Course', on_delete=models.CASCADE, null=True, blank=True)
    paid_lesson = models.ForeignKey('materials.Lesson', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=[('cash', 'Наличными'), ('transfer', 'Перевод на счет')])

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.payment_method})"
