from django.contrib import admin
from .models import UserProfile,PartnerProfile,CustomUser,Wallet
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(PartnerProfile)
admin.site.register(CustomUser)
admin.site.register(Wallet)