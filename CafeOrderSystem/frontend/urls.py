from django.urls import path
from .views import menu_list

app_name = 'frontend'
urlpatterns = [
    path('menu/list', menu_list, name='menu_list'),
    ]