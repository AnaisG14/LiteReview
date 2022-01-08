# review/forms
from django import forms
from django.contrib.auth import get_user_model

from . import models
from .models import UserFollows


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
        model = UserFollows
        fields = ['followed_user']


class StopFollowForm(forms.Form):
    stop_follow = forms.BooleanField(widget=forms.HiddenInput, initial=True)
