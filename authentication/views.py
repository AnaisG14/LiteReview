from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from . import forms


def logout_user(request):
    """ Logout the user and redirect to the authentication page. """

    logout(request)
    return redirect('authentication:login')


def login_page(request):
    """ Login the user and redirect to the home page. """

    form = forms.LoginForm()
    message = ''
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('review:home')
            else:
                message = "identifiants invalides"
    context = {'form': form, 'message': message}
    return render(request, 'authentication/login.html', context)


def signup(request):
    """ Create a new count for a new user and
    redirect to the authentication page. """

    form = forms.SignUpForm()
    message = ''
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Votre inscription est effectuée, connectez-vous'
    context = {'form': form, 'message': message}
    return render(request, 'authentication/signup.html', context)
