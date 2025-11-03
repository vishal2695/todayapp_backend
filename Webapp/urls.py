from django.urls import path
from .views import *

urlpatterns = [
    
    path('', web_login, name='web_login'),
    path('dashboard', web_home, name='web_home'),
    path('logout', web_logout, name='web_logout'),


    path('user_detail', web_user_detail, name='user_detail'),
    path('payment_detail', web_payment_detail, name='payment_detail'),
    path('topic_list', web_topic_list, name='topic_list'),
    path('all_activity_list', web_all_activity_list, name='all_activity_list'),
    path('reset_password', web_reset_password, name='reset_password'),

]