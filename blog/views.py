import json
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import blog
from login.models import RegisterUser
from django.db.models import Q
from django.core.paginator import Paginator
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
def recom(request):
    page_num=request.GET.get('page',1)
    users=RegisterUser.objects.get(username=request.user.username)
    recom_posts=list()
    try:
        user_likes=json.loads(users.liked_posts)
        for key,value in user_likes.items():
            users=blog.objects.get(id=value)
            recom_posts.append(blog.objects.filter(author=users.author))
            recom_posts.append(blog.objects.filter(category=users.category))
        for i in range(len(recom_posts)/2,2):
           recom_posts=recom_posts[i]|recom_posts[i+1]
        print(recom_posts)
    except:
        recom_posts=blog.objects.all()
    p=Paginator(recom_posts,5)
    page=p.page(page_num)
    return render(request,"view_posts.html",{"posts":page,"flag":1})

@login_required(login_url='/login_user/')
def index(request):
    page_num=request.GET.get('page',1)
    try:
        key=request.GET.get('q')
        print(key)
        searches=blog.objects.filter(Q(author__username__icontains=key)|Q(category__icontains=key)|Q(title__icontains=key))
        p=Paginator(searches,5)
        page=p.page(page_num)
        return render(request,"view_posts.html",{"posts":page,"key":key})
    except:
        print("try failed")
        try:
            this_user=RegisterUser.objects.get(username=request.user.username)
            followers_list=json.loads(this_user.followers)
            follow_posts=list()
            for key,value in followers_list.items():
                try:
                    user=RegisterUser.objects.get(username=value)
                    follow_posts.append(blog.objects.filter(author=user))
                except:
                    follow_posts.append(blog.objects.filter(category=value))
            if len(follow_posts)>0:
                follow_posts=follow_posts[0]|follow_posts[1]
            print(follow_posts)
            p=Paginator(follow_posts,5)
            page=p.page(page_num)
        except:
            all_posts=blog.objects.get(author=request.user.username)
            p=Paginator(all_posts,5)
            page=p.page(page_num)
        return render(request,"view_posts.html",{"posts":page,"flag":0})
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
    like_user=RegisterUser.objects.get(username=request.user.username)
    try:
       liked=json.loads(like_post.liked_by_users)
    except:
       liked={}
    liked[f'like-{like_post.no_of_likes+1}']=f"{request.user.id}"
    like_post.no_of_likes+=1
    like_post.liked_by_users=json.dumps(liked)
    like_post.save()
    try:
        likeu=json.loads(like_user.liked_posts)
    except:
        likeu={}
    likeu[f'like-{len(likeu)}']=f'{post_id}'
    like_user.liked_posts=json.dumps(likeu)
    like_user.save()
    return redirect("/blog/")

def unlike_post(request,post_id):
    unlike_post=blog.objects.get(id=post_id)
    unlike_user=RegisterUser.objects.get(username=request.user.username)
    liked=json.loads(unlike_post.liked_by_users)
    likedu=json.loads(unlike_user.liked_posts)
    del liked[f'like-{request.user.id}']
    dp=str()
    for key,value in likedu.items():
        if int(value)==post_id:
            dp=key
            break
    del likedu[dp]
    unlike_post.liked_by_users=json.dumps(liked)
    unlike_user.liked_posts=json.dumps(likedu)
    unlike_post.no_of_likes-=1
    unlike_post.save()
    unlike_user.save()
    print(unlike_post)
    return redirect("/blog/")
