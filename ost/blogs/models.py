from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from uuslug import uuslug


class Blog(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    creator = models.ForeignKey(User, related_name="created_blogs")
    authors = models.ManyToManyField(User, related_name="authored_blogs")
    followers = models.ManyToManyField(User, related_name="followed_blogs",
                                       null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Blog, self).save(*args, **kwargs)


class Post(models.Model):
    author = models.ForeignKey(User)
    blog = models.ForeignKey(Blog)
    title = models.CharField()
    slug = models.SlugField(max_length=200)
    content = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Blog, self).save(*args, **kwargs)
