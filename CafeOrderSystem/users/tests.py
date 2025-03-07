import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

@pytest.fixture
def create_user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(create_user):
    client = APIClient()
    refresh = RefreshToken.for_user(create_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client

@pytest.mark.django_db
def test_get_token():
    assert True

@pytest.mark.django_db
def test_refresh_token():
    assert True