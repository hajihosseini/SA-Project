from django.shortcuts import render
from .models import *
from django.views import generic
from .forms import *
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout as auth_logout
from django.contrib.messages.api import get_messages


class Home(generic.ListView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    template_name = "home.html"
#----------------------------------------------------------------------------------------------------------------------


class UserPageView(generic.DetailView):
    model = UserProfile
    template_name = "userpage.html"
#----------------------------------------------------------------------------------------------------------------------


class EditProfile(generic.UpdateView):
    model = UserProfile
    fields = ['state']
    template_name = "userpage.html"
#----------------------------------------------------------------------------------------------------------------------


class ForumList(generic.ListView):
    paginate_by = 20
    model = Forum
    template_name = "list.html"
#----------------------------------------------------------------------------------------------------------------------


class ForumView(generic.detail.SingleObjectMixin, generic.ListView):
    paginate_by = 20
    template_name = "forum.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Forum.objects.all())
        return super(ForumView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['forum'] = self.object
        return context

    def get_queryset(self):
        return self.object.topics.all()

#----------------------------------------------------------------------------------------------------------------------


class TopicView(generic.detail.SingleObjectMixin, generic.ListView):
    paginate_by = 20
    template_name = "topic.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Topic.objects.all())
        return super(TopicView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TopicView, self).get_context_data(**kwargs)
        context['topic'] = self.object
        return context

    def get_queryset(self):
        return self.object.posts.all()
#----------------------------------------------------------------------------------------------------------------------


class NewTopic(generic.CreateView):
    model = Topic
    fields = ["title"]

    def form_valid(self, form):
        form.instance.creator=self.request.user
        form.instance.forum = Forum.objects.get(pk=self.kwargs['pk'])
        form.instance.date = timezone.now()
        return super(NewTopic, self).form_valid(form)
#----------------------------------------------------------------------------------------------------------------------


class NewPost(generic.CreateView):
    model = Post
    fields = ["title","body"]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.date = timezone.now()
        form.instance.topic = Topic.objects.get(pk=self.kwargs['pk'])
        return super(NewPost, self).form_valid(form)
#----------------------------------------------------------------------------------------------------------------------


class NewProject(generic.CreateView):
    model = Project
    fields = ['ProjectName','projectDescription','projectAccessType','startTime','finishedTime']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(NewProject, self).form_valid(form)
#----------------------------------------------------------------------------------------------------------------------


class NewTask(generic.CreateView):
    model = Task
    fields = ['taskTitle', 'taskDescription', 'skills', 'operator', 'deadline']

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs['pk'])
        #form.instance.progress = 0
        return super(NewTask, self).form_valid(form)
#-----------------------------------------------------------------------------------------------------------------------


class ProjectView(generic.detail.SingleObjectMixin, generic.ListView):
    paginate_by = 20
    template_name = "projectPage.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Project.objects.all())
        return super(ProjectView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['project'] = self.object
        return context

    def get_queryset(self):
        return self.object.task.all()

#----------------------------------------------------------------------------------------------------------------------


class TaskDone(generic.UpdateView):
    model = Task
    fields = ['done']
    template_name = 'taskPage.html'
#----------------------------------------------------------------------------------------------------------------------
