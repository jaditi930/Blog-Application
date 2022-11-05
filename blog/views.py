import json
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import blog
from login.models import RegisterUser
# Create your views here.
def add_follower(request,post_id,flag):
    print(request.user.username)
    this_user=RegisterUser.objects.get(username=request.user.username)
    try:
        followers=json.loads(this_user.followers)
    except:
        followers={}
    if flag==0:
       followers[f"follower-{len(followers)+1}"]=blog.objects.get(id=post_id).author.username
    else:
       followers[f"follower-{len(followers)+1}"]=blog.objects.get(id=post_id).category
    this_user.followers=json.dumps(followers)
    this_user.save()
    return redirect("/blog")
@login_required(login_url='/login_user/')
def index(request):
    try:
        this_user=RegisterUser.objects.get(username=request.user.username)
        followers_list=json.loads(this_user.followers)
        follow_posts=list()
        for key,value in followers_list.items():
            print(value)
            try:
                user=RegisterUser.objects.get(username=value)
                follow_posts.append(blog.objects.filter(author=user))
            except:
                follow_posts.append(blog.objects.filter(category=value))
        if len(follow_posts)>0:
            follow_posts=follow_posts[0]|follow_posts[1]
        print(follow_posts)
        return render(request,"view_posts.html",{"posts":follow_posts})
    except:
        all_posts=blog.objects.get(author=request.user.username)
        return render(request,"view_posts.html",{"posts":all_posts})

def new_post(request,id):
    new_post=PostForm()
    return render(request,"create_post.html",{
        "form":new_post
    })


def view_all(request,user):
    t_user=RegisterUser.objects.get(username=user)
    all_posts=blog.objects.filter(is_draft=False).filter(author=t_user)
    return render(request,"view_posts.html",{
        "posts":all_posts
    })
def save(request,id):
    new_post=PostForm(request.POST or None,request.FILES or None)
    i_id=int()
    if new_post.is_valid():
        post=new_post.save(commit=False)
        post.author=RegisterUser.objects.get(username=request.user.username)
        print(post.author.username)
        i_id=post.author
        print(post.author)
        post.save()
    return redirect(f"/{i_id}/view_all/")

def like_post(request,post_id):
    like_post=blog.objects.get(id=post_id)
    try:
       liked=json.loads(like_post.liked_by_users)
    except:
       liked={}
    liked[f'like-{like_post.no_of_likes+1}']=f"{request.user.id}"
    like_post.no_of_likes+=1
    like_post.liked_by_users=json.dumps(liked)
    like_post.save()
    return redirect("/blog/")

def unlike_post(request,post_id):
    unlike_post=blog.objects.get(id=post_id)
    liked=json.loads(unlike_post.liked_by_users)
    del liked[f'like-{request.user.id}']
    unlike_post.liked_by_users=json.dumps(liked)
    unlike_post.no_of_likes-=1
    unlike_post.save()
    print(unlike_post)
    return redirect("/blog/")
