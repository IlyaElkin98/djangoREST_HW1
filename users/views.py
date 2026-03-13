from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer
from .service import create_price, create_session


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Закрыть экшены авторизацией, кроме регистрации.


class PaymentsViewSet(viewsets.ModelViewSet):
    """
    Контроллер платежей с фильтрацией и сортировкой
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("pay_date",)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        price = create_price(int(payment.amount))

        session_id, payment_link = create_session(price)
        payment.link = payment_link
        payment.session_id = session_id
        payment.save()
