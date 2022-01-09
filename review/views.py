from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from . import forms, models
from .models import UserFollows


@login_required
def home(request):
    user_follows = [instance.followed_user for instance in UserFollows.objects.filter(user=request.user)]
    tickets = models.Ticket.objects.filter(Q(user__in=user_follows)|Q(user=request.user))
    reviews = models.Review.objects.filter(Q(user__in=user_follows)|Q(user=request.user))
    context = {'tickets': tickets, 'reviews': reviews}
    return render(request, 'review/home.html', context)


@login_required
def add_ticket(request):
    form_ticket = forms.TicketForm()
    if request.method == "POST":
        form_ticket = forms.TicketForm(request.POST, request.FILES)
        if form_ticket.is_valid():
            # ajouter l'uploader avant de sauvegarder le ticket dans la bdd
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('review:home')
    context = {'form_ticket': form_ticket}
    return render(request, 'review/add_ticket.html', context)


@login_required
def add_review(request, ticket_id=None):
    if ticket_id is None:
        form_ticket = forms.TicketForm()
        form_review = forms.ReviewForm()
        if request.method == "POST":
            form_ticket = forms.TicketForm(request.POST, request.FILES)
            form_review = forms.ReviewForm(request.POST)
            if all([form_ticket.is_valid(), form_review.is_valid()]):
                ticket = form_ticket.save(commit=False)
                ticket.user = request.user
                ticket.save()
                review = form_review.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                ticket.review_ok = True
                ticket.save()
                return redirect('review:home')
        context = {'form_ticket': form_ticket, 'form_review': form_review}
    else:
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        form_review = forms.ReviewForm()
        if request.method == "POST":
            form_review = forms.ReviewForm(request.POST)
            if form_review.is_valid():
                review = form_review.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                ticket.review_ok = True
                ticket.save()
                return redirect('review:home')
        context = {'ticket': ticket, 'form_review': form_review}

    return render(request, 'review/add_review.html', context)



@login_required
def follow_user(request):
    form = forms.FollowUsersForm()
    if request.method == "POST":
        form = forms.FollowUsersForm(request.POST)
        if form.is_valid():
            new_follow = form.save(commit=False)
            new_follow.user = request.user
            new_follow.save()
            return redirect('review:following_page')
    context = {'form': form}
    return render(request, 'review/follow_users_form.html', context)


@login_required
def stop_follow(request, followed_id):
    followed = get_object_or_404(models.UserFollows, id=followed_id)
    stop_form = forms.StopFollowForm()
    if request.method == "POST":
        stop_form = forms.StopFollowForm(request.POST)
        if stop_form.is_valid():
            followed.delete()
            return redirect('review:following_page')
    context = {'form': stop_form, 'followed': followed}
    return render(request, 'review/stop_follow.html', context)


@login_required
def display_followers(request):
    instance_userfollows = [instance for instance in UserFollows.objects.filter(user=request.user)]
    user_followers = [ins.user for ins in UserFollows.objects.filter(followed_user=request.user)]
    context = {'instance_userfollows': instance_userfollows, 'user_followers': user_followers}
    return render(request, 'review/following_page.html', context)
