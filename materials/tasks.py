from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from users.service import send_mailing
from .models import Subscription, Course


@shared_task
def mailing_about_updates(course_id):
    """Функция отправления сообщений об обновлении курса клиентам"""
    course = Course.objects.get(pk=course_id)
    subscription_list = course.subscription.all()
    user_list = [subscription.user for subscription in subscription_list]
    subject = 'Обновление'
    body = f'Вышло обновление по курсу {course}'
    send_mailing(user_list, subject, body)