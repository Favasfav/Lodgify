from django.urls import path 
from . import views
from . import utils

from .views import *
from rest_framework_simplejwt.views import (
   
    TokenRefreshView,
)

urlpatterns=[
    path('',views.getRoutes ),
    path('token/', UserLoginView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
      path('partnerlogin/', PartnerLoginView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('signup/',UserSignupAPI.as_view()),
     path('signup/otp/',utils.generate_otp_and_send_email),
     path('Partnersignup/',PartnerSignupAPI.as_view()),
    # path('user-login/', UserLoginView.as_view(), name='user-login'),
    path('adminlogin/', AdminLoginView.as_view(), name='admin-login'),
    path('userlist/', Userlist.as_view(), name='useliserlist'),
    path('userblock/<int:user_id>/', views.userblock, name='userblock'),
     path('profileupdate/<int:user_id>/', views.profileupdate, name='profileupdate'),
     path('userprofile/<int:user_id>/', views.userprofile, name='userprofile'),
     path('Partnerprofile/<int:user_id>/', views.Partnerprofile, name='Partnerprofile'),
      path('wallet/<int:user_id>/', Walletmoney.as_view(), name='wallet'),
    
    
    ]