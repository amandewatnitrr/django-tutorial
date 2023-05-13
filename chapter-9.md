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
                <a class="tag tag--pill tag--main settings__btn" href="#"><i class="im im-edit"></i> Edit</a>
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
                <a class="tag tag--pill tag--sub settings__btn tag--lg" href="#"><i class="im im-plus"></i> Add Skill</a>
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
                    <a class="tag tag--pill tag--main settings__btn" href="#"><i class="im im-edit"></i> Edit</a>
                    <a class="tag tag--pill tag--main settings__btn" href="#"><i class="im im-x-mark-circle-o"></i>
                    Delete</a>
                </td>
                </tr>
                {% endfor %}
            </table>

            <div class="settings">
                <h3 class="settings__title">Projects</h3>
                <a class="tag tag--pill tag--sub settings__btn tag--lg" href="#"><i class="im im-plus"></i> Add Project</a>
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
                    <a class="tag tag--pill tag--main settings__btn" href="{% url 'delete-project' project.id %}"><i class="im im-x-mark-circle-o"></i>
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
    # Add this to the bottom of the existing code
    @login_required(login_url="login")
    def userAccount(request):
        profile = request.user.profile
        skills = profile.skill_set.all()
        projects = profile.project_set.all()

        context = {'profile':profile,'skills':skills,"projects":projects}
        return render(request,"users/account.html", context)
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
    ]
    ```

- Make some small change to the `navbar.html` in the `root` template.

    `navabr.html` - `root` template

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

</p>