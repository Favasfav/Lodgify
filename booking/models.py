from django.db import models
from partner.models import *
from accounts.models import *


class Booking(models.Model):
    room = models.ForeignKey(RoomProperty, on_delete=models.CASCADE)
    guest_name = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)





