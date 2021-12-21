from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
