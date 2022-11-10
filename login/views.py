from django.shortcuts import render,redirect
from .models import RegisterUser
from .forms import RegisterUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import json
# Create your views here.
def index(request):
    return render(request,"index.html")
def signin(request):
    form=RegisterUserForm()
    return render(request,"sign_in.html",{"form":form})
def log_user(request):
    return render(request,"login.html")

def authenticate_user(request):
    username=request.POST["name"]
    password=request.POST["password"]
    this_user=RegisterUser.objects.get(username=username)
    user=authenticate(username=username,password=password)
    if user is not None:
        login(request,user)
        if(this_user.role=="User"):
           print("hello")
           return redirect(f"/user/{username}/")
        else:
            return redirect(f"/author/{username}/")
    else:
        messages.error(request,"User does not exist")
        return redirect("/login_user/")
def view_profile(request,username,user):
    user=RegisterUser.objects.get(username=user)
    print(username)
    return render(request,"view_profile.html",{"user":user})
def logged_user(request,username):
    if request.user.is_authenticated:
        this_user=RegisterUser.objects.get(username=request.user)
        try:
            followers=json.loads(this_user.followers)
            fol_1=list()
            fol_2=list()
            for f in followers:
                if f.startswith("follower"):
                   fol_1.append(followers[f'{f}'])
                else:
                    fol_2.append(followers[f'{f}'])
            return render(request,"user_details.html",{
                "user":this_user,
                "followers":fol_1,
                "category":fol_2,
            })
        except:
            return render(request,"user_details.html",{"user":this_user})
    else :
        return redirect("/login_user/")


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




