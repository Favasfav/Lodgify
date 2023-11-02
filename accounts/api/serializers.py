from rest_framework import serializers

from rest_framework.serializers import ModelSerializer, ValidationError, ImageField
# from base.models import Note
# from django.contrib.auth.models import User
from accounts.models import UserProfile,PartnerProfile,CustomUser

from partner.models import RoomProperty,RoomCategory, RoomAmenity, RoomPhoto

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        model = CustomUser

 


class SignupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ('email','username','phone_no','password')
        extra_kwargs = {
            'password':{'write_only':True}
        }


class EmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        depth=1
       

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'  # Use '*' to include all fields from the model
        depth = 1

class PartnerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerProfile
        fields = '__all__'  # Use '*' to include all fields from the model
        depth = 1        
class profileupdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = '__all__'  # Use '*' to include all fields from the model
        depth = 1        

