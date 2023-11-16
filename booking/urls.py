from django.urls import path

from .views import *
urlpatterns=[
path('cancelbooking/', CancelOrder.as_view(), name='cancelbooking'),
 path('checkroomavailblity/<int:propertyId>/<str:checkindate>/<str:checkoutdate>/<str:roomqty>', Checkroomavailblity.as_view(), name='checkroomavailblity'), 

path('bookinglist/<int:user_id>/', Bookinglist.as_view(), name='bookinglist'), 
 path('cancelbooking/', CancelOrder.as_view(), name='cancelbooking'),
 path('bookinglistall/',Bookingall.as_view(),name='bookinglistall'),
  path('totalreveniue/',Totalrevenue.as_view(),name='totalreveniue')
]