from django.forms import ModelForm
from .models import Project
from django import forms

# Specifying ModelForm within the argument of the class, specifies that the given class is a Form.


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title","description","featured_image","demo_link","source_link","tags"]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update({'class':'input','placeholder':'Add title'})
        self.fields["description"].widget.attrs.update({'class':'input','placeholder':'Add Description'})
        self.fields["tags"].widget.attrs.update({'class':'input--checkbox'})
        self.fields["demo_link"].widget.attrs.update({'class':'input','placeholder':'Add Demo Link'})
        self.fields["source_link"].widget.attrs.update({'class':'input','placeholder':'Add Source Link'})