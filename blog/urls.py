from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('new_post/',views.new_post),
    path('save/<int:post_id>',views.save),

    path('like_post/<int:post_id>/',views.like_post),
    path('unlike_post/<int:post_id>/',views.unlike_post),

    path('follow/<int:post_id>/<int:flag>/',views.follow),
    path('unfollow/<int:post_id>/<int:flag>/',views.unfollow),
    
    path('discover',views.recom),
    path('edit_post/<int:post_id>/',views.edit_post),

    path('<str:title>/<int:post_id>/',views.post_details),
    
    path('liked_posts/',views.liked_posts),
    path('drafts/',views.view_drafts),

]

