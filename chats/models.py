from django.db import models
from accounts.models import CustomUser
# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,related_name="sender_message_set")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,related_name="reciever_message_set")
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    # class Meta:
    #     ordering=["-id"]
    def __str__(self):
        return f"{ {self.thread_name}}"