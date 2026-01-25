from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets

from users.models import Payment
from .models import Lesson, Course
from .serializers import LessonSerializer, CourseSerializer, PaymentSerializer


# CRUD для модели "Course" (View-sets)
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


# CRUD для модели "Lesson" (Generic-классы)
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()



class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentFilter
