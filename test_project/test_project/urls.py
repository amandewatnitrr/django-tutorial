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


urlpatterns = [
    path("admin/", admin.site.urls),
    path("",include("projects.urls")), 
    # Here we are importing the paths from the projects app that we created, there in we have a file urls.py which has the urls to the views.
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
