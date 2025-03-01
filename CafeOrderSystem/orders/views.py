from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from .models import Order, Meal
from .serializers import OrderSerializer, MealSerializer
from rest_framework.filters import SearchFilter


class MealViewSet(ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    http_method_names = ['get', 'post', 'patch', 'put', 'delete']

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get', 'post', 'patch', 'put', 'delete']
    filter_backends = [SearchFilter]
    search_fields = ['table_number', 'status']