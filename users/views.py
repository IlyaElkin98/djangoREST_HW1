from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Закрыть экшены авторизацией, кроме регистрации.

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [permissions.AllowAny]  # Разрешить регистрацию для всех
        return super().get_permissions()

