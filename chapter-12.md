<p align="justify">

# Reviews and Messages

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

    `single-project.html` - `projects` app

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

    Now, we need to start thinking about the calculation in order to calaculate the `vote_count` and the `vote_ratio`.

</p>