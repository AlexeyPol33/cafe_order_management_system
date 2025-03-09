from django.urls import path, include
from rest_framework.routers import DefaultRouter
from itertools import chain
from users.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'users'
router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'),
]