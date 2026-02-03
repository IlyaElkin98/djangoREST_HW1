from rest_framework import viewsets, permissions
from .models import User
from .permissions import Moderator
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Закрыть экшены авторизацией, кроме регистрации.

