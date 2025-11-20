from django.urls import path
from .views import *

urlpatterns = [
    path('api/razorpay/create-subscription', CreateSubscriptionAPI.as_view()),
    path('api/get_plan', get_plan),

    path('api/create', create),
    path('api/cancelled', cancelled),

    path('api/payment/all_filter', payment_all_filter),
    path('api/payment/all', payment_all),
    
    path('webhook/razorpay/', RazorpayWebhookView.as_view({'post': 'create'}), name='razorpay-webhook'),

    path('plan/<int:id>/<int:pid>', home, name='home'),
    path('plan/create-order/',create_order),
    path('plan/success/', payment_success),
    path('plan/success/detail/<str:pid>', payment_detail),


]