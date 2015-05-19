from django.forms import ModelForm
from issues.models import *
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields=['ProjectName','projectDescription','projectAccessType']
