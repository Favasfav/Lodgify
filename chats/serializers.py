
from .models import *
from rest_framework.serializers  import ModelSerializer
from rest_framework import serializers
from channels.db import database_sync_to_async
class MessageSerializer(ModelSerializer):
    # sender_email = serializers.EmailField(source='sender.email')

    class Meta:
        model = Message
        fields = '__all__'
        depth=2