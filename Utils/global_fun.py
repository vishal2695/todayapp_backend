
import random  # Import random module

def generate_otp(): # Define the function with the parameter ‘length’
    length=4
    otp = ""
    for _ in range(length): # Use for loop 
        otp += str(random.randint(0, 9)) # 
    return otp




################################################### Authorization #############################################

from cryptography.fernet import Fernet
import base64
import os, sys
from pathlib import Path
import json

from rest_framework.response import Response
from django.http import JsonResponse
from functools import wraps

from today import settings
from Employee.models import *


key = settings.SECRET_KEY
cipher_suite = Fernet(key)

def encrypt_token(data):
    data = json.dumps(data)
    print("enctrupt...",data)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return base64.b64encode(encrypted_data).decode()


def decrypt_token(encrypted_data):
    try:
        str_token = encrypted_data
        print(str_token)
        encrypted_data = base64.b64decode(encrypted_data)
        print("vvv",encrypted_data)
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        print("sss",decrypted_data)
        data = json.loads(decrypted_data.decode())
        print("data decrpit", data, type(data))
        status = None
        if "id" in data:
            if Employee.objects.filter(id=data["id"], activeStatus=True, accountStatus=True, accessToken=str_token).exists():
                status = data
        return status
    except Exception as e:
        return None



def authenticate_custom_token(requestt):
    if 'HTTP_AUTHORIZATION' in requestt.META:
        auth_header = requestt.META['HTTP_AUTHORIZATION']
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            bearer_token = parts[1]
            authenticated = decrypt_token(bearer_token)
            if authenticated:  # Assume this returns None or dict
                requestt.user_data = authenticated
                return 200
        else:
            authenticated = 401
    else:
        authenticated = 401
    return authenticated


def authenticate_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        authenticated = authenticate_custom_token(request)
        if authenticated == 200:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({"message": "Unauthorized", "status":401, "data":[]})
    return _wrapped_view




