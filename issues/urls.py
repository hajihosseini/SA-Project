from django.conf.urls import *
from django.contrib.auth.decorators import login_required as LR
from .models import *
from .views import *
urlpatterns = patterns('',
    url(r"^profile/(?P<pk>\d+)/$", LR(EditProfile.as_view()), name="profile"),
    url(r"^viewprofile/(?P<pk>\d+)/$" , LR(UserPageView.as_view()), name="viewprofile"),
    url(r"^forum/(?P<dpk>\d+)/$", LR(ForumView.as_view()), name= "forum"),
    url(r"^topic/(?P<dpk>\d+)/$", LR(TopicView.as_view()), name= "topic"),
    url(r"^forums$", LR(ForumList.as_view()), name="forums"),
    url(r"^$", Main.as_view(), name="main"),
)
