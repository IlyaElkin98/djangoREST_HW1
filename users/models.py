from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission

from config import settings
from users.managers import UserManager


class User(AbstractUser):
    """Модель пользователь"""
    username = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    objects = UserManager()

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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments', verbose_name='Пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey('materials.Course', on_delete=models.CASCADE, null=True, blank=True)
    paid_lesson = models.ForeignKey('materials.Lesson', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=[('cash', 'Наличными'), ('transfer', 'Перевод на счет')])
    session_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='ID сессии')
    link = models.URLField(max_length=500, null=True, blank=True, verbose_name='Ссылка на оплату')
    payment_status = models.CharField(max_length=50, default='pending')

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.payment_method})"
