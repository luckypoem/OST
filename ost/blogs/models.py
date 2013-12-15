from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from uuslug import uuslug
from taggit.managers import TaggableManager
from django.core.urlresolvers import reverse


class Blog(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    creator = models.ForeignKey(User, related_name="created_blogs")
    authors = models.ManyToManyField(User, related_name="authored_blogs")
    followers = models.ManyToManyField(User, related_name="followed_blogs")
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Blog, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.slug


class Post(models.Model):
    author = models.ForeignKey(User)
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    content = RichTextField(blank=True)
    tags = TaggableManager()  # Automatically store comma-separated tags
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', args=(self.blog.slug, self.slug))

    def __unicode__(self):
        return self.slug
