from rest_framework.routers import DefaultRouter
from django.urls import path
import itertools
from .views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import logging


app_name = 'users'

router = DefaultRouter()
router.register('', UserViewSet, basename='users')
tokenpatterns = [
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh')
]

urlpatterns = itertools.chain(router.urls, tokenpatterns)
