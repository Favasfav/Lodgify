from rest_framework import serializers

from accounts.models import *
from accounts.api.serializers import *
from .models import *

class MessageSerializer(serializers.ModelSerializer):  
    receiver = PartnerModelSerializer(read_only=True)
    sender = UserModelSerializer(read_only=True)
    print("gggg")

    class Meta:
        model = ChatMessage
        fields = '__all__'
        depth = 2
