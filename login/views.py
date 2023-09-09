from django.shortcuts import render,redirect
from .models import RegisterUser
from blog.models import blog
from .forms import RegisterUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import json
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        this_user=RegisterUser.objects.get(username=request.user.username)
    elif request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        # print(username,password)
        this_user=RegisterUser.objects.get(username=username)
        # print(this_user)
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
        else:
            return render(request,"login.html")
    else:
        return render(request,"login.html")
        
    try:
        followers=json.loads(this_user.followers)
        posts_1=list()
        posts_2=list()
        for f in followers:
            if f.startswith("follower"):
                author=RegisterUser.objects.get(username=followers[f])
                posts_1=blog.objects.filter(author=author)
            else:
                posts_2=blog.objects.filter(category=followers[f])
        posts=posts_1.union(posts_2)
        print(posts)
        return render(request,"view_posts.html",{
            "posts":posts,
            "flag":0,
        })
    except:
        posts=blog.objects.filter(author=this_user)
        print(posts)
        return render(request,"view_posts.html",{"posts":posts,"flag":1})

def signin(request):
    form=RegisterUserForm()
    return render(request,"sign_in.html",{"form":form})
def log_user(request):
    return render(request,"login.html")

def view_profile(request,username):
    user=RegisterUser.objects.get(username=username)
    role=user.role
    print(username)
    if user.username!=request.user.username:
        posts=blog.objects.filter(author=user)
        return render(request,"view_profile.html",{"user":user,"posts":posts})
    else:
        follower=list()
        category=list()
        try:
            followers=json.loads(user.followers)
            for f in followers:
                if f.startswith("follower"):
                    follower.append(followers[f])
                else:
                    category.append(followers[f])
        except:
            pass
        
        return render(request,"user_details.html",{"currentuser_role":role,"user":user,"followers":follower,"category":category})


def logout_user(request):
    logout(request)
    return redirect("/")

def signup_user(request):
    print(request.POST)
    new_form=RegisterUserForm(request.POST or None, request.FILES or None)
    form=new_form.save(commit=False)
    try:
        this_user=RegisterUser.objects.filter(username=new_form.cleaned_data['username']).first()
        this_user.password=new_form.cleaned_data['password']
        return redirect("/signin/")
    except:
        form.set_password(new_form.cleaned_data['password'])
        form.save()
        return render(request,"login.html")




