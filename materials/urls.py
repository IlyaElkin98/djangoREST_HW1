from django.urls import path, include
from rest_framework.routers import DefaultRouter
from materials.apps import MaterialsConfig
from .views import CourseViewSet, CourseListView, PaymentListView, LessonViewSet, SubscriptionAPIView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lesson', LessonViewSet, basename='lesson')

app_name = MaterialsConfig.name

urlpatterns = [
    path('', include(router.urls)),

    path('courses_detail/', CourseListView.as_view(), name='courses-detail'),
    path('payment_list/', PaymentListView.as_view(), name='payment-list'),
    path('count/', PaymentListView.as_view(), name='count-list'),
    path('subscribe/', SubscriptionAPIView.as_view(), name='subscription'),
] + router.urls
