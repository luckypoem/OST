from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^$', 'blogs.views.index', name="index"),
    url(r'^create/$', 'blogs.views.create', name="create"),
    url(r'^following/$', 'blogs.views.following', name="following"),
)
