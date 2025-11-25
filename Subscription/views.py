from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import razorpay
from datetime import datetime, timedelta
from Employee.models import Employee 


RAZORPAY_KEY_ID     = 'rzp_test_zPgaGkNcjHMsdZ'
RAZORPAY_KEY_SECRET = 'VbL5RhqzLUebGs758QPdNH01'



class CreateSubscriptionAPI(APIView):
    def post(self, request):
        # user_email = request.data.get("email")
        # plan_id = request.data.get("plan_id")  # You should have created this plan via dashboard or API
        user_email = "vkd2699@gmail.com"
        # plan_id = "plan_QZFrkSIJwnvc74"  # You should have created this plan via dashboard or API
        plan_id = "plan_QbvXRsq7f9aUxg"  # You should have created this plan via dashboard or API
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        # customer = client.customer.create({
        #     "name": "Vishal Dubey Test",
        #     "email": "vishal.dubey@cinntra.com",
        #     "contact": "+918802114410"
        # })
        data = {
            "plan_id": plan_id,
            "customer_notify": 1,
            "total_count": 1,
            "quantity": 1,
            # "customer_id": customer["id"]
            "customer_id": "cust_QZGD5F7vJjMiKN"
        }

        subscription = client.subscription.create(data=data)

        # payment_data = {
        #     "amount": 1000,  # Amount in paise (example: 1000 paise = 10 INR)
        #     "currency": "INR",
        #     "receipt": "receipt#1",
        #     "payment_capture": 1,  # Auto-capture after payment
        # }

        # order = client.order.create(data=payment_data)
        # print("order details....",order)
        print("subscription details....",subscription)

        return Response({
            "subscription_id": subscription["id"],
            "razorpay_key_id": RAZORPAY_KEY_ID
        }, status=status.HTTP_201_CREATED)

    def get(self, request):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        all_subs = client.subscription.all()
        print(all_subs)
        for item in  all_subs["items"]:
            # print(item)
            # item = 

            # timestamp = item["current_start"]  # your timestamp
            # dt = datetime.fromtimestamp(timestamp)

            # print("start...",dt.strftime("%Y-%m-%d %H:%M:%S"))
            # timestamp = item["current_end"]  # your timestamp
            # dt = datetime.fromtimestamp(timestamp)

            # print("end....",dt.strftime("%Y-%m-%d %H:%M:%S"))
            pass
        return Response({
            # "subscription_id": subscription["id"],
            "razorpay_key_id": RAZORPAY_KEY_ID
        }, status=status.HTTP_200_OK)
    

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from Utils.global_fun import *


@authenticate_token
@api_view(['GET'])
def get_plan(request):
    try:
        user_info = getattr(request, 'user_data', None)
        print(user_info)
        id = user_info["id"]
        print("auth data", id)
        if Employee.objects.filter(id=id).exists():
            # print(id)
            # client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
            # raz_plan = client.plan.all()    
            # print(raz_plan)
            # for item in raz_plan['items']:
            #     if not Plan.objects.filter(razorpay_key=item['id']).exists():
            #         print(item['id'])
            #         plan_data = {
            #             "razorpay_key":item['id'],
            #             "period": item['period'],
            #             "interval": item['interval'],
            #             "name": item['item']['name'],
            #             "amount": item['item']['amount'],
            #             "currency": item['item']['currency'],
            #             "description": item['item']['description']
            #             }
            #         print("created...",plan_data)
            #         plan_ser = PlanSerializer(data=plan_data)
            #         if plan_ser.is_valid():
            #             plan_ser.save()

            plan_objj = Plan.objects.raw("SELECT id, period FROM `Subscription_plan` GROUP BY `period`")
            final_data = []
            for row in plan_objj:
                objj = {}
                objj["plan"] = row.period
                plan_obj = Plan.objects.filter(period=row.period).order_by('interval')
                serializer = PlanSerializer(plan_obj, many=True).data
                objj["plan_list"] = serializer
                final_data.append(objj)

            return Response({"message":"Success", "status":200, "data":final_data})
        else:
            return Response({"message":"Unsuccess", "status":404, "data":[]})

    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})



@authenticate_token
@api_view(['POST'])
def create(request):
    try:
        user_info = getattr(request, 'user_data', None)
        print(user_info)
        id = user_info["id"]
        print("auth data", id)
        if Employee.objects.filter(id=id).exists():
            emp_obj = Employee.objects.get(id=id)
            requestData = request.data
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
            plan_obj = Plan.objects.filter(id=requestData["plan_id"]).first()
            # subscription_data = {
            #     "plan_id": plan_obj.razorpay_key,
            #     "customer_notify": 1,
            #     "total_count": 12
            # }

            
            # subscription_data = {
            #     "plan_id": plan_obj.razorpay_key,
            #     "customer_notify": 1,
            #     "total_count": None,
            #     "customer": {
            #         "name": "John Doe",
            #         "email": "honeybeeofficial2020@gmail.com",
            #         "contact": "9716336699"
            #     },
            #     "notify_info": {
            #         "notify_phone": "9716336699",
            #         "notify_email": "honeybeeofficial2020@gmail.com"
            #     }
            # }

            notify_info = {}
            if emp_obj.email != "":
                notify_info["notify_email"] = emp_obj.email
            if emp_obj.email != "":
                notify_info["notify_phone"] = emp_obj.phone
            subscription_data = {
                "plan_id": plan_obj.razorpay_key,
                "customer_notify": 1,
                "total_count":100
            }
            if notify_info:
                subscription_data["notify_info"] = notify_info

            # if 'addons' in serializer.validated_data:
            #     subscription_data['addons'] = serializer.validated_data['addons']
            
            # if 'notes' in serializer.validated_data:
            #     subscription_data['notes'] = serializer.validated_data['notes']
            
            razorpay_subscription = client.subscription.create(subscription_data)
            print(razorpay_subscription)
            # Create local subscription
            subscription = Subscription.objects.create(
                user=emp_obj,
                plan=plan_obj,
                razorpay_subscription_id=razorpay_subscription['id'],
                total_count=razorpay_subscription.get('total_count'),
                status='created'
            )
            print(razorpay_subscription)
            return Response({"message":"Success", "status":200, "data":[{razorpay_subscription["short_url"]}]})
        else:
            return Response({"message":"Unsuccess", "status":404, "data":[]})

    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})




@authenticate_token
@api_view(['POST'])
def cancelled(request):
    try:
        user_info = getattr(request, 'user_data', None)
        print(user_info)
        id = user_info["id"]
        print("auth data", id)
        if Employee.objects.filter(id=id).exists():
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
            requestData = request.data
            emp_obj = Employee.objects.get(id=id)
            try:
                # Cancel in Razorpay
                subs_id = requestData["subs_id"]
                subs_obj = Subscription.objects.get(id=subs_id)
                client.subscription.cancel(subs_obj.razorpay_subscription_id)
                
                # Update local subscription
                subs_obj.status = 'cancelled'
                subs_obj.save()
                
                return Response(
                    {"message": "Subscription cancelled successfully", "status":200, "data":[]}
                    
                )
            except Exception as e:
                return Response(
                    {"error": f"Failed to cancel subscription: {str(e)}", "status":404, "data":[]}
                )
        else:
            return Response({"message":"Unsuccess", "status":404, "data":[]})

    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})





from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



# @method_decorator(csrf_exempt, name='dispatch')
# class RazorpayWebhookView(viewsets.ViewSet):
    
#     def create(self, request):
#         print("webhook called......!!!!!")
#         # Verify webhook signature
#         razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
#         # webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
#         webhook_secret = "todayapp_apikey"
#         webhook_signature = request.headers.get('X-Razorpay-Signature')
        
#         if not webhook_signature:
#             print("missin signature.....error")
#             return Response(
#                 {"error": "Missing signature"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         body = request.body
        
#         try:
#             razorpay_client.utility.verify_webhook_signature(
#                 body.decode('utf-8'), webhook_signature, webhook_secret
#             )
#         except Exception as e:
#             print("Invalid signature .....error")
#             return Response(
#                 {"error": "Invalid signature"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         # Process webhook event
#         event = json.loads(body)
#         event_type = event.get('event')
#         print("success msg....", event_type)
#         return Response(
#                 {"mesaags": "data success from webhookss"},
#                 status=200,
#                 data=event
#             )



@method_decorator(csrf_exempt, name='dispatch')
class RazorpayWebhookView(viewsets.ViewSet):

    def create(self, request):
        print("Webhook called...")
        WEBHOOK_SECRET = "todayapp_apikey"
        webhook_signature = request.headers.get('X-Razorpay-Signature')
        if not webhook_signature:
            print("Missing signature")
            return Response(
                {"error": "Missing signature"},
                status=status.HTTP_400_BAD_REQUEST
            )

        body = request.body
        try:
            razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
            razorpay_client.utility.verify_webhook_signature(
                body.decode('utf-8'),
                webhook_signature,
                WEBHOOK_SECRET
            )
        except Exception as e:
            print("Invalid signature:", e)
            return Response(
                {"error": "Invalid signature"},
                status=status.HTTP_400_BAD_REQUEST
            )

        event = json.loads(body)
        event_type = event.get('event')
        print("Event received:", event_type)

        if event_type == 'subscription.activated':
            print("activated....", event['payload']['subscription']['entity'])
            self._handle_subscription_activated(event['payload']['subscription']['entity'])
        elif event_type == 'subscription.charged':
            print("charged....", event['payload'])
            self._handle_subscription_charged(event['payload'])
        elif event_type == 'subscription.cancelled':
            print("cancelled...",event['payload']['subscription']['entity'])
            self._handle_subscription_cancelled(event['payload']['subscription']['entity'])
        elif event_type == 'subscription.completed':
            print("completed.....",event['payload']['subscription']['entity'])
            self._handle_subscription_completed(event['payload']['subscription']['entity'])
        elif event_type == 'subscription.halted':
            print("halted....", event['payload']['subscription']['entity'])
            self._handle_subscription_halted(event['payload']['subscription']['entity'])
        elif event_type == 'payment.captured':
            print("captured......", event['payload']['payment']['entity'])
            self._handle_payment_captured(event['payload']['payment']['entity'])
        elif event_type == 'payment.failed':
            print("failed......", event['payload']['payment']['entity'])
            self._handle_payment_failed(event['payload']['payment']['entity'])
        
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    
    def _handle_subscription_activated(self, subscription_data):
        try:
            subscription = Subscription.objects.get(
                razorpay_subscription_id=subscription_data['id']
            )
            subscription.status = 'active'
            subscription.start_at = datetime.fromtimestamp(subscription_data.get('start_at'))
            subscription.end_at = datetime.fromtimestamp(subscription_data.get('end_at'))
            subscription.next_charge_at = datetime.fromtimestamp(subscription_data.get('charge_at'))
            subscription.save()
        except Subscription.DoesNotExist:
            pass
    
    def _handle_subscription_charged(self, payload):
        subscription_data = payload['subscription']['entity']
        payment_data = payload['payment']['entity']
        
        try:
            subscription = Subscription.objects.get(
                razorpay_subscription_id=subscription_data['id']
            )
            ss = subscription.user.id
            subscription.paid_count = subscription_data.get('paid_count', 0)
            subscription.remaining_count = subscription_data.get('remaining_count')
            subscription.save()


            Employee.objects.filter(id=ss).update(subscription="paid")
            
            # Create payment record
            Payment.objects.create(
                subscription=subscription,
                razorpay_payment_id=payment_data['id'],
                razorpay_order_id=payment_data.get('order_id'),
                amount=payment_data['amount'],
                currency=payment_data['currency'],
                status='captured',
                method=payment_data.get('method'),
                description='auto'
            )
        except Subscription.DoesNotExist:
            pass
    
    def _handle_subscription_cancelled(self, subscription_data):
        try:
            subscription = Subscription.objects.get(
                razorpay_subscription_id=subscription_data['id']
            )
            subscription.status = 'cancelled'
            subscription.save()
        except Subscription.DoesNotExist:
            pass
    
    def _handle_subscription_completed(self, subscription_data):
        try:
            subscription = Subscription.objects.get(
                razorpay_subscription_id=subscription_data['id']
            )
            subscription.status = 'completed'
            subscription.save()
        except Subscription.DoesNotExist:
            pass
    
    def _handle_subscription_halted(self, subscription_data):
        try:
            subscription = Subscription.objects.get(
                razorpay_subscription_id=subscription_data['id']
            )
            subscription.status = 'halted'
            subscription.save()
        except Subscription.DoesNotExist:
            pass
    
    def _handle_payment_captured(self, payment_data):
        try:
            payment = Payment.objects.get(razorpay_payment_id=payment_data['id'])

            payment.status = 'captured'
            payment.save()

            
        except Payment.DoesNotExist:
            pass
    
    def _handle_payment_failed(self, payment_data):
        try:
            payment = Payment.objects.get(razorpay_payment_id=payment_data['id'])
            payment.status = 'failed'
            payment.save()
        except Payment.DoesNotExist:
            pass





################################## Payment #################################


@authenticate_token
@api_view(['GET'])
def payment_all_filter(request):
    try:
        user_info = getattr(request, 'user_data', None)
        print(user_info)
        id = user_info["id"]
        if Employee.objects.filter(id=id).exists():
            # subs_id = list(Subscription.objects.filter(user_id=id).values_list('id', flat=True))
            emp_obj = Payment.objects.filter(subscription__user_id=id).order_by('-id')
            serializers = PaymentDetailSerializer(emp_obj, many=True).data
            return Response({"message":"Success", "status":200, "data":serializers})
        return Response({"message":"Invalid User", "status":404, "data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})



@authenticate_token
@api_view(['GET'])
def payment_all(request):
    try:
        user_info = getattr(request, 'user_data', None)
        print(user_info)
        id = user_info["id"]
        if Employee.objects.filter(id=id).exists():
            emp_obj = Payment.objects.all().order_by('-id')
            serializers = PaymentDetailSerializer(emp_obj, many=True).data
            return Response({"message":"Success", "status":200, "data":serializers})
        return Response({"message":"Invalid User", "status":404, "data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})




#### >>>>>>>>>>>>>>>>> ####x

def home(request, id, pid):
    plan_obj = Plan.objects.all()
    plan_objj = Plan.objects.filter(id=pid).first()
    context = {"plan":plan_obj, "uid":id, "ppid":pid, "plan_validity":plan_objj.validity, "amt":plan_objj.amount}
    print(context)
    return render(request, 'payment.html', context)


def create_order(request):
    if request.method == "POST":
        amount = int(request.POST.get("amount")) * 100  # in paisa
        name = request.POST.get("name")
        pid = request.POST.get("pid")
        uid = request.POST.get("uid")
        print("pid......",pid)
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

        plan_obj = Plan.objects.get(id=pid)
        end_at = datetime.now() + timedelta(days=plan_obj.validity)
        subs_obj = Subscription(user_id=uid, plan_id=pid, start_at=datetime.now(), end_at=end_at, next_charge_at=end_at)
        subs_obj.save()


        payment = Payment.objects.create(subscription_id=subs_obj.id, amount=amount / 100)

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        payment.razorpay_order_id = order["id"]

        payment.save()

        return JsonResponse({
            "order_id": order["id"],
            "key": RAZORPAY_KEY_ID,
            "amount": amount,
            "name": name,
        })



@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        order_id = data.get("razorpay_order_id")
        payment_id = data.get("razorpay_payment_id")
        signature  = data.get("razorpay_signature")

        payment = Payment.objects.get(razorpay_order_id=order_id)
        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.status = "captured"
        # payment.paid = True
        payment.save()

        Subscription.objects.filter(id=payment.subscription.id).update(status="active")

        plan_obj = payment.subscription.plan
        plan_days = plan_obj.validity
        plan_availableSecond = plan_obj.availableSecond
        plan_end = datetime.now() + timedelta(days=plan_days)

        if payment.subscription.user.subscription != "trial":
            subs_status = "renew"
        else:
            subs_status = "paid"

        Employee.objects.filter(id=payment.subscription.user.id).update(availableSecond=plan_availableSecond, selectedPlan=plan_obj, subscription=subs_status, startPlan=datetime.now(), endPlan=plan_end)


        return JsonResponse({
            "status": "success",
            "pid": payment_id
        })


def payment_detail(request, pid):
    pobj = Payment.objects.get(razorpay_payment_id=pid)
    context = {
        "payment_id": pobj.razorpay_payment_id,
        "order_id": pobj.razorpay_order_id,
        "amount": pobj.amount,                              
        "plan_name": pobj.subscription.plan.name,
        "validity_days": pobj.subscription.plan.validity
    }
    return render(request, "success.html", context)

def payment_cancel_detail(request, pid):
    pobj = Payment.objects.get(razorpay_order_id=pid)
    context = {
        "order_id": pobj.razorpay_order_id,
        "amount": pobj.amount,                              
        "plan_name": pobj.subscription.plan.name,
        "validity_days": pobj.subscription.plan.validity
    }
    return render(request, "failed.html", context)


@csrf_exempt
def payment_cancel(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")

        try:
            payment = Payment.objects.get(razorpay_order_id=order_id)
        except Payment.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid order id"})

        # Mark payment cancelled
        payment.status = "failed"
        payment.save()

        # Delete subscription created during order
        Subscription.objects.filter(id=payment.subscription.id).update(status="cancelled")

        return JsonResponse({"status": "cancelled", "order_id":payment.razorpay_order_id})



