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

  ![](/imgs/Screenshot%202023-04-03%20at%201.22.36%20AM.png)

## Create Read Update Delete (CRUD)

- Till now we have only added forms to our website with `Model Form`, the next thing we need to do is add some CRUD functionality to our website.

### CREATE

- If you have a look on the form template we are sending a POST request and we have the submit button. All we need to do is process the POST request we are getting here.
- For example, if we fill some values into this form and submit it, we will get a POST request.

  ![](/imgs/Screenshot%202023-04-04%20at%202.13.50%20AM.png)

  ![](/imgs/Screenshot%202023-04-04%20at%202.15.36%20AM.png)

  We can specify an `action` to the `form`, so we can do something here, but for now we keep it as a empty string, which means we are going to send to whatever page we are on. As we want to send it back to same URL, so that's why we have it like that.

  ```Jinja
  {% extends 'main.html' %}

  {% block content %}

  <form action="" method="POST">
      {% csrf_token %}
      {{ form.as_p }}
      <input type="submit">
  </form>

  {% endblock %}
  ```

- In the view we will check what the `METHOD` was, so we update the `views.py` for `projects` app as follows:

  `views.py` - `projects` app

  ```python
  def createProject(request):
    form = ProjectForm
    if request.method == "POST":
        form = ProjectForm(request.POST)
        print(request.POST)
    context = {'form':form}
    return render(request, "projects/project_form.html", context)
  ```

  Here, what's actually happening is, if `request.method` equals `POST`, than we will go ahead and process the form. So, we go ahead and specify the form here and instantiate the form class and we are gonna pass in the `POST` data. So, all that data that was sent in comes as a `POST` Request.

  ![](/imgs/Screenshot%202023-04-04%20at%202.13.50%20AM.png)

  Now, when we submit this form, we will see all of the `POST` data when we print `request.POST`.

  ![](/imgs/Screenshot%202023-04-04%20at%205.15.38%20AM.png)

- So, now what we want to do is save the data to the database as a record that we just added in. In order to do that, we will make a small change to the `views.py` in `projects` app.

  `views.py` - `projects` app

  ```python
  from django.shortcuts import render, redirect 
  # We added redirect to the import so that we can return to the specified page after submission 
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
      
      if request.method == "POST":
          form = ProjectForm(request.POST)
          if form.is_valid():
              form.save()
              print(request.POST)
              return redirect("projects")
              # Upon submission, the user will be redirected to "projects" page

      context = {'form':form}
      return render(request, "projects/project_form.html", context)
  ```

  So, here what's happening is and this is a cool thing about django that it will check that all the required fields are filled or not, making sure that everythig matches up and checks if everything is valid. Once the form is validated  i.e. `form.is_valid()` returns `true`, the form will save and new object is added to the database. You can see this in the example below:

  ![](/imgs/Screenshot%202023-04-04%20at%205.27.32%20AM.png)

  <br>

  ![](/imgs/Screenshot%202023-04-04%20at%205.28.23%20AM.png)
    
  <br>

  ![](/imgs/Screenshot%202023-04-04%20at%205.34.11%20AM.png)

  <br>

  ![](/imgs/Screenshot%202023-04-04%20at%205.47.03%20AM.png)

- So, now we are able to add data into the database now. What happened here is we have the model form (`project_form.html`), that form was rendered out inside of our template. When we submitted it, the form was sent to `views.py`. We sent it with the `POST` request because we were using `POST` method as specified in the template. We check the method and if it's a `POST` method, we created a new instance of that form, we checked if it was valid, if so data was sent into it, we saved it, which creates a user because it's a model form, and at the end we redirect the user.

</p>
</storng>
