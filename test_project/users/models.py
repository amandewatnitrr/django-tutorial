from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # Deleting the Profile will also delete the user associated with it

    name = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(max_length=500, blank=True,null=True)
    username = models.CharField(max_length=200, blank=True,null=True)
    location = models.CharField(max_length=200, blank=True,null=True)
    short_intro = models.TextField(blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    profile_image = models.ImageField(blank=True,null=True,upload_to="profile-pics/",default="profile-pics/user-default.png")

    social_github = models.CharField(max_length=500,blank=True,null=True)
    social_twitter = models.CharField(max_length=500,blank=True,null=True)
    social_linkedin = models.CharField(max_length=500,blank=True,null=True)
    social_instagram = models.CharField(max_length=500,blank=True,null=True)
    social_website = models.CharField(max_length=500,blank=True,null=True)

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

class Skill(models.Model):
    owner = models.ForeignKey(Profile,null=True,on_delete=models.CASCADE,blank=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.name)

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