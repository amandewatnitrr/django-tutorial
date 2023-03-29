<strong>
<p align="justify">

# Models and Admin Panel

- Before moving, further with anything, we have to take care of the unapplied migrations. Also, we have to check out the Django Admin Panel.

![](/imgs/Screenshot%202023-03-13%20at%2010.46.26%20AM.png)

- So, what's going on here, why do we see this message. So, when Django sets up our Project for us and we run the first `startproject` command, we get the boilerplate files and with that comes the `sqlite` database. We won't see anything in `db.sqlite3` but it is connected to `settings.py`, django is configured to it. So, there if we haven't changed anything around line 80, we will see something like this:

    `settings.py` - `test_project`

    ```python
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    ```

  So, Django is connected to this database, but there is nothing in this databse for us yet. So, that means it's completely empty. There are no tables and we need to migrate it to actually prep it to make sure it can get built out for us. Now, the beautiful thing about Django is we don't have to buid it out manually. Django already prepares a bunch of tables for us, some default thing like sessions, user models so we can actually have a user to start right away. It builds out this table for us and so on.

  There are some defaults that comes with it. And basically we have to run one command and that way our database is setup and ready to be customized. So, if we go to URLs, we also have admin panel, as you can see below:

    `urls.py` - `test_project`

    ```python
    from django.contrib import admin
    from django.urls import path, include


    urlpatterns = [
        path("admin/", admin.site.urls),
        path("",include("projects.urls")), 
        # Here we are importing the paths from the projects app that we created, there in we have a file urls.py which has the urls to the views.
    ]
    ```

    But that can't be accessed unless and untill we have our database ready. So, if my server is on and we try to visit it, we see something like this. We get the exception message `no such table exists here`. `django_session` is how django authenticates users in this table, but it doesnot exist yet.<br>

    ![](/imgs/Screenshot%202023-03-13%20at%2011.01.03%20AM.png)

    <br>

    So, what we need to do is, we need to run a command and build out these tables. Django already has lot of these tables prepared for us, so it's basically just  going to execute those.

- In order to do so, we execute the command `python3 manage.py migrate`. We have gone through this initially, when we first installed Django and we saw the `makemigrations` command and `migrate` make migrations.

<br>

![](/imgs/Screenshot%202023-03-14%20at%2012.25.01%20AM.png)

<br>

- After executing the command, we can clearly see that there's no warning message appearing anymore. So, if we now visit the admin page `http://127.0.0.1:8000/admin/`. We encounter a login page. Now, so far we have only succeded to access the admin panel, but we are not able to login yet. So, in order to access the admin panel, we need to create a `superuser` using the `createsuperuser` as follows: `python manage.py createsuperuser`.

- As soon as you hit enter, you are asked to provide your `username`, `email-id` and `password`. And the `superuser` is created succesfully. Now, we can actually access the admin panel and by default there are different user permissions that django has for us. If, we use the `createsuperuser` command  that's going to create a user with top-level permission. So, this means we will have admin level access and hecne access it.

<br>

![](/imgs/Screenshot%202023-03-14%20at%2011.04.26%20AM.png)

- So, this is how our admin panel initially looks like. When we executed the `migrate` command, it created this `groups` and `users` table for us. We can see in database when we run the `python manage.py createsuperuser` command. It created the user with given details on the user database. We can actually view this user and modify the information.

![](/imgs/Screenshot%202023-03-14%20at%2011.11.05%20AM.png)

<br>

![](/imgs/Screenshot%202023-03-14%20at%2011.12.59%20AM.png)

## Django Models

- In Django, we model our data using classes. In `models.py` file, we define the tables.
- So, having a look at an example below:

```python
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) 
    # Setting the null=true means that it's not nessecary to have a description, it's an optional thing.
    # null by default is always set to false.
    # blank=True again means this field can be empty.
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    created =  models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
```

- So, whenever we create a class what we do is inherit from `models.Model` and this will tell django that this officially a model and not just a class.
- And soon as we run our migrations, what django is gonna do is, the migration will be reprepared and run. It's gonna take the model mentioned and it will create a table in our database like the model mentioned and would look something like:

<table>
    <tr>
        <th colspan="3">Project</th>
    </tr>
    <tr>
        <th>ID</th>
        <th>Title</th>
        <th>Decription</th>
    </tr>
    <tr>
        <td>Project Number</td>
        <td>Project Name</td>
        <td>Project Description</td>
    </tr>
</table>

- The Table name will be the same as Class name. And for each field within the table we need to specify it's datatype within the class. So, make the model as a class and once we migrate it, it turns into a database table. And using the models that's how we can actually acces and query our data and django makes it pretty simple for us.
- After, the model is created we move the terminal and run the command `python3 manage.py makemigrations`. And as soon as we run the command, django runs a set of commands by it's own to conver the given models into tables. Along, with that it creates migrations saying it created a model called `Project`.

![](/imgs/Screenshot%202023-03-28%20at%203.02.54%20PM.png)

- So, now if we go to the migrations folder, we can see a file by the name `0001_initial.py` created. And it looks something like this:

  - `0001_initial.py` - `/projects/migrations/`

    ```python
    # Generated by Django 4.1.7 on 2023-03-28 09:32

    from django.db import migrations, models
    import uuid


    class Migration(migrations.Migration):

        initial = True

        dependencies = [
        ]

        operations = [
            migrations.CreateModel(
                name='Project',
                fields=[
                    ('title', models.CharField(max_length=200)),
                    ('description', models.TextField(blank=True, null=True)),
                    ('demo_link', models.CharField(blank=True, max_length=2000, null=True)),
                    ('source_link', models.CharField(blank=True, max_length=2000, null=True)),
                    ('created', models.DateTimeField(auto_now_add=True)),
                    ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ],
            ),
        ]

    ```

- So, django prepared all of this for us and we don't to run SQL commands to do all this stuff. Now, that we have a new migration. Let's go ahead and execute this new migration. So, anytime we have mdoel update or something like that we run `python3 manage.py migrate`.

![](/imgs/Screenshot%202023-03-28%20at%203.10.19%20PM.png)

- So, as soon as we executed that what happened is it added whatever these migrations told into the database. But even after that you won't be able to see it on the admin panel ause there's still something that needs to be added up. We need to register the model with the admin panel after creating it.

- For this inside `projects`, we need to go to `admin.py`, so what  we need to do here is import the model as follows and it will be visible on the admin panel.

  - `admin.py` - `/projects`

    ```python
    from django.contrib import admin
    from .models import Project
    # Register your models here.

    admin.site.register(Project) 
    # This will register the Model Project and show it on the admin panel.

    ```

![](/imgs/Screenshot%202023-03-28%20at%203.18.28%20PM.png)

- From here we can actually update, modify, do what we need here to actually add projects to the database. Add when we add them it looks something like this:

![](/imgs/Screenshot%202023-03-28%20at%204.28.57%20PM.png)

- But the new records added to the table appear as project objects here rather than there title, we can do so by adding the following code to the class in `models.py`.

    ```python
    def __str__(self):
            return self.title
    ```

![](/imgs/Screenshot%202023-03-28%20at%204.55.27%20PM.png)

</p>
</storng>