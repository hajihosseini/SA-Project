from django.forms import ModelForm
from issues.models import *
class ProfileForm(ModelForm):
    class Meta:
        model  = UserProfile
        exclude = ["grade", "user"]
class PostForm( ModelForm):
    """post form class which contains all the fields except creator and topic fields."""
    class Meta:
        model = Post
        exclude = ["creator", "topic"]
