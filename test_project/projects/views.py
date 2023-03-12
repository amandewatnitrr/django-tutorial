from django.shortcuts import render
from django.http import HttpResponse

projectsList = [
    {
        'id': '1',
        'title': 'Ecommerce Website',
        'description': 'Fully functional ecommerce website'
    },
    {
        'id': '2',
        'title': 'Portfolio Website',
        'description': 'A personal website to write articles and display work'
    },
    {
        'id': '3',
        'title': 'Social Network',
        'description': 'An open source project built by the community'
    }
]


def projects(request):
    # return HttpResponse("Here are our Projects")
    # The above statement gives the specified Argument as an HTTpResponse.
    msg = "This is Projects Page."
    number = 11
    context = {"msg":msg, "number":number, "projects": projectsList}
    return render(request, "projects/projects.html", context)

def project(request, pk):
    projectObj = None
    context = None
    for i in projectsList:
        if i['id'] == pk:
            projectObj = i
            context = {"project":projectObj}
    return render(request, "projects/single-project.html",context)
