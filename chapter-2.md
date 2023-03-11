<strong>
<p align="justify">

# Baiscs of Django

## Views and URLs

``` Mermaid
        flowchart LR
            A{{page}} ==> B[returnPage] ==> C[[page.html]]
```

- So, in django we will have URL Patterns, we find which path is associated inside of a variable. If, the path doesn't exist and we try hitting that URL that doesn't exist it will return some error.
- Once, it does find a match, we are going to trigger a function, this function will probably get some kind of template. It will probably query the database, pull back some data and then the user will see this page returned inside of their browser.

## Creating Basic Views

- First of all let's start with very basic.
- We need to first create a function called `projects()` for returning back some projects and we pass parameter `request` to this function.
- This parameter `request` is a request object like an HTTP Request. That makes this a view.
- Now to return it, we need to return back something to the user. So, right now we are just returing a HTTP Response using the library `from django.http import HTTpResponse` for testing purpose.
- Than we add another path element to `urlpatterns` as `path("projects/",projects,name="projects")`.

- Code for `urls.py` in test_project:

    ```python
    from django.contrib import admin
    from django.urls import path
    from django.http import HttpResponse

    def projects(request):
        return HttpResponse("Here are our Projects")

    def project(request, pk): #Here in the pk also must be specified in the URL or it will show that the response is missing
        return HttpResponse("SINGLE PROJECT " + pk) 

    urlpatterns = [
        path("admin/", admin.site.urls),
        path("projects/",projects,name="projects"),
        path("project/<str:pk>",project,name="project") #Dynamic Data being rendered
    ]
    ```

- Now when we execute `python manage.py runserver`, we see 404 page as below. This happened because we don't have a home page yet.

<img width="60%" src="imgs/Screenshot%202023-03-07%20at%201.16.42%20AM.png"/>

- Now, if we visit `http://127.0.0.1:8000/projects/`. You will see the following:

<img width="60%" src="imgs/Screenshot%202023-03-07%20at%209.02.19%20AM.png"/>

## Templates and Templates Inheritance

- So, to get started with it, I created a folder with the name `templates` at the same level as projects app.

- Let's add 2 files `projects.html` and `single-project.html`.
- Put some simple HTML inside it for now.
- Move to `settings.py` for our project and look for `TEMPLATES` variable.
- Within `TEMPLATES` under `DIRS` list, add the following: `os.path.join(BASE_DIR,"templates"),`
- This will let django where the specified template is present.
  
  ```python
  TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR,"templates"), # This let's Django know where our templates are.
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
  ]
  ```

- Now, go to `views.py` of your `project` app. And instead of returing a `HTTpResponse` return the rendered template.

  ```python
  from django.shortcuts import render
    from django.http import HttpResponse

    def projects(request):
        # return HttpResponse("Here are our Projects")
        # The above statement gives the specified Argument as an HTTpResponse.

        return render(request, "projects.html")

    def project(request, pk):
        return render(request, "single-project.html")
  ```

- Now, check the localhost. You will see the template being rendered sucessfully.

- In order to have all `projects` related component in one folder we must have the `templates` for `projects` under `projects` only. So, we made a new `templates` folder inside `projects`, so the current structure for these templates is `/test_project/projects/templates/`.

- Now, when we have shifted the `projects.html` and `singlr-project.html` to the other templates folder.
- This is to make the structure clean and understandable.
- So, now we need to update the `view.py` for `projects` and `urls.py` for both `projects` and `test_project`.
-
  `urls.py` - `test_project`

  ```python
  from django.contrib import admin
  from django.urls import path, include


    urlpatterns = [
        path("admin/", admin.site.urls),
        path("",include("projects.urls")), 
        # Here we are importing the paths from the projects app that we created, 
        # there in we have a file urls.py which has the urls to the views.
    ]
  ```

  `urls.py` - `projects`
  
  ```python
    from django.urls import path
    from . import views


    urlpatterns = [
        path("",views.projects,name="projects"),
        path("project/<str:pk>",views.project,name="project")
    ]
  ```

  `views.py` -  `projects`

  ```python
    from django.shortcuts import render
    from django.http import HttpResponse

    def projects(request):
        # return HttpResponse("Here are our Projects")
        # The above statement gives the specified Argument as an HTTpResponse.

        return render(request, "projects/projects.html")

    def project(request, pk):
        return render(request, "projects/single-project.html")
  ```

- With all the changes, we are good to go, but before that let's discuss a little about `Django Template Language`.

# Django Template Language and Jinja <img src="https://img.shields.io/badge/Jinja-B41717?style=plastic&logo=Jinja&logoColor=white"/>

- A Django project can be configured with one or several template engines (or even zero if you don’t use templates). Django ships built-in backends for its own template system, creatively called the Django template language (DTL), and for the popular alternative Jinja2.
- Jinja is a fast, expressive, extensible templating engine. Special placeholders in the template allow writing code similar to Python syntax. Then the template is passed data to render the final document.
  
</p>
</strong>
