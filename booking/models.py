from django.db import models
from partner.models import *
from accounts.models import *
from django.db.models import Q
from django.db.models.functions import Now
from django.utils import timezone

class Booking(models.Model):
    room = models.ForeignKey(RoomProperty,related_name='room_bookings', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,related_name='user_bookings',on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room_qty_booked = models.PositiveIntegerField(default=1,blank=True,null=True)  
    total_amount=models.PositiveIntegerField(blank=True,null=True)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(check_in_date__gte=timezone.now()),
                name="check_in_date must be greater than or equal to today"
            )
        ]

# class Payment(models.Model):
#     booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
#     payment_method = models.CharField(max_length=50)
#     total_amount = models.DecimalField(max_digits=8, decimal_places=2)


class Transcation(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    partner = models.ForeignKey(PartnerProfile, on_delete=models.CASCADE)
    partner_share = models.DecimalField(max_digits=15, decimal_places=2)
    company_share = models.DecimalField(max_digits=15, decimal_places=2)
    
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, verbose_name="Payment ID", null=True, blank=True)
    order_id = models.CharField(max_length=100, verbose_name="Order ID", null=True, blank=True)
    signature = models.CharField(max_length=200, verbose_name="Signature", null=True, blank=True)

    def _str_(self):
        return str(self.id)
    
    class Meta:
        ordering = ['-transaction_date']


