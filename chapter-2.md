<strong>
<p align="justify">

# Baiscs of Django

## Views and URLs


flowchart LR
    A{{page}} ==> B[returnPage] ==> C[[page.html]]


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

  <img  src="imgs/Screenshot%202023-03-07%20at%201.16.42%20AM.png"/>

- Now, if we visit `http://127.0.0.1:8000/projects/`. You will see the following:

  <img  src="imgs/Screenshot%202023-03-07%20at%209.02.19%20AM.png"/>

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
- Jinja is a fast, expressive, extensible templating engine. Special placeholders in the template allow writing code similar to Python syntax. Then the template is passed data to render the final document. It's basically a way to output content and have some kind of business logic in our template.

- Django defines a standard API for loading and rendering templates regardless of the backend. Loading consists of finding the template for a given identifier and preprocessing it, usually compiling it to an in-memory representation. Rendering means interpolating the template with context data and returning the resulting string.

- A Django template is a text document or a Python string marked-up using the Django template language. Some constructs are recognized and interpreted by the template engine. The main ones are variables and tags.
- A template is rendered with a context. Rendering replaces variables with their values, which are looked up in the context, and executes tags. Everything else is output as is.

### Variables

- If we want to pass variables into our template it's done as follows `{{ variable_name }}`.
- Similarly, we can have a look at dictionary, attribute lookup and list-index lookups are implemented with a dot notation:
  
  ```Jinja
  {{ my_dict.key }}
  {{ my_object.attribute }}
  {{ my_list.0 }}
  ```

### Tags

- This is basically a way of adding python like logic to our tmeplate.
- They provide arbitary logic in the rendering process.
- We can write if condition, for loops, else statements and so on.
- Let's understand this with an example:

  ```Jinja
  {% if user.is_authenticated %} Hello, {{ user.username }}
  {% endif %}
  ```

- Now, let's try implmenting this to render data into our Templates.
- So, first we need to edit `views.py` for our project app, in there let's say we want to pass a message, so we do it as follows:

  `views.py` - `projects`

  ```python
  from django.shortcuts import render
  from django.http import HttpResponse

  def projects(request):
      # return HttpResponse("Here are our Projects")
      # The above statement gives the specified Argument as an HTTpResponse.
      msg = "This is Projects Page."
      return render(request, "projects/projects.html", {"msg":msg})
      # We are sending the data here as a key-value pair.

  def project(request, pk):
      return render(request, "projects/single-project.html")
  ```

  `projects.html` - `template` - `projects`

  ```Jinja
  {% extends 'main.html' %}
  {% block content %}
  <h5>Projects Template</h5>
  {{ msg }}
  {% endblock content %}
  ```

- Here's the output what we get:

  <img src="./imgs/Screenshot%202023-03-11%20at%206.27.00%20PM.png">

- Let's now try writting some condition for our webpage.
- For this purpose, we will be working with 2 files: `/test_project/projects/templates/projects` - `projects.html` and `/test_project/projects/` - `views.py`.
- Here's the code:

  `views.py` - `projects`

  ```python
  from django.shortcuts import render
  from django.http import HttpResponse

  def projects(request):
      # return HttpResponse("Here are our Projects")
      # The above statement gives the specified Argument as an HTTpResponse.
      msg = "This is Projects Page."
      number = 11
      context = {"msg":msg, "number":number}
      return render(request, "projects/projects.html", context)

  def project(request, pk):
      return render(request, "projects/single-project.html")
  ```

  `projects.html` - `/projects/template`

  ```Jinja
  {% extends 'main.html' %}

  {% block content %}
  <h5>Projects Template</h5>
  {{ msg }}
  {% if number > 10  %}
      <p>Number is greater than 10.</p>
  {% elif number == 10 %}
      <p>Number equals 10.</p>
  {% else %}
      <p>Number is less than 10.</p>
  {% endif %}

  {% endblock content %}
  ```

  The output looks something like this:

  <img src="./imgs/Screenshot 2023-03-12 at 4.32.34 PM.png"/>

- Now let's try implementing for loop here, we will be working with the same files.
- Here's the code:

  `views.py` - `projects`

  ```python
  from django.shortcuts import render
  from django.http import HttpResponse

  projectsList = [
      {
          'id': '1',
          'title': 'Ecommerce Website',
          'description': 'Fully functional ecommerce website'
      },
      {
          'id': '2',
          'title': 'Portfolio Website',
          'description': 'A personal website to write articles and display work'
      },
      {
          'id': '3',
          'title': 'Social Network',
          'description': 'An open source project built by the community'
      }
  ]


  def projects(request):
      # return HttpResponse("Here are our Projects")
      # The above statement gives the specified Argument as an HTTpResponse.
      msg = "This is Projects Page."
      number = 11
      context = {"msg":msg, "number":number, "projects": projectsList}
      return render(request, "projects/projects.html", context)

  def project(request, pk):
      return render(request, "projects/single-project.html")

  ```

  `projects.html` - `/projects/template`

  ```Jinja
  {% extends 'main.html' %}

  {% block content %}

  <hr>

  <h5>Projects Template</h5>
  {{ msg }}

  {% if number > 10  %}
      <p>Number is greater than 10.</p>
  {% elif number == 10 %}
      <p>Number equals 10.</p>
  {% else %}
      <p>Number is less than 10.</p>
  {% endif %}

  <hr>

  <ul>
      {% for project in projects %}
          <li>Project Title: {{ project.title }}</li>
      {% endfor %}
  </ul>

  {% endblock content %}
  ```

  The output looks something like this:

  <img src="./imgs/Screenshot 2023-03-12 at 6.29.53 PM.png"/>

- Now let's try doing something intresting, let's render the page for eac indiviadula project. For that we need to make views for all the project well it's easy.
- If you remember previously in the `urls.py` for `projects` app, we spcified out url as `path("project/<str:pk>",views.project,name="project")`.
- So, basically we need to iterate throught the List of Projects and show that specific project which matches with the specified ID.
- Here's the code:

  `views.py` - `projects`

  ```python
  from django.shortcuts import render
  from django.http import HttpResponse

  projectsList = [
      {
          'id': '1',
          'title': 'Ecommerce Website',
          'description': 'Fully functional ecommerce website'
      },
      {
          'id': '2',
          'title': 'Portfolio Website',
          'description': 'A personal website to write articles and display work'
      },
      {
          'id': '3',
          'title': 'Social Network',
          'description': 'An open source project built by the community'
      }
  ]


  def projects(request):
      # return HttpResponse("Here are our Projects")
      # The above statement gives the specified Argument as an HTTpResponse.
      msg = "This is Projects Page."
      number = 11
      context = {"msg":msg, "number":number, "projects": projectsList}
      return render(request, "projects/projects.html", context)

  def project(request, pk):
      projectObj = None # Here we set the projectObj to none, this will be the project we want to see.
      context = None # The context is specifed as none to clean the garbage value.
      for i in projectsList: # We iterate through the list of projects
          if i['id'] == pk: # The project id that matches the primary key here ...
              projectObj = i # Will be shifted to projectObj
              context = {"project":projectObj} # and further projectObj will be sent enclosed in the dictionary to the page
      return render(request, "projects/single-project.html",context)

  ```

  `project.html` - `projects/template`

  ```Jinja
  {% extends 'main.html' %}

  {% block content %}
  <hr>
  <h1>Single Project Template</h1>

  <h2>{{ project.title }}</h2>
  <p>{{ project.description }}</p>

  {% endblock content %}
  ```

  Here's the output(URL: 127.0.0.1:8000/project/2):<br><br>
  <img src="./imgs/Screenshot 2023-03-12 at 6.57.36 PM.png"/>

- We can also link the projects page to each and every project page with a minor change.
- Code here:

  `projects.html` - `/projects/template`

  ```Jinja
  {% extends 'main.html' %}

  {% block content %}

  <hr>

  <h5>Projects Template</h5>
  {{ msg }}

  {% if number > 10  %}
      <p>Number is greater than 10.</p>
  {% elif number == 10 %}
      <p>Number equals 10.</p>
  {% else %}
      <p>Number is less than 10.</p>
  {% endif %}

  <hr>

  <ul>
      {% for project in projects %}
          <li>Project Title: <a href={% url 'project' project.id %}>{{ project.title }}</a> - {{ project.description }}</li>
          {# In the line above we are saying that this is a link to /project and a specified project id. #}
      {% endfor %}
  </ul>

  {% endblock content %}
  ```
  
- Just for some clarity, this is our codebase structure right now at this stage:

<img width="20%" src="./imgs/Screenshot 2023-03-12 at 7.03.55 PM.png"/>

</p>
</strong>
