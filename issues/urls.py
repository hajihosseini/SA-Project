from django.conf.urls import *
from django.contrib.auth.decorators import login_required as LR
from .models import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *
urlpatterns = patterns('',
    url(r"^setoperators/(?P<pk>\d+)/$", LR(setoperator), name="setoperator"),
    url(r"^outsourcingSuggest/(?P<pk>\d+)/$",outsourcingSuggest, name="outsourcingSuggest"),
    url(r"^outsourcingUser/(?P<pk>\d+)/$",outsourcingUser, name="outsourcingUser"),
    url(r"^newComment/(?P<pk>\d+)/$", LR(NewComment.as_view()), name="newComment"),
    url(r"^upgrade/(?P<pk>\d+)/$", LR(upgrade), name="upgrade"),
    url(r"^taskPage/(?P<pk>\d+)/$", LR(TaskView.as_view()), name="taskPage"),
    url(r"^taskDone/(?P<pk>\d+)/$", LR(taskDone), name="taskDone"),
    url(r"^delTask/(?P<pk>\d+)/$", LR(delTask), name="delTask"),
    url(r"^editTask/(?P<pk>\d+)/$", LR(EditTask.as_view()), name="editTask"),
    url(r"^newTopic/(?P<pk>\d+)/$", LR(NewTopic.as_view()), name="newTopic"),
    url(r"^projectPage/(?P<pk>\d+)/$", LR(ProjectView.as_view()), name="projectPage"),
    url(r"^newTask/(?P<pk>\d+)/$", LR(NewTask.as_view()), name="newTask"),
    url(r"^newProject/(?P<pk>\d+)/$", LR(NewProject.as_view()), name="newProject"),
    url(r"^(?P<pk>\d+)/editprofile/$", LR(editProfile), name='editprofile'),
    url(r"^profile/(?P<pk>\d+)/$", LR(userPageView), name="profile"),
    url(r"^forum/(?P<pk>\d+)/$", LR(ForumView.as_view()), name="forum"),
    url(r"^topic/(?P<pk>\d+)/$", LR(TopicView.as_view()), name="topic"),
    url(r"^newPost/(?P<pk>\d+)/$", LR(NewPost.as_view()), name="newPost"),
    url(r"^forums$", LR(ForumList.as_view()), name="forums"),
    url(r"^$", Home.as_view(), name="home"),
)
urlpatterns += staticfiles_urlpatterns()
