from django.urls import path
from .views import *

urlpatterns = [
    path('create', create, name='create'),
    path('create_topic', create_topic, name='create_topic'),

    path('all_topic', topic_all_filter, name='all_topic')


]