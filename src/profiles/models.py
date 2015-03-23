from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
import uuid
from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager

class BaseProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                primary_key=True)
    slug = models.SlugField(max_length=32, unique=True, blank=True,
                            editable=False)
    # Add more user profile fields here. Make sure they are nullable
    # or with default values
    name = models.CharField(max_length = 20,null=True, blank=True)
    picture = models.ImageField('Profile picture',
                                upload_to='profile_pics/%Y-%m-%d/',
                                null=True,
                                blank=True)
    bio = models.CharField("Short Bio", max_length=200, blank=True, null=True)
    email_verified = models.BooleanField("Email verified", default=False)

    def save(self, *args, **kwargs):
        if self.slug is None or len(self.slug) == 0:
            self.slug = uuid.uuid4().hex
        super(BaseProfile, self).save(*args, **kwargs)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Profile(BaseProfile):
    def __str__(self):
        return "{}'s profile". format(self.user)
        
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    

class StartUpIdea(models.Model):
    creator = models.ForeignKey(Profile)
    name = models.CharField(max_length=20)
    pub_date = models.DateField(auto_now=True)
    description = models.TextField()
    likes = models.IntegerField(default=0)
    category = models.ForeignKey(Category)
    tags = TaggableManager()
    
    def __str__(self):
        return self.name
    
