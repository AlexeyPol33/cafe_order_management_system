from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/Order-Meal/', include('orders.urls', namespace='orders')),
    path('', include('frontend.urls', namespace='frontend')),
    path('api/users/', include('users.urls', namespace='users')),
    path('users/', include('users_front.urls', namespace='users_front')),
]