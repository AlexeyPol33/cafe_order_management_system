from django.urls import path
import itertools
from .views import menu_list, menu_detail, basket, basket_add_item, basket_del_item
from .views import basket, basket_add_item, basket_del_item
from .views import management_menu_view, management_report_view, \
management_order_detail_view,order_del_button
from .views import post_order, order_list_one_line_view, order_list_view, \
oreder_detail_view, order_pay_button, order_canc_button, oreder_detail_view


app_name = 'frontend'

menupatterns = [
    path('',menu_list,name='home'),
    path('menu/list', menu_list, name='menu_list'),
    path('menu/detail/<int:meal_id>', menu_detail, name='menu_detail'),
]
managementpattern = [
    path(
        'management/',
        management_menu_view,
        name='management_menu'),
    path(
        'management/report/',
        management_report_view,
        name='management_report'),
    path(
        'management/order/detail/<int:order_id>',
        management_order_detail_view,
        name='management_order_detail')
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
        'order/detail/<int:order_id>',
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
        'order/button/pay/<int:order_id>',
        order_pay_button,
        name='order_pay'),
    path(
        'order/button/canc/<int:order_id>',
        order_canc_button,
        name='order_canc'),
    path(
        'order/delete/<int:order_id>',
        order_del_button,
        name='order_dell'
        )
]
urlpatterns = list(itertools.chain(menupatterns, basketpatterns, orderpatterns, managementpattern))