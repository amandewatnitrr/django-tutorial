<strong>
<p align="justify">

# Create Update Delete(CRUD)

## Model Forms

- In order to make the user perform CRUD operations, we will first start with the create operation. Here we will be making a form where user can put values into the form and add it to the database.
- For that we need to have the `views.py` and `urls.py` updated. Also, in addition to that we need to create a new template for `createe-project` page.
- Let's start with the template first. Within projects app inside `/templates/projects/`, create a new template with the name `project-form.html`. Type the following content into it:
  
  ```Jinja
    {% extends 'main.html' %}

    {% block content %}

    <form method="POST">
        {% csrf_token %}
        {% for field in form %}
            {{ field.label }}
            {{ field }}
            <br><br>
        {% endfor %}
        <input type="submit">
    </form>

    {% endblock %}
  ```

- Now, the template is created, create a view for the template. In the `projects` app, `views.py` update it by adding the following function:
  
  ```python
    from django.shortcuts import render
    from django.http import HttpResponse
    from .models import Project, Review, Tag
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

    def createProject(request):
        form = ProjectForm
        context = {'form':form}
        return render(request, "projects/project_form.html", context)

  ```

  This will render the template we created previously, whenever we visit the specified URL for the form page.

- Now, in the `projects` app, `urls.py` in the list urlpatterns, add the URL for this page:

  ```python
  from django.urls import path
  from . import views

  urlpatterns = [
        path("",views.projects,name="projects"),
        path("project/<str:pk>",views.project,name="project"),
        path("create-project/",views.createProject,name="create-project")
  ]
  ```

- In order to make the `createProject` page accessible, we make minor changes to the `/template/navbar.html` of our project.

  ```Jinja
  {% load static %}

    <!-- Header Section -->
    <header class="header">
        <div class="container container--narrow">
            <nav class="header__nav">
                <a href="{% url 'create-project' %}">Add Projects</a>
            </nav>
        </div>
    </header>
  ```

- Now, instead of creating a complete form by our ownself, django offer this comfort of developing form with ease using `ModalForm`.
- So, for this in the `projects` app, we create a new file `form.py`.
- Specifying ModelForm within the argument of the class, specifies that the given class is a Form.
- At a minimum, A Modal form requires 2 fields.

  - model
  - field

- We can do 2 things here now, one is we can create  a list here and we can add in all the fields that we wnat to allow and if we want it for all the fields, we can type `field = '__all__'`. Now, what's gonna happen is Django is going to look at the `Project` Model, and it's going to create a form based around the model, taking in consideration all the attributes, look at the type of field for each attribute. It will generate a form based on what we have in the model.

- `forms.py` - `projects` app

  ```python
  from django.forms import ModelForm
  from .models import Project

  class ProjectForm(ModelForm):
      class Meta:
      model = Project
      fields = '__all__'
  ```

- But ther are some attributes, which will not be taken into consideration by the form such as `ID` becuase that is not a editable field.

- And, our output looks something like this:

  ![](/imgs/Screenshot%202023-04-03%20at%201.10.54%20AM.png)


</p>
</storng>
