from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

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
        return self.ProjectName

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
    operator = models.ManyToManyField(User, related_name="operator",null=True)
    done = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-deadline"]

    def __str__(self):
        return self.taskTitle

    def get_absolute_url(self) :
        return reverse('issues:projectPage', args=[self.project.pk])

    def get_queryset(self):
        Task.objects.filter(project=self.kwargs['pk'])
#----------------------------------------------------------------------------------------------------------------------


class UserProfile(models.Model):
    avatar = models.URLField(null=True)
    state = models.BooleanField(default=True)
    location = models.CharField(null=True,max_length=100)
    position = models.CharField(null=True,max_length=100)
    grade = models.IntegerField(default=0)
    user = models.OneToOneField(User, related_name="profile")
    skills = models.ManyToManyField(Skill,related_name="userSkills",null=True)
    @models.permalink

    def get_absolute_url(self):
        return ('issues:profile', None,{'pk':self.user.pk})

    class Meta:
        ordering = ["-grade"]
    def __str__(self):
        return self.user.username


def user_post_save(sender,instance, created, **kwargs):
    """Create a user profile when a new user account is created"""

    if created == True:
        p = UserProfile()
        p.user = instance
        p.save()

post_save.connect(user_post_save, sender=User)
from allauth.account.signals import user_logged_in
from django.dispatch import receiver
@receiver(user_logged_in)
def user_logged_in_(request, user, sociallogin=None, **kwargs):
    if sociallogin:
        # Extract first / last names from social nets and store on User record
        if sociallogin.account.provider == 'linkedin':
            user.first_name = sociallogin.account.extra_data['first-name']
            user.last_name = sociallogin.account.extra_data['last-name']
            profile = UserProfile.objects.get(pk=user.pk)
            if 'picture-url' in sociallogin.account.extra_data:
                profile.avatar = sociallogin.account.extra_data['picture-url']
            if 'location' in sociallogin.account.extra_data:
                profile.location = sociallogin.account.extra_data['location']['name']
            if 'headline' in sociallogin.account.extra_data:
                profile.position = sociallogin.account.extra_data['headline']
            profile.save()
        user.save()
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


class Comment(models.Model):
    creator = models.ForeignKey(User, blank=True, null=True)
    body = models.TextField(max_length=1000)
    task = models.ForeignKey(Task, related_name="comment",  blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-date"]
    def __unicode__(self):
        return u"%s: %s" % (self.profile, self.body[:60])

    def get_absolute_url(self) :
        """ it gets the absolute url of current topic page, this method has been used in views"""
        return reverse('issues:taskPage',args=[self.task.pk])
