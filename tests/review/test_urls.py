import pytest

from django.urls import reverse, resolve
from review.models import Ticket
from authentication.models import User

def test_home_url():
    path = reverse('review:home')
    assert path == '/home/'
    assert resolve(path).view_name == 'review:home'


def test_add_ticket_url():
    path = reverse('review:add_ticket')
    assert path == '/home/add_ticket/'
    assert resolve(path).view_name == 'review:add_ticket'


@pytest.mark.django_db
def test_modify_ticket_url():
    user = User.objects.create_user(username='testuser', password="userpass")
    Ticket.objects.create(title='ticket title',
                          description='ticket description',
                          user=user)

    path = reverse('review:add_ticket', kwargs={'ticket_id': 1})

    assert path == '/home/add_ticket/1'
    assert resolve(path).view_name == 'review:add_ticket'
