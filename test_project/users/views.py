from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.

def loginUser(request):
    page = 'login'
    context = {'page':page}
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
            # Checking if the username with given username exists in database orr not

        except:
            messages.error(request,"Username not found")

        user = authenticate(request, username=username, password=password)
        # The above command checks if the credentials given for the existing user is correct or not.

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request,"Username or Password Incorrect...")

    return render(request, "users/login_register.html",context)


def logoutUser(request):
    logout(request)
    messages.success(request,"User Logged Out...")
    return redirect("login")

def signupUser(request):
    page = 'signup'
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("User Creation Initiated..")
            user = form.save(commit=False) # Here we hold a single instance of the form
            user.username = user.username.lower()
            print(user)
            user.save()
            messages.success(request,"User Account Created")

    context = {'page':page,'form':form}
    return render(request, "users/login_register.html", context)


def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles":profiles}
    return render(request, "users/profiles.html",context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topskills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")

    context = {'profile':profile,'topskills':topskills,"otherskills":otherskills}
    return render(request, "users/user-profile.html",context)
