from django.urls import path
from . import views

app_name = 'review'
urlpatterns = [
    path('', views.home, name='home'),
    path('add_ticket/', views.add_ticket, name='add_ticket'),
    path('add_ticket/<int:ticket_id>', views.add_ticket, name='add_ticket'),
    path('follow_users_form/', views.follow_user, name='follow_users_form'),
    path('following_page/', views.display_followers, name='following_page'),
    path('stop_follow/<int:followed_id>', views.stop_follow, name="stop_follow"),
    path('add_review_ticket/', views.add_review, name="add_review_ticket"),
    path('add_review/<int:ticket_id>', views.add_review, name="add_review"),
    path('display_user_posts/', views.display_user_posts, name="display_user_posts"),
    path("edit_review/<int:review_id>", views.edit_review, name="edit_review"),
    path("delete_review/<int:review_id>", views.delete_review, name="delete_review"),
    path("delete_ticket/<int:ticket_id>", views.delete_ticket, name="delete_ticket")
]
