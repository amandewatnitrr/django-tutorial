<strong>
<p align="justify">

# User Profile Creation and Rendering Profiles

- So, we have installed our theme and other stuff, and now our Website looks something like this:

![](./imgs/Screenshot%202023-04-15%20at%206.40.47%20PM.png)

![](./imgs/Screenshot%202023-04-15%20at%2011.23.09%20PM.png)

- So, till now in our project we have a review model, Project model and a tag model. But none of them is associated to a certain user or a profile. So, as till now we have only discussed the concept of apps and haven't implemented it actually yet. So, we are going to build `Profile`, `Skill` and `Message` model. And these 3 are not going to be the same app as the `Project`, `Tag` and `Review`. They are going to be in project but in different apps.
- The good thing is we don't need to worry about the user model because that's already built into django, but that's something we are gonna connect to and make some edits. So, even though we are gonna make different apps, they need to be connected to each other. As we need to have `Project` and `Review` model connected to the profile. And hence, these 2 apps will be able to communicate with each other.

- So, in our projectm we are going to have 2 apps. One the `projects` app and the other `user` app. We are gonna create a seprate `user` app where we have our own database models, our own neutral routing and templates.

</p>
</storng>
