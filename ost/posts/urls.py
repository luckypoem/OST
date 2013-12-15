from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^$', 'posts.views.index', name="index"),
    url(r'^create/$', 'posts.views.create', name="create"),
    url(r'^dashboard/$', 'posts.views.dashboard', name="dashboard"),
)
