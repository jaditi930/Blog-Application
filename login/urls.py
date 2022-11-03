from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index),
    path('signin/',views.signin),
    path('signup_user/',views.signup_user),
    path('logged_user/',views.logged_user),
    path('login_user/',views.log_user),
    path('user_authenticate/',views.authenticate_user),
    path('logout/',views.logout_user),
]
