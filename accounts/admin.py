from django.contrib import admin
from .models import UserProfile,PartnerProfile,CustomUser
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(PartnerProfile)
admin.site.register(CustomUser)