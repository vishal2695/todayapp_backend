from django.db import models

# Create your models here.


class WebUser(models.Model):
    Email     = models.CharField(max_length=200, blank=True)
    Password  = models.CharField(max_length=200, blank=True)
    Active    = models.BooleanField(default=True)
    Role      = models.CharField(max_length=100, blank=True)
    CreatedAt = models.DateField(auto_now_add=True)
    UpdatedAt = models.DateField(auto_now=True)





