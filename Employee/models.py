from django.db import models
import uuid
from django.utils.text import slugify
import random
import string
# Create your models here.
from datetime import timedelta
from django.utils.timezone import now

def default_end_plan():
    return now() + timedelta(days=15)


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
    subscription   = models.CharField(max_length=50, default='trial', blank=True)  # paid/trial/expire/renew
    availableSecond = models.IntegerField(default=1800)
    selectedPlan   = models.ForeignKey('Subscription.Plan', on_delete=models.SET_NULL, null=True, blank=True)
    startPlan      = models.DateTimeField(auto_now_add=True)
    endPlan        = models.DateTimeField(default=default_end_plan)
    lastLogin      = models.DateTimeField(auto_now_add=True)
    createdAt      = models.DateTimeField(auto_now_add=True)
    updatedAt      = models.DateTimeField(auto_now=True)

    slug           = models.SlugField(max_length=50, unique=True, blank=True)

    def generate_slug(self):
        length = random.randint(10, 20)  # ensures between 10–20 chars
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def save(self, *args, **kwargs):
        # ALWAYS regenerate slug on create & update
        self.slug = self.generate_slug()
        super().save(*args, **kwargs)




class OTP(models.Model):
    phone          = models.CharField(max_length=50)
    countryCode    = models.CharField(max_length=10, default="+91")
    otp            = models.CharField(max_length=5)
    status         = models.BooleanField(default=False)
    createdAt      = models.DateTimeField(auto_now_add=True)
    updatedAt      = models.DateTimeField(auto_now=True)


