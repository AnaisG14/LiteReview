from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name="signup"),
]
