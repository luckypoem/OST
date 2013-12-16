from bs4 import BeautifulSoup
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from blogs.models import Blog, Post
from posts.utils import wrap_plain


class CorrectMimeTypeFeed(Rss201rev2Feed):
    mime_type = 'application/xml'


class LatestPostsFeed(Feed):
    feed_type = CorrectMimeTypeFeed

    def get_object(self, request, slug):
        return Blog.objects.get(slug=slug)

    def title(self, obj):
        return obj.name

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return obj.name

    def author_name(self, obj):
        return obj.creator.username

    def author_email(self, obj):
        return obj.creator.email

    def items(self, obj):
        return Post.objects.filter(blog=obj)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        plain = BeautifulSoup(item.content).get_text()[:500]
        return plain

    def item_author_name(self, item):
        return item.author.username

    def item_author_email(self, item):
        return item.author.email

    def item_pubdate(self, item):
        return item.date_created
