from django.urls import path
from .views import *

urlpatterns = [
    path('api/razorpay/create-subscription', CreateSubscriptionAPI.as_view()),
    path('api/get_plan', get_plan),

    path('api/create', create),
    path('api/cancelled', cancelled),

    path('api/payment/all_filter', payment_all_filter),
    path('api/payment/all', payment_all),
    
    # path('webhook/razorpay/', RazorpayWebhookView.as_view({'post': 'create'}), name='razorpay-webhook'),

    path('plan/<str:id>/<str:pid>', start_payment, name='start_payment'),
    path('plan/create-order/',create_order),
    path('plan/success/', payment_success),
    path('plan/success/detail/<str:pid>', payment_detail),
    path('plan/cancel/detail/<str:pid>', payment_cancel_detail),
    path("plan/cancel/", payment_cancel, name="payment-cancel"),
    path("check/<str:id>", check, name="check"),

    path("payment/webhook/razorpay/", payment_razorpay_webhook, name="payment-razorpay-webhook"),

]