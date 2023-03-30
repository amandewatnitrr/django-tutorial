from django.contrib import admin
from .models import Project, Review, Tag
# Register your models here.

admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)
# This will register the Model Project and show it on the admin panel.
