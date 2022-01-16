# review/forms
from django import forms
from django.contrib.auth import get_user_model
from django.forms import Textarea, TextInput

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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['headline'].widget.attrs.update(size='100')
    #     self.fields['body'].widget.attrs.update(col='800')


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']


class StopFollowForm(forms.Form):
    stop_follow = forms.BooleanField(widget=forms.HiddenInput, initial=True)
