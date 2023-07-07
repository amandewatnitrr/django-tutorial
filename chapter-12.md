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

- Now run the command `python3 manaage.py makemigrations` to make the migrations for changes in the model and than use the command `python3 manage.py migrate`.

</p>