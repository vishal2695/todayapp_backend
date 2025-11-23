from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse, JsonResponse
from .forms import *
from .models import *
from Employee.models import *
from Subscription.models import *
from Activity.models import *
from Employee.serializers import EmployeeSerializer
from Subscription.serializers import *
from Activity.serializers import *
from django.conf import settings


##########################>>>>>>>>>>@<<<<<<<<<###############################

def session_required(view_func):
    def wrapper(request, *args, **kwargs):
        if "session_id" in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("/")  # or render index.html directly
    return wrapper

def web_login(request):
    if request.method == 'POST':
        email = request.POST["Email"]
        password = request.POST["Password"]
        if WebUser.objects.filter(Email=email, Password=password).exists():
            user = WebUser.objects.filter(Email=email, Password=password).first()
            request.session["session_id"] = user.id
            return JsonResponse({'message': 'success'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid Credentials'}, status=404)
    elif "session_id" in request.session:
        return redirect('/dashboard')
    else:
        return render(request, 'index.html')



@session_required
def web_home(request):
    print(request.session.get("session_id"))
    emp_data = Employee.objects.all().count()
    act_data = Activity.objects.all()
    pay_data = Payment.objects.filter(status="captured")
    print("pay_data")
    total_time = sum(act.totalSecond for act in act_data)
    total_amount = sum(pay.amount for pay in pay_data)
    user_list = Employee.objects.all().order_by('id')
    context = {
        "user_count" :emp_data,
        "total_time" :round(total_time/3600,2),
        "user_list":user_list,
        "total_amount":total_amount

    }
    return render(request, 'home.html', context)



from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from datetime import date, timedelta


@session_required
@csrf_exempt
def web_user_detail(request):
    id = request.POST["id"]
    emp_data = Employee.objects.filter(id=id)
    data = []
    for emp in emp_data:
        ser = EmployeeSerializer(emp).data
        print(emp.userName,"new",emp.userName.split(' '))
        shortName = "N/A"
        userName  = "N/A"
        if emp.userName != "":
            userName = emp.userName
            name = emp.userName.split(' ') 
            if len(name)>1:
                shortName = name[0][:1] + name[-1][:1]
            elif len(name) == 1:
                shortName = name[0][:1]
            else:
                shortName = "N/A"

        ser["shortName"] = shortName
        ser["userName"]  = userName
    
        act_data    = Activity.objects.filter(empId=id)
        total_time  = sum(act.totalSecond for act in act_data)

        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        week_dates = [start_of_week + timedelta(days=i) for i in range(7)]  # Mon to Sun

        # 2. Run raw SQL query to get existing data
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DATE(startDate) as start_date, id
                FROM Activity_activity
                WHERE empId_id = %s AND DATE(startDate) BETWEEN %s AND %s
            """, [id, week_dates[0], week_dates[-1]])
            rows = cursor.fetchall()  # [(2025-06-10, 12), (2025-06-11, 15), ...]

        # 3. Convert query result into a dictionary
        activity_map = {row[0]: row[1] for row in rows}  # {date: id}

        # 4. Merge with 7-day week to get nulls for missing days
        final_data = []
        for d in week_dates:
            final_data.append({
                "date": d,
                "activity_id": activity_map.get(d)  # will be None if not found
            })

        # 5. Print or use final_data
        act_final = []
        act_time_list = []
        cal_time = 0
        for item in final_data:
            print(item)
            act_data_obj = Activity.objects.filter(startDate=item["date"], empId=id)
            all_act_ser  = json.loads(json.dumps(ActivitySerializer(act_data_obj, many=True).data))
            total_time  = round(sum(act.totalSecond for act in act_data_obj)/3600, 2)
            act_time_list.append(total_time)
            starttime = ""
            endtime   = ""
            if act_data_obj:
                start_obj = act_data_obj
                start_obj = start_obj.first()
                starttime = start_obj.startTimeStamp
                end_obj   = act_data_obj.last()
                endtime   = end_obj.closeTimeStamp
            obj = {}
            print("ite date", type(item["date"]), item["date"])
            obj["activity_date"] = item["date"]
            obj["start_time"]    = starttime
            obj["end_time"]      = endtime
            obj["total_time"]    = total_time
            obj["all_activity_list"] = all_act_ser
            act_final.append(obj)
            cal_time += total_time
        
        week_activity        = []
        ser["week_activity"] = week_activity

        ser["activity_data"] = act_final
        ser["activity_time_list"] = act_time_list
        ser["calculated_time"] = cal_time
        pay_data = []
        payment_detail = Payment.objects.filter(subscription__user__id=id)
        print(payment_detail)
        for pay in payment_detail:
            payment_serializer = PaymentDetailSerializer(pay).data
            print(payment_serializer)
            payment_serializer["subscribe_detail"] = SubscriptionDetailSerializer(pay.subscription).data
            pay_data.append(payment_serializer)

        ser["payment_detail"] = pay_data
        data.append(ser)

    return JsonResponse({'message': 'success', "data":data}, status=200)


@session_required
def web_logout(request):
    if "session_id" in request.session:
        del request.session["session_id"]
    return redirect('/')

# def web_reset_password(request):
#     print(request.POST["email"])
#     return JsonResponse({'message': 'success', "data":[]}, status=200)

from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def web_reset_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')

        try:
            user = WebUser.objects.get(Email=email)
            import random

            random_number_str = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            print(random_number_str)

            user.Password = random_number_str

            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Your Gmail credentials
            GMAIL_USER = settings.GMAIL_USER
            GMAIL_APP_PASSWORD = settings.GMAIL_APP_PASSWORD  # 16-character app password (no spaces)

            # Email details
            to_email = 'honeybeeofficial2020@gmail.com'
            subject = 'Today App password reset'
            body = f'Your New Password is {random_number_str}'

            # Create the email message
            message = MIMEMultipart()
            message['From'] = GMAIL_USER
            message['To'] = to_email
            message['Subject'] = subject

            # Add plain text body
            message.attach(MIMEText(body, 'plain'))

            try:
                # Connect to Gmail's SMTP server
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()  # Secure the connection
                server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
                server.sendmail(GMAIL_USER, to_email, message.as_string())
                server.quit()
                user.save()

                print("✅ Email sent successfully.")
            except Exception as e:
                print("❌ Failed to send email:", str(e))



            return JsonResponse({"message": "Password reset link has been sent to your email."})
        except WebUser.DoesNotExist:
            return JsonResponse({"message": "No account with this email."}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def web_payment_detail(request):
    try:
        id = request.POST["id"]
        pay_data = []
        payment_detail = Payment.objects.filter(id=id)
        for pay in payment_detail:
            payment_serializer = PaymentDetailSerializer(pay).data
            print(payment_serializer)
            payment_serializer["subscribe_detail"] = SubscriptionDetailSerializer(pay.subscription).data

            payment_serializer["plan_detail"] = PlanDetailSerializer(pay.subscription.plan).data

            pay_data.append(payment_serializer)
        return JsonResponse({"message":"Success", "status":200, "data":pay_data})
    except Exception as e:
        return JsonResponse({"message":str(e), "status":500, "data":[]})




@csrf_exempt
def web_topic_list(request):
    try:
        id = request.POST["id"]
        topic = Topic.objects.filter(empId=id).order_by('-id')
        topic_ser = TopicSerializer(topic, many=True).data
        return JsonResponse({"message":"Success", "status":200, "data":topic_ser})
    except Exception as e:
        return JsonResponse({"message":str(e), "status":500, "data":[]})


from django.db.models import Count, Sum

@csrf_exempt
def web_all_activity_list(request):
    try:
        id = request.POST["id"]
        act_data_obj = (
            Activity.objects.filter(empId=id)
            .values("startDate")
            .annotate(
                total=Count("id"),                 # how many activities
                total_seconds=Sum("totalSecond")   # sum of totalSecond
            )
        )
        print("web all activity list......")
        print(list(act_data_obj))
        return JsonResponse({"message":"Success", "status":200, "data":list(act_data_obj)})
    except Exception as e:
        return JsonResponse({"message":str(e), "status":500, "data":[]})

