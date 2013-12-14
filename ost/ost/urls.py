from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'portal.views.index', name='portal'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^blogs/', include('blogs.urls', namespace='blogs')),
    url(r'^blog/(?P<slug>[\w.@+-]+)/$', 'blogs.views.blog', name="blog"),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
