from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from Subscription.models import *
from Subscription.serializers import *
from .serializers import *
from Utils.global_fun import *
from django.conf import settings
from twilio.rest import Client
from datetime import datetime
from django.utils import timezone
# Create your views here.


# @api_view(['GET'])
def send_msg(otp, mobile, code):
    try:
        account_sid = settings.ACCOUNT_SID
        auth_token = settings.AUTH_TOKEN
        twilio_number = settings.TWILIO_NUMBER  # Your Twilio number

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f'{otp} is your verification code for Today',
            from_=twilio_number,
            to=code+mobile  # Receiver's phone number
            # to='+17815488932'  # Receiver's phone number
        )
        if message.sid:
            print(f'Message sent! SID: {message.sid}')
            return 200
        else:
            return 400
    except Exception as e:
        return 500


@api_view(['GET'])
def get_items(request):
    data = {
        'items': ['Item 1', 'Item 2', 'Item 3']
    }
    return Response(data)



@api_view(['POST'])
def login_or_signup(request):
    try:
        req = request.data
        print(req)
        UType = str(req["userType"]).lower()
        if UType == "email":
            email = req['email']
            if email != "":
                if not Employee.objects.filter(email=email).exists():
                    ser = EmployeeSerializer(data=request.data)
                    if ser.is_valid():
                        obj = ser.save()
                    else:
                        return Response({"message":str(ser.errors), "status":404, "data":[]})
                else:
                    obj = Employee.objects.filter(email=email, userType=UType).first()
                    obj.lastLogin = datetime.now()
                    print("timing....",datetime.now())
                print("final daataa", obj)
                token_data = {"id":obj.id}
                token = encrypt_token(token_data)
                print("token..", token)

                obj.accessToken = token
                obj.activeStatus = True
                obj.accountStatus = True
                obj.save()

                context = {"token":token}
                return Response({"message":"Success", "status":200, "data":[context]})
            else:
                return Response({"message":"Invalid Email", "status":404, "data":[]})
        elif UType == "phone":
            phone = req['phone']
            countryCode = req['countryCode']
            if phone != "":
                otp = generate_otp()
                # otp   = "1234"
                # msg = send_msg(otp, phone, countryCode)
                msg = 200
                print("msg...",msg)
                if msg == 200:
                    if OTP.objects.filter(phone=phone).exists():
                        OTP.objects.filter(phone=phone).update(otp=otp, status=0)
                    else:
                        OTP(otp=otp, phone=phone, countryCode=countryCode).save()
                    
                    return Response({"message":"OTP send to your number", "status":200, "data":[{"OTP":otp}]})
                else:
                    return Response({"message":"Invalid Phone Number", "status":404, "data":[]})
            else:
                return Response({"message":"Invalid Phone Number", "status":404, "data":[]})
        else:
            return Response({"message":"Unsuccess", "status":404, "data":[]})    
    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})


@api_view(['POST'])
def otpVerify(request):
    try:
        otp = request.data["otp"]
        phone = request.data["phone"]
        countryCode = request.data["countryCode"]
        if OTP.objects.filter(otp=otp, phone=phone, status=False):
            OTP.objects.filter(otp=otp, phone=phone, status=False).update(status=True)
            if Employee.objects.filter(phone=phone, accountStatus=True).exists():
                obj = Employee.objects.filter(phone=phone, accountStatus=True).first()
                msg = "User login successfully"
                obj.lastLogin = datetime.now()
            else:
                # emp_obj = Employee(phone=phone, userType='phone')
                # emp_obj.save()
                data = {
                    "userType":"phone",
                    "phone":phone,
                    "countryCode":countryCode
                }

                ser = EmployeeSerializer(data=data)
                if ser.is_valid():
                    obj = ser.save()
                    print("objjj", obj)
                    msg = "User created successfully"
                else:
                    return Response({"message":str(ser.errors), "status":404, "data":[]})
            print("final daataa", obj)
            token_data = {"id":obj.id}
            token = encrypt_token(token_data)
            obj.accessToken = token
            obj.activeStatus = True
            obj.accountStatus = True
            obj.save()

            context = {"token":token}
            return Response({"message":msg, "status":200, "data":[context]})
        else:
            return Response({"message":"Wrong OTP", "status":404, "data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})


@authenticate_token
@api_view(['GET'])
def one(request):
    try:
        user_info = getattr(request, 'user_data', None)
        print(user_info)
        id = user_info["id"]
        emp_obj = Employee.objects.filter(id=id).first()

        data = []
        utc_dt = emp_obj.endPlan
        native_dt = timezone.localtime(utc_dt).replace(tzinfo=None)
        tt = native_dt < datetime.now()
        if tt and emp_obj.subscription != "expire":
            emp_obj.subscription = "expire"
            emp_obj.save()

        serializers = EmployeeDetailSerializer(emp_obj).data
        subs_data = []
        if emp_obj.selectedPlan:
            subs_data = UserSelectedPlanSerializer(emp_obj.selectedPlan).data
        serializers["selectedPlan_detail"] = [subs_data]
        
        data.append(serializers)

            # if str(emp.subscription).lower() in ["paid","cancelled"]:
            #     subs = Subscription.objects.filter(user=id).order_by('-id').first()
            #     subs_ser = SubscriptionProfileDetailSerializer(subs).data
            #     subs_data.append(subs_ser)
            # else:
            #     subs_ser = SubscriptionProfileDetailSerializer().data
            #     subs_ser["start_at"] = emp.createdAt
            #     # subs_ser["end_at"]   = (emp.createdAt+15)
            #     subs_data.append(subs_ser)
            # serializers["subscription_detail"] = subs_data
            # data.append(serializers)
        return Response({"message":"Success", "status":200, "data":data})
    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})

@authenticate_token
@api_view(['POST'])
def update(request):
    try:
        # id = request.data["id"]
        user_info = getattr(request, 'user_data', None)
        print(user_info)
        id = user_info["id"]
        if Employee.objects.filter(id=id).exists():
            emp_obj = Employee.objects.filter(id=id).first()
            if emp_obj.userType == "email":
                if 'email' in request.data:
                    request.data.pop('email')
                else:
                    request.data.pop('phone')
            serializers = EmployeeDetailSerializer(emp_obj, data=request.data, partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response({"message":"Success", "status":200, "data":[]})
            else:
                return Response({"message":str(serializers.errors), "status":404, "data":[]})
        else:
            return Response({"message":"Unsuccess", "status":404, "data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})




import os
from django.core.files.storage import FileSystemStorage 

# @authenticate_token
# @api_view(['POST'])
# def profile_upload(request):
#     try:
#         user_info = getattr(request, 'user_data', None)
#         id = user_info["id"]
#         if Employee.objects.filter(id=id).exists():
#             File = request.data['image']
#             attachmentsImage_url = ""
#             if File !="" :
#                 target ='./static/image/profileImages'
#                 os.makedirs(target, exist_ok=True)
#                 fss = FileSystemStorage()
#                 file = fss.save(target+"/"+File.name, File)
#                 productImage_url = fss.url(file)
#                 attachmentsImage_url = productImage_url.replace('/today/', '/') 

#                 print("attachmentsImage_url", attachmentsImage_url)
#             Employee.objects.filter(id=id).update(profile_image=attachmentsImage_url)
#             # serializers = EmployeeSerializer(emp_obj, many=True).data
#             return Response({"message":"Success", "status":200, "data":[{"Image_url":settings.BASE_URL+attachmentsImage_url}]})
#         else:
#             return Response({"message":"Unsuccess", "status":404, "data":[]})
#     except Exception as e:
#         return Response({"message":str(e), "status":500, "data":[]})




@api_view(['POST'])
def image_upload(request):
    try:
        File = request.data['image']
        attachmentsImage_url = ""
        if File !="" :
            target ='./static/image'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/today/', '/') 

        return Response({"message":"Success", "status":200, "data":[{"Image_url":settings.BASE_URL+attachmentsImage_url}]})
    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})



@authenticate_token
@api_view(['POST'])
def deactivate(request):
    try:
        user_info = getattr(request, 'user_data', None)
        id = user_info["id"]
        if Employee.objects.filter(id=id).exists():
            Employee.objects.filter(id=id).update(accountStatus=False)

            return Response({"message":"Your Account has been deleted successfully.", "status":200, "data":[]})
        else:
            return Response({"message":"Unsuccess", "status":404, "data":[]})

    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})

import os

# @authenticate_token
# @api_view(['POST'])
# def image_remove(request):
#     try:
#         user_info = getattr(request, 'user_data', None)
#         id = user_info["id"]
#         if Employee.objects.filter(id=id).exists():
#             url = request.data["url"]
#             url = Employee.objects.filter(id=id).first()
#             file_path = url.profile_image[1:]
#             print(file_path)
#             print(os.path.exists(file_path))
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#                 print("File removed successfully")
#             else:
#                 print("File not found")
#             Employee.objects.filter(id=id).update(profile_image="")

#             return Response({"message":"Image removed successfully.", "status":200, "data":[]})
#         else:
#             return Response({"message":"Unsuccess", "status":404, "data":[]})
#     except Exception as e:
#         return Response({"message":str(e), "status":500, "data":[]})



@api_view(['POST'])
def image_remove(request):
    try:
        url = request.data["url"]
        base_url = settings.BASE_URL
        file_path = url.replace(base_url, '/var/www/today')
        if os.path.exists(file_path):
            os.remove(file_path)
            print("File removed successfully")
            return Response({"message":"Image removed successfully.", "status":200, "data":[]})
        else:
            print("File not found")
            return Response({"message":"File not found.", "status":404, "data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})




@authenticate_token
@api_view(['POST'])
def valid_user_access(request):
    try:
        user_info = getattr(request, 'user_data', None)
        print(user_info)
        id = user_info["id"]
        if Employee.objects.filter(id=id).exists():
            use_time = request.data["seconds"]
            emp_obj = Employee.objects.get(id=id)
            utc_dt = emp_obj.endPlan
            native_dt = timezone.localtime(utc_dt).replace(tzinfo=None)
            print(native_dt)
            print(datetime.now())

            tt = native_dt > datetime.now()
            if tt and emp_obj.subscription != "expire":
                if int(emp_obj.availableSecond) >= int(use_time):
                    seconds_left = emp_obj.availableSecond - int(use_time)
                    emp_obj.availableSecond = seconds_left
                    if seconds_left == 0:
                        emp_obj.subscription = "expire"
                    emp_obj.save()

                    return Response({"message":"Success", "status":200, "data":[]})
                else:
                    return Response({"message":"Access Denied", "status":404, "data":[]})
            else:
                return Response({"message":"Subscription Expired!", "status":404, "data":[]})
        return Response({"message":"Invalid User", "status":404, "data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})
