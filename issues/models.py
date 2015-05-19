from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.dispatch import receiver

# Create your models here.
#==========================================================================================
class Skill(models.Model):
    skillName = models.CharField(max_length=200)
    def __str__(self):
        return self.skillName
#==========================================================================================
class Project(models.Model):
    ProjectName = models.CharField(max_length=200)
    projectDescription = models.TextField(max_length=2000)
    projectAccessType = models.BooleanField(default=True)
    startTime = models.DateTimeField(null=True)
    finishedTime = models.DateTimeField(null=True)
    owner = models.ForeignKey(User, related_name="owner")
    def __str__(self):
        return self.name
    def get_absolute_url(self) :
        """ it gets the absolute url of current topic page, this method has been used in views"""
        return reverse("issues:main")
#==========================================================================================
class Task(models.Model):
    taskTitle = models.CharField(max_length=200)
    taskDescription = models.TextField(max_length=2000)
    skills = models.ManyToManyField(Skill,"taskSkills")
    project=models.ForeignKey(Project,related_name="project")
    operator = models.ManyToManyField(User,related_name="operator")
    def __str__(self):
        return self.taskTitle
#==========================================================================================
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
def user_post_save(sender, instance, created, **kwargs):
    """Create a user profile when a new user account is created"""
    if created == True:
        p = UserProfile()
        p.user = instance
        p.save()

post_save.connect(user_post_save, sender=User)

#==========================================================================================
class Forum(models.Model):

    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
       """ it gets the absolute url of current forum page , this method has been used in views"""
       return str("issues:forum",args=[self.pk])

    def numPosts(self):
        """returns the total number of  the posts in each forum"""
        return sum([t.numPosts() for t in self.topics.all()])

    def lastPost(self):
        """finds the last post of all the topics in a forum"""
        topics = self.topics.all()# the list of topics in a forum
        last    = None
        for topic in topics:#like finding the maximum of a list
            templastp = topic.lastPost()
            if templastp and (not last or templastp.date > last.date):
                last = templastp
        return last

#==========================================================================================
class Topic(models.Model):
    title   = models.CharField(max_length=60)
    date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    forum   = models.ForeignKey(Forum, related_name="topics")

    class Meta:
        ordering = ["-date"]# order topics by their date of creation

    def __str__(self):
        return str("%s - %s" % (self.creator, self.title))

    def get_absolute_url(self) :
        """ it gets the absolute url of current topic page, this method has been used in views"""
        return reverse("issues:topic", args=[self.pk])

    def lastPost(self)  :
        """returns the most recent post of the topic"""
        return self.posts.all()[0]#the first post is the recent post

    def numPosts(self) :
        """returns the number of  the posts in each topic"""
        return self.posts.count()

    def numReplies(self) :
        """returns the number of the replies in each topic"""
        return self.posts.count() - 1#because the first post isn't a reply

#==========================================================================================
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

    def short(self):
        """this method is used in lastposts column to show creator and title and date"""
        date = self.date.strftime("%b %d, %I:%M %p")
        return u"%s - %s\n%s" % (self.creator, self.title, date)

    def profileData(self):
        """this method is used in each post to see the creator's avatar and number of his posts"""
        p = self.creator.profile
        return p.posts
