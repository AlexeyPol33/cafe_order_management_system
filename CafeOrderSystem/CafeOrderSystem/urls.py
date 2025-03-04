from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Order-Meal/', include('orders.urls', namespace='orders')),
    path('', include('frontend.urls', namespace='frontend')),
    path('users/', include('users.urls', namespace='users')),

]