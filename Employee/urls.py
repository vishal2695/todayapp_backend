from django.urls import path
from .views import *
from .views_speak import *

urlpatterns = [
    # path('', get_items, name='get-items'),
    path('login_or_signup', login_or_signup, name='login'),
    path('verify_otp', otpVerify, name='otp'),
    path('one', one, name='one'),
    path('update', update, name='update'),
    # path('profile_upload', profile_upload, name='profile_upload'),
    path('image_upload', image_upload, name='image_upload'),
    path('image_remove', image_remove, name='image_remove'),
    path('deactivate', deactivate, name='deactivate'),



    path("speak", speak, name="speak"),


]