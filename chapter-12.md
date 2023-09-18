<p align="justify">

# Reviews

- So, if youu pguys precisely remember that we have commented out the `owner` variable in `Review` model for `models.py`. What we are gonna do is we have to make sure that to a project each user has it's own unique single review only. So, within the `models.py` file in `projects` app, for the `Review` model we are gonna bind `owner` and `project` variable. And, also we will have to take care that the owner of the project can't review his own project.

- Make the following changes to `models.py` in `projects` app:

  `models.py` - `projects` app

    ```python
    from django.db import models
    import uuid
    from users.models import Profile

    # Create your models here.

    class Project(models.Model):
        owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
        title = models.CharField(max_length=200)
        description = models.TextField(null=True, blank=True)
        featured_image = models.ImageField(null=True, blank=True,default="default.jpg")
        # Setting the null=true means that it's not nessecary to have a description, it's an optional thing.
        # null by default is always set to false.
        # blank=True again means this field can be empty.
        demo_link = models.CharField(max_length=2000, null=True, blank=True)
        source_link = models.CharField(max_length=2000, null=True, blank=True)
        tags = models.ManyToManyField('Tag', blank=True)
        vote_total = models.IntegerField(default=0,null=True,blank=True)
        vote_ratio = models.IntegerField(default=0,null=True,blank=True)
        created =  models.DateTimeField(auto_now_add=True)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

        def __str__(self):
            return self.title
        
        class Meta:
            ordering = ["created"]

    class Review(models.Model):
        VOTE_TYPE = (
            ('up', 'Up Vote'),
            ('down', 'Down Vote')
        )
        owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
        project = models.ForeignKey(Project, on_delete=models.CASCADE)
        body = models.TextField(null = True, blank = True)
        value = models.CharField(max_length = 200, choices = VOTE_TYPE)
        created =  models.DateTimeField(auto_now_add=True)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

        class Meta:
            ordering = ["created"]
            unique_together = [["owner", "project"]]

        def __str__(self):
            return self.value
        
    class Tag(models.Model):
        name = models.CharField(max_length=255)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
        created =  models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.name

    ```

- Now run the command `python3 manaage.py makemigrations` to make the migrations for changes in the model and than use the command `python3 manage.py migrate`. And, this will add owner attribute to the `Reviews` model and make sure it's unique.

- Now, when you have made these changes if the owner of the project tries to write a review for the project that is owned by him only. The Review won't be accepted, you can see this in the below example.

  ![](/imgs/Screenshot%202023-07-11%20at%2011.20.08%20AM.png)

- Now, if you are having good look at `single-project.html` in the `templates` folder of `projects` app. Delete out, the unrequired portion of the code that is there, and edit it as follows:

    `single-project.html` - `templates` - `projects`

    ```Jinja

    {% extends 'main.html' %}

    {% block content %}

    <!-- Main Section -->
    <main class="singleProject my-md">
        <div class="container">
        <div class="layout">
            <div class="column column--1of3">
            <h3 class="singleProject__subtitle">Tools & Stacks</h3>
            <div class="singleProject__toolStack">

                {% for tag in project.tags.all %}
                <span class="tag tag--pill tag--sub tag--lg">
                <small>{{ tag }}</small>
                </span>
                {% endfor %}
                
            </div>
            {% if project.source_link %}
            <a class="singleProject__liveLink" href="{{ project.source_link }}" target="_blank"><i class="im im-external-link"></i>Source Code
            </a>
            {% endif %}

            </div>
            <div class="column column--2of3">
            <img class="singleProject__preview" src="{{ project.featured_image.url }}" alt="portfolio thumbnail" />
            <a href="profile.html" class="singleProject__developer">{{project.owner.name}}</a>
            <h2 class="singleProject__title">{{ project.title }}</h2>
            <h3 class="singleProject__subtitle">About the Project</h3>
            <div class="singleProject__info">
                {{ project.description }}
            </div>

            <div class="comments">
                <h3 class="singleProject__subtitle">Feedback</h3>
                <h5 class="project--rating">
                {{ project.vote_ratio }}% Postitive Feedback ({{ project.vote_total }} Vote{{ project.vote_total|pluralize:"s" }})
                </h5>

                <form class="form" action="#" method="POST">
                <!-- Textarea -->
                <div class="form__field">
                    <label for="formInput#textarea">Comments: </label>
                    <textarea class="input input--textarea" name="message" id="formInput#textarea"
                    placeholder="Write your comments here..."></textarea>
                </div>
                <input class="btn btn--sub btn--lg" type="submit" value="Comments" />
                </form>

                <div class="commentList">
                
                {% for review in project.review_set.all %}
                <div class="comment">
                    <a href="profile.html">
                    <img class="avatar avatar--md"
                        src="{{review.owner.profile_image.url}}" alt="user" />
                    </a>

                    <div class="comment__details">
                    <a href="{% url "user-profile" review.owner.id %}" class="comment__author">{{ review.owner.name }}</a>
                    <p class="comment__info">
                        {{ review.body }}
                    </p>
                    </div>
                </div>
                {% endfor %}
                
                </div>
            </div>
            </div>
        </div>
        </div>
        </div>
    </main>

    {% endblock content %}
    ```

    And, this should do it. Now, we are able to see the reviews on the website, but there's still one issue to be resolved that we haven't taken care of yet. That, the reviews with no body section, still will apppear, which doesn't make sense. So, we need to eliminate such reviews from getting displayed which have no body section. For, this purpose we add and if condition within the for loop as shown below:

    `single-project.html` - `templates` - `projects`

    ```Jinja
    {% extends 'main.html' %}

    {% block content %}

    <!-- Main Section -->
    <main class="singleProject my-md">
        <div class="container">
        <div class="layout">
            <div class="column column--1of3">
            <h3 class="singleProject__subtitle">Tools & Stacks</h3>
            <div class="singleProject__toolStack">

                {% for tag in project.tags.all %}
                <span class="tag tag--pill tag--sub tag--lg">
                <small>{{ tag }}</small>
                </span>
                {% endfor %}
                
            </div>
            {% if project.source_link %}
            <a class="singleProject__liveLink" href="{{ project.source_link }}" target="_blank"><i class="im im-external-link"></i>Source Code
            </a>
            {% endif %}

            </div>
            <div class="column column--2of3">
            <img class="singleProject__preview" src="{{ project.featured_image.url }}" alt="portfolio thumbnail" />
            <a href="profile.html" class="singleProject__developer">{{project.owner.name}}</a>
            <h2 class="singleProject__title">{{ project.title }}</h2>
            <h3 class="singleProject__subtitle">About the Project</h3>
            <div class="singleProject__info">
                {{ project.description }}
            </div>

            <div class="comments">
                <h3 class="singleProject__subtitle">Feedback</h3>
                <h5 class="project--rating">
                {{ project.vote_ratio }}% Postitive Feedback ({{ project.vote_total }} Vote{{ project.vote_total|pluralize:"s" }})
                </h5>

                <form class="form" action="#" method="POST">
                <!-- Textarea -->
                <div class="form__field">
                    <label for="formInput#textarea">Comments: </label>
                    <textarea class="input input--textarea" name="message" id="formInput#textarea"
                    placeholder="Write your comments here..."></textarea>
                </div>
                <input class="btn btn--sub btn--lg" type="submit" value="Comments" />
                </form>

                <div class="commentList">
                
                {% for review in project.review_set.all %}
                {% if review.body %}
                <div class="comment">
                    <a href="{% url "user-profile" review.owner.id %}">
                    <img class="avatar avatar--md"
                        src="{{review.owner.profile_image.url}}" alt="user" />
                    </a>

                    <div class="comment__details">
                    <a href="{% url "user-profile" review.owner.id %}" class="comment__author">{{ review.owner.name }}</a>
                    <p class="comment__info">
                        {{ review.body|linebreaksbr }}
                    </p>
                    </div>
                </div>
                {% endif %}
                {% endfor %}
                
                </div>
            </div>
            </div>
        </div>
        </div>
        </div>
    </main>

    {% endblock content %}
    ```

    And, now our project page has reviews which look something like this:

    ![](/imgs/Screenshot%202023-08-07%20at%2011.37.52%20AM.png)

    Also, if you observe carefully we also added a filter `linebreaksbr` to the `review.body`. This makes sure, that the reviews has all the spaces intact whereever present.

    Now, we want to actually be able to add some data via the comment form at the bottom. Now, as you can see we have a form down there which we can use to put in the comments. But, right now if you try submitting those form it doesn't seem to work. And shows something like this, on trying to submit the form.

    ![](/imgs/Screenshot%202023-08-10%20at%201.10.45%20PM.png)

    For this purpose we are going to make some changes to the `forms.py` within the `projects` app as follows:

    `forms.py` - `projects` app

    ```python
    from django.forms import ModelForm
    from .models import Project, Review
    from django import forms

    # Specifying ModelForm within the argument of the class, specifies that the given class is a Form.


    class ProjectForm(ModelForm):
        class Meta:
            model = Project
            fields = ["title","description","featured_image","demo_link","source_link","tags"]
            widgets = {
                'tags': forms.CheckboxSelectMultiple(),
            }

        def __init__(self, *args, **kwargs):
            super(ProjectForm, self).__init__(*args, **kwargs)

            self.fields["title"].widget.attrs.update({'class':'input','placeholder':'Add title'})
            self.fields["description"].widget.attrs.update({'class':'input','placeholder':'Add Description'})
            self.fields["tags"].widget.attrs.update({'class':'input--checkbox'})
            self.fields["demo_link"].widget.attrs.update({'class':'input','placeholder':'Add Demo Link'})
            self.fields["source_link"].widget.attrs.update({'class':'input','placeholder':'Add Source Link'})


    class ReviewForm(ModelForm):
        class Meta:
            model = Review
            fields = ['value','body']

            labels = {
                'value':"Put your vote",
                'body':"Add a Comment with your vote"
            }

        def __init__(self, *args, **kwargs):
            super(ReviewForm, self).__init__(*args, **kwargs)

            for name,field in self.fields.items():
                field.widget.attrs.update({"class":'input'})
    ```

    Once, this is done what we want to do next is add this to the `views.py` within the `projects app`.

    `views.py` - `projects` app

    ```python
    from django.shortcuts import render, redirect
    from django.db.models import Q
    from django.http import HttpResponse
    from .models import Project, Review, Tag
    from django.contrib.auth.decorators import login_required
    from .forms import ProjectForm, ReviewForm
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
        form = ReviewForm()
        context = {"project": projectObj,"tags":tags,"form":form}
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

    And it's done, now we can access this form within the `single-project.html` template inside the `projects` app.

    `single-project.html` -  `templates` - `projects` app

    ```Jinja
    {% extends 'main.html' %}

    {% block content %}

    <!-- Main Section -->
    <main class="singleProject my-md">
        <div class="container">
        <div class="layout">
            <div class="column column--1of3">
            <h3 class="singleProject__subtitle">Tools & Stacks</h3>
            <div class="singleProject__toolStack">

                {% for tag in project.tags.all %}
                <span class="tag tag--pill tag--sub tag--lg">
                <small>{{ tag }}</small>
                </span>
                {% endfor %}
                
            </div>
            {% if project.source_link %}
            <a class="singleProject__liveLink" href="{{ project.source_link }}" target="_blank"><i class="im im-external-link"></i>Source Code
            </a>
            {% endif %}

            </div>
            <div class="column column--2of3">
            <img class="singleProject__preview" src="{{ project.featured_image.url }}" alt="portfolio thumbnail" />
            <a href="profile.html" class="singleProject__developer">{{project.owner.name}}</a>
            <h2 class="singleProject__title">{{ project.title }}</h2>
            <h3 class="singleProject__subtitle">About the Project</h3>
            <div class="singleProject__info">
                {{ project.description }}
            </div>

            <div class="comments">
                <h3 class="singleProject__subtitle">Feedback</h3>
                <h5 class="project--rating">
                {{ project.vote_ratio }}% Postitive Feedback ({{ project.vote_total }} Vote{{ project.vote_total|pluralize:"s" }})
                </h5>

                <form class="form" action="{% url 'project' project.id %}" method="POST">
                <!-- Textarea -->
                {% csrf_token %}
                {% for field in form %}
                <div class="form__field">
                    <label for="formInput#textarea">{{field.label}}</label>
                    {{field}}
                </div>
                {% endfor %}
                <input class="btn btn--sub btn--lg" type="submit" value="Comments" />
                </form>

                <div class="commentList">
                
                {% for review in project.review_set.all %}
                {% if review.body %}
                <div class="comment">
                    <a href="{% url "user-profile" review.owner.id %}">
                    <img class="avatar avatar--md"
                        src="{{review.owner.profile_image.url}}" alt="user" />
                    </a>

                    <div class="comment__details">
                    <a href="{% url "user-profile" review.owner.id %}" class="comment__author">{{ review.owner.name }}</a>
                    <p class="comment__info">
                        {{ review.body|linebreaksbr }}
                    </p>
                    </div>
                </div>
                {% endif %}
                {% endfor %}
                
                </div>
            </div>
            </div>
        </div>
        </div>
        </div>
    </main>

    {% endblock content %}
    ```

    Here, the `action` is going to send a `POST` request back to the `project` page. And, now after making this changes we refresh the page, it looks something like this.

    ![](/imgs/Screenshot%202023-08-22%20at%206.57.19%20PM.png)

    Once, we are done with all of this, we need to start processing these comments. So, tha it gets saved. Also, we need to update the `vote_count` and the `vote_ratio`, once the votes have been updated.

    Also, don't forget to add the `{% csrf_token %}` above the `for` loop for the form in `single-project.html`, as I forgot to do it. We expect you don't repeat the same mistake.

    `views.py` - `projects` app

    ```python
    from django.shortcuts import render, redirect
    from django.db.models import Q
    from django.http import HttpResponse
    from .models import Project, Review, Tag
    from django.contrib.auth.decorators import login_required
    from django.contrib import messages
    from .forms import ProjectForm, ReviewForm
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
        form = ReviewForm()
        context = {"project": projectObj,"tags":tags,"form":form}

        if request.method == "POST":
            form = ReviewForm(request.POST)
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()

            # Update vote_count and vote_ratio
            messages.success(request,"Your review has succesfully been submitted.")
            return redirect('project', pk=projectObj.id)

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

    Once you have done the code changes as mentioned in `views.py` - `projects` app. Try, adding the comment from the website and, it should look something like this.

    ![](/imgs/Screenshot%202023-08-23%20at%204.26.27%20AM.png)

    Now, we need to start thinking about the calculation in order to calaculate the `vote_count` and the `vote_ratio`. For this purpose, we need to make some changes inside the `models.py` within the `projects` app. We are going to create a method for this purpose, that will handle this for us. And always remember that after making these changes to the `models.py`, you need to make migrations and migrate the changes to the database. We will also, make some changes to the `views.py`, within the projects app.

    `models.py` - `projects` app

    ```python
    from django.db import models
    import uuid
    from users.models import Profile

    # Create your models here.

    class Project(models.Model):
        owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
        title = models.CharField(max_length=200)
        description = models.TextField(null=True, blank=True)
        featured_image = models.ImageField(null=True, blank=True,default="default.jpg")
        # Setting the null=true means that it's not nessecary to have a description, it's an optional thing.
        # null by default is always set to false.
        # blank=True again means this field can be empty.
        demo_link = models.CharField(max_length=2000, null=True, blank=True)
        source_link = models.CharField(max_length=2000, null=True, blank=True)
        tags = models.ManyToManyField('Tag', blank=True)
        vote_total = models.IntegerField(default=0,null=True,blank=True)
        vote_ratio = models.IntegerField(default=0,null=True,blank=True)
        created =  models.DateTimeField(auto_now_add=True)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

        def __str__(self):
            return self.title
        
        class Meta:
            ordering = ["created"]

        @property
        def getVoteCount(self):
            reviews = self.review_set.all()
            upvotes = reviews.filter(value="up").count()
            totalvotes = reviews.count() #Gives the count how many values in our queryset

            ratio = (upvotes/totalvotes) * 100
            self.vote_total = totalvotes
            self.vote_ratio = ratio
            self.save()
            

    class Review(models.Model):
        VOTE_TYPE = (
            ('up', 'Up Vote'),
            ('down', 'Down Vote')
        )
        owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
        project = models.ForeignKey(Project, on_delete=models.CASCADE)
        body = models.TextField(null = True, blank = True)
        value = models.CharField(max_length = 200, choices = VOTE_TYPE)
        created =  models.DateTimeField(auto_now_add=True)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

        class Meta:
            ordering = ["created"]
            unique_together = [["owner", "project"]]

        def __str__(self):
            return self.value
        
    class Tag(models.Model):
        name = models.CharField(max_length=255)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
        created =  models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.name
    ```

    `views.py` - `projects` app

    ```python
    from django.shortcuts import render, redirect
    from django.db.models import Q
    from django.http import HttpResponse
    from .models import Project, Review, Tag
    from django.contrib.auth.decorators import login_required
    from django.contrib import messages
    from .forms import ProjectForm, ReviewForm
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
        form = ReviewForm()
        context = {"project": projectObj,"tags":tags,"form":form}

        if request.method == "POST":
            form = ReviewForm(request.POST)
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()

            # Update vote_count and vote_ratio
            projectObj.getVoteCount
            messages.success(request,"Your review has succesfully been submitted.")
            return redirect('project', pk=projectObj.id)

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

    Anytime, we trigger the `getVoteCount` function, all the calculation related tot the `vote_count` and the `vote_ratio` will be performed immediately, and than we are immediately going to update the instance. nOw, when we have this let's test this out. So, I created a project and added a review to it, and this is how it looks like.

    ![](/imgs/Screenshot%202023-08-23%20at%205.19.15%20AM.png)

    Now, in the frontend what we want is the projects to be sorted in the order of the ratings, the highest votes appearing first and, the least voted ones appearing later.

    `models.py` - `projects` app

    ```python
    from django.db import models
    import uuid
    from users.models import Profile

    # Create your models here.

    class Project(models.Model):
        owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
        title = models.CharField(max_length=200)
        description = models.TextField(null=True, blank=True)
        featured_image = models.ImageField(null=True, blank=True,default="default.jpg")
        # Setting the null=true means that it's not nessecary to have a description, it's an optional thing.
        # null by default is always set to false.
        # blank=True again means this field can be empty.
        demo_link = models.CharField(max_length=2000, null=True, blank=True)
        source_link = models.CharField(max_length=2000, null=True, blank=True)
        tags = models.ManyToManyField('Tag', blank=True)
        vote_total = models.IntegerField(default=0,null=True,blank=True)
        vote_ratio = models.IntegerField(default=0,null=True,blank=True)
        created =  models.DateTimeField(auto_now_add=True)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

        def __str__(self):
            return self.title
        
        class Meta:
            ordering = ["-vote_total","-vote_ratio","title"]

        @property
        def getVoteCount(self):
            reviews = self.review_set.all()
            upvotes = reviews.filter(value="up").count()
            totalvotes = reviews.count() #Gives the count how many values in our queryset

            ratio = (upvotes/totalvotes) * 100
            self.vote_total = totalvotes
            self.vote_ratio = ratio
            self.save()
            

    class Review(models.Model):
        VOTE_TYPE = (
            ('up', 'Up Vote'),
            ('down', 'Down Vote')
        )
        owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
        project = models.ForeignKey(Project, on_delete=models.CASCADE)
        body = models.TextField(null = True, blank = True)
        value = models.CharField(max_length = 200, choices = VOTE_TYPE)
        created =  models.DateTimeField(auto_now_add=True)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

        class Meta:
            ordering = ["created"]
            unique_together = [["owner", "project"]]

        def __str__(self):
            return self.value
        
    class Tag(models.Model):
        name = models.CharField(max_length=255)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
        created =  models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.name
    ```

    The next thing I want to make sure that user's that aren't logged in can't vote. And, than we also want to make sure that we can't vote our own project. For, this in the `models.py` file in `projects` app we will make a new method here.

    For, this purpose we want to get all the reviews, and than what we want to o is go to the values list, and get all the `owner__id`'s as a list.

    `models.py` - `projects` app

    ```python
    from django.db import models
    import uuid
    from users.models import Profile

    # Create your models here.

    class Project(models.Model):
        owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
        title = models.CharField(max_length=200)
        description = models.TextField(null=True, blank=True)
        featured_image = models.ImageField(null=True, blank=True,default="default.jpg")
        # Setting the null=true means that it's not nessecary to have a description, it's an optional thing.
        # null by default is always set to false.
        # blank=True again means this field can be empty.
        demo_link = models.CharField(max_length=2000, null=True, blank=True)
        source_link = models.CharField(max_length=2000, null=True, blank=True)
        tags = models.ManyToManyField('Tag', blank=True)
        vote_total = models.IntegerField(default=0,null=True,blank=True)
        vote_ratio = models.IntegerField(default=0,null=True,blank=True)
        created =  models.DateTimeField(auto_now_add=True)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

        def __str__(self):
            return self.title
        
        class Meta:
            ordering = ["-vote_total","-vote_ratio","title"]

        @property
        def reviewers(self):
            queryset = self.review_seta.all().values_list("owner__id", flat=True)
            return queryset

        @property
        def getVoteCount(self):
            reviews = self.review_set.all()
            upvotes = reviews.filter(value="up").count()
            totalvotes = reviews.count() #Gives the count how many values in our queryset

            ratio = (upvotes/totalvotes) * 100
            self.vote_total = totalvotes
            self.vote_ratio = ratio
            self.save()
            

    class Review(models.Model):
        VOTE_TYPE = (
            ('up', 'Up Vote'),
            ('down', 'Down Vote')
        )
        owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
        project = models.ForeignKey(Project, on_delete=models.CASCADE)
        body = models.TextField(null = True, blank = True)
        value = models.CharField(max_length = 200, choices = VOTE_TYPE)
        created =  models.DateTimeField(auto_now_add=True)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

        class Meta:
            ordering = ["created"]
            unique_together = [["owner", "project"]]

        def __str__(self):
            return self.value
        
    class Tag(models.Model):
        name = models.CharField(max_length=255)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
        created =  models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.name
    ```

    Make the changes mentioned below to `single-project.html` template in `projects` app.

    `single-project.html` - `templates` - `projects` app

    ```Jinja
    {% extends 'main.html' %}

    {% block content %}

    <!-- Main Section -->
    <main class="singleProject my-md">
        <div class="container">
        <div class="layout">
            <div class="column column--1of3">
            <h3 class="singleProject__subtitle">Tools & Stacks</h3>
            <div class="singleProject__toolStack">

                {% for tag in project.tags.all %}
                <span class="tag tag--pill tag--sub tag--lg">
                <small>{{ tag }}</small>
                </span>
                {% endfor %}
                
            </div>
            {% if project.source_link %}
            <a class="singleProject__liveLink" href="{{ project.source_link }}" target="_blank"><i class="im im-external-link"></i>Source Code
            </a>
            {% endif %}

            </div>
            <div class="column column--2of3">
            <img class="singleProject__preview" src="{{ project.featured_image.url }}" alt="portfolio thumbnail" />
            <a href="profile.html" class="singleProject__developer">{{project.owner.name}}</a>
            <h2 class="singleProject__title">{{ project.title }}</h2>
            <h3 class="singleProject__subtitle">About the Project</h3>
            <div class="singleProject__info">
                {{ project.description }}
            </div>

            <div class="comments">
                <h3 class="singleProject__subtitle">Feedback</h3>
                <h5 class="project--rating">
                {{ project.vote_ratio }}% Postitive Feedback ({{ project.vote_total }} Vote{{ project.vote_total|pluralize:"s" }})
                </h5>

                {% if request.user.profile.id in project.reviewers %}
                    <p>You have already submitted your review for this project.</p>
                {% elif request.user.profile == project.owner %}
                    <p>You cannot review your own project.</p>
                {% elif request.user.is_authenticated %}
                <form class="form" action="{% url 'project' project.id %}" method="POST">
                <!-- Textarea -->
                {% csrf_token %}
                {% for field in form %}
                <div class="form__field">
                    <label for="formInput#textarea">{{field.label}}</label>
                    {{field}}
                </div>
                {% endfor %}
                <input class="btn btn--sub btn--lg" type="submit" value="Comments" />
                </form>
                {% else %}
                <a href='{% url "login" %}?next={{request.path}}'>Login to leave a Review.</a>
                {% endif %}

                <div class="commentList">
                
                {% for review in project.review_set.all %}
                {% if review.body %}
                <div class="comment">
                    <a href="{% url "user-profile" review.owner.id %}">
                    <img class="avatar avatar--md"
                        src="{{review.owner.profile_image.url}}" alt="user" />
                    </a>

                    <div class="comment__details">
                    <a href="{% url "user-profile" review.owner.id %}" class="comment__author">{{ review.owner.name }}</a>
                    <p class="comment__info">
                        {{ review.body|linebreaksbr }}
                    </p>
                    </div>
                </div>
                {% endif %}
                {% endfor %}
                
                </div>
            </div>
            </div>
        </div>
        </div>
        </div>
    </main>

    {% endblock content %}
    ```

    Also, we had an issue so, far that we had been facing that our search bar for projects had a "/" appraring all the time, even when no search is made, it's because of a minor bug that we just resolved by making a small change to `projects.html` inside `projects` app.

    `projects.html` - `templates` - `projects` app

    ```Jinja
    {% extends 'main.html' %}

    {% block content %}

        <main class="projects">
            <section class="hero-section text-center">
            <div class="container container--narrow">
                <div class="hero-section__box">
                <h2>Search for <span>Projects</span></h2>
                </div>
        
                <div class="hero-section__search">
                <form id='searchForm' class="form" action="{% url 'projects'  %}" method="get">
                    <div class="form__field">
                    <label for="formInput#search">Search By Projects </label>
                    <input class="input input--text" id="formInput#search" type="text" name="search_query"
                        placeholder="Search by Project Title/Developer Name" value="{{search_query}}" />
                    </div>
        
                    <input class="btn btn--sub btn--lg" type="submit" value="Search" />
                </form>
                </div>
            </div>
            </section>
            <!-- Search Result: DevList -->
            <section class="projectsList">
            <div class="container">
                <div class="grid grid--three">

                {% for project in projects %}
                <div class="column">
                    <div class="card project">
                    <a href={% url 'project' project.id %} class="project">
                        <img class="project__thumbnail" src="{{ project.featured_image.url }}" alt="project thumbnail" />
                        <div class="card__body">
                        <h3 class="project__title"><a href={% url 'project' project.id %}>{{ project.title }}</a></h3>
                        <p><a class="project__author" href={% url 'user-profile' project.owner.id %}>By {{ project.owner.name }}</a></p>
                        <p class="project--rating">
                            <span style="font-weight: bold;">{{ project.vote_ratio }}%</span> Postitive
                            Feedback ({{ project.vote_total }} Vote{{ project.vote_total|pluralize:"s" }})
                        </p>
                        
                        <div class="project__tags">
                            {% for tag in project.tags.all %}
                            <span class="tag tag--pill tag--main">
                            <small>{{ tag }}</small>
                            </span>
                            {% endfor %}
                        </div>
                        </div>
                    </a>
                    </div>
                </div>
                {% endfor %}
        
        
                </div>
            </div>
            </section>
            
            {% include 'pagination.html' with queryset=projects custom_range=custom_range %}
            
        </main>

    {% endblock content %}
    ```

    Once, this changes have been done, login to the admin panel and delete all the previous reviews and bring the `vote_count` and `vote_ratio` to 0, to ensure avoiding any mathematical error. And, everything will work fine except for one.

    In the case, when you are logged out, when you click on `login to add your review`, you are directed to the login page that's not configured for this yet. And, for this we need to make some updates to the login form in `users` app. So, we move to `views.py` in `users` app and goto `loginUser` and make the following edits.

    `views.py` - `users` app

    ```python
    from django.shortcuts import redirect, render
    from django.contrib.auth import login, authenticate, logout
    from django.contrib.auth.decorators import login_required
    from django.contrib import messages
    from .forms import CustomUserCreationForm, ProfileForm, SkillForm
    from django.contrib.auth.models import User
    from .models import Profile
    from .utils import searchProfiles, paginateProfiles

    # Create your views here.

    def loginUser(request):
        page = 'login'
        context = {'page':page}
        if request.user.is_authenticated:
            return redirect("profiles")

        if request.method == "POST":
            username = request.POST["username"].lower()
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
                return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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
        custom_range, profiles =  paginateProfiles(request, profiles, 3)
        context = {"profiles":profiles,'search_query':search_query,'range':custom_range}
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

    And, we are done with the `reviews`.

# Messages

- For, this there's nothing to do with the projects app. So, we are not gonna touch it anyway. We will be dealing completely with the `users` app, for this. So, first let's move onto the `models.py` of `users` app, to make some changes. So, we start by making a new class `Message` here. Now, talking about `Message`, it's pretty obvious to guess 2 of the common attributes to expect here. First one, the `sender` and, other one the `receiver`. In order to do this add the `message` class model as shown below:

    `models.py` - `users` app

    ```python
    class Message(models.Model):
        sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
        # null here is set to true, cause a person with no account on the platform might also send a message to the person.
        reciever = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="messages")

        name = models.CharField(max_length=200, null=True ,blank=True)
        email = models.EmailField(max_length=200, null=True ,blank=True)
        subject = models.CharField(max_length=200, null=True ,blank=True)
        body = models.TextField()
        is_read = models.BooleanField(default=False, null=True)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
        created = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.subject
        
        # To order the messages by default. So, that when a user opens the inbox, they should first see the unread message.
        class Meta:
            ordering = ['is_read','-created']
            # Any message that is not read will be at the top and, the most recently created ones will also be at the top.
    ```

- Most of the things for the `reciever` and the `sender` is almost the same, except the fact that we add an extra attribute `related_name` to the receiver cause the recipient connection to the profile is going to interfere with our sender.
  
  - So, now what happens is when we go to the profile to access the profiles messages instead of doing something like `Profile.message_set`, we will just be able to directly write messages. So, this is how `Profile` model is going to connect to this. So, we need to add this to one of these atleast, because if we don't, then it will not allow us to have a connection to the profile modeltwice.
  
- Once, this is done and saved. The next thing we are going to do is, `makemigrationgs` and `migrate`. And, this should apply the migrations. Now, I want to register this with the admin panel. For this we will create a few messages, manually here. For this we need to make changes to the `admin.py` for the `users` app.

    `admin.py` - `users` app

    ```python
    from django.contrib import admin
    from .models import Profile, Skill, Message

    admin.site.register(Profile)
    admin.site.register(Skill)
    admin.site.register(Message)
    # Register your models here.
    ```

- So, now if you go back to the admin panel, we can see a message section clearly visible.

    ![](/imgs/Screenshot%202023-09-17%20at%204.42.41%20AM.png)

- So, before we start screating message or sending messages we want to have a template for our messages. For this we need to add the `inbox.html` template in `users` app. And, than make changes to `views.py` and `urls.py` file for `users` app.

    `views.py` - `users` app

    ```python

    # Add this function to the `views.py` in `users` app.

    @login_required(login_url="login")
    def inbox(request):
        context = {}
        return render(request,"users/inbox.html", context)
    ```

    `urls.py` - `users` app

    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path("login/", views.loginUser, name="login"),
        path("logout/", views.logoutUser, name="logout"),
        path("signup/", views.signupUser, name="signup"),

        path("", views.profiles, name="profiles"),
        path("profile/<str:pk>/", views.userProfile, name="user-profile"),
        
        path("account/", views.userAccount, name="account"),
        path("edit-account/", views.editAccount, name="edit-account"),

        path("add-skill/",views.addSkill, name="add-skill"),
        path("update-skill/<str:pk>/",views.updateSkill, name="update-skill"),
        path("delete-skill/<str:pk>/",views.deleteSkill, name="delete-skill"),

        path("inbox/",views.inbox,name="inbox"),
    ]
    ```

    So, now we have the URL Path and we have view in the template. And, now we can render this out. To, render this out we go into our navigation bar in the `root` directory `template` folder, and make the following changes.

    `navbar.html` - `templates` -`root`

    ```python
    {% load static %}
    <!-- Header Section -->
    <header class="header">
        <div class="container container--narrow">
        <a href="{% url 'projects' %}" class="header__logo">
            <img  class="logo" src = "{% static "images/logo.svg" %}"/>
        </a>
        <nav class="header__nav">
            <input type="checkbox" id="responsive-menu" />
            <label for="responsive-menu" class="toggle-menu">
            <span>Menu</span>
            <div class="toggle-menu__lines"></div>
            </label>
            <ul class="header__menu">
            <li class="header__menuItem"><a href="{% url "profiles" %}">Developers</a></li>
            <li class="header__menuItem"><a href="{% url "projects" %}">Projects</a></li>

            {% if request.user.is_authenticated %}
            <li class="header__menuItem"><a href="{% url 'inbox' %}">Inbox</a></li>
            <li class="header__menuItem"><a href="{% url 'account' %}">My Account</a></li>
            <li class="header__menuItem"><a href="{% url 'create-project' %}" class="btn btn--sub">Add Projects</a></li>
            <li class="header__menuItem"><a href="{% url 'logout' %}" class="btn btn--sub"><i class="fa-regular fa-right-from-bracket"></i> Logout</a></li>
            {% else %}
            <li class="header__menuItem"><a href="{% url 'login' %}" class="btn btn--sub">Login/SignUp</a></li>
            {% endif %}
            </ul>
        </nav>
        </div>
    </header>
    ```

    ![](/imgs/Screenshot%202023-09-17%20at%205.00.08%20AM.png)

    And, this is what we see, cause we haven't implemented any styling and all for this yet. So, we need to open up the template and fix a few things over here.

    `inbox.html` - `templates` - `users` app

    ```Jinja
    {% extends 'main.html' %}

    {% block content %}
    <!-- Main Section -->
    <main class="inbox my-xl">
    <div class="content-box">
        <h3 class="inbox__title">New Messages(<span>2</span>)</h3>
        <ul class="messages">
        <li class="message message--unread">
            <a href="message.html">
            <span class="message__author">Dennis Ivanov</span>
            <span class="message__subject">Working Opportunity for Web Design Company</span>
            <span class="message__date">May 31, 2021, 04:37 PM</span>
            </a>
        </li>
        <li class="message message--unread">
            <a href="message.html">
            <span class="message__author">Md. Shahriar Parvez</span>
            <span class="message__subject">Up for a Freelancing Project?</span>
            <span class="message__date">May 30, 2021, 07:47 PM</span>
            </a>
        </li>
        <li class="message">
            <a href="message.html">
            <span class="message__author">Sulamita Ivanov</span>
            <span class="message__subject">Another Opportunity for Side Income</span>
            <span class="message__date">May 29, 2021, 09:45 AM</span>
            </a>
        </li>
        </ul>
    </div>
    </main>
    {% endblock content %}

    ```

    And, this is what you would see.

    ![](/imgs/Screenshot%202023-09-17%20at%205.07.09%20AM.png)

    Now, when we have rendered the static template for the messages succesfully. Let' move to the admin panel and, add some actual messages. Once, we are done adding up these mesages to the database, move back to the `inbox.html` - `templates` in `users` app and `views.py` - `users` app to make some nessecary changes.

    `views.py` - `users` app

    ```python
    from django.shortcuts import redirect, render
    from django.contrib.auth import login, authenticate, logout
    from django.contrib.auth.decorators import login_required
    from django.contrib import messages
    from .forms import CustomUserCreationForm, ProfileForm, SkillForm
    from django.contrib.auth.models import User
    from .models import Profile, Message
    from .utils import searchProfiles, paginateProfiles

    # Create your views here.

    def loginUser(request):
        page = 'login'
        context = {'page':page}
        if request.user.is_authenticated:
            return redirect("profiles")

        if request.method == "POST":
            username = request.POST["username"].lower()
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
                return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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
        custom_range, profiles =  paginateProfiles(request, profiles, 3)
        context = {"profiles":profiles,'search_query':search_query,'range':custom_range}
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

    @login_required(login_url="login")
    def inbox(request):
        profile = request.user.profile
        messageRequests = profile.messages.all()
        unreadCount = messageRequests.filter(is_read=False).count() 
        context = {"messages":messageRequests,"unread":unreadCount}
        return render(request,"users/inbox.html", context)

    ```

    `inbox.html` - `templates` - `users` app

    ```Jinja
    {% extends 'main.html' %}

    {% block content %}
    <!-- Main Section -->
    <main class="inbox my-xl">
    <div class="content-box">
        <h3 class="inbox__title">New Messages(<span>{{unread}}</span>)</h3>
        <ul class="messages">
        {% for message in messages %}

        {% if message.is_read == False %}
            <li class="message message--unread">
        {% else %}
            <li class="message">
        {% endif %}
            <a href="{% url "message" message.id %}">
            <span class="message__author">{{message.name}}</span>
            <span class="message__subject">{{message.subject}}</span>
            <span class="message__date">{{message.created}}</span>
            </a>
        </li>
        {% endfor %}
        </ul>
    </div>
    </main>
    {% endblock content %}
    ```

    Once, we are done. This is how our Inbox would actually, look like.

    ![](/imgs/Screenshot%202023-09-17%20at%205.07.09%20AM.png)

    But, still we need to create a template to read the message. As, of now we can't read our messages. Also, unless we need to add the feature to mark the message as read and unread. So, we need a new template file for our `message`.

    `message.html` - `templates` - `users` app

    ```Jinja
    {% extends 'main.html' %}

    {% block content %}
    <!-- Main Section -->
    <main class="messagePage my-xl">
        <div class="content-box">
        <div class="message">
            <a class="backButton" href="{% url "inbox" %}"><i class="im im-angle-left"></i></a>
            <h2 class="message__subject">{{message.subject}}</h4>
            <a href="profile.html" class="message__author">{{message.name}}</a>
            <p class="message__date">{{message.created}}</p>
            <div class="message__body">
                {{message.body|linebreaksbr}}
            </div>
        </div>
        </div>
    </main>
    {% endblock content %}
    ```

    Add this to `views.py` within `users` app.

    `views.py` - `users` app

    ```python
    @login_required(login_url="login")
    def viewMessage(request,pk):
        profile = request.user.profile
        message = profile.messages.get(id=pk)
        if message.is_read == False:
            message.is_read = True
            message.save()
        context = {"message":message}
        return render(request,"users/message.html", context)
    ```

    `urls.py` - `users` app

    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path("login/", views.loginUser, name="login"),
        path("logout/", views.logoutUser, name="logout"),
        path("signup/", views.signupUser, name="signup"),

        path("", views.profiles, name="profiles"),
        path("profile/<str:pk>/", views.userProfile, name="user-profile"),
        
        path("account/", views.userAccount, name="account"),
        path("edit-account/", views.editAccount, name="edit-account"),

        path("add-skill/",views.addSkill, name="add-skill"),
        path("update-skill/<str:pk>/",views.updateSkill, name="update-skill"),
        path("delete-skill/<str:pk>/",views.deleteSkill, name="delete-skill"),

        path("inbox/",views.inbox,name="inbox"),
        path("message/<str:pk>/",views.viewMessage,name="message"),
    ]

    ```

    Once, done we can read the messages that we have received on our account. And, it would look something like this.

    ![](/imgs/Screenshot%202023-09-17%20at%208.00.41%20AM.png)

    Now, we are donw with all these stuff. We can read the messages that we have received from other users. But, theres still one issue that we still need to resolve, is that we can't send messages to others yet. Also, if you right now have a look at your own profile, you can send a message to your ownself as well, which doesn't make sense. But anyways, we will do this up at the end, we will first startup with the form to send messages to others.

    So, let's first startup witth a template for the `message_form.html` in the `users` app - `templates`.

    `message_form.html` - `users` - `templates`

    ```Jinja
    {% extends "main.html" %}

    {% block content %}
    <!-- Main Section -->
    <main class="formPage my-xl">
        <div class="content-box">
            <div class="formWrapper">
                <a class="backButton" href="{% url "user-profile" recipient.id %}"><i class="im im-angle-left"></i></a>
                <br>

                <form class="form" method="POST">
                    {% csrf_token %}
                    <!-- Input:Text -->
                    <div class="form__field">
                        <label for="formInput#text">Text Field: </label>
                        <input class="input input--text" id="formInput#text" type="text" name="text"
                            placeholder="Enter text" />
                    </div>
                    <input class="btn btn--sub btn--lg  my-md" type="submit" value="Submit" />
                </form>
            </div>
        </div>
    </main>
    {% endblock content %}
    ```

    We will make some changes later as well. But, keep this template here on hold. Now, move to `views.py` within the `users` app, and add this fucntion in there.

    `views.py` - `users` app

    ```python
    def createMessage(request, pk):
        recipient = Profile.objects.get(id=pk)
        context = {"recipient":recipient}
        return render(request,"users/message_form.html",context)
    ```

    Make changes to the `urls.py` for `users` app.

    `urls.py` - `users` app

    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path("login/", views.loginUser, name="login"),
        path("logout/", views.logoutUser, name="logout"),
        path("signup/", views.signupUser, name="signup"),

        path("", views.profiles, name="profiles"),
        path("profile/<str:pk>/", views.userProfile, name="user-profile"),
        
        path("account/", views.userAccount, name="account"),
        path("edit-account/", views.editAccount, name="edit-account"),

        path("add-skill/",views.addSkill, name="add-skill"),
        path("update-skill/<str:pk>/",views.updateSkill, name="update-skill"),
        path("delete-skill/<str:pk>/",views.deleteSkill, name="delete-skill"),

        path("inbox/",views.inbox,name="inbox"),
        path("message/<str:pk>/",views.viewMessage,name="message"),
        path("create-message/<str:pk>/",views.createMessage,name="create-message"),
    ]
    ```

    Once, we are done with all this, we need to be careful of one thing that, a user must not be able to send message to his ownself, so we need to make some changes to the `user-profile.html` template within `users` app.

    `user-profile.html` - `templates` - `users` app

    ```Jinja
    {% extends 'main.html' %}

    {% block content %}

    <!-- Main Section -->
    <main class="profile my-md">
        <div class="container">
        <div class="layout">
            <div class="column column--1of3">
            <div class="card text-center">
                <div class="card__body dev">
                <img class="avatar avatar--xl" src="{{ profile.profile_image.url }}" />
                <h2 class="dev__name">{{profile.name}}</h2>
                <p class="dev__title">{{profile.short_intro}}</p>
                <p class="dev__location">Based in {{profile.location}}</p>
                <ul class="dev__social">
                    {% if profile.social_github %}
                    <li>
                    <a title="Github" href="{{profile.social_github}}" target="_blank"><i class="fa-brands fa-github"></i></a>
                    </li>
                    {% endif %}
                    {% if profile.social_twitter %}
                    <li>
                    <a title="Twitter" href="{{profile.social_twitter}}" target="_blank"><i class="fa-brands fa-twitter"></i></a>
                    </li>
                    {% endif %}
                    {% if profile.social_linkedin %}
                    <li>
                    <a title="LinkedIn" href="{{profile.social_linkedin}}" target="_blank"><i class="fa-brands fa-linkedin"></i></a>
                    </li>
                    {% endif %}
                    {% if profile.social_website %}
                    <li>
                    <a title="Website" href="{{profile.social_website}}" target="_blank"><i class="fa-solid fa-link"></i></a>
                    </li>
                    {% endif %}
                </ul>
                <a href="{% url "create-message" profile.id %}" class="btn btn--sub btn--lg">Send Message </a>
                </div>
            </div>
            </div>
            <div class="column column--2of3">
            <div class="devInfo">
                <h3 class="devInfo__title">About Me</h3>
                <p class="devInfo__about">
                {{profile.bio}}
                </p>
            </div>
            <div class="devInfo">
                <h3 class="devInfo__title">Skills</h3>
                {% for skill in topskills %}
                <div class="devInfo__skills">
                    <div class="devSkill">
                    <h4 class="devSkill__title">{{skill.name}}</h4>
                    <p class="devSkill__info">
                        {{skill.description}}
                    </p>
                    </div>
                {% endfor %}
                </div>
                <div class="devInfo__otherSkills">
                    {% for skill in profile.skill_set.all %}
                    <span class="tag tag--pill tag--outline tag--lg">
                    <small>{{skill}}</small>
                    </span>
                    {% endfor %}
                </div>
                </div>
            </div>
            <div class="devInfo">
                <h3 class="devInfo__title">Projects</h3>
                <div class="grid grid--two">

                {% for project in profile.project_set.all %}
                <div class="column">
                    <div class="card project">
                    <a href="{% url 'project' project.id %}" class="project">
                        <img class="project__thumbnail" src="{{ project.featured_image.url }}" alt="project thumbnail" />
                        <div class="card__body">
                        <h3 class="project__title">{{project.title}}</h3>
                        <p><a class="project__author" href="profile.html">By {{project.owner.name}}</a></p>
                        <p class="project--rating">
                            <span style="font-weight: bold;">{{project.vote_ratio}}%</span> Postitive
                            Feedback ({{project.vote_total}} Vote{{project.vote_total|pluralize:"s"}})
                        </p>
                        <div class="project__tags">
                            {% for tag in project.tags.all %}
                            <span class="tag tag--pill tag--main">
                            <small>{{tag}}</small>
                            </span>
                            {% endfor %}
                        </div>
                        </div>
                    </a>
                    </div>
                </div>
                {% endfor %}

                </div>
            </div>
            </div>
        </div>
        </div>
    </main>

    {% endblock content %}
    ```

    Once, we are done. This is what it would look like:

    ![](/imgs/Screenshot%202023-09-19%20at%203.38.02%20AM.png)

- Now, let's continue making edits to the `forms.py` within `users` app, we do it by adding the below function to the file.

    `forms.py` - `users` app

    ```python
    from django.forms import ModelForm, TextInput, URLInput
    from django.contrib.auth.forms import UserCreationForm
    from django.contrib.auth.models import User
    from .models import Profile, Skill, Message



    class CustomUserCreationForm(UserCreationForm):
        class Meta:
            model = User
            fields = ['first_name','email','username','password1','password2']
            labels = {
                "first_name":"Name",
            }

        def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({"class":"input"})

    class ProfileForm(ModelForm):
        class Meta:
            model = Profile
            fields = ['name', 'email', 'username',
                    'location', 'bio', 'short_intro', 'profile_image',
                    'social_github', 'social_linkedin', 'social_twitter','social_website']

        def __init__(self, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})

    class SkillForm(ModelForm):
        class Meta:
            model = Skill
            fields = '__all__'
            exclude = ["owner"]

        def __init__(self, *args, **kwargs):
            super(SkillForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})

    class MessageForm(ModelForm):

        class Meta:
            model = Message
            fields = ["name", "email", "subject", "body"]

        def __init__(self, *args, **kwargs):
            super(MessageForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})
    ```

    Go back to the `views.py` file in `users` app.

    `views.py` - `users` app

    ```python
    from django.shortcuts import redirect, render
    from django.contrib.auth import login, authenticate, logout
    from django.contrib.auth.decorators import login_required
    from django.contrib import messages
    from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
    from django.contrib.auth.models import User
    from .models import Profile, Message
    from .utils import searchProfiles, paginateProfiles

    # Create your views here.

    def loginUser(request):
        page = 'login'
        context = {'page':page}
        if request.user.is_authenticated:
            return redirect("profiles")

        if request.method == "POST":
            username = request.POST["username"].lower()
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
                return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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
        custom_range, profiles =  paginateProfiles(request, profiles, 3)
        context = {"profiles":profiles,'search_query':search_query,'range':custom_range}
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

    @login_required(login_url="login")
    def inbox(request):
        profile = request.user.profile
        messageRequests = profile.messages.all()
        unreadCount = messageRequests.filter(is_read=False).count() 
        context = {"messages":messageRequests,"unread":unreadCount}
        return render(request,"users/inbox.html", context)

    @login_required(login_url="login")
    def viewMessage(request,pk):
        profile = request.user.profile
        message = profile.messages.get(id=pk)
        if message.is_read == False:
            message.is_read = True
            message.save()
        context = {"message":message}
        return render(request,"users/message.html", context)

    def createMessage(request, pk):
        recipient = Profile.objects.get(id=pk)
        form = MessageForm()
        context = {"recipient":recipient, "form":form}
        return render(request,"users/message_form.html",context)
    ```

    Now, we need to make some changes back again to the `message_form.html` in `users` app. Cause, we don't need to fill in some categories of input like name and mail if the sender is already logged in.

    `message_form.html` - `templates` - `users` app

    ```Jinja
    {% extends "main.html" %}

    {% block content %}
    <!-- Main Section -->
    <main class="formPage my-xl">
        <div class="content-box">
            <div class="formWrapper">
                <a class="backButton" href="{% url "user-profile" recipient.id %}"><i class="im im-angle-left"></i></a>
                <br>

                <form class="form" method="POST">
                    {% csrf_token %}

                    {% if request.user.is_authenticated == False %}
                        {% for field in form %}
                        <div class="form__field">
                            <label for="formInput#text">{{field.label}}</label>
                            {{field}}
                        </div>
                        {% endfor %}
                    {% else %}
                        
                    <div class="form__field">
                            <label for="formInput#text">{{form.subject.label}}</label>
                            {{form.subject}}
                        </div>

                        <div class="form__field">
                            <label for="formInput#text">{{form.body.label}}</label>
                            {{form.body}}
                        </div>

                    {% endif %}

                    <input class="btn btn--sub btn--lg  my-md" type="submit" value="Submit" />
                </form>
            </div>
        </div>
    </main>
    {% endblock content %}
    ```

    Now, we are ready, just need to make some few changes to the `views.py` inside `users` app.

    `views.py` - `users` app

    ```python
    from django.shortcuts import redirect, render
    from django.contrib.auth import login, authenticate, logout
    from django.contrib.auth.decorators import login_required
    from django.contrib import messages
    from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
    from django.contrib.auth.models import User
    from .models import Profile, Message
    from .utils import searchProfiles, paginateProfiles

    # Create your views here.

    def loginUser(request):
        page = 'login'
        context = {'page':page}
        if request.user.is_authenticated:
            return redirect("profiles")

        if request.method == "POST":
            username = request.POST["username"].lower()
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
                return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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
        custom_range, profiles =  paginateProfiles(request, profiles, 3)
        context = {"profiles":profiles,'search_query':search_query,'range':custom_range}
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

    @login_required(login_url="login")
    def inbox(request):
        profile = request.user.profile
        messageRequests = profile.messages.all()
        unreadCount = messageRequests.filter(is_read=False).count() 
        context = {"messages":messageRequests,"unread":unreadCount}
        return render(request,"users/inbox.html", context)

    @login_required(login_url="login")
    def viewMessage(request,pk):
        profile = request.user.profile
        message = profile.messages.get(id=pk)
        if message.is_read == False:
            message.is_read = True
            message.save()
        context = {"message":message}
        return render(request,"users/message.html", context)

    def createMessage(request, pk):
        recipient = Profile.objects.get(id=pk)
        form = MessageForm()

        try:
            sender = request.user.profile
            
        except:
            sender = None

        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = sender
                message.reciever = recipient
                message.recipient = Profile.objects.get(id=pk)

                if sender:
                    message.name = sender.name
                    message.email = sender.email
                message.save()

                messages.success(request, 'Your message was successfully sent!')
                return redirect('user-profile', pk=recipient.id)

        context = {'recipient': recipient, 'form': form}
        return render(request, 'users/message_form.html', context)
    ```

    And, now we are ready to send, recieve and read the messages. Now, a very small change we need to make, that the user shouldn't be able to send a message to his ownselff, and for that we need to add a condition to `user-profile.html` in `users` app for that.

    `user-profile.html` - `templates` - `users` app

    ```Jinja
    {% extends 'main.html' %}

    {% block content %}

    <!-- Main Section -->
    <main class="profile my-md">
        <div class="container">
        <div class="layout">
            <div class="column column--1of3">
            <div class="card text-center">
                <div class="card__body dev">
                <img class="avatar avatar--xl" src="{{ profile.profile_image.url }}" />
                <h2 class="dev__name">{{profile.name}}</h2>
                <p class="dev__title">{{profile.short_intro}}</p>
                <p class="dev__location">Based in {{profile.location}}</p>
                <ul class="dev__social">
                    {% if profile.social_github %}
                    <li>
                    <a title="Github" href="{{profile.social_github}}" target="_blank"><i class="fa-brands fa-github"></i></a>
                    </li>
                    {% endif %}
                    {% if profile.social_twitter %}
                    <li>
                    <a title="Twitter" href="{{profile.social_twitter}}" target="_blank"><i class="fa-brands fa-twitter"></i></a>
                    </li>
                    {% endif %}
                    {% if profile.social_linkedin %}
                    <li>
                    <a title="LinkedIn" href="{{profile.social_linkedin}}" target="_blank"><i class="fa-brands fa-linkedin"></i></a>
                    </li>
                    {% endif %}
                    {% if profile.social_website %}
                    <li>
                    <a title="Website" href="{{profile.social_website}}" target="_blank"><i class="fa-solid fa-link"></i></a>
                    </li>
                    {% endif %}
                </ul>
                {% if request.user.profile.id != profile.id %}
                <a href="{% url 'create-message' profile.id %}" class="btn btn--sub btn--lg">Send Message </a>
                {% endif %}
                </div>
            </div>
            </div>
            <div class="column column--2of3">
            <div class="devInfo">
                <h3 class="devInfo__title">About Me</h3>
                <p class="devInfo__about">
                {{profile.bio}}
                </p>
            </div>
            <div class="devInfo">
                <h3 class="devInfo__title">Skills</h3>
                {% for skill in topskills %}
                <div class="devInfo__skills">
                    <div class="devSkill">
                    <h4 class="devSkill__title">{{skill.name}}</h4>
                    <p class="devSkill__info">
                        {{skill.description}}
                    </p>
                    </div>
                {% endfor %}
                </div>
                <div class="devInfo__otherSkills">
                    {% for skill in profile.skill_set.all %}
                    <span class="tag tag--pill tag--outline tag--lg">
                    <small>{{skill}}</small>
                    </span>
                    {% endfor %}
                </div>
                </div>
            </div>
            <div class="devInfo">
                <h3 class="devInfo__title">Projects</h3>
                <div class="grid grid--two">

                {% for project in profile.project_set.all %}
                <div class="column">
                    <div class="card project">
                    <a href="{% url 'project' project.id %}" class="project">
                        <img class="project__thumbnail" src="{{ project.featured_image.url }}" alt="project thumbnail" />
                        <div class="card__body">
                        <h3 class="project__title">{{project.title}}</h3>
                        <p><a class="project__author" href="profile.html">By {{project.owner.name}}</a></p>
                        <p class="project--rating">
                            <span style="font-weight: bold;">{{project.vote_ratio}}%</span> Postitive
                            Feedback ({{project.vote_total}} Vote{{project.vote_total|pluralize:"s"}})
                        </p>
                        <div class="project__tags">
                            {% for tag in project.tags.all %}
                            <span class="tag tag--pill tag--main">
                            <small>{{tag}}</small>
                            </span>
                            {% endfor %}
                        </div>
                        </div>
                    </a>
                    </div>
                </div>
                {% endfor %}

                </div>
            </div>
            </div>
        </div>
        </div>
    </main>

    {% endblock content %}
    ```

    And that's it for this section of the tutorial.

</p>
