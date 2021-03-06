from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from blogs.feeds import LatestPostsFeed

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'portal.views.index', name='portal'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^blogs/', include('blogs.urls', namespace='blogs')),
    url(r'^blog/(?P<slug>[\w.@+-]+)/$', 'blogs.views.blog', name='blog'),
    url(r'^blog/(?P<slug>[\w.@+-]+)/feeds.xml$', LatestPostsFeed(), name='feeds'),
    url(r'^blog/(?P<slug>[\w.@+-]+)/settings/$', 'blogs.views.settings',
        name='settings'),
    url(r'^blog/(?P<slug>[\w.@+-]+)/query/authors/$', 'blogs.ajax.authors',
        name='authors'),  # Ajax
    url(r'^blog/(?P<slug>[\w.@+-]+)/follow/$', 'blogs.ajax.follow',
        name='follow'),  # Ajax
    url(r'^blog/(?P<slug>[\w.@+-]+)/unfollow/$', 'blogs.ajax.unfollow',
        name='unfollow'),  # Ajax
    url(r'^blog/(?P<slug>[\w.@+-]+)/search/$', 'blogs.views.search',
        name='search'),
    url(r'^blog/(?P<slug>[\w.@+-]+)/posts/',
        include('posts.urls', namespace='posts')),
    url(r'^blog/(?P<blog_slug>[\w.@+-]+)/post/(?P<post_slug>[\w.@+-]+)/$',
        'posts.views.post', name='post'),
    url(r'^blog/(?P<blog_slug>[\w.@+-]+)/post/(?P<post_slug>[\w.@+-]+)/edit/$',
        'posts.views.edit', name='edit'),
    url(r'^blog/(?P<blog_slug>[\w.@+-]+)/tag/(?P<tag_slug>[\w.@+-]+)/$',
        'posts.views.tag', name='tag'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
