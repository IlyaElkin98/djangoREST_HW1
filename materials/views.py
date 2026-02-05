from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import Payment
from users.permissions import Moderator, IsOwner
from .models import Lesson, Course
from .serializers import LessonSerializer, CourseSerializer, PaymentSerializer, CourseCountSerializer


# CRUD для модели "Course" (View-sets)
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

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


# CRUD для модели "Lesson" (View-sets)
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

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
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCountSerializer


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