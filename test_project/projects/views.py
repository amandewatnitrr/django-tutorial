from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Project, Review, Tag
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm
from .utils import searchProjects, paginateProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def projects(request):
    # return HttpResponse("Here are our Projects")
    # The above statement gives the specified Argument as an HTTpResponse.
    projects, search_query = searchProjects(request)

    custom_range, projects =  paginateProjects(request, projects, 3)

    context = {"projects": projects, 'search_query': search_query, 'range':custom_range}
    return render(request, "projects/projects.html", context)

def project(request, pk):
    projects = Project.objects.all()
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    context = {"project": projectObj,"tags":tags}
    return render(request, "projects/single-project.html",context)

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm
    
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            print(request.POST)
            return redirect("account")

    context = {'form':form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
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

@login_required(login_url="login")
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("account")
    context = {"object":project}
    return render(request, "projects/delete_template.html", context)