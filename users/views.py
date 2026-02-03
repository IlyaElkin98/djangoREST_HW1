from rest_framework import viewsets, permissions
from .models import User
from .permissions import Moderator
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Закрыть экшены авторизацией, кроме регистрации.

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [~Moderator]  # Запретить создание и удаления курсов и уроков
        elif self.action in ['list', 'retrieve', 'update']:
            self.permission_classes = [Moderator]  # Разрешить просмотр и обновления курсов и уроков
        return super().get_permissions()

