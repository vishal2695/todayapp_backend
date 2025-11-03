from rest_framework import serializers
from .models import Employee, OTP
import datetime



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Employee
        fields = "__all__"


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OTP
        fields = "__all__"
