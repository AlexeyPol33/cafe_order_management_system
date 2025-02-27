import requests
from django.shortcuts import render
from django.urls import reverse
import logging

logger = logging.getLogger('main')

def menu_list(request):
    url = request.build_absolute_uri(reverse('orders:meal-list'))
    meals = requests.get(url).json()

    return render(
        request=request,
        template_name='menu/list.html',
        context={'meals':meals})

def menu_detail(request, meal_id:int):
    url = request.build_absolute_uri(reverse('orders:meal-detail', kwargs={'pk': meal_id}))
    meal_data = requests.get(url)
    if meal_data.status_code != 200:
        return render(
            request=request,
            template_name='error/error.html',
            context={'message':meal_data.text},
            status=meal_data.status_code)
    else:
        meal_data = meal_data.json()
    return render(
        request=request,
        template_name='menu/detail.html',
        context={'meal':meal_data})
    