<p align="justify">

# Creating Account Page

- In order to create the account page, we need to first get a templte reqdy to be used. So, with the `users` app, in the templates we create a template for the same.

  `account.html` - `users` app

  ```Jinja
    {% extends 'main.html' %}
    {% load static %}
    {% block content %}
    <!-- Main Section -->
    <main class="settingsPage profile my-md">
        <div class="container">
        <div class="layout">
            <div class="column column--1of3">
            <div class="card text-center">
                <div class="card__body dev">
                <a class="tag tag--pill tag--main settings__btn" href="{% url 'edit-account' %}"><i class="im im-edit"></i> Edit</a>
                <img class="avatar avatar--xl dev__avatar" src="{{ profile.profile_image.url }}" />
                <h2 class="dev__name">{{profile.name}}</h2>
                <p class="dev__title">{{profile.short_intro}}</p>
                <p class="dev__location">Based in {{profile.location}}</p>
                <ul class="dev__social">
                    <li>
                    <a title="Github" href="{{profile.social_github}}" target="_blank"><i class="fa-brands fa-github"></i></a>
                    </li>
                    <li>
                    <a title="Twitter" href="{{profile.social_twitter}}" target="_blank"><i class="fa-brands fa-twitter"></i></a>
                    </li>
                    <li>
                    <a title="LinkedIn" href="{{profile.social_linkedin}}" target="_blank"><i class="fa-brands fa-linkedin"></i></a>
                    </li>
                    <li>
                    <a title="Personal Website" href="{{profile.social_website}}" target="_blank"><i class="fa-solid fa-link"></i></a>
                    </li>
                </ul>
                <a href="#" class="btn btn--sub btn--lg">Send Message </a>
                </div>
            </div>
            </div>
            <div class="column column--2of3">
            <div class="devInfo">
                <h3 class="devInfo__title">About Me</h3>
                <p class="devInfo__about">
                {{profile.bio}}
                </p>
            </div>
            <div class="settings">
                <h3 class="settings__title">Skills</h3>
                <a class="tag tag--pill tag--sub settings__btn tag--lg" href="{% url 'add-skill' %}"><i class="im im-plus"></i> Add Skill</a>
            </div>

            <table class="settings__table">
                {% for skill in skills %}
                <tr>
                <td class="settings__tableInfo">
                    <h4>{{skill.name}}</h4>
                    <p>
                    {{skill.description}}
                    </p>
                </td>
                <td class="settings__tableActions">
                    <a class="tag tag--pill tag--main settings__btn" href="{% url 'update-skill' skill.id %}"><i class="im im-edit"></i> Edit</a>
                    <a class="tag tag--pill tag--main settings__btn" href="{% url 'delete-skill' skill.id %}"><i class="im im-x-mark-circle-o"></i>
                    Delete</a>
                </td>
                </tr>
                {% endfor %}
            </table>

            <div class="settings">
                <h3 class="settings__title">Projects</h3>
                <a class="tag tag--pill tag--sub settings__btn tag--lg" href="{% url 'create-project' %}"><i class="im im-plus"></i> Add Project</a>
            </div>

            <table class="settings__table">
                {% for project in projects %}
                <tr>
                <td class="settings__thumbnail">
                    <a href="{% url 'project' project.id %}"><img src="{{project.featured_image.url}}" alt="Project Thumbnail" /></a>
                </td>
                <td class="settings__tableInfo">
                    <a href="{% url 'project' project.id %}">{{project.title}}</a>
                    <p>
                    {{project.description|slice:"150"}}
                    </p>
                </td>
                <td class="settings__tableActions">
                    <a class="tag tag--pill tag--main settings__btn" href="{% url 'update-project' project.id %}"><i class="im im-edit"></i> Edit</a>
                    <a class="tag tag--pill tag--main settings__btn" href="{% url 'delete-project' project.id %}?next=/account"><i class="im im-x-mark-circle-o"></i>
                    Delete</a>
                </td>
                </tr>
                {% endfor %}
            </table>
            </div>
        </div>
        </div>
    </main>
    {% endblock content %}
  ```

- Once the template is ready, just go to `views.py` aand `urls.py` for the `users` app.

    `views.py` - `users` app

    ```python
    from django.shortcuts import redirect, render
    from django.contrib.auth import login, authenticate, logout
    from django.contrib.auth.decorators import login_required
    from django.contrib import messages
    from .forms import CustomUserCreationForm, ProfileForm, SkillForm
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
        profiles = Profile.objects.all()
        context = {"profiles":profiles}
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
    ```

    `urls.py` - `users` app

    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("signup/", views.signupUser, name="signup"),

    path("", views.profiles, name="profiles"),
    path("profile/<str:pk>/", views.userProfile, name="user-profile"),
    
    path("account/", views.userAccount, name="account"),
    path("edit-account/", views.editAccount, name="edit-account"),

    path("add-skill/",views.addSkill, name="add-skill"),
    path("update-skill/<str:pk>/",views.updateSkill, name="update-skill"),
    path("delete-skill/<str:pk>/",views.deleteSkill, name="delete-skill"),
    ]
    ```

- Make some small change to the `navbar.html` in the `root` template.

    `navabar.html` - `root` template

    ```Jinja
    {% load static %}

    <!-- Header Section -->
    <header class="header">
        <div class="container container--narrow">
        <a href="{% url 'projects' %}" class="header__logo">
            <img  class="logo" src = "{% static "images/logo.svg" %}"/>
        </a>
        <nav class="header__nav">
            <input type="checkbox" id="responsive-menu" />
            <label for="responsive-menu" class="toggle-menu">
            <span>Menu</span>
            <div class="toggle-menu__lines"></div>
            </label>
            <ul class="header__menu">
            <li class="header__menuItem"><a href="{% url "profiles" %}">Developers</a></li>
            <li class="header__menuItem"><a href="{% url "projects" %}">Projects</a></li>

            {% if request.user.is_authenticated %}
            <li class="header__menuItem"><a href="">Inbox</a></li>
            <li class="header__menuItem"><a href="{% url 'account' %}">My Account</a></li>
            <li class="header__menuItem"><a href="{% url 'create-project' %}" class="btn btn--sub">Add Projects</a></li>
            <li class="header__menuItem"><a href="{% url 'logout' %}" class="btn btn--sub"><i class="fa-regular fa-right-from-bracket"></i> Logout</a></li>
            {% else %}
            <li class="header__menuItem"><a href="{% url 'login' %}" class="btn btn--sub">Login/SignUp</a></li>
            {% endif %}
            </ul>
        </nav>
        </div>
    </header>
    ```

- Add Signals for account details updation in `signals.py` in `users` app.

    `signals.py` - `users` app

    ```python
    # Imports for the Signals
    from django.db.models.signals import post_save, post_delete
    from django.dispatch import receiver
    from django.contrib.auth.models import User
    from .models import Profile


    def createProfile(sender, instance, created, **kwargs):
        if created:
            user = instance
            profile = Profile.objects.create(user=user, username=user.username, email=user.email, name=user.first_name)
        print("Profile Saved Succesfully... ")

    def updateProfile(sender, instance, created, **kwargs):
        profile = instance
        user = profile.user

        if created == False:
            user.first_name = profile.name
            user.username = profile.username
            user.email = profile.email
            user.save()
        print("Profile Updated...")

    def profileDeleted(sender, instance, **kwargs):
        user = instance.user
        user.delete()
        print("Profile Deleted...")

    post_save.connect(createProfile, sender=User)
    post_save.connect(updateProfile, sender=Profile)
    post_delete.connect(profileDeleted, sender=Profile)
    ```

- In `forms.py` for the `users` app, define the field details and classes for the input fields for the Profile and Skill as `ProfileForm` and `SkillForm`.

    `forms.py` - `users` app

    ```python
    from django.forms import ModelForm, TextInput, URLInput
    from django.contrib.auth.forms import UserCreationForm
    from django.contrib.auth.models import User
    from .models import Profile, Skill



    class CustomUserCreationForm(UserCreationForm):
        class Meta:
            model = User
            fields = ['first_name','email','username','password1','password2']
            labels = {
                "first_name":"Name",
            }

        def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({"class":"input"})

    class ProfileForm(ModelForm):
        class Meta:
            model = Profile
            fields = ['name', 'email', 'username',
                    'location', 'bio', 'short_intro', 'profile_image',
                    'social_github', 'social_linkedin', 'social_twitter','social_website']

        def __init__(self, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})

    class SkillForm(ModelForm):
        class Meta:
            model = Skill
            fields = '__all__'
            exclude = ["owner"]

        def __init__(self, *args, **kwargs):
            super(SkillForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})
            
    ```

- Now define the template form for the `ProfileForm` and `SkilForm`.

    `profile_form.html` - `template` `users` app

    ```Jinja
    {% extends 'main.html' %}
    {% load static %}
    {% block content %}


    <!-- Main Section -->
    <main class="formPage my-xl">
        <div class="content-box">
            <div class="formWrapper">
                <a class="backButton" href="{% url 'account' %}"><i class="fa-solid fa-arrow-left"></i></a>
                <br>

                <form class="form" method="POST" action="{% url 'edit-account' %}" enctype="multipart/form-data">
                    {% csrf_token %}
                    {% for field in form %}
                    <div class="form__field">
                        <label for="formInput#text">{{field.label}}</label>
                        {{field}}
                    </div>
                    {% endfor %}
                    <input class="btn btn--sub btn--lg  my-md" type="submit" value="Submit" />
                </form>
            </div>
        </div>
    </main>

    {% endblock content %}
    ```

    `skill_form.html` - `templates` - `users` app

    ```Jinja
    {% extends 'main.html' %}

    {% block content %}


    <!-- Main Section -->
    <main class="formPage my-xl">
        <div class="content-box">
            <div class="formWrapper">
                <a class="backButton" href="{% url 'account' %}"><i class="im im-angle-left"></i></a>
                <br>

                <form class="form" method="POST" action="">
                    {% csrf_token %}

                    {% for field in form %}
                    <div class="form__field">
                        <label for="formInput#text"> {{field.label}}</label>
                        {{field}}
                    </div>
                    {% endfor %}

                    <input class="btn btn--sub btn--lg  my-md" type="submit" value="Submit" />
                </form>
            </div>
        </div>
    </main>
    {% endblock %}
    ```


</p>