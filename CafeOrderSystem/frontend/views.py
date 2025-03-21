import requests
import json
import logging
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import OrderPostForm, SearchForm
from django.utils.dateparse import parse_date

logger = logging.getLogger('main')
order_template = {
  "table_number": 5,
  "status": "PEND",
  "items": [
    {"meal": None, "quantity": None},
    {"meal": None, "quantity": None}
  ]
}

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
                 'total_price': round(total_price, 2),
                 'total_quantity': total_quantity,
                 'form': OrderPostForm()})


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


def post_order(request):
    # Получение данных из формы и корзины
    form = None
    if request.method == 'POST':
        form = OrderPostForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                'error/error.html',
                {'status': 400, 'message': "Не верные значения формы"}, 
                status=400)
    else:
        HttpResponseRedirect(reverse('frontend:basket'))
    items = request.COOKIES.get('basket', None)
    if items is None:
        return render(
            request,
            'error/error.html',
            {'status': 400, 'message': "В корзине нет товаров"}, 
            status=400)

    # Запрос к внутреннему API
    request_tem = {
            "table_number": form.cleaned_data['table'],
            "items": [],
            "status": "PEND"}
    items = json.loads(items)["items"]
    for item in items:
        for key, value in item.items():
            request_tem["items"].append({'meal':key,'quantity':value.get('quantity',1)})
    url = request.build_absolute_uri(
    reverse('orders:order-list'))
    logger.error(request_tem)
    req = requests.post(url, json=request_tem)
    if req.status_code != 201:
        return render(
            request,
            'error/error.html',
            {'status': req.status_code, 'message': req.text})

    # Сохраняем id заказа и Удаляем корзину
    orders = request.COOKIES.get('orders', json.dumps([]))
    orders = json.loads(orders) or [] 
    orders.append(req.json().get('id'))
    response = HttpResponseRedirect(reverse('frontend:order_detail', kwargs={'order_id': req.json().get('id')}))
    response.set_cookie('orders', json.dumps(orders))
    response.delete_cookie('basket')
    return response

def order_list_one_line_view(request):
    orders_url = request.build_absolute_uri(reverse('orders:order-list'))
    form = form = SearchForm()
    orders = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            req = requests.get(orders_url + f'?search={query}')
            if req.status_code != 200:
                return render(
                    request,
                    'error/error.html',
                    {'status': req.status_code, 'message': req.text})
            orders = req.json()
        else:
            return render(
                    request,
                    'error/error.html',
                    {'status': 400, 'message': "Не корректные данные поиска"})
    else:
        req = requests.get(orders_url)
        if req.status_code != 200:
            return render(
                request,
                'error/error.html',
                {'status': req.status_code, 'message': req.text})
        orders = req.json()
    return render(
        request,
        'order/list_one_line.html',
        context={'context':orders})


def oreder_detail_view(request, order_id:int):
    order_id = int(order_id)
    order_url = request.build_absolute_uri(reverse('orders:order-detail', kwargs={'pk': order_id}))
    order = requests.get(order_url)
    if order.status_code != 200:
        return render(
            request,
            'error/error.html',
            context={'status': order.status_code, 'message': order.text},
            status=order.status_code
        )
    else:
        order = order.json()

    return render(
        request,
        'order/detail.html',
        context={'order':order})


def order_list_view(request):# todo
    return HttpResponseRedirect(reverse('frontend:order_list_one_line'))


def order_pay_button(request, order_id):
    order_url = request.build_absolute_uri(reverse('orders:order-detail', kwargs={'pk': order_id}))
    req = requests.patch(order_url, json={'status':'PAID'})
    if req.status_code != 200:
        return render(
            request,
            'error/error.html',
            {'status': req.status_code, 'message': req.text})

    return HttpResponseRedirect(reverse('frontend:order_detail',kwargs={'order_id': order_id}))


def order_canc_button(request, order_id):
    order_id = int(order_id)
    order_url = request.build_absolute_uri(reverse('orders:order-detail', kwargs={'pk': order_id}))
    req = requests.patch(order_url, json={'status':'CANC'})
    if req.status_code != 200:
        return render(
            request,
            'error/error.html',
            {'status': req.status_code, 'message': req.text})

    return HttpResponseRedirect(reverse('frontend:order_detail',kwargs={'order_id': order_id}))

def order_del_button(request, order_id):
    order_id = int(order_id)
    order_url = request.build_absolute_uri(reverse('orders:order-detail', kwargs={'pk': order_id}))
    req = requests.delete(order_url)
    if req.status_code != 204:
        return render(
            request,
            'error/error.html',
            {'status': req.status_code, 'message': req.text})
    return HttpResponseRedirect(reverse('frontend:order_list_one_line'))


def management_menu_view(request):
    return render(
        request,
        'management/menu.html')

def management_report_view(request):
    date_param = request.GET.get('date', None)
    if date_param:
        url = request.build_absolute_uri(reverse('orders:order-list'))
        date = parse_date(date_param)
        req = requests.get(url + f"?date={date}")
        if req.status_code != 200:
            return render(
                request,
                'error/error.html',
                {'status': req.status_code, 'message': req.text})
        total_prices = 0
        total_orders = 0
        for order in req.json():
            total_orders += 1
            total_prices += float(order['total_price'])
        return render(
            request,
            'management/report.html',
            context={'context':{
                'date': str(date),
                'total_orders':total_orders,
                'total_prices':round(total_prices, 2)}})
    return render(
        request,
        'management/report.html')


def management_order_detail_view(request,order_id=None):
    order_id = int(order_id)
    order_url = request.build_absolute_uri(reverse('orders:order-detail', kwargs={'pk': order_id}))
    if request.method == "PATCH":
        status = request.POST.get('status')

    order = requests.get(order_url)
    if order.status_code != 200:
        return render(
            request,
            'error/error.html',
            context={'status': order.status_code, 'message': order.text},
            status=order.status_code
        )
    else:
        order = order.json()

    return render(
        request,
        'management/order_management.html',
        context={'order':order})