from rest_framework import serializers
from .models import Plan, Subscription, Payment

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
        read_only_fields = ['id', 'razorpay_plan_id', 'created_at', 'updated_at']

class SubscriptionSerializer(serializers.ModelSerializer):
    plan_details = PlanSerializer(source='plan', read_only=True)
    
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['id', 'user', 'razorpay_subscription_id', 'razorpay_customer_id',
                          'status', 'paid_count', 'remaining_count', 'created_at', 'updated_at']


class SubscriptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'




class SubscriptionProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["start_at","end_at"]


class CreateSubscriptionSerializer(serializers.Serializer):
    plan_id = serializers.UUIDField()
    total_count = serializers.IntegerField(required=False, allow_null=True)
    customer_notify = serializers.BooleanField(default=True)
    addons = serializers.ListField(child=serializers.DictField(), required=False)
    notes = serializers.DictField(required=False)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        # depth = 1
        # read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'



class PlanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
