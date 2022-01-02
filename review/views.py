from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    context = {'tickets': tickets}
    return render(request, 'review/home.html', context)


@login_required
def add_ticket(request):
    form_ticket = forms.TicketForm()
    if request.method == "POST":
        form_ticket = forms.TicketForm(request.POST, request.FILES)
        if form_ticket.is_valid():
            # ajouter l'uploader avant de sauvegarder la photo dans la bdd
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('review:home')
    context = {'form_ticket': form_ticket}
    return render(request, 'review/add_ticket.html', context)


def follow_user(request):
    form = forms.FollowUsersForm()
    if request.method == "POST":
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('review:following_page')
    context = {'form': form}
    return render(request, 'review/follow_users_form.html', context)


def display_followers(request):
    user_followed = request.user.follower.all()
    user_followers = request.user.user_set.all()
    context = {'user_followed': user_followed, 'user_followers': user_followers}
    return render(request, 'review/following_page.html', context)
