from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=60, label='nom d\'utilisateur')
    password = forms.CharField(max_length=20, label='mot de passe', widget=forms.PasswordInput)