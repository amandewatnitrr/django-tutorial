# Setting Up a Simple API

- In this particular chapter, we will be working on making a Simple API for our project.
- We will be working with "Django REST Framework", it's a toolkit/library built-on top of django that makes building API very easy.
- But, before we start making API with `djangorestframework`, we will use manual methods to make a Simple API.
- For, this purpose move to the folder where `manage.py` is located, and create a folder called `api`. And, we do it using the command `python3 manage.py startapp api`. And edit them as follows:

    `views.py` - `api` app

    ```python
    from django.shortcuts import render
    from django.http import JsonResponse

    # Create your views here.

    def getRoutes(request):
        routes = [
            {'GET':'/api/projects'},
            {'GET':'/api/projects/id'},
            
            {'POST':'/api/projects/id/vote'},
            {'POST':'/api/users/token'},
            {'POST':'/api/users/token/refresh'},
        ]
        return JsonResponse(routes, safe=False)
    ```

    Here, we have `safe=False` so that we can return something here more than python dictionary. By default, JsonResponse can only return a dictionary, because we are sending a list, we set `safe=False`.

    Similarly, create a `urls.py`.

    `urls.py` - `api` app

    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path('',views.getRoutes)
    ]
    ```

    Once, you are done with this move to the `urls.py` in the project folder, in our case `test-project` folder, as we need to let it know about this api app.

    `urls.py` - `test-project`

    ```python
    """test_project URL Configuration

    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/4.1/topics/http/urls/
    Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    """
    from django.contrib import admin
    from django.urls import path, include

    from django.conf import settings
    # 👆🏻 we want to have access to the setting.py file over here, because we have to connect to our media route and media url.
    from django.conf.urls.static import static
    # 👆🏻 So, we are importing static, which help us create urls for our static
    from django.contrib.auth import views as auth_views

    urlpatterns = [
        path("admin/", admin.site.urls),
        path("",include("projects.urls")),
        path("users/",include("users.urls")),
        path("api/",include("api.urls")), 
        # Here we are importing the paths from the projects app that we created, there in we have a file urls.py which has the urls to the views.

        path('reset_password/',auth_views.PasswordResetView.as_view(template_name="reset_password.html"),name="reset_password"),
        path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),name="password_reset_done"),
        path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"),name="password_reset_confirm"),
        path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),name="password_reset_complete"),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    ```

    Once, done we can go ahead, and test this out. And, this what you would see:

    ![](/imgs/Screenshot%202023-10-05%20at%202.52.19 AM.png)

    It's not really an API at this point, but we will work on it later.