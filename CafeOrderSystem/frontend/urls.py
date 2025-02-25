from django.urls import path
from .views import base

app_name = 'frontend'
urlpatterns = [path('base/',base,name='base')]