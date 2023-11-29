from django.contrib import admin

# Register your models here.
from .models import RoomProperty,RoomCategory,RoomAmenity,RoomPhoto,Blockbooking
admin.site.register(RoomCategory)
admin.site.register(RoomAmenity)
admin.site.register(RoomPhoto)
admin.site.register(RoomProperty)
admin.site.register(Blockbooking)