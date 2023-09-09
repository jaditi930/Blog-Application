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

def recom(request):
    print("reached")
    users=RegisterUser.objects.get(username=request.user.username)
    if users.role=="User":
        flag=0
    else:
        flag=1
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
        recom_posts=blog.objects.filter().order_by('no_of_likes')
    return render(request,"view_posts.html",{"posts":recom_posts,"flag":flag,"user":users})

def liked_posts(request):
    try:
        user=RegisterUser.objects.get(username=request.user.username)
        liked=json.loads(user.liked_posts)
        # print(liked)
        liked_posts=[]
        for posts in liked.keys():
           liked_blog=blog.objects.get(id=int(liked[f"{posts}"]))
           print(liked_blog.category)
           liked_posts.append(liked_blog)
        print(liked_posts)
    except:
        liked_posts={}
    return render(request,"view_posts.html",{"posts":liked_posts,"flag":0})

@login_required(login_url="/")
def new_post(request):
    user_role=RegisterUser.objects.get(username=request.user.username).role
    if user_role == "Author":
        new_post=PostForm()
        print(new_post)
        return render(request,"create_post.html",{
            "form":new_post
        })
    else:
        return HttpResponse("Switch to Author account for writig blogs with us.")

def post_details(request,title,post_id):
    post=blog.objects.get(id=post_id)
    users=RegisterUser.objects.get(username=request.user.username)
    if users.role=="User":
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
        try:
            follow_a=json.loads(users.followers)
            for i,j in enumerate(follow_a.keys()):
                if j.startswith("follower"):
                    if follow_a[f"{j}"]==post.author.username:
                        author=1
                else:
                    if follow_a[f"{j}"]==post.category:
                        category=1
        except:
            pass
        return render(request,"post_details.html",{"post":post,"role":1,"liked":flag,"author":author,"category":category})
    else:
        return render(request,"post_details.html",{"post":post,"role":0})


def save(request,post_id):
    new_post=PostForm(request.POST or None,request.FILES or None)
    if new_post.is_valid():
        post=new_post.save(commit=False)
        post.author=RegisterUser.objects.get(username=request.user.username)
        post.save()
        old_post=blog.objects.get(id=post_id)
        old_post.delete()
    return redirect("/")

@login_required(login_url="/")
def edit_post(request,post_id):
    post=blog.objects.get(id=post_id)
    edit_post_form=PostForm(instance=post)
    return render(request,"create_post.html",{"form":edit_post_form,"post_id":post_id})


@login_required(login_url="/")
def view_drafts(request,username):
    user_drafts=blog.objects.filter(author__username=username)&blog.objects.filter(is_draft=True)
    return render(request,"view_posts.html",{"posts":user_drafts})






@login_required(login_url="/")
def like_post(request,post_id):
    like_post=blog.objects.get(id=post_id)
    post_title=like_post.title
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
    return redirect(f"/{post_title}/{post_id}/")

@login_required(login_url="/")
def unlike_post(request,post_id):
    unlike_post=blog.objects.get(id=post_id)
    post_title=unlike_post.title
    unlike_user=RegisterUser.objects.get(username=request.user.username)
    liked=json.loads(unlike_post.liked_by_users)
    del liked[f'like-{request.user.id}']
    likedu=json.loads(unlike_user.liked_posts)
    del likedu[f'like-{post_id}']
    unlike_post.liked_by_users=json.dumps(liked)
    unlike_user.liked_posts=json.dumps(likedu)
    unlike_post.no_of_likes-=1
    unlike_post.save()
    unlike_user.save()
    return redirect(f"/{post_title}/{post_id}/")

@login_required(login_url="/")
def follow(request,post_id,flag):
    this_user=RegisterUser.objects.get(username=request.user.username)
    post_title=blog.objects.get(id=post_id).title
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
    return redirect(f"/{post_title}/{post_id}")

@login_required(login_url="/")
def unfollow(request,post_id,flag):
    this_user=RegisterUser.objects.get(username=request.user.username)
    this_blog=blog.objects.get(id=post_id)
    post_title=this_blog.title
    followers=json.loads(this_user.followers)
    # if flag==0:
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
    return redirect(f"/{post_title}/{post_id}")
