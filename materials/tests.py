from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):
    """Класс для тестирования представления курсов"""

    def setUp(self):
        """В setUp мы прописывам некие фикстуры можно сказать
        создать какие-то значения. Это для того, что перед каждым выполнением теста
        будет очищаться база и запускаться setUp, который будет создавть то что нам надо"""

        self.user = User.objects.create(email="admin@mail.ru",)
        self.course = Course.objects.create(name='Первый курс', description='Описание первого курса', owner=self.user)
        self.lesson = Lesson.objects.create(title='Урок 1', description='Описание урока 1',
                                            course=self.course, video_url='youtube.com', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson-detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse('materials:lesson-list')
        data = {
            "title": "Основы базы данных",
            "description": "Описание",
            "video_url": "youtube.com",
            "course": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('materials:lesson-detail', args=(self.lesson.pk,))
        data = {
            "title": "Основы Django",
            "description": "Описание к уроку"
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Основы Django")

    def test_lesson_destroy(self):
        url = reverse('materials:lesson-detail', args=(self.lesson.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionAPIViewTest(APITestCase):
    def setUp(self):
        # Создание пользователя и курса для тестирования
        self.user = User.objects.create_user(email="test@mail.ru", username='testuser', password='testpassword')
        self.course = Course.objects.create(name='Test Course')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_add_subscription(self):
        url = reverse('materials:subscription')
        data = {'id': self.course.id}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_remove_subscription(self):
        # Сначала добавим подписку
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse('materials:subscription')
        data = {'id': self.course.id}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_course_not_found(self):
        url = reverse('materials:subscription')
        data = {'id': 999}  # ID, который не существует

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
