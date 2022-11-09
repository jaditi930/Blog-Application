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
    this_user=RegisterUser.objects.get(username=request.user.username)
    try:
        followers=json.loads(this_user.followers)
    except:
        followers={}
    if flag==0:
       followers[f"follower_{len(followers)+1}"]=blog.objects.get(id=post_id).author.username
    else:
       followers[f"category_{len(followers)+1}"]=blog.objects.get(id=post_id).category
    this_user.followers=json.dumps(followers)
    this_user.save()
    return redirect(f"/post_details/{post_id}")

def unfollow(request,post_id,flag):
    this_user=RegisterUser.objects.get(username=request.user.username)
    this_blog=blog.objects.get(id=post_id)
    followers=json.loads(this_user.followers)
    if flag==0:
        for i,j in enumerate(followers.keys()):
            if j.startswith("follower"):
                if followers[f"{j}"]==this_blog.author.username:
                    del followers[f"{j}"]
                    break
            else:
                if followers[f"{j}"]==this_blog.category:
                    del followers[f"{j}"]
                    break
    this_user.followers=json.dumps(followers)
    this_user.save()
    return redirect(f"/post_details/{post_id}")

def recom(request,username):
    page_num=request.GET.get('page',1)
    users=RegisterUser.objects.get(username=username)
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
    recom_posts.order_by('no_of_likes')
    p=Paginator(recom_posts,3)
    page=p.page(page_num)
    return render(request,"view_posts.html",{"posts":page,"flag":1,"user":users})

def liked_posts(request,username):
    try:
        user=RegisterUser.objects.get(username=username)
        liked=json.loads(user.liked_posts)
        print(liked)
        liked_posts=[]
        for posts in liked.keys():
           liked_blog=blog.objects.get(id=int(liked[f"{posts}"]))
           print(liked_blog.category)
           liked_posts.append(liked_blog)
        print(liked_posts)
    except:
        liked_posts={}
    return render(request,"view_posts.html",{"posts":liked_posts})

@login_required(login_url='/login_user/')
def index(request,username):
    user=RegisterUser.objects.get(username=username)
    print(user.profile_picture)
    page_num=request.GET.get('page',1)
    try:
        key=request.GET.get('q')
        searches=blog.objects.filter(Q(author__username__icontains=key)|Q(category__icontains=key)|Q(title__icontains=key)).order_by('no_of_likes')
        p=Paginator(searches,3)
        page=p.page(page_num)
        return render(request,"view_posts.html",{"posts":page,"key":key,"user":user})
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
            if len(follow_posts)>1:
                follow_posts=follow_posts[0]|follow_posts[1]
            follow_posts.order_by('no_of_likes')
            print(follow_posts)
            p=Paginator(follow_posts,3)
            page=p.page(page_num)
        except:
            print("another try failed")
            all_posts=blog.objects.filter(author__username=request.user.username).order_by('no_of_likes')
            p=Paginator(all_posts,3)
            page=p.page(page_num)
        return render(request,"view_posts.html",{"posts":page,"flag":0,"user":user})
def new_post(request,username):
    new_post=PostForm()
    return render(request,"create_post.html",{
        "form":new_post
    })

def post_details(request,username,post_id):
    post=blog.objects.get(id=post_id)
    users=RegisterUser.objects.get(username=username)
    if users.role=="Patient":
        try:
            liked=json.loads(users.liked_posts)
            flag=0
            for l in liked:
                if liked[l]==str(post_id):
                    flag=1
        except:
            flag=0
        author=0
        category=0
        follow_a=json.loads(users.followers)
        print(follow_a)
        for i,j in enumerate(follow_a.keys()):
            if j.startswith("follower"):
                if follow_a[f"{j}"]==post.author.username:
                    author=1
            else:
                if follow_a[f"{j}"]==post.category:
                    category=1
        print(author,category)
        return render(request,"post_details.html",{"post":post,"role":1,"liked":flag,"author":author,"category":category})
    else:
        return render(request,"post_details.html",{"post":post,"role":0})

def view_my_posts(request,username):
    t_user=RegisterUser.objects.get(username=username)
    all_posts=blog.objects.filter(is_draft=False).filter(author=t_user)
    return render(request,"view_posts.html",{
        "posts":all_posts
    })


def save(request,post_id):
    new_post=PostForm(request.POST or None,request.FILES or None)
    i_id=str()
    if new_post.is_valid():
        try:
            exis_post=blog.objects.get(id=post_id)
            exis_post.delete()
            new_post.save()
            i_id=new_post.author.username
        except:
            post=new_post.save(commit=False)
            post.author=RegisterUser.objects.get(username=request.user.username)
            post.save()
        i_id=post.author.username
    else:
        print("create failed")
    return redirect(f"/{i_id}/view_my_posts/")

def like_post(request,post_id):
    like_post=blog.objects.get(id=post_id)
    like_user=RegisterUser.objects.get(username=request.user.username)
    try:
       liked=json.loads(like_post.liked_by_users)
    except:
       liked={}
    liked[f'like-{request.user.id}']=f"{request.user.id}"
    like_post.no_of_likes+=1
    like_post.liked_by_users=json.dumps(liked)
    like_post.save()
    try:
        likeu=json.loads(like_user.liked_posts)
    except:
        likeu={}
    likeu[f'like-{post_id}']=f'{post_id}'
    like_user.liked_posts=json.dumps(likeu)
    like_user.save()
    return redirect(f"/post_details/{post_id}/")

def unlike_post(request,post_id):
    unlike_post=blog.objects.get(id=post_id)
    unlike_user=RegisterUser.objects.get(username=request.user.username)
    liked=json.loads(unlike_post.liked_by_users)
    print(liked)
    del liked[f'like-{request.user.id}']
    likedu=json.loads(unlike_user.liked_posts)
    print(likedu)
    del likedu[f'like-{post_id}']
    unlike_post.liked_by_users=json.dumps(liked)
    unlike_user.liked_posts=json.dumps(likedu)
    unlike_post.no_of_likes-=1
    unlike_post.save()
    unlike_user.save()
    print(unlike_post)
    return redirect(f"/post_details/{post_id}/")


def edit_post(request,post_id):
    post=blog.objects.get(id=post_id)
    edit_post_form=PostForm(instance=post)
    return render(request,"create_post.html",{"form":edit_post_form,"post_id":post_id})

def view_drafts(request,username):
    user_drafts=blog.objects.filter(author__username=username)&blog.objects.filter(is_draft=True)
    return render(request,"view_posts.html",{"posts":user_drafts})
