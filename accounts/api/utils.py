import random
import smtplib
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view 
from accounts.api.serializers import EmailOTPSerializer
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

@api_view(['POST'])
def generate_otp_and_send_email(request):
    print("utilsssssssssss")
    if request.method == 'POST':
        print("utilsssssssssss")
        print("data",request.data)
        serializer = EmailOTPSerializer(data=request.data)
        print("serializer",serializer)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = str(random.randint(1000, 9999))

            try:
                message = f'Your OTP to verify your account is {otp}'
                send_mail(
                    'Welcome to Lodgify! Verify your account with your email',
                    message,
                    settings.EMAIL_HOST_USER,  
                    [email],
                    fail_silently=False
                )
                return Response({'otp': otp}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'Failed to send OTP email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# @api_view(['POST'])
# def generate_otp_and_send_email(request):
#     print("utilsssssssssss")
#     if request.method == 'POST':
#         print("utilsssssssssss")
#         print("data",request.data)
#         serializer = EmailOTPSerializer(data=request.data)
#         print("serializer",serializer)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             otp = str(random.randint(1000, 9999))

#             try:
#                 message = f'Your OTP to verify your account is {otp}'
#                 send_mail(
#                     'Welcome to Lodgify! Verify your account with your email',
#                     message,
#                     settings.EMAIL_HOST_USER,  
#                     [email],
#                     fail_silently=False
#                 )
#                 return Response( status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({'error': 'Failed to send OTP email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
