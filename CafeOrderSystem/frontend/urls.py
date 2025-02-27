from django.urls import path
from .views import menu_list, menu_detail

app_name = 'frontend'
urlpatterns = [
    path('',menu_list,name='home'),
    path('menu/list', menu_list, name='menu_list'),
    path('menu/detail/<int:meal_id>', menu_detail, name='menu_detail'),
    ]