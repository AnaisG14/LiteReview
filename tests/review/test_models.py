import pytest

from django.test import Client, TestCase
from review.models import Ticket, Review, UserFollows
from authentication.models import User


class TestModels:
    USER = {'username': 'user test', 'password': 'passtest'}
    TICKET = {'title': 'ticket title', 'description': 'ticket description'}

    @pytest.mark.django_db
    def test_ticket_model(self):
        client = Client()
        self.user = User.objects.create_user(**self.USER)
        self.ticket = Ticket.objects.create(**self.TICKET, user=self.user)
        expected_value = "'ticket title' by user test (id=1)"
        assert str(self.ticket) == expected_value
        assert self.ticket.description == 'ticket description'
        assert self.ticket.user.username == "user test"

    @pytest.mark.django_db
    def test_review_model(self):
        self.user = User.objects.create_user(**self.USER)
        self.ticket = Ticket.objects.create(**self.TICKET, user=self.user)
        self.review = Review.objects.create(ticket=self.ticket,
                                            rating=4,
                                            user=self.user,
                                            headline='title review',
                                            body='body review')
        expected_value = "En réponse à 'ticket title' : title review par user test (id=1)"
        assert str(self.review) == expected_value

    @pytest.mark.django_db
    def test_user_follow(self):
        self.user1 = User.objects.create_user(**self.USER)
        self.user2 = User.objects.create_user(username="user 2", password='pass2')
        self.userfollow = UserFollows.objects.create(user=self.user1, followed_user=self.user2)
        expected_value = "user test suivi par user 2 (id=1)"
        assert str(self.userfollow) == expected_value


class TestTicketModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="user test", password='userpass')
        Ticket.objects.create(title="ticket title",
                              description="ticket description",
                              user=user)

    def test_title_label(self):
        self.ticket = Ticket.objects.get(id=1)
        field_label_title = Ticket._meta.get_field('title').verbose_name
        assert str(self.ticket) == "'ticket title' by user test (id=1)"
        self.assertEqual(field_label_title, "Titre")

    def test_length_title(self):
        self.ticket = Ticket.objects.get(id=1)
        max_length = Ticket._meta.get_field('title').max_length
        self.assertEqual(max_length, 128)
