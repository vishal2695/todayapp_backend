from django.db import models
from Employee.models import Employee

class Plan(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    name = models.CharField(max_length=255)
    amount = models.IntegerField(help_text="Amount in paise")
    currency = models.CharField(max_length=3, default='INR')
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    interval = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    razorpay_key = models.TextField(blank=True)
    days = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - ₹{self.amount/100}/{self.period}"

class Subscription(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('authenticated', 'Authenticated'),
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('halted', 'Halted'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    razorpay_subscription_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    razorpay_customer_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    total_count = models.IntegerField(null=True, blank=True)
    paid_count = models.IntegerField(default=0)
    remaining_count = models.IntegerField(null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    next_charge_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.userName} - {self.plan.name} - {self.status}"



class Payment(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('authorized', 'Authorized'),
        ('captured', 'Captured'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]
    TYPE_CHOICES = [
        ('one time', 'One Time'),
        ('subscription', 'Subscription'),
    ]
    
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    razorpay_payment_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    amount = models.IntegerField()
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    method = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True)
    payment_type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='one time')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.razorpay_payment_id} - ₹{self.amount/100} - {self.status}"





