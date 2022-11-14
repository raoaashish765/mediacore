from asyncio.windows_events import NULL
from datetime import datetime
from email.policy import default
from re import U
from statistics import mode
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class setting(models.Model):
    user = models.CharField(max_length=10, null=True)
    interest=models.CharField(max_length=300, null=True)
    public=models.BooleanField(default=False)

    def __str__(self):
        return self.user

class Follow(models.Model):
    user = models.CharField(max_length=10, null=True)
    followers=models.CharField(max_length=500, null=True)
    following=models.CharField(max_length=10000, null=True)

    def __str__(self):
        return self.user

class Unfpenalty(models.Model):
    user = models.CharField(max_length=10, null=True)
    unfollow=models.CharField(max_length=10, null=True)
    time = models.DateTimeField(null=True)

    def __str__(self):
        return self.user

class Allposts(models.Model):
    post_id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=10, null=True)
    text=models.CharField(max_length=100, null=True)
    topic=models.CharField(max_length=10, null=True)
    image=models.ImageField(upload_to=None, max_length=None)
    timeadded = models.DateTimeField(auto_now_add=True)
    public=models.BooleanField(default=False)

    def __str__(self):
        return self.user+"-"+str(self.post_id)+"-"+self.topic

class Postlikes(models.Model):
    post=models.CharField(max_length=10, null=True)
    user=models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.post)+self.user

class Postcomments(models.Model):
    post=models.CharField(max_length=10, null=True)
    comment=models.CharField(max_length=100, null=True)
    user=models.CharField(max_length=10, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post)+self.user

class Repo(models.Model):
    rtitle=models.CharField(max_length=30, null=True)
    rexplain=models.CharField(max_length=300, null=True)
    user=models.CharField(max_length=10, null=True)
    rimage = models.ImageField(upload_to=None, max_length=None)

    def __str__(self):
        return str(self.rtitle)+self.user