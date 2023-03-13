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

    But that can't be accessed unless and untill we have our database ready. So, if my server is on and we try to visit it, we see something like this. We get the exception message `no such table exists here`. `django_session` is how django authenticates users in this table, but it doesnot exist yet.

</p>
</storng>