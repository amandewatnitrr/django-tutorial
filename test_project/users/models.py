from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # Deleting the Profile will also delete the user associated with it

    name = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(max_length=500, blank=True,null=True)
    short_intro = models.TextField(blank=True,null=True)
    profile_image = models.ImageField(blank=True,null=True,upload_to="profile-pics/",default="profile-pics/user-default.png")

    social_github = models.URLField(max_length=500,blank=True,null=True)
    social_twitter = models.URLField(max_length=500,blank=True,null=True)
    social_linkedin = models.URLField(max_length=500,blank=True,null=True)
    social_instagram = models.URLField(max_length=500,blank=True,null=True)
    social_website = models.URLField(max_length=500,blank=True,null=True)

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user.username)
