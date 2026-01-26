from django.core.management.base import BaseCommand
from users.models import Payment, User
from materials.models import Course, Lesson
from datetime import date

class Command(BaseCommand):
    help = 'Populate payment data'

    def handle(self, *args, **kwargs):
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        course1 = Course.objects.get(pk=1)
        lesson1 = Lesson.objects.get(pk=1)
        lesson2 = Lesson.objects.get(pk=2)

        Payment.objects.create(user=user1, payment_date=date(2023, 10, 1), paid_course=course1, paid_lesson=lesson1, amount=100.00, payment_method='cash')
        Payment.objects.create(user=user2, payment_date=date(2023, 10, 2), paid_course=course1, paid_lesson=lesson2, amount=150.00, payment_method='transfer')

        self.stdout.write(self.style.SUCCESS('Successfully populated payments'))
