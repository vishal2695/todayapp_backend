from django.db import models

# Create your models here.


class Employee(models.Model):
    userName       = models.CharField(max_length=200, blank=True)
    email          = models.CharField(max_length=200, blank=True)
    phone          = models.CharField(max_length=50, blank=True)
    userType       = models.CharField(max_length=50, blank=True)
    activeStatus   = models.BooleanField(default=True)
    profile_image  = models.CharField(max_length=200, blank=True)
    dob            = models.CharField(max_length=50, blank=True)
    profession     = models.CharField(max_length=200, blank=True)
    deviceType     = models.CharField(max_length=200, blank=True)
    accessToken    = models.TextField(blank=True)
    country        = models.CharField(max_length=50, blank=True)
    countryCode    = models.CharField(max_length=50, blank=True)
    accountStatus  = models.BooleanField(default=True)
    subscription   = models.CharField(max_length=50, default='trial', blank=True)  # paid/trial
    lastLogin      = models.DateTimeField(auto_now_add=True)
    createdAt      = models.DateTimeField(auto_now_add=True)
    updatedAt      = models.DateTimeField(auto_now=True)

class OTP(models.Model):
    phone          = models.CharField(max_length=50)
    countryCode    = models.CharField(max_length=10, default="+91")
    otp            = models.CharField(max_length=5)
    status         = models.BooleanField(default=False)
    createdAt      = models.DateTimeField(auto_now_add=True)
    updatedAt      = models.DateTimeField(auto_now=True)


