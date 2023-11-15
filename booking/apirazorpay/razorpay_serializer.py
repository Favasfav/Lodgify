from rest_framework import serializers
from django.db import models
from booking.models import *
class CreateOrderSerializer(serializers.Serializer):
    amount=serializers.IntegerField()
    currency=serializers.CharField()

class TranscationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transcation
        fields='__all__'

class TransactioncharcheckSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transcation
        fields=['signature','order_id','payment_id']        
        