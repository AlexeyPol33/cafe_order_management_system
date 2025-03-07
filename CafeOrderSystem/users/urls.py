from django.urls import path
from rest_framework.routers import DefaultRouter
from itertools import chain
from users.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'users'
router = DefaultRouter()
router.register('', UserViewSet, basename='users')

tokenpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

urlpatterns = list(chain(router.urls, tokenpatterns))

urlpatterns = router.urls