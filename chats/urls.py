from django.urls import path

from .views import *
urlpatterns=[
path('getchatlist/<int:user_id>', Chatlist.as_view(), name='getchatlist'),
path('getchatlistpartner/<int:user_id>', Chatlistpartner.as_view(), name='getchatlistpartner'),
path('previous_message/<int:currentUserId>/<int:otherUserId>', Previouschat.as_view(), name='previous_message'),
path('fetch_userobj/<int:otherUserId1>', Fetch_userobj.as_view(), name='previous_message'),
 
]