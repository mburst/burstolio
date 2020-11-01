from django.db import models
from django.urls import reverse

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
    
    def get_absolute_url(self):
        return reverse('core:entry', args=[self.slug])
        
    def __str__(self):
        return self.title
    
class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    
    def __str__(self):
        return self.name
    
class Subscriber(models.Model):
    email = models.EmailField()
    uuid = models.CharField(max_length=50, default=uuid4)
    
    def __str__(self):
        return self.email