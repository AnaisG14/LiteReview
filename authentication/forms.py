from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    username = forms.CharField(max_length=60, label='nom d\'utilisateur')
    password = forms.CharField(max_length=20, label='mot de passe', widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()    # permet d'obtenir le model user sans l'importer
        fields = ('username', 'first_name', 'last_name', 'email')
