
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^issues/', include('issues.urls', namespace="issues")),#issues urls
    url(r'^admin/', include(admin.site.urls)),#admin urls
    (r'^accounts/', include('allauth.urls')), #allauth urls
)