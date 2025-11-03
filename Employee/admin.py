from django.contrib import admin
from .models import *
from Activity.models import *
from Webapp.models import *
from Subscription.models import *

# Register your models here.

admin.site.register(Employee)
admin.site.register(OTP)
admin.site.register(Activity)
admin.site.register(Topic)
admin.site.register(WebUser)
admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(Payment)
