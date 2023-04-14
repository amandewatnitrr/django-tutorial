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
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(request.POST)
            return redirect("projects")

    context = {'form':form}
    return render(request, "projects/project_form.html", context)

def updateProject(request,pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    # We are calling a instance of form that is prefilled with the instance of the project we want to edit
    
    if request.method == "POST":
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            print(request.POST)
            return redirect("projects")

    context = {'form':form}
    return render(request, "projects/project_form.html", context)

def deleteProject(request,pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("projects")
    context = {"object":project}
    return render(request, "projects/delete_template.html", context)