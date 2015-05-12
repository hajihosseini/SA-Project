from django.shortcuts import render

# Create your views here.
from .models import *
from django.views import generic
from .forms import *
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.messages.api import get_messages
class Main(generic.ListView):
    """desplays list of forums names and their last post."""
    model = Project
    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    template_name = "main.html"
class UserPageView(generic.DetailView):
    model = UserProfile
    template_name = "userpage.html"

class EditProfile(generic.UpdateView):
    model = UserProfile
    fields = ['state']
    template_name_suffix = '_update_form'

class ForumList(generic.ListView):
    """desplays list of forums names and their last post."""
    list_model = Forum
    model = Forum
    template_name = "list.html"

class ForumView(generic.ListView):#(listview+detailview)
    """desplays all of the topics in each forum"""
    list_model = Topic
    model = Topic
    related_name = "topics"
    template_name = "forum.html"

class TopicView(generic.ListView):
    """desplays all of the posts in each topic"""
    list_model = Post
    detail_model = Topic
    model = Post
    related_name  = "posts"
    template_name = "topic.html"
