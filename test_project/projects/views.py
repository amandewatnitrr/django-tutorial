from django.shortcuts import render, redirect
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

    context = {'form':form}
    return render(request, "projects/project_form.html", context)
