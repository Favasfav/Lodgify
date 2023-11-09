from django.urls import path

from .views import *
urlpatterns=[


    path('mymessages/<int:user_id>/', MyIndex.as_view(), name='mymessages'), 
    path('get-messages/<sender_id>/<reciever_id>/',GetMessages.as_view(),name='get-messages'),
     path('sendmessages/',SendMessages.as_view(),name='sendmessages'),
]