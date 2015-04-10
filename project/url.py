
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^issues/', include('issues.urls', namespace="issues")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
)
