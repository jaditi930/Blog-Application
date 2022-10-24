from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import RegisterUser
from .forms import RegisterUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

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
    user=authenticate(username=username,password=password)
    if user is not None:
        this_user=RegisterUser.objects.get(username=username)
        login(request,user)
        return render(request,"user_details.html",{"user":this_user})
    else:
        return redirect("/")
def logout_user(request):
    logout(request)
    return redirect("/")
def signup_user(request):
    new_form=RegisterUserForm(request.POST or None, request.FILES or None)
    form=new_form.save(commit=False)
    try:
        this_user=RegisterUser.objects.get(username=new_form.cleaned_data['username'])
        return redirect("/signin/")
    except:
        form.set_password(new_form.cleaned_data['password'])
        form.save()
        return render(request,"login.html")
