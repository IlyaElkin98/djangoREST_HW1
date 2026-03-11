from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Payment
from users.permissions import Moderator, IsOwner
from .models import Lesson, Course, Subscription
from .paginations import CustomPagination
from .serializers import LessonSerializer, CourseSerializer, PaymentSerializer, CourseCountSerializer
from materials.tasks import mailing_about_updates


# CRUD для модели "Course" (View-sets)
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):
        """Определяем права доступа с учетом запрашиваемого действия"""
        if self.action == 'create':
            self.permission_classes = [~Moderator]
        elif self.action in ['list', 'retrieve', 'update']:
            self.permission_classes = [Moderator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]
        return [permission() for permission in self.permission_classes]


    def perform_create(self, serializer):
        """Привязываем текущего пользователя к создаваемому объекту"""
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        course = serializer.save()
        mailing_about_updates.delay(course.pk)


# CRUD для модели "Lesson" (View-sets)
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomPagination


    def get_permissions(self):
        """Определяем права доступа с учетом запрашиваемого действия"""
        if self.action == 'create':
            self.permission_classes = [~Moderator]
        elif self.action in ['list', 'retrieve', 'partial_update']:
            self.permission_classes = [Moderator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]
        return [permission() for permission in self.permission_classes]


    def perform_create(self, serializer):
        """Привязываем текущего пользователя к создаваемому объекту"""
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCountSerializer

    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True, context={'request': request})
        return Response(serializer.data)


class PaymentFilter(filters.FilterSet):
    date_paid = filters.DateTimeFilter(field_name='date_paid', lookup_expr='exact')
    course = filters.ModelChoiceFilter(queryset=Course.objects.all())
    payment_method = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Payment
        fields = ['date_paid', 'course', 'payment_method']


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)


class SubscriptionAPIView(APIView):
    """ Контроллер управлением подпиской"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('id')
        course_item = get_object_or_404(Course, id=course_id)

        # Проверка, существует ли подписка
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            # Удаляем подписку
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            # Создаем новую подписку
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)