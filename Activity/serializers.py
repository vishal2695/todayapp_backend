from rest_framework import serializers
from .models import *
import datetime



class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Activity
        fields = "__all__"

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Topic
        fields = "__all__"