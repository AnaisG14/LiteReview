from itertools import chain
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, CharField, Value
from . import forms, models
from .models import UserFollows


@login_required
def home(request):
    """ Display the tickets and the reviews posted by the user or its followers. """

    user_follows = [instance.followed_user for instance in UserFollows.objects.filter(user=request.user)]
    tickets = models.Ticket.objects.filter(Q(user__in=user_follows) | Q(user=request.user))
    reviews = models.Review.objects.filter(Q(user__in=user_follows) |
                                           Q(user=request.user) |
                                           Q(ticket__user=request.user))
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    # the home variable is used in the template to add an active link in the nav
    context = {'posts': posts, 'home': 'home'}
    return render(request, 'review/home.html', context)


@login_required
def add_ticket(request, ticket_id=None):
    """ Add a ticket in the db or modify an existing ticket with its id in parameter."""

    # if ticket_id, modify the existing ticket
    if ticket_id:
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        form_ticket = forms.TicketForm(instance=ticket)
        if request.method == "POST":
            form_ticket = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if form_ticket.is_valid():
                # add the uploader before to save the ticket in the bdd
                ticket = form_ticket.save(commit=False)
                ticket.user = request.user
                ticket.save()
                return redirect('review:display_user_posts')
    else:
        # if not ticket_id, create a new_one
        form_ticket = forms.TicketForm()
        if request.method == "POST":
            form_ticket = forms.TicketForm(request.POST, request.FILES)
            if form_ticket.is_valid():
                # add the uploader before to save the ticket in the bdd
                ticket = form_ticket.save(commit=False)
                ticket.user = request.user
                ticket.save()
                return redirect('review:home')
    # the all_posts variable is used in the template to add an active link in the nav
    context = {'form_ticket': form_ticket, 'all_posts': 'all_posts'}
    return render(request, 'review/add_ticket.html', context)


@login_required
def add_review(request, ticket_id=None):
    """ Add a new review, corresponding to a specific ticket known with
    the parameter 'ticket_id'.
    Add a new review without ticket so the user has to create a ticket
    at the same time of the review.
    """

    # if not ticket_id, create a new ticket as the same time of a new review
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
        context = {'form_ticket': form_ticket, 'form_review': form_review, 'posts': 'posts'}
    else:
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        form_review = forms.ReviewForm()
        # search if review exist for the user in order to not create 2 reviews for one user
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
        # the all_posts variable is used in the template to add an active link in the nav
        context = {'ticket': ticket, 'form_review': form_review, 'all_posts': 'all_posts'}

    return render(request, 'review/add_review.html', context)


@login_required
def follow_user(request):
    """ Follow a new user. """

    form_follow_user = forms.FollowUsersForm()
    if request.method == "POST":
        form = forms.FollowUsersForm(request.POST)
        if form.is_valid():
            new_follow = form.save(commit=False)
            new_follow.user = request.user
            new_follow.save()
            return redirect('review:following_page')
    # the followers variable is used in the template to add an active link in the nav
    context = {'form_follow_user': form_follow_user, 'followers': 'followers'}
    return render(request, 'review/follow_users_form.html', context)


@login_required
def stop_follow(request, followed_id):
    """ Stop to follow a user. The function need a parameter : the followed_user_id."""

    followed = get_object_or_404(models.UserFollows, id=followed_id)
    stop_form = forms.StopFollowForm()
    if request.method == "POST":
        stop_form = forms.StopFollowForm(request.POST)
        if stop_form.is_valid():
            followed.delete()
            return redirect('review:following_page')
    context = {'form': stop_form, 'followed': followed, 'followers': 'followers'}
    # the followers variable is used in the template to add an active link in the nav
    return render(request, 'review/stop_follow.html', context)


@login_required
def display_followers(request):
    """ Display the followed user and the followed_by users."""

    instance_userfollows = [instance for instance in UserFollows.objects.filter(user=request.user)]
    user_followers = [ins.user for ins in UserFollows.objects.filter(followed_user=request.user)]
    form_search_user = forms.FollowUsersForm()
    if request.method == "POST":
        form_search_user = forms.FollowUsersForm(request.POST)
        if form_search_user.is_valid():
            new_follow = form_search_user.save(commit=False)
            new_follow.user = request.user
            new_follow.save()
            return redirect('review:following_page')
    # the followers variable is used in the template to add an active link in the nav
    context = {
        'instance_userfollows': instance_userfollows,
        'user_followers': user_followers,
        'form_search_user': form_search_user,
        'followers': 'followers'
    }
    return render(request, 'review/following_page.html', context)


@login_required
def display_user_posts(request):
    """ Display all the tickets and reviews of the connected user. """

    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    # the all_posts variable is used in the template to add an active link in the nav
    context = {'posts': posts, 'all_posts': 'all_posts'}
    return render(request, 'review/user_post.html', context)


@login_required
def edit_review(request, review_id):
    """ Edit a review. Requires a parameter : the review_id."""

    review = get_object_or_404(models.Review, id=review_id)
    if request.user == review.user:
        ticket = review.ticket
        edit_form = forms.ReviewForm(instance=review)
        if request.method == "POST":
            edit_form = forms.ReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('review:display_user_posts')
        # the all_posts variable is used in the template to add an active link in the nav
        context = {
            'edit_form': edit_form,
            'review': review,
            'ticket': ticket,
            'all_posts': 'all_posts'
        }
        return render(request, 'review/edit_review.html', context)
    else:
        return redirect('review:home')


@login_required
def delete_review(request, review_id):
    """ Delete a review. Requires a parameter : the review_id."""

    review = get_object_or_404(models.Review, id=review_id)
    if request.user == review.user:
        delete_form = forms.DeleteReviewForm()
        if request.method == "POST":
            delete_form = forms.DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('review:display_user_posts')
        # the all_posts variable is used in the template to add an active link in the nav
        context = {
            'delete_form': delete_form,
            'review': review,
            'all_posts': 'all_posts'
        }
        return render(request, 'review/delete_review.html', context)
    else:
        return redirect('review:home')


@login_required
def delete_ticket(request, ticket_id):
    """ Delete a ticket. Requires a parameter : the ticket_id."""
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.user == ticket.user:
        delete_ticket = forms.DeleteTicketForm()
        if request.method == "POST":
            delete_ticket = forms.DeleteTicketForm(request.POST)
            if delete_ticket.is_valid():
                ticket.delete()
                return redirect('review:display_user_posts')
        # the all_posts variable is used in the template to add an active link in the nav
        context = {
            'delete_ticket': delete_ticket,
            'ticket': ticket,
            'all_posts': 'all_posts'
        }
        return render(request, 'review/delete_ticket.html', context)
    else:
        return redirect('review:home')
