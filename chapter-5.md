<strong>
<p align="justify">

# Static Files and Theme Installation

- So, far now when we have covered the basic main stuff, we can make our website look a bit better. Cause all the previous looks honestly sucks. So, it's now time to configure our static files  with our django  project, so static files are basically any kind of css, javascript or image file or any kind of external file here. So, before start styling our page we don't have to write css inline in our html template.
- We will create a external folder that's going to handle all the static files. So, Django has a way for configuring that for us. So, we're just going to run through that.
- And what we are going to do in this video is first connect our stylesheet, adding a logo in the navbar and finish up by adding another field into our project model, so we can actually see a picture that goes with project.
- To do that, we first need to create a seprate directory at the root project area. So, we create a folder and name it `static`. So, inside of `static`, let's go ahead and create a file for styling. Within that we will have different folders for `css`, `js` and `images`.
- So, this is how our folder structure  should look like:

  ![](/imgs/Screenshot%202023-04-08%20at%203.07.56%20AM.png)

- Inside of the styles folder, and creare a stylesheet. Let's call this `main.css`
- For now, let's keep it simple by putting in some simple css, so:

  `main.css` - `static`

  ```CSS
  h1{
    color: purple;
  }
  ```

- So, the first stpe here is go into the `settings.py` and configure the static files. Go, to the botttom of the file where, we see `STATIC_URL`, underneath that create a new folder called `STATICFILES_DIRS` which will be a list and do as shown below:

  `settings.py`
  
  ```python
  STATIC_URL = "static/"

  STATICFILES_DIRS = [
      os.path.join(BASE_DIR,"static") # This is a older way of including in files.
      # There's a new way, where we can directly include it as:
      # BASE_DIR / "static"
  ]
  ```

- After this django knows about this static folder. So, now to actually apply a static file in our template, we will go to `main.html`. So, first all we need to link the css to the html and than we need to changes the `href`. After that, it won't work unill we have loaded the static folder into the template. And we make the following changes:

  `main.html`

  ```jinja
    <!DOCTYPE html>
    {% load static %}
    {# The above line loads the files in "static" folder on the template. #}
    <html>

    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />

        <link rel="stylesheet" type="text/css" media="screen" href='{% static "css/main.css" %}'>
        {# In this way we can import a css file into django template as mentioned. #}

        <title>DevSearch - Connect with Developers!</title>

    </head>

    <body>
        {% include 'navbar.html' %}

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

  Also, we did a minor change in our existing template `projects.html` as we have nothing related to `h1` tag we got to add something in there.

  `projects.html` - `/templates/projects`

  ```Jinja
    {% extends 'main.html' %}

    {% block content %}

    <h1>Projects</h1>

    <ul>
        <table style="border: 1px solid white;border-collapse: collapse;">
            <tr>
                <th>Project Title</th>
                <th>Date Created</th>
                <th>Edit</th>
                <th>Delete</th>
            </tr>
            {% for project in projects %}
            <tr>
                <td><a href={% url 'project' project.id %}>{{ project.title }}</a></td>
                <td>{{ project.created }}</td>
                {# In the line above we are saying that this is a link to /project and a specified project id. #}
                <td><a href="{% url 'update-project' project.id %}">📝</td>
                <td><a href="{% url 'delete-project' project.id %}">🗑️</td>
            </tr>
            {% endfor %}
        </table>
    </ul>

    {% endblock content %}  
  ```

  And this is how the output would look like and the CSS has been implemented as mentioned:

  ![](/imgs/Screenshot%202023-04-08%20at%205.54.50%20AM.png)

- Now, we are gonna put the logo up on the website. So, get our logo from somewhere first of all. So, inside the `static` folder in `images`, we have our logo. So, we need to make following changes to the `navbar.html` template:

  ```Jinja
  {% load static %}

  <!-- Header Section -->
  <header class="header">
      <div class="container container--narrow">
          <nav class="header__nav">
              <img class="logo" src = "{% static "images/logo.svg" %}"/>
              <a href="{% url 'create-project' %}">Add Projects</a>
          </nav>
      </div>
  </header>
  ```

  And now, when you refresh the page, the logo is there in the navbar.

- Now adding images for the project is going to be the tough part actually, and is not so simple as it might appear cause the project is a seprate model in the datbase. So, for this we need to go to `models.py` file of the `projects` app, and add it as a attribute of the `Project` model. And the the new updated `model` for projects would look something like this:

  `models.py` - `projects` app(Updated Project model)

  ```python
  class Project(models.Model):
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

  But, now when we save it back again, we get some error. Basically working with images in django requires a python library called `Pillow`, which needs to be installed. So, now close your live server and install the library using th command:

  ```bash
  pip3 install Pillow
  ```

  But, now also we will get error because we need to make the migrations so, that the column becomes a part of the database. So, we use the command `python3 manage.py makemigrations` to create migrations and than run the command `python3 manage.py migrate`. This will add the field to the table now, and all the errors are resolved now and we are good to go. But, now there's a small issue that is unreported that still needs to be resolved. So, right now if we upload the image from the admin panel, it is saved in the root directory of the project, and that is something which will disturb the file structure of the project. So, we need to configure it, so we need to go to `settings.py` and make the following changes:

  `settings.py`

  ```python
  MEDIA_ROOT = os.path.join(BASE_DIR,"static/images")
  # Add the above line just below STATICFILES_DIRS
  ```

  `MEDIA_ROOT` here tells django where to store the media related things when added to the page. And save it. Now, if you add the image for any of the project, that will be added directly to the `/static/images`.

  But, even after that we still can't access the image from the browser and will give an error. This is happening because useruploaded content is really it's own thing. So, we have to do some more changes to `settings.py`
  again. The changes are as follows:

  `settings.py`

  ```python
  #This the change that we need to do

  STATIC_URL = "/static/"
  MEDIA_URL = "/images/"

  STATICFILES_DIRS = [
      os.path.join(BASE_DIR,"static")
  ]

  MEDIA_ROOT = os.path.join(BASE_DIR,"static/images")
  STATIC_ROOT = os.path.join(BASE_DIR, "static")
  ```

  So, things don't simply end here. In the `urls.py` for the project, we need to add the url path to the `urls.py`. The changes to the file is as follows:

  `urls.py`

  ```python
  from django.contrib import admin
  from django.urls import path, include

  from django.conf import settings
  from django.conf.urls.static import static


  urlpatterns = [
      path("admin/", admin.site.urls),
      path("",include("projects.urls")), 
      # Here we are importing the paths from the projects app that we created, there in we have a file urls.py which has the urls to the views.
  ]

  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  ```

  We want to have access to the `settings.py` file over here, because we have to connect to our media route and media url. We are importing static, which help us create urls for our static. `MEDIA_ROOT` is where we send the user uploaded content and we just created a file. So, django actually didn't knew previously how to set that. So, now it's time when we finally make change to the template.

  `single-project.html` - `/templates/projects`

  ```Jinja
  {% extends 'main.html' %}
  {% block content %}
  <img src = "{{ project.featured_image }}"/>
  <h2>{{ project.title }}</h2>
  <hr>
  {% for tag in tags %}
  <span style="border:1px solid grey">{{tag}}</span>
  {% endfor %}
  <br>
  <p>{{ project.description }}</p>

  {% endblock content %}
  ```

</p>
</storng>
