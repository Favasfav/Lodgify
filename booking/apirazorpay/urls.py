from django.urls import path
from .api_razorpay import *



urlpatterns=[
    path("order/compleate/<int:propertyId>/<str:checkindate>/<str:checkoutdate>/<int:roomqty>/<int:user_id>",TranscationAPIView.as_view(),name="create-order-api"),
    path("order/create/<int:propertyId>/<str:checkindate>/<str:checkoutdate>/<int:roomqty>/<int:user_id>",CreateOrderAPIView.as_view(),name="compleate-order-api"),

    
]