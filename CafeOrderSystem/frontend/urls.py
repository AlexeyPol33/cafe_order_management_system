from django.urls import path
from .views import menu_list, menu_detail, basket, basket_add_item, basket_del_item, post_order

app_name = 'frontend'
urlpatterns = [
    path('',menu_list,name='home'),
    path('menu/list', menu_list, name='menu_list'),
    path('menu/detail/<int:meal_id>', menu_detail, name='menu_detail'),

    path('basket/', basket, name='basket'),
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
        name='basket_del_with_quantity'
    ),
    path(
        'order/post',
        post_order,
        name='post_order',
    )
]