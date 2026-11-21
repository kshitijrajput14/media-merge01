import pytest
from core.models import Role, UserProfile
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_user_login_success():
    client = APIClient()
    role = Role.objects.get_or_create(role_id=1, defaults={'role_name': 'Admin'})[0]
    user = UserProfile.objects.create(
        role=role,
        full_name="Test Officer",
        email="test.officer@mediamerge.in",
        password_hash=""
    )
    user.set_password("SecurePass123!")
    user.save()

    response = client.post('/api/auth/login/', {
        'email': 'test.officer@mediamerge.in',
        'password': 'SecurePass123!'
    }, format='json')

    assert response.status_code == 200
    assert 'token' in response.data
    assert response.data['user']['email'] == 'test.officer@mediamerge.in'


@pytest.mark.django_db
def test_user_login_invalid_password():
    client = APIClient()
    role = Role.objects.first() or Role.objects.create(role_id=1, role_name='Admin')
    user = UserProfile.objects.create(
        role=role,
        full_name="User Two",
        email="usertwo@mediamerge.in",
        password_hash=""
    )
    user.set_password("CorrectPassword")
    user.save()

    response = client.post('/api/auth/login/', {
        'email': 'usertwo@mediamerge.in',
        'password': 'WrongPassword'
    }, format='json')

    assert response.status_code == 401
    assert 'error' in response.data


@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    role = Role.objects.first() or Role.objects.create(role_id=1, role_name='Subscriber')

    response = client.post('/api/auth/register/', {
        'role': role.role_id,
        'full_name': 'New Creator',
        'email': 'new.creator@mediamerge.in',
        'password': 'Password123!',
        'city': 'Mumbai',
        'state': 'Maharashtra'
    }, format='json')

    assert response.status_code == 201
    assert 'token' in response.data
    assert response.data['user']['full_name'] == 'New Creator'
