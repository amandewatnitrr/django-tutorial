<strong>
<p align="justify">

# User Profile Creation and Rendering Profiles

- So, we have installed our theme and other stuff, and now our Website looks something like this:

![](./imgs/Screenshot%202023-04-15%20at%206.40.47%20PM.png)

![](./imgs/Screenshot%202023-04-15%20at%2011.23.09%20PM.png)

- So, till now in our project we have a review model, Project model and a tag model. But none of them is associated to a certain user or a profile. So, as till now we have only discussed the concept of apps and haven't implemented it actually yet. So, we are going to build `Profile`, `Skill` and `Message` model. And these 3 are not going to be the same app as the `Project`, `Tag` and `Review`. They are going to be in project but in different apps.
- The good thing is we don't need to worry about the user model because that's already built into django, but that's something we are gonna connect to and make some edits. So, even though we are gonna make different apps, they need to be connected to each other. As we need to have `Project` and `Review` model connected to the profile. And hence, these 2 apps will be able to communicate with each other.

- So, in our project we are going to have 2 apps. One the `projects` app and the other `user` app. We are gonna create a seprate `user` app where we have our own database models, our own neutral routing and templates.

- Now we need to create a new app called `users` app. We will do this using the command `python3 manage.py startapp users`. So, now the app is created, we need to connect this app to the project.
- The next thing we will do is make some changes in `settings.py`, so as to include this app into the project.

  `settings.py`

  ```python
  # Update INSTALLED_APPS in setting.py

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        
        "projects.apps.ProjectsConfig", # Added by us
        "users.apps.UsersConfig", # Added by us
    ]
  ```

- Now, we before we create some views and urls, let's create some template for our pages. So, in the users app we create a folder `users\templates\users`.
- Now create a file with name `profiles.html` in the `templates` folder of the `users` inside `users` and let's put some test content in it.

  `profiles.html` - `\users\templates\users`

  ```Jinja
    {% extends 'main.html' %}

    {% block  content %}

        <h1> User Profile </h1>

    {% endblock %}
  ```

- Now, when we have the template ready, let's move to making the `views.py` and `urls.py` for this app.

  `views.py` - `users` app

  ```python
    from django.shortcuts import render
    from .models import Profile

    # Create your views here.

    def profiles(request):
        profiles = Profile.objects.all()
        context = {"profiles":profiles}
        return render(request, "users/profiles.html",context)
  ```

  `urls.py` - `users` app

  ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path("", views.profiles, name="profiles"),
    ]
  ```

- Now, update `urls.py` for the project.

  `urls.py` - `project`

  ```python
    urlpatterns = [
        path("admin/", admin.site.urls),
        path("",include("projects.urls")),
        path("users/",include("users.urls")), 
        # Here we are importing the paths from the projects app that we created, there in we have a file urls.py which has the urls to the views.
    ]
  ```

- Now, if we try visiting `http://127.0.0.1:8000/users/`, we would see something like this:

    ![](/imgs/Screenshot%202023-04-20%20at%207.28.57%20PM.png)

- Now, let's create the model for `Profile`, but there might be a question you think of, Why we are doing all this if django already has a `user` model of it's own?? Well, we can do direct changes, that's for sure but doing that might be pretty risky and hence is not recommended to developers. Hence, we create a one-to-one relationship b/w pre-defined `User` and `Profile` model, when creating the `Profile` model. Cause if `User` model breaks all authentication breaks, and a lot can go wrong with our application. So, instead of modifying it what I like to do is replicate it. We take the username, email, name and than we add in other information. Now, we create what we call one-to-one field so every single user in database will have profile and every profile will have one user and the profile will get automatically generated at the time we create the user. Also, here we will be creating here django model relationship here, let's see how we do it.

  `models.py` - `users` app

    ```python
    from django.db import models
    from django.contrib.auth.models import User
    import uuid
    # Create your models here.

    class Profile(models.Model):
        
        user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
        # Deleting the Profile will also delete the user associated with it

        name = models.CharField(max_length=200,blank=True,null=True)
        email = models.EmailField(max_length=500, blank=True,null=True)
        short_intro = models.TextField(blank=True,null=True)
        profile_image = models.ImageField(blank=True,null=True,upload_to="profile-pics/",default="profile-pics/user-default.png")

        social_github = models.URLField(max_length=500,blank=True,null=True)
        social_twitter = models.URLField(max_length=500,blank=True,null=True)
        social_linkedin = models.URLField(max_length=500,blank=True,null=True)
        social_instagram = models.URLField(max_length=500,blank=True,null=True)
        social_website = models.URLField(max_length=500,blank=True,null=True)

        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
        created = models.DateTimeField(auto_now_add=True)


        def __str__(self):
            return str(self.user.username)

    ```

- Now, once the model is ready, let's create the migrations and migrate it. So, we hit the command `python3 manage.py makemigrations` and than `python3 manage.py migrate`, and now, we need to edit `admin.py` for `users` app as follows:

  `admin.py` - `users` app

  ```python
    from django.contrib import admin
    from .models import Profile

    admin.site.register(Profile)
    # Register your models here.
  ```

- Now, if you go to the admin panel, we can see the `Profiles` model on the admin panel. And we also added a profile for the existing user.

  ![](/imgs/Screenshot%202023-04-21%20at%205.20.13%20AM.png)

- The `project` model has one-to-one relation with the `profile`. So, we will add a owner field to the `Project` model, we do it as follows:

  `models.py` - `projects` app

    ```python
    # Update as follows

    from django.db import models
    import uuid
    from users.models import Profile

    # Create your models here.

    class Project(models.Model):
        # Below is the mentioned update .
        owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
        title = models.CharField(max_length=200)
        description = models.TextField(null=True, blank=True)
        featured_image = models.ImageField(null=True, blank=True,default="default.jpg")
        # Setting the null=true means that it's not nessecary to have a description, it's an optional thing.
        # null by default is always set to false.
        # blank=True again means this field can be empty.
        demo_link = models.CharField(max_length=2000, null=True, blank=True)
        source_link = models.CharField(max_length=2000, null=True, blank=True)
        tags = models.ManyToManyField('Tag', blank=True)
        vote_total = models.IntegerField(default=0,null=True,blank=True)
        vote_ratio = models.IntegerField(default=0,null=True,blank=True)
        created =  models.DateTimeField(auto_now_add=True)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

        def __str__(self):
            return self.title
    ```

- Now, we again need to create some migrations. Use the command `python3 manage.py makemigrations` and than `python3 manage.py migrate` and now the change in the models have been migrated.

- Now, move back to the templates for the `projects` page and make the changes there to show the name of the actual owner of the project as follows and make the followung change:

  `projects.html` - `projects` app - `projects/templates/projects`

  ```Jinja
  <p><a class="project__author" href="">By {{ project.owner.name }}</a></p>
  ```

  And you would see something like this, each project mentioneing there owner's name:

  ![](/imgs/Screenshot%202023-04-21%20at%205.41.55%20AM.png)

# Add & Render Profiles

- So, this portion will again be not available as it's more about just copy pasting the template from the resources folder of the Course. But we did make some changes to the `models.py` and other files which we will mention where we made the changes.

  `models.py` - `users` app

  ```python
    from django.db import models
    from django.contrib.auth.models import User
    import uuid
    # Create your models here.

    class Profile(models.Model):
        
        user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
        # Deleting the Profile will also delete the user associated with it

        name = models.CharField(max_length=200,blank=True,null=True)
        email = models.EmailField(max_length=500, blank=True,null=True)
        username = models.CharField(max_length=200, blank=True,null=True)
        location = models.CharField(max_length=200, blank=True,null=True)
        short_intro = models.TextField(blank=True,null=True)
        bio = models.TextField(blank=True,null=True)
        profile_image = models.ImageField(blank=True,null=True,upload_to="profile-pics/",default="profile-pics/user-default.png")

        social_github = models.URLField(max_length=500,blank=True,null=True)
        social_twitter = models.URLField(max_length=500,blank=True,null=True)
        social_linkedin = models.URLField(max_length=500,blank=True,null=True)
        social_instagram = models.URLField(max_length=500,blank=True,null=True)
        social_website = models.URLField(max_length=500,blank=True,null=True)

        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
        created = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return str(self.user.username)

    class Skill(models.Model):
        owner = models.ForeignKey(Profile,null=True,on_delete=models.CASCADE,blank=True)
        name = models.CharField(max_length=200,blank=True,null=True)
        description = models.TextField(blank=True,null=True)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
        created = models.DateTimeField(auto_now_add=True)


        def __str__(self):
            return str(self.name)
  ```

  Don't forget to exectue `python3 manage.py makemigrations` and `python3 manage.py migrate` command after making this changes. And than register your app.

  `views.py` - `users` app

  ```python
    from django.shortcuts import render
    from .models import Profile

    # Create your views here.

    def profiles(request):
        profiles = Profile.objects.all()
        context = {"profiles":profiles}
        return render(request, "users/profiles.html",context)

    def userProfile(request, pk):
        profile = Profile.objects.get(id=pk)
        context = {'profile':profile}
        return render(request, "users/user-profile.html",context)
  ```

  `urls.py` - `users` app

  ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path("", views.profiles, name="profiles"),
        path("profile/<str:pk>/", views.userProfile, name="user-profile"),
    ]
  ```

  `admin.py` - `users` app

  ```python
    from django.contrib import admin
    from .models import Profile, Skill

    admin.site.register(Profile)
    admin.site.register(Skill)
    # Register your models here.
  ```

</p>
</storng>
