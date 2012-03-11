from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from dbarray import IntegerArrayField

from datetime import datetime
from uuid import uuid4

class Entry(models.Model):
    content = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    published = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag')
    
    class Meta:
        ordering=['-date']
    
    @models.permalink
    def get_absolute_url(self):
        return ('core.views.entry', (), {'slug': self.slug})
        
    def __unicode__(self):
        return self.title
    
class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    
    def __unicode__(self):
        return self.name
    
class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    path = IntegerArrayField(blank=True, editable=False) #Can't be null as using append to path for replies and can't append to a None path
    depth = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    entry = models.ForeignKey('Entry', blank=True, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child')
    spam = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.content
    
class Subscriber(models.Model):
    email = models.EmailField()
    uuid = models.CharField(max_length=50, default=uuid4)
    
    def __unicode__(self):
        return self.email