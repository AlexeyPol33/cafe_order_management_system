from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from .models import Order, Meal
from .serializers import OrderSerializer, MealSerializer


class MealViewSet(ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer