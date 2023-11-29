# accounts/urls.py
from django.urls import path
from .views import test  # Make sure to adjust this import based on your actual views structure

urlpatterns = [
    path('test/<int:user_id>/<str:checkoutdate>/', test, name='test'),
    # other URL patterns for the accounts app
]
