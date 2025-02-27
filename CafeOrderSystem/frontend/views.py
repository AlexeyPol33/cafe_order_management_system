import requests
from django.shortcuts import render
from django.urls import reverse
import logging

logger = logging.getLogger('main')

def menu_list(request):
    url = request.build_absolute_uri(reverse('orders:meal-list'))
    meals = requests.get(url).json()

    return render(
        request,
        'menu/list.html',
        {'meals':meals})