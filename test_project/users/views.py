from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from django.contrib.auth.models import User
from .models import Profile, Message
from .utils import searchProfiles, paginateProfiles

# Create your views here.

def loginUser(request):
    page = 'login'
    context = {'page':page}
    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
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
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request,"Username or Password Incorrect...")

    return render(request, "users/login_register.html",context)


def logoutUser(request):
    logout(request)
    messages.success(request,"User Logged Out...")
    return redirect("login")

def signupUser(request):
    page = 'signup'
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("User Creation Initiated..")
            user = form.save(commit=False) # Here we hold a single instance of the form
            user.username = user.username.lower()
            print(user)
            user.save()
            messages.success(request,"User Account Created")

            login(request, user)
            return redirect("edit-account")

    context = {'page':page,'form':form}
    return render(request, "users/login_register.html", context)


def profiles(request):
    profiles, search_query = searchProfiles(request) 
    custom_range, profiles =  paginateProfiles(request, profiles, 3)
    context = {"profiles":profiles,'search_query':search_query,'range':custom_range}
    return render(request, "users/profiles.html",context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topskills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")

    context = {'profile':profile,'topskills':topskills,"otherskills":otherskills}
    return render(request, "users/user-profile.html",context)

@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all().order_by('-description')
    projects = profile.project_set.all()

    context = {'profile':profile,'skills':skills,"projects":projects}
    return render(request,"users/account.html", context)

@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request,"Account Updated Successfully...")
            return redirect("account")

    context = {'form':form}
    return render(request,"users/profile_form.html",context)

@login_required(login_url="login")
def addSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,"New Skill Added")
            return redirect("account")
    
    context = {'form':form}
    return render(request,"users/skill_form.html",context)

@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,"Skill Updated Successfully")
            return redirect("account")
    
    context = {'form':form}
    return render(request,"users/skill_form.html",context)

@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request,"Skill Deleted Successfully")
        return redirect("account")
    
    context = {"object":skill}
    return render(request,"delete-template.html",context)

@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count() 
    context = {"messages":messageRequests,"unread":unreadCount}
    return render(request,"users/inbox.html", context)
