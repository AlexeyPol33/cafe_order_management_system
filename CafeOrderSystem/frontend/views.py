import requests
import json
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
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
            context={
                'status':meal_data.status_code,
                'message':meal_data.text
                },
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
    except json.JSONDecodeError as e:
        logger.error(f'basket JSONDecodeError: {e.msg}, cookie: {basket}')
        _render = render(
                request=request,
                template_name='error/error.html',
                context={
                    'status':400,
                    'message':"error: Invalid JSON in cookie"},
                status=400)
        _render.delete_cookie('basket')
        return _render
    total_price = 0
    total_quantity = 0
    for item in items:
        for value in item.values():
            total_price += float(value['price']) * int(value['quantity'])
            total_quantity += int(value['quantity'])
    return render(
        request=request,
        template_name='order/basket.html',
        context={'items': items,
                 'total_price': total_price,
                 'total_quantity': total_quantity})


def basket_add_item(request, meal_id: int, quantity=1):
    meal_id = int(meal_id)
    basket = request.COOKIES.get('basket', None)

    # Получаем информацию о товаре
    meal_url = request.build_absolute_uri(reverse('orders:meal-detail', kwargs={'pk': meal_id}))
    meal_response = requests.get(meal_url)

    if meal_response.status_code != 200:
        return render(
            request=request,
            template_name='error/error.html',
            context={'status': 400, 'message': meal_response.text},
            status=meal_response.status_code
        )

    meal = meal_response.json()

    # Загружаем корзину, если есть
    if basket:
        try:
            data = json.loads(basket)
        except json.JSONDecodeError:
            logger.error("basket_add_item: Invalid JSON in cookie")
            response = render(request, 'error/error.html', {'status': 400, 'message': "Invalid JSON in cookie"}, status=400)
            response.delete_cookie('basket')
            return response
    else:
        data = {"items": []}

    # Проверяем, есть ли уже товар в корзине
    item_found = False
    for item in data["items"]:
        meal_key = list(item.keys())[0]
        if int(meal_key) == meal_id:
            item[meal_key]["quantity"] += quantity
            item_found = True
            break

    # Если товара нет — добавляем новый
    if not item_found:
        data["items"].append({
            str(meal_id): {
                "name": meal["name"],
                "price": meal["price"],
                "quantity": quantity,
                "url": request.build_absolute_uri(reverse('frontend:menu_detail', args=[meal_id]))
            }
        })

    # Сохраняем обновленные данные в cookie
    response = HttpResponseRedirect(reverse('frontend:basket'))
    response.set_cookie('basket', json.dumps(data))

    return response


def basket_del_item(request, meal_id: int, quantity=1):
    meal_id = int(meal_id)
    basket = request.COOKIES.get('basket', None)
    #Проверяем существование корзины
    if basket is None:
        return render(
            request,
            'error/error.html',
            {'status': 404, 'message': "Корзина пуста"}, 
            status=404)
    
    #Проверяем, есть ли товар в корзине
    data = json.loads(basket)
    item_found = False
    for i, item in enumerate(data["items"]):
        meal_key = list(item.keys())[0]
        if int(meal_key) == meal_id:
            item[meal_key]["quantity"] -= quantity
            if item[meal_key]["quantity"] <= 0:
                data["items"].pop(i)
            item_found = True
            break

    # Если товара в корзине нет
    if not item_found:
        return render(
            request,
            'error/error.html',
            {'status': 404, 'message': "Товар отсутствует"}, 
            status=404)
    
    # Сохраняем обновленные данные в cookie
    response = HttpResponseRedirect(reverse('frontend:basket'))
    response.set_cookie('basket', json.dumps(data))

    return response
