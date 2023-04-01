from django.shortcuts import render
from django.http import HttpResponse
from .models import Project, Review, Tag


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
