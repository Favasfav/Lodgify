# task.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def sendmail_func(user_email):
    for i in range(10):
        print(i)
    
    print("email--------", user_email)
    
    send_mail(
        "Hello Thanks for choosing Lodgify Please Rate Us",
        "Your email body goes here",  # Add your email body/message
        settings.DEFAULT_FROM_EMAIL,
        [user_email],  # Add the recipient list as a list
        fail_silently=True
    )
    
    return 'Done'
