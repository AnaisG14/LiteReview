from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from . import forms


def logout_user(request):
    logout(request)
    return redirect('authentication:login')


def login_page(request):
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
    form = forms.SignUpForm()
    message = ''
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Votre inscription est effectuée, connectez-vous'
    context = {'form': form, 'message': message}
    return render(request, 'authentication/signup.html', context)


