from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Meal, Order
import logging

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'name', 'description', 'price']

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
    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items', 'total_price', 'status']

    def validate_table_number(self, table_number):
        if table_number is None:
            raise ValidationError(
                'table_name parameter is required',
                code=400)
        return table_number

    def validate_items(self, items):
        return items

    def validate_status(self, status):
        return status

    def create(self, validated_data):
        self.validate_table_number(validated_data.get('table_number', None))
        self.validate_items(validated_data.get('items', None))
        self.validate_total_price(validated_data.get('total_price', None))
        self.validate_status(validated_data.get('status', None))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.table_number = self.validate_table_number(validated_data.get('table_number', None))
        instance.items = self.validate_items(validated_data.get('items', None))
        instance.total_price = self.validate_total_price(validated_data.get('total_price', None))
        instance.status = self.validate_status(validated_data.get('status', None))
        return super().update(instance, validated_data)