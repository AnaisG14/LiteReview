from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User

        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=[
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
        

class LoginForm(forms.Form):
    """ A login form to connect the user. """
    username = forms.CharField(max_length=60, label='nom d\'utilisateur')
    password = forms.CharField(max_length=20, label='mot de passe', widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    """ A signup form to create a new count for a new user. """
    class Meta(UserCreationForm.Meta):
        # permet d'obtenir le model user sans l'importer
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')
