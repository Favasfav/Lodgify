from django.urls import path

from .views import *
urlpatterns=[
#  path('Addproperty/', Addproperty.as_view(), name='Addproperty'),
 path('checkroomavailblity/<int:propertyId>/<str:checkindate>/<str:checkoutdate>/<str:roomqty>', Checkroomavailblity.as_view(), name='checkroomavailblity'), 
     path('roombooking/<int:propertyId>/<str:checkindate>/<str:checkoutdate>/<int:roomqty>/<int:user_id>', Roombooking.as_view(), name='checkroomavailblity'), 

]