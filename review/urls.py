from django.urls import path
from . import views

app_name = 'review'
urlpatterns = [
    path('', views.home, name='home'),
    path('add_ticket/', views.add_ticket, name='add_ticket'),
    path('follow_users/', views.follow_user, name='follow_users'),
    path('following_page', views.display_followers, name='following_page')
]
