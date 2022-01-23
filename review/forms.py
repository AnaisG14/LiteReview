# review/forms
from django import forms
from django.forms import Textarea, TextInput
from . import models
from .models import UserFollows
from authentication.models import User


class TicketForm(forms.ModelForm):
    """ A form based on a model 'Ticket' to create a new ticket. """

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    """ A form based on a model 'Review' to create a new review. """

    class Meta:
        model = models.Review
        fields = ['headline', 'body', 'rating']
        RATING_CHOICES = [
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
        ]
        widgets = {
            'body': Textarea(attrs={'cols': 120, 'rows': 20}),
            'headline': TextInput(attrs={'size': 100}),
            'rating': forms.RadioSelect(choices=RATING_CHOICES)
        }


class FollowUsersForm(forms.ModelForm):
    """ A form based on a model 'FollowUsers' to create
    a new follower for a user. """

    class Meta:
        users = User.objects.all()
        model = UserFollows
        fields = ['followed_user']
        labels = {
            'followed_user': "sélectionner un utilisateur"
        }


class StopFollowForm(forms.Form):
    """ A form to stop a user follow another. """

    stop_follow = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteReviewForm(forms.Form):
    """ A form to delete a review create by the connected user. """

    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteTicketForm(forms.Form):
    """ A form to delete a ticket create by the connected user. """

    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
