from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.core.exceptions import ValidationError
from django.http import JsonResponse


User = get_user_model()

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if not access_token and refresh_token:
            try:
                new_access_token = str(RefreshToken(refresh_token).access_token)
                response = JsonResponse({'detail': 'access token refreshed'})
                response.set_cookie(
                    key="access_token",
                    value=new_access_token,
                    httponly=True,
                    secure=False,  # TODO Поменять при переходе на https
                    samesite='Lax',
                    max_age=3600)
                return response
            except Exception:
                pass

        if access_token:
            try:
                decoded_token = AccessToken(access_token)
                request.user = User.objects.get(id=decoded_token["user_id"])
            except Exception:
                request.user = AnonymousUser()

        