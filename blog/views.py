import json
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import blog
from login.models import RegisterUser
# Create your views here.
@login_required(login_url='/login_user/')
def index(request):
    all_posts=blog.objects.all()
    return render(request,"view_posts.html",{"posts":all_posts})

def new_post(request,id):
    new_post=PostForm()
    new_post.author=id
    return render(request,"create_post.html",{
        "form":new_post
    })

def view_all(request,id):
    all_posts=blog.objects.filter(is_draft=False and author==request.user)
    return render(request,"view_posts.html",{
        "posts":all_posts
    })
def save(request,id):
    new_post=PostForm(request.POST or None,request.FILES or None)
    if new_post.is_valid():
            post=new_post.save(commit=False)
            post.author=RegisterUser.objects.get(user_id=id)
            post.save()
            # print(post.author_id.id)
    return redirect("/blog/")

def like_post(request,post_id):
    like_post=blog.objects.get(id=post_id)
    print(like_post)
    if like_post.no_of_likes==0:
       like_post.liked_by_users+=f'"like-{like_post.no_of_likes+1}":"{request.user.id}"'
    else:
       like_post.liked_by_users+=f',"like-{like_post.no_of_likes+1}":"{request.user.id}"' 
    like_post.no_of_likes+=1
    like_post.save()
    print(like_post)
    return redirect("/blog/")