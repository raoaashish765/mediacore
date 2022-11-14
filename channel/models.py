from asyncio.windows_events import NULL
from django.db import models

# Create your models here.

class Channeldet(models.Model):
    user=models.CharField(max_length=10, default=NULL)
    chname=models.CharField(max_length=20, default=NULL)

    def __str__(self):
        return self.user+"-"+self.chname

class upallvideo(models.Model):
    vid=models.IntegerField(primary_key=True)
    user=models.CharField(max_length=10, default=NULL)
    chname=models.CharField(max_length=20, default=NULL)
    titlle=models.CharField(max_length=100, default=NULL)
    details=models.CharField(max_length=2000, default=NULL)
    video=models.FileField(upload_to=None, max_length=None)
    thumb=models.ImageField(upload_to=None, max_length=None)
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user+"-"+str(self.vid)+self.chname

class videolikes(models.Model):
    vid=models.CharField(max_length=10, default=NULL)
    user=models.CharField(max_length=10, default=NULL)

    def __str__(self):
        return self.user+"-"+str(self.vid)

class videocom(models.Model):
    vid=models.CharField(max_length=10, default=NULL)
    user=models.CharField(max_length=10, default=NULL)
    comment=models.CharField(max_length=100, default=NULL)

    def __str__(self):
        return self.user+"-"+str(self.vid)

class videoview(models.Model):
    vid=models.CharField(max_length=10, default=NULL)
    user=models.CharField(max_length=10, default=NULL)

    def __str__(self):
        return self.user+"-"+str(self.vid)