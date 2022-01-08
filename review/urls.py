from django.urls import path
from . import views

app_name = 'review'
urlpatterns = [
    path('', views.home, name='home'),
    path('add_ticket/', views.add_ticket, name='add_ticket'),
    path('follow_users/', views.follow_user, name='follow_users'),
    path('following_page/', views.display_followers, name='following_page'),
    path('stop_follow/<int:followed_id>', views.stop_follow, name="stop_follow"),
    path('add_review_ticket/', views.add_review, name="add_review_ticket"),
    path('add_review/<int:ticket_id>', views.add_review, name="add_review")
]
