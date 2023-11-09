from django.contrib import admin
from .models import *

# Register your models here.

class ChatMessageAdmin(admin.ModelAdmin):
    list_editable=['is_read']
    list_display=['sender','reciever','message','is_read']
admin.site.register(ChatMessage,ChatMessageAdmin)