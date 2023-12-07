from django.urls import path

from .views import *
urlpatterns=[
path('cancelbooking/', CancelOrder.as_view(), name='cancelbooking'),
 path('checkroomavailblity/<int:propertyId>/<str:checkindate>/<str:checkoutdate>/<str:roomqty>', Checkroomavailblity.as_view(), name='checkroomavailblity'), 

path('bookinglist/<int:user_id>/', Bookinglist.as_view(), name='bookinglist'), 
 path('cancelbooking/', CancelOrder.as_view(), name='cancelbooking'),
 path('bookinglistall/',Bookingall.as_view(),name='bookinglistall'),
  path('totalreveniue/',Totalrevenue.as_view(),name='totalreveniue'),
   path('get_revenue_amount/<int:partner_id>/', GetpartnerRevenue.as_view(), name='get_revenue_amount'),
   path('bookinglatest/<int:user_id>/', Bookinglatest.as_view(), name='bookinglatest'), 
   path('gettotalnobooking/<int:user_id>/', Bookingtotalno.as_view(), name='gettotalnobooking'),
   path('blockproperty/<int:property_id>/', Blockproperty.as_view(), name='gettotalnobooking'),
   path('latestsale/',Bookinglistlatest.as_view(),name='latestsale'),
   path('salesreport/',Bookingreport.as_view(),name='latestsale'),
]