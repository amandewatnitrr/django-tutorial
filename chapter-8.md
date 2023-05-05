<strong>
<p align="justify">

# Auhthentication

- So, now we have most of the stuff ready, we wil start off with desigining template for user login and logout page and Flash Messages. Also, we will add some restrictions, so that authourized users can only access this pages. We want certaing pages to be only accessible by the admin only. But, before that we must know the difference b/w authourization and authentication.

<table align="center">
    <tr>
        <th align="center"> Authentication </th>
        <th align="center"> Authourization </th>
    </tr>
    <tr>
        <td> Confirms who you are </td>
        <td> Grants on denies you permission to certain resources </td>
    </tr>
    <tr>
        <td> Authentication is nothing just a form to verify that someone is user of the website </td>
        <td> Authourization defines what users are allowed to do on the website </td>
    </tr>
</table>

- So, when we ran our migrations initially, there were few tables created for us overe here. One of those was a table called sessions. And this table stores user sessions. So, django uses sessions by default. So, if you move onto admin panel and go to inspect -> storage -> cookies. You would see your `sessionid` there.

  ![](/imgs/Screenshot%202023-04-29%20at%2010.45.30%20AM.png)

- Let's first start with the login page template here.

  `login_register.html` - `users` app

  ```Jinja
    {% extends 'main.html' %}

    {% block content %}
    <div class="auth">
        <div class="card">
        <div class="auth__header text-center">
            <a href="/">
            <img class="logo" src="../../../static/images/icon.svg" alt="icon" />
            </a>
            <h3>Account Login</h3>
            <p>Hello Developer, Welcome Back!</p>
        </div>

        <form action="{% url 'login' %}" method="POST" class="form auth__form">
        {% csrf_token %}
            <!-- Input:Email -->
            <div class="form__field">
            <label for="formInput#text">Username: </label>
            <input
                class="input input--text"
                id="formInput#text"
                type="text"
                name="username"
                placeholder="Enter your username..."
            />
            </div>

            <!-- Input:Password -->
            <div class="form__field">
            <label for="formInput#password">Password: </label>
            <input
                class="input input--password"
                id="formInput#passowrd"
                type="password"
                name="password"
                placeholder="••••••••"
            />
            </div>
            <div class="auth__actions">
            <input class="btn btn--sub btn--lg" type="submit" value="Login" />
            <a href="forgetpassword.html">Forget Password?</a>
            </div>
        </form>
        <div class="auth__alternative">
            <p>Don’t have an Account?</p>
            <a href="signup.html">Sign Up</a>
        </div>
        </div>
    </div>
    </body>

    {% endblock content %}
  ```

  Along with this, we have done a couple of changes in `root` and `projects` templates as well.

  `main.html` - `root`

  ```Jinja
    <!DOCTYPE html>
    {% load static %}
    <html>

    <head>
        <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <!-- Favicon -->
    <link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon" />
    <!-- Mumble UI -->
    <link rel="stylesheet" href="{% static 'uikit/styles/uikit.css' %}" />
    <!-- Dev Search UI -->
    <link rel="stylesheet" href="{% static 'css/app.css' %}" />
    <!-- Font Awesome Icons -->
    <script src="https://kit.fontawesome.com/c79118cca6.js" crossorigin="anonymous"></script>
    <link href="{% static 'fontawesomefree/css/fontawesome.css' %}" rel="stylesheet" type="text/css">
    <link href="{% static 'fontawesomefree/css/brands.css' %}" rel="stylesheet" type="text/css">
    <link href="{% static 'fontawesomefree/css/solid.css' %}" rel="stylesheet" type="text/css">

    <title>DevSearch - Connect with Developers!</title>

    </head>

    <body>
        {% include 'navbar.html' %}
        {% if messages %}
        <ul class="messages">
            {% for message in messages %}
            <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
            {% endfor %}
        </ul>
        {% endif %}
        <hr>


        {% block content %}

        {% endblock content %}
        <hr>
        <p>FOOTER</p>
    </body>
    <script src="{% static 'uikit/app.js' %}"></script>
    <script src="{% static 'js/main.js' %}"></script>

    </html>
  ```

  In the `main.html` we have added a section for the messages just below the navbar, so that we can view any message generated over there.

  `navbar.html` - `root`

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
            <li class="header__menuItem"><a href="">My Account</a></li>
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

  In `navbar.html`, we have added links to login page, and also added authourization for certain pages, such as Inbox, My Account, Add Project, Update Project and Delete Project should only be visible to a logged in user. If, the user is not looged in it can only view projects and developers and will get the option to Sign In.

  For `views.py` - `projects` app, we have made those changes by adding decorators, such that only after login the uuser will get the option to Add, Update or Delete Project.

  `views.py` - `projects` app

  ```python
    from django.shortcuts import render, redirect
    from django.http import HttpResponse
    from .models import Project, Review, Tag
    from django.contrib.auth.decorators import login_required
    from .forms import ProjectForm


    def projects(request):
        # return HttpResponse("Here are our Projects")
        # The above statement gives the specified Argument as an HTTpResponse.
        projects = Project.objects.all()
        context = {"projects": projects}
        return render(request, "projects/projects.html", context)

    def project(request, pk):
        projects = Project.objects.all()
        projectObj = Project.objects.get(id=pk)
        tags = projectObj.tags.all()
        context = {"project": projectObj,"tags":tags}
        return render(request, "projects/single-project.html",context)

    @login_required(login_url="login")
    def createProject(request):
        form = ProjectForm
        
        if request.method == "POST":
            form = ProjectForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                print(request.POST)
                return redirect("projects")

        context = {'form':form}
        return render(request, "projects/project_form.html", context)

    @login_required(login_url="login")
    def updateProject(request,pk):
        project = Project.objects.get(id=pk)
        form = ProjectForm(instance=project)
        # We are calling a instance of form that is prefilled with the instance of the project we want to edit
        
        if request.method == "POST":
            form = ProjectForm(request.POST,request.FILES,instance=project)
            if form.is_valid():
                form.save()
                print(request.POST)
                return redirect("projects")

        context = {'form':form}
        return render(request, "projects/project_form.html", context)

    @login_required(login_url="login")
    def deleteProject(request,pk):
        project = Project.objects.get(id=pk)
        if request.method == "POST":
            project.delete()
            return redirect("projects")
        context = {"object":project}
        return render(request, "projects/delete_template.html", context)
  ```

  `@login_required(login_url="login")` added at the top of specific function indicate that the feature would be made available to the user, after the user has logged in. This is called a decorator.

  `views.py` - `users` app

  ```python
    from django.shortcuts import redirect, render
    from django.contrib.auth import login, authenticate, logout
    from django.contrib.auth.decorators import login_required
    from django.contrib import messages
    from django.contrib.auth.models import User
    from .models import Profile

    # Create your views here.

    def loginUser(request):

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

        return render(request, "users/login_register.html")


    def logoutUser(request):
        logout(request)
        messages.success(request,"User Logged Out...")
        return redirect("login")


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

  ```

  Now, this is the code we need to study in order to understand things as a lot of things are happening here. We have already covered up thing srelated to `userProfile` and `profiles` in `chapter-6.md`. You can go back if you haven't checked on it yet.
  
  Let's first discuss about `loginUser`. So, if the user is authenticated, the user is redirected to the `profiles` page. If not so, than we move to the next step, where we first check if the username entered in the form exist in the database or notusing `try & except`. If the `username` is not present in the database, the error message is shown if the username is not present. If the `username` is present in the database, we go ahead to the next step to `authenticate` where we pass the arguments `username` and `password`. If the, user is None, this means that the password enter is not for the given username, or the password entered is incorrect. If everything goes fine, the `login` function redirects user to `profiles` page.

  Now, with the `logoutUser`, we just need to send call `logout` function, passing the request as the parameter and the user is logged out.
  
  We now add the urls for the `loginUser` and `logoutUser` finally.

  `urls.py` - `users` app

  ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path("login/", views.loginUser, name="login"),
        path("logout/", views.logoutUser, name="logout"),

        path("", views.profiles, name="profiles"),
        path("profile/<str:pk>/", views.userProfile, name="user-profile"),
    ]
  ```

# User Registration

- So, now when we have out login form ready, the next thing we are gonna build is the SigUp Page or the User Registration Form.
- We will first create a template for the signup and than move ahead to make some minor changes for the flash messages in the `main.html` in the `root` templates folder later.

    `login_register.html` - `users` app

    ```Jinja
    {% extends 'main.html' %}
    {% load static %}
    {% block content %}

    {% if page == 'signup' %}

    <br><br><br>
    <div class="auth">
        <div class="card">
            <div class="auth__header text-center">
                <a href="/">
                    <img src="{% static 'images/icon.svg' %}" alt="icon" />
                </a>
                <h3>Register an Account</h3>
                <p>Create a new developer account</p>
            </div>

            <form method="POST" action="{% url 'signup' %}" class="form auth__form">
                {% csrf_token %}

                {% for field in form %}
                <div class="form__field">
                    <label for="formInput#text">{{field.label}}</label>
                    {{field}}

                    <!-- {% if field.help_text %}
                    <small>{{field.help_text}}</small>
                    {% endif %} -->

                    {% for error in field.errors %}
                    <p style="color: red;">{{error}}</p>
                    {% endfor %}

                </div>

                {% endfor %}

                <div class="auth__actions">
                    <input class="btn btn--sub btn--lg" type="submit" value="Sign  In" />
                </div>
            </form>
            <div class="auth__alternative">
                <p>Already have an Account?</p>
                <a href="{% url 'login' %}">Log In</a>
            </div>
        </div>
    </div>

    <br><br><br>    

    {% else %}

    <div class="auth">

        <div class="card">

            <div class="auth__header text-center">
                <a href="/">
                    <img src="{% static 'images/icon.svg' %}" alt="icon" />
                </a>
                <h3>Account Login</h3>
                <p>Hello Developer, Welcome Back!</p>
            </div>

            <form action="" method="POST" class="form auth__form">
                {% csrf_token %}
                <!-- Input:Username -->
                <div class="form__field">
                    <label for="formInput#text">Username: </label>
                    <input class="input input--text" id="formInput#text" type="text" name="username"
                        placeholder="Enter your username..." />
                </div>

                <!-- Input:Password -->
                <div class="form__field">
                    <label for="formInput#password">Password: </label>
                    <input class="input input--password" id="formInput#passowrd" type="password" name="password"
                        placeholder="••••••••" />
                </div>

                <div class="auth__actions">
                    <input class="btn btn--sub btn--lg" type="submit" value="Log In" />

                </div>
            </form>

            <div class="auth__alternative">
                <p>Don’t have an Account?</p>
                <a href="{% url 'signup' %}">Sign Up</a>
            </div>
        </div>
    </div>
    {% endif %}
    {% endblock content %}
    ```

    `main.html` - `root` templates

    ```Jinja
    <!DOCTYPE html>
    {% load static %}
    <html>

    <head>
        <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <!-- Favicon -->
    <link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon" />
    <!-- Mumble UI -->
    <link rel="stylesheet" href="{% static 'uikit/styles/uikit.css' %}" />
    <!-- Dev Search UI -->
    <link rel="stylesheet" href="{% static 'css/app.css' %}" />
    <!-- Font Awesome Icons -->
    <script src="https://kit.fontawesome.com/c79118cca6.js" crossorigin="anonymous"></script>
    <link href="{% static 'fontawesomefree/css/fontawesome.css' %}" rel="stylesheet" type="text/css">
    <link href="{% static 'fontawesomefree/css/brands.css' %}" rel="stylesheet" type="text/css">
    <link href="{% static 'fontawesomefree/css/solid.css' %}" rel="stylesheet" type="text/css">

    <title>DevSearch - Connect with Developers!</title>

    </head>

    <body>
        {% include 'navbar.html' %}

        {% if messages %}
            {% for message in messages %}
                <div class="alert  alert--{{message.tags}}">
                    <p class="alert__message">{{message}}</p>
                    <button class="alert__close">x</button>
                </div>
            {% endfor %}
        {% endif %}

        {% block content %}
        {% endblock content %}
        <hr>
        <p>FOOTER</p>
    </body>
    <script src="{% static 'uikit/app.js' %}"></script>
    <script src="{% static 'js/main.js' %}"></script>

    </html>
    ```

    So, now when we have the templates ready, let's move on to working with views, urls and forms. So, first wew will create a `forms.py` files for User Signup, this will will contain the details of the form of what all fields user needs to fill at the time of signup.

    `forms.py` - `users` app

    ```python
    from django.forms import ModelForm
    from django.contrib.auth.forms import UserCreationForm
    from django.contrib.auth.models import User

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
    ```

    This is very much similar to what we have done for the `forms.py` of the `projects` app. We define the fields of the form and assign the class to them for adding styling.

    Next, we need to do the most important thing, creating the views and urls for the User SignUp.

    `views.py` - `users` app

    ```python
    from django.shortcuts import redirect, render
    from django.contrib.auth import login, authenticate, logout
    from django.contrib.auth.decorators import login_required
    from django.contrib import messages
    from .forms import CustomUserCreationForm
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
                return redirect("profiles")

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

    ```

    In this file, we have add a new function `signupUser` that is views for signup page. It has a variable called `page` that holdes a string value, if the string value is `signup` than the signup page will be rendered, and if not the `login` page will be rendered. We than create a instance of our `CustomUserCreationForm`. Now, if the METHOD is a `POST` METHOD, we create a instance of the `CustomUserCreationForm` in variable `form` with the values given by the user. We check if the form is valid or not, if valid than and than assign it to `user` variable as `user = form.save(commit=False)`. This will create an instance of the model with the give data that is not added to the database yet. Finally, the user is saved and logged in and redirected to the `profiles` page.

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
    ]
    ```

    Now, once the nessecary templates and `views.py` are ready, last thing we need to update is `urls.py`, o that we can start seeing the actual stuff. We add the `signupUser` views to the urls and that's all said and done.

</p>
</storng>
