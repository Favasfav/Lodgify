
from rest_framework import serializers

from rest_framework.serializers import ModelSerializer, ValidationError, ImageField
from partner.models import *
from accounts.api.serializers import PartnerModelSerializer



class RoomPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPhoto
        fields = '__all__'

class RoomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCategory
        fields = '__all__'

class RoomAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAmenity
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    photos = RoomPhotoSerializer(many=True, read_only=True)
    category = RoomCategorySerializer(many=True, read_only=True)
    amenities = RoomAmenitySerializer(many=True, read_only=True)
    partner_name = serializers.CharField(source='partner.user.username',read_only=True)

    class Meta:
        model = RoomProperty
        fields = '__all__'
        # depth=2
