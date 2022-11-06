from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('blog/',views.index),
    path('<int:id>/new_post/',views.new_post),
    path('<int:uid>/view_all/',views.view_all),
    path('<int:id>/new_post/save/',views.save),
    path('like_post/<int:post_id>/',views.like_post),
    path('unlike_post/<int:post_id>/',views.unlike_post),
    path('follow/add_author/<int:post_id>/<int:flag>/',views.add_follower),
    path('unfollow/<int:post_id>/<int:flag>/',views.unfollow),
    path('recommended_posts/',views.recom),
    path('post_details/<int:post_id>/',views.post_details),

]
