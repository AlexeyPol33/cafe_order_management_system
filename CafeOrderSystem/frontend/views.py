import requests
import json
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
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


def basket(request):
    try:
        basket = request.COOKIES.get('basket', json.dumps({}))
        items = json.loads(basket).get('items',[])
    except json.JSONDecodeError:
            return render(
                request=request,
                template_name='error/error.html',
                context={'message':"error: Invalid JSON in cookie"},
                status=400)
    total_price = sum([i.price for i in items])
    total_quantity = sum([i.quantity for i in items])

    return render(
        request=request,
        template_name='order/basket.html',
        context={'items': items,
                 'total_price': total_price,
                 'total_quantity': total_quantity})


def basket_add_item(request, meal_id:int, quantity=1):
    basket = request.COOKIES.get('basket', None)
    meal_url = request.build_absolute_uri(reverse('orders:meal-detail', kwargs={'pk': meal_id}))
    meal = requests.get(meal_url)
    if meal.status_code != 200:
        return render(
            request=request,
            template_name='error/error.html',
            context={'message':meal.text},
            status=meal.status_code)
    if basket:
        try:
            data = json.load(basket)
            items = data['items']
            try:
                item = [i for i, _ in enumerate(items) if _==meal_id].pop() # Если элемент уже есть в корзине
                data['items'][item]['quantity'] += quantity
            except IndexError: # Если элемента нет
                data['items'].append(
                {meal.id:{
                    'name': meal.name,
                    'price': meal.price,
                    'quantity': quantity,
                    'url': request.build_absolute_uri(reverse('frontend:menu_detail',args=meal.id))}})
        except json.JSONDecodeError:
            return render(
                request=request,
                template_name='error/error.html',
                context={'message':"error: Invalid JSON in cookie"},
                status=400)
    else:
        data = json.dumps({
                'items':[{meal.id:{
                    'name': meal.name,
                    'quantity': quantity,
                    'url': request.build_absolute_uri(reverse('frontend:menu_detail',args=meal.id))}}]})
    return HttpResponse('',).set_cookie()