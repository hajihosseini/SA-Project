from django.shortcuts import render

# Create your views here.
from PIL import Image as PImage
from project.settings import MEDIA_URL
from .models import *
from django.views import generic
from .form import *
class Main(generic.ListView):
    """desplays list of forums names and their last post."""
    model = UserProfile
    template_name = "main.html"
class UserPageView(generic.DetailView):
    model = UserProfile
    template_name = "userpage.html"

class EditProfile(generic.UpdateView):
    model = UserProfile
    fields = ['avatar','state']
    template_name_suffix = '_update_form'
