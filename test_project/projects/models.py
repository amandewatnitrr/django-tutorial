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
