from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index),
    path('signin/',views.signin),
    path('signup_user/',views.signup_user),
    path('user/<str:username>/',views.logged_user),
    path('author/<str:username>/',views.logged_user),
    path('login_user/',views.log_user),
    path('user_authenticate/',views.authenticate_user),
    path('logout/',views.logout_user),
    path('user/<str:username>/profile/<str:user>',views.view_profile),
]
