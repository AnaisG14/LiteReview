from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, CharField, Value
from . import forms, models
from .models import UserFollows


@login_required
def home(request):
    user_follows = [instance.followed_user for instance in UserFollows.objects.filter(user=request.user)]
    tickets = models.Ticket.objects.filter(Q(user__in=user_follows)|Q(user=request.user))
    reviews = models.Review.objects.filter(Q(user__in=user_follows)|Q(user=request.user))
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    # for review in reviews:
    #     review.rating = chr(9733) * int(review.rating) + chr(9734) * int(5 - review.rating)
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    context = {'posts': posts}
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
                ticket.number_reviews += 1
                ticket.save()
                return redirect('review:home')
        context = {'form_ticket': form_ticket, 'form_review': form_review}
    else:
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        form_review = forms.ReviewForm()
        # search if review exist for the user
        reviews = models.Review.objects.all()
        for review in reviews:
            if review.ticket.id == ticket_id and review.user == request.user:
                return redirect("review:home")
        if request.method == "POST":
            form_review = forms.ReviewForm(request.POST)
            if form_review.is_valid():
                review = form_review.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                ticket.number_reviews += 1
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


@login_required
def display_user_posts(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    context = {'posts': posts}
    return render(request, 'review/user_post.html', context)


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == "POST":
        if edit_form.is_valid():
            edit_form.save()
            return redirect('review:display_user_posts')
    context = {
        'edit_form': edit_form,
    }
    return render(request, 'review/add_ticket.html', context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    ticket = review.ticket
    edit_form = forms.ReviewForm(instance=review)
    if request.method == "POST":
        edit_form = forms.ReviewForm(request.POST, instance=review)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('review:display_user_posts')
    context = {
        'edit_form': edit_form,
        'review': review,
        'ticket': ticket,
    }
    return render(request, 'review/edit_review.html', context)
