from django.db import models
from Employee.models import *

# Create your models here.


class Activity(models.Model):
    empId          = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    startDate      = models.DateField(max_length=100, blank=True)
    startTimeStamp = models.CharField(max_length=100, blank=True)
    closeTimeStamp = models.CharField(max_length=100, blank=True)
    totalSecond    = models.FloatField(default=0)
    status         = models.IntegerField(default=0)  #0-start, 1-stop
    createdAt      = models.DateTimeField(auto_now_add=True)
    updatedAt      = models.DateTimeField(auto_now=True)



class Topic(models.Model):
    empId          = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    title          = models.CharField(max_length=200, blank=True)
    section        = models.CharField(max_length=200, blank=True)
    video_Time     = models.CharField(max_length=200, blank=True)
    description    = models.TextField(blank=True)
    createdAt      = models.DateTimeField(auto_now_add=True)
    updatedAt      = models.DateTimeField(auto_now=True)

