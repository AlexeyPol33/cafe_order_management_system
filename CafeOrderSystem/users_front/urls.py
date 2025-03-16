from django.urls import path
from .views import login_view, registration_view, profile_view, logout


app_name = 'users_front'

urlpatterns = [
    path(
        'login/',
        login_view,
        name='login'),
    path(
        'registration/',
        registration_view,
        name='registration'),
    path(
        'profile/',
        profile_view,
        name='profile'),
    path('logout/',
         logout,
         name='logout')
    
]