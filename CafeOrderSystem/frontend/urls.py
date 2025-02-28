from django.urls import path
import itertools
from .views import menu_list, menu_detail, basket, basket_add_item, basket_del_item
from .views import basket, basket_add_item, basket_del_item
from .views import post_order, order_list_one_line_view, order_list_view, \
oreder_detail_view, order_pay_button, order_canc_button, oreder_detail_view
app_name = 'frontend'
urlpatterns = []

menupatterns = [
    path('',menu_list,name='home'),
    path('menu/list', menu_list, name='menu_list'),
    path('menu/detail/<int:meal_id>', menu_detail, name='menu_detail'),
]

basketpatterns = [
    path(
        'basket/',
        basket,
        name='basket'),
    path(
        'basket/add/<int:meal_id>',
        basket_add_item,
        name='basket_add'),
    path(
        'basket/add/<int:meal_id>/<int:quantity>',
        basket_add_item,
        name='basket_add_with_quantity'),
    path(
        'basket/del/<int:meal_id>',
        basket_del_item,
        name='basket_del'),
    path(
        'basket/del/<int:meal_id>/<int:quantity>',
        basket_del_item,
        name='basket_del_with_quantity'),
]

orderpatterns = [
    path(
        'order/post',
        post_order,
        name='post_order',),
    path(
        'oreder/detail',
        oreder_detail_view,
        name='order_detail'),
    path(
        'order/list/',
        order_list_view,
        name='order_list'),
    path(
        'order/list/one-line/',
        order_list_one_line_view,
        name='order_list_one_line'),
    path(
        'order/button/pay',
        order_pay_button,
        name='order_pay'),
    path(
        'order/button/canc',
        order_canc_button,
        name='order_canc')
]
urlpatterns = list(itertools.chain(menupatterns, basketpatterns, orderpatterns))