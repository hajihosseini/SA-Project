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
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.core.context_processors import csrf


class Home(generic.ListView):
    model = Project
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    template_name = "home.html"
#----------------------------------------------------------------------------------------------------------------------


class UserPageView(generic.detail.SingleObjectMixin, generic.ListView):
    paginate_by = 20
    template_name = "userpage.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=UserProfile.objects.all())
        return super(UserPageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserPageView, self).get_context_data(**kwargs)
        context['operator'] = self.object
        return context

    def get_queryset(self):
        return self.object.user.owner.all()

#----------------------------------------------------------------------------------------------------------------------

def editProfile(request, pk):
    """ when a user press the like buttons the number of post creator's score will be increased
        and an email will be sent to postcreator"""
    user=request.user

    if user.profile.state:
        user.profile.state=False
        user.profile.save()
    else:
        user.profile.state=True
        user.profile.save()

    return HttpResponseRedirect(reverse('issues:profile', args=(user.id,)))
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
        user=self.request.user
        topic=Topic.objects.get(pk=self.kwargs['pk'])
        message= "%s (%s) post in your topic :%s(%s)"% (user,'http://localhost:8000/issues/profile/%d/'%(user.id), topic,'http://localhost:8000/issues/topic/%d/'%(topic.id))
        recipient_list = [topic.creator.email]
        from_addr="pyissues.noreply@gmail.com"
        send_mail("Post Notification", message, from_addr, recipient_list)
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
    fields = ['taskTitle', 'taskDescription','operator' 'skills', 'deadline']
    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs['pk'])
        return super(NewTask, self).form_valid(form)
#----------------------------------------------------------------------------------------------------------------------
def outsourcingUser(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = User.objects.all()
    return render(request, "outsourcing.html", {'task': task , 'operators':user})

def setoperator(request,pk):
    task = get_object_or_404(Task, pk=pk)
    selected_operators = request.POST.getlist("operator")
    print(selected_operators)
    for o in selected_operators:
        o=get_object_or_404(User , pk=o)
        task.operator.add(o)
    task.save()
    return HttpResponseRedirect(reverse('issues:taskPage', args=(task.pk,)))
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


class TaskView(generic.detail.SingleObjectMixin, generic.ListView):
    paginate_by = 20
    template_name = "taskPage.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Task.objects.all())
        return super(TaskView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        context['task'] = self.object
        return context

    def get_queryset(self):
        return self.object.comment.all()
#----------------------------------------------------------------------------------------------------------------------
def taskDone(request, pk):
    """ when a user press the like buttons the number of post creator's score will be increased
        and an email will be sent to postcreator"""
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    user = request.user
    if task.done:
        task.done = False
        message= "%s (%s)has unDone The task:%s(%s)"% (user,'http://localhost:8000/issues/profile/%d/'%(user.id),task,'http://localhost:8000/issues/task/%d/'%(task.id))
        task.save()
    else:
        task.done = True
        message= "%s (%s)has Done The task:%s(%s)"% (user,'http://localhost:8000/issues/profile/%d/'%(user.id),task,'http://localhost:8000/issues/task/%d/'%(task.id))
        task.save()
    recipient_list = [project.owner.email]
    from_addr="pyissues.noreply@gmail.com"
    send_mail("Task Done Notification", message, from_addr, recipient_list)

    return HttpResponseRedirect(reverse('issues:taskPage', args=(task.id,)))
#----------------------------------------------------------------------------------------------------------------------

def upgrade(request,pk):
    task = get_object_or_404(Task, pk=pk)
    grade = request.POST['grade']
    for o in task.operator.all():
        print ("profile",type(o.profile.grade))
        o.profile.grade += int(grade)
        o.profile.save()
    task.completed=True
    task.save()
    return HttpResponseRedirect(reverse('issues:projectPage', args=(task.project.id,)))
#----------------------------------------------------------------------------------------------------------------------


class NewComment (generic.CreateView):
    model = Comment
    fields = ["body"]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.task = Task.objects.get(pk=self.kwargs['pk'])
        form.instance.date = timezone.now()
        return super(NewComment, self).form_valid(form)
