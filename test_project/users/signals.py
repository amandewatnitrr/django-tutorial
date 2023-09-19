# Imports for the Signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(user=user, username=user.username, email=user.email, name=user.first_name)

        subject = "Welcome to Devsearch"
        message = "Thanks for Siging Up :D"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )
    print("Profile Saved Succesfully... ")

def updateProfile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
    print("Profile Updated...")

def profileDeleted(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    print("Profile Deleted...")

post_save.connect(createProfile, sender=User)
post_save.connect(updateProfile, sender=Profile)
post_delete.connect(profileDeleted, sender=Profile)