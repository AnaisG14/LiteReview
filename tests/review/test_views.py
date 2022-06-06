import pytest

from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from review.models import Ticket
from authentication.models import User


@pytest.mark.django_db
def test_home():
    client = Client()

    # create a user
    credentials = {
        'username': 'test_user',
        'first_name': 'test',
        'last_name': 'user',
        'email': 'test@email.com',
        'password1': 'userpass',
        'password2': 'userpass'
    }

    client.post('/signup/', credentials)
    client.post('/', {"username": "test_user", "password": "userpass"})

    path = reverse('review:home')
    response = client.get(path)

    assert response.status_code == 200
    assertTemplateUsed(response, 'review/home.html')

    content = response.content.decode()
    assert 'Créer une critique' in content
    assert 'Demander une critique' in content
