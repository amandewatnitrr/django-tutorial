from .models import Profile, Skill
from django.db.models import Q


def searchProfiles(request):
    search_query = ""
    if request.GET.get("search_query"): # If there's a given search query, this block of if statement will be executed.
        search_query = request.GET.get("search_query")
        print("Searched: ",search_query)
    
    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
    )
    return profiles, search_query