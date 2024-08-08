import pytest
from django.contrib.auth.models import User


# Fixtures
@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "password": "securepassword",
        "email": "testuser@example.com"
    }


@pytest.fixture
def create_user(user_data):
    user = User.objects.create_user(**user_data)
    return user


# Test cases
@pytest.mark.django_db
class TestUserRegistration:
    def test_user_registration_success(self, client, user_data):
        url = '/api/users/register'
        response = client.post(url, user_data, content_type='application/json')
        assert response.status_code == 200
        assert response.json() == {"success": "User registered successfully"}

    def test_user_registration_existing_username(self, client, create_user, user_data):
        user_data['email'] = 'newemail@example.com'  # Ensure the email is unique
        url = '/api/users/register'
        response = client.post(url, user_data, content_type='application/json')
        assert response.status_code == 400
        assert response.json() == {"error": "Username already exists"}

    def test_user_registration_existing_email(self, client, create_user, user_data):
        user_data['username'] = 'newusername'  # Ensure the username is unique
        url = '/api/users/register'
        response = client.post(url, user_data, content_type='application/json')
        assert response.status_code == 400
        assert response.json() == {"error": "Email already registered"}


@pytest.mark.django_db
class TestUserLogin:
    def test_user_login_success(self, client, create_user, user_data):
        url = '/api/users/login'
        response = client.post(url, user_data, content_type='application/json')
        assert response.status_code == 200
        assert "access" in response.json()
        assert "refresh" in response.json()

    def test_user_login_invalid_credentials(self, client, user_data):
        user_data['password'] = 'wrongpassword'
        url = '/api/users/login'
        response = client.post(url, user_data, content_type='application/json')
        assert response.status_code == 401
        assert response.json() == {"error": "Invalid credentials"}


@pytest.mark.django_db
class TestTokenRefresh:
    def test_token_refresh_success(self, client, create_user, user_data):
        # Log in to get refresh token
        login_url = '/api/users/login'
        login_response = client.post(login_url, user_data, content_type='application/json')
        refresh_token = login_response.json()['refresh']

        # Refresh token
        refresh_url = '/api/users/token/refresh'
        response = client.post(refresh_url, {}, content_type='application/json',
                               HTTP_AUTHORIZATION=f'Bearer {refresh_token}')
        assert response.status_code == 200
        assert "access" in response.json()
        assert "refresh" in response.json()

    def test_token_refresh_no_token(self, client):
        refresh_url = '/api/users/token/refresh'
        response = client.post(refresh_url, {}, content_type='application/json')
        assert response.status_code == 401
        assert response.json() == {"error": "No refresh token provided"}

    def test_token_refresh_invalid_token(self, client):
        refresh_url = '/api/users/token/refresh'
        response = client.post(refresh_url, {}, content_type='application/json',
                               HTTP_AUTHORIZATION='Bearer invalidtoken')
        assert response.status_code == 401
        assert response.json() == {"error": "Invalid refresh token"}
