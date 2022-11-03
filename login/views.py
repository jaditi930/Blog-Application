from django.shortcuts import render,redirect
from .models import RegisterUser
from .forms import RegisterUserForm
from django.contrib.auth import authenticate,login,logout
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
        login(request,user)
        return redirect("/logged_user/")
    else:
        return redirect("/")

def logged_user(request):
    if request.user.is_authenticated:
        this_user=RegisterUser.objects.get(username=request.user)
        return render(request,"user_details.html",{
            "user":this_user
        })
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
