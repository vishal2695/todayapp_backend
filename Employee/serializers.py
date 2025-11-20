from rest_framework import serializers
from .models import Employee, OTP
from Subscription.models import Plan
import datetime



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Employee
        fields = "__all__"

class EmployeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Employee
        exclude = ('accessToken',)


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OTP
        fields = "__all__"

class UserSelectedPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Plan
        fields = "__all__"




