from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from .models import Order, Meal
from .serializers import OrderSerializer, MealSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.dateparse import parse_date

class MealViewSet(ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    http_method_names = ['get', 'post', 'patch', 'put', 'delete']


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get', 'post', 'patch', 'put', 'delete']
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['table_number', 'status']

    def get_queryset(self):
        queryset = super().get_queryset()
        date_param = self.request.query_params.get('date')
        if date_param:
            try:
                date_obj = parse_date(date_param)
                if date_obj:
                    queryset = queryset.filter(created__date=date_obj)
                    queryset = queryset.exclude(status__in=[Order.Status.PENDING, Order.Status.CANCELED])
                else:
                    return Order.objects.none()
            except ValueError:
                return Order.objects.none()
    
        return queryset