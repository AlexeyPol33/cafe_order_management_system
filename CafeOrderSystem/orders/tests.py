import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from orders.models import Meal, Order, OrderMeal

@pytest.mark.django_db
def test_get_meals():
    Meal.objects.create(name="Pizza", price=10.99)
    client = APIClient()
    url = reverse("orders:meal-list")

    response = client.get(url)
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Pizza"

@pytest.mark.django_db
def test_create_meal():
    client = APIClient()
    url = reverse("orders:meal-list")

    data = {"name": "Sushi", "price": 105.50}
    response = client.post(url, data, format="json")

    assert response.status_code == 201
    assert response.json()["name"] == "Sushi"
    assert Meal.objects.count() == 1

@pytest.mark.django_db
def test_create_order():
    client = APIClient()
    url = reverse("orders:order-list")
    meal = Meal.objects.create(name="Pizza", price=10.99)
    data = {
        "table_number": 4,
        "status": "PEND",
        "items": [{"meal":meal.id, "quantity": 3}]}
    
    response = client.post(url, data, format="json")

    assert response.status_code == 201
    assert response.json()["table_number"] == 4
    assert Order.objects.count() == 1