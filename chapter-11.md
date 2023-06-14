<p align="justify">

# Pagination

- Now, when we are done with the `Search` part of the project, let's move to pagination. So, when there are more number of profiles or projects, we need to limit the number of projects or profiles on a single page, something like 10 results per page or 20. For that, we want to navigate through different pages.

- So, let's first deal with some stuff before that. Let's order the contents of the projects in the order of the oldest created first. For this move to the `models.py` inside `projects` app, and add the following to the `Project` model.

    `Project` Model - `models.py` - `projects` app

    ```python
    class Meta:
        ordering = ["created"]
        # making it -created will have the new ones first
    ```

- To actually, paginate the contents of the page, django gives us a `Paginator` class which makes thing lot easier for us. For this, we will move to `views.py` in the `projects` folder. Firstly import the `Paginator` class by using `from django.core.paginator import Paginator`, and than update as follows:

    Update `views.py` - `projects` app

    ```python
    def projects(request):
        # return HttpResponse("Here are our Projects")
        # The above statement gives the specified Argument as an HTTpResponse.
        projects, search_query = searchProjects(request)

        page = 1
        results = 3 # This will show only 3 results per page.
        paginator = Paginator(projects, results)

        projects = paginator.page(page)

        context = {"projects": projects, 'search_query': search_query}
        return render(request, "projects/projects.html", context)
    ```

    With this we will get output for the 1st page after pagination, but we don't have buttons, so for this we need to change few things.

    `views.py` - `projects` app

    ```python
    def projects(request):
        # return HttpResponse("Here are our Projects")
        # The above statement gives the specified Argument as an HTTpResponse.
        projects, search_query = searchProjects(request)

        page = request.GET.get("page") # But the page needs to be an integer here.
        results = 3
        paginator = Paginator(projects, results)

        projects = paginator.page(page)

        context = {"projects": projects, 'search_query': search_query}
        return render(request, "projects/projects.html", context)
    ```

    As, the variable page is not an integer here, naturally we will get an error, that looks something like this.

    ![](/imgs/Screenshot%202023-06-08%20at%201.06.13%20PM.png)

    Well, that's not a big issue, if you are worried just change the URL as follows on your browser `http://localhost:8000/?page=1`. And, things should be clearly visible now. But it's still a warning kinda thing for this we again need to import some more things as `from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage` and update the `projects` view as follows:

    `views.py` - `projects` app

    ```python
    def projects(request):
        # return HttpResponse("Here are our Projects")
        # The above statement gives the specified Argument as an HTTpResponse.
        projects, search_query = searchProjects(request)

        page = request.GET.get("page")
        results = 3
        paginator = Paginator(projects, results)

        try:
            projects = paginator.page(page)
        
        except PageNotAnInteger:
            page = 1
            projects = paginator.page(page)

        except EmptyPage:
            page = paginator.num_pages
            projects = paginator.page(page)

        leftIndex =  int(page) - 4
        rightIndex = int(page) + 5

        if leftIndex < 1:
            leftIndex = 1
        
        if rightIndex > paginator.num_pages
            rightIndex = paginator.num_pages
 
        custom_range = range(leftIndex,rightIndex)

        context = {"projects": projects, 'search_query': search_query, 'paginator': paginator, 'range':custom_range}
        return render(request, "projects/projects.html", context)
    ```

    Here, we implement `try` and `catch` to implement. In case, when we don't have a search parameter, it will by default show the 1st page of the projects. And, if you try visiting a page that doesn't exist, it will redirect you to the last page. Now, as for swtiching b/w the pages we need to have buttons for the paginators and for that we need to make something more like a sliding window of the paginator button, to make navigation throught the pages easier. So, in order to do that we define, `leftIndex` and `rightIndex`. The `leftIndex` is like the lower limit of the page navigator, while the `rightIndex` is more like the upper limit of the page navigator. And, hence even if we have insane number of pages, it will not create a mess as it will keep sliding the lower and the upper limits of the paginator.

    Now, let's make some changes to the `projects.html` template in `projects` app.

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
                <form class="form" action="{% url 'projects'  %}" method="get">
                    <div class="form__field">
                    <label for="formInput#search">Search By Projects </label>
                    <input class="input input--text" id="formInput#search" type="text" name="search_query"
                        placeholder="Search by Project Title" value={{search_query}} />
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

            {% if projects.has_other_pages %}
            <div class="pagination">
            <ul class="container">
                {% if projects.has_previous %}
                <li><a href="?page={{projects.previous_page_number}}" class="btn btn--disabled">&#10094; Prev</a></li>
                {% endif %}
                {% for page in range %}
                <li><a href="?page={{page}}" class="btn page-link">{{ page }}</a></li>
                {% endfor %}
                {% if projects.has_next %}
                <li><a href="?page={{projects.next_page_number}}" class="btn btn--disabled">Next &#10095;</a></li>
                {% endif %}
            </ul>
            </div>
            {% endif %}
        
            
        </main>

    {% endblock content %}
    ```

    And, finally you would see output to be something like this:

    ![](/imgs/Screenshot%202023-06-14%20at%209.39.38%20AM.png)

    Now, the issue will have to deal is that the `projects` view is really kinda getting messy, so we need to make the code more readable by cleaning up the mess we created, and for that we gonna take the help of `utils.py` in the `projects` app. So, we create a new function inside `utils.py` in `projects` app. Along, with that we need to update the `views.py` for `projects` in `projects` app as well.

    `utils.py` - `projects` app

    ```python
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    def paginateProjects(request, projects, results):

        page = request.GET.get("page")
        results = 3
        paginator = Paginator(projects, results)

        try:
            projects = paginator.page(page)
        
        except PageNotAnInteger:
            page = 1
            projects = paginator.page(page)

        except EmptyPage:
            page = paginator.num_pages
            projects = paginator.page(page)

        leftIndex =  int(page) - 4
        rightIndex = int(page) + 5

        if leftIndex < 1:
            leftIndex = 1
        
        if rightIndex > paginator.num_pages:
            rightIndex = paginator.num_pages + 1

        custom_range = range(leftIndex,rightIndex)

        return custom_range, projects
    ```

    `views.py` - `projects` app

    ```python
    # Update projects views as follows:

    def projects(request):
        # return HttpResponse("Here are our Projects")
        # The above statement gives the specified Argument as an HTTpResponse.
        projects, search_query = searchProjects(request)

        custom_range, projects =  paginateProjects(request, projects, 3)

        context = {"projects": projects, 'search_query': search_query, 'range':custom_range}
        return render(request, "projects/projects.html", context)
    ```

    And, everything works fine. But, here comes a li'l important part now.

</p>
