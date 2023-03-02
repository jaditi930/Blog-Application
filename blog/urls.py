from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('user/<str:username>/blog/',views.index),
    path('author/<str:username>/new_post/',views.new_post),
    path('author/<str:username>/view_my_posts/',views.view_my_posts),
    path('save/',views.save),
    path('like_post/<int:post_id>/',views.like_post),
    path('unlike_post/<int:post_id>/',views.unlike_post),
    path('follow/add_author/<int:post_id>/<int:flag>/',views.add_follower),
    path('unfollow/<int:post_id>/<int:flag>/',views.unfollow),
    path('user/<str:username>/recommended_posts/',views.recom),
    path('user/<str:username>/post_details/<int:post_id>/',views.post_details),
    path('author/<str:username>/post_details/<int:post_id>/',views.post_details),
    path('edit_post/<int:post_id>/',views.edit_post),
    path('user/<str:username>/liked_posts/',views.liked_posts),
    path('author/<str:username>/drafts/',views.view_drafts),
    path('user/<str:username>/view_posts/<str:user>',views.view_posts),

]
