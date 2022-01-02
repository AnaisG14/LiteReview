# review/forms
from django import forms
from django.contrib.auth import get_user_model

from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['headline', 'body', 'rating']


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['follower']
