<strong>
<p align="justify">

# Signals in Django

- Before, learning and actually learning about django, let's see where signals are useful. So, imagine this scenario if someone visits our website and go to the registration form, fill it and hit the button and, than they are added to the database. Well, on submit we want to fire off somekind of action, that sends out an email to the user and it let's them know that they now have an account with some kind of welcome message. Well, this is the kind of example a signal maybe very useful.

- Signals are just a way of listening to actions that ar performed in our application and they can fire off certain events. So, here we create some kind of a listner for that action and we would listen to every single time a new user was added to the database.

- So, signals are comprised of senders and receivers. So, the sender would be that action or that instance of that user being created and the receiver would be the function that hear that action and than fires off a different action.

![](/imgs/Signals1.png)

- So, in the example we have a sender above and down the receiver. So, the sender is a user model here. And, in this case whenever this sender on the left triggers off every time we trigger the same method on a user. So, what we can do is we can create these recievers and one type of receiver we can create is a piece of receiver that triggers before the action is created.

- So, right before save is completed, or that action is run, we can go ahead and trigger a receiver, and that receiver can trigger a function that does whatever we want to do at this point. And the other receiver we call the POST save method, which would trigeer after the user was created. So, this is where we can trigger an action and send an email. So, we don't have to write this logic anywhere in `view.py`. We just create these listeners and listen for events.

- Now what if we want to update the admin, and let an admin in our application know a user was deleted. So, everytime a user deletes there account, we send out somekind of email or some kind of alert message to maybe the administrator of that website. So, in this case the sender is still the user model, and we're listening for delete method here. So, anytime a user is deleted we can trigger an action that triggers before the user is deleted, or after the user is deleted.

- So, let's say a user gets deleted, and we just want to gfire off an email, and send it to that user. So, they're very convinent. Let's go ahead and see this in implementation, how this actually works out.

- We will be writing the `Signals` directly into the `models.py` file of `users` app. And some point, we will seprate it into it's own file. But for now, we will just directly write it down within `models.py` only. So, first of all we will create some kind of receiver and sender that's going to fire off any time the save method is called on the user profile.

> **_NOTE:_** <br><br>
> So, there is something that we wanna keep in mind before proceeding further with the course. We will discuss about *argsand **kwargs in Python. <br> <br>
> We use the “wildcard” or “*” notation like this – *args OR **kwargs – as our function’s argument when we have doubts about the number of  arguments we should pass in a function. <br> <br>
> *args in function definitions in Python is used to pass a variable number of arguments to a function. It is used to pass a non-keyworded, variable-length argument list. <br><br>
> **kwargs in function definitions in Python is used to pass a keyworded, variable-length argument list. We use the name kwargs with the double star. The reason is that the double star allows us to pass through keyword arguments (and any number of them). <br><br>
> A keyword argument is where you provide a name to the variable as you pass it into the function. One can think of the kwargs as being a dictionary that maps each keyword to the value that we pass alongside it. That is why when we iterate over the kwargs there doesn’t seem to be any order in which they were printed out.

- `models.py` - `users` app

  ```python

  # Added to the end of previous content of models.py of users app

  # Imports for the Signals
  from django.db.models.signals import post_save, post_delete
  # This method right here is gonna trigger anytime a model is saved already, after it gets saved.

  # Receiver for POST Save
  def profileUpdated(sender, instance, created, **kwargs):
      print("Profile Saved Succesfully... ")

  def profileDeleted(sender, instance, created, **kwargs):
      print("Profile Deleted...")

  post_save.connect(profileUpdated, sender=Profile)
  post_delete.connect(profileDeleted, sender=Profile)
  ```

  - `sender` is going to be the model that actually sends this.
  - `instance` will be the object of the model that actually triggered this.
  - `created` argument here is goin to be true or false, if a new user was added, it would be true, else it would be false, if it's an update.
  - `post_save.connect(profileUpdated, sender=Profile)` actually means that whenever afterr the profile is saved and is reported by the Profile model about the change, it will show this message.

  - Now, when we change something on one fo the profiles, we can see the message `Profile Saved Successfully..` is being displayed on the termianl.

  ![](/imgs/Screenshot%202023-04-27%20at%205.14.40%20AM.png)

  - Now, let's see what really happened here. So, the profile was updated and than we were conneced to it. The sender here is the `Profile` Model. So, anytimme the profile is updated or added to the database, we just fire ooff this fucntion.

  - And, now the same way if we delete someone's profile, the function associated with `post_delete` will be trigerred.

  - So, from here on we will be using something called decorator from here onwards, instead of having these `Signals` within other file. We are doing so as to keep the code seprated.

- We can do the same exact thing using the decorator, let's see how we are gonna do it. But before, doing thta comment out the previous `post_save` and `post_delete` lines before trying to implement this one.

  `models.py` - `usres` app

  ```python
  # Imports for the Signals
  from django.db.models.signals import post_save, post_delete
  from django.dipatch import receiever
  # This method right here is gonna trigger anytime a model is saved already, after it gets saved.

  # Receiver for POST Save
  @receiver(post_save, sender=Profile)
  def profileUpdated(sender, instance, created, **kwargs):
      print("Profile Saved Succesfully... ")

  
  @receiver(post_delete, sender=Profile)
  def profileDeleted(sender, instance, created, **kwargs):
      print("Profile Deleted...")

  #post_save.connect(profileUpdated, sender=Profile)
  #post_delete.connect(profileDeleted, sender=Profile)
  ```

  So, that's just another way of doing it, nothing different.

- From here on what we are gonna do is we're going to create a signal that creates a user profile at anytime a user is created. So, in our application here in our website, we're going to have a registration form. Someone's going to register and remember, we're connecting a profile to user. So, instead of having to submit different forms , sombody is going to create a user profile, and then or they're going to create a user account, and then immediately a profile will be generated for them. So, right now we have to first create a user and than create a profile for the user. Let's fix this automate the process.

  `models.py` - `users` app

  ```python

  # Edits to pre-exisitng models.py file at the end

  # Imports for the Signals
  from django.db.models.signals import post_save, post_delete

  def createProfile(sender, instance, created, **kwargs):
      if created:
          user = instance
          profile = Profile.objects.create(user=user, username=user.username, email=user.email, name=user.first_name)
      print("Profile Saved Succesfully... ")

  def profileDeleted(sender, instance, **kwargs):
      user = instance.user
      user.delete()
      print("Profile Deleted...")

  post_save.connect(createProfile, sender=User)
  post_delete.connect(profileDeleted, sender=Profile)
  ```

  - So, let's first understand what this code does over here. First, of all we import `post_save` and `psot_delete` methods. Than we create a function `createProfile`. The function creates the profile as soon as the user is created. Previously, we were doing all of this manually. So, thinking from scratch, the instance in this case will be `User` firstly. In addition, we will have three other arguments `sender`, `**kwargs` and `created`. `created` will be used for the if condition, if the user is created or not. Now, as soon as the user is created, we take the instance in a variable, and create a profile with the given variable.

  - Now, for `profileDeleted`, first of all why we need it, if in the `models.py` of `users` app, `Profile` has a one-to-one relationship with User, meaning as soon as the User is deleted, the profile is also deleted. But, what if the one getting deleted is the profile and not the user. In that case, even the Profile is deleted, the user will still exist which is contradictory. Hence, that's why we need this function. So, we pass in only 3 variables here, `instance`, `sender` and `**kwargs`, we don't need connected here as we are deleting the User if the Profile is deleted. So, the instance in this case will be Profile. So, we want the `user` associated with that instance. We grab it in a variable and delete it.

- Now, when we are all done undertanding the signals, let's go ahead and restructure and organize our signals code into a different file now. So, within the `users` app, we create a new file called `signals.py`. For, that first cut out all the signals related changes from `models.py` of  `users` app. Once done, create `signals.py` file within the `users` app and than paste the following into it.

  `signals.py` - `users` app

  ```python
  # Imports for the Signals
  from django.db.models.signals import post_save, post_delete
  from django.dispatch import receiver
  from django.contrib.auth.models import User
  from .models import Profile


  def createProfile(sender, instance, created, **kwargs):
      if created:
          user = instance
          profile = Profile.objects.create(user=user, username=user.username, email=user.email, name=user.first_name)
      print("Profile Saved Succesfully... ")

  def profileDeleted(sender, instance, **kwargs):
      user = instance.user
      user.delete()
      print("Profile Deleted...")

  post_save.connect(createProfile, sender=User)
  post_delete.connect(profileDeleted, sender=Profile)
  ```

  Now, it might look like all the work is done, and finished. Well, that's not the case, we still need to include as a part of the app, or else the `signals.py` won't work at all. For that, we need to make small change within the `apps.py` file of `users` app as hsown below:

  `apps.py` - `users` app

  ```python
  from django.apps import AppConfig


  class UsersConfig(AppConfig):
      default_auto_field = 'django.db.models.BigAutoField'
      name = 'users'

      def ready(self):
          import users.signals

  ```

  And yeah, that's all said and done now. Finally, done and dusted.

</p>
</storng>
