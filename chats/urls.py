from django.urls import path

from .views import *
urlpatterns=[
path('getchatlist/<int:user_id>', Chatlist.as_view(), name='getchatlist'),
 
]