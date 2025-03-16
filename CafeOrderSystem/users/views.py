from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from .permissions import isAccountOwnerPermission
from .serializers import UserSerializer
from .models import User



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in [
            'update', 'partial_update',
                'destroy', 'retrieve',]:
            permission_classes = [isAccountOwnerPermission | IsAdminUser]
        elif self.action in ['list']:
            permission_classes = [IsAdminUser]
        else:
            return []
        return [permission() for permission in permission_classes]