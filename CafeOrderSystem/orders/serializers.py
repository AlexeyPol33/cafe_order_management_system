from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from typing import Sequence
from .models import Meal, Order, OrderMeal
from django.core.exceptions import ObjectDoesNotExist
import logging


logger = logging.getLogger('main')

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'name', 'description', 'price']
        read_only_fields = ['id']

    def validate_name(self, name):
        if name is None:
            raise ValidationError(
                'name is a required parameter',
                code=400)
        else:
            name = str(name)
        if name.isdigit():
            raise ValidationError(
                'name must contain the characters',
                code=400)
        if len(name) < 2 or len(name) > 200:
            raise ValidationError(
                'price must be no less than 2 and no more than 200 characters long',
                code=400)
        return name

    def validate_price(self, price):
        try:
            _price = float(price)
        except Exception as e:
            logging.ERROR(str(e))
        if _price <= 100:
            raise ValidationError(
                "the price can't be less than a hundred roubles",
                code=400)
        return price

    def create(self, validated_data):
        self.validate_name(validated_data.get('name',None))
        self.validate_price(validated_data.get('price'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = self.validate_name(validated_data.get('name',None))
        instance.price = self.validate_name(validated_data.get('price',None))
        return super().update(instance, validated_data)

class OrderSerializer(serializers.ModelSerializer):

    items = serializers.ListSerializer(
        child=serializers.DictField(
            child=serializers.IntegerField()))

    status = serializers.ChoiceField(
        choices=Order.Status.choices,
        required=False,
        allow_null=True)

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items', 'status']
        read_only_fields = ['id']

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            attrs.pop('status', None)
        return attrs

    def validate_table_number(self, table_number):
        if table_number is None:
            raise ValidationError(
                'table_name parameter is required',
                code=400)
        return table_number

    def create(self, validated_data):
        table_number = self.validate_table_number(validated_data.get('table_number', None))
        items = validated_data.get('items')
        if not items:
            raise ValidationError("Items are required", code=400)
        order = Order.objects.create(table_number=table_number, status=Order.Status.PENDING)
        logger.error(items)
        for item in items:
            try:
                meal = Meal.objects.get(id=item['meal'])
                quantity=int(item['quantity'])
            except Meal.DoesNotExist:
                raise ValidationError('Meal Does Not Exist', code=404)
            OrderMeal.objects.create(order=order, meal=meal, quantity=quantity)
            
        return order

    def update(self, instance, validated_data):
        instance.table_number = self.validate_table_number(validated_data.get('table_number', None))
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        items_data = validated_data.get('items', [])
        for item_data in items_data:
            meal = Meal.objects.get(id=item_data)
            OrderMeal.objects.update_or_create(
                order=instance, meal=meal,
                defaults={'quantity': 1}
            )
    
    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            'table_number': instance.table_number,
            'status': instance.status,
            'total_price': 0,
            'total_quantity': 0
        }

        items_representation = []
        order_meals = OrderMeal.objects.filter(order=instance)
        for order_meal in order_meals:
            meal_data = MealSerializer(order_meal.meal).data
            meal_data['quantity'] = order_meal.quantity
            items_representation.append(meal_data)
            representation['total_price'] += float(meal_data['price']) * int(order_meal.quantity)
            representation['total_quantity'] += int(order_meal.quantity)
        
        representation['items'] = items_representation
        return representation