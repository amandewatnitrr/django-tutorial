<p align="justify">

# Search and Pagination

- So, let's pick from where we left off. Move to the `views.py` in `users` app. There go to the `profiles` function and add the following stuff:

    `views.py` - `users` app

    ```python
    # Let's make some small changes to the profile fucntion in the views.py of the users app.
    def profiles(request):
        search_query = ""
        if request.GET.get("search_query"): # If there's a given search query, this block of if statement will be executed.
            search_query = request.GET.get("search_query")
            print("Searched: ",search_query)
        profiles = Profile.objects.all()
        context = {"profiles":profiles}
        return render(request, "users/profiles.html",context)
    ```

    With this code we just tested out if our search_query is accessible by yhe backend or not. Once, you save and search something, you can see the search_quesry being displayed here.

    ![](/imgs/Screenshot%202023-05-22%20at%203.59.00%20PM.png)

    So, now we are going to use something called Q Look-up, so we can actually search by multiple parameters. But before we do that we just want to test the fitler here, and so for this purpose we will use the standard django query here, and we will filter it by `name__icontains`, so as to make it it non case-sensitive, and than pass `search_query` to it. So, ig there's no search query we are gonna get all the profiles, and if we do have a value, we will run a search in that case.

    `views.py` - `users` app

    ```python
    def profiles(request):
        search_query = ""
        if request.GET.get("search_query"): # If there's a given search query, this block of if statement will be executed.
            search_query = request.GET.get("search_query")
            print("Searched: ",search_query)
        profiles = Profile.objects.filter(name__icontains=search_query)
        context = {"profiles":profiles}
        return render(request, "users/profiles.html",context)
    ```

    Now, when we search for something, let's say `Ayush`, we get his profile.

    ![](/imgs/Screenshot%202023-05-22%20at%207.15.12%20PM.png)

    But, now the issue here is that as you can see that as we submit the search query, the search is done but the query is removed. So, we need to fix that and for that we need to send the query to the template itself. So, we edit the `views.py` for `users` app as follows:

    `views.py` - `users` app

    ```python
    # Edited code for profiles function in views.py
    def profiles(request):
        search_query = ""
        if request.GET.get("search_query"): # If there's a given search query, this block of if statement will be executed.
            search_query = request.GET.get("search_query")
            print("Searched: ",search_query)
        profiles = Profile.objects.filter(name__icontains=search_query)
        context = {"profiles":profiles,'search_query':search_query}
        return render(request, "users/profiles.html",context)
    ```

    Let's imagine what if now I want to search someone based on there certain description. If we just add another `search_query` parameter, it won't work as it's more like `AND` operation of both the search queries, which is not what we want. And, for this purpose we will be using a Q-Look Up, it basically helps us extend our searches. Add the library `from django.db.models import Q` to the python file, before making the below mentioned changes:

    `views.py` - `users` app

    ```python
    def profiles(request):
        search_query = ""
        if request.GET.get("search_query"): # If there's a given search query, this block of if statement will be executed.
            search_query = request.GET.get("search_query")
            print("Searched: ",search_query)
        profiles = Profile.objects.filter(Q(name__icontains=search_query) | Q(short_intro__icontains=search_query))
        context = {"profiles":profiles,'search_query':search_query}
        return render(request, "users/profiles.html",context)
    ```

    And now if we searh something related to there intro, we will get something like this.

    ![](/imgs/Screenshot%202023-05-23%20at%2012.41.27%20PM.png)

- Now, we want to search developers by their skills. This would be a bit different because it's hs a parent-child relationship with the `Profile` model.

    For that let's again make some changes to the `views.py` of `users` app.

    `views.py` - `users` app

    ```python
    # Changes in views.py for users app.
    def profiles(request):
        search_query = ""
        if request.GET.get("search_query"): # If there's a given search query, this block of if statement will be executed.
            search_query = request.GET.get("search_query")
            print("Searched: ",search_query)
        
        skills = Skill.objects.filter(name__iexact=search_query)

        profiles = Profile.objects.filter(
            Q(name__icontains=search_query) | 
            Q(short_intro__icontains=search_query) |
            Q(skill__in=skills)
        )
        context = {"profiles":profiles,'search_query':search_query}
        return render(request, "users/profiles.html",context)
    ```

    In the above code, we are taking the user query in the `skills` variable and looking for it. And than we do the same thing in the profile object. But, than there's a issue, before we even run the search we see duplicates of the profiles already like this:

    ![](/imgs/Screenshot%202023-05-23%20at%201.02.41%20PM.png)

    In order to avoid this duplication of the profiles, we are gonna use `distinct` function, so we return back one table for each instance or one table object that's it. And hence, the problem is solved.

    `views.py` - `users` app

    ```python
    def profiles(request):
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
        context = {"profiles":profiles,'search_query':search_query}
        return render(request, "users/profiles.html",context)
    ```

    And, now we get only one-instance of each user, as shown below:

    ![](/imgs/Screenshot%202023-05-23%20at%201.12.22%20PM.png)

- But, now as you can see the code has started to look more and more messy, over the period as we add things to the profile page, so what we wanna do is keep the search function seprate from the `profile` views.

    For this purpose we are creating a new file `utils.py` within the `users` app. And this can be called whenever we want to.

    `utils.py` - `users` app

    ```python
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
    ```

    `views.py` - `users` app

    ```python
    # Update the views.py for users app as follows:
    from django.shortcuts import redirect, render
    from django.contrib.auth import login, authenticate, logout
    from django.contrib.auth.decorators import login_required
    from django.contrib import messages
    from .forms import CustomUserCreationForm, ProfileForm, SkillForm
    from django.contrib.auth.models import User
    from .models import Profile
    from .utils import searchProfiles

    # Create your views here.

    def loginUser(request):
        page = 'login'
        context = {'page':page}
        if request.user.is_authenticated:
            return redirect("profiles")

        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]

            try:
                user = User.objects.get(username=username)
                # Checking if the username with given username exists in database orr not

            except:
                messages.error(request,"Username not found")

            user = authenticate(request, username=username, password=password)
            # The above command checks if the credentials given for the existing user is correct or not.

            if user is not None:
                login(request, user)
                return redirect('profiles')
            else:
                messages.error(request,"Username or Password Incorrect...")

        return render(request, "users/login_register.html",context)


    def logoutUser(request):
        logout(request)
        messages.success(request,"User Logged Out...")
        return redirect("login")

    def signupUser(request):
        page = 'signup'
        form = CustomUserCreationForm()
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                print("User Creation Initiated..")
                user = form.save(commit=False) # Here we hold a single instance of the form
                user.username = user.username.lower()
                print(user)
                user.save()
                messages.success(request,"User Account Created")

                login(request, user)
                return redirect("edit-account")

        context = {'page':page,'form':form}
        return render(request, "users/login_register.html", context)


    def profiles(request):
        profiles, search_query = searchProfiles(request) 
        context = {"profiles":profiles,'search_query':search_query}
        return render(request, "users/profiles.html",context)

    def userProfile(request, pk):
        profile = Profile.objects.get(id=pk)

        topskills = profile.skill_set.exclude(description__exact="")
        otherskills = profile.skill_set.filter(description="")

        context = {'profile':profile,'topskills':topskills,"otherskills":otherskills}
        return render(request, "users/user-profile.html",context)

    @login_required(login_url="login")
    def userAccount(request):
        profile = request.user.profile
        skills = profile.skill_set.all().order_by('-description')
        projects = profile.project_set.all()

        context = {'profile':profile,'skills':skills,"projects":projects}
        return render(request,"users/account.html", context)

    @login_required(login_url="login")
    def editAccount(request):
        profile = request.user.profile
        form = ProfileForm(instance=profile)

        if request.method == "POST":
            form = ProfileForm(request.POST,request.FILES,instance=profile)

            if form.is_valid():
                form.save()
                messages.success(request,"Account Updated Successfully...")
                return redirect("account")

        context = {'form':form}
        return render(request,"users/profile_form.html",context)

    @login_required(login_url="login")
    def addSkill(request):
        profile = request.user.profile
        form = SkillForm()

        if request.method == "POST":
            form = SkillForm(request.POST)
            if form.is_valid():
                skill = form.save(commit=False)
                skill.owner = profile
                skill.save()
                messages.success(request,"New Skill Added")
                return redirect("account")
        
        context = {'form':form}
        return render(request,"users/skill_form.html",context)

    @login_required(login_url="login")
    def updateSkill(request, pk):
        profile = request.user.profile
        skill = profile.skill_set.get(id=pk)
        form = SkillForm(instance=skill)

        if request.method == "POST":
            form = SkillForm(request.POST,instance=skill)
            if form.is_valid():
                form.save()
                messages.success(request,"Skill Updated Successfully")
                return redirect("account")
        
        context = {'form':form}
        return render(request,"users/skill_form.html",context)

    @login_required(login_url="login")
    def deleteSkill(request, pk):
        profile = request.user.profile
        skill = profile.skill_set.get(id=pk)
        if request.method == "POST":
            skill.delete()
            messages.success(request,"Skill Deleted Successfully")
            return redirect("account")
        
        context = {"object":skill}
        return render(request,"delete-template.html",context)
    ```

    And, now the code looks completely fine and, perfect. Now, we need to move to the projects and, do the same thing over there.

  - First of all, we start with some minor changes to `projects.py` file, where we do some changes on the `input` field as follows:

    `projects.py` - `projects` app

    ```python
    <input class="input input--text" id="formInput#search" type="text" name="search_query"
                    placeholder="Search by Project Title" value={{search_query}} />
    ```

    `views.py` - `projects` app

    ```python
    # Update the projects view as follows:
    from django.shortcuts import render, redirect
    from django.db.models import Q
    from django.http import HttpResponse
    from .models import Project, Review, Tag
    from django.contrib.auth.decorators import login_required
    from .forms import ProjectForm
    from .utils import searchProjects


    def projects(request):
        # return HttpResponse("Here are our Projects")
        # The above statement gives the specified Argument as an HTTpResponse.
        projects, search_query = searchProjects(request)
        context = {"projects": projects, 'search_query': search_query}
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
    ```

    Create a new file `utils.py` within the projects app and put in the following `searchProjects` function in there:

    `utils.py` - `projects` app

    ```python
    from .models import Project, Tag
    from django.db.models import Q


    def searchProjects(request):
        search_query = ""
        if request.GET.get("search_query"): # If there's a given search query, this block of if statement will be executed.
            search_query = request.GET.get("search_query")
            print("Searched: ",search_query)

        tags = Tag.objects.filter(name__icontains=search_query)


        projects = Project.objects.distinct().filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(owner__name__icontains=search_query) |
            Q(tags__in=tags)
        )
        return projects, search_query
    ```

    And, the search is read and, going finally.

    ![](/imgs/Screenshot%202023-05-30%20at%202.54.22%20PM.png)

</p>
