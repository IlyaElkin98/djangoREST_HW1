from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urls import app_name

from .apps import MaterialsConfig
from .views import LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView, CourseViewSet, CourseListView, PaymentListView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

app_name = MaterialsConfig.name

urlpatterns = [
    path('', include(router.urls)),
    path('lesson/new/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    path('courses_detail/', CourseListView.as_view(), name='courses-detail'),
    path('payment_list/', PaymentListView.as_view(), name='payment-list'),
    path('count/', PaymentListView.as_view(), name='count-list'),
] + router.urls
