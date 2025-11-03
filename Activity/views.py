from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Employee.models import *
from Employee.serializers import EmployeeSerializer
from .models import *
from .serializers import ActivitySerializer, TopicSerializer
from Utils.global_fun import *
from datetime import datetime
# Create your views here.


from django.utils import timezone
# import datetime

# If you have a naive datetime like this:




@authenticate_token
@api_view(['POST'])
def create(request):
    try:
        user_info = getattr(request, 'user_data', None)
        print(user_info)
        emp_id = user_info["id"]
        json_data = request.data
        if int(json_data["status"]) == 0:
            date_time = datetime.fromtimestamp(request.data.get('timeStamp'))
            naive_dt = date_time

            # Convert it to an aware datetime
            aware_dt = timezone.make_aware(naive_dt)
            empp = Employee.objects.filter(id=emp_id).first()
            empp.lastLogin=aware_dt
            empp.save()
            print("sasas",empp, empp.lastLogin, empp.createdAt, empp.updatedAt)
            date_obj = date_time.date()
            date_time = datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S")
            print(date_time)
            if Activity.objects.filter(empId_id=emp_id, status=0).exists():
                act_pre = Activity.objects.filter(empId_id=emp_id, status=0)
                for pre in act_pre:
                    dt_str1 = date_time
                    dt_str2 = pre.startTimeStamp

                    # Convert to datetime objects
                    dt1 = datetime.strptime(dt_str1, "%Y-%m-%d %H:%M:%S")
                    dt2 = datetime.strptime(dt_str2, "%Y-%m-%d %H:%M:%S")

                    # Get the difference in seconds
                    diff_seconds = abs((dt1 - dt2).total_seconds())
                    Activity.objects.filter(id=pre.id).update(status=1, closeTimeStamp=date_time, totalSecond=diff_seconds)

            json_data["empId"]          = emp_id
            # json_data["startDate"]      = datetime.strftime(date_time, "%Y-%m-%d")
            json_data["startDate"]      = date_obj
            json_data["startTimeStamp"] = date_time
            print("json_data", json_data)
            act_ser = ActivitySerializer(data=json_data)
            if act_ser.is_valid():
                act_ser.save()
                return Response({"message":"Success", "status":200, "data":[]})
            else:
                return Response({"message":"Unsuccess", "status":404, "data":[]})
        elif int(json_data["status"]) == 1:
            if Activity.objects.filter(empId_id=emp_id, status=0).exists():
                act_obj = Activity.objects.filter(empId_id=emp_id, status=0).order_by('-id')
                for aobj in act_obj:
                    date_time = datetime.fromtimestamp(request.data.get('timeStamp'))
                    date_time = datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S")

                    dt_str1 = date_time
                    dt_str2 = aobj.startTimeStamp

                    # Convert to datetime objects
                    dt1 = datetime.strptime(dt_str1, "%Y-%m-%d %H:%M:%S")
                    dt2 = datetime.strptime(dt_str2, "%Y-%m-%d %H:%M:%S")

                    # Get the difference in seconds
                    diff_seconds = abs((dt1 - dt2).total_seconds())
                    Activity.objects.filter(id=aobj.id).update(status=1, closeTimeStamp=date_time, totalSecond=diff_seconds)

            return Response({"message":"Success", "status":200, "data":[]})
        # return Response({"message":"Unsuccess", "status":404, "data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})




@authenticate_token
@api_view(['POST'])
def create_topic(request):
    try:
        user_info = getattr(request, 'user_data', None)
        print(user_info)
        emp_id = user_info["id"]
        json_data = request.data
        json_data["empId"] = emp_id
        act_ser = TopicSerializer(data=json_data)
        if act_ser.is_valid():
            act_ser.save()
            return Response({"message":"Success", "status":200, "data":[]})
        return Response({"message":"Unsuccess", "status":404, "data":[]})
    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})




@authenticate_token
@api_view(['GET'])
def topic_all_filter(request):
    try:
        user_info = getattr(request, 'user_data', None)
        print(user_info)
        emp_id = user_info["id"]
        act_topic = Topic.objects.filter(empId=emp_id).order_by('-id')
        act_ser   = TopicSerializer(act_topic, many=True).data
        
        return Response({"message":"Success", "status":200, "data":act_ser})
    except Exception as e:
        return Response({"message":str(e), "status":500, "data":[]})
    



    