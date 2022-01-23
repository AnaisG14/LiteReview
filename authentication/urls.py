from django.urls import path
from . import views

# urls for the part of authentication of the application
app_name = 'authentication'
urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name="signup"),
]
