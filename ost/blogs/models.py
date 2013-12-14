from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from uuslug import uuslug
from taggit.managers import TaggableManager


class Blog(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    creator = models.ForeignKey(User, related_name="created_blogs")
    authors = models.ManyToManyField(User, related_name="authored_blogs")
    followers = models.ManyToManyField(User, related_name="followed_blogs")

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Blog, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User)
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    content = RichTextField()
    tags = TaggableManager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Blog, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
