from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
from django.utils import timezone
from django.core.urlresolvers import reverse


class Skill(models.Model):
    skillName = models.CharField(max_length=200)
    def __str__(self):
        return self.skillName
#----------------------------------------------------------------------------------------------------------------------


class Project(models.Model):
    ProjectName = models.CharField(max_length=200)
    projectDescription = models.TextField(max_length=2000)
    projectAccessType = models.BooleanField(default=True)  #is public
    startTime = models.DateTimeField(null=True)
    finishedTime = models.DateTimeField(null=True)
    owner = models.ForeignKey(User, related_name="owner")
    progress = models.FloatField(default=0, max_length=10)


    class Meta:
        ordering = ["-startTime"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """ it gets the absolute url of current topic page, this method has been used in views"""
        return reverse('issues:projectPage',args=[self.pk])

    def progressUpdate(self):
        total = Task.objects.filter(project=Project.objects.get(pk=self.pk))
        done = total.filter(done=True)
        if total:
            self.progress = (float(len(done))*100)/len(total)
            self.save()
        return self.progress
#----------------------------------------------------------------------------------------------------------------------


class Task(models.Model):
    taskTitle = models.CharField(max_length=200)
    taskDescription = models.TextField(max_length=2000)
    skills = models.ManyToManyField(Skill, "taskSkills")
    project = models.ForeignKey(Project, related_name="task")
    operator = models.ManyToManyField(User, related_name="operator")
    done = models.BooleanField(default=False)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.taskTitle

    def get_absolute_url(self) :
        return reverse('issues:projectPage', args=[self.project.pk])

    def get_queryset(self):
        Task.objects.filter(project=self.kwargs['pk'])
#----------------------------------------------------------------------------------------------------------------------


class UserProfile(models.Model):
    #avatar = models.URLField(null=True)
    state = models.BooleanField(default=True)
    #fieldOfStudy = models.CharField(max_length=200)
    #university = models.CharField(max_length=200)
    #cityState = models.CharField(max_length=100)
    #city = models.CharField(max_length=100)
    #grade = models.IntegerField(default=0)
    user = models.OneToOneField(User, related_name="profile")
    #skills = models.ManyToManyField(Skill,related_name="userSkills",null=True)
    #tasks = models.ManyToManyField (Task,related_name="userTasks",null=True)
    @models.permalink
    def get_absolute_url(self):
        return ('issues:profile', None,{'pk':self.user.pk})

    def __str__(self):
        return self.user.username


def user_post_save(sender,instance, created, **kwargs):
    """Create a user profile when a new user account is created"""

    if created == True:
        p = UserProfile()
        p.user = instance
        p.save()

post_save.connect(user_post_save, sender=User)

#----------------------------------------------------------------------------------------------------------------------


class Forum(models.Model):
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
       #""" it gets the absolute url of current forum page , this method has been used in views"""
       return str("issues:forum",args=[self.pk])

#----------------------------------------------------------------------------------------------------------------------


class Topic(models.Model):
    title   = models.CharField(max_length=60)
    date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    forum = models.ForeignKey(Forum, related_name="topics")

    class Meta:
        ordering = ["-date"]# order topics by their date of creation

    def __str__(self):
        return str("%s - %s" % (self.creator, self.title))

    def get_absolute_url(self) :
        """ it gets the absolute url of current topic page, this method has been used in views"""
        return reverse("issues:newPost", args=[self.pk])

#----------------------------------------------------------------------------------------------------------------------


class Post(models.Model):
    title = models.CharField(max_length=60)
    date = models.DateTimeField(auto_now_add=True)
    creator=models.ForeignKey(User, blank=True, null=True)
    topic = models.ForeignKey(Topic, related_name="posts")
    body = models.TextField(max_length=10000)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return u"%s - %s - %s" % (self.creator, self.topic, self.title)

    def get_absolute_url(self) :
        return reverse('issues:topic',args=[self.topic.pk])
#----------------------------------------------------------------------------------------------------------------------
