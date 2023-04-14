from django.forms import ModelForm
from .models import Project

# Specifying ModelForm within the argument of the class, specifies that the given class is a Form.


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title","description","featured_image","demo_link","source_link","tags"]