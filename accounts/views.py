# views.py
from django.shortcuts import render
from .task import sendmail_func
from django.http import HttpResponse
from rest_framework.decorators import api_view 
from rest_framework import status
from rest_framework.response import Response
from accounts.api.serializers import *
from accounts.models import UserProfile,PartnerProfile,CustomUser,Wallet

from datetime import datetime,timedelta

def test(request,user_id,checkoutdate):
    
          
            data=request.data
            print("user",data,"kkkkkkk",checkoutdate)
            user=CustomUser.objects.get(id=user_id)
            user_email1=user.email
            li_user=user_email1.split("-")
            user_email=li_user[1]
            print(user_email)
             
            checkoutdate_str = datetime.strptime( checkoutdate, "%Y-%m-%d").date()

            date_object = datetime.combine(checkoutdate_str, datetime.min.time())
            print("date_object",date_object)
            current_datetime = datetime.now()
            sendmail_func.apply_async(args=[user_email],eta=current_datetime )  # date_object or 
            countdown=20 #we can make for check out date email send for asking review

            # return HttpResponse("Done")
