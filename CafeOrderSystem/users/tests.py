import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def prepared_user(db) -> dict:
    user_name = 'testuser'
    password = 'testpassword'
    user = User.objects.create_user(username=user_name, password=password)
    return {'user':user, 'username':user_name, 'password':password}

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
def test_create_user(api_client: APIClient):
    url = reverse('users:users-list')
    username = 'newusername'
    password = 'newuserpassword'
    data = {'username': username, 'password': password}
    response = api_client.post(url, data=data,format='json')

    assert response.status_code == 201
    assert User.objects.filter(username=username).exists()

@pytest.mark.django_db
def test_get_token(api_client: APIClient, prepared_user: dict):
    url = reverse('users:token_obtain_pair')
    user = prepared_user
    data = {'username': user['username'], 'password': user['password']}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 200
    assert 'access' in response.json()
    assert "refresh" in response.json()