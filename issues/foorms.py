from django.conf.urls import *
from django.contrib.auth.decorators import login_required as LR
from .models import *
import social_auth
from .views import *
urlpatterns = patterns('',
    url(r"^profile/(?P<pk>\d+)/$", LR(EditProfile.as_view()), name="profile"),
    url(r"^viewprofile/(?P<dpk>\d+)/$" , LR(UserPageView.as_view()), name="viewprofile"),
    url(r"^$", Main.as_view(), name="main"),
)
